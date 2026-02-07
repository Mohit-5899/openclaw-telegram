"""
MCP Client

Manages connections to MCP servers via subprocess and JSON-RPC over stdio.
Handles tool discovery, execution, and server lifecycle.
"""

import asyncio
import json
import os
import subprocess
from dataclasses import dataclass
from typing import Any, Optional

from ..utils.logger import get_logger
from .config import load_mcp_config, MCPServerConfig
from .tool_converter import mcp_tools_to_anthropic, parse_tool_name, format_mcp_result

logger = get_logger("mcp-client")


@dataclass
class MCPServer:
    """Represents a connected MCP server."""
    name: str
    process: subprocess.Popen
    tools: list[dict]
    request_id: int = 0


# Connected servers
_servers: dict[str, MCPServer] = {}


async def initialize_mcp() -> None:
    """Initialize all configured MCP servers."""
    logger.info("Initializing MCP servers...")
    
    config = load_mcp_config()
    
    if not config.servers:
        logger.info("No MCP servers configured")
        return
    
    for server_config in config.servers:
        try:
            await _connect_server(server_config)
        except Exception as e:
            logger.error(f"Failed to connect to MCP server {server_config.name}: {e}")
    
    total_tools = sum(len(s.tools) for s in _servers.values())
    logger.info(f"MCP initialized: {len(_servers)} servers, {total_tools} tools")


async def _connect_server(config: MCPServerConfig) -> None:
    """Connect to a single MCP server."""
    logger.info(f"Connecting to MCP server: {config.name}")
    
    # Prepare environment
    env = os.environ.copy()
    env.update(config.env)
    
    # Spawn the process
    try:
        process = subprocess.Popen(
            [config.command] + config.args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            text=True,
            bufsize=0,
        )
    except Exception as e:
        logger.error(f"Failed to spawn {config.name}: {e}")
        raise
    
    server = MCPServer(
        name=config.name,
        process=process,
        tools=[],
    )
    
    # Initialize the server
    try:
        # Send initialize request
        init_result = await _send_request(server, "initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "telegram-clawdbot",
                "version": "1.0.0"
            }
        })
        
        logger.debug(f"Server {config.name} initialized: {init_result}")
        
        # Send initialized notification
        await _send_notification(server, "notifications/initialized", {})
        
        # Discover tools
        tools_result = await _send_request(server, "tools/list", {})
        server.tools = tools_result.get("tools", [])
        
        logger.info(f"Server {config.name} connected with {len(server.tools)} tools")
        
        _servers[config.name] = server
        
    except Exception as e:
        logger.error(f"Failed to initialize {config.name}: {e}")
        process.terminate()
        raise


async def _send_request(server: MCPServer, method: str, params: dict) -> dict:
    """Send a JSON-RPC request to the server."""
    server.request_id += 1
    
    request = {
        "jsonrpc": "2.0",
        "id": server.request_id,
        "method": method,
        "params": params,
    }
    
    request_str = json.dumps(request) + "\n"
    
    try:
        server.process.stdin.write(request_str)
        server.process.stdin.flush()
        
        # Read response (with timeout)
        response_line = await asyncio.wait_for(
            asyncio.get_event_loop().run_in_executor(
                None, server.process.stdout.readline
            ),
            timeout=30.0
        )
        
        if not response_line:
            raise Exception("Empty response from server")
        
        response = json.loads(response_line)
        
        if "error" in response:
            raise Exception(f"MCP error: {response['error']}")
        
        return response.get("result", {})
        
    except asyncio.TimeoutError:
        logger.error(f"Timeout waiting for response from {server.name}")
        raise
    except Exception as e:
        logger.error(f"Request failed: {e}")
        raise


async def _send_notification(server: MCPServer, method: str, params: dict) -> None:
    """Send a JSON-RPC notification (no response expected)."""
    notification = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
    }
    
    notification_str = json.dumps(notification) + "\n"
    
    server.process.stdin.write(notification_str)
    server.process.stdin.flush()


async def shutdown_mcp() -> None:
    """Shutdown all MCP servers."""
    logger.info("Shutting down MCP servers...")
    
    for name, server in _servers.items():
        try:
            server.process.terminate()
            server.process.wait(timeout=5)
            logger.debug(f"Server {name} terminated")
        except Exception as e:
            logger.warning(f"Error shutting down {name}: {e}")
            server.process.kill()
    
    _servers.clear()
    logger.info("MCP servers shut down")


def get_all_tools() -> list[dict]:
    """
    Get all tools from all connected servers in OpenAI format.
    
    Returns:
        List of OpenAI function definitions
    """
    all_tools = []
    
    for name, server in _servers.items():
        anthropic_tools = mcp_tools_to_anthropic(server.tools, name)
        all_tools.extend(anthropic_tools)
    
    return all_tools


async def execute_tool(tool_name: str, args: dict) -> Any:
    """
    Execute an MCP tool.
    
    Args:
        tool_name: Full tool name (e.g., "github_create_issue")
        args: Tool arguments
    
    Returns:
        Tool execution result
    """
    parsed = parse_tool_name(tool_name)
    
    if not parsed:
        raise ValueError(f"Unknown tool: {tool_name}")
    
    server_name, original_tool_name = parsed
    
    server = _servers.get(server_name)
    if not server:
        raise ValueError(f"MCP server not connected: {server_name}")
    
    logger.info(f"Executing MCP tool: {server_name}/{original_tool_name}")
    
    try:
        result = await _send_request(server, "tools/call", {
            "name": original_tool_name,
            "arguments": args,
        })
        
        return result
    except Exception as e:
        logger.error(f"MCP tool execution failed: {e}")
        raise


def is_mcp_tool(tool_name: str) -> bool:
    """Check if a tool name is an MCP tool."""
    return parse_tool_name(tool_name) is not None
