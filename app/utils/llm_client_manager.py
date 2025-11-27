# app/utils/llm_client_manager.py
import os
from abc import ABC, abstractmethod
import asyncio
from dotenv import load_dotenv
load_dotenv()

# --- Base Interface ---
class BaseLLMClient(ABC):
    @abstractmethod
    def generate(self, prompt: str, **kwargs):
        pass

    @abstractmethod
    async def generate_async(self, prompt: str, **kwargs):
        pass

# --- Provider Implementations ---

# OpenAI
class OpenAIClient(BaseLLMClient):
    def __init__(self, api_key: str):
        import openai
        openai.api_key = api_key
        self.openai = openai

    def generate(self, prompt: str, **kwargs):
        response = self.openai.ChatCompletion.create(
            model=kwargs.get("model", "gpt-4"),
            messages=[{"role": "user", "content": prompt}],
            temperature=kwargs.get("temperature", 0.7)
        )
        return response.choices[0].message["content"]

    async def generate_async(self, prompt: str, **kwargs):
        return await asyncio.to_thread(self.generate, prompt, **kwargs)

# Azure OpenAI
class AzureOpenAIClient(BaseLLMClient):
    def __init__(self, api_key: str, endpoint: str):
        from openai import AzureOpenAI
        self.client = AzureOpenAI(api_key=api_key, azure_endpoint=endpoint)

    def generate(self, prompt: str, **kwargs):
        response = self.client.chat.completions.create(
            model=kwargs.get("model", "gpt-4"),
            messages=[{"role": "user", "content": prompt}],
            temperature=kwargs.get("temperature", 0.7)
        )
        return response.choices[0].message.content

    async def generate_async(self, prompt: str, **kwargs):
        return await asyncio.to_thread(self.generate, prompt, **kwargs)

# Google Gemini
class GoogleGeminiClient(BaseLLMClient):
    def __init__(self, api_key: str):
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-pro")

    def generate(self, prompt: str, **kwargs):
        response = self.model.generate_content(prompt)
        return response.text

    async def generate_async(self, prompt: str, **kwargs):
        return await asyncio.to_thread(self.generate, prompt, **kwargs)

# OpenRouter
class OpenRouterClient(BaseLLMClient):
    def __init__(self, api_key: str):
        import requests
        self.api_key = api_key
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"

    def generate(self, prompt: str, **kwargs):
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {
            "model": kwargs.get("model", "openai/gpt-4"),
            "messages": [{"role": "user", "content": prompt}],
            "temperature": kwargs.get("temperature", 0.7)
        }
        import requests
        response = requests.post(self.base_url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    async def generate_async(self, prompt: str, **kwargs):
        return await asyncio.to_thread(self.generate, prompt, **kwargs)

# Anthropic Claude
class AnthropicClaudeClient(BaseLLMClient):
    def __init__(self, api_key: str):
        import anthropic
        self.client = anthropic.Anthropic(api_key=api_key)

    def generate(self, prompt: str, **kwargs):
        response = self.client.messages.create(
            model=kwargs.get("model", "claude-3-opus-20240229"),
            max_tokens=kwargs.get("max_tokens", 1024),
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text

    async def generate_async(self, prompt: str, **kwargs):
        return await asyncio.to_thread(self.generate, prompt, **kwargs)

# --- Manager ---
class LLMClientManager:
    def __init__(self):
        self.clients = {}
        self._load_default_clients()

    def _load_default_clients(self):
        if os.getenv("OPENAI_API_KEY"):
            self.register_client("openai", OpenAIClient(os.getenv("OPENAI_API_KEY")))
        if os.getenv("AZURE_OPENAI_API_KEY") and os.getenv("AZURE_OPENAI_ENDPOINT"):
            self.register_client("azure", AzureOpenAIClient(os.getenv("AZURE_OPENAI_API_KEY"), os.getenv("AZURE_OPENAI_ENDPOINT")))
        if os.getenv("GOOGLE_API_KEY"):
            self.register_client("gemini", GoogleGeminiClient(os.getenv("GOOGLE_API_KEY")))
        if os.getenv("OPENROUTER_API_KEY"):
            self.register_client("openrouter", OpenRouterClient(os.getenv("OPENROUTER_API_KEY")))
        if os.getenv("ANTHROPIC_API_KEY"):
            self.register_client("claude", AnthropicClaudeClient(os.getenv("ANTHROPIC_API_KEY")))

    def register_client(self, name: str, client: BaseLLMClient):
        self.clients[name] = client

    def generate(self, provider: str, prompt: str, **kwargs):
        if provider not in self.clients:
            raise ValueError(f"Provider '{provider}' not registered.")
        return self.clients[provider].generate(prompt, **kwargs)

    async def generate_async(self, provider: str, prompt: str, **kwargs):
        if provider not in self.clients:
            raise ValueError(f"Provider '{provider}' not registered.")
        return await self.clients[provider].generate_async(prompt, **kwargs)