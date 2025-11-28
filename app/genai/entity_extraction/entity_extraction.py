#!/usr/bin/env python3
"""
Prompt-Based Entity Extraction System - GenAI Solution Implementation

Description: Entity extraction system using LLM integration with few-shot
prompting to identify and extract person names and dates from meeting
descriptions and narrative text.

This solution uses few-shot prompting techniques to guide an LLM in consistently
extracting entities in a structured JSON format, supporting various text
formats and date representations.

Dependencies: app.utils.llm_client_manager
Time Complexity: O(1) for processing + O(n) for LLM generation
Space Complexity: O(m) where m = size of text + extracted entities
Author: chronosnehal
Date: 2025-11-27
"""

from app.utils.llm_client_manager import LLMClientManager
from typing import Optional, Dict, Any, List
import json
import re
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class EntityExtractor:
    """
    Prompt-based entity extraction system using LLM integration.
    
    This class extracts person names and dates from text using few-shot
    prompting techniques with LLMClientManager.
    
    Attributes:
        manager: LLMClientManager instance
        provider: Selected LLM provider
        model: Model name to use
    """
    
    # Few-shot examples for entity extraction
    FEW_SHOT_EXAMPLES = [
        {
            "text": "The quarterly review meeting was scheduled for March 15, 2024. John Smith, Sarah Johnson, and Michael Chen attended the meeting.",
            "entities": {
                "persons": ["John Smith", "Sarah Johnson", "Michael Chen"],
                "dates": ["March 15, 2024"]
            }
        },
        {
            "text": "On December 25, 2023, Alice Williams and Bob Martinez met with the team. They discussed the project timeline and set deadlines for January 10, 2024.",
            "entities": {
                "persons": ["Alice Williams", "Bob Martinez"],
                "dates": ["December 25, 2023", "January 10, 2024"]
            }
        },
        {
            "text": "The conference is scheduled for 2024-06-15. Registration opens on 05/01/2024. Dr. Emily Davis and Professor Robert Lee will be presenting.",
            "entities": {
                "persons": ["Dr. Emily Davis", "Professor Robert Lee"],
                "dates": ["2024-06-15", "05/01/2024"]
            }
        },
        {
            "text": "Meeting notes from the team standup: Present were Tom Wilson, Lisa Brown, and James Taylor. The next meeting is on May 30th, 2024.",
            "entities": {
                "persons": ["Tom Wilson", "Lisa Brown", "James Taylor"],
                "dates": ["May 30th, 2024"]
            }
        }
    ]
    
    def __init__(
        self,
        provider: str = "openai",
        model: Optional[str] = None
    ):
        """
        Initialize entity extractor.
        
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
        
        logger.info(f"EntityExtractor initialized with provider: {provider}, model: {self.model}")
    
    def _build_few_shot_prompt(
        self,
        text: str,
        entity_types: List[str],
        context: Optional[str]
    ) -> str:
        """
        Build few-shot prompt for entity extraction.
        
        Args:
            text: Text to extract entities from
            entity_types: Types of entities to extract
            context: Optional context about the text
        
        Returns:
            Formatted prompt string with few-shot examples
        """
        # Filter examples based on entity types
        filtered_examples = []
        for example in self.FEW_SHOT_EXAMPLES:
            filtered_entities = {}
            if "person" in entity_types:
                filtered_entities["persons"] = example["entities"].get("persons", [])
            if "date" in entity_types:
                filtered_entities["dates"] = example["entities"].get("dates", [])
            
            if filtered_entities:
                filtered_examples.append({
                    "text": example["text"],
                    "entities": filtered_entities
                })
        
        # Build system prompt
        system_prompt = """You are an expert entity extraction system. Extract person names and dates from the given text.

Guidelines:
- Extract full person names (first name + last name)
- Include titles if present (Dr., Mr., Ms., Professor, etc.)
- Extract dates in all formats (ISO: 2024-03-15, US: 03/15/2024, Written: March 15, 2024)
- Return results as valid JSON only
- If no entities found, return empty lists
- Be precise and accurate

