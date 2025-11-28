#!/usr/bin/env python3
"""
Prompt-Based Data Augmentation System - GenAI Solution Implementation

Description: Data augmentation system using LLM integration to generate
diverse variants of product descriptions with different styles and tones.

This solution uses LLM capabilities to create formal, casual, detailed, concise,
marketing, and technical versions of product descriptions while preserving key
information, demonstrating systematic content variation and dataset expansion.

Dependencies: app.utils.llm_client_manager
Time Complexity: O(n) where n = number of variants
Space Complexity: O(m) where m = total size of generated variants
Author: chronosnehal
Date: 2025-11-27
"""

from app.utils.llm_client_manager import LLMClientManager
from typing import Optional, Dict, Any, List
import re
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DataAugmentation:
    """
    Prompt-based data augmentation system using LLM integration.
    
    This class generates diverse variants of product descriptions using
    LLMClientManager. Supports multiple styles, tones, and length variations
    while preserving key product information.
    
    Attributes:
        manager: LLMClientManager instance
        provider: Selected LLM provider
        model: Model name to use
    """
    
    # Style descriptions
    STYLES = {
        "formal": "Professional, structured, business language with formal tone",
        "casual": "Conversational, friendly, relaxed tone with everyday language",
        "detailed": "Comprehensive, thorough descriptions with extensive information",
        "concise": "Brief, to-the-point versions with essential information only",
        "marketing": "Persuasive, benefit-focused language emphasizing value proposition",
        "technical": "Specification-focused, precise terminology with technical details"
    }
    
    # Length guidelines (word counts)
    LENGTH_GUIDELINES = {
        "short": "50-100 words",
        "medium": "100-200 words",
        "long": "200-300 words",
        "mixed": "Varies across variants"
    }
    
    def __init__(
        self,
        provider: str = "openai",
        model: Optional[str] = None
    ):
        """
        Initialize data augmentation system.
        
        Args:
            provider: LLM provider name (openai, azure, gemini, claude, openrouter)
            model: Model name (defaults to provider's default)
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        self.manager = LLMClientManager()
        self.provider = provider
        
        # Set default models per provider
        default_models = {
            "openai": "gpt-4",
            "azure": "gpt-4",
            "gemini": "gemini-pro",
            "claude": "claude-3-opus-20240229",
            "openrouter": "openai/gpt-4"
        }
        
        self.model = model or default_models.get(provider, "gpt-4")
        
        logger.info(f"DataAugmentation initialized with provider: {provider}, model: {self.model}")
    
    def _extract_key_info(self, description: str) -> List[str]:
        """
        Extract key information from product description.
        
        Args:
            description: Product description text
        
        Returns:
            List of key information points
        """
        key_info = []
        
        # Extract numbers (specifications, measurements, etc.)
        numbers = re.findall(r'\d+[\d,.]*\s*(?:hour|hours|day|days|month|months|year|years|inch|inches|cm|kg|g|mb|gb|tb|%|percent)', description, re.IGNORECASE)
        if numbers:
            key_info.extend(numbers)
        
        # Extract features (words after "with", "features", "includes")
        features = re.findall(r'(?:with|features?|includes?)\s+([^.,;]+)', description, re.IGNORECASE)
        if features:
            key_info.extend([f.strip() for f in features])
        
        # Extract key adjectives/qualities
        quality_words = re.findall(r'\b(premium|advanced|smart|wireless|professional|high-quality|durable|innovative)\b', description, re.IGNORECASE)
        if quality_words:
            key_info.extend(quality_words)
        
        return list(set(key_info))[:10]  # Limit to top 10
    
    def _build_augmentation_prompt(
        self,
        description: str,
        style: str,
        length: str,
        preserve_key_info: bool,
        key_info: List[str]
    ) -> str:
        """
        Build prompt for LLM augmentation.
        
        Args:
            description: Original product description
            style: Target style for variant
            length: Target length category
            preserve_key_info: Whether to preserve key information
            key_info: List of key information points
        
        Returns:
            Formatted prompt string
        """
        style_desc = self.STYLES.get(style, style)
        length_guideline = self.LENGTH_GUIDELINES.get(length, "100-200 words")
        
        system_prompt = f"""You are an expert copywriter specializing in product descriptions. Generate a {style} variant of the given product description.

