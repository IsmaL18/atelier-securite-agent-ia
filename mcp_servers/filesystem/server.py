"""
Filesystem MCP server implementation.

Simple MCP server that provides access to conference files.
"""

import asyncio
import json
import sys
from pathlib import Path

try:
    import openpyxl
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
except ImportError as e:
    print(f"Error importing dependencies: {e}", file=sys.stderr)
    print("Please install: pip install mcp openpyxl", file=sys.stderr)
    sys.exit(1)


# Data directory containing conference files
DATA_DIR = Path(__file__).parent / "data"

# Create MCP server instance
app = Server("conference-filesystem")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    List available filesystem tools.
    
    Returns:
        List of tool definitions
    """
    return [
        Tool(
            name="list_files",
            description="List all available files in the conference data directory",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        Tool(
            name="read_file",
            description="Read the content of a specific file (horaires.txt, programme.txt, participants.xlsx)",
            inputSchema={
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Name of the file to read",
                    },
                },
                "required": ["filename"],
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
    if name == "list_files":
        return await handle_list_files()
    elif name == "read_file":
        return await handle_read_file(arguments.get("filename", ""))
    else:
        raise ValueError(f"Unknown tool: {name}")


async def handle_list_files() -> list[TextContent]:
    """
    Handle list_files tool call.
    
    Returns:
        List of available files
    """
    files = []
    if DATA_DIR.exists():
        for file_path in DATA_DIR.iterdir():
            if file_path.is_file():
                files.append(file_path.name)
    
    result = {
        "success": True,
        "files": sorted(files),
        "count": len(files),
    }
    
    return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]


async def handle_read_file(filename: str) -> list[TextContent]:
    """
    Handle read_file tool call.
    
    Args:
        filename: Name of the file to read
        
    Returns:
        File content
    """
    file_path = DATA_DIR / filename
    
    if not file_path.exists():
        result = {
            "success": False,
            "error": f"File not found: {filename}",
            "available_files": sorted([f.name for f in DATA_DIR.iterdir() if f.is_file()]),
        }
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    
    # Security check: ensure file is within DATA_DIR
    if not file_path.resolve().is_relative_to(DATA_DIR.resolve()):
        result = {
            "success": False,
            "error": "Access denied: file outside data directory",
        }
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    
    try:
        # Handle Excel files
        if filename.endswith(('.xlsx', '.xls')):
            workbook = openpyxl.load_workbook(file_path)
            sheet = workbook.active
            
            # Convert to list of dictionaries
            headers = [cell.value for cell in sheet[1]]
            participants = []
            
            for row in sheet.iter_rows(min_row=2, values_only=True):
                participant = {}
                for header, value in zip(headers, row):
                    if header:
                        participant[header] = value
                participants.append(participant)
            
            result = {
                "success": True,
                "filename": filename,
                "type": "excel",
                "data": participants,
                "count": len(participants),
            }
        else:
            # Handle text files
            content = file_path.read_text(encoding="utf-8")
            result = {
                "success": True,
                "filename": filename,
                "type": "text",
                "content": content,
            }
        
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    
    except Exception as e:
        result = {
            "success": False,
            "error": f"Error reading file: {str(e)}",
        }
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]


async def main() -> None:
    """Run the MCP server using stdio transport."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
