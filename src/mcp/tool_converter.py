"""
MCP Tool Converter

Converts MCP tool definitions to OpenAI function calling format.
"""

import json
from typing import Any

from ..utils.logger import get_logger

logger = get_logger("tool-converter")


def mcp_tool_to_openai(tool: dict, server_name: str) -> dict:
    """
    Convert a single MCP tool to OpenAI function format.
    
    Args:
        tool: MCP tool definition
        server_name: Name of the MCP server
    
    Returns:
        OpenAI function tool definition
    """
    # Create a unique tool name by prefixing with server name
    tool_name = f"{server_name}_{tool['name']}"
    
    # Build OpenAI function schema
    return {
        "type": "function",
        "function": {
            "name": tool_name,
            "description": tool.get("description", f"{server_name} tool: {tool['name']}"),
            "parameters": tool.get("inputSchema", {
                "type": "object",
                "properties": {},
                "required": []
            }),
        }
    }


def mcp_tools_to_openai(tools: list[dict], server_name: str) -> list[dict]:
    """
    Convert multiple MCP tools to OpenAI format.
    
    Args:
        tools: List of MCP tool definitions
        server_name: Name of the MCP server
    
    Returns:
        List of OpenAI function tool definitions
    """
    return [mcp_tool_to_openai(tool, server_name) for tool in tools]


def parse_tool_name(full_name: str) -> tuple[str, str] | None:
    """
    Parse a prefixed tool name into server and tool name.
    
    Args:
        full_name: Full tool name (e.g., "github_create_issue")
    
    Returns:
        Tuple of (server_name, tool_name) or None if not an MCP tool
    """
    known_prefixes = ["github", "notion"]
    
    for prefix in known_prefixes:
        if full_name.startswith(f"{prefix}_"):
            tool_name = full_name[len(prefix) + 1:]
            return (prefix, tool_name)
    
    return None


def format_mcp_result(result: Any) -> str:
    """
    Format an MCP tool result for display.
    
    Args:
        result: Raw MCP result
    
    Returns:
        Formatted string
    """
    if result is None:
        return "✅ Action completed successfully"
    
    # Handle content array format (common MCP response)
    if isinstance(result, dict) and "content" in result:
        content = result["content"]
        if isinstance(content, list):
            parts = []
            for item in content:
                if isinstance(item, dict):
                    if item.get("type") == "text":
                        parts.append(item.get("text", ""))
                    else:
                        parts.append(json.dumps(item, indent=2))
                else:
                    parts.append(str(item))
            return "\n".join(parts)
    
    # Handle dict results
    if isinstance(result, dict):
        # Try to extract meaningful info
        if "url" in result:
            return f"✅ Created: {result['url']}"
        if "message" in result:
            return f"✅ {result['message']}"
        return json.dumps(result, indent=2)
    
    # Handle list results
    if isinstance(result, list):
        if len(result) == 0:
            return "No results found"
        return json.dumps(result, indent=2)
    
    return str(result)
