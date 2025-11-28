# Simple Code Generator

> **GenAI Problem** - Simple code generation system using LLM integration

A straightforward code generation system that uses LLM integration to generate code snippets from natural language prompts. Supports Python and JavaScript with basic validation and error handling.

**Author:** chronosnehal  
**Category:** GenAI  
**Difficulty:** Medium  
**Time:** 20-25 minutes

---

## 🎯 Features

- ✅ **Python Support**: Generate Python functions with type hints and docstrings
- ✅ **JavaScript Support**: Generate JavaScript functions with modern ES6+ syntax
- ✅ **LLM Integration**: Uses LLMClientManager for multi-provider support
- ✅ **Error Handling**: Comprehensive validation and error messages
- ✅ **Explanations**: Optional code explanations
- ✅ **Comments**: Optional code comments

---

## 📁 Project Structure

```
simple_code_generator/
├── question_simple_code_generator.md   # Problem description
├── simple_code_generator.py            # Solution implementation
└── README.md                           # This file
```

---

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Set your LLM API key (e.g., OpenAI)
export OPENAI_API_KEY=your_api_key_here

# Or use .env file
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

### 2. Run the Solution

```bash
# From repository root
python app/genai/simple_code_generator/simple_code_generator.py
```

---

## 💻 Usage Examples

### Basic Usage

```python
from app.genai.simple_code_generator.simple_code_generator import SimpleCodeGenerator

# Initialize generator
generator = SimpleCodeGenerator(provider="openai")

# Generate Python code
result = generator.generate(
    prompt="Create a function to calculate fibonacci numbers",
    language="python",
    include_explanation=True,
    include_comments=True
)

if result["success"]:
    print(result["code"])
    print(result["explanation"])
else:
    print(f"Error: {result['error']}")
```

### Generate JavaScript Code

```python
result = generator.generate(
    prompt="Create a function to filter even numbers from an array",
    language="javascript",
    include_explanation=True
)

print(result["code"])
```

---

## 📖 API Reference

### `SimpleCodeGenerator`

#### Constructor

```python
generator = SimpleCodeGenerator(
    provider: str = "openai",
    model: Optional[str] = None
)
```

**Parameters:**
- `provider`: LLM provider (openai, azure, gemini, claude, openrouter)
- `model`: Model name (defaults to provider's default)

#### `generate()`

```python
result = generator.generate(
    prompt: str,
    language: str,
    include_explanation: bool = True,
    include_comments: bool = True
) -> Dict[str, Any]
```

**Parameters:**
- `prompt`: Natural language description (10-500 characters)
- `language`: "python" or "javascript"
- `include_explanation`: Whether to include explanation (default: True)
- `include_comments`: Whether to include comments (default: True)

**Returns:**
```python
{
    "success": bool,
    "code": str,
    "language": str,
    "explanation": str,
    "error": str | None
}
```

**Raises:**
- `ValueError`: If input is invalid

---

## 🧪 Examples

### Example 1: Python Function

**Input:**
```python
generator.generate(
    "Create a function to check if a number is prime",
    "python"
)
```

**Output:**
```python
{
    "success": True,
    "code": "def is_prime(n: int) -> bool:\n    \"\"\"Check if n is prime.\"\"\"\n    if n < 2:\n        return False\n    for i in range(2, int(n**0.5) + 1):\n        if n % i == 0:\n            return False\n    return True",
    "language": "python",
    "explanation": "This function checks if a number is prime by testing divisibility up to sqrt(n).",
    "error": None
}
```

### Example 2: JavaScript Function

**Input:**
```python
generator.generate(
    "Create a function to find the maximum value in an array",
    "javascript"
)
```

**Output:**
```python
{
    "success": True,
    "code": "function findMax(arr) {\n    return Math.max(...arr);\n}",
    "language": "javascript",
    "explanation": "Uses Math.max with spread operator to find maximum value.",
    "error": None
}
```

---

## 🏗️ Architecture

### Simple Flow

```
User Prompt → Input Validation → Prompt Engineering → LLM Call → Code Extraction → Validation → Response
```

### Key Components

1. **Input Validation**: Validates prompt length and language
2. **Prompt Engineering**: Builds language-specific prompts
3. **LLM Integration**: Uses LLMClientManager for generation
4. **Code Extraction**: Parses code blocks from LLM response
5. **Basic Validation**: Checks syntax patterns and brackets

---

## 🔧 Configuration

### Supported Providers

- **OpenAI**: GPT-4, GPT-3.5-turbo
- **Azure OpenAI**: GPT-4
- **Google Gemini**: gemini-pro
- **Anthropic Claude**: claude-3-opus-20240229
- **OpenRouter**: Various models

### Environment Variables

```bash
# Required for OpenAI
OPENAI_API_KEY=your_key

# Optional - other providers
ANTHROPIC_API_KEY=your_key
GOOGLE_API_KEY=your_key
AZURE_OPENAI_API_KEY=your_key
AZURE_OPENAI_ENDPOINT=your_endpoint
```

---

## ⚠️ Limitations

- **Languages**: Only Python and JavaScript supported
- **Complexity**: Best for simple to medium complexity functions
- **No Multi-Agent**: Single LLM call (no orchestration)
- **Basic Validation**: Syntax validation only, no execution testing

---

## 📝 Notes

- This is a simplified version for learning GenAI patterns
- For production use, consider the agentic version
- Always validate generated code before use
- Test with your specific use cases

---

## 🤝 Contributing

When extending this solution:
1. Keep it simple (no multi-agent workflow)
2. Use LLMClientManager for all LLM calls
3. Add proper error handling
4. Include example usage
5. Document complexity analysis

---

**Built with ❤️ by chronosnehal**

