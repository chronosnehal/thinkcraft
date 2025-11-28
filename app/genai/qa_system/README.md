# Question Answering System

> **GenAI Problem** - Question answering system using LLM integration

A comprehensive question answering system that answers questions based on provided context documents. Handles various question types, provides confidence scoring, supports different answer formats, implements citation mechanisms, and handles complex multi-part questions using LLMClientManager.

**Author:** chronosnehal  
**Category:** GenAI  
**Difficulty:** Medium  
**Time:** 25-30 minutes

---

## 🎯 Features

- ✅ **Multiple Question Types**: Factual, Analytical, Comparative, Multi-part
- ✅ **Answer Formats**: Short, Detailed, Bullet points
- ✅ **Confidence Scoring**: 0.0 to 1.0 confidence scores
- ✅ **Citation Mechanism**: Source references with excerpts
- ✅ **Multi-Context Support**: Handle multiple context documents
- ✅ **LLM Integration**: Uses LLMClientManager for multi-provider support
- ✅ **Question Type Detection**: Auto-detects question type

---

## 📁 Project Structure

```
qa_system/
├── question_qa_system.md   # Problem description
├── qa_system.py           # Solution implementation
└── README.md              # This file
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
python app/genai/qa_system/qa_system.py
```

---

## 💻 Usage Examples

### Basic Usage

```python
from app.genai.qa_system.qa_system import QASystem

# Initialize QA system
qa = QASystem(provider="openai")

# Answer a question
result = qa.answer(
    question="What is Python?",
    context="Python is a high-level programming language known for its simplicity.",
    answer_format="short",
    include_citations=True
)

print(f"Answer: {result['answer']}")
print(f"Confidence: {result['confidence']}")
```

### Multiple Context Documents

```python
context = [
    "Python is a programming language.",
    "Python features dynamic typing and readability.",
    "Python is used for web development and data science."
]

result = qa.answer(
    question="What are Python's main features?",
    context=context,
    answer_format="bullets"
)
```

### Detailed Answer

```python
result = qa.answer(
    question="Why is machine learning important?",
    context="Machine learning enables businesses to analyze data and automate decisions.",
    answer_format="detailed",
    max_length=300
)
```

---

## 📖 API Reference

### `QASystem`

#### Constructor

```python
qa = QASystem(
    provider: str = "openai",
    model: Optional[str] = None
)
```

**Parameters:**
- `provider`: LLM provider (openai, azure, gemini, claude, openrouter)
- `model`: Model name (defaults to provider's default)

#### `answer()`

```python
result = qa.answer(
    question: str,
    context: Union[str, List[str]],
    answer_format: str = "detailed",
    include_citations: bool = True,
    max_length: int = 200,
    question_type: Optional[str] = None
) -> Dict[str, Any]
```

**Parameters:**
- `question`: Question to answer (10-500 characters)
- `context`: Context document(s) (string or list of strings)
- `answer_format`: "short", "detailed", or "bullets" (default: "detailed")
- `include_citations`: Whether to include citations (default: True)
- `max_length`: Maximum answer length in words (default: 200)
- `question_type`: Optional type hint (auto-detected if None)

**Returns:**
```python
{
    "success": bool,
    "answer": str,
    "confidence": float,  # 0.0 to 1.0
    "citations": [
        {
            "source_index": int,
            "text": str,
            "relevance_score": float
        }
    ],
    "question_type": str,
    "metadata": {
        "context_sources": int,
        "answer_length": int,
        "answer_format": str,
        "processing_time": float
    },
    "error": str | None
}
```

**Raises:**
- `ValueError`: If input is invalid

---

## 🎯 Question Types

### Factual
Direct questions about facts ("What is...", "Who is...", "When...", "Where...").

```python
result = qa.answer(
    "What is the capital of France?",
    context="France's capital is Paris."
)
```

### Analytical
Questions requiring explanation ("Why...", "How...", "Explain...").

```python
result = qa.answer(
    "Why is Python popular?",
    context="Python is popular due to its simplicity and readability."
)
```

### Comparative
Questions comparing things ("Compare...", "Difference between...").

```python
result = qa.answer(
    "What is the difference between Python and Java?",
    context=["Python uses dynamic typing.", "Java uses static typing."]
)
```

### Multi-Part
Questions with multiple parts.

```python
result = qa.answer(
    "What is Python and how does it compare to Java?",
    context=["Python is a language.", "Java is also a language."]
)
```

---

## 📝 Answer Formats

### Short
Concise 1-2 sentence answers.

```python
result = qa.answer(
    question="...",
    context="...",
    answer_format="short"
)
```

### Detailed
Comprehensive, detailed explanations.

```python
result = qa.answer(
    question="...",
    context="...",
    answer_format="detailed"
)
```

### Bullets
Structured bullet point format.

```python
result = qa.answer(
    question="...",
    context="...",
    answer_format="bullets"
)
```

---

## 📚 Citations

The system automatically extracts citations from answers:

```python
result = qa.answer(
    question="...",
    context=["Document 1...", "Document 2..."],
    include_citations=True
)

for citation in result["citations"]:
    print(f"Source {citation['source_index'] + 1}: {citation['text']}")
    print(f"Relevance: {citation['relevance_score']}")
```

---

## 🧪 Examples

### Example 1: Factual Question

```python
result = qa.answer(
    question="What is the capital of France?",
    context="France is a country. Its capital is Paris.",
    answer_format="short"
)

print(result["answer"])  # "The capital of France is Paris."
print(result["confidence"])  # 0.95
```

### Example 2: Multi-Part Question

```python
context = [
    "Python is a programming language.",
    "Java is also a programming language.",
    "Python uses dynamic typing, Java uses static typing."
]

result = qa.answer(
    question="What are Python's features and how does it compare to Java?",
    context=context,
    answer_format="bullets"
)
```

### Example 3: Analytical Question

```python
result = qa.answer(
    question="Why is machine learning important?",
    context="Machine learning enables data analysis and automation.",
    answer_format="detailed",
    max_length=300
)
```

---

## 🏗️ Architecture

### Question Answering Flow

```
Question + Context → Type Detection → Context Extraction → Prompt Building → LLM Generation → Citation Extraction → Confidence Calculation → Formatted Answer
```

### Key Components

1. **Question Type Detection**: Identifies question type from patterns
2. **Context Extraction**: Finds relevant context passages
3. **Prompt Engineering**: Builds format-specific prompts
4. **LLM Integration**: Uses LLMClientManager for answer generation
5. **Citation Extraction**: Identifies source references
6. **Confidence Calculation**: Estimates answer confidence
7. **Answer Formatting**: Formats according to requested format

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

## 💡 Use Cases

1. **Document Q&A**: Answer questions about documents
2. **Knowledge Base**: Query knowledge bases with context
3. **Research Assistance**: Answer research questions from sources
4. **Customer Support**: Answer questions from documentation
5. **Educational**: Answer questions from course materials

---

## ⚠️ Limitations

- **Context Length**: Very long contexts may be truncated
- **Accuracy**: Depends on LLM quality and context relevance
- **Citations**: Citation extraction is pattern-based
- **Confidence**: Confidence scoring is heuristic-based
- **Multi-part**: Complex multi-part questions may need refinement

---

## 📝 Notes

- Uses lower temperature (0.3) for more accurate answers
- Question type detection uses pattern matching
- Citation extraction looks for explicit citations or keyword matching
- Confidence scoring considers citations, answer length, and keyword overlap
- Supports both single and multiple context documents

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

