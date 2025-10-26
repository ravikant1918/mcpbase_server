"""
Basic Tools Implementation
=========================

Contains basic utility tools for text processing and echo functionality.
"""

from typing import Dict, Any
from datetime import datetime
from ..utils.validation import ToolResult
from ..utils.logging_setup import get_logger

logger = get_logger("tools.basic")


async def echo_tool(message: str) -> Dict[str, Any]:
    """
    Echo back the provided message with timestamp.
    
    This tool simply returns the input message with additional metadata
    including a timestamp and confirmation of successful processing.
    
    Args:
        message: The message to echo back
        
    Returns:
        Dict containing status, echoed message, and metadata
        
    Example:
        >>> await echo_tool("Hello World")
        {
            "status": "success",
            "result": "Echo: Hello World",
            "metadata": {"timestamp": "2025-10-26T..."}
        }
    """
    logger.info(f"Echo tool called with message: {message}")
    
    try:
        result = ToolResult.success(
            result=f"Echo: {message}",
            metadata={
                "timestamp": datetime.now().isoformat(),
                "original_message": message,
                "message_length": len(message)
            }
        )
        
        return {
            "status": result.status,
            "result": result.result,
            "metadata": result.metadata
        }
        
    except Exception as e:
        logger.error(f"Echo tool error: {e}")
        error_result = ToolResult.error(f"Failed to echo message: {str(e)}")
        return {
            "status": error_result.status,
            "result": error_result.result,
            "error": error_result.error
        }


async def reverse_tool(text: str) -> Dict[str, Any]:
    """
    Reverse the provided text string.
    
    This tool takes any string input and returns it with the character
    order reversed. Includes validation and metadata about the operation.
    
    Args:
        text: The text string to reverse
        
    Returns:
        Dict containing status, reversed text, and metadata
        
    Raises:
        TypeError: If input is not a string
        
    Example:
        >>> await reverse_tool("Hello")
        {
            "status": "success", 
            "result": "olleH",
            "metadata": {"original_length": 5}
        }
    """
    logger.info(f"Reverse tool called with text: {text}")
    
    try:
        # Validate input type
        if not isinstance(text, str):
            error_result = ToolResult.error(
                f"Input must be a string, got {type(text).__name__}"
            )
            return {
                "status": error_result.status,
                "result": error_result.result,
                "error": error_result.error
            }
        
        # Perform the reversal
        reversed_text = text[::-1]
        
        result = ToolResult.success(
            result=reversed_text,
            metadata={
                "original_text": text,
                "original_length": len(text),
                "reversed_length": len(reversed_text),
                "operation": "string_reverse"
            }
        )
        
        return {
            "status": result.status,
            "result": result.result,
            "metadata": result.metadata
        }
        
    except Exception as e:
        logger.error(f"Reverse tool error: {e}")
        error_result = ToolResult.error(f"Failed to reverse text: {str(e)}")
        return {
            "status": error_result.status,
            "result": error_result.result,
            "error": error_result.error
        }