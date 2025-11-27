# LLMClientManager Guide

**Author:** chronosnehal

Centralized manager for multiple LLM providers in ThinkCraft. Provides a unified interface for OpenAI, Azure, Gemini, Claude, and OpenRouter.

---

## Purpose

The `LLMClientManager` provides:
- **Unified Interface:** Same API for all LLM providers
- **Easy Switching:** Change providers without code changes
- **Centralized Configuration:** Manage API keys in one place
- **Sync & Async Support:** Both synchronous and asynchronous calls
- **Error Handling:** Consistent error handling across providers

---

## Supported Providers

| Provider | Models | API Key Required |
|----------|--------|------------------|
| **OpenAI** | GPT-3.5, GPT-4, GPT-4 Turbo | `OPENAI_API_KEY` |
| **Azure OpenAI** | GPT-3.5, GPT-4 | `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT` |
| **Google Gemini** | Gemini Pro | `GOOGLE_API_KEY` |
| **Anthropic Claude** | Claude 3 (Opus, Sonnet, Haiku) | `ANTHROPIC_API_KEY` |
| **OpenRouter** | Multiple models | `OPENROUTER_API_KEY` |

---

## Configuration

### 1. Environment Variables

Create `.env` file in repository root:

```bash
# OpenAI
OPENAI_API_KEY=sk-your-openai-key-here

# Azure OpenAI
AZURE_OPENAI_API_KEY=your-azure-key-here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/

# Google Gemini
GOOGLE_API_KEY=your-google-api-key-here

# Anthropic Claude
ANTHROPIC_API_KEY=your-anthropic-key-here

# OpenRouter
OPENROUTER_API_KEY=your-openrouter-key-here
```

### 2. Load Environment

The manager automatically loads environment variables:

```python
from app.utils.llm_client_manager import LLMClientManager

# Automatically loads .env and registers available providers
manager = LLMClientManager()
```

---

## Basic Usage

### Synchronous Calls

```python
from app.utils.llm_client_manager import LLMClientManager

# Initialize manager
manager = LLMClientManager()

# Generate with OpenAI
response = manager.generate(
    provider="openai",
    prompt="Explain quantum computing in simple terms",
    model="gpt-4",
    temperature=0.7
)

print(response)
```

### Asynchronous Calls

```python
from app.utils.llm_client_manager import LLMClientManager

# Initialize manager
manager = LLMClientManager()

# Generate asynchronously
response = await manager.generate_async(
    provider="openai",
    prompt="Explain quantum computing in simple terms",
    model="gpt-4",
    temperature=0.7
)

print(response)
```

---

## Provider-Specific Usage

### OpenAI

```python
response = manager.generate(
    provider="openai",
    prompt="Your prompt here",
    model="gpt-4",           # or "gpt-3.5-turbo", "gpt-4-turbo"
    temperature=0.7,
    max_tokens=1000
)
```

**Available Models:**
- `gpt-3.5-turbo` - Fast, cost-effective
- `gpt-4` - Most capable
- `gpt-4-turbo` - Faster GPT-4

### Azure OpenAI

```python
response = manager.generate(
    provider="azure",
    prompt="Your prompt here",
    model="gpt-4",           # Deployment name in Azure
    temperature=0.7
)
```

**Note:** Model name should match your Azure deployment name.

### Google Gemini

```python
response = manager.generate(
    provider="gemini",
    prompt="Your prompt here",
    model="gemini-pro",      # or "gemini-pro-vision"
    temperature=0.7
)
```

**Available Models:**
- `gemini-pro` - Text generation
- `gemini-pro-vision` - Multimodal (text + images)

### Anthropic Claude

```python
response = manager.generate(
    provider="claude",
    prompt="Your prompt here",
    model="claude-3-opus-20240229",  # or sonnet, haiku
    temperature=0.7,
    max_tokens=1024
)
```

**Available Models:**
- `claude-3-opus-20240229` - Most capable
- `claude-3-sonnet-20240229` - Balanced
- `claude-3-haiku-20240307` - Fast and cost-effective

