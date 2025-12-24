#!/usr/bin/env python3
"""Test script to verify MCP servers are working correctly."""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

# Add src to path (go up one level from tests/ to reach project root)
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from conference_agent.config import settings
from conference_agent.logging import logger
from conference_agent.mcp.client import build_mcp_clients


async def test_mcp_servers():
    """Test both MCP servers and their tools."""
    logger.info("=" * 60)
    logger.info("Testing MCP Servers")
    logger.info("=" * 60)
    
    try:
        # Build MCP clients (must use as context manager)
        logger.info("Connecting to MCP servers...")
        async with await build_mcp_clients(
            filesystem_command=settings.mcp_filesystem_command,
            filesystem_args=settings.get_filesystem_args_list(),
            gmail_command=settings.mcp_gmail_command,
            gmail_args=settings.get_gmail_args_list(),
        ) as mcp_clients:
            logger.info("Connected to both servers")
            
            # Test filesystem tools
            logger.info("\n--- Testing Filesystem Server ---")
            
            logger.info("Listing filesystem tools...")
            fs_tools = await mcp_clients.list_filesystem_tools()
            logger.info(f"Available tools: {[t.get('name') for t in fs_tools]}")
            
            logger.info("\nCalling 'list_files' tool...")
            result = await mcp_clients.call_filesystem("list_files", {})
            logger.info(f"Result: {result}")
            
            logger.info("\nCalling 'read_file' tool (participants.xlsx)...")
            result = await mcp_clients.call_filesystem("read_file", {"filename": "participants.xlsx"})
            logger.info(f"Result preview: {str(result)[:200]}...")
            
            # Test Gmail tools
            logger.info("\n--- Testing Gmail Server ---")
            
            logger.info("Listing Gmail tools...")
            gmail_tools = await mcp_clients.list_gmail_tools()
            logger.info(f"Available tools: {[t.get('name') for t in gmail_tools]}")
            
            logger.info("\nCalling 'list_emails' tool...")
            result = await mcp_clients.call_gmail("list_emails", {"max_results": 3})
            logger.info(f"Result: {result}")
            
            logger.info("\nCalling 'send_email' tool (test)...")
            result = await mcp_clients.call_gmail("send_email", {
                "to": ["test@example.com"],
                "subject": "Test email",
                "body": "This is a test email from the MCP server."
            })
            logger.info(f"Result: {result}")
            
            # Context manager automatically closes everything properly
            
            logger.info("\n" + "=" * 60)
            logger.info("All tests passed!")
            logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"✗ Test failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(test_mcp_servers())
