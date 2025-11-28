#!/usr/bin/env python3
"""
Text Summarization System - GenAI Solution Implementation

Description: Text summarization system using LLM integration to generate
summaries of various lengths and formats.

This solution supports both extractive and abstractive summarization approaches,
handles different content types, provides customizable summary styles, and uses
LLMClientManager for LLM integration.

Dependencies: app.utils.llm_client_manager
Time Complexity: O(n) where n = text length
Space Complexity: O(m) where m = summary size
Author: chronosnehal
Date: 2025-11-27
"""

from app.utils.llm_client_manager import LLMClientManager
from typing import Optional, Dict, Any, List
import re
import logging
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TextSummarizer:
    """
    Text summarization system using LLM integration.
    
    This class generates summaries using extractive or abstractive approaches
    with customizable lengths, formats, and styles using LLMClientManager.
    
    Attributes:
        manager: LLMClientManager instance
        provider: Selected LLM provider
        model: Model name to use
    """
    
    # Length guidelines (word counts)
    LENGTH_GUIDELINES = {
        "short": "20-50 words (1-2 sentences)",
        "medium": "50-150 words (3-5 sentences)",
        "long": "150-300 words (6-10 sentences)"
    }
    
    # Style descriptions
    STYLES = {
        "concise": "Brief, to-the-point summary focusing on essential information",
        "detailed": "Comprehensive summary with context and supporting details",
        "executive": "High-level summary for decision-makers, focusing on key findings and recommendations",
        "technical": "Precise summary with technical terminology and specifications"
    }
    
    def __init__(
        self,
        provider: str = "openai",
        model: Optional[str] = None
    ):
        """
        Initialize text summarizer.
        
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
        
        logger.info(f"TextSummarizer initialized with provider: {provider}, model: {self.model}")
    
    def _determine_length_words(self, length: str) -> int:
        """
        Determine target word count from length specification.
        
        Args:
            length: Length specification ("short", "medium", "long", or integer)
        
        Returns:
            Target word count
        """
        if length == "short":
            return 35  # Average of 20-50
        elif length == "medium":
            return 100  # Average of 50-150
        elif length == "long":
            return 225  # Average of 150-300
        else:
            # Try to parse as integer
            try:
                return int(length)
            except ValueError:
                return 100  # Default to medium
    
    def _build_summarization_prompt(
        self,
        text: str,
        summary_type: str,
        length: str,
        format_type: str,
        style: str,
        focus_areas: Optional[List[str]],
        max_sentences: Optional[int]
    ) -> str:
        """
        Build prompt for text summarization.
        
        Args:
            text: Text to summarize
            summary_type: "extractive" or "abstractive"
            length: Length specification
            format_type: Format type
            style: Summary style
            focus_areas: Optional focus areas
            max_sentences: Maximum sentences for extractive
        
        Returns:
            Formatted prompt string
        """
        length_words = self._determine_length_words(length)
        length_desc = self.LENGTH_GUIDELINES.get(length, f"{length_words} words")
        style_desc = self.STYLES.get(style, style)
        
        system_prompt = f"""You are an expert text summarization system. Generate a {summary_type} summary of the given text.

Summary Type: {summary_type}
Length: {length} ({length_desc})
Format: {format_type}
Style: {style}
Description: {style_desc}

