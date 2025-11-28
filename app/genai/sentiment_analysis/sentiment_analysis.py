#!/usr/bin/env python3
"""
Sentiment Analysis System - GenAI Solution Implementation

Description: Sentiment analysis system using LLM integration to analyze
text sentiment, detect emotions, and provide detailed reasoning.

This solution uses LLM capabilities to perform comprehensive sentiment analysis,
emotion detection, and provide structured output with confidence scoring. Supports
batch processing and various text formats.

Dependencies: app.utils.llm_client_manager
Time Complexity: O(n) where n = number of texts × text length
Space Complexity: O(m) where m = total text size + analysis results
Author: chronosnehal
Date: 2025-11-27
"""

from app.utils.llm_client_manager import LLMClientManager
from typing import Optional, Dict, Any, List, Union
import json
import re
import logging
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    """
    Sentiment analysis system using LLM integration.
    
    This class analyzes text sentiment, detects emotions, and provides detailed
    reasoning using LLMClientManager. Supports batch processing and various
    analysis types.
    
    Attributes:
        manager: LLMClientManager instance
        provider: Selected LLM provider
        model: Model name to use
    """
    
    # Emotion categories
    EMOTIONS = ["joy", "sadness", "anger", "fear", "surprise", "disgust", "neutral"]
    
    def __init__(
        self,
        provider: str = "openai",
        model: Optional[str] = None
    ):
        """
        Initialize sentiment analyzer.
        
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
        
        logger.info(f"SentimentAnalyzer initialized with provider: {provider}, model: {self.model}")
    
    def _build_analysis_prompt(
        self,
        text: str,
        analysis_type: str,
        include_reasoning: bool
    ) -> str:
        """
        Build prompt for sentiment analysis.
        
        Args:
            text: Text to analyze
            analysis_type: Type of analysis
            include_reasoning: Whether to include reasoning
        
        Returns:
            Formatted prompt string
        """
        system_prompt = """You are an expert sentiment and emotion analysis system. Analyze the given text and provide structured sentiment and emotion analysis.

Guidelines:
- Analyze sentiment (positive, negative, neutral) with score from -1.0 to 1.0
- Detect emotions: joy, sadness, anger, fear, surprise, disgust, neutral (scores 0.0 to 1.0)
- Identify key phrases that influence sentiment
- Be accurate and objective
"""
        
        if analysis_type == "sentiment":
            system_prompt += "\nFocus: Sentiment analysis only (emotions optional)\n"
        elif analysis_type == "emotion":
            system_prompt += "\nFocus: Emotion detection (sentiment secondary)\n"
        else:  # comprehensive
            system_prompt += "\nFocus: Comprehensive analysis (both sentiment and emotions)\n"
        
        if include_reasoning:
            system_prompt += "\nProvide detailed reasoning explaining your analysis.\n"
        
        system_prompt += """
