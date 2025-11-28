# Sentiment Analysis System

> **GenAI Problem** - Sentiment analysis system using LLM integration

A comprehensive sentiment analysis system that analyzes text sentiment, detects emotions, and provides detailed reasoning. Handles various text formats, provides confidence scoring, and supports batch processing with structured output using LLMClientManager.

**Author:** chronosnehal  
**Category:** GenAI  
**Difficulty:** Medium  
**Time:** 25-30 minutes

---

## 🎯 Features

- ✅ **Sentiment Analysis**: Positive, negative, neutral classification with scores (-1.0 to 1.0)
- ✅ **Emotion Detection**: 7 emotions (joy, sadness, anger, fear, surprise, disgust, neutral)
- ✅ **Detailed Reasoning**: Explanations for sentiment and emotion classifications
- ✅ **Confidence Scoring**: 0.0 to 1.0 confidence scores
- ✅ **Batch Processing**: Analyze multiple texts at once
- ✅ **Structured Output**: JSON-formatted results with metadata
- ✅ **LLM Integration**: Uses LLMClientManager for multi-provider support

---

## 📁 Project Structure

```
sentiment_analysis/
├── question_sentiment_analysis.md   # Problem description
├── sentiment_analysis.py           # Solution implementation
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
python app/genai/sentiment_analysis/sentiment_analysis.py
```

---

## 💻 Usage Examples

### Basic Usage

```python
from app.genai.sentiment_analysis.sentiment_analysis import SentimentAnalyzer

# Initialize analyzer
analyzer = SentimentAnalyzer(provider="openai")

# Analyze single text
result = analyzer.analyze(
    text="I love this product!",
    analysis_type="comprehensive"
)

print(f"Sentiment: {result['results'][0]['sentiment']}")
print(f"Score: {result['results'][0]['sentiment_score']}")
print(f"Emotions: {result['results'][0]['emotions']}")
```

### Batch Processing

```python
texts = [
    "This is amazing!",
    "I'm disappointed.",
    "It's okay, nothing special."
]

result = analyzer.analyze(
    text=texts,
    analysis_type="comprehensive"
)

for i, r in enumerate(result["results"], 1):
    print(f"Text {i}: {r['sentiment']} (score: {r['sentiment_score']})")
```

### Emotion-Only Analysis

```python
result = analyzer.analyze(
    text="I'm so excited!",
    analysis_type="emotion",
    include_reasoning=False
)

print(result["results"][0]["emotions"])
```

---

## 📖 API Reference

### `SentimentAnalyzer`

#### Constructor

```python
analyzer = SentimentAnalyzer(
    provider: str = "openai",
    model: Optional[str] = None
)
```

