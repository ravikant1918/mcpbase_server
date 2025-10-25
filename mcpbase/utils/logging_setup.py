"""
Logging Setup Utility
=====================

Configures logging for the MCPBase server with consistent formatting
and proper log levels.
"""

import logging
import sys
from ..config import SERVER_CONFIG, ENV_CONFIG


def setup_logging() -> logging.Logger:
    """
    Setup logging configuration for the MCPBase server.
    
    Returns:
        logging.Logger: Configured logger instance
    """
    # Configure basic logging
    logging.basicConfig(
        level=getattr(logging, SERVER_CONFIG.log_level),
        format=SERVER_CONFIG.log_format,
        stream=sys.stdout
    )
    
    # Create and return logger for the package
    logger = logging.getLogger("mcpbase")
    
    if ENV_CONFIG.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug logging enabled")
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger for a specific module.
    
    Args:
        name: Module name for the logger
        
    Returns:
        logging.Logger: Logger instance for the module
    """
    return logging.getLogger(f"mcpbase.{name}")