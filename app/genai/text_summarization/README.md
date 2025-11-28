# Text Summarization System

> **GenAI Problem** - Text summarization system using LLM integration

A comprehensive text summarization system that generates summaries of various lengths and formats. Supports both extractive and abstractive summarization approaches, handles different content types, and provides customizable summary styles using LLMClientManager.

**Author:** chronosnehal  
**Category:** GenAI  
**Difficulty:** Medium  
**Time:** 25-30 minutes

---

## 🎯 Features

- ✅ **Two Summary Types**: Extractive (key sentences) and Abstractive (paraphrased)
- ✅ **Multiple Lengths**: Short, Medium, Long, or custom word count
- ✅ **Various Formats**: Paragraph, Bullets, Structured
- ✅ **Customizable Styles**: Concise, Detailed, Executive, Technical
- ✅ **Key Points Extraction**: Automatically extracts key points
- ✅ **Metadata Tracking**: Compression ratios, length statistics
- ✅ **LLM Integration**: Uses LLMClientManager for multi-provider support

---

## 📁 Project Structure

```
text_summarization/
├── question_text_summarization.md   # Problem description
├── text_summarization.py           # Solution implementation
└── README.md                       # This file
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
python app/genai/text_summarization/text_summarization.py
```

---

## 💻 Usage Examples

### Basic Usage

```python
from app.genai.text_summarization.text_summarization import TextSummarizer

# Initialize summarizer
summarizer = TextSummarizer(provider="openai")

# Generate abstractive summary
result = summarizer.summarize(
    text="Long article text here...",
    summary_type="abstractive",
    length="short",
    format="paragraph"
)

print(result["summary"])
```

### Extractive Summary

```python
result = summarizer.summarize(
    text="Long document text...",
    summary_type="extractive",
    format="bullets",
    max_sentences=5
)

print(result["summary"])
```

### Executive Summary

```python
result = summarizer.summarize(
    text="Business report text...",
    summary_type="abstractive",
    length="medium",
    format="structured",
    style="executive"
)

print(result["summary"])
```

---

## 📖 API Reference

### `TextSummarizer`

#### Constructor

```python
summarizer = TextSummarizer(
    provider: str = "openai",
    model: Optional[str] = None
)
```

