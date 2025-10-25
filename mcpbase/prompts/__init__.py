"""
Prompts Module for MCPBase
==========================

Contains all MCP prompt implementations organized by category.
"""

from .development_prompts import code_review_prompt

__all__ = [
    "code_review_prompt"
]