### OpenRouter

```python
response = manager.generate(
    provider="openrouter",
    prompt="Your prompt here",
    model="openai/gpt-4",    # Specify provider/model
    temperature=0.7
)
```

**Available Models:** Many! Check [OpenRouter docs](https://openrouter.ai/docs)

---

## Advanced Usage

### Custom Parameters

```python
response = manager.generate(
    provider="openai",
    prompt="Write a haiku about coding",
    model="gpt-4",
    temperature=0.9,         # Higher for creativity
    max_tokens=100,          # Limit response length
    top_p=0.95,             # Nucleus sampling
    frequency_penalty=0.5,   # Reduce repetition
    presence_penalty=0.5     # Encourage diversity
)
```

### Batch Processing

```python
prompts = [
    "Explain machine learning",
    "Explain deep learning",
    "Explain reinforcement learning"
]

responses = []
for prompt in prompts:
    response = manager.generate(
        provider="openai",
        prompt=prompt,
        model="gpt-3.5-turbo"
    )
    responses.append(response)
```

### Async Batch Processing

```python
import asyncio

async def process_batch(prompts: list[str]) -> list[str]:
    manager = LLMClientManager()
    
    tasks = [
        manager.generate_async(
            provider="openai",
            prompt=prompt,
            model="gpt-3.5-turbo"
        )
        for prompt in prompts
    ]
    
    responses = await asyncio.gather(*tasks)
    return responses

# Usage
prompts = ["Prompt 1", "Prompt 2", "Prompt 3"]
responses = await process_batch(prompts)
```

---

## Error Handling

```python
from app.utils.llm_client_manager import LLMClientManager
import logging

logger = logging.getLogger(__name__)
manager = LLMClientManager()

try:
    response = manager.generate(
        provider="openai",
        prompt="Your prompt",
        model="gpt-4"
    )
    print(response)
    
except ValueError as e:
    # Provider not registered or invalid parameters
    logger.error(f"Configuration error: {e}")
    
except Exception as e:
    # API errors, network issues, etc.
    logger.error(f"Generation failed: {e}")
    # Fallback to different provider
    response = manager.generate(
        provider="gemini",
        prompt="Your prompt"
    )
```

---

## Best Practices

### 1. Use Appropriate Models

```python
# For simple tasks: Use cheaper, faster models
response = manager.generate(
    provider="openai",
    model="gpt-3.5-turbo",  # Fast and cheap
    prompt="Summarize this text"
)

# For complex tasks: Use more capable models
response = manager.generate(
    provider="openai",
    model="gpt-4",          # More capable
    prompt="Analyze this complex data"
)
```

### 2. Adjust Temperature

```python
# For factual, deterministic outputs
response = manager.generate(
    provider="openai",
    prompt="What is 2+2?",
    temperature=0.0  # Deterministic
)

# For creative outputs
response = manager.generate(
    provider="openai",
    prompt="Write a creative story",
    temperature=0.9  # More creative
)
```

### 3. Implement Retry Logic

```python
import time

def generate_with_retry(manager, prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            return manager.generate(
                provider="openai",
                prompt=prompt
            )
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            logger.warning(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(2 ** attempt)  # Exponential backoff
```

### 4. Monitor Token Usage

```python
def count_tokens(text: str) -> int:
    """Approximate token count."""
    return len(text.split()) * 1.3  # Rough estimate

prompt = "Your prompt here"
estimated_tokens = count_tokens(prompt)
logger.info(f"Estimated tokens: {estimated_tokens}")

response = manager.generate(provider="openai", prompt=prompt)
```

### 5. Cache Responses

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_generate(prompt: str, provider: str = "openai") -> str:
    """Cache LLM responses for repeated queries."""
    manager = LLMClientManager()
    return manager.generate(provider=provider, prompt=prompt)

# Subsequent calls with same prompt use cache
response1 = cached_generate("What is AI?")
response2 = cached_generate("What is AI?")  # Uses cache
```

---

## Integration Examples

### In GenAI Solutions

```python
from app.utils.llm_client_manager import LLMClientManager

class TextSummarizer:
    def __init__(self, provider: str = "openai"):
        self.manager = LLMClientManager()
        self.provider = provider
    
    def summarize(self, text: str, max_length: int = 100) -> str:
        """Summarize text using LLM."""
        prompt = f"Summarize this text in {max_length} words: {text}"
        
        return self.manager.generate(
            provider=self.provider,
            prompt=prompt,
            model="gpt-3.5-turbo"
        )
```

### In Agentic Systems

```python
from app.utils.llm_client_manager import LLMClientManager

class AgentOrchestrator:
    def __init__(self, provider: str = "openai"):
        self.manager = LLMClientManager()
        self.provider = provider
    
    async def execute(self, query: str) -> str:
        """Execute agent workflow."""
        # Perceive
        perception = await self.manager.generate_async(
            provider=self.provider,
            prompt=f"Analyze: {query}",
            temperature=0.3
        )
        
        # Reason
        reasoning = await self.manager.generate_async(
            provider=self.provider,
            prompt=f"Plan for: {perception}",
            temperature=0.7
        )
        
        # Act
        action = await self.manager.generate_async(
            provider=self.provider,
            prompt=f"Execute: {reasoning}",
            temperature=0.5
        )
        
        return action
```

---

## Troubleshooting

### Issue: "Provider not registered"

**Cause:** API key not set in `.env`

**Solution:**
```bash
# Check .env file
cat .env | grep OPENAI_API_KEY

# Add missing key
echo "OPENAI_API_KEY=your-key-here" >> .env
```

### Issue: API Rate Limits

**Solution:** Implement rate limiting and backoff

```python
import time
from functools import wraps

def rate_limit(calls_per_minute=60):
    min_interval = 60.0 / calls_per_minute
    last_called = [0.0]
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            left_to_wait = min_interval - elapsed
            if left_to_wait > 0:
                time.sleep(left_to_wait)
            ret = func(*args, **kwargs)
            last_called[0] = time.time()
            return ret
        return wrapper
    return decorator

@rate_limit(calls_per_minute=30)
def generate_limited(manager, prompt):
    return manager.generate(provider="openai", prompt=prompt)
```

### Issue: Timeout Errors

**Solution:** Increase timeout or use async

```python
# Use async for better timeout handling
try:
    response = await asyncio.wait_for(
        manager.generate_async(provider="openai", prompt=prompt),
        timeout=30.0  # 30 second timeout
    )
except asyncio.TimeoutError:
    logger.error("Request timed out")
```

---

## Performance Tips

### 1. Use Async for Multiple Calls
```python
# Faster: Parallel execution
responses = await asyncio.gather(
    manager.generate_async(provider="openai", prompt=prompt1),
    manager.generate_async(provider="openai", prompt=prompt2),
    manager.generate_async(provider="openai", prompt=prompt3)
)
```

### 2. Choose Right Model
```python
# Fast tasks: Use GPT-3.5
response = manager.generate(provider="openai", model="gpt-3.5-turbo")

# Complex tasks: Use GPT-4
response = manager.generate(provider="openai", model="gpt-4")
```

### 3. Optimize Prompts
```python
# Bad: Verbose prompt
prompt = "I would like you to please analyze this text and provide..."

# Good: Concise prompt
prompt = "Analyze this text: ..."
```

---

## Quick Reference

```python
# Initialize
from app.utils.llm_client_manager import LLMClientManager
manager = LLMClientManager()

# Sync call
response = manager.generate(
    provider="openai",
    prompt="Your prompt",
    model="gpt-4",
    temperature=0.7
)

# Async call
response = await manager.generate_async(
    provider="openai",
    prompt="Your prompt"
)

# Error handling
try:
    response = manager.generate(provider="openai", prompt="...")
except ValueError as e:
    logger.error(f"Config error: {e}")
except Exception as e:
    logger.error(f"API error: {e}")
```

---

**Use LLMClientManager for all LLM interactions in ThinkCraft!**