Output Format (JSON):
{
    "persons": ["Name1", "Name2", ...],
    "dates": ["Date1", "Date2", ...]
}

Examples:"""
        
        # Add few-shot examples
        for i, example in enumerate(filtered_examples[:4], 1):
            system_prompt += f"\n\nExample {i}:\n"
            system_prompt += f"Text: {example['text']}\n"
            system_prompt += f"Output: {json.dumps(example['entities'], indent=2)}"
        
        # Add context if provided
        if context:
            system_prompt += f"\n\nAdditional Context: {context}\n"
        
        # Add user text
        entity_types_str = " and ".join(entity_types)
        user_prompt = f"\nNow extract {entity_types_str} from this text:\n\n{text}\n\nOutput (JSON only):"
        
        return f"{system_prompt}\n\n{user_prompt}"
    
    def _extract_json_from_response(self, response: str) -> Optional[Dict[str, Any]]:
        """
        Extract JSON from LLM response.
        
        Args:
            response: Raw LLM response
        
        Returns:
            Extracted JSON dictionary or None
        """
        # Try to find JSON block
        json_match = re.search(r'\{[^{}]*"persons"[^{}]*"dates"[^{}]*\}', response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(0))
            except json.JSONDecodeError:
                pass
        
        # Try to find any JSON structure
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(0))
            except json.JSONDecodeError:
                pass
        
        # Try to parse entire response as JSON
        try:
            return json.loads(response.strip())
        except json.JSONDecodeError:
            pass
        
        return None
    
    def _validate_entities(self, entities: Dict[str, Any], entity_types: List[str]) -> Dict[str, Any]:
        """
        Validate and clean extracted entities.
        
        Args:
            entities: Extracted entities dictionary
            entity_types: Expected entity types
        
        Returns:
            Validated entities dictionary
        """
        validated = {
            "persons": [],
            "dates": []
        }
        
        # Validate persons
        if "person" in entity_types and "persons" in entities:
            persons = entities["persons"]
            if isinstance(persons, list):
                # Clean and validate person names
                for person in persons:
                    if isinstance(person, str) and len(person.strip()) > 0:
                        # Basic validation: should contain at least one space or be a known title
                        cleaned = person.strip()
                        if len(cleaned.split()) >= 1:  # At least one word
                            validated["persons"].append(cleaned)
        
        # Validate dates
        if "date" in entity_types and "dates" in entities:
            dates = entities["dates"]
            if isinstance(dates, list):
                # Clean and validate dates
                for date in dates:
                    if isinstance(date, str) and len(date.strip()) > 0:
                        # Basic validation: should look like a date
                        cleaned = date.strip()
                        # Check if it contains numbers (dates usually do)
                        if re.search(r'\d', cleaned):
                            validated["dates"].append(cleaned)
        
        return validated
    
    def _calculate_confidence(
        self,
        entities: Dict[str, Any],
        text_length: int
    ) -> str:
        """
        Calculate extraction confidence level.
        
        Args:
            entities: Extracted entities
            text_length: Length of input text
        
        Returns:
            Confidence level ("high", "medium", "low")
        """
        total_entities = len(entities.get("persons", [])) + len(entities.get("dates", []))
        
        if total_entities == 0:
            return "low"
        
        # Simple heuristic: more entities relative to text length = higher confidence
        entity_density = total_entities / max(text_length / 100, 1)
        
        if entity_density > 0.1:
            return "high"
        elif entity_density > 0.05:
            return "medium"
        else:
            return "low"
    
    def extract(
        self,
        text: str,
        entity_types: Optional[List[str]] = None,
        context: Optional[str] = None,
        strict_mode: bool = False
    ) -> Dict[str, Any]:
        """
        Extract entities from text using few-shot prompting.
        
        Args:
            text: Text to extract entities from
            entity_types: Types of entities to extract (default: ["person", "date"])
            context: Optional context about the text
            strict_mode: Whether to use strict extraction (default: False)
        
        Returns:
            Dictionary with extracted entities and metadata
        
        Raises:
            ValueError: If input is invalid
        
        Time Complexity: O(1) for processing + O(n) for LLM generation
        Space Complexity: O(m) where m = size of text + extracted entities
        
        Examples:
            >>> extractor = EntityExtractor()
            >>> result = extractor.extract(
            ...     "John Smith and Sarah Johnson met on March 15, 2024.",
            ...     entity_types=["person", "date"]
            ... )
            >>> print(result["entities"])
        """
        # Validate input
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")
        
        if len(text) < 50:
            raise ValueError("Text must be at least 50 characters")
        
        if len(text) > 5000:
            raise ValueError("Text must be at most 5000 characters")
        
        if entity_types is None:
            entity_types = ["person", "date"]
        
        invalid_types = [et for et in entity_types if et not in ["person", "date"]]
        if invalid_types:
            raise ValueError(
                f"Invalid entity types: {invalid_types}. "
                f"Supported: ['person', 'date']"
            )
        
        if context and len(context) > 200:
            raise ValueError("Context must be at most 200 characters")
        
        logger.info(
            f"Extracting entities from text: {text[:50]}... "
            f"(types: {entity_types})"
        )
        
        try:
            # Build few-shot prompt
            prompt = self._build_few_shot_prompt(
                text=text.strip(),
                entity_types=entity_types,
                context=context
            )
            
            # Generate extraction using LLM
            response = self.manager.generate(
                provider=self.provider,
                prompt=prompt,
                model=self.model,
                temperature=0.3  # Lower temperature for more consistent extraction
            )
            
            # Extract JSON from response
            entities_json = self._extract_json_from_response(response)
            
            if entities_json is None:
                logger.warning("Failed to extract JSON from LLM response")
                return {
                    "success": False,
                    "entities": {
                        "persons": [],
                        "dates": []
                    },
                    "metadata": {
                        "total_persons": 0,
                        "total_dates": 0,
                        "text_length": len(text),
                        "extraction_confidence": "low"
                    },
                    "raw_response": response,
                    "error": "Failed to parse JSON from LLM response"
                }
            
            # Validate entities
            validated_entities = self._validate_entities(entities_json, entity_types)
            
            # Calculate metadata
            total_persons = len(validated_entities["persons"])
            total_dates = len(validated_entities["dates"])
            confidence = self._calculate_confidence(validated_entities, len(text))
            
            logger.info(
                f"Extraction successful: {total_persons} persons, {total_dates} dates "
                f"(confidence: {confidence})"
            )
            
            return {
                "success": True,
                "entities": validated_entities,
                "metadata": {
                    "total_persons": total_persons,
                    "total_dates": total_dates,
                    "text_length": len(text),
                    "extraction_confidence": confidence
                },
                "raw_response": response,
                "error": None
            }
            
        except ValueError as e:
            logger.error(f"Validation error: {e}")
            raise
        
        except Exception as e:
            logger.error(f"Extraction failed: {e}")
            return {
                "success": False,
                "entities": {
                    "persons": [],
                    "dates": []
                },
                "metadata": {
                    "total_persons": 0,
                    "total_dates": 0,
                    "text_length": len(text),
                    "extraction_confidence": "low"
                },
                "raw_response": "",
                "error": f"Extraction failed: {str(e)}"
            }


def main():
    """Demonstrate entity extraction with examples."""
    extractor = EntityExtractor(provider="openai")
    
    print("=" * 80)
    print("Prompt-Based Entity Extraction System - Examples")
    print("=" * 80)
    
    # Example 1: Meeting Description
    print("\n" + "-" * 80)
    print("Example 1: Meeting Description")
    print("-" * 80)
    
    try:
        result1 = extractor.extract(
            text="The quarterly review meeting was scheduled for March 15, 2024. John Smith, Sarah Johnson, and Michael Chen attended the meeting. We discussed the Q1 results and planned the next steps. The follow-up meeting is set for April 20, 2024.",
            entity_types=["person", "date"]
        )
        
        if result1["success"]:
            print(f"\n✓ Extracted Entities:")
            print(f"  Persons ({result1['metadata']['total_persons']}): {result1['entities']['persons']}")
            print(f"  Dates ({result1['metadata']['total_dates']}): {result1['entities']['dates']}")
            print(f"\n  Confidence: {result1['metadata']['extraction_confidence']}")
            print(f"  Text Length: {result1['metadata']['text_length']} characters\n")
        else:
            print(f"✗ Error: {result1['error']}\n")
    
    except Exception as e:
        print(f"✗ Exception: {e}\n")
    
    # Example 2: Narrative Text
    print("\n" + "-" * 80)
    print("Example 2: Narrative Text")
    print("-" * 80)
    
    try:
        result2 = extractor.extract(
            text="On December 25, 2023, Alice Williams and Bob Martinez met with the team. They discussed the project timeline and set deadlines for January 10, 2024 and February 5, 2024.",
            entity_types=["person", "date"]
        )
        
        if result2["success"]:
            print(f"\n✓ Extracted Entities:")
            print(f"  Persons: {result2['entities']['persons']}")
            print(f"  Dates: {result2['entities']['dates']}\n")
        else:
            print(f"✗ Error: {result2['error']}\n")
    
    except Exception as e:
        print(f"✗ Exception: {e}\n")
    
    # Example 3: Date Only Extraction
    print("\n" + "-" * 80)
    print("Example 3: Date Only Extraction")
    print("-" * 80)
    
    try:
        result3 = extractor.extract(
            text="The conference is scheduled for 2024-06-15. Registration opens on 05/01/2024 and closes on May 30th, 2024.",
            entity_types=["date"]
        )
        
        if result3["success"]:
            print(f"\n✓ Extracted Dates: {result3['entities']['dates']}\n")
        else:
            print(f"✗ Error: {result3['error']}\n")
    
    except Exception as e:
        print(f"✗ Exception: {e}\n")
    
    # Example 4: Person Names with Titles
    print("\n" + "-" * 80)
    print("Example 4: Person Names with Titles")
    print("-" * 80)
    
    try:
        result4 = extractor.extract(
            text="Dr. Emily Davis and Professor Robert Lee will be presenting at the conference on 2024-07-20. The event coordinator is Ms. Jennifer Wilson.",
            entity_types=["person", "date"]
        )
        
        if result4["success"]:
            print(f"\n✓ Extracted Entities:")
            print(f"  Persons: {result4['entities']['persons']}")
            print(f"  Dates: {result4['entities']['dates']}\n")
        else:
            print(f"✗ Error: {result4['error']}\n")
    
    except Exception as e:
        print(f"✗ Exception: {e}\n")
    
    # Example 5: Error case - empty text
    print("\n" + "-" * 80)
    print("Example 5: Error Case - Empty Text")
    print("-" * 80)
    
    try:
        result5 = extractor.extract(
            text="",
            entity_types=["person", "date"]
        )
        print(f"Result: {result5}\n")
    except ValueError as e:
        print(f"✓ Caught expected error: {e}\n")
    
    # Example 6: Error case - invalid entity type
    print("\n" + "-" * 80)
    print("Example 6: Error Case - Invalid Entity Type")
    print("-" * 80)
    
    try:
        result6 = extractor.extract(
            text="Some text with entities",
            entity_types=["invalid_type"]  # Invalid
        )
        print(f"Result: {result6}\n")
    except ValueError as e:
        print(f"✓ Caught expected error: {e}\n")
    
    print("=" * 80)
    print("Examples completed!")
    print("=" * 80)


if __name__ == "__main__":
    main()

