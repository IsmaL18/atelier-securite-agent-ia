"""
Core agent implementation using LangGraph.

This module contains the main agent logic that orchestrates between
the LLM and MCP tools using LangGraph for state management.
"""

import json
from typing import Annotated, Any, TypedDict

from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages

from src.conference_agent.agent.prompts import get_system_prompt
from src.conference_agent.llm.client import LLMClient
from src.conference_agent.logging import logger
from src.conference_agent.mcp.client import MCPClients


class AgentState(TypedDict):
    """
    State for the agent graph.
    
    Tracks conversation messages and execution metadata.
    """
    messages: Annotated[list[dict[str, Any]], add_messages]
    tool_calls_made: int
    max_iterations: int


class ConferenceAgent:
    """
    Conference management agent using LangGraph.
    
    This agent helps manage conference communications and can be exploited
    for security awareness training (intentionally vulnerable).
    """
    
    def __init__(
        self,
        llm_client: LLMClient,
        mcp_clients: MCPClients,
        max_iterations: int = 10,
    ):
        """
        Initialize the conference agent.
        
        Args:
            llm_client: LLM client for reasoning
            mcp_clients: MCP clients for tool access
            max_iterations: Maximum number of reasoning iterations
        """
        self.llm_client = llm_client
        self.mcp_clients = mcp_clients
        self.max_iterations = max_iterations
        self.tools: list[dict[str, Any]] = []
        
        # Build the agent graph
        self.graph = self._build_graph()
        
        logger.info("ConferenceAgent initialized")
    
    async def initialize(self) -> None:
        """
        Initialize the agent by loading available tools.
        
        Must be called before using the agent.
        """
        # Load all available tools from MCP clients
        self.tools = await self.mcp_clients.list_all_tools()
        logger.info(f"Loaded {len(self.tools)} tools")
        
        for tool in self.tools:
            logger.debug(f"  - {tool['name']}: {tool['description']}")
    
    def _build_graph(self) -> StateGraph:
        """
        Build the LangGraph state graph for the agent.
        
        Returns:
            Compiled state graph
        """
        # Create graph
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("llm", self._llm_node)
        workflow.add_node("tools", self._tools_node)
        
        # Define edges
        workflow.set_entry_point("llm")
        workflow.add_conditional_edges(
            "llm",
            self._should_continue,
            {
                "continue": "tools",
                "end": END,
            },
        )
        workflow.add_edge("tools", "llm")
        
        return workflow.compile()
    
    async def _llm_node(self, state: AgentState) -> dict[str, Any]:
        """
        LLM reasoning node.
        
        Args:
            state: Current agent state
            
        Returns:
            Updated state with LLM response
        """
        messages = state["messages"]
        
        # Ensure system message is present
        if not messages or messages[0].type != "system":
            messages = [
                {"role": "system", "content": get_system_prompt()},
                *messages,
            ]
        
        # Call LLM with available tools
        response = await self.llm_client.call(
            messages=messages,
            tools=self.tools if self.tools else None,
            tool_choice="auto",
        )
        
        # Add LLM response to messages
        new_message = {
            "role": response["role"],
            "content": response.get("content", ""),
        }
        
        # Add tool calls if present
        if "tool_calls" in response:
            new_message["tool_calls"] = response["tool_calls"]
        
        return {"messages": [new_message]}
    
    async def _tools_node(self, state: AgentState) -> dict[str, Any]:
        """
        Tool execution node.
        
        Args:
            state: Current agent state
            
        Returns:
            Updated state with tool results
        """
        messages = state["messages"]
        last_message = messages[-1]
        
        tool_results = []
        
        # Execute each tool call
        if "tool_calls" in last_message:
            for tool_call in last_message["tool_calls"]:
                tool_name = tool_call["function"]["name"]
                tool_args_str = tool_call["function"]["arguments"]
                
                # Parse arguments
                try:
                    if isinstance(tool_args_str, str):
                        tool_args = json.loads(tool_args_str)
                    else:
                        tool_args = tool_args_str
                except json.JSONDecodeError:
                    tool_args = {}
                
                logger.info(f"🔧 Tool call: {tool_name}")
                logger.debug(f"   Parameters: {tool_args}")
                
                # Route to appropriate MCP client
                result = await self._execute_tool(tool_name, tool_args)
                
                status = "SUCCESS" if result.get("success", False) else "FAIL"
                logger.info(f"{status} Tool result: {tool_name}")
                logger.debug(f"   Result: {result}")
                
                # Format tool result for LLM
                tool_result_message = {
                    "role": "tool",
                    "tool_call_id": tool_call["id"],
                    "name": tool_name,
                    "content": json.dumps(result, ensure_ascii=False),
                }
                tool_results.append(tool_result_message)
        
        # Increment tool calls counter
        new_tool_calls_made = state.get("tool_calls_made", 0) + len(tool_results)
        
        return {
            "messages": tool_results,
            "tool_calls_made": new_tool_calls_made,
        }
    
    async def _execute_tool(self, tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        """
        Execute a tool by routing to the appropriate MCP client.
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Tool arguments
            
        Returns:
            Tool execution result
        """
        # Determine which MCP client to use based on tool name
        filesystem_tools = ["list_files", "read_file"]
        gmail_tools = ["list_emails", "send_email", "read_email"]
        
        try:
            if tool_name in filesystem_tools:
                return await self.mcp_clients.call_filesystem(tool_name, arguments)
            elif tool_name in gmail_tools:
                return await self.mcp_clients.call_gmail(tool_name, arguments)
            else:
                return {
                    "success": False,
                    "error": f"Unknown tool: {tool_name}",
                }
        except Exception as e:
            logger.error(f"Tool execution failed: {e}")
            return {
                "success": False,
                "error": str(e),
            }
    
    def _should_continue(self, state: AgentState) -> str:
        """
        Determine if the agent should continue iterating.
        
        Args:
            state: Current agent state
            
        Returns:
            "continue" if should keep going, "end" if should stop
        """
        messages = state["messages"]
        last_message = messages[-1]
        
        # Check iteration limit
        if state.get("tool_calls_made", 0) >= state.get("max_iterations", self.max_iterations):
            logger.warning("Max iterations reached")
            return "end"
        
        # If the last message has tool calls, continue
        if "tool_calls" in last_message:
            return "continue"
        
        # Otherwise, we're done
        return "end"
    
    async def run(self, user_message: str) -> str:
        """
        Run the agent with a user message.
        
        Args:
            user_message: User's input message
            
        Returns:
            Agent's response
        """
        logger.info(f"User message: {user_message}")
        
        # Initialize state
        initial_state: AgentState = {
            "messages": [
                {"role": "system", "content": get_system_prompt()},
                {"role": "user", "content": user_message},
            ],
            "tool_calls_made": 0,
            "max_iterations": self.max_iterations,
        }
        
        # Run the graph
        final_state = await self.graph.ainvoke(initial_state)
        
        # Extract final response
        messages = final_state["messages"]
        
        # Find the last assistant message
        for message in reversed(messages):
            # Handle both dict and Message object formats
            if isinstance(message, dict):
                if message.get("role") == "assistant" and message.get("content"):
                    response = message["content"]
                    logger.info(f"Agent response: {response}")
                    return response
            elif hasattr(message, "type") and hasattr(message, "content"):
                if message.type == "ai" and message.content:
                    response = message.content
                    logger.info(f"Agent response: {response}")
                    return response
        
        return "Je n'ai pas pu générer une réponse. Veuillez réessayer."
    
    async def run_with_history(
        self,
        user_message: str,
        conversation_history: list[dict[str, str]],
    ) -> tuple[str, list[dict[str, str]]]:
        """
        Run the agent with conversation history.
        
        Args:
            user_message: User's input message
            conversation_history: Previous conversation messages
            
        Returns:
            Tuple of (response, updated_history)
        """
        logger.info(f"User message: {user_message}")
        
        # Build messages with history
        messages = [{"role": "system", "content": get_system_prompt()}]
        messages.extend(conversation_history)
        messages.append({"role": "user", "content": user_message})
        
        # Initialize state
        initial_state: AgentState = {
            "messages": messages,
            "tool_calls_made": 0,
            "max_iterations": self.max_iterations,
        }
        
        # Run the graph
        final_state = await self.graph.ainvoke(initial_state)
        
        # Extract final response
        final_messages = final_state["messages"]
        
        # Find the last assistant message
        response = "Je n'ai pas pu générer une réponse. Veuillez réessayer."
        for message in reversed(final_messages):
            # Handle both dict and Message object formats
            if isinstance(message, dict):
                if message.get("role") == "assistant" and message.get("content"):
                    response = message["content"]
                    break
            elif hasattr(message, "type") and hasattr(message, "content"):
                if message.type == "ai" and message.content:
                    response = message.content
                    break
        
        logger.info(f"Agent response: {response}")
        
        # Update history (add user message and assistant response)
        updated_history = conversation_history + [
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": response},
        ]
        
        return response, updated_history


async def create_agent(
    llm_client: LLMClient,
    mcp_clients: MCPClients,
) -> ConferenceAgent:
    """
    Create and initialize a conference agent.
    
    Args:
        llm_client: LLM client instance
        mcp_clients: MCP clients instance
        
    Returns:
        Initialized ConferenceAgent
    """
    agent = ConferenceAgent(llm_client, mcp_clients)
    await agent.initialize()
    return agent

