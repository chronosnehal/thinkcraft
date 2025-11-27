#!/usr/bin/env python3
"""
[Problem Title] - GenAI Solution Implementation

Description: [Brief description of the GenAI solution]

This solution uses LLM capabilities to [describe what it does].
Supports multiple LLM providers through LLMClientManager.

Dependencies: app.utils.llm_client_manager, openai, anthropic, google-generativeai
Author: chronosnehal
Date: [YYYY-MM-DD]
"""

from app.utils.llm_client_manager import LLMClientManager
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
import logging
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class PromptTemplate:
    """Template for structuring prompts."""
    system_message: str
    user_template: str
    
    def format(self, **kwargs) -> str:
        """
        Format the user template with provided kwargs.
        
        Args:
            **kwargs: Variables to insert into template
        
        Returns:
            Formatted prompt string
        """
        return self.user_template.format(**kwargs)


class GenAISolver:
    """
    GenAI-based solution for [Problem Name].
    
    This class uses LLM capabilities to solve [describe problem].
    Supports multiple providers: OpenAI, Azure, Gemini, Claude, OpenRouter.
    
    Attributes:
        manager: LLMClientManager instance
        provider: Selected LLM provider
        model: Model name to use
        temperature: Temperature for generation
    """
    
    def __init__(
        self,
        provider: str = "openai",
        model: Optional[str] = None,
        temperature: float = 0.7
    ):
        """
        Initialize GenAI solver.
        
        Args:
            provider: LLM provider name (openai, azure, gemini, claude, openrouter)
            model: Model name (defaults to provider's default)
            temperature: Temperature for generation (0.0 to 1.0)
        
        Raises:
            ValueError: If provider is not supported
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        self.manager = LLMClientManager()
        self.provider = provider
        self.temperature = temperature
        
        # Set default models per provider
        default_models = {
            "openai": "gpt-4",
            "azure": "gpt-4",
            "gemini": "gemini-pro",
            "claude": "claude-3-opus-20240229",
            "openrouter": "openai/gpt-4"
        }
        
        self.model = model or default_models.get(provider, "gpt-4")
        
        # Initialize prompt templates
        self.prompts = self._initialize_prompts()
        
        logger.info(f"Initialized GenAI solver with provider: {provider}, model: {self.model}")
    
    def _initialize_prompts(self) -> Dict[str, PromptTemplate]:
        """
        Initialize prompt templates for different tasks.
        
        Returns:
            Dictionary of prompt templates
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        return {
            "main_task": PromptTemplate(
                system_message="You are an expert assistant for [task description].",
                user_template="Task: {task}\n\nInput: {input_data}\n\nProvide a detailed response."
            ),
            "validation": PromptTemplate(
                system_message="You validate and verify outputs.",
                user_template="Validate this output: {output}\n\nCriteria: {criteria}"
            )
        }
    
    def solve(
        self,
        input_data: str,
        task_type: str = "main_task",
        **kwargs
    ) -> str:
        """
        Solve the problem using LLM.
        
        Args:
            input_data: Input text or data
            task_type: Type of task (corresponds to prompt template)
            **kwargs: Additional parameters for prompt formatting
        
        Returns:
            Generated response from LLM
        
        Raises:
            ValueError: If input is invalid or task_type not found
            Exception: If LLM generation fails
        
        Time Complexity: O(1) - API call (not counting LLM processing)
        Space Complexity: O(n) - Where n is response size
        
        Examples:
            >>> solver = GenAISolver(provider="openai")
            >>> result = solver.solve("Analyze this text", task_type="main_task")
            >>> print(result)
        """
        # Validate input
        if not input_data:
            raise ValueError("Input data cannot be empty")
        
        if task_type not in self.prompts:
            raise ValueError(f"Unknown task type: {task_type}")
        
        # Build prompt
        prompt = self._build_prompt(input_data, task_type, **kwargs)
        logger.info(f"Generated prompt for task: {task_type}")
        logger.debug(f"Prompt: {prompt[:100]}...")
        
        # Generate response
        try:
            response = self.manager.generate(
                provider=self.provider,
                prompt=prompt,
                model=self.model,
                temperature=self.temperature
            )
            
            logger.info("Successfully generated response")
            logger.debug(f"Response: {response[:100]}...")
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise
    
    async def solve_async(
        self,
        input_data: str,
        task_type: str = "main_task",
        **kwargs
    ) -> str:
        """
        Async version of solve method.
        
        Args:
            input_data: Input text or data
            task_type: Type of task
            **kwargs: Additional parameters
        
        Returns:
            Generated response from LLM
        
        Time Complexity: O(1) - API call
        Space Complexity: O(n) - Response size
        """
        if not input_data:
            raise ValueError("Input data cannot be empty")
        
        prompt = self._build_prompt(input_data, task_type, **kwargs)
        
        try:
            response = await self.manager.generate_async(
                provider=self.provider,
                prompt=prompt,
                model=self.model,
                temperature=self.temperature
            )
            
            logger.info("Successfully generated async response")
            return response
            
        except Exception as e:
            logger.error(f"Error in async generation: {e}")
            raise
    
    def _build_prompt(
        self,
        input_data: str,
        task_type: str,
        **kwargs
    ) -> str:
        """
        Build prompt from template and input data.
        
        Args:
            input_data: Input data
            task_type: Type of task
            **kwargs: Additional template variables
        
        Returns:
            Formatted prompt string
        
        Time Complexity: O(n) - Where n is prompt length
        Space Complexity: O(n)
        """
        template = self.prompts[task_type]
        
        # Prepare template variables
        template_vars = {
            "input_data": input_data,
            "task": kwargs.get("task", "Process the input"),
            **kwargs
        }
        
        # Format prompt
        user_prompt = template.format(**template_vars)
        
        # Combine system and user messages
        full_prompt = f"{template.system_message}\n\n{user_prompt}"
        
        return full_prompt
    
    def batch_solve(
        self,
        inputs: List[str],
        task_type: str = "main_task",
        **kwargs
    ) -> List[str]:
        """
        Process multiple inputs in batch.
        
        Args:
            inputs: List of input strings
            task_type: Type of task
            **kwargs: Additional parameters
        
        Returns:
            List of responses
        
        Time Complexity: O(k) - Where k is number of inputs
        Space Complexity: O(k*n) - Where n is average response size
        """
        if not inputs:
            raise ValueError("Inputs list cannot be empty")
        
        logger.info(f"Processing batch of {len(inputs)} inputs")
        
        results = []
        for i, input_data in enumerate(inputs):
            try:
                result = self.solve(input_data, task_type, **kwargs)
                results.append(result)
                logger.debug(f"Processed input {i+1}/{len(inputs)}")
            except Exception as e:
                logger.error(f"Error processing input {i+1}: {e}")
                results.append(f"Error: {str(e)}")
        
        logger.info(f"Batch processing completed: {len(results)} results")
        return results
    
    def extract_structured_output(
        self,
        response: str,
        output_format: str = "json"
    ) -> Dict[str, Any]:
        """
        Extract structured data from LLM response.
        
        Args:
            response: Raw LLM response
            output_format: Expected format (json, yaml, etc.)
        
        Returns:
            Parsed structured data
        
        Raises:
            ValueError: If parsing fails
        
        Time Complexity: O(n) - Where n is response length
        Space Complexity: O(n)
        """
        try:
            if output_format == "json":
                # Try to find JSON in response
                start = response.find("{")
                end = response.rfind("}") + 1
                
                if start != -1 and end > start:
                    json_str = response[start:end]
                    return json.loads(json_str)
                else:
                    raise ValueError("No JSON found in response")
            
            else:
                raise ValueError(f"Unsupported format: {output_format}")
                
        except Exception as e:
            logger.error(f"Error extracting structured output: {e}")
            raise ValueError(f"Failed to parse {output_format}: {e}")


