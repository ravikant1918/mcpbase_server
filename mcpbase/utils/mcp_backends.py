"""
MCP Backend Detection and Import Utilities
==========================================

Handles detection and importing of different MCP backends (FastMCP vs standard MCP).
"""

import logging
from typing import Tuple, Optional

logger = logging.getLogger("mcpbase.utils.mcp_backends")


def detect_mcp_backend() -> Tuple[str, dict]:
    """
    Detect available MCP backend and return appropriate imports.
    
    Returns:
        Tuple[str, dict]: Backend name and import dictionary
        
    Raises:
        ImportError: If no MCP backend is available
    """
    try:
        # Try FastMCP first
        from mcp.server.fastmcp import FastMCP
        from mcp.server.stdio import stdio_server
        
        imports = {
            "FastMCP": FastMCP,
            "stdio_server": stdio_server
        }
        
        logger.info("Using FastMCP backend")
        return "fastmcp", imports
        
    except ImportError:
        try:
            # Fallback to standard MCP
            from mcp.server import Server
            from mcp.server.stdio import stdio_server
            from mcp import types
            
            imports = {
                "Server": Server,
                "stdio_server": stdio_server,
                "types": types
            }
            
            logger.info("Using standard MCP backend")
            return "standard", imports
            
        except ImportError:
            logger.error("Neither FastMCP nor standard MCP is available")
            raise ImportError(
                "No MCP backend available. Please install the 'mcp' package:\n"
                "pip install mcp"
            )


def get_mcp_imports() -> Tuple[str, dict]:
    """
    Get MCP imports with caching.
    
    Returns:
        Tuple[str, dict]: Backend name and imports
    """
    if not hasattr(get_mcp_imports, "_cache"):
        get_mcp_imports._cache = detect_mcp_backend()
    
    return get_mcp_imports._cache


def check_fastapi_availability() -> Tuple[bool, Optional[dict]]:
    """
    Check if FastAPI and Uvicorn are available.
    
    Returns:
        Tuple[bool, Optional[dict]]: Availability status and imports if available
    """
    try:
        from fastapi import FastAPI, HTTPException
        import uvicorn
        
        imports = {
            "FastAPI": FastAPI,
            "HTTPException": HTTPException,
            "uvicorn": uvicorn
        }
        
        logger.debug("FastAPI is available")
        return True, imports
        
    except ImportError:
        logger.warning("FastAPI not available. HTTP endpoints will be disabled.")
        return False, None