"""
Development-Related Prompts
===========================

Contains prompts for software development tasks like code review,
documentation generation, and code analysis.
"""

from datetime import datetime
from ..utils.logging_setup import get_logger

logger = get_logger("prompts.development")


async def code_review_prompt(
    code: str = "# Your code here",
    language: str = "python", 
    focus: str = "general"
) -> str:
    """
    Generate a comprehensive code review prompt template.
    
    Creates a structured code review request with the provided code,
    language context, and specific focus areas for review.
    
    Args:
        code: The source code to be reviewed
        language: Programming language of the code (default: "python")
        focus: Specific focus area for the review (default: "general")
               Examples: "security", "performance", "readability", "best-practices"
    
    Returns:
        Formatted code review prompt as a string
        
    Example:
        >>> prompt = await code_review_prompt(
        ...     code="def hello(): print('world')",
        ...     language="python",
        ...     focus="best-practices"
        ... )
    """
    logger.info(f"Generating code review prompt for {language} code, focus: {focus}")
    
    # Determine language-specific guidelines
    language_guidelines = _get_language_guidelines(language)
    
    # Create focus-specific checklist items
    focus_items = _get_focus_checklist(focus, language)
    
    # Generate the complete prompt
    prompt_template = f"""# Code Review Request

## Code to Review ({language.title()})
```{language}
{code}
```

## Review Focus
**Primary Focus:** {focus.title()}

## Code Analysis Checklist

### General Code Quality
- Code clarity and readability
- Proper naming conventions
- Comment quality and documentation
- Code structure and organization

### {focus.title()} Focus
{focus_items}

### {language.title()}-Specific Considerations
{language_guidelines}

## Detailed Review Guidelines

Please provide a thorough review covering:

1. **Code Quality Assessment**
   - Rate the overall code quality (1-10)
   - Identify any code smells or anti-patterns
   - Suggest improvements for better maintainability

2. **Functionality Review**
   - Verify the code logic is correct
   - Check for potential bugs or edge cases
   - Assess error handling adequacy

3. **Performance Considerations**
   - Identify performance bottlenecks
   - Suggest optimizations if applicable
   - Consider memory usage and efficiency

4. **Security Analysis**
   - Check for security vulnerabilities
   - Assess input validation and sanitization
   - Review authentication and authorization

5. **Best Practices Compliance**
   - Adherence to {language} coding standards
   - Use of appropriate design patterns
   - Consistency with team conventions

## Additional Context
- **Language:** {language}
- **Focus Area:** {focus}
- **Review Generated:** {datetime.now().isoformat()}
- **Code Length:** {len(code)} characters

## Review Output Format
Please structure your review with:
- Executive summary
- Detailed findings with line references
- Prioritized recommendations
- Suggested improvements with code examples
"""

    logger.debug(f"Generated code review prompt ({len(prompt_template)} characters)")
    return prompt_template


def _get_language_guidelines(language: str) -> str:
    """Get language-specific review guidelines."""
    guidelines = {
        "python": """- PEP 8 compliance (formatting, naming)
- Proper use of Python idioms and features
- Type hints usage and correctness
- Exception handling best practices
- Use of context managers where appropriate
- List comprehensions vs loops optimization""",
        
        "javascript": """- ESLint compliance and modern ES6+ usage
- Proper async/await vs Promise usage
- Variable scoping (let/const vs var)
- Function declaration best practices
- Error handling with try/catch
- Memory leak prevention""",
        
        "typescript": """- Type safety and proper type annotations
- Interface vs type alias usage
- Generic type usage and constraints
- Strict mode compliance
- Proper import/export patterns
- Null safety and optional chaining""",
        
        "java": """- Java coding conventions compliance
- Proper use of access modifiers
- Exception handling hierarchy
- Resource management (try-with-resources)
- Collection framework usage
- Thread safety considerations""",
        
        "rust": """- Memory safety without garbage collection
- Ownership and borrowing rules compliance
- Error handling with Result types
- Pattern matching usage
- Lifetime annotations correctness
- Performance and zero-cost abstractions"""
    }
    
    return guidelines.get(language.lower(), """- Language-specific best practices
- Standard library usage
- Error handling patterns
- Performance considerations
- Security best practices
- Code maintainability""")


def _get_focus_checklist(focus: str, language: str) -> str:
    """Get focus-specific checklist items."""
    focus_checklists = {
        "security": """- Input validation and sanitization
- Authentication and authorization checks
- SQL injection and XSS prevention
- Sensitive data handling
- Cryptographic implementation review
- Access control verification""",
        
        "performance": """- Algorithm complexity analysis
- Memory usage optimization
- I/O operation efficiency
- Caching strategies implementation
- Database query optimization
- Resource cleanup and management""",
        
        "readability": """- Clear variable and function naming
- Appropriate code comments
- Logical code organization
- Consistent formatting and style
- Self-documenting code practices
- Complexity reduction opportunities""",
        
        "best-practices": f"""- {language} idioms and conventions
- Design pattern implementation
- SOLID principles adherence
- DRY (Don't Repeat Yourself) compliance
- Separation of concerns
- Testability and modularity""",
        
        "maintainability": """- Code modularity and reusability
- Clear separation of concerns
- Documentation completeness
- Test coverage adequacy
- Refactoring opportunities
- Technical debt assessment"""
    }
    
    return focus_checklists.get(focus.lower(), """- General code quality
- Logic correctness
- Error handling
- Documentation quality
- Maintainability aspects
- Performance considerations""")