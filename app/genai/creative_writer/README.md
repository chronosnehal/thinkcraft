# Creative Writing System

> **GenAI Problem** - Creative writing system using LLM integration

A comprehensive creative writing system that generates various types of creative content based on prompts, themes, and style requirements. Supports stories, poems, articles, essays, dialogues, and descriptions with customizable styles, tones, and lengths.

**Author:** chronosnehal  
**Category:** GenAI  
**Difficulty:** Medium  
**Time:** 25-30 minutes

---

## 🎯 Features

- ✅ **Multiple Content Types**: Story, Poem, Article, Essay, Dialogue, Description
- ✅ **Writing Styles**: Formal, Casual, Poetic, Narrative, Descriptive, Conversational
- ✅ **Themes & Tones**: Customizable themes and tones for creative control
- ✅ **Length Control**: Short, Medium, or Long content generation
- ✅ **LLM Integration**: Uses LLMClientManager for multi-provider support
- ✅ **Metadata**: Word count and character count tracking
- ✅ **Error Handling**: Comprehensive validation and error messages

---

## 📁 Project Structure

```
creative_writer/
├── question_creative_writer.md   # Problem description
├── creative_writer.py            # Solution implementation
└── README.md                     # This file
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
python app/genai/creative_writer/creative_writer.py
```

---

## 💻 Usage Examples

### Basic Usage

```python
from app.genai.creative_writer.creative_writer import CreativeWriter

# Initialize writer
writer = CreativeWriter(provider="openai")

# Generate a short story
result = writer.generate(
    prompt="A young explorer discovers a hidden city",
    content_type="story",
    theme="adventure",
    style="narrative",
    length="short",
    tone="mysterious"
)

if result["success"]:
    print(result["content"])
    print(f"Word count: {result['metadata']['word_count']}")
else:
    print(f"Error: {result['error']}")
```

### Generate a Poem

```python
result = writer.generate(
    prompt="The changing seasons",
    content_type="poem",
    theme="nature",
    style="poetic",
    length="short",
    tone="contemplative"
)

print(result["content"])
```

### Generate an Article

```python
result = writer.generate(
    prompt="The benefits of reading",
    content_type="article",
    style="formal",
    length="medium",
    tone="informative"
)

print(result["content"])
```

---

## 📖 API Reference

### `CreativeWriter`

#### Constructor

```python
writer = CreativeWriter(
    provider: str = "openai",
    model: Optional[str] = None
)
```

