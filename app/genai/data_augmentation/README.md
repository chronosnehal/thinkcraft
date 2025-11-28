# Prompt-Based Data Augmentation System

> **GenAI Problem** - Data augmentation system using LLM integration

A comprehensive data augmentation system that generates diverse variants of product descriptions using GenAI. Creates formal, casual, detailed, concise, marketing, and technical versions while preserving key product information, demonstrating systematic content variation and dataset expansion.

**Author:** chronosnehal  
**Category:** GenAI  
**Difficulty:** Medium  
**Time:** 25-30 minutes

---

## 🎯 Features

- ✅ **Multiple Styles**: Formal, Casual, Detailed, Concise, Marketing, Technical
- ✅ **Style Preservation**: Maintains core meaning while adapting tone
- ✅ **Key Info Preservation**: Preserves important product details
- ✅ **Length Variation**: Short, Medium, Long, or Mixed lengths
- ✅ **Batch Generation**: Generate multiple variants at once
- ✅ **LLM Integration**: Uses LLMClientManager for multi-provider support
- ✅ **Structured Output**: Organized variants with metadata

---

## 📁 Project Structure

```
data_augmentation/
├── question_data_augmentation.md   # Problem description
├── data_augmentation.py            # Solution implementation
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
python app/genai/data_augmentation/data_augmentation.py
```

---

## 💻 Usage Examples

### Basic Usage

```python
from app.genai.data_augmentation.data_augmentation import DataAugmentation

# Initialize augmenter
augmenter = DataAugmentation(provider="openai")

# Generate variants
result = augmenter.augment(
    description="Wireless Bluetooth headphones with noise cancellation, 30-hour battery life.",
    variants=3,
    styles=["formal", "casual", "marketing"]
)

if result["success"]:
    for variant in result["variants"]:
        print(f"{variant['style']}: {variant['text']}")
```

### Formal and Casual Versions

```python
result = augmenter.augment(
    description="Smart fitness tracker with heart rate monitor and sleep tracking.",
    variants=2,
    styles=["formal", "casual"],
    length_variation="mixed"
)

print("Formal:", result["variants"][0]["text"])
print("Casual:", result["variants"][1]["text"])
```

### Multiple Styles

```python
result = augmenter.augment(
    description="4K Ultra HD Smart TV with HDR10, 55-inch display.",
    variants=4,
    styles=["technical", "marketing", "concise", "detailed"],
    preserve_key_info=True
)
```

---

## 📖 API Reference

### `DataAugmentation`

#### Constructor

```python
augmenter = DataAugmentation(
    provider: str = "openai",
    model: Optional[str] = None
)
```

