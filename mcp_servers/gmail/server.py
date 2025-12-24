"""
Gmail MCP server implementation.

Simple MCP server that provides Gmail functionality using mock data.
"""

import asyncio
import json
import sys
from datetime import datetime

try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
except ImportError as e:
    print(f"Error importing dependencies: {e}", file=sys.stderr)
    print("Please install: pip install mcp", file=sys.stderr)
    sys.exit(1)


# Create MCP server instance
app = Server("conference-gmail")

# Mock email storage for the workshop
MOCK_EMAILS = [
    {
        "id": "email_001",
        "from": "conference@example.com",
        "subject": "Bienvenue à la conférence 2026",
        "date": "2025-12-20",
        "snippet": "Nous sommes ravis de vous accueillir...",
    },
    {
        "id": "email_002",
        "from": "speaker@example.com",
        "subject": "Confirmation de votre intervention",
        "date": "2025-12-19",
        "snippet": "Merci d'avoir accepté de parler à notre conférence...",
    },
]

SENT_EMAILS = []


@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    List available Gmail tools.
    
    Returns:
        List of tool definitions
    """
    return [
        Tool(
            name="list_emails",
            description="List recent emails from the inbox",
            inputSchema={
                "type": "object",
                "properties": {
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of emails to retrieve",
                        "default": 10,
                    },
                },
            },
        ),
        Tool(
            name="send_email",
            description="Send an email to one or more recipients",
            inputSchema={
                "type": "object",
                "properties": {
                    "to": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of recipient email addresses",
                    },
                    "subject": {
                        "type": "string",
                        "description": "Email subject",
                    },
                    "body": {
                        "type": "string",
                        "description": "Email body content",
                    },
                },
                "required": ["to", "subject", "body"],
            },
        ),
        Tool(
            name="read_email",
            description="Read the full content of a specific email by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "email_id": {
                        "type": "string",
                        "description": "ID of the email to read",
                    },
                },
                "required": ["email_id"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """
    Handle tool calls.
    
    Args:
        name: Name of the tool to call
        arguments: Tool arguments
        
    Returns:
        List of text content responses
    """
    if name == "list_emails":
        return await handle_list_emails(arguments.get("max_results", 10))
    elif name == "send_email":
        return await handle_send_email(
            to=arguments.get("to", []),
            subject=arguments.get("subject", ""),
            body=arguments.get("body", ""),
        )
    elif name == "read_email":
        return await handle_read_email(arguments.get("email_id", ""))
    else:
        raise ValueError(f"Unknown tool: {name}")


async def handle_list_emails(max_results: int) -> list[TextContent]:
    """
    Handle list_emails tool call.
    
    Args:
        max_results: Maximum number of emails to return
        
    Returns:
        List of emails
    """
    emails = MOCK_EMAILS[:max_results]
    
    result = {
        "success": True,
        "emails": emails,
        "count": len(emails),
    }
    
    return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]


async def handle_send_email(to: list[str], subject: str, body: str) -> list[TextContent]:
    """
    Handle send_email tool call.
    
    Args:
        to: List of recipient email addresses
        subject: Email subject
        body: Email body
        
    Returns:
        Send confirmation
    """
    # Validate inputs
    if not to:
        result = {
            "success": False,
            "error": "No recipients specified",
        }
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    
    if not subject:
        result = {
            "success": False,
            "error": "No subject specified",
        }
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    
    # Mock sending email
    email_record = {
        "id": f"sent_{len(SENT_EMAILS) + 1}",
        "to": to,
        "subject": subject,
        "body": body,
        "sent_at": datetime.now().isoformat(),
    }
    
    SENT_EMAILS.append(email_record)
    
    result = {
        "success": True,
        "message": f"Email sent to {len(to)} recipient(s)",
        "recipients": to,
        "subject": subject,
        "email_id": email_record["id"],
    }
    
    return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]


async def handle_read_email(email_id: str) -> list[TextContent]:
    """
    Handle read_email tool call.
    
    Args:
        email_id: ID of the email to read
        
    Returns:
        Email content
    """
    # Search in mock emails
    for email in MOCK_EMAILS:
        if email["id"] == email_id:
            full_email = {
                **email,
                "body": f"Ceci est le contenu complet de l'email '{email['subject']}'.\n\n"
                        f"Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            }
            result = {
                "success": True,
                "email": full_email,
            }
            return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    
    # Email not found
    result = {
        "success": False,
        "error": f"Email not found: {email_id}",
        "available_ids": [email["id"] for email in MOCK_EMAILS],
    }
    
    return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]


async def main() -> None:
    """Run the MCP server using stdio transport."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
