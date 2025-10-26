"""
Resource Management Utilities
=============================

Contains resource implementations for the MCP server.
"""

import json
from typing import Dict, Any, Optional
from ..config import DEFAULT_KV_DATA
from ..utils.logging_setup import get_logger

logger = get_logger("resources")


class KeyValueStore:
    """
    In-memory key-value store resource for MCP server.
    
    Provides get, set, list, and delete operations on a simple
    key-value data structure.
    """
    
    def __init__(self, initial_data: Optional[Dict[str, Any]] = None):
        """
        Initialize the key-value store.
        
        Args:
            initial_data: Initial data to populate the store
        """
        self.data = initial_data.copy() if initial_data else DEFAULT_KV_DATA.copy()
        logger.debug(f"Initialized KV store with {len(self.data)} items")
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get a value by key.
        
        Args:
            key: The key to look up
            
        Returns:
            The value if found, None otherwise
        """
        value = self.data.get(key)
        logger.debug(f"KV GET: {key} -> {'found' if value is not None else 'not found'}")
        return value
    
    def set(self, key: str, value: Any) -> bool:
        """
        Set a key-value pair.
        
        Args:
            key: The key to set
            value: The value to store
            
        Returns:
            True if successful
        """
        self.data[key] = value
        logger.debug(f"KV SET: {key} -> {type(value).__name__}")
        return True
    
    def delete(self, key: str) -> bool:
        """
        Delete a key-value pair.
        
        Args:
            key: The key to delete
            
        Returns:
            True if key existed and was deleted, False otherwise
        """
        if key in self.data:
            del self.data[key]
            logger.debug(f"KV DELETE: {key} -> deleted")
            return True
        logger.debug(f"KV DELETE: {key} -> not found")
        return False
    
    def list_keys(self) -> list[str]:
        """
        List all keys in the store.
        
        Returns:
            List of all keys
        """
        keys = list(self.data.keys())
        logger.debug(f"KV LIST: {len(keys)} keys")
        return keys
    
    def get_info(self) -> Dict[str, Any]:
        """
        Get information about the store.
        
        Returns:
            Dictionary with store information
        """
        return {
            "description": "In-memory key-value store",
            "operations": ["get", "set", "list", "delete"],
            "current_keys": self.list_keys(),
            "count": len(self.data)
        }
    
    def to_json(self) -> str:
        """
        Convert store info to JSON string.
        
        Returns:
            JSON representation of store info
        """
        return json.dumps(self.get_info(), indent=2)