**Parameters:**
- `provider`: LLM provider (openai, azure, gemini, claude, openrouter)
- `model`: Model name (defaults to provider's default)

#### `summarize()`

```python
result = summarizer.summarize(
    text: str,
    summary_type: str = "abstractive",
    length: str = "medium",
    format: str = "paragraph",
    style: str = "concise",
    focus_areas: Optional[List[str]] = None,
    max_sentences: Optional[int] = None
) -> Dict[str, Any]
```

**Parameters:**
- `text`: Text to summarize (100-50000 characters)
- `summary_type`: "extractive" or "abstractive" (default: "abstractive")
- `length`: "short", "medium", "long", or integer word count (default: "medium")
- `format`: "paragraph", "bullets", "structured" (default: "paragraph")
- `style`: "concise", "detailed", "executive", "technical" (default: "concise")
- `focus_areas`: Optional list of topics to emphasize
- `max_sentences`: Maximum sentences for extractive (default: 5)

**Returns:**
```python
{
    "success": bool,
    "summary": str,
    "summary_type": str,
    "metadata": {
        "original_length": int,
        "summary_length": int,
        "compression_ratio": float,
        "length_category": str,
        "format": str,
        "style": str
    },
    "key_points": list[str],
    "error": str | None
}
```

**Raises:**
- `ValueError`: If input is invalid

---

## 📝 Summary Types

### Extractive
Selects and extracts key sentences from the original text.

```python
result = summarizer.summarize(
    text="...",
    summary_type="extractive",
    max_sentences=5
)
```

**Use Cases:**
- Quick overviews
- Preserving original wording
- Legal/document summaries

### Abstractive
Generates new summary text that paraphrases and condenses content.

```python
result = summarizer.summarize(
    text="...",
    summary_type="abstractive",
    length="short"
)
```

**Use Cases:**
- Article summaries
- Report abstracts
- Content curation

---

## 📏 Length Options

| Option | Word Count | Use Case |
|--------|-----------|----------|
| **Short** | 20-50 words | Quick overviews, headlines |
| **Medium** | 50-150 words | Standard summaries, abstracts |
| **Long** | 150-300 words | Detailed summaries, executive briefs |
| **Custom** | Integer | Specific word count requirement |

---

## 🎨 Summary Formats

### Paragraph
Continuous prose format.

```python
result = summarizer.summarize(
    text="...",
    format="paragraph"
)
```

### Bullets
Bullet point list format.

```python
result = summarizer.summarize(
    text="...",
    format="bullets"
)
```

### Structured
Organized sections (e.g., Executive Summary format).

```python
result = summarizer.summarize(
    text="...",
    format="structured",
    style="executive"
)
```

---

## 🎯 Summary Styles

### Concise
Brief, to-the-point summary focusing on essential information.

```python
result = summarizer.summarize(
    text="...",
    style="concise"
)
```

### Detailed
Comprehensive summary with context and supporting details.

```python
result = summarizer.summarize(
    text="...",
    style="detailed"
)
```

### Executive
High-level summary for decision-makers, focusing on key findings and recommendations.

```python
result = summarizer.summarize(
    text="...",
    style="executive"
)
```

### Technical
Precise summary with technical terminology and specifications.

```python
result = summarizer.summarize(
    text="...",
    style="technical"
)
```

---

## 🧪 Examples

### Example 1: Article Summary

```python
article_text = "Long article about machine learning..."

result = summarizer.summarize(
    text=article_text,
    summary_type="abstractive",
    length="short",
    format="paragraph",
    style="concise"
)

print(result["summary"])
print(f"Compression: {result['metadata']['compression_ratio']}")
```

### Example 2: Meeting Notes Summary

```python
meeting_text = "Long meeting transcript..."

result = summarizer.summarize(
    text=meeting_text,
    summary_type="extractive",
    format="bullets",
    max_sentences=10
)

for point in result["key_points"]:
    print(f"- {point}")
```

### Example 3: Research Paper Abstract

```python
paper_text = "Long research paper..."

result = summarizer.summarize(
    text=paper_text,
    summary_type="abstractive",
    length="medium",
    format="paragraph",
    style="technical"
)

print(result["summary"])
```

---

## 🏗️ Architecture

### Summarization Flow

```
Input Text → Validation → Prompt Building → LLM Generation → Summary Extraction → Formatting → Key Points Extraction → Metadata Calculation → Structured Output
```

### Key Components

1. **Input Validation**: Validates text and parameters
2. **Length Determination**: Converts length spec to word count
3. **Prompt Engineering**: Builds type/format/style-specific prompts
4. **LLM Integration**: Uses LLMClientManager for summarization
5. **Summary Extraction**: Cleans and extracts summary from response
6. **Formatting**: Formats summary according to requested format
7. **Key Points Extraction**: Extracts key points from summary
8. **Metadata Calculation**: Calculates compression ratios and statistics

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

1. **Document Summarization**: Summarize long documents and reports
2. **Article Summarization**: Create article summaries for quick reading
3. **Meeting Notes**: Summarize meeting transcripts
4. **Research Papers**: Generate paper abstracts and summaries
5. **Content Curation**: Create summaries for content aggregation

---

## ⚠️ Limitations

- **Text Length**: Very long texts (>50000 chars) may need chunking
- **Accuracy**: Depends on LLM quality and text clarity
- **Extractive Quality**: May not always select optimal sentences
- **Format Consistency**: Structured format may vary
- **Cost**: LLM API calls for each summarization

---

## 📝 Notes

- Uses moderate temperature (0.5) for balanced creativity/accuracy
- Extractive summaries preserve original wording
- Abstractive summaries paraphrase content
- Compression ratio indicates summary efficiency
- Key points extracted automatically from summary

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