# Standalone function for simple use cases
def generate_with_llm(
    prompt: str,
    provider: str = "openai",
    model: Optional[str] = None,
    temperature: float = 0.7
) -> str:
    """
    Simple function to generate text with LLM.
    
    Args:
        prompt: Prompt text
        provider: LLM provider
        model: Model name
        temperature: Temperature
    
    Returns:
        Generated text
    
    Time Complexity: O(1) - API call
    Space Complexity: O(n) - Response size
    
    Examples:
        >>> result = generate_with_llm("Write a haiku about coding")
        >>> print(result)
    """
    if not prompt:
        raise ValueError("Prompt cannot be empty")
    
    manager = LLMClientManager()
    
    default_models = {
        "openai": "gpt-4",
        "azure": "gpt-4",
        "gemini": "gemini-pro",
        "claude": "claude-3-opus-20240229",
        "openrouter": "openai/gpt-4"
    }
    
    model = model or default_models.get(provider, "gpt-4")
    
    try:
        response = manager.generate(
            provider=provider,
            prompt=prompt,
            model=model,
            temperature=temperature
        )
        return response
    except Exception as e:
        logger.error(f"Error in generation: {e}")
        raise


def main():
    """
    Main function to demonstrate GenAI solution with examples.
    """
    print("=" * 60)
    print("GenAI Solution: [Problem Title]")
    print("=" * 60)
    
    # Example 1: Basic usage with OpenAI
    print("\n--- Example 1: Basic Usage (OpenAI) ---")
    try:
        solver = GenAISolver(provider="openai", model="gpt-4", temperature=0.7)
        
        input_text = "Explain what a binary search tree is in simple terms."
        result = solver.solve(input_text, task="Explain concept")
        
        print(f"Input: {input_text}")
        print(f"Output: {result[:200]}...")
        
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 1b: Using dataset
    print("\n--- Example 1b: Using Dataset ---")
    try:
        # Load text data from datasets directory
        # data_path = "datasets/genai/text/reviews.txt"
        # with open(data_path, 'r') as f:
        #     texts = f.readlines()
        
        # For demo, use sample texts
        texts = [
            "This product is amazing! Highly recommend.",
            "Not satisfied with the quality.",
            "Great value for money."
        ]
        
        solver = GenAISolver(provider="openai")
        for i, text in enumerate(texts[:2], 1):  # Process first 2
            result = solver.solve(text, task="Sentiment analysis")
            print(f"\nText {i}: {text}")
            print(f"Analysis: {result[:100]}...")
        
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 2: Using different provider
    print("\n--- Example 2: Using Claude ---")
    try:
        solver_claude = GenAISolver(provider="claude", temperature=0.5)
        
        input_text = "Write a Python function to reverse a string."
        result = solver_claude.solve(input_text, task="Code generation")
        
        print(f"Input: {input_text}")
        print(f"Output: {result[:200]}...")
        
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 3: Batch processing
    print("\n--- Example 3: Batch Processing ---")
    try:
        solver = GenAISolver(provider="openai")
        
        inputs = [
            "What is machine learning?",
            "What is deep learning?",
            "What is reinforcement learning?"
        ]
        
        results = solver.batch_solve(inputs)
        
        for i, (inp, res) in enumerate(zip(inputs, results), 1):
            print(f"\nInput {i}: {inp}")
            print(f"Output {i}: {res[:100]}...")
        
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 4: Simple function usage
    print("\n--- Example 4: Simple Function Usage ---")
    try:
        prompt = "List 3 benefits of using type hints in Python."
        result = generate_with_llm(prompt, provider="openai")
        
        print(f"Prompt: {prompt}")
        print(f"Result: {result}")
        
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()

