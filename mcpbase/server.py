"""
MCPBase Server Implementation
============================

Main server module that orchestrates all components of the MCPBase server.
Simplified to use FastMCP's native capabilities for all transports.
"""

from typing import Dict, Any

from .config import SERVER_CONFIG
from .utils.logging_setup import setup_logging
from .utils.mcp_backends import get_mcp_imports
from .utils.resources import KeyValueStore
from .tools import echo_tool, reverse_tool, calculator_tool
from .prompts import code_review_prompt

# Setup logging
logger = setup_logging()


class MCPBaseServer:
    """
    Simplified MCP server using FastMCP's native capabilities.
    
    FastMCP handles all protocol details, transports, and server management.
    We just need to register our tools, resources, and prompts.
    """
    
    def __init__(self):
        """Initialize the MCPBase server with FastMCP."""
        logger.info(f"Initializing {SERVER_CONFIG.name} v{SERVER_CONFIG.version}")
        
        # Detect MCP backend - simplified to FastMCP only
        self.backend, self.mcp_imports = get_mcp_imports()
        logger.info(f"Using MCP backend: {self.backend}")
        
        if self.backend != "fastmcp":
            logger.error("MCPBase now requires FastMCP. Please install: pip install fastmcp")
            raise RuntimeError("FastMCP is required")
        
        # Initialize FastMCP server
        self.server = self.mcp_imports["FastMCP"](SERVER_CONFIG.name)
        
        # Initialize key-value store for resources
        self.kv_store = KeyValueStore()
        
        # Register all components using FastMCP decorators
        self._register_tools()
        self._register_resources()
        self._register_prompts()
        
        logger.info("MCPBase server initialized successfully")
    
    def _register_tools(self):
        """Register tools using FastMCP decorators."""
        logger.info("Registering tools...")
        
        @self.server.tool()
        async def echo(message: str) -> Dict[str, Any]:
            """Echo back the provided message."""
            return await echo_tool(message)
        
        @self.server.tool()
        async def reverse(text: str) -> Dict[str, Any]:
            """Reverse the provided text."""
            return await reverse_tool(text)
        
        @self.server.tool()
        async def calculator(operation: str, a: float, b: float) -> Dict[str, Any]:
            """Perform basic arithmetic operations (add, subtract, multiply, divide)."""
            return await calculator_tool(operation, a, b)
        
        logger.info("Registered 3 tools: echo, reverse, calculator")
    
    def _register_resources(self):
        """Register resources using FastMCP decorators."""
        logger.info("Registering resources...")
        
        @self.server.resource(SERVER_CONFIG.kv_store_uri)
        async def kv_store() -> str:
            """Key-value store resource with get/set/list operations."""
            return self.kv_store.to_json()
        
        logger.info("Registered 1 resource: key-value store")
    
    def _register_prompts(self):
        """Register prompts using FastMCP decorators."""
        logger.info("Registering prompts...")
        
        @self.server.prompt()
        async def code_review(
            code: str = "# Your code here",
            language: str = "python", 
            focus: str = "general"
        ) -> str:
            """Generate a comprehensive code review prompt template."""
            return await code_review_prompt(code, language, focus)
        
        logger.info("Registered 1 prompt: code_review")
    
    def run(self, transport: str = "stdio"):
        """
        Run the server with the specified transport.
        
        Args:
            transport: Transport type - 'stdio', 'sse', or any FastMCP supported transport
        """
        logger.info(f"Starting MCPBase server with {transport} transport...")
        
        # Let FastMCP handle everything
        if transport == "sse":
            self.server.run(transport="sse")
        else:
            self.server.run(transport=transport)