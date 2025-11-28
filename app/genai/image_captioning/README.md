# Image Captioning System

> **GenAI Problem** - Image captioning system using vision models and LLM enhancement

An image captioning system that generates both factual and creative descriptions for images. Uses vision-capable LLM providers to generate initial factual captions, then enhances them with creative variations using LLMClientManager, demonstrating the combination of specialized computer vision models with general language models.

**Author:** chronosnehal  
**Category:** GenAI  
**Difficulty:** Medium  
**Time:** 25-30 minutes

---

## 🎯 Features

- ✅ **Factual Captions**: Initial descriptive captions from vision models
- ✅ **Creative Variations**: Multiple creative styles (creative, humorous, poetic, technical, marketing)
- ✅ **Multiple Image Formats**: File paths, URLs, base64-encoded images
- ✅ **Vision Model Support**: GPT-4 Vision, Claude 3, Gemini Pro Vision
- ✅ **LLM Enhancement**: Uses LLMClientManager for creative captions
- ✅ **Structured Output**: Organized captions with metadata

---

## 📁 Project Structure

```
image_captioning/
├── question_image_captioning.md   # Problem description
├── image_captioning.py           # Solution implementation
└── README.md                      # This file
```

---

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Set your LLM API key (e.g., OpenAI for vision)
export OPENAI_API_KEY=your_api_key_here

# Or use .env file
echo "OPENAI_API_KEY=your_api_key_here" > .env

# Install optional dependencies
pip install requests pillow
```

### 2. Run the Solution

```bash
# From repository root
python app/genai/image_captioning/image_captioning.py
```

---

## 💻 Usage Examples

### Basic Usage

```python
from app.genai.image_captioning.image_captioning import ImageCaptioning

# Initialize captioner
captioner = ImageCaptioning(vision_provider="openai", enhancement_provider="openai")

# Generate captions from local image
result = captioner.caption(
    image="path/to/image.jpg",
    styles=["creative", "humorous"]
)

print(f"Factual: {result['factual_caption']}")
for caption in result["creative_captions"]:
    print(f"{caption['style']}: {caption['caption']}")
```

### Multiple Styles

```python
result = captioner.caption(
    image="path/to/image.jpg",
    styles=["poetic", "technical", "marketing"],
    creativity_level="high"
)

for caption in result["creative_captions"]:
    print(f"{caption['style']}: {caption['caption']}")
```

### Image URL

```python
result = captioner.caption(
    image="https://example.com/image.jpg",
    image_type="url",
    styles=["creative"]
)
```

---

## 📖 API Reference

### `ImageCaptioning`

#### Constructor

```python
captioner = ImageCaptioning(
    vision_provider: str = "openai",
    enhancement_provider: str = "openai"
)
```

**Parameters:**
- `vision_provider`: Vision-capable provider (openai, claude, gemini)
- `enhancement_provider`: Provider for creative enhancements (default: same as vision)

#### `caption()`

```python
result = captioner.caption(
    image: str,
    image_type: Optional[str] = None,
    styles: Optional[List[str]] = None,
    include_factual: bool = True,
    creativity_level: str = "medium"
) -> Dict[str, Any]
```

**Parameters:**
- `image`: Image path, URL, or base64 string
- `image_type`: Type hint ("path", "url", "base64") - auto-detected if None
- `styles`: List of creative styles (default: ["creative", "humorous"])
- `include_factual`: Whether to include factual caption (default: True)
- `creativity_level`: "low", "medium", "high" (default: "medium")

**Returns:**
```python
{
    "success": bool,
    "factual_caption": str,
    "creative_captions": [
        {
            "style": str,
            "caption": str,
            "word_count": int
        }
    ],
    "metadata": {
        "image_source": str,
        "vision_model": str,
        "styles_generated": list[str],
        "total_captions": int
    },
    "error": str | None
}
```

**Raises:**
- `ValueError`: If input is invalid

---

## 🎨 Creative Styles

### Creative
Imaginative, descriptive, engaging language with vivid imagery.

```python
result = captioner.caption(image="...", styles=["creative"])
```

### Humorous
Funny, witty, entertaining with light-hearted humor.

```python
result = captioner.caption(image="...", styles=["humorous"])
```

### Poetic
Artistic, metaphorical, lyrical language with poetic devices.

```python
result = captioner.caption(image="...", styles=["poetic"])
```

### Technical
Precise, detailed, factual with technical terminology.

```python
result = captioner.caption(image="...", styles=["technical"])
```

### Marketing
Persuasive, benefit-focused, compelling marketing language.

```python
result = captioner.caption(image="...", styles=["marketing"])
```

---

## 🖼️ Image Input Formats

### Local File Path
```python
result = captioner.caption(
    image="path/to/image.jpg",
    image_type="path"
)
```

**Supported formats:** JPEG, PNG, WebP

### Image URL
```python
result = captioner.caption(
    image="https://example.com/image.jpg",
    image_type="url"
)
```

**Requirements:** `requests` library (`pip install requests`)

### Base64 Encoded
```python
import base64