**Parameters:**
- `provider`: LLM provider (openai, azure, gemini, claude, openrouter)
- `model`: Model name (defaults to provider's default)

#### `generate()`

```python
result = writer.generate(
    prompt: str,
    content_type: str,
    theme: Optional[str] = None,
    style: Optional[str] = None,
    length: str = "medium",
    tone: Optional[str] = None,
    additional_requirements: Optional[str] = None
) -> Dict[str, Any]
```

**Parameters:**
- `prompt`: Main writing prompt (10-500 characters)
- `content_type`: One of ["story", "poem", "article", "essay", "dialogue", "description"]
- `theme`: Optional theme (e.g., "adventure", "romance", "mystery")
- `style`: One of ["formal", "casual", "poetic", "narrative", "descriptive", "conversational"]
- `length`: One of ["short", "medium", "long"] (default: "medium")
- `tone`: Optional tone (e.g., "humorous", "serious", "melancholic")
- `additional_requirements`: Optional extra instructions (max 200 characters)

**Returns:**
```python
{
    "success": bool,
    "content": str,
    "content_type": str,
    "metadata": {
        "theme": str | None,
        "style": str | None,
        "length": str | None,
        "tone": str | None,
        "word_count": int,
        "character_count": int
    },
    "error": str | None
}
```

**Raises:**
- `ValueError`: If input is invalid

---

## 📝 Content Types

### Story
Narrative with characters, plot, and setting. Best for creative storytelling.

```python
writer.generate(
    "A magical forest adventure",
    content_type="story",
    theme="fantasy",
    style="narrative"
)
```

### Poem
Poetic verse with rhythm, imagery, and emotional expression.

```python
writer.generate(
    "The ocean at sunset",
    content_type="poem",
    style="poetic",
    tone="melancholic"
)
```

### Article
Informative, structured, and factual content.

```python
writer.generate(
    "Climate change impacts",
    content_type="article",
    style="formal",
    tone="informative"
)
```

### Essay
Argumentative or expository writing with clear structure.

```python
writer.generate(
    "The importance of education",
    content_type="essay",
    style="formal",
    length="medium"
)
```

### Dialogue
Conversation between characters.

```python
writer.generate(
    "Two friends planning a trip",
    content_type="dialogue",
    style="conversational"
)
```

### Description
Vivid, detailed scene or object description.

```python
writer.generate(
    "A bustling marketplace",
    content_type="description",
    style="descriptive"
)
```

---

## 🎨 Writing Styles

| Style | Description | Best For |
|-------|-------------|----------|
| **Formal** | Professional, structured, academic | Articles, Essays |
| **Casual** | Conversational, relaxed, friendly | Stories, Dialogues |
| **Poetic** | Figurative language, imagery, rhythm | Poems, Descriptions |
| **Narrative** | Storytelling, chronological flow | Stories |
| **Descriptive** | Vivid details, sensory language | Descriptions, Stories |
| **Conversational** | Dialogue-like, engaging | Dialogues, Articles |

---

## 📏 Length Guidelines

| Length | Word Count | Best For |
|--------|-----------|----------|
| **Short** | 200-500 words | Poems, Short stories, Brief articles |
| **Medium** | 500-1000 words | Stories, Articles, Essays |
| **Long** | 1000-2000 words | Detailed stories, Long-form articles |

---

## 🧪 Examples

### Example 1: Adventure Story

```python
result = writer.generate(
    prompt="A treasure hunter finds an ancient map",
    content_type="story",
    theme="adventure",
    style="narrative",
    length="medium",
    tone="exciting"
)
```

### Example 2: Nature Poem

```python
result = writer.generate(
    prompt="Spring flowers blooming",
    content_type="poem",
    theme="nature",
    style="poetic",
    length="short",
    tone="joyful"
)
```

### Example 3: Formal Article

```python
result = writer.generate(
    prompt="The future of artificial intelligence",
    content_type="article",
    style="formal",
    length="long",
    tone="informative",
    additional_requirements="Include statistics and examples"
)
```

---

## 🏗️ Architecture

### Simple Flow

```
User Request → Input Validation → Prompt Engineering → LLM Call → Content Extraction → Metadata Calculation → Response
```

### Key Components

1. **Input Validation**: Validates prompt, content_type, style, length
2. **Prompt Engineering**: Builds content-type and style-specific prompts
3. **LLM Integration**: Uses LLMClientManager for generation
4. **Content Extraction**: Cleans and extracts content from LLM response
5. **Metadata Calculation**: Counts words and characters
6. **Error Handling**: Handles failures gracefully

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

- **Content Types**: 6 types supported (story, poem, article, essay, dialogue, description)
- **Quality**: Depends on LLM provider and model
- **Length**: Approximate word counts (LLM may vary)
- **No Editing**: Single-pass generation (no refinement)

---

## 💡 Tips

1. **Be Specific**: Clear prompts produce better results
2. **Match Style**: Choose style appropriate for content type
3. **Use Themes**: Themes help guide the creative direction
4. **Adjust Length**: Longer content needs more time to generate
5. **Experiment**: Try different combinations for best results

---

## 📝 Notes

- Uses higher temperature (0.8) for more creative output
- Content extraction handles various LLM response formats
- Metadata includes word/character counts for reference
- Always validate generated content before use

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

