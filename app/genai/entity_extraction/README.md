# Prompt-Based Entity Extraction System

> **GenAI Problem** - Entity extraction system using LLM integration with few-shot prompting

A comprehensive entity extraction system that identifies and extracts person names and dates from meeting descriptions and narrative text. Uses few-shot prompting techniques to guide an LLM in consistently extracting entities in a structured JSON format.

**Author:** chronosnehal  
**Category:** GenAI  
**Difficulty:** Medium  
**Time:** 25-30 minutes

---

## 🎯 Features

- ✅ **Person Name Extraction**: Identifies full names with titles (Dr., Mr., Professor, etc.)
- ✅ **Date Extraction**: Supports multiple formats (ISO, US, written dates)
- ✅ **Few-Shot Prompting**: Uses 4 examples to guide LLM extraction
- ✅ **Structured Output**: Returns JSON format with organized entities
- ✅ **Multiple Text Formats**: Handles meetings, narratives, emails
- ✅ **LLM Integration**: Uses LLMClientManager for multi-provider support
- ✅ **Confidence Scoring**: Provides extraction confidence levels

---

## 📁 Project Structure

```
entity_extraction/
├── question_entity_extraction.md   # Problem description
├── entity_extraction.py           # Solution implementation
└── README.md                      # This file
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
python app/genai/entity_extraction/entity_extraction.py
```

---

## 💻 Usage Examples

### Basic Usage

```python
from app.genai.entity_extraction.entity_extraction import EntityExtractor

# Initialize extractor
extractor = EntityExtractor(provider="openai")

# Extract entities
result = extractor.extract(
    text="John Smith and Sarah Johnson met on March 15, 2024.",
    entity_types=["person", "date"]
)

if result["success"]:
    print(f"Persons: {result['entities']['persons']}")
    print(f"Dates: {result['entities']['dates']}")
```

### Meeting Description

```python
text = """
The quarterly review meeting was scheduled for March 15, 2024.
John Smith, Sarah Johnson, and Michael Chen attended the meeting.
The follow-up meeting is set for April 20, 2024.
"""

result = extractor.extract(text, entity_types=["person", "date"])
print(result["entities"])
```

### Date Only Extraction

```python
result = extractor.extract(
    text="The conference is on 2024-06-15. Registration opens 05/01/2024.",
    entity_types=["date"]
)

print(f"Dates: {result['entities']['dates']}")
```

---

## 📖 API Reference

### `EntityExtractor`

#### Constructor

```python
extractor = EntityExtractor(
    provider: str = "openai",
    model: Optional[str] = None
)
```

**Parameters:**
- `provider`: LLM provider (openai, azure, gemini, claude, openrouter)
- `model`: Model name (defaults to provider's default)

#### `extract()`

```python
result = extractor.extract(
    text: str,
    entity_types: Optional[List[str]] = None,
    context: Optional[str] = None,
    strict_mode: bool = False
) -> Dict[str, Any]
```

**Parameters:**
- `text`: Text to extract entities from (50-5000 characters)
- `entity_types`: List of entity types - ["person", "date"] (default: both)
- `context`: Optional context about the text (max 200 characters)
- `strict_mode`: Whether to use strict extraction (default: False)

**Returns:**
```python
{
    "success": bool,
    "entities": {
        "persons": list[str],
        "dates": list[str]
    },
    "metadata": {
        "total_persons": int,
        "total_dates": int,
        "text_length": int,
        "extraction_confidence": str  # "high", "medium", "low"
    },
    "raw_response": str,
    "error": str | None
}
```

**Raises:**
- `ValueError`: If input is invalid

---

## 🎯 Entity Types

### Person Names
Extracts full names including titles:
- Full names: "John Smith", "Sarah Johnson"
- With titles: "Dr. Emily Davis", "Professor Robert Lee", "Mr. James Taylor"
- Multiple names: Handles lists and conjunctions

### Dates
Supports multiple date formats:
- **ISO Format**: 2024-03-15, 2024-06-15
- **US Format**: 03/15/2024, 05/01/2024
- **Written Format**: March 15, 2024, May 30th, 2024
- **Various Styles**: December 25, 2023, January 10, 2024

---

## 🧪 Examples

### Example 1: Meeting Notes

```python
text = """
Meeting notes from Q1 review:
Attendees: John Smith, Sarah Johnson, Michael Chen
Date: March 15, 2024
Next meeting: April 20, 2024
"""

result = extractor.extract(text, entity_types=["person", "date"])
print(f"Attendees: {result['entities']['persons']}")
print(f"Meeting dates: {result['entities']['dates']}")
```

### Example 2: Narrative Text

```python
text = """
On December 25, 2023, Alice Williams and Bob Martinez met with the team.
They discussed the project timeline and set deadlines for January 10, 2024
and February 5, 2024.
"""

result = extractor.extract(text)
print(result["entities"])
```

### Example 3: Email Content

```python
text = """
From: Dr. Emily Davis
Date: 2024-07-20
Subject: Conference Presentation

Dear Professor Robert Lee,

The conference is scheduled for July 20, 2024.
"""

result = extractor.extract(text, entity_types=["person", "date"])
```

---

## 🏗️ Architecture

### Few-Shot Prompting Flow

```
Input Text → Few-Shot Examples → LLM Prompt → JSON Extraction → Validation → Structured Output
```

### Key Components

1. **Few-Shot Examples**: 4 pre-defined examples showing extraction patterns
2. **Prompt Engineering**: Builds prompts with examples and guidelines
3. **LLM Integration**: Uses LLMClientManager for entity extraction
4. **JSON Parsing**: Extracts JSON from LLM response
5. **Entity Validation**: Validates and cleans extracted entities
6. **Confidence Calculation**: Estimates extraction confidence

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

1. **Meeting Notes Processing**: Extract attendees and dates from meeting notes
2. **Email Analysis**: Identify people and dates mentioned in emails
3. **Document Processing**: Extract entities from narrative documents
4. **Calendar Integration**: Extract dates for calendar events
5. **Contact Management**: Extract person names for contact lists
6. **Event Planning**: Extract participants and event dates

---

## 📝 Few-Shot Prompting

The system uses 4 carefully crafted examples to guide the LLM:

1. **Meeting with multiple people and dates**
2. **Narrative text with embedded entities**
3. **Various date formats (ISO, US)**
4. **Titles and professional names**

Each example demonstrates:
- Expected input format
- Expected output structure
- Handling of edge cases
- Consistent JSON formatting

---

## ⚠️ Limitations

- **Accuracy**: Depends on LLM quality and prompt clarity
- **Date Formats**: May not handle all possible date formats
- **Name Ambiguity**: May struggle with ambiguous names
- **Context**: Limited context understanding
- **Cost**: LLM API calls for each extraction

---

## 🔍 Confidence Levels

The system provides confidence levels based on:
- **High**: Many entities relative to text length
- **Medium**: Moderate entity density
- **Low**: Few or no entities found

---

## 📝 Notes

- Uses lower temperature (0.3) for consistent extraction
- Few-shot examples are filtered based on requested entity types
- JSON extraction handles various response formats
- Entity validation ensures quality output
- Raw response included for debugging

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

