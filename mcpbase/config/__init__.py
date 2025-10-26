"""
Configuration Module for MCPBase
================================

Contains all configuration constants, settings, and environment variables
for the MCP server. Uses python-dotenv to load from .env file.
"""

import os
from dataclasses import dataclass
from typing import Dict, Any
from datetime import datetime

try:
    from dotenv import load_dotenv
    load_dotenv()  # Load .env file
except ImportError:
    pass  # dotenv not available, use environment variables directly


def get_env_bool(key: str, default: bool = False) -> bool:
    """Get boolean value from environment variable."""
    value = os.getenv(key, str(default)).lower()
    return value in ('true', '1', 'yes', 'on')


def get_env_int(key: str, default: int = 0) -> int:
    """Get integer value from environment variable."""
    try:
        return int(os.getenv(key, str(default)))
    except ValueError:
        return default
    
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
    debug: bool = False
    reload: bool = False
    
    # Optional features
    enable_fastapi: bool = True
    enable_logging: bool = True


# Create configuration instances with environment variable overrides
SERVER_CONFIG = ServerConfig(
    name=os.getenv('MCPBASE_SERVER_NAME', 'MCPBase Server'),
    version=os.getenv('MCPBASE_SERVER_VERSION', '1.0.0'),
    description=os.getenv('MCPBASE_SERVER_DESCRIPTION', 'A minimal yet structured MCP base server'),
    
    default_host=os.getenv('MCPBASE_DEFAULT_HOST', '0.0.0.0'),
    default_http_port=get_env_int('MCPBASE_DEFAULT_HTTP_PORT', 8000),
    default_sse_port=get_env_int('MCPBASE_DEFAULT_SSE_PORT', 8000),
    
    protocol_version=os.getenv('MCPBASE_PROTOCOL_VERSION', '2024-11-05'),
    
    log_level=os.getenv('MCPBASE_LOG_LEVEL', 'INFO'),
    log_format=os.getenv('MCPBASE_LOG_FORMAT', '%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
    
    default_transport=os.getenv('MCPBASE_DEFAULT_TRANSPORT', 'stdio'),
    sse_mount_path=os.getenv('MCPBASE_SSE_MOUNT_PATH', '/sse'),
    
    enable_kv_store=get_env_bool('MCPBASE_ENABLE_KV_STORE', True),
    kv_store_uri=os.getenv('MCPBASE_KV_STORE_URI', 'kv://store')
)

ENV_CONFIG = EnvironmentConfig(
    debug=get_env_bool('MCPBASE_DEBUG', False),
    reload=get_env_bool('MCPBASE_RELOAD', False),
    enable_fastapi=get_env_bool('MCPBASE_ENABLE_FASTAPI', True),
    enable_logging=get_env_bool('MCPBASE_ENABLE_LOGGING', True)
)

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