with open("image.jpg", "rb") as f:
    image_data = base64.b64encode(f.read()).decode("utf-8")

result = captioner.caption(
    image=f"data:image/jpeg;base64,{image_data}",
    image_type="base64"
)
```

---

## 🔧 Configuration

### Supported Vision Providers

- **OpenAI**: GPT-4 Vision (`gpt-4-vision-preview`, `gpt-4o`)
- **Claude**: Claude 3 (`claude-3-opus-20240229`, `claude-3-sonnet-20240229`)
- **Gemini**: Gemini Pro Vision (`gemini-pro-vision`)
- **OpenRouter**: Free vision models (`qwen/qwen2.5-vl-32b-instruct:free`, `google/gemini-2.0-flash-exp:free`)

### Environment Variables

```bash
# Required for OpenAI vision
OPENAI_API_KEY=your_key

# Optional - other providers
ANTHROPIC_API_KEY=your_key
GOOGLE_API_KEY=your_key
OPENROUTER_API_KEY=your_key  # For free vision models
```

### Free Vision Models via OpenRouter

OpenRouter offers **free vision models** that you can use without cost:

- **`qwen/qwen2.5-vl-32b-instruct:free`** - High-quality vision model
- **`google/gemini-2.0-flash-exp:free`** - Gemini Flash vision model

To use free models, append `:free` to the model ID:

```python
captioner = ImageCaptioning(
    vision_provider="openrouter",
    enhancement_provider="openai"
)

# The system automatically uses free vision model
result = captioner.caption("image.jpg")
```

**Note:** Free models may have rate limits or different availability compared to paid versions.

### Optional Dependencies

```bash
# For URL image support
pip install requests

# For image validation
pip install pillow
```

---

## 💡 Use Cases

1. **Content Creation**: Generate captions for social media posts
2. **Accessibility**: Provide image descriptions for visually impaired users
3. **E-commerce**: Create product descriptions from images
4. **Documentation**: Generate captions for technical documentation
5. **Creative Writing**: Use as inspiration for creative content

---

## 🏗️ Architecture

### Two-Stage Process

```
Image → Vision Model → Factual Caption → LLM Enhancement → Creative Captions
```

### Key Components

1. **Image Loading**: Loads images from path, URL, or base64
2. **Vision Model**: Generates initial factual caption
3. **Prompt Engineering**: Builds style-specific prompts
4. **LLM Enhancement**: Uses LLMClientManager for creative variations
5. **Output Structuring**: Formats results consistently

---

## ⚠️ Limitations

- **Vision Model Access**: Requires vision-capable LLM provider
- **Image Size**: Large images may need resizing
- **Format Support**: JPEG, PNG, WebP supported
- **API Costs**: Both vision and text generation API calls
- **Accuracy**: Depends on vision model quality

---

## 📝 Notes

- Vision models require specific API access (GPT-4 Vision, Claude 3, etc.)
- Factual caption generation uses lower temperature (0.3) for accuracy
- Creative captions use higher temperature (0.7-0.8) for diversity
- Image is encoded as base64 for API transmission
- Supports auto-detection of image type

---

## 🔍 Vision Model Integration

The system uses vision-capable LLM providers:

1. **GPT-4 Vision**: OpenAI's vision model
2. **Claude 3**: Anthropic's vision-capable models
3. **Gemini Pro Vision**: Google's vision model

Each provider requires:
- API key configuration
- Proper image encoding (base64)
- Vision-capable model selection

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

