"""
Validation and Data Classes
===========================

Contains validation classes and data structures used throughout MCPBase.
"""

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class ToolResult:
    """
    Standardized tool result format for consistent response structure.
    
    Attributes:
        status: Status of the operation ("success", "error")
        result: The actual result data
        error: Error message if status is "error"
        metadata: Additional metadata about the operation
    """
    status: str
    result: Any
    error: Optional[str] = None
    metadata: Optional[dict] = None
    
    def is_success(self) -> bool:
        """Check if the result represents a successful operation."""
        return self.status == "success"
    
    def is_error(self) -> bool:
        """Check if the result represents an error."""
        return self.status == "error"
    
    @classmethod
    def success(cls, result: Any, metadata: Optional[dict] = None) -> "ToolResult":
        """Create a successful result."""
        return cls(status="success", result=result, metadata=metadata)
    
    @classmethod
    def error(cls, error_msg: str, metadata: Optional[dict] = None) -> "ToolResult":
        """Create an error result."""
        return cls(status="error", result=None, error=error_msg, metadata=metadata)