Guidelines:"""
        
        if summary_type == "extractive":
            system_prompt += "\n- Extract and select the most important sentences from the original text"
            system_prompt += "\n- Preserve original wording as much as possible"
            if max_sentences:
                system_prompt += f"\n- Select at most {max_sentences} key sentences"
        else:  # abstractive
            system_prompt += "\n- Generate a new summary that paraphrases and condenses the content"
            system_prompt += "\n- Use your own words while preserving key information"
            system_prompt += f"\n- Target approximately {length_words} words"
        
        if format_type == "paragraph":
            system_prompt += "\n- Format as continuous prose"
        elif format_type == "bullets":
            system_prompt += "\n- Format as bullet points"
        elif format_type == "structured":
            if style == "executive":
                system_prompt += "\n- Structure as: Key Findings, Recommendations, Next Steps"
            else:
                system_prompt += "\n- Structure with clear sections and headings"
        
        if focus_areas:
            system_prompt += f"\n- Emphasize these topics: {', '.join(focus_areas)}"
        
        if style == "concise":
            system_prompt += "\n- Be brief and focus on essential information only"
        elif style == "detailed":
            system_prompt += "\n- Include context and supporting details"
        elif style == "executive":
            system_prompt += "\n- Focus on key findings, implications, and actionable insights"
        elif style == "technical":
            system_prompt += "\n- Use precise technical terminology and include specifications"
        
        user_prompt = f"Text to summarize:\n\n{text}\n\nGenerate {summary_type} summary:"
        
        return f"{system_prompt}\n\n{user_prompt}"
    
    def _extract_summary(self, response: str, format_type: str) -> str:
        """
        Extract and clean summary from LLM response.
        
        Args:
            response: Raw LLM response
            format_type: Expected format type
        
        Returns:
            Cleaned summary text
        """
        summary = response.strip()
        
        # Remove common prefixes
        prefixes = [
            r'^(Here\'s|Here is|Here\'s a|Summary|Generated summary):\s*',
            r'^SUMMARY:\s*',
        ]
        for prefix in prefixes:
            summary = re.sub(prefix, '', summary, flags=re.IGNORECASE | re.MULTILINE)
        
        summary = summary.strip()
        
        # Ensure proper formatting
        if format_type == "bullets":
            # Ensure bullet points start with bullet markers
            lines = summary.split('\n')
            formatted_lines = []
            for line in lines:
                line = line.strip()
                if line and not line.startswith(('•', '-', '*')):
                    formatted_lines.append(f"• {line}")
                elif line:
                    formatted_lines.append(line)
            summary = '\n'.join(formatted_lines)
        
        return summary
    
    def _extract_key_points(self, summary: str) -> List[str]:
        """
        Extract key points from summary.
        
        Args:
            summary: Summary text
        
        Returns:
            List of key points
        """
        key_points = []
        
        # Split by sentences or bullet points
        if '•' in summary or '-' in summary:
            # Bullet format
            points = re.split(r'[•\-]\s*', summary)
            key_points = [p.strip() for p in points if p.strip()][:10]
        else:
            # Paragraph format - extract first few sentences
            sentences = re.split(r'[.!?]+', summary)
            key_points = [s.strip() for s in sentences if s.strip()][:5]
        
        return key_points
    
    def _calculate_metadata(
        self,
        original_text: str,
        summary: str,
        length: str,
        format_type: str,
        style: str
    ) -> Dict[str, Any]:
        """
        Calculate summary metadata.
        
        Args:
            original_text: Original text
            summary: Generated summary
            length: Length specification
            format_type: Format type
            style: Style used
        
        Returns:
            Metadata dictionary
        """
        original_words = len(original_text.split())
        summary_words = len(summary.split())
        
        compression_ratio = summary_words / max(original_words, 1)
        
        # Determine length category
        if summary_words < 50:
            length_category = "short"
        elif summary_words < 150:
            length_category = "medium"
        else:
            length_category = "long"
        
        return {
            "original_length": original_words,
            "summary_length": summary_words,
            "compression_ratio": round(compression_ratio, 2),
            "length_category": length_category,
            "format": format_type,
            "style": style
        }
    
    def summarize(
        self,
        text: str,
        summary_type: str = "abstractive",
        length: str = "medium",
        format: str = "paragraph",
        style: str = "concise",
        focus_areas: Optional[List[str]] = None,
        max_sentences: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Summarize text with specified parameters.
        
        Args:
            text: Text to summarize (100-50000 characters)
            summary_type: "extractive" or "abstractive" (default: "abstractive")
            length: "short", "medium", "long", or integer word count (default: "medium")
            format: "paragraph", "bullets", "structured" (default: "paragraph")
            style: "concise", "detailed", "executive", "technical" (default: "concise")
            focus_areas: Optional list of topics to emphasize
            max_sentences: Maximum sentences for extractive (default: 5)
        
        Returns:
            Dictionary with summary and metadata
        
        Raises:
            ValueError: If input is invalid
        
        Time Complexity: O(n) where n = text length
        Space Complexity: O(m) where m = summary size
        
        Examples:
            >>> summarizer = TextSummarizer()
            >>> result = summarizer.summarize(
            ...     "Long text here...",
            ...     summary_type="abstractive",
            ...     length="short"
            ... )
            >>> print(result["summary"])
        """
        # Validate input
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")
        
        if len(text) < 100:
            raise ValueError("Text must be at least 100 characters")
        
        if len(text) > 50000:
            raise ValueError("Text must be at most 50000 characters")
        
        if summary_type not in ["extractive", "abstractive"]:
            raise ValueError(
                f"Invalid summary_type: {summary_type}. "
                f"Supported: extractive, abstractive"
            )
        
        if format not in ["paragraph", "bullets", "structured"]:
            raise ValueError(
                f"Invalid format: {format}. "
                f"Supported: paragraph, bullets, structured"
            )
        
        if style not in self.STYLES:
            raise ValueError(
                f"Invalid style: {style}. "
                f"Supported: {list(self.STYLES.keys())}"
            )
        
        if max_sentences is not None and (max_sentences < 1 or max_sentences > 20):
            raise ValueError("max_sentences must be between 1 and 20")
        
        if max_sentences is None:
            max_sentences = 5
        
        logger.info(
            f"Summarizing text: {len(text)} chars, "
            f"type: {summary_type}, length: {length}, format: {format}, style: {style}"
        )
        
        try:
            # Build summarization prompt
            prompt = self._build_summarization_prompt(
                text=text.strip(),
                summary_type=summary_type,
                length=length,
                format_type=format,
                style=style,
                focus_areas=focus_areas,
                max_sentences=max_sentences if summary_type == "extractive" else None
            )
            
            # Generate summary using LLM
            response = self.manager.generate(
                provider=self.provider,
                prompt=prompt,
                model=self.model,
                temperature=0.5  # Moderate temperature for balanced creativity/accuracy
            )
            
            # Extract and clean summary
            summary = self._extract_summary(response, format)
            
            if not summary or len(summary.strip()) < 20:
                logger.warning("Generated summary seems too short")
                return {
                    "success": False,
                    "summary": summary,
                    "summary_type": summary_type,
                    "metadata": {
                        "original_length": len(text.split()),
                        "summary_length": len(summary.split()) if summary else 0,
                        "compression_ratio": 0.0,
                        "length_category": "short",
                        "format": format,
                        "style": style
                    },
                    "key_points": [],
                    "error": "Generated summary is too short or empty"
                }
            
            # Extract key points
            key_points = self._extract_key_points(summary)
            
            # Calculate metadata
            metadata = self._calculate_metadata(text, summary, length, format, style)
            
            logger.info(
                f"Summary generated: {metadata['summary_length']} words, "
                f"compression: {metadata['compression_ratio']}"
            )
            
            return {
                "success": True,
                "summary": summary,
                "summary_type": summary_type,
                "metadata": metadata,
                "key_points": key_points,
                "error": None
            }
            
        except ValueError as e:
            logger.error(f"Validation error: {e}")
            raise
        
        except Exception as e:
            logger.error(f"Summarization failed: {e}")
            return {
                "success": False,
                "summary": "",
                "summary_type": summary_type,
                "metadata": {
                    "original_length": len(text.split()),
                    "summary_length": 0,
                    "compression_ratio": 0.0,
                    "length_category": "short",
                    "format": format,
                    "style": style
                },
                "key_points": [],
                "error": f"Summarization failed: {str(e)}"
            }