Output Format (JSON):
{
    "sentiment": "positive|negative|neutral",
    "sentiment_score": -1.0 to 1.0,
    "emotions": {
        "joy": 0.0-1.0,
        "sadness": 0.0-1.0,
        "anger": 0.0-1.0,
        "fear": 0.0-1.0,
        "surprise": 0.0-1.0,
        "disgust": 0.0-1.0,
        "neutral": 0.0-1.0
    },
    "reasoning": "Detailed explanation",
    "key_phrases": ["phrase1", "phrase2", ...]
}
"""
        
        user_prompt = f"Analyze this text:\n\n{text}\n\nProvide analysis in JSON format:"
        
        return f"{system_prompt}\n\n{user_prompt}"
    
    def _extract_structured_analysis(self, response: str) -> Optional[Dict[str, Any]]:
        """
        Extract structured analysis from LLM response.
        
        Args:
            response: Raw LLM response
        
        Returns:
            Extracted analysis dictionary or None
        """
        # Try to find JSON block
        json_match = re.search(r'\{[^{}]*"sentiment"[^{}]*"emotions"[^{}]*\}', response, re.DOTALL)
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
    
    def _normalize_analysis(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize and validate analysis results.
        
        Args:
            analysis: Raw analysis dictionary
        
        Returns:
            Normalized analysis dictionary
        """
        normalized = {
            "sentiment": "neutral",
            "sentiment_score": 0.0,
            "emotions": {emotion: 0.0 for emotion in self.EMOTIONS},
            "reasoning": "",
            "key_phrases": []
        }
        
        # Extract sentiment
        if "sentiment" in analysis:
            sentiment = str(analysis["sentiment"]).lower()
            if sentiment in ["positive", "negative", "neutral"]:
                normalized["sentiment"] = sentiment
        
        # Extract sentiment score
        if "sentiment_score" in analysis:
            try:
                score = float(analysis["sentiment_score"])
                normalized["sentiment_score"] = max(-1.0, min(1.0, score))
            except (ValueError, TypeError):
                pass
        
        # Extract emotions
        if "emotions" in analysis and isinstance(analysis["emotions"], dict):
            for emotion in self.EMOTIONS:
                if emotion in analysis["emotions"]:
                    try:
                        score = float(analysis["emotions"][emotion])
                        normalized["emotions"][emotion] = max(0.0, min(1.0, score))
                    except (ValueError, TypeError):
                        pass
        
        # Extract reasoning
        if "reasoning" in analysis:
            normalized["reasoning"] = str(analysis["reasoning"]).strip()
        
        # Extract key phrases
        if "key_phrases" in analysis and isinstance(analysis["key_phrases"], list):
            normalized["key_phrases"] = [
                str(phrase).strip() for phrase in analysis["key_phrases"][:10]
            ]
        
        return normalized
    
    def _calculate_confidence(
        self,
        sentiment_score: float,
        emotions: Dict[str, float],
        text_length: int
    ) -> float:
        """
        Calculate confidence score for analysis.
        
        Args:
            sentiment_score: Sentiment score
            emotions: Emotion scores
            text_length: Text length in characters
        
        Returns:
            Confidence score (0.0 to 1.0)
        """
        confidence = 0.5  # Base confidence
        
        # Higher confidence for stronger sentiment
        sentiment_strength = abs(sentiment_score)
        confidence += sentiment_strength * 0.3
        
        # Higher confidence for clear emotion dominance
        max_emotion = max(emotions.values())
        if max_emotion > 0.5:
            confidence += 0.2
        
        # Higher confidence for longer, more specific text
        if text_length > 50:
            confidence += 0.1
        if text_length > 200:
            confidence += 0.1
        
        return max(0.0, min(1.0, confidence))
    
    def _generate_summary(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate summary statistics for batch results.
        
        Args:
            results: List of analysis results
        
        Returns:
            Summary dictionary
        """
        if not results:
            return {
                "average_sentiment": 0.0,
                "sentiment_distribution": {"positive": 0, "negative": 0, "neutral": 0}
            }
        
        # Calculate average sentiment
        avg_sentiment = sum(r["sentiment_score"] for r in results) / len(results)
        
        # Count sentiment distribution
        sentiment_dist = {"positive": 0, "negative": 0, "neutral": 0}
        for result in results:
            sentiment = result["sentiment"]
            if sentiment in sentiment_dist:
                sentiment_dist[sentiment] += 1
        
        return {
            "average_sentiment": round(avg_sentiment, 2),
            "sentiment_distribution": sentiment_dist
        }
    
    def analyze(
        self,
        text: Union[str, List[str]],
        analysis_type: str = "comprehensive",
        include_reasoning: bool = True,
        granularity: str = "document"
    ) -> Dict[str, Any]:
        """
        Analyze sentiment and emotions in text(s).
        
        Args:
            text: Text(s) to analyze (string or list of strings)
            analysis_type: "sentiment", "emotion", or "comprehensive" (default: "comprehensive")
            include_reasoning: Whether to include reasoning (default: True)
            granularity: "sentence", "paragraph", or "document" (default: "document")
        
        Returns:
            Dictionary with analysis results and metadata
        
        Raises:
            ValueError: If input is invalid
        
        Time Complexity: O(n) where n = number of texts × text length
        Space Complexity: O(m) where m = total text size + analysis results
        
        Examples:
            >>> analyzer = SentimentAnalyzer()
            >>> result = analyzer.analyze(
            ...     "I love this product!",
            ...     analysis_type="comprehensive"
            ... )
            >>> print(result["results"][0]["sentiment"])
        """
        start_time = time.time()
        
        # Validate input
        if analysis_type not in ["sentiment", "emotion", "comprehensive"]:
            raise ValueError(
                f"Invalid analysis_type: {analysis_type}. "
                f"Supported: sentiment, emotion, comprehensive"
            )
        
        if granularity not in ["sentence", "paragraph", "document"]:
            raise ValueError(
                f"Invalid granularity: {granularity}. "
                f"Supported: sentence, paragraph, document"
            )
        
        # Normalize text to list
        if isinstance(text, str):
            if not text.strip():
                raise ValueError("Text cannot be empty")
            if len(text) < 10:
                raise ValueError("Text must be at least 10 characters")
            if len(text) > 5000:
                raise ValueError("Text must be at most 5000 characters")
            text_list = [text]
        elif isinstance(text, list):
            if not text:
                raise ValueError("Text list cannot be empty")
            text_list = []
            for idx, t in enumerate(text):
                if not isinstance(t, str):
                    raise ValueError(f"Text {idx + 1} must be a string")
                if not t.strip():
                    logger.warning(f"Skipping empty text at index {idx + 1}")
                    continue
                if len(t) < 10:
                    logger.warning(f"Text {idx + 1} is too short, may affect accuracy")
                if len(t) > 5000:
                    logger.warning(f"Text {idx + 1} is too long, truncating")
                    t = t[:5000]
                text_list.append(t.strip())
            
            if not text_list:
                raise ValueError("No valid texts to analyze")
        else:
            raise ValueError("Text must be string or list of strings")
        
        logger.info(
            f"Analyzing {len(text_list)} text(s) with type: {analysis_type}, "
            f"reasoning: {include_reasoning}"
        )
        
        try:
            results = []
            
            # Analyze each text
            for idx, text_item in enumerate(text_list):
                try:
                    # Build analysis prompt
                    prompt = self._build_analysis_prompt(
                        text=text_item,
                        analysis_type=analysis_type,
                        include_reasoning=include_reasoning
                    )
                    
                    # Generate analysis using LLM
                    response = self.manager.generate(
                        provider=self.provider,
                        prompt=prompt,
                        model=self.model,
                        temperature=0.3  # Lower temperature for consistent analysis
                    )
                    
                    # Extract structured analysis
                    analysis = self._extract_structured_analysis(response)
                    
                    if analysis is None:
                        logger.warning(f"Failed to parse analysis for text {idx + 1}")
                        # Create default analysis
                        analysis = {
                            "sentiment": "neutral",
                            "sentiment_score": 0.0,
                            "emotions": {emotion: 0.0 for emotion in self.EMOTIONS},
                            "reasoning": "Unable to parse analysis",
                            "key_phrases": []
                        }
                    
                    # Normalize analysis
                    normalized = self._normalize_analysis(analysis)
                    
                    # Calculate confidence
                    confidence = self._calculate_confidence(
                        normalized["sentiment_score"],
                        normalized["emotions"],
                        len(text_item)
                    )
                    
                    # Build result
                    result = {
                        "text": text_item,
                        "sentiment": normalized["sentiment"],
                        "sentiment_score": round(normalized["sentiment_score"], 2),
                        "emotions": {
                            emotion: round(score, 2)
                            for emotion, score in normalized["emotions"].items()
                        },
                        "confidence": round(confidence, 2),
                        "reasoning": normalized["reasoning"] if include_reasoning else "",
                        "key_phrases": normalized["key_phrases"]
                    }
                    
                    results.append(result)
                    logger.info(
                        f"Analyzed text {idx + 1}/{len(text_list)}: "
                        f"{result['sentiment']} (score: {result['sentiment_score']}, "
                        f"confidence: {result['confidence']})"
                    )
                
                except Exception as e:
                    logger.error(f"Error analyzing text {idx + 1}: {e}")
                    # Add error result
                    results.append({
                        "text": text_item,
                        "sentiment": "neutral",
                        "sentiment_score": 0.0,
                        "emotions": {emotion: 0.0 for emotion in self.EMOTIONS},
                        "confidence": 0.0,
                        "reasoning": f"Analysis failed: {str(e)}",
                        "key_phrases": []
                    })
            
            # Generate summary
            summary = self._generate_summary(results)
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            return {
                "success": True,
                "results": results,
                "summary": summary,
                "metadata": {
                    "total_texts": len(text_list),
                    "analysis_type": analysis_type,
                    "processing_time": round(processing_time, 2)
                },
                "error": None
            }
            
        except ValueError as e:
            logger.error(f"Validation error: {e}")
            raise
        
        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            return {
                "success": False,
                "results": [],
                "summary": {
                    "average_sentiment": 0.0,
                    "sentiment_distribution": {"positive": 0, "negative": 0, "neutral": 0}
                },
                "metadata": {
                    "total_texts": len(text_list) if 'text_list' in locals() else 0,
                    "analysis_type": analysis_type,
                    "processing_time": time.time() - start_time
                },
                "error": f"Analysis failed: {str(e)}"
            }


def main():
    """Demonstrate sentiment analyzer with examples."""
    analyzer = SentimentAnalyzer(provider="openai")
    
    print("=" * 80)
    print("Sentiment Analysis System - Examples")
    print("=" * 80)
    
    # Example 1: Single Text Analysis
    print("\n" + "-" * 80)
    print("Example 1: Single Text - Comprehensive Analysis")
    print("-" * 80)
    
    try:
        result1 = analyzer.analyze(
            text="I absolutely love this product! It's amazing and exceeded my expectations.",
            analysis_type="comprehensive",
            include_reasoning=True
        )
        
        if result1["success"]:
            r = result1["results"][0]
            print(f"\n✓ Text: {r['text']}")
            print(f"✓ Sentiment: {r['sentiment']} (score: {r['sentiment_score']})")
            print(f"✓ Confidence: {r['confidence']}")
            print(f"✓ Top Emotions: {sorted(r['emotions'].items(), key=lambda x: x[1], reverse=True)[:3]}")
            print(f"✓ Key Phrases: {r['key_phrases']}")
            if r['reasoning']:
                print(f"✓ Reasoning: {r['reasoning'][:150]}...")
            print(f"\nMetadata: {result1['metadata']}\n")
        else:
            print(f"✗ Error: {result1['error']}\n")
    
    except Exception as e:
        print(f"✗ Exception: {e}\n")
    
    # Example 2: Batch Processing
    print("\n" + "-" * 80)
    print("Example 2: Batch Processing - Multiple Texts")
    print("-" * 80)
    
    try:
        texts = [
            "This is the worst service I've ever experienced.",
            "The product is okay, nothing special.",
            "Fantastic! Highly recommend to everyone!"
        ]
        
        result2 = analyzer.analyze(
            text=texts,
            analysis_type="comprehensive"
        )
        
        if result2["success"]:
            print(f"\n✓ Analyzed {len(result2['results'])} texts:\n")
            for i, r in enumerate(result2["results"], 1):
                print(f"Text {i}: {r['sentiment']} (score: {r['sentiment_score']}, confidence: {r['confidence']})")
            print(f"\n✓ Summary: {result2['summary']}\n")
        else:
            print(f"✗ Error: {result2['error']}\n")
    
    except Exception as e:
        print(f"✗ Exception: {e}\n")
    
    # Example 3: Emotion-Only Analysis
    print("\n" + "-" * 80)
    print("Example 3: Emotion-Only Analysis")
    print("-" * 80)
    
    try:
        result3 = analyzer.analyze(
            text="I'm so excited about this opportunity!",
            analysis_type="emotion",
            include_reasoning=False
        )
        
        if result3["success"]:
            r = result3["results"][0]
            print(f"\n✓ Text: {r['text']}")
            print(f"✓ Emotions: {r['emotions']}\n")
        else:
            print(f"✗ Error: {result3['error']}\n")
    
    except Exception as e:
        print(f"✗ Exception: {e}\n")
    
    # Example 4: Negative Sentiment
    print("\n" + "-" * 80)
    print("Example 4: Negative Sentiment Analysis")
    print("-" * 80)
    
    try:
        result4 = analyzer.analyze(
            text="I'm really disappointed with the quality. This is not what I expected at all.",
            analysis_type="comprehensive"
        )
        
        if result4["success"]:
            r = result4["results"][0]
            print(f"\n✓ Sentiment: {r['sentiment']} (score: {r['sentiment_score']})")
            print(f"✓ Top Emotions: {sorted(r['emotions'].items(), key=lambda x: x[1], reverse=True)[:3]}\n")
        else:
            print(f"✗ Error: {result4['error']}\n")
    
    except Exception as e:
        print(f"✗ Exception: {e}\n")
    
    # Example 5: Error case - empty text
    print("\n" + "-" * 80)
    print("Example 5: Error Case - Empty Text")
    print("-" * 80)
    
    try:
        result5 = analyzer.analyze(text="")
        print(f"Result: {result5}\n")
    except ValueError as e:
        print(f"✓ Caught expected error: {e}\n")
    
    # Example 6: Error case - invalid analysis type
    print("\n" + "-" * 80)
    print("Example 6: Error Case - Invalid Analysis Type")
    print("-" * 80)
    
    try:
        result6 = analyzer.analyze(
            text="Some text",
            analysis_type="invalid_type"
        )
        print(f"Result: {result6}\n")
    except ValueError as e:
        print(f"✓ Caught expected error: {e}\n")
    
    print("=" * 80)
    print("Examples completed!")
    print("=" * 80)


if __name__ == "__main__":
    main()

