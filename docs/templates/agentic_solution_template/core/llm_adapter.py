#!/usr/bin/env python3
"""
LLM Adapter for LangChain Integration

Adapts LLMClientManager to work with LangChain/LangGraph by creating
LangChain-compatible LLM instances using the configured provider.

Author: chronosnehal
Date: [YYYY-MM-DD]
"""

import os
import logging
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class LangChainLLMAdapter:
    """
    Adapter to create LangChain LLM instances from LLMClientManager.
    
    This adapter reads the LLM_PROVIDER environment variable and creates
    the appropriate LangChain LLM instance using the provider's API key.
    """
    
    @staticmethod
    def create_llm(
        provider: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7
    ):
        """
        Create LangChain LLM instance based on provider.
        
        Args:
            provider: Provider name (openai, anthropic, gemini, claude, azure)
                     If None, reads from LLM_PROVIDER env var
            model: Model name (if None, uses default for provider)
            temperature: Temperature for generation
        
        Returns:
            LangChain LLM instance
        
        Raises:
            ValueError: If provider is not supported or API key is missing
        """
        # Get provider from env if not specified
        if provider is None:
            provider = os.getenv("LLM_PROVIDER", "openai").lower()
        
        # Map provider names
        provider_map = {
            "openai": "openai",
            "anthropic": "anthropic",
            "claude": "anthropic",
            "gemini": "gemini",
            "google": "gemini",
            "azure": "azure"
        }
        
        normalized_provider = provider_map.get(provider, provider)
        
        # Get API key for provider
        api_key = LangChainLLMAdapter._get_api_key(normalized_provider)
        
        if not api_key:
            raise ValueError(
                f"API key not found for provider '{provider}'. "
                f"Please set the appropriate environment variable."
            )
        
        # Create LangChain LLM instance
        if normalized_provider == "openai":
            from langchain_openai import ChatOpenAI
            default_model = model or os.getenv("OPENAI_MODEL", "gpt-4")
            logger.info(f"Creating OpenAI LLM: {default_model}")
            return ChatOpenAI(
                model=default_model,
                temperature=temperature,
                api_key=api_key
            )
        
        elif normalized_provider == "anthropic":
            from langchain_anthropic import ChatAnthropic
            default_model = model or os.getenv("ANTHROPIC_MODEL", "claude-3-opus-20240229")
            logger.info(f"Creating Anthropic LLM: {default_model}")
            return ChatAnthropic(
                model=default_model,
                temperature=temperature,
                api_key=api_key
            )
        
        elif normalized_provider == "gemini":
            from langchain_google_genai import ChatGoogleGenerativeAI
            default_model = model or os.getenv("GOOGLE_MODEL", "gemini-pro")
            logger.info(f"Creating Google Gemini LLM: {default_model}")
            return ChatGoogleGenerativeAI(
                model=default_model,
                temperature=temperature,
                google_api_key=api_key
            )
        
        elif normalized_provider == "azure":
            from langchain_openai import AzureChatOpenAI
            endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
            if not endpoint:
                raise ValueError("AZURE_OPENAI_ENDPOINT not set for Azure provider")
            default_model = model or os.getenv("AZURE_OPENAI_MODEL", "gpt-4")
            logger.info(f"Creating Azure OpenAI LLM: {default_model}")
            return AzureChatOpenAI(
                azure_endpoint=endpoint,
                azure_deployment=default_model,
                api_key=api_key,
                api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2023-05-15"),
                temperature=temperature
            )
        
        else:
            raise ValueError(f"Unsupported provider: {provider}")
    
    @staticmethod
    def _get_api_key(provider: str) -> Optional[str]:
        """Get API key for provider from environment variables."""
        key_map = {
            "openai": "OPENAI_API_KEY",
            "anthropic": "ANTHROPIC_API_KEY",
            "gemini": "GOOGLE_API_KEY",
            "google": "GOOGLE_API_KEY",
            "azure": "AZURE_OPENAI_API_KEY"
        }
        
        env_var = key_map.get(provider)
        if env_var:
            return os.getenv(env_var)
        return None
    
    @staticmethod
    def get_available_providers() -> list[str]:
        """Get list of available providers based on environment variables."""
        available = []
        
        if os.getenv("OPENAI_API_KEY"):
            available.append("openai")
        if os.getenv("ANTHROPIC_API_KEY"):
            available.append("anthropic")
        if os.getenv("GOOGLE_API_KEY"):
            available.append("gemini")
        if os.getenv("AZURE_OPENAI_API_KEY") and os.getenv("AZURE_OPENAI_ENDPOINT"):
            available.append("azure")
        
        return available

