#!/usr/bin/env python3
"""
Simple Code Generator - GenAI Solution Implementation

Description: Simple code generation system using LLM integration for Python and JavaScript.

This solution uses LLM capabilities to generate code snippets from natural language
descriptions. Supports Python and JavaScript with basic validation and error handling.

Dependencies: app.utils.llm_client_manager
Time Complexity: O(1) for processing + O(n) for LLM generation
Space Complexity: O(m) where m = size of generated code
Author: chronosnehal
Date: 2025-11-27
"""

from app.utils.llm_client_manager import LLMClientManager
from typing import Optional, Dict, Any
import re
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SimpleCodeGenerator:
    """
    Simple code generator using LLM integration.
    
    This class generates code snippets from natural language prompts using
    LLMClientManager. Supports Python and JavaScript languages.
    
    Attributes:
        manager: LLMClientManager instance
        provider: Selected LLM provider
        model: Model name to use
    """
    
    # Language-specific syntax patterns for basic validation
    SYNTAX_PATTERNS = {
        "python": [r'def\s+\w+\s*\(', r'class\s+\w+', r'import\s+\w+', r'=\s*\w+'],
        "javascript": [r'function\s+\w+\s*\(', r'const\s+\w+\s*=', r'=>', r'class\s+\w+']
    }
    
    def __init__(
        self,
        provider: str = "openai",
        model: Optional[str] = None
    ):
        """
        Initialize simple code generator.
        
        Args:
            provider: LLM provider name (openai, azure, gemini, claude, openrouter)
            model: Model name (defaults to provider's default)
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        self.manager = LLMClientManager()
        self.provider = provider
        
        # Set default models per provider
        default_models = {
            "openai": "gpt-4",
            "azure": "gpt-4",
            "gemini": "gemini-pro",
            "claude": "claude-3-opus-20240229",
            "openrouter": "openai/gpt-4"
        }
        
        self.model = model or default_models.get(provider, "gpt-4")
        
        logger.info(f"SimpleCodeGenerator initialized with provider: {provider}, model: {self.model}")
    
    def _build_prompt(
        self,
        prompt: str,
        language: str,
        include_comments: bool,
        include_explanation: bool
    ) -> str:
        """
        Build prompt for LLM code generation.
        
        Args:
            prompt: User's natural language description
            language: Target programming language
            include_comments: Whether to include comments
            include_explanation: Whether to include explanation
        
        Returns:
            Formatted prompt string
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        lang_name = "Python" if language == "python" else "JavaScript"
        
        system_prompt = f"""You are an expert {lang_name} programmer. Generate clean, well-structured {lang_name} code based on user requirements.

Guidelines:
- Write idiomatic {lang_name} code
- Follow best practices for {lang_name}
- Include proper error handling when appropriate
- Use clear variable and function names
"""
        
        if include_comments:
            system_prompt += "- Add comments explaining key logic\n"
        
        if language == "python":
            system_prompt += "- Use type hints where appropriate\n"
            system_prompt += "- Include docstrings for functions\n"
        elif language == "javascript":
            system_prompt += "- Use modern ES6+ syntax\n"
            system_prompt += "- Add JSDoc comments for functions\n"
        
        system_prompt += "\nOutput Format:\n"
        system_prompt += "CODE:\n```" + language + "\n[your code here]\n```\n"
        
        if include_explanation:
            system_prompt += "\nEXPLANATION:\n[Brief explanation of the code]\n"
        
        user_prompt = f"Generate {lang_name} code for: {prompt}"
        
        return f"{system_prompt}\n\n{user_prompt}"
    
    def _extract_code(self, response: str, language: str) -> str:
        """
        Extract code block from LLM response.
        
        Args:
            response: Raw LLM response
            language: Programming language
        
        Returns:
            Extracted code string
        """
        # Try to find code block with language tag
        pattern = rf'CODE:\s*```{language}\s*\n(.*?)```'
        match = re.search(pattern, response, re.DOTALL)
        
        if match:
            return match.group(1).strip()
        
        # Try to find any code block
        pattern = r'```[\w]*\s*\n(.*?)```'
        match = re.search(pattern, response, re.DOTALL)
        
        if match:
            return match.group(1).strip()
        
        # If no code block found, return response as-is
        return response.strip()
    
    def _extract_explanation(self, response: str) -> str:
        """
        Extract explanation from LLM response.
        
        Args:
            response: Raw LLM response
        
        Returns:
            Extracted explanation string
        """
        pattern = r'EXPLANATION:\s*(.*?)(?=\n(?:CODE:|$))'
        match = re.search(pattern, response, re.DOTALL)
        
        if match:
            return match.group(1).strip()
        
        return ""
    
    def _validate_code_basic(self, code: str, language: str) -> tuple[bool, Optional[str]]:
        """
        Basic validation of generated code.
        
        Args:
            code: Generated code
            language: Programming language
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not code or not code.strip():
            return False, "Generated code is empty"
        
        # Check for balanced brackets
        brackets = {'(': ')', '[': ']', '{': '}'}
        stack = []
        for char in code:
            if char in brackets.keys():
                stack.append(char)
            elif char in brackets.values():
                if not stack or brackets[stack.pop()] != char:
                    return False, "Unbalanced brackets/parentheses"
        
        if stack:
            return False, "Unclosed brackets/parentheses"
        
        # Check for language-specific patterns
        patterns = self.SYNTAX_PATTERNS.get(language, [])
        if patterns:
            has_valid_pattern = any(re.search(pattern, code) for pattern in patterns)
            if not has_valid_pattern:
                return False, f"Code doesn't match expected {language} syntax patterns"
        
        return True, None
    
    def generate(
        self,
        prompt: str,
        language: str,
        include_explanation: bool = True,
        include_comments: bool = True
    ) -> Dict[str, Any]:
        """
        Generate code from natural language prompt.
        
        Args:
            prompt: Natural language description of desired code
            language: Programming language ("python" or "javascript")
            include_explanation: Whether to include explanation
            include_comments: Whether to include comments
        
        Returns:
            Dictionary with generated code and metadata
        
        Raises:
            ValueError: If input is invalid
        
        Time Complexity: O(1) for processing + O(n) for LLM generation
        Space Complexity: O(m) where m = size of generated code
        
        Examples:
            >>> generator = SimpleCodeGenerator()
            >>> result = generator.generate(
            ...     "Create a function to add two numbers",
            ...     "python"
            ... )
            >>> print(result["code"])
        """
        # Validate input
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty")
        
        if len(prompt) < 10:
            raise ValueError("Prompt must be at least 10 characters")
        
        if len(prompt) > 500:
            raise ValueError("Prompt must be at most 500 characters")
        
        if language not in ["python", "javascript"]:
            raise ValueError(f"Unsupported language: {language}. Supported: python, javascript")
        
        logger.info(f"Generating {language} code for prompt: {prompt[:50]}...")
        
        try:
            # Build prompt
            full_prompt = self._build_prompt(
                prompt=prompt.strip(),
                language=language,
                include_comments=include_comments,
                include_explanation=include_explanation
            )
            
            # Generate code using LLM
            response = self.manager.generate(
                provider=self.provider,
                prompt=full_prompt,
                model=self.model,
                temperature=0.7
            )
            
            # Extract code and explanation
            code = self._extract_code(response, language)
            explanation = self._extract_explanation(response) if include_explanation else ""
            
            # Basic validation
            is_valid, error_msg = self._validate_code_basic(code, language)
            
            if not is_valid:
                logger.warning(f"Code validation failed: {error_msg}")
                return {
                    "success": False,
                    "code": code,
                    "language": language,
                    "explanation": explanation,
                    "error": f"Validation warning: {error_msg}"
                }
            
            logger.info(f"Code generation successful: {len(code)} characters")
            
            return {
                "success": True,
                "code": code,
                "language": language,
                "explanation": explanation if include_explanation else "",
                "error": None
            }
            
        except ValueError as e:
            logger.error(f"Validation error: {e}")
            raise
        
        except Exception as e:
            logger.error(f"Code generation failed: {e}")
            return {
                "success": False,
                "code": "",
                "language": language,
                "explanation": "",
                "error": f"Generation failed: {str(e)}"
            }


def main():
    """Demonstrate simple code generator with examples."""
    generator = SimpleCodeGenerator(provider="openai")
    
    print("=" * 80)
    print("Simple Code Generator - Examples")
    print("=" * 80)
    
    # Example 1: Python function
    print("\n" + "-" * 80)
    print("Example 1: Python Function - Factorial")
    print("-" * 80)
    
    try:
        result1 = generator.generate(
            prompt="Create a function to calculate factorial of a number",
            language="python",
            include_explanation=True,
            include_comments=True
        )
        
        if result1["success"]:
            print(f"\n✓ Generated Code:\n{result1['code']}\n")
            if result1["explanation"]:
                print(f"Explanation: {result1['explanation']}\n")
        else:
            print(f"✗ Error: {result1['error']}\n")
    
    except Exception as e:
        print(f"✗ Exception: {e}\n")
    
    # Example 2: JavaScript function
    print("\n" + "-" * 80)
    print("Example 2: JavaScript Function - String Reversal")
    print("-" * 80)
    
    try:
        result2 = generator.generate(
            prompt="Create a function to reverse a string",
            language="javascript",
            include_explanation=True,
            include_comments=False
        )
        
        if result2["success"]:
            print(f"\n✓ Generated Code:\n{result2['code']}\n")
            if result2["explanation"]:
                print(f"Explanation: {result2['explanation']}\n")
        else:
            print(f"✗ Error: {result2['error']}\n")
    
    except Exception as e:
        print(f"✗ Exception: {e}\n")
    
    # Example 3: Error case - invalid language
    print("\n" + "-" * 80)
    print("Example 3: Error Case - Invalid Language")
    print("-" * 80)
    
    try:
        result3 = generator.generate(
            prompt="Create a function",
            language="java",  # Invalid - only python/javascript supported
            include_explanation=True
        )
        print(f"Result: {result3}\n")
    except ValueError as e:
        print(f"✓ Caught expected error: {e}\n")
    
    # Example 4: Error case - empty prompt
    print("\n" + "-" * 80)
    print("Example 4: Error Case - Empty Prompt")
    print("-" * 80)
    
    try:
        result4 = generator.generate(
            prompt="",
            language="python"
        )
        print(f"Result: {result4}\n")
    except ValueError as e:
        print(f"✓ Caught expected error: {e}\n")
    
    print("=" * 80)
    print("Examples completed!")
    print("=" * 80)


if __name__ == "__main__":
    main()

