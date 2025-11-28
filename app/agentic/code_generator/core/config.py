#!/usr/bin/env python3
"""
Configuration Management

Centralized configuration for the code generator agentic system.

Author: chronosnehal
Date: 2025-11-27
"""

import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings."""
    
    # LLM Provider Configuration
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "openai").lower()
    
    # OpenAI Settings
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4")
    
    # Anthropic Settings
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    ANTHROPIC_MODEL: str = os.getenv("ANTHROPIC_MODEL", "claude-3-opus-20240229")
    
    # Google Gemini Settings
    GOOGLE_API_KEY: Optional[str] = os.getenv("GOOGLE_API_KEY")
    GOOGLE_MODEL: str = os.getenv("GOOGLE_MODEL", "gemini-pro")
    
    # Azure OpenAI Settings
    AZURE_OPENAI_API_KEY: Optional[str] = os.getenv("AZURE_OPENAI_API_KEY")
    AZURE_OPENAI_ENDPOINT: Optional[str] = os.getenv("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_MODEL: str = os.getenv("AZURE_OPENAI_MODEL", "gpt-4")
    AZURE_OPENAI_API_VERSION: str = os.getenv("AZURE_OPENAI_API_VERSION", "2023-05-15")
    
    # Application Settings
    APP_NAME: str = "AI Code Generator"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Agent Settings
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))
    DEFAULT_TEMPERATURE: float = float(os.getenv("DEFAULT_TEMPERATURE", "0.7"))
    
    @classmethod
    def get_available_providers(cls) -> list[str]:
        """Get list of available providers based on API keys."""
        available = []
        if cls.OPENAI_API_KEY:
            available.append("openai")
        if cls.ANTHROPIC_API_KEY:
            available.append("anthropic")
        if cls.GOOGLE_API_KEY:
            available.append("gemini")
        if cls.AZURE_OPENAI_API_KEY and cls.AZURE_OPENAI_ENDPOINT:
            available.append("azure")
        return available


settings = Settings()