**Parameters:**
- `provider`: LLM provider (openai, azure, gemini, claude, openrouter)
- `model`: Model name (defaults to provider's default)

#### `augment()`

```python
result = augmenter.augment(
    description: str,
    variants: int = 3,
    styles: Optional[List[str]] = None,
    preserve_key_info: bool = True,
    length_variation: str = "mixed",
    tone_variation: bool = True
) -> Dict[str, Any]
```

**Parameters:**
- `description`: Product description (20-1000 characters)
- `variants`: Number of variants to generate (1-10, default: 3)
- `styles`: List of styles (default: rotation of all styles)
- `preserve_key_info`: Whether to preserve key information (default: True)
- `length_variation`: Length strategy - "short", "medium", "long", "mixed" (default: "mixed")
- `tone_variation`: Whether to vary tone (default: True)

**Returns:**
```python
{
    "success": bool,
    "original": str,
    "variants": [
        {
            "text": str,
            "style": str,
            "length": str,
            "word_count": int,
            "key_info_preserved": bool
        }
    ],
    "metadata": {
        "total_variants": int,
        "styles_used": list[str],
        "average_length": float,
        "key_info_preserved": bool
    },
    "error": str | None
}
```

**Raises:**
- `ValueError`: If input is invalid

---

## 🎨 Supported Styles

### Formal
Professional, structured, business language with formal tone.

```python
result = augmenter.augment(
    description="...",
    styles=["formal"]
)
```

**Example Output:**
> "Premium wireless Bluetooth headphones featuring active noise cancellation technology, extended 30-hour battery capacity, and exceptional audio fidelity."

### Casual
Conversational, friendly, relaxed tone with everyday language.

```python
result = augmenter.augment(
    description="...",
    styles=["casual"]
)
```

**Example Output:**
> "Awesome wireless headphones with noise canceling! Battery lasts 30 hours and the sound is amazing."

### Detailed
Comprehensive, thorough descriptions with extensive information.

```python
result = augmenter.augment(
    description="...",
    styles=["detailed"]
)
```

### Concise
Brief, to-the-point versions with essential information only.

```python
result = augmenter.augment(
    description="...",
    styles=["concise"]
)
```

**Example Output:**
> "Fitness tracker: heart rate + sleep tracking."

### Marketing
Persuasive, benefit-focused language emphasizing value proposition.

```python
result = augmenter.augment(
    description="...",
    styles=["marketing"]
)
```

**Example Output:**
> "Experience crystal-clear audio with our wireless Bluetooth headphones! Advanced noise cancellation blocks distractions, while the 30-hour battery keeps you immersed in premium sound quality all day long."

### Technical
Specification-focused, precise terminology with technical details.

```python
result = augmenter.augment(
    description="...",
    styles=["technical"]
)
```

**Example Output:**
> "Wearable device featuring photoplethysmography (PPG) sensors for real-time heart rate measurement and accelerometer-based sleep stage detection."

---

## 📏 Length Variation

| Option | Word Count | Use Case |
|--------|-----------|----------|
| **Short** | 50-100 words | Quick summaries, mobile displays |
| **Medium** | 100-200 words | Standard product pages |
| **Long** | 200-300 words | Detailed product descriptions |
| **Mixed** | Varies | Diverse dataset generation |

---

## 🧪 Examples

### Example 1: Dataset Expansion

```python
# Generate multiple variants for dataset expansion
descriptions = [
    "Wireless headphones with noise cancellation",
    "Smart fitness tracker with heart rate monitor",
    "4K Smart TV with voice control"
]

all_variants = []
for desc in descriptions:
    result = augmenter.augment(
        description=desc,
        variants=3,
        styles=["formal", "casual", "marketing"]
    )
    all_variants.extend(result["variants"])

print(f"Generated {len(all_variants)} variants from {len(descriptions)} descriptions")
```

### Example 2: A/B Testing Variants

```python
# Generate formal and casual versions for A/B testing
result = augmenter.augment(
    description="Premium coffee maker with programmable timer",
    variants=2,
    styles=["formal", "casual"],
    length_variation="medium"
)

formal_version = result["variants"][0]["text"]
casual_version = result["variants"][1]["text"]
```

### Example 3: Style-Specific Generation

```python
# Generate only marketing-focused variants
result = augmenter.augment(
    description="Eco-friendly water bottle, 32oz capacity, leak-proof design",
    variants=5,
    styles=["marketing"],
    length_variation="mixed"
)
```

---

## 🏗️ Architecture

### Simple Flow

```
Product Description → Key Info Extraction → Style-Specific Prompt Building → LLM Generation → Variant Validation → Structured Output
```

### Key Components

1. **Key Information Extraction**: Identifies important product details
2. **Prompt Engineering**: Builds style-specific augmentation prompts
3. **LLM Integration**: Uses LLMClientManager for variant generation
4. **Variant Validation**: Checks key info preservation
5. **Metadata Calculation**: Tracks statistics and metrics

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

1. **Dataset Expansion**: Generate training data for NLP models
2. **A/B Testing**: Create variations for marketing tests
3. **Content Localization**: Adapt descriptions for different audiences
4. **SEO Optimization**: Create multiple versions for search optimization
5. **Product Catalog**: Maintain consistent but varied product descriptions
6. **Content Personalization**: Generate style-specific content for different user segments

---

## ⚠️ Limitations

- **Quality**: Depends on LLM provider and model quality
- **Key Info**: May not preserve all information perfectly
- **Consistency**: Variants may vary in quality
- **Cost**: Multiple LLM calls for batch generation

---

## 📝 Notes

- Uses higher temperature (0.8) for more diverse variants
- Key information extraction identifies numbers, features, and qualities
- Variant validation checks if key info is preserved (50% threshold)
- Metadata includes statistics for analysis
- Always validate generated variants before use

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