def main():
    """Demonstrate text summarizer with examples."""
    summarizer = TextSummarizer(provider="openai")
    
    print("=" * 80)
    print("Text Summarization System - Examples")
    print("=" * 80)
    
    # Example text
    sample_text = """Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed. It uses algorithms to analyze data, identify patterns, and make decisions. Common applications include image recognition, natural language processing, and recommendation systems. The field has grown rapidly due to increased data availability and computational power. Machine learning models can be supervised, unsupervised, or reinforcement-based, each suited for different types of problems. Recent advances in deep learning have revolutionized the field, enabling breakthroughs in areas like computer vision and natural language understanding."""
    
    # Example 1: Abstractive Summary
    print("\n" + "-" * 80)
    print("Example 1: Abstractive Summary - Short, Concise")
    print("-" * 80)
    
    try:
        result1 = summarizer.summarize(
            text=sample_text,
            summary_type="abstractive",
            length="short",
            format="paragraph",
            style="concise"
        )
        
        if result1["success"]:
            print(f"\n✓ Summary:\n{result1['summary']}\n")
            print(f"✓ Metadata: {result1['metadata']}\n")
            print(f"✓ Key Points: {result1['key_points'][:3]}\n")
        else:
            print(f"✗ Error: {result1['error']}\n")
    
    except Exception as e:
        print(f"✗ Exception: {e}\n")
    
    # Example 2: Extractive Summary
    print("\n" + "-" * 80)
    print("Example 2: Extractive Summary - Bullets")
    print("-" * 80)
    
    try:
        result2 = summarizer.summarize(
            text=sample_text,
            summary_type="extractive",
            length="medium",
            format="bullets",
            max_sentences=4
        )
        
        if result2["success"]:
            print(f"\n✓ Summary:\n{result2['summary']}\n")
            print(f"✓ Compression Ratio: {result2['metadata']['compression_ratio']}\n")
        else:
            print(f"✗ Error: {result2['error']}\n")
    
    except Exception as e:
        print(f"✗ Exception: {e}\n")
    
    # Example 3: Executive Summary
    print("\n" + "-" * 80)
    print("Example 3: Executive Summary - Structured Format")
    print("-" * 80)
    
    try:
        result3 = summarizer.summarize(
            text=sample_text,
            summary_type="abstractive",
            length="medium",
            format="structured",
            style="executive"
        )
        
        if result3["success"]:
            print(f"\n✓ Summary:\n{result3['summary'][:300]}...\n")
        else:
            print(f"✗ Error: {result3['error']}\n")
    
    except Exception as e:
        print(f"✗ Exception: {e}\n")
    
    # Example 4: Technical Summary
    print("\n" + "-" * 80)
    print("Example 4: Technical Summary - Detailed Style")
    print("-" * 80)
    
    try:
        result4 = summarizer.summarize(
            text=sample_text,
            summary_type="abstractive",
            length="long",
            format="paragraph",
            style="technical"
        )
        
        if result4["success"]:
            print(f"\n✓ Summary:\n{result4['summary'][:200]}...\n")
            print(f"✓ Summary Length: {result4['metadata']['summary_length']} words\n")
        else:
            print(f"✗ Error: {result4['error']}\n")
    
    except Exception as e:
        print(f"✗ Exception: {e}\n")
    
    # Example 5: Error case - empty text
    print("\n" + "-" * 80)
    print("Example 5: Error Case - Empty Text")
    print("-" * 80)
    
    try:
        result5 = summarizer.summarize(text="")
        print(f"Result: {result5}\n")
    except ValueError as e:
        print(f"✓ Caught expected error: {e}\n")
    
    # Example 6: Error case - invalid summary type
    print("\n" + "-" * 80)
    print("Example 6: Error Case - Invalid Summary Type")
    print("-" * 80)
    
    try:
        result6 = summarizer.summarize(
            text=sample_text,
            summary_type="invalid_type"
        )
        print(f"Result: {result6}\n")
    except ValueError as e:
        print(f"✓ Caught expected error: {e}\n")
    
    print("=" * 80)
    print("Examples completed!")
    print("=" * 80)


if __name__ == "__main__":
    main()

