"""
Mathematical Tools Implementation
================================

Contains mathematical computation tools including basic arithmetic operations.
"""

from typing import Dict, Any, Union
from ..utils.validation import ToolResult
from ..utils.logging_setup import get_logger

logger = get_logger("tools.math")


async def calculator_tool(
    operation: str, 
    a: Union[int, float], 
    b: Union[int, float]
) -> Dict[str, Any]:
    """
    Perform basic arithmetic operations on two numbers.
    
    Supports addition, subtraction, multiplication, and division with
    proper error handling for edge cases like division by zero.
    
    Args:
        operation: The arithmetic operation to perform
                  ("add", "subtract", "multiply", "divide")
        a: First number (int or float)
        b: Second number (int or float)
        
    Returns:
        Dict containing status, calculation result, and metadata
        
    Raises:
        ValueError: For unknown operations
        ZeroDivisionError: For division by zero
        
    Example:
        >>> await calculator_tool("add", 5, 3)
        {
            "status": "success",
            "result": 8,
            "metadata": {"operation": "5 add 3 = 8"}
        }
    """
    logger.info(f"Calculator tool called: {a} {operation} {b}")
    
    try:
        # Validate operation type
        valid_operations = ["add", "subtract", "multiply", "divide"]
        if operation not in valid_operations:
            error_result = ToolResult.error(
                f"Unknown operation '{operation}'. "
                f"Valid operations: {', '.join(valid_operations)}"
            )
            return {
                "status": error_result.status,
                "result": error_result.result,
                "error": error_result.error
            }
        
        # Validate number types
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            error_result = ToolResult.error(
                f"Both operands must be numbers. Got {type(a).__name__} and {type(b).__name__}"
            )
            return {
                "status": error_result.status,
                "result": error_result.result,
                "error": error_result.error
            }
        
        # Perform the calculation
        if operation == "add":
            calc_result = a + b
        elif operation == "subtract":
            calc_result = a - b
        elif operation == "multiply":
            calc_result = a * b
        elif operation == "divide":
            if b == 0:
                error_result = ToolResult.error("Division by zero is not allowed")
                return {
                    "status": error_result.status,
                    "result": error_result.result,
                    "error": error_result.error
                }
            calc_result = a / b
        
        # Create success result with metadata
        result = ToolResult.success(
            result=calc_result,
            metadata={
                "operation": f"{a} {operation} {b} = {calc_result}",
                "operand_a": a,
                "operand_b": b,
                "operation_type": operation,
                "result_type": type(calc_result).__name__
            }
        )
        
        return {
            "status": result.status,
            "result": result.result,
            "metadata": result.metadata
        }
        
    except Exception as e:
        logger.error(f"Calculator tool error: {e}")
        error_result = ToolResult.error(f"Calculation failed: {str(e)}")
        return {
            "status": error_result.status,
            "result": error_result.result,
            "error": error_result.error
        }