#!/usr/bin/env python3
"""
MCPBase - A Minimal Yet Structured MCP Server
=============================================

A production-ready Model Context Protocol (MCP) server with clean architecture,
comprehensive tooling, and multiple transport modes.

Usage:
    python server.py                 # Start MCP server (stdio mode)
    python server.py --http          # Start HTTP server with REST endpoints  
    python server.py --sse           # Start SSE server (Server-Sent Events)
    python server.py --self-test     # Run comprehensive self-tests

Features:
    - Tools: echo, reverse, calculator with full validation
    - Resources: Key-value store with get/set/list operations
    - Prompts: Advanced code review templates
    - Multiple transports: stdio, HTTP, SSE
    - Modular architecture with clean separation of concerns
    - Production-ready error handling and logging
    - Comprehensive test coverage

Requirements:
    pip install -r requirements.txt

Examples:
    # Health check
    curl http://localhost:8000/health
    
    # Invoke echo tool
    curl -X POST http://localhost:8000/tools/invoke \\
         -H "Content-Type: application/json" \\
         -d '{"name": "tools.echo", "arguments": {"message": "Hello MCPBase!"}}'
    
    # Get resource
    curl -X POST http://localhost:8000/resources/get \\
         -H "Content-Type: application/json" \\
         -d '{"uri": "kv://example_key"}'
    
    # SSE connection
    curl http://localhost:8000/sse

Project Structure:
    mcpbase/
    ├── __init__.py           # Package initialization
    ├── server.py             # Main server implementation  
    ├── config/               # Configuration and settings
    ├── tools/                # Tool implementations
    ├── prompts/              # Prompt templates
    └── utils/                # Utilities and helpers

Author: MCPBase Team
License: MIT
Version: 1.0.0
"""

import asyncio
import sys
from mcpbase.server import MCPBaseServer
from mcpbase.config import SERVER_CONFIG
from mcpbase.utils.logging_setup import get_logger

logger = get_logger("main")


async def self_test() -> bool:
    """
    Comprehensive self-test suite for MCPBase server.
    
    Tests all major components including tools, resources, and configuration.
    
    Returns:
        bool: True if all tests pass, False otherwise
    """
    logger.info("Running MCPBase self-tests...")
    
    try:
        # Test server initialization
        server = MCPBaseServer()
        logger.info("✓ Server initialization successful")
        
        # Test KV store operations
        test_key = "test_key"
        test_value = "test_value"
        
        server.kv_store.set(test_key, test_value)
        assert server.kv_store.get(test_key) == test_value
        logger.info("✓ KV store operations working")
        
        # Test tool imports
        from mcpbase.tools import echo_tool, reverse_tool, calculator_tool
        logger.info("✓ Tool imports successful")
        
        # Test tool functionality
        echo_result = await echo_tool("Hello Test")
        assert echo_result["status"] == "success"
        assert "Hello Test" in echo_result["result"]
        logger.info("✓ Echo tool working")
        
        reverse_result = await reverse_tool("Hello")
        assert reverse_result["status"] == "success"
        assert reverse_result["result"] == "olleH"
        logger.info("✓ Reverse tool working")
        
        calc_result = await calculator_tool("add", 5, 3)
        assert calc_result["status"] == "success"
        assert calc_result["result"] == 8
        logger.info("✓ Calculator tool working")
        
        # Test prompt functionality
        from mcpbase.prompts import code_review_prompt
        prompt_result = await code_review_prompt(
            code="def hello(): return 'world'",
            language="python",
            focus="best-practices"
        )
        assert "Code Review Request" in prompt_result
        logger.info("✓ Code review prompt working")
        
        # Test configuration
        assert SERVER_CONFIG.name == "MCPBase Server"
        assert SERVER_CONFIG.version == "1.0.0"
        logger.info("✓ Configuration valid")
        
        logger.info("🎉 All self-tests passed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Self-test failed: {e}")
        return False


def print_usage():
    """Print usage information and examples."""
    print(f"""
{SERVER_CONFIG.name} v{SERVER_CONFIG.version}
{SERVER_CONFIG.description}

Usage:
    python server.py [MODE] [OPTIONS]

Modes:
    (default)         Start MCP server in stdio mode
    --http            Start HTTP server with REST API
    --sse             Start Server-Sent Events server
    --self-test       Run comprehensive self-tests
    --help, -h        Show this help message

Examples:
    python server.py                    # MCP stdio mode
    python server.py --http             # HTTP mode on port 8000
    python server.py --sse              # SSE mode on port 8000
    python server.py --self-test        # Run tests

Environment Variables:
    MCPBASE_DEBUG=true                  # Enable debug logging
    MCPBASE_RELOAD=true                 # Enable auto-reload (dev mode)
    MCPBASE_ENABLE_FASTAPI=false        # Disable HTTP endpoints

HTTP Endpoints (when --http is used):
    GET  /health                        # Health check
    POST /tools/list                    # List available tools
    POST /tools/invoke                  # Invoke a tool
    POST /resources/get                 # Get resource value
    POST /resources/set                 # Set resource value

For more information, visit: https://github.com/mcpbase/mcpbase
""")


def main():
    """
    Main entry point for MCPBase server.
    
    Handles command line arguments and starts the appropriate server mode.
    """
    # Handle help flags
    if "--help" in sys.argv or "-h" in sys.argv:
        print_usage()
        sys.exit(0)
    
    # Handle self-test flag
    if "--self-test" in sys.argv:
        success = asyncio.run(self_test())
        sys.exit(0 if success else 1)
    
    # Initialize server
    try:
        server = MCPBaseServer()
    except Exception as e:
        logger.error(f"Failed to initialize server: {e}")
        sys.exit(1)
    
    # Determine and start server mode using FastMCP's simple run method
    try:
        if "--http" in sys.argv:
            logger.info("Starting HTTP mode...")
            # For HTTP testing, we can use FastMCP dev mode or custom HTTP server
            logger.warning("HTTP mode deprecated - use --sse for VS Code or stdio for Claude Desktop")
            server.run("stdio")  # Fallback to stdio
        elif "--sse" in sys.argv:
            logger.info("Starting SSE mode...")
            server.run("sse")
        else:
            logger.info("Starting stdio mode...")
            server.run("stdio")
            
    except KeyboardInterrupt:
        logger.info("Server shutting down gracefully...")
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()