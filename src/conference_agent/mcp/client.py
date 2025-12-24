"""
MCP client for connecting to filesystem and Gmail MCP servers.

This module provides a unified interface to interact with MCP servers
using the official MCP library via stdio transport.
"""

import json
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from conference_agent.config import settings
from conference_agent.logging import logger


class MCPClients:
    """
    Manager for MCP client connections.
    
    Handles connections to both filesystem and Gmail MCP servers
    using the official MCP library.
    """
    
    def __init__(
        self,
        filesystem_command: str,
        filesystem_args: list[str],
        gmail_command: str,
        gmail_args: list[str],
    ):
        """
        Initialize MCP clients manager.
        
        Args:
            filesystem_command: Command to run filesystem MCP server
            filesystem_args: Arguments for filesystem server
            gmail_command: Command to run Gmail MCP server
            gmail_args: Arguments for Gmail server
        """
        self.filesystem_params = StdioServerParameters(
            command=filesystem_command,
            args=filesystem_args,
        )
        self.gmail_params = StdioServerParameters(
            command=gmail_command,
            args=gmail_args,
        )
        
        self.filesystem_session: ClientSession | None = None
        self.gmail_session: ClientSession | None = None
        
        # Store context managers  
        self._filesystem_ctx = None
        self._gmail_ctx = None
        
        logger.info("MCP Clients initialized")
    
    async def __aenter__(self) -> "MCPClients":
        """Context manager entry."""
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit."""
        await self.disconnect()
    
    async def connect(self) -> None:
        """Connect to both MCP servers."""
        logger.info("Connecting to MCP servers...")
        
        try:
            # Connect to filesystem server
            logger.info("Starting filesystem server...")
            self._filesystem_ctx = stdio_client(self.filesystem_params)
            fs_read, fs_write = await self._filesystem_ctx.__aenter__()
            self.filesystem_session = ClientSession(fs_read, fs_write)
            await self.filesystem_session.__aenter__()
            await self.filesystem_session.initialize()
            logger.info("✓ Filesystem server connected")
            
            # Connect to Gmail server
            logger.info("Starting Gmail server...")
            self._gmail_ctx = stdio_client(self.gmail_params)
            gmail_read, gmail_write = await self._gmail_ctx.__aenter__()
            self.gmail_session = ClientSession(gmail_read, gmail_write)
            await self.gmail_session.__aenter__()
            await self.gmail_session.initialize()
            logger.info("✓ Gmail server connected")
        except Exception as e:
            logger.error(f"Failed to connect to MCP servers: {e}")
            await self.disconnect()
            raise
    
    async def disconnect(self) -> None:
        """Disconnect from MCP servers - simple cleanup."""
        logger.info("Disconnecting from MCP servers...")
        
        # Just close the sessions, let Python cleanup the rest
        errors = []
        
        for name, session in [("Gmail", self.gmail_session), ("Filesystem", self.filesystem_session)]:
            if session:
                try:
                    await session.__aexit__(None, None, None)
                except Exception as e:
                    errors.append(f"{name}: {e}")
        
        # Don't try to manually close contexts - causes cancel scope issues
        # The context managers will cleanup automatically
        
        if errors:
            logger.debug(f"Minor cleanup warnings: {errors}")
        else:
            logger.info("Disconnected cleanly")
        
        logger.info("Disconnected from MCP servers")
    
    async def list_filesystem_tools(self) -> list[dict[str, Any]]:
        """
        List available filesystem tools.
        
        Returns:
            List of tool definitions
        """
        if not self.filesystem_session:
            raise RuntimeError("Filesystem session not connected")
        
        response = await self.filesystem_session.list_tools()
        
        # Convert MCP Tool objects to dictionaries
        tools = []
        for tool in response.tools:
            tools.append({
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.inputSchema,
            })
        
        return tools
    
    async def list_gmail_tools(self) -> list[dict[str, Any]]:
        """
        List available Gmail tools.
        
        Returns:
            List of tool definitions
        """
        if not self.gmail_session:
            raise RuntimeError("Gmail session not connected")
        
        response = await self.gmail_session.list_tools()
        
        # Convert MCP Tool objects to dictionaries
        tools = []
        for tool in response.tools:
            tools.append({
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.inputSchema,
            })
        
        return tools
    
    async def list_all_tools(self) -> list[dict[str, Any]]:
        """
        List all available tools from both servers.
        
        Returns:
            Combined list of all tool definitions
        """
        filesystem_tools = await self.list_filesystem_tools()
        gmail_tools = await self.list_gmail_tools()
        return filesystem_tools + gmail_tools
    
    async def call_filesystem(self, tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        """
        Call a filesystem tool.
        
        Args:
            tool_name: Name of the tool to call
            arguments: Arguments to pass to the tool
            
        Returns:
            Tool execution result as a dictionary
        """
        if not self.filesystem_session:
            raise RuntimeError("Filesystem session not connected")
        
        logger.debug(f"Calling filesystem tool: {tool_name} with args: {arguments}")
        
        try:
            result = await self.filesystem_session.call_tool(tool_name, arguments)
            
            # Parse result content (MCP returns TextContent)
            if result.content:
                content_text = result.content[0].text
                return json.loads(content_text)
            
            return {"success": False, "error": "No content in response"}
            
        except Exception as e:
            logger.error(f"Filesystem tool call failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def call_gmail(self, tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        """
        Call a Gmail tool.
        
        Args:
            tool_name: Name of the tool to call
            arguments: Arguments to pass to the tool
            
        Returns:
            Tool execution result as a dictionary
        """
        if not self.gmail_session:
            raise RuntimeError("Gmail session not connected")
        
        logger.debug(f"Calling Gmail tool: {tool_name} with args: {arguments}")
        
        try:
            result = await self.gmail_session.call_tool(tool_name, arguments)
            
            # Parse result content (MCP returns TextContent)
            if result.content:
                content_text = result.content[0].text
                return json.loads(content_text)
            
            return {"success": False, "error": "No content in response"}
            
        except Exception as e:
            logger.error(f"Gmail tool call failed: {e}")
            return {"success": False, "error": str(e)}


async def build_mcp_clients(
    filesystem_command: str | None = None,
    filesystem_args: list[str] | None = None,
    gmail_command: str | None = None,
    gmail_args: list[str] | None = None,
) -> MCPClients:
    """
    Build MCP clients from configuration.
    
    Args:
        filesystem_command: Command to run filesystem server
        filesystem_args: Arguments for filesystem server
        gmail_command: Command to run Gmail server
        gmail_args: Arguments for Gmail server
        
    Returns:
        MCPClients instance (not yet connected, use as context manager)
    """
    fs_command = filesystem_command or settings.mcp_filesystem_command
    fs_args = filesystem_args or settings.get_filesystem_args_list()
    
    gmail_cmd = gmail_command or settings.mcp_gmail_command
    gmail_args_list = gmail_args or settings.get_gmail_args_list()
    
    return MCPClients(
        filesystem_command=fs_command,
        filesystem_args=fs_args,
        gmail_command=gmail_cmd,
        gmail_args=gmail_args_list,
    )

