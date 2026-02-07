"""
MCP Configuration

Loads MCP server configurations from environment variables or config file.
"""

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from ..utils.logger import get_logger
from ..config import get_config

logger = get_logger("mcp-config")

# Pattern to match ${VAR_NAME} env var references
_ENV_VAR_PATTERN = re.compile(r"^\$\{([^}]+)\}$")


@dataclass
class MCPServerConfig:
    """Configuration for an MCP server."""
    name: str
    command: str
    args: list[str]
    env: dict[str, str]


@dataclass
class MCPConfig:
    """Complete MCP configuration."""
    servers: list[MCPServerConfig]


def load_mcp_config() -> MCPConfig:
    """
    Load MCP configuration.
    
    Priority:
    1. mcp-config.json file in project root
    2. Environment variables
    """
    servers = []
    
    # Try loading from config file first
    config_path = Path("mcp-config.json")
    if config_path.exists():
        try:
            with open(config_path) as f:
                data = json.load(f)
            
            for name, server_config in data.get("mcpServers", {}).items():
                # Resolve ${VAR_NAME} references in env values
                raw_env = server_config.get("env", {})
                resolved_env = {}
                for key, value in raw_env.items():
                    match = _ENV_VAR_PATTERN.match(value)
                    if match:
                        var_name = match.group(1)
                        resolved = os.environ.get(var_name)
                        if resolved:
                            resolved_env[key] = resolved
                        else:
                            logger.warning(f"Environment variable {var_name} not set for MCP server '{name}'")
                    else:
                        resolved_env[key] = value

                servers.append(MCPServerConfig(
                    name=name,
                    command=server_config.get("command", "npx"),
                    args=server_config.get("args", []),
                    env=resolved_env,
                ))
            
            logger.info(f"Loaded {len(servers)} MCP servers from config file")
            return MCPConfig(servers=servers)
        except Exception as e:
            logger.warning(f"Failed to load mcp-config.json: {e}")
    
    # Fallback: build from environment variables
    logger.info("Building MCP config from environment variables")
    
    config = get_config()
    
    # GitHub MCP Server
    github_token = config.mcp.github_token or os.environ.get("GITHUB_TOKEN")
    if github_token:
        servers.append(MCPServerConfig(
            name="github",
            command="npx",
            args=["-y", "@modelcontextprotocol/server-github"],
            env={"GITHUB_PERSONAL_ACCESS_TOKEN": github_token},
        ))
        logger.info("GitHub MCP server configured")
    
    # Notion MCP Server
    notion_token = config.mcp.notion_token or os.environ.get("NOTION_TOKEN")
    if notion_token:
        servers.append(MCPServerConfig(
            name="notion",
            command="npx",
            args=["-y", "@notionhq/notion-mcp-server"],
            env={"NOTION_TOKEN": notion_token},
        ))
        logger.info("Notion MCP server configured")
    
    return MCPConfig(servers=servers)