Style: {style}
Description: {style_desc}
Target Length: {length} ({length_guideline})

Guidelines:
- Maintain the core meaning and information
- Adapt the tone and style according to the specified style
- Ensure the description is engaging and appropriate for the style
- Use natural, fluent language
"""
        
        if preserve_key_info and key_info:
            system_prompt += f"\nIMPORTANT: Preserve these key information points:\n"
            for info in key_info:
                system_prompt += f"- {info}\n"
        
        if style == "formal":
            system_prompt += "- Use professional, business-appropriate language\n"
            system_prompt += "- Avoid contractions and casual expressions\n"
        elif style == "casual":
            system_prompt += "- Use conversational, friendly language\n"
            system_prompt += "- Contractions and casual expressions are acceptable\n"
        elif style == "detailed":
            system_prompt += "- Provide comprehensive information\n"
            system_prompt += "- Include additional relevant details\n"
        elif style == "concise":
            system_prompt += "- Be brief and to-the-point\n"
            system_prompt += "- Focus on essential information only\n"
        elif style == "marketing":
            system_prompt += "- Emphasize benefits and value proposition\n"
            system_prompt += "- Use persuasive, compelling language\n"
        elif style == "technical":
            system_prompt += "- Use precise technical terminology\n"
            system_prompt += "- Focus on specifications and technical details\n"
        
        user_prompt = f"Original description:\n{description}\n\nGenerate a {style} variant:"
        
        return f"{system_prompt}\n\n{user_prompt}"
    
    def _classify_length(self, text: str) -> str:
        """
        Classify text length category.
        
        Args:
            text: Text to classify
        
        Returns:
            Length category (short, medium, long)
        """
        word_count = len(text.split())
        
        if word_count < 50:
            return "short"
        elif word_count < 150:
            return "medium"
        else:
            return "long"
    
    def _check_key_info_preserved(self, variant: str, key_info: List[str]) -> bool:
        """
        Check if key information is preserved in variant.
        
        Args:
            variant: Generated variant text
            key_info: List of key information points
        
        Returns:
            True if key info is preserved
        """
        if not key_info:
            return True
        
        # Check if at least 50% of key info is present
        preserved_count = sum(1 for info in key_info if info.lower() in variant.lower())
        return preserved_count >= len(key_info) * 0.5
    
    def augment(
        self,
        description: str,
        variants: int = 3,
        styles: Optional[List[str]] = None,
        preserve_key_info: bool = True,
        length_variation: str = "mixed",
        tone_variation: bool = True
    ) -> Dict[str, Any]:
        """
        Generate diverse variants of product description.
        
        Args:
            description: Original product description
            variants: Number of variants to generate (1-10)
            styles: List of styles to use (if None, uses default rotation)
            preserve_key_info: Whether to preserve key information
            length_variation: Length variation strategy (short, medium, long, mixed)
            tone_variation: Whether to vary tone
        
        Returns:
            Dictionary with generated variants and metadata
        
        Raises:
            ValueError: If input is invalid
        
        Time Complexity: O(n) where n = variants
        Space Complexity: O(m) where m = total size of variants
        
        Examples:
            >>> augmenter = DataAugmentation()
            >>> result = augmenter.augment(
            ...     "Wireless headphones with noise cancellation",
            ...     variants=3,
            ...     styles=["formal", "casual"]
            ... )
            >>> print(result["variants"])
        """
        # Validate input
        if not description or not description.strip():
            raise ValueError("Description cannot be empty")
        
        if len(description) < 20:
            raise ValueError("Description must be at least 20 characters")
        
        if len(description) > 1000:
            raise ValueError("Description must be at most 1000 characters")
        
        if variants < 1 or variants > 10:
            raise ValueError("Variants must be between 1 and 10")
        
        if styles:
            invalid_styles = [s for s in styles if s not in self.STYLES]
            if invalid_styles:
                raise ValueError(
                    f"Invalid styles: {invalid_styles}. "
                    f"Supported: {list(self.STYLES.keys())}"
                )
        
        if length_variation not in self.LENGTH_GUIDELINES:
            raise ValueError(
                f"Invalid length_variation: {length_variation}. "
                f"Supported: {list(self.LENGTH_GUIDELINES.keys())}"
            )
        
        logger.info(
            f"Augmenting description: {description[:50]}... "
            f"(variants: {variants}, styles: {styles})"
        )
        
        try:
            # Extract key information
            key_info = self._extract_key_info(description) if preserve_key_info else []
            
            # Determine styles to use
            if styles is None:
                # Default rotation: formal, casual, marketing, detailed, concise, technical
                default_styles = ["formal", "casual", "marketing", "detailed", "concise", "technical"]
                styles = [default_styles[i % len(default_styles)] for i in range(variants)]
            else:
                # Repeat styles if needed
                styles = [styles[i % len(styles)] for i in range(variants)]
            
            # Determine length for each variant
            if length_variation == "mixed":
                length_options = ["short", "medium", "long"]
                lengths = [length_options[i % len(length_options)] for i in range(variants)]
            else:
                lengths = [length_variation] * variants
            
            # Generate variants
            generated_variants = []
            
            for i, (style, length) in enumerate(zip(styles, lengths)):
                try:
                    # Build prompt
                    prompt = self._build_augmentation_prompt(
                        description=description.strip(),
                        style=style,
                        length=length,
                        preserve_key_info=preserve_key_info,
                        key_info=key_info
                    )
                    
                    # Generate variant using LLM
                    response = self.manager.generate(
                        provider=self.provider,
                        prompt=prompt,
                        model=self.model,
                        temperature=0.8  # Higher temperature for diversity
                    )
                    
                    # Clean response
                    variant_text = response.strip()
                    
                    # Remove common prefixes
                    prefixes = [
                        r'^(Here\'s|Here is|Here\'s a|Here is a|Generated|Variant):\s*',
                        r'^Style:\s*.*?\n',
                    ]
                    for prefix in prefixes:
                        variant_text = re.sub(prefix, '', variant_text, flags=re.IGNORECASE | re.MULTILINE)
                    
                    variant_text = variant_text.strip()
                    
                    if not variant_text or len(variant_text) < 20:
                        logger.warning(f"Generated variant {i+1} is too short, skipping")
                        continue
                    
                    # Classify length
                    actual_length = self._classify_length(variant_text)
                    
                    # Check key info preservation
                    key_info_preserved = self._check_key_info_preserved(variant_text, key_info) if preserve_key_info else True
                    
                    generated_variants.append({
                        "text": variant_text,
                        "style": style,
                        "length": actual_length,
                        "word_count": len(variant_text.split()),
                        "key_info_preserved": key_info_preserved
                    })
                    
                    logger.info(f"Generated variant {i+1}/{variants} ({style}, {actual_length})")
                
                except Exception as e:
                    logger.error(f"Error generating variant {i+1}: {e}")
                    continue
            
            if not generated_variants:
                return {
                    "success": False,
                    "original": description,
                    "variants": [],
                    "metadata": {
                        "total_variants": 0,
                        "styles_used": [],
                        "average_length": 0.0,
                        "key_info_preserved": False
                    },
                    "error": "Failed to generate any variants"
                }
            
            # Calculate metadata
            total_words = sum(v["word_count"] for v in generated_variants)
            avg_length = total_words / len(generated_variants) if generated_variants else 0
            
            metadata = {
                "total_variants": len(generated_variants),
                "styles_used": list(set(v["style"] for v in generated_variants)),
                "average_length": round(avg_length, 1),
                "key_info_preserved": all(v["key_info_preserved"] for v in generated_variants) if preserve_key_info else True
            }
            
            logger.info(f"Successfully generated {len(generated_variants)} variants")
            
            return {
                "success": True,
                "original": description,
                "variants": generated_variants,
                "metadata": metadata,
                "error": None
            }
            
        except ValueError as e:
            logger.error(f"Validation error: {e}")
            raise
        
        except Exception as e:
            logger.error(f"Augmentation failed: {e}")
            return {
                "success": False,
                "original": description,
                "variants": [],
                "metadata": {
                    "total_variants": 0,
                    "styles_used": [],
                    "average_length": 0.0,
                    "key_info_preserved": False
                },
                "error": f"Augmentation failed: {str(e)}"
            }


def main():
    """Demonstrate data augmentation with examples."""
    augmenter = DataAugmentation(provider="openai")
    
    print("=" * 80)
    print("Prompt-Based Data Augmentation System - Examples")
    print("=" * 80)
    
    # Example 1: Basic Augmentation
    print("\n" + "-" * 80)
    print("Example 1: Basic Augmentation - Multiple Styles")
    print("-" * 80)
    
    try:
        result1 = augmenter.augment(
            description="Wireless Bluetooth headphones with noise cancellation, 30-hour battery life, and premium sound quality.",
            variants=3,
            styles=["formal", "casual", "marketing"]
        )
        
        if result1["success"]:
            print(f"\n✓ Original: {result1['original']}\n")
            print(f"✓ Generated {result1['metadata']['total_variants']} variants:\n")
            for i, variant in enumerate(result1['variants'], 1):
                print(f"Variant {i} ({variant['style']}, {variant['length']}):")
                print(f"  {variant['text'][:150]}...")
                print(f"  Word count: {variant['word_count']}, Key info preserved: {variant['key_info_preserved']}\n")
            print(f"Metadata: {result1['metadata']}\n")
        else:
            print(f"✗ Error: {result1['error']}\n")
    
    except Exception as e:
        print(f"✗ Exception: {e}\n")
    
    # Example 2: Formal and Casual Versions
    print("\n" + "-" * 80)
    print("Example 2: Formal and Casual Versions")
    print("-" * 80)
    
    try:
        result2 = augmenter.augment(
            description="Smart fitness tracker with heart rate monitor and sleep tracking.",
            variants=2,
            styles=["formal", "casual"],
            length_variation="mixed"
        )
        
        if result2["success"]:
            print(f"\n✓ Original: {result2['original']}\n")
            for i, variant in enumerate(result2['variants'], 1):
                print(f"✓ {variant['style'].title()} Version:")
                print(f"  {variant['text']}\n")
        else:
            print(f"✗ Error: {result2['error']}\n")
    
    except Exception as e:
        print(f"✗ Exception: {e}\n")
    
    # Example 3: Multiple Styles
    print("\n" + "-" * 80)
    print("Example 3: Multiple Styles - Technical, Marketing, Concise")
    print("-" * 80)
    
    try:
        result3 = augmenter.augment(
            description="4K Ultra HD Smart TV with HDR10, 55-inch display, and voice control.",
            variants=4,
            styles=["technical", "marketing", "concise", "detailed"],
            preserve_key_info=True
        )
        
        if result3["success"]:
            print(f"\n✓ Original: {result3['original']}\n")
            for variant in result3['variants']:
                print(f"✓ {variant['style'].title()} ({variant['length']}):")
                print(f"  {variant['text'][:200]}...\n")
        else:
            print(f"✗ Error: {result3['error']}\n")
    
    except Exception as e:
        print(f"✗ Exception: {e}\n")
    
    # Example 4: Error case - invalid style
    print("\n" + "-" * 80)
    print("Example 4: Error Case - Invalid Style")
    print("-" * 80)
    
    try:
        result4 = augmenter.augment(
            description="Some product description",
            variants=1,
            styles=["invalid_style"]  # Invalid
        )
        print(f"Result: {result4}\n")
    except ValueError as e:
        print(f"✓ Caught expected error: {e}\n")
    
    # Example 5: Error case - empty description
    print("\n" + "-" * 80)
    print("Example 5: Error Case - Empty Description")
    print("-" * 80)
    
    try:
        result5 = augmenter.augment(
            description="",
            variants=1
        )
        print(f"Result: {result5}\n")
    except ValueError as e:
        print(f"✓ Caught expected error: {e}\n")
    
    print("=" * 80)
    print("Examples completed!")
    print("=" * 80)


if __name__ == "__main__":
    main()

