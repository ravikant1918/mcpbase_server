# MCPBase - A Minimal Yet Structured MCP Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Model Context Protocol](https://img.shields.io/badge/MCP-2024--11--05-green.svg)](https://modelcontextprotocol.io/)

A production-ready **Model Context Protocol (MCP)** server implementation with clean architecture, comprehensive tooling, and multiple transport modes. MCPBase provides a solid foundation for building MCP-compatible AI assistants and automation tools.

## ✨ Features

### 🛠️ **Tools**
- **Echo Tool**: Message echoing with timestamps and metadata
- **Reverse Tool**: Text reversal with input validation
- **Calculator Tool**: Basic arithmetic operations (add, subtract, multiply, divide)

### 📦 **Resources**
- **Key-Value Store**: In-memory storage with get/set/list/delete operations
- **REST API**: HTTP endpoints for easy testing and integration

### 🎯 **Prompts**
- **Code Review**: Advanced code review templates with language-specific guidelines
- **Customizable**: Support for different programming languages and focus areas

### 🚀 **Transport Modes**
- **stdio**: Standard MCP protocol over stdin/stdout
- **HTTP**: REST API endpoints for testing and debugging
- **SSE**: Server-Sent Events for real-time communication

### 🏗️ **Architecture**
- **Modular Design**: Clean separation of concerns
- **Production Ready**: Comprehensive error handling and logging
- **Type Safety**: Full type hints throughout the codebase
- **Backend Agnostic**: Supports both FastMCP and standard MCP backends

## 📋 Requirements

- **Python 3.9+**
- **MCP Package**: `pip install mcp`
- **Optional**: FastAPI and Uvicorn for HTTP endpoints

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/mcpbase/mcpbase.git
cd mcpbase

# Install dependencies
pip install -r requirements.txt

# Run self-tests
python server.py --self-test

# Start the server
python server.py
```

### Basic Usage

```bash
# Start MCP server (stdio mode) - default
python server.py

# Start HTTP server for testing
python server.py --http

# Start SSE server
python server.py --sse

# Run comprehensive self-tests
python server.py --self-test

# Show help
python server.py --help
```

## 📖 Usage Examples

### MCP Protocol (stdio)

```bash
# Start the MCP server
python server.py

# Example JSON-RPC 2.0 initialize message
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0.0"}}}' | python server.py
```

### HTTP API

```bash
# Start HTTP server
python server.py --http

# Health check
curl http://localhost:8000/health

# List available tools
curl -X POST http://localhost:8000/tools/list

# Invoke echo tool
curl -X POST http://localhost:8000/tools/invoke \\
     -H "Content-Type: application/json" \\
     -d '{
       "name": "tools.echo", 
       "arguments": {"message": "Hello MCPBase!"}
     }'

# Use calculator
curl -X POST http://localhost:8000/tools/invoke \\
     -H "Content-Type: application/json" \\
     -d '{
       "name": "tools.calculator", 
       "arguments": {"operation": "add", "a": 15, "b": 25}
     }'

# Get resource
curl -X POST http://localhost:8000/resources/get \\
     -H "Content-Type: application/json" \\
     -d '{"uri": "kv://example_key"}'

# Set resource value
curl -X POST http://localhost:8000/resources/set \\
     -H "Content-Type: application/json" \\
     -d '{"key": "my_key", "value": "my_value"}'
```

### Server-Sent Events (SSE)

```bash
# Start SSE server
python server.py --sse

# Connect to SSE endpoint
curl http://localhost:8000/sse
```

## 🏗️ Project Structure

```
mcpbase/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── server.py                # Main entry point
│
├── mcpbase/                 # Main package
│   ├── __init__.py          # Package initialization
│   ├── server.py            # Core server implementation
│   │
│   ├── config/              # Configuration management
│   │   └── __init__.py      # Server settings and registries
│   │
│   ├── tools/               # Tool implementations
│   │   ├── __init__.py      # Tool exports
│   │   ├── basic_tools.py   # Echo and reverse tools
│   │   └── math_tools.py    # Calculator tool
│   │
│   ├── prompts/             # Prompt templates
│   │   ├── __init__.py      # Prompt exports
│   │   └── development_prompts.py  # Code review prompts
│   │
│   └── utils/               # Utility modules
│       ├── __init__.py      # Utility exports
│       ├── logging_setup.py # Logging configuration
│       ├── mcp_backends.py  # MCP backend detection
│       ├── resources.py     # Resource implementations
│       └── validation.py    # Data validation classes
```

## ⚙️ Configuration

MCPBase uses environment variables for configuration. Copy `.env.example` to `.env` and modify values as needed:

```bash
cp .env.example .env
```

### Environment Variables

```bash
# Server settings
MCPBASE_SERVER_NAME="MCPBase Server"
MCPBASE_SERVER_VERSION="1.0.0"