**Parameters:**
- `provider`: LLM provider (openai, azure, gemini, claude, openrouter)
- `model`: Model name (defaults to provider's default)

#### `analyze()`

```python
result = analyzer.analyze(
    text: Union[str, List[str]],
    analysis_type: str = "comprehensive",
    include_reasoning: bool = True,
    granularity: str = "document"
) -> Dict[str, Any]
```

**Parameters:**
- `text`: Text(s) to analyze (string or list of strings, 10-5000 chars each)
- `analysis_type`: "sentiment", "emotion", or "comprehensive" (default: "comprehensive")
- `include_reasoning`: Whether to include reasoning (default: True)
- `granularity`: "sentence", "paragraph", or "document" (default: "document")

**Returns:**
```python
{
    "success": bool,
    "results": [
        {
            "text": str,
            "sentiment": str,  # "positive", "negative", "neutral"
            "sentiment_score": float,  # -1.0 to 1.0
            "emotions": {
                "joy": float,
                "sadness": float,
                "anger": float,
                "fear": float,
                "surprise": float,
                "disgust": float,
                "neutral": float
            },
            "confidence": float,  # 0.0 to 1.0
            "reasoning": str,
            "key_phrases": list[str]
        }
    ],
    "summary": {
        "average_sentiment": float,
        "sentiment_distribution": dict
    },
    "metadata": {
        "total_texts": int,
        "analysis_type": str,
        "processing_time": float
    },
    "error": str | None
}
```

**Raises:**
- `ValueError`: If input is invalid

---

## 🎯 Analysis Types

### Sentiment Only
Focus on sentiment classification.

```python
result = analyzer.analyze(
    text="...",
    analysis_type="sentiment"
)
```

### Emotion Only
Focus on emotion detection.

```python
result = analyzer.analyze(
    text="...",
    analysis_type="emotion"
)
```

### Comprehensive
Full analysis with both sentiment and emotions.

```python
result = analyzer.analyze(
    text="...",
    analysis_type="comprehensive"
)
```

---

## 😊 Emotion Detection

The system detects 7 basic emotions:

- **Joy**: Happiness, excitement, pleasure
- **Sadness**: Sorrow, disappointment, melancholy
- **Anger**: Frustration, irritation, rage
- **Fear**: Anxiety, worry, concern
- **Surprise**: Astonishment, amazement
- **Disgust**: Revulsion, distaste
- **Neutral**: No strong emotion

Each emotion has a score from 0.0 to 1.0, with scores typically summing to approximately 1.0.

---

## 📊 Sentiment Scores

- **Positive**: Sentiment score > 0.3
- **Negative**: Sentiment score < -0.3
- **Neutral**: -0.3 ≤ sentiment score ≤ 0.3

Sentiment scores range from -1.0 (very negative) to 1.0 (very positive).

---

## 🧪 Examples

### Example 1: Positive Sentiment

```python
result = analyzer.analyze(
    text="I absolutely love this product! It's amazing!",
    analysis_type="comprehensive"
)

r = result["results"][0]
print(f"Sentiment: {r['sentiment']}")  # "positive"
print(f"Score: {r['sentiment_score']}")  # ~0.9
print(f"Top Emotion: {max(r['emotions'], key=r['emotions'].get)}")  # "joy"
```

### Example 2: Negative Sentiment

```python
result = analyzer.analyze(
    text="This is terrible. I'm very disappointed.",
    analysis_type="comprehensive"
)

r = result["results"][0]
print(f"Sentiment: {r['sentiment']}")  # "negative"
print(f"Score: {r['sentiment_score']}")  # ~-0.8
```

### Example 3: Batch Analysis

```python
reviews = [
    "Great product, highly recommend!",
    "Not worth the money.",
    "It's okay, nothing special."
]

result = analyzer.analyze(reviews)

print(f"Average Sentiment: {result['summary']['average_sentiment']}")
print(f"Distribution: {result['summary']['sentiment_distribution']}")
```

---

## 🏗️ Architecture

### Analysis Flow

```
Input Text → Validation → Prompt Building → LLM Analysis → JSON Parsing → Normalization → Confidence Calculation → Structured Output
```

### Key Components

1. **Input Validation**: Validates text and parameters
2. **Prompt Engineering**: Builds analysis-specific prompts
3. **LLM Integration**: Uses LLMClientManager for sentiment analysis
4. **JSON Parsing**: Extracts structured data from LLM responses
5. **Normalization**: Validates and normalizes analysis results
6. **Confidence Calculation**: Estimates prediction confidence
7. **Batch Processing**: Handles multiple texts efficiently
8. **Summary Generation**: Aggregates statistics for batches

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

1. **Social Media Monitoring**: Analyze customer sentiment on social platforms
2. **Product Reviews**: Analyze review sentiment and emotions
3. **Customer Feedback**: Process customer feedback at scale
4. **Content Moderation**: Identify negative or harmful content
5. **Market Research**: Analyze public opinion and trends

---

## ⚠️ Limitations

- **Accuracy**: Depends on LLM quality and text clarity
- **Sarcasm**: May struggle with sarcastic or ironic text
- **Context**: Limited context understanding
- **Language**: Best results with English text
- **Cost**: LLM API calls for each analysis

---

## 📝 Notes

- Uses lower temperature (0.3) for consistent analysis
- JSON extraction handles various response formats
- Confidence scoring considers sentiment strength and emotion dominance
- Batch processing analyzes texts sequentially
- Summary statistics aggregate results for batches

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

