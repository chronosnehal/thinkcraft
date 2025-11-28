#!/usr/bin/env python3
"""
Question Answering System - GenAI Solution Implementation

Description: Question answering system using LLM integration to answer
questions based on provided context documents.

This solution handles various question types, provides confidence scoring,
supports different answer formats, implements citation mechanisms, and handles
complex multi-part questions using LLMClientManager.

Dependencies: app.utils.llm_client_manager
Time Complexity: O(n) where n = context length + question length
Space Complexity: O(m) where m = context size + answer size
Author: chronosnehal
Date: 2025-11-27
"""

from app.utils.llm_client_manager import LLMClientManager
from typing import Optional, Dict, Any, List, Union
import re
import logging
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class QASystem:
    """
    Question answering system using LLM integration.
    
    This class answers questions based on provided context documents using
    LLMClientManager. Supports various question types, answer formats, citations,
    and confidence scoring.
    
    Attributes:
        manager: LLMClientManager instance
        provider: Selected LLM provider
        model: Model name to use
    """
    
    # Question type patterns
    QUESTION_PATTERNS = {
        "factual": [r"^what (is|are|was|were)", r"^who (is|are|was|were)", r"^when (is|are|was|were)", r"^where (is|are|was|were)"],
        "analytical": [r"^why", r"^how", r"^explain", r"^describe"],
        "comparative": [r"compare", r"difference", r"similar", r"versus", r"vs"],
        "multi_part": [r"\?", r"and", r"also", r"what.*how", r"what.*why"]
    }
    
    def __init__(
        self,
        provider: str = "openai",
        model: Optional[str] = None
    ):
        """
        Initialize QA system.
        
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
        
        logger.info(f"QASystem initialized with provider: {provider}, model: {self.model}")
    
    def _detect_question_type(self, question: str) -> str:
        """
        Detect question type from question text.
        
        Args:
            question: Question text
        
        Returns:
            Detected question type
        """
        question_lower = question.lower().strip()
        
        # Check for multi-part first (most specific)
        if any(re.search(pattern, question_lower) for pattern in self.QUESTION_PATTERNS["multi_part"]):
            # Count question marks and conjunctions
            if question.count("?") > 1 or (" and " in question_lower and "?" in question):
                return "multi_part"
        
        # Check other types
        for qtype, patterns in self.QUESTION_PATTERNS.items():
            if qtype == "multi_part":
                continue
            if any(re.search(pattern, question_lower) for pattern in patterns):
                return qtype
        
        return "factual"  # Default
    
    def _extract_relevant_context(
        self,
        context: Union[str, List[str]],
        question: str
    ) -> tuple[List[str], List[int]]:
        """
        Extract relevant context passages for the question.
        
        Args:
            context: Context document(s)
            question: Question text
        
        Returns:
            Tuple of (relevant_passages, source_indices)
        """
        # Normalize context to list
        if isinstance(context, str):
            context_list = [context]
        else:
            context_list = context
        
        # Simple relevance: check for question keywords in context
        question_keywords = set(re.findall(r'\b\w+\b', question.lower()))
        
        relevant_passages = []
        source_indices = []
        
        for idx, doc in enumerate(context_list):
            doc_lower = doc.lower()
            # Count keyword matches
            matches = sum(1 for keyword in question_keywords if keyword in doc_lower and len(keyword) > 3)
            
            if matches > 0:
                relevant_passages.append(doc)
                source_indices.append(idx)
        
        # If no matches, return all context
        if not relevant_passages:
            return context_list, list(range(len(context_list)))
        
        return relevant_passages, source_indices
    
    def _build_qa_prompt(
        self,
        question: str,
        context: List[str],
        answer_format: str,
        include_citations: bool,
        max_length: int,
        question_type: str
    ) -> str:
        """
        Build prompt for question answering.
        
        Args:
            question: Question text
            context: Context documents
            answer_format: Desired answer format
            include_citations: Whether to include citations
            max_length: Maximum answer length
            question_type: Detected question type
        
        Returns:
            Formatted prompt string
        """
        system_prompt = f"""You are an expert question answering system. Answer questions based on the provided context documents.

Question Type: {question_type}
Answer Format: {answer_format}
Maximum Length: {max_length} words
Include Citations: {include_citations}