# Network settings
MCPBASE_DEFAULT_HOST="0.0.0.0"
MCPBASE_DEFAULT_HTTP_PORT=8000

# Development settings
MCPBASE_DEBUG=false
MCPBASE_RELOAD=false

# Logging
MCPBASE_LOG_LEVEL="INFO"
```

## 🔧 Development

### Adding New Tools

1. Create a new tool function in `mcpbase/tools/`:

```python
# mcpbase/tools/my_tools.py
async def my_custom_tool(input_param: str) -> Dict[str, Any]:
    """My custom tool implementation."""
    return ToolResult.success(f"Processed: {input_param}").to_dict()
```

2. Register the tool in `mcpbase/config/__init__.py`:

```python
TOOL_REGISTRY = {
    # existing tools...
    "my_tool": {
        "name": "tools.my_tool",
        "description": "My custom tool",
        "module": "mcpbase.tools.my_tools", 
        "function": "my_custom_tool"
    }
}
```

3. Update the server registration in `mcpbase/server.py`

### Adding New Resources

Resources are managed through the `KeyValueStore` class in `mcpbase/utils/resources.py`. You can extend this or create new resource classes following the same pattern.

### Adding New Prompts

1. Create prompt functions in `mcpbase/prompts/`:

```python
# mcpbase/prompts/my_prompts.py
async def my_prompt_template(param: str = "default") -> str:
    """Generate my custom prompt."""
    return f"Custom prompt with {param}"
```

2. Register in `mcpbase/config/__init__.py` and update server registration.

## 🧪 Testing

MCPBase includes comprehensive self-tests:

```bash
# Run all tests
python server.py --self-test

# Expected output:
# ✓ Server initialization successful
# ✓ KV store operations working  
# ✓ Tool imports successful
# ✓ Echo tool working
# ✓ Reverse tool working
# ✓ Calculator tool working
# ✓ Code review prompt working
# ✓ Configuration valid
# 🎉 All self-tests passed successfully!
```

### Manual Testing

Test individual components:

```python
# Test tools directly
import asyncio
from mcpbase.tools import echo_tool, calculator_tool

async def test():
    result = await echo_tool("Hello World")
    print(result)
    
    calc_result = await calculator_tool("multiply", 6, 7)
    print(calc_result)

asyncio.run(test())
```

## 🔌 API Reference

### Tools

#### Echo Tool
- **Name**: `tools.echo`
- **Parameters**: `message: str`
- **Returns**: Echoed message with timestamp

#### Reverse Tool  
- **Name**: `tools.reverse`
- **Parameters**: `text: str`
- **Returns**: Reversed text with metadata

#### Calculator Tool
- **Name**: `tools.calculator` 
- **Parameters**: `operation: str, a: float, b: float`
- **Operations**: `add`, `subtract`, `multiply`, `divide`
- **Returns**: Calculation result

### Resources

#### Key-Value Store
- **URI**: `kv://`
- **Operations**: get, set, list, delete
- **Format**: JSON

### Prompts

#### Code Review
- **Name**: `code_review`
- **Parameters**: `code: str, language: str, focus: str`
- **Returns**: Formatted code review template

## 🚀 Production Deployment

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "server.py", "--http"]
```

### Environment Variables

```bash
# Production settings
MCPBASE_DEBUG=false
MCPBASE_RELOAD=false
MCPBASE_ENABLE_FASTAPI=true
```

### Systemd Service

```ini
[Unit]
Description=MCPBase Server
After=network.target

[Service]
Type=simple
User=mcpbase
WorkingDirectory=/opt/mcpbase
ExecStart=/usr/bin/python3 server.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Development Setup

```bash
# Development installation
git clone https://github.com/mcpbase/mcpbase.git
cd mcpbase
pip install -r requirements.txt

# Enable development mode
export MCPBASE_DEBUG=true
export MCPBASE_RELOAD=true

# Run tests
python server.py --self-test
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Model Context Protocol](https://modelcontextprotocol.io/) - The protocol specification
- [Anthropic](https://www.anthropic.com/) - For creating the MCP standard
- [FastMCP](https://github.com/phasellm/fastmcp) - FastMCP backend support

## 📚 Resources

- [Model Context Protocol Specification](https://spec.modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [FastMCP Documentation](https://phasellm.github.io/fastmcp/)

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/mcpbase/mcpbase/issues)
- **Discussions**: [GitHub Discussions](https://github.com/mcpbase/mcpbase/discussions)
- **Documentation**: [Wiki](https://github.com/mcpbase/mcpbase/wiki)

---

**MCPBase** - Building the future of AI assistant integrations, one protocol at a time. 🚀