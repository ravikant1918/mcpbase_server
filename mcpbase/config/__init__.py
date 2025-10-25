"""
Configuration Module for MCPBase
================================

Contains all configuration constants, settings, and environment variables
for the MCP server.
"""

import os
from dataclasses import dataclass
from typing import Dict, Any
from datetime import datetime


@dataclass
class ServerConfig:
    """Server configuration settings."""
    
    # Server identification
    name: str = "MCPBase Server"
    version: str = "1.0.0"
    description: str = "A minimal yet structured MCP base server"
    
    # Network settings
    default_host: str = "0.0.0.0"
    default_http_port: int = 8000
    default_sse_port: int = 8000
    
    # MCP Protocol settings
    protocol_version: str = "2024-11-05"
    
    # Logging settings
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Transport settings
    default_transport: str = "stdio"  # stdio, http, sse
    sse_mount_path: str = "/sse"
    
    # Resource settings
    enable_kv_store: bool = True
    kv_store_uri: str = "kv://store"


@dataclass
class EnvironmentConfig:
    """Environment-specific configuration."""
    
    # Development settings
    debug: bool = os.getenv("MCPBASE_DEBUG", "false").lower() == "true"
    reload: bool = os.getenv("MCPBASE_RELOAD", "false").lower() == "true"
    
    # Optional features
    enable_fastapi: bool = os.getenv("MCPBASE_ENABLE_FASTAPI", "true").lower() == "true"
    enable_logging: bool = os.getenv("MCPBASE_ENABLE_LOGGING", "true").lower() == "true"


# Global configuration instances
SERVER_CONFIG = ServerConfig()
ENV_CONFIG = EnvironmentConfig()

# Initial KV store data
DEFAULT_KV_DATA: Dict[str, Any] = {
    "example_key": "example_value",
    "server_started": datetime.now().isoformat(),
    "counter": 0,
    "config": {
        "server_name": SERVER_CONFIG.name,
        "version": SERVER_CONFIG.version
    }
}

# Tool registry configuration
TOOL_REGISTRY = {
    "echo": {
        "name": "tools.echo",
        "description": "Echo back the provided message",
        "module": "mcpbase.tools.basic_tools",
        "function": "echo_tool"
    },
    "reverse": {
        "name": "tools.reverse", 
        "description": "Reverse the provided text",
        "module": "mcpbase.tools.basic_tools",
        "function": "reverse_tool"
    },
    "calculator": {
        "name": "tools.calculator",
        "description": "Perform basic arithmetic operations",
        "module": "mcpbase.tools.math_tools",
        "function": "calculator_tool"
    }
}

# Prompt registry configuration
PROMPT_REGISTRY = {
    "code_review": {
        "name": "code_review",
        "description": "Generate a code review prompt template",
        "module": "mcpbase.prompts.development_prompts",
        "function": "code_review_prompt"
    }
}

# Resource registry configuration
RESOURCE_REGISTRY = {
    "kv_store": {
        "uri": SERVER_CONFIG.kv_store_uri,
        "name": "Key-Value Store",
        "description": "In-memory key-value store with get/set/list operations",
        "mime_type": "application/json",
        "module": "mcpbase.utils.resources",
        "class": "KeyValueStore"
    }
}