Guidelines:
- Answer based ONLY on the provided context
- If the answer is not in the context, say so clearly
- Be accurate and precise
- Use the specified answer format
"""
        
        if answer_format == "short":
            system_prompt += "- Provide a concise 1-2 sentence answer\n"
        elif answer_format == "detailed":
            system_prompt += "- Provide a comprehensive, detailed answer\n"
        elif answer_format == "bullets":
            system_prompt += "- Provide answer as structured bullet points\n"
        
        if include_citations:
            system_prompt += "\nCitation Requirements:\n"
            system_prompt += "- Reference which context document(s) you used\n"
            system_prompt += "- Include relevant excerpts from sources\n"
            system_prompt += "- Format citations as: [Source X: excerpt]\n"
        
        if question_type == "multi_part":
            system_prompt += "- Address all parts of the question\n"
            system_prompt += "- Structure answer to cover each part\n"
        elif question_type == "comparative":
            system_prompt += "- Highlight similarities and differences\n"
        elif question_type == "analytical":
            system_prompt += "- Provide reasoning and explanation\n"
        
        # Add context
        system_prompt += "\nContext Documents:\n"
        for idx, doc in enumerate(context):
            system_prompt += f"\n[Source {idx + 1}]:\n{doc}\n"
        
        user_prompt = f"\nQuestion: {question}\n\nAnswer:"
        
        return f"{system_prompt}\n\n{user_prompt}"
    
    def _extract_citations(self, answer: str, context: List[str]) -> List[Dict[str, Any]]:
        """
        Extract citations from answer text.
        
        Args:
            answer: Generated answer text
            context: Context documents
        
        Returns:
            List of citation dictionaries
        """
        citations = []
        
        # Look for citation patterns like [Source X: text]
        citation_pattern = r'\[Source\s+(\d+):\s*([^\]]+)\]'
        matches = re.findall(citation_pattern, answer, re.IGNORECASE)
        
        for source_num, excerpt in matches:
            try:
                source_index = int(source_num) - 1  # Convert to 0-based
                if 0 <= source_index < len(context):
                    # Calculate relevance (simple: excerpt length / context length)
                    relevance = min(len(excerpt) / max(len(context[source_index]), 1), 1.0)
                    
                    citations.append({
                        "source_index": source_index,
                        "text": excerpt.strip(),
                        "relevance_score": round(relevance, 2)
                    })
            except ValueError:
                continue
        
        # If no citations found, try to match answer text with context
        if not citations:
            for idx, doc in enumerate(context):
                # Simple keyword matching
                answer_words = set(re.findall(r'\b\w+\b', answer.lower()))
                doc_words = set(re.findall(r'\b\w+\b', doc.lower()))
                common_words = answer_words.intersection(doc_words)
                
                if len(common_words) > 3:
                    # Find a relevant excerpt (first sentence with common words)
                    sentences = re.split(r'[.!?]+', doc)
                    for sentence in sentences:
                        sentence_words = set(re.findall(r'\b\w+\b', sentence.lower()))
                        if len(sentence_words.intersection(common_words)) > 2:
                            relevance = len(common_words) / max(len(answer_words), 1)
                            citations.append({
                                "source_index": idx,
                                "text": sentence.strip()[:200],  # Limit excerpt length
                                "relevance_score": round(min(relevance, 1.0), 2)
                            })
                            break
        
        return citations[:5]  # Limit to top 5 citations
    
    def _calculate_confidence(
        self,
        answer: str,
        question: str,
        context: List[str],
        citations: List[Dict[str, Any]]
    ) -> float:
        """
        Calculate confidence score for the answer.
        
        Args:
            answer: Generated answer
            question: Original question
            context: Context documents
            citations: Extracted citations
        
        Returns:
            Confidence score (0.0 to 1.0)
        """
        confidence = 0.5  # Base confidence
        
        # Check if answer indicates uncertainty
        uncertainty_phrases = [
            "i don't know", "cannot determine", "not in the context",
            "unclear", "uncertain", "may be", "possibly"
        ]
        answer_lower = answer.lower()
        if any(phrase in answer_lower for phrase in uncertainty_phrases):
            confidence -= 0.3
        
        # Boost confidence if citations found
        if citations:
            confidence += 0.2
            # Higher relevance scores boost confidence
            avg_relevance = sum(c["relevance_score"] for c in citations) / len(citations)
            confidence += avg_relevance * 0.2
        
        # Boost confidence if answer is substantial
        answer_length = len(answer.split())
        if answer_length > 20:
            confidence += 0.1
        
        # Check answer completeness (question keywords in answer)
        question_keywords = set(re.findall(r'\b\w+\b', question.lower()))
        answer_keywords = set(re.findall(r'\b\w+\b', answer_lower))
        keyword_overlap = len(question_keywords.intersection(answer_keywords)) / max(len(question_keywords), 1)
        confidence += keyword_overlap * 0.1
        
        return max(0.0, min(1.0, confidence))  # Clamp between 0 and 1
    
    def answer(
        self,
        question: str,
        context: Union[str, List[str]],
        answer_format: str = "detailed",
        include_citations: bool = True,
        max_length: int = 200,
        question_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Answer a question based on provided context.
        
        Args:
            question: Question to answer
            context: Context document(s) (string or list of strings)
            answer_format: Answer format - "short", "detailed", "bullets" (default: "detailed")
            include_citations: Whether to include citations (default: True)
            max_length: Maximum answer length in words (default: 200)
            question_type: Optional question type hint (auto-detected if None)
        
        Returns:
            Dictionary with answer, confidence, citations, and metadata
        
        Raises:
            ValueError: If input is invalid
        
        Time Complexity: O(n) where n = context length + question length
        Space Complexity: O(m) where m = context size + answer size
        
        Examples:
            >>> qa = QASystem()
            >>> result = qa.answer(
            ...     "What is Python?",
            ...     "Python is a programming language.",
            ...     answer_format="short"
            ... )
            >>> print(result["answer"])
        """
        start_time = time.time()
        
        # Validate input
        if not question or not question.strip():
            raise ValueError("Question cannot be empty")
        
        if len(question) < 10:
            raise ValueError("Question must be at least 10 characters")
        
        if len(question) > 500:
            raise ValueError("Question must be at most 500 characters")
        
        # Normalize context
        if isinstance(context, str):
            if not context.strip():
                raise ValueError("Context cannot be empty")
            context_list = [context]
        elif isinstance(context, list):
            if not context or all(not c.strip() for c in context):
                raise ValueError("Context list cannot be empty")
            context_list = [c.strip() for c in context if c.strip()]
        else:
            raise ValueError("Context must be string or list of strings")
        
        # Validate context length
        for idx, doc in enumerate(context_list):
            if len(doc) < 50:
                raise ValueError(f"Context document {idx + 1} must be at least 50 characters")
            if len(doc) > 10000:
                logger.warning(f"Context document {idx + 1} is very long ({len(doc)} chars), may be truncated")
                context_list[idx] = doc[:10000]
        
        if answer_format not in ["short", "detailed", "bullets"]:
            raise ValueError(f"Invalid answer_format: {answer_format}. Supported: short, detailed, bullets")
        
        if max_length < 20 or max_length > 1000:
            raise ValueError("max_length must be between 20 and 1000")
        
        # Detect question type
        if question_type is None:
            question_type = self._detect_question_type(question)
        
        logger.info(
            f"Answering question: {question[:50]}... "
            f"(type: {question_type}, format: {answer_format})"
        )
        
        try:
            # Extract relevant context
            relevant_context, source_indices = self._extract_relevant_context(context_list, question)
            
            # Build QA prompt
            prompt = self._build_qa_prompt(
                question=question.strip(),
                context=relevant_context,
                answer_format=answer_format,
                include_citations=include_citations,
                max_length=max_length,
                question_type=question_type
            )
            
            # Generate answer using LLM
            response = self.manager.generate(
                provider=self.provider,
                prompt=prompt,
                model=self.model,
                temperature=0.3  # Lower temperature for more accurate answers
            )
            
            answer = response.strip()
            
            # Extract citations
            citations = []
            if include_citations:
                citations = self._extract_citations(answer, relevant_context)
            
            # Calculate confidence
            confidence = self._calculate_confidence(answer, question, relevant_context, citations)
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            logger.info(
                f"Answer generated: {len(answer.split())} words, "
                f"confidence: {confidence:.2f}, citations: {len(citations)}"
            )
            
            return {
                "success": True,
                "answer": answer,
                "confidence": round(confidence, 2),
                "citations": citations,
                "question_type": question_type,
                "metadata": {
                    "context_sources": len(relevant_context),
                    "answer_length": len(answer.split()),
                    "answer_format": answer_format,
                    "processing_time": round(processing_time, 2)
                },
                "error": None
            }
            
        except ValueError as e:
            logger.error(f"Validation error: {e}")
            raise
        
        except Exception as e:
            logger.error(f"Answer generation failed: {e}")
            return {
                "success": False,
                "answer": "",
                "confidence": 0.0,
                "citations": [],
                "question_type": question_type if question_type else "unknown",
                "metadata": {
                    "context_sources": 0,
                    "answer_length": 0,
                    "answer_format": answer_format,
                    "processing_time": time.time() - start_time
                },
                "error": f"Answer generation failed: {str(e)}"
            }


