"""
MCP client for connecting to filesystem and Gmail MCP servers.

This module provides a unified interface to interact with MCP servers
using the official MCP library via stdio transport.
"""

import json
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from src.conference_agent.config import settings
from src.conference_agent.logging import logger


class MCPClients:
    """Manager for MCP client connections using simple async with."""
    
    def __init__(
        self,
        filesystem_command: str,
        filesystem_args: list[str],
        gmail_command: str,
        gmail_args: list[str],
    ):
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
        
        self._fs_stdio_ctx = None
        self._fs_session_ctx = None
        self._gmail_stdio_ctx = None
        self._gmail_session_ctx = None
        
        logger.info("MCP Clients initialized")
    
    async def __aenter__(self) -> "MCPClients":
        # Connect to filesystem server
        logger.info("Starting filesystem server...")
        self._fs_stdio_ctx = stdio_client(self.filesystem_params)
        fs_streams = await self._fs_stdio_ctx.__aenter__()
        
        self._fs_session_ctx = ClientSession(*fs_streams)
        self.filesystem_session = await self._fs_session_ctx.__aenter__()
        await self.filesystem_session.initialize()
        logger.info("✓ Filesystem server connected")
        
        # Connect to Gmail server
        logger.info("Starting Gmail server...")
        self._gmail_stdio_ctx = stdio_client(self.gmail_params)
        gmail_streams = await self._gmail_stdio_ctx.__aenter__()
        
        self._gmail_session_ctx = ClientSession(*gmail_streams)
        self.gmail_session = await self._gmail_session_ctx.__aenter__()
        await self.gmail_session.initialize()
        logger.info("✓ Gmail server connected")
        
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        logger.info("Disconnecting from MCP servers...")
        
        # Close in reverse order
        if self._gmail_session_ctx:
            try:
                await self._gmail_session_ctx.__aexit__(exc_type, exc_val, exc_tb)
            except Exception as e:
                logger.debug(f"Gmail session cleanup: {e}")
        
        if self._gmail_stdio_ctx:
            try:
                await self._gmail_stdio_ctx.__aexit__(exc_type, exc_val, exc_tb)
            except Exception as e:
                logger.debug(f"Gmail stdio cleanup: {e}")
        
        if self._fs_session_ctx:
            try:
                await self._fs_session_ctx.__aexit__(exc_type, exc_val, exc_tb)
            except Exception as e:
                logger.debug(f"Filesystem session cleanup: {e}")
        
        if self._fs_stdio_ctx:
            try:
                await self._fs_stdio_ctx.__aexit__(exc_type, exc_val, exc_tb)
            except Exception as e:
                logger.debug(f"Filesystem stdio cleanup: {e}")
        
        self.filesystem_session = None
        self.gmail_session = None
        self._fs_stdio_ctx = None
        self._fs_session_ctx = None
        self._gmail_stdio_ctx = None
        self._gmail_session_ctx = None
        
        logger.info("✓ Disconnected from MCP servers")
    
    async def list_filesystem_tools(self) -> list[dict[str, Any]]:
        if not self.filesystem_session:
            raise RuntimeError("Filesystem session not connected")
        
        response = await self.filesystem_session.list_tools()
        
        tools = []
        for tool in response.tools:
            tools.append({
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.inputSchema,
            })
        
        return tools
    
    async def list_gmail_tools(self) -> list[dict[str, Any]]:
        if not self.gmail_session:
            raise RuntimeError("Gmail session not connected")
        
        response = await self.gmail_session.list_tools()
        
        tools = []
        for tool in response.tools:
            tools.append({
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.inputSchema,
            })
        
        return tools
    
    async def list_all_tools(self) -> list[dict[str, Any]]:
        filesystem_tools = await self.list_filesystem_tools()
        gmail_tools = await self.list_gmail_tools()
        return filesystem_tools + gmail_tools
    
    async def call_filesystem(self, tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        if not self.filesystem_session:
            raise RuntimeError("Filesystem session not connected")
        
        logger.debug(f"Calling filesystem tool: {tool_name} with args: {arguments}")
        
        try:
            result = await self.filesystem_session.call_tool(tool_name, arguments)
            
            if result.content:
                content_text = result.content[0].text
                return json.loads(content_text)
            
            return {"success": False, "error": "No content in response"}
            
        except Exception as e:
            logger.error(f"Filesystem tool call failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def call_gmail(self, tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        if not self.gmail_session:
            raise RuntimeError("Gmail session not connected")
        
        logger.debug(f"Calling Gmail tool: {tool_name} with args: {arguments}")
        
        try:
            result = await self.gmail_session.call_tool(tool_name, arguments)
            
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
