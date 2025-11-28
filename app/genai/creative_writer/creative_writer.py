#!/usr/bin/env python3
"""
Creative Writing System - GenAI Solution Implementation

Description: Creative writing system using LLM integration for generating
various types of creative content based on prompts, themes, and style requirements.

This solution uses LLM capabilities to generate creative content including stories,
poems, articles, essays, dialogues, and descriptions with customizable styles,
themes, and tones.

Dependencies: app.utils.llm_client_manager
Time Complexity: O(1) for processing + O(n) for LLM generation
Space Complexity: O(m) where m = size of generated content
Author: chronosnehal
Date: 2025-11-27
"""

from app.utils.llm_client_manager import LLMClientManager
from typing import Optional, Dict, Any
import re
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CreativeWriter:
    """
    Creative writing system using LLM integration.
    
    This class generates creative content from natural language prompts using
    LLMClientManager. Supports multiple content types, writing styles, themes,
    and tones.
    
    Attributes:
        manager: LLMClientManager instance
        provider: Selected LLM provider
        model: Model name to use
    """
    
    # Content type descriptions
    CONTENT_TYPES = {
        "story": "A narrative with characters, plot, and setting",
        "poem": "Poetic verse with rhythm, imagery, and emotional expression",
        "article": "Informative, structured, and factual content",
        "essay": "Argumentative or expository writing with clear structure",
        "dialogue": "Conversation between characters",
        "description": "Vivid, detailed scene or object description"
    }
    
    # Style descriptions
    STYLES = {
        "formal": "Professional, structured, academic tone",
        "casual": "Conversational, relaxed, friendly tone",
        "poetic": "Figurative language, imagery, rhythm",
        "narrative": "Storytelling with chronological flow",
        "descriptive": "Vivid details and sensory language",
        "conversational": "Dialogue-like, engaging, interactive"
    }
    
    # Length guidelines (word counts)
    LENGTH_GUIDELINES = {
        "short": "200-500 words",
        "medium": "500-1000 words",
        "long": "1000-2000 words"
    }
    
    def __init__(
        self,
        provider: str = "openai",
        model: Optional[str] = None
    ):
        """
        Initialize creative writer.
        
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
        
        logger.info(f"CreativeWriter initialized with provider: {provider}, model: {self.model}")
    
    def _build_prompt(
        self,
        prompt: str,
        content_type: str,
        theme: Optional[str],
        style: Optional[str],
        length: str,
        tone: Optional[str],
        additional_requirements: Optional[str]
    ) -> str:
        """
        Build prompt for LLM creative writing generation.
        
        Args:
            prompt: User's main writing prompt
            content_type: Type of content to generate
            theme: Optional theme or mood
            style: Optional writing style
            length: Desired length (short, medium, long)
            tone: Optional tone
            additional_requirements: Optional extra instructions
        
        Returns:
            Formatted prompt string
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        content_desc = self.CONTENT_TYPES.get(content_type, content_type)
        
        system_prompt = f"""You are an expert creative writer. Generate high-quality {content_type} content based on user requirements.

Content Type: {content_type}
Description: {content_desc}
"""
        
        if style:
            style_desc = self.STYLES.get(style, style)
            system_prompt += f"\nWriting Style: {style}\nDescription: {style_desc}\n"
        
        if theme:
            system_prompt += f"\nTheme: {theme}\n"
        
        if tone:
            system_prompt += f"\nTone: {tone}\n"
        
        length_guideline = self.LENGTH_GUIDELINES.get(length, "500-1000 words")
        system_prompt += f"\nLength: {length} ({length_guideline})\n"
        
        if additional_requirements:
            system_prompt += f"\nAdditional Requirements: {additional_requirements}\n"
        
        system_prompt += "\nGuidelines:\n"
        system_prompt += "- Write engaging, creative, and original content\n"
        system_prompt += "- Follow the specified style and tone\n"
        system_prompt += "- Ensure appropriate length\n"
        system_prompt += "- Use vivid language and imagery\n"
        system_prompt += "- Maintain consistency throughout\n"
        
        if content_type == "poem":
            system_prompt += "- Use poetic devices (metaphor, alliteration, rhythm)\n"
        elif content_type == "article":
            system_prompt += "- Structure with clear introduction, body, conclusion\n"
        elif content_type == "essay":
            system_prompt += "- Include thesis statement and supporting arguments\n"
        elif content_type == "dialogue":
            system_prompt += "- Use natural, realistic dialogue\n"
        elif content_type == "description":
            system_prompt += "- Focus on sensory details and vivid imagery\n"
        
        user_prompt = f"Write a {content_type} about: {prompt}"
        
        return f"{system_prompt}\n\n{user_prompt}"
    
    def _extract_content(self, response: str) -> str:
        """
        Extract clean content from LLM response.
        
        Args:
            response: Raw LLM response
        
        Returns:
            Extracted content string
        """
        # Remove common prefixes/suffixes
        content = response.strip()
        
        # Remove markdown code blocks if present
        pattern = r'```[\w]*\s*\n(.*?)```'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            content = match.group(1).strip()
        
        # Remove common LLM response prefixes
        prefixes = [
            r'^(Here\'s|Here is|Here\'s a|Here is a|I\'ll|I will|Let me|Let\'s)',
            r'^(Generated|Creative|Writing|Content):\s*',
            r'^Title:\s*.*?\n',
        ]
        
        for prefix in prefixes:
            content = re.sub(prefix, '', content, flags=re.IGNORECASE | re.MULTILINE)
        
        return content.strip()
    
    def _calculate_metadata(self, content: str) -> Dict[str, int]:
        """
        Calculate word and character count metadata.
        
        Args:
            content: Generated content
        
        Returns:
            Dictionary with word_count and character_count
        """
        words = len(content.split())
        characters = len(content)
        
        return {
            "word_count": words,
            "character_count": characters
        }
    
    def generate(
        self,
        prompt: str,
        content_type: str,
        theme: Optional[str] = None,
        style: Optional[str] = None,
        length: str = "medium",
        tone: Optional[str] = None,
        additional_requirements: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate creative content from prompt and requirements.
        
        Args:
            prompt: Main writing prompt or topic
            content_type: Type of content (story, poem, article, essay, dialogue, description)
            theme: Optional theme or mood
            style: Optional writing style
            length: Desired length (short, medium, long)
            tone: Optional tone
            additional_requirements: Optional extra instructions
        
        Returns:
            Dictionary with generated content and metadata
        
        Raises:
            ValueError: If input is invalid
        
        Time Complexity: O(1) for processing + O(n) for LLM generation
        Space Complexity: O(m) where m = size of generated content
        
        Examples:
            >>> writer = CreativeWriter()
            >>> result = writer.generate(
            ...     "A magical forest",
            ...     "story",
            ...     theme="fantasy",
            ...     style="narrative"
            ... )
            >>> print(result["content"])
        """
        # Validate input
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty")
        
        if len(prompt) < 10:
            raise ValueError("Prompt must be at least 10 characters")
        
        if len(prompt) > 500:
            raise ValueError("Prompt must be at most 500 characters")
        
        if content_type not in self.CONTENT_TYPES:
            raise ValueError(
                f"Invalid content_type: {content_type}. "
                f"Supported: {list(self.CONTENT_TYPES.keys())}"
            )
        
        if style and style not in self.STYLES:
            raise ValueError(
                f"Invalid style: {style}. "
                f"Supported: {list(self.STYLES.keys())}"
            )
        
        if length not in self.LENGTH_GUIDELINES:
            raise ValueError(
                f"Invalid length: {length}. "
                f"Supported: {list(self.LENGTH_GUIDELINES.keys())}"
            )
        
        if additional_requirements and len(additional_requirements) > 200:
            raise ValueError("Additional requirements must be at most 200 characters")
        
        logger.info(
            f"Generating {content_type} content for prompt: {prompt[:50]}... "
            f"(style: {style}, theme: {theme}, length: {length})"
        )
        
        try:
            # Build prompt
            full_prompt = self._build_prompt(
                prompt=prompt.strip(),
                content_type=content_type,
                theme=theme,
                style=style,
                length=length,
                tone=tone,
                additional_requirements=additional_requirements
            )
            
            # Generate content using LLM
            response = self.manager.generate(
                provider=self.provider,
                prompt=full_prompt,
                model=self.model,
                temperature=0.8  # Higher temperature for creativity
            )
            
            # Extract content
            content = self._extract_content(response)
            
            if not content or len(content.strip()) < 50:
                logger.warning("Generated content seems too short or empty")
                return {
                    "success": False,
                    "content": content,
                    "content_type": content_type,
                    "metadata": {
                        "theme": theme,
                        "style": style,
                        "length": length,
                        "tone": tone,
                        "word_count": 0,
                        "character_count": 0
                    },
                    "error": "Generated content is too short or empty"
                }
            
            # Calculate metadata
            metadata = self._calculate_metadata(content)
            metadata.update({
                "theme": theme,
                "style": style,
                "length": length,
                "tone": tone
            })
            
            logger.info(
                f"Content generation successful: {metadata['word_count']} words, "
                f"{metadata['character_count']} characters"
            )
            
            return {
                "success": True,
                "content": content,
                "content_type": content_type,
                "metadata": metadata,
                "error": None
            }
            
        except ValueError as e:
            logger.error(f"Validation error: {e}")
            raise
        
        except Exception as e:
            logger.error(f"Content generation failed: {e}")
            return {
                "success": False,
                "content": "",
                "content_type": content_type,
                "metadata": {
                    "theme": theme,
                    "style": style,
                    "length": length,
                    "tone": tone,
                    "word_count": 0,
                    "character_count": 0
                },
                "error": f"Generation failed: {str(e)}"
            }


def main():
    """Demonstrate creative writer with examples."""
    writer = CreativeWriter(provider="openai")
    
    print("=" * 80)
    print("Creative Writing System - Examples")
    print("=" * 80)
    
    # Example 1: Short Story
    print("\n" + "-" * 80)
    print("Example 1: Short Story - Adventure Theme")
    print("-" * 80)
    
    try:
        result1 = writer.generate(
            prompt="A young explorer discovers a hidden city in the mountains",
            content_type="story",
            theme="adventure",
            style="narrative",
            length="short",
            tone="mysterious"
        )
        
        if result1["success"]:
            print(f"\n✓ Generated {result1['content_type']}:")
            print(f"\n{result1['content'][:500]}...\n")
            print(f"Metadata: {result1['metadata']}\n")
        else:
            print(f"✗ Error: {result1['error']}\n")
    
    except Exception as e:
        print(f"✗ Exception: {e}\n")
    
    # Example 2: Poem
    print("\n" + "-" * 80)
    print("Example 2: Poem - Nature Theme")
    print("-" * 80)
    
    try:
        result2 = writer.generate(
            prompt="The changing seasons",
            content_type="poem",
            theme="nature",
            style="poetic",
            length="short",
            tone="contemplative"
        )
        
        if result2["success"]:
            print(f"\n✓ Generated {result2['content_type']}:")
            print(f"\n{result2['content']}\n")
            print(f"Metadata: {result2['metadata']}\n")
        else:
            print(f"✗ Error: {result2['error']}\n")
    
    except Exception as e:
        print(f"✗ Exception: {e}\n")
    
    # Example 3: Article
    print("\n" + "-" * 80)
    print("Example 3: Article - Formal Style")
    print("-" * 80)
    
    try:
        result3 = writer.generate(
            prompt="The benefits of reading",
            content_type="article",
            style="formal",
            length="medium",
            tone="informative"
        )
        
        if result3["success"]:
            print(f"\n✓ Generated {result3['content_type']}:")
            print(f"\n{result3['content'][:500]}...\n")
            print(f"Metadata: {result3['metadata']}\n")
        else:
            print(f"✗ Error: {result3['error']}\n")
    
    except Exception as e:
        print(f"✗ Exception: {e}\n")
    
    # Example 4: Dialogue
    print("\n" + "-" * 80)
    print("Example 4: Dialogue - Casual Style")
    print("-" * 80)
    
    try:
        result4 = writer.generate(
            prompt="Two friends discussing their weekend plans",
            content_type="dialogue",
            style="conversational",
            length="short",
            tone="casual"
        )
        
        if result4["success"]:
            print(f"\n✓ Generated {result4['content_type']}:")
            print(f"\n{result4['content'][:500]}...\n")
            print(f"Metadata: {result4['metadata']}\n")
        else:
            print(f"✗ Error: {result4['error']}\n")
    
    except Exception as e:
        print(f"✗ Exception: {e}\n")
    
    # Example 5: Error case - invalid content_type
    print("\n" + "-" * 80)
    print("Example 5: Error Case - Invalid Content Type")
    print("-" * 80)
    
    try:
        result5 = writer.generate(
            prompt="Some content",
            content_type="novel",  # Invalid - not in supported types
            length="medium"
        )
        print(f"Result: {result5}\n")
    except ValueError as e:
        print(f"✓ Caught expected error: {e}\n")
    
    # Example 6: Error case - empty prompt
    print("\n" + "-" * 80)
    print("Example 6: Error Case - Empty Prompt")
    print("-" * 80)
    
    try:
        result6 = writer.generate(
            prompt="",
            content_type="story"
        )
        print(f"Result: {result6}\n")
    except ValueError as e:
        print(f"✓ Caught expected error: {e}\n")
    
    print("=" * 80)
    print("Examples completed!")
    print("=" * 80)


if __name__ == "__main__":
    main()