def main():
    """Demonstrate QA system with examples."""
    qa = QASystem(provider="openai")
    
    print("=" * 80)
    print("Question Answering System - Examples")
    print("=" * 80)
    
    # Example 1: Factual Question
    print("\n" + "-" * 80)
    print("Example 1: Factual Question")
    print("-" * 80)
    
    try:
        result1 = qa.answer(
            question="What is the capital of France?",
            context="France is a country in Western Europe. Its capital city is Paris, which is also the largest city in the country.",
            answer_format="short",
            include_citations=True
        )
        
        if result1["success"]:
            print(f"\n✓ Question: What is the capital of France?")
            print(f"✓ Answer: {result1['answer']}")
            print(f"✓ Confidence: {result1['confidence']}")
            print(f"✓ Question Type: {result1['question_type']}")
            if result1['citations']:
                print(f"✓ Citations: {len(result1['citations'])} found")
                for cit in result1['citations']:
                    print(f"  - Source {cit['source_index'] + 1}: {cit['text'][:80]}...")
            print(f"\nMetadata: {result1['metadata']}\n")
        else:
            print(f"✗ Error: {result1['error']}\n")
    
    except Exception as e:
        print(f"✗ Exception: {e}\n")
    
    # Example 2: Multi-Part Question
    print("\n" + "-" * 80)
    print("Example 2: Multi-Part Question")
    print("-" * 80)
    
    try:
        context2 = [
            "Python is a high-level programming language known for its simplicity and readability.",
            "Java is an object-oriented programming language designed for portability.",
            "Python features dynamic typing, while Java uses static typing."
        ]
        
        result2 = qa.answer(
            question="What are the main features of Python and how does it compare to Java?",
            context=context2,
            answer_format="bullets",
            include_citations=True
        )
        
        if result2["success"]:
            print(f"\n✓ Question: What are the main features of Python and how does it compare to Java?")
            print(f"✓ Answer:\n{result2['answer']}")
            print(f"✓ Confidence: {result2['confidence']}")
            print(f"✓ Question Type: {result2['question_type']}\n")
        else:
            print(f"✗ Error: {result2['error']}\n")
    
    except Exception as e:
        print(f"✗ Exception: {e}\n")
    
    # Example 3: Analytical Question
    print("\n" + "-" * 80)
    print("Example 3: Analytical Question")
    print("-" * 80)
    
    try:
        result3 = qa.answer(
            question="Why is machine learning important for modern businesses?",
            context="Machine learning enables businesses to analyze large datasets, automate decision-making, and gain competitive advantages through predictive analytics.",
            answer_format="detailed",
            include_citations=True
        )
        
        if result3["success"]:
            print(f"\n✓ Question: Why is machine learning important for modern businesses?")
            print(f"✓ Answer: {result3['answer'][:200]}...")
            print(f"✓ Confidence: {result3['confidence']}\n")
        else:
            print(f"✗ Error: {result3['error']}\n")
    
    except Exception as e:
        print(f"✗ Exception: {e}\n")
    
    # Example 4: Error case - empty question
    print("\n" + "-" * 80)
    print("Example 4: Error Case - Empty Question")
    print("-" * 80)
    
    try:
        result4 = qa.answer(
            question="",
            context="Some context"
        )
        print(f"Result: {result4}\n")
    except ValueError as e:
        print(f"✓ Caught expected error: {e}\n")
    
    # Example 5: Error case - invalid format
    print("\n" + "-" * 80)
    print("Example 5: Error Case - Invalid Answer Format")
    print("-" * 80)
    
    try:
        result5 = qa.answer(
            question="What is Python?",
            context="Python is a programming language.",
            answer_format="invalid_format"
        )
        print(f"Result: {result5}\n")
    except ValueError as e:
        print(f"✓ Caught expected error: {e}\n")
    
    print("=" * 80)
    print("Examples completed!")
    print("=" * 80)


if __name__ == "__main__":
    main()

