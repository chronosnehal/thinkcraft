#!/usr/bin/env python3
"""
Code Generator - Agentic Solution with LangGraph

Implements a multi-agent code generation system using LangGraph for orchestration.
Agents: Perception → Planning → Generation → Validation → Refinement (if needed)

Time Complexity: O(k) where k = number of agent steps
Space Complexity: O(m) where m = size of generated code

Dependencies: langgraph, langchain, app.utils.llm_client_manager
Author: chronosnehal
Date: 2025-11-27
"""

import re
import time
import logging
from typing import Dict, List, Optional, Literal
import os
import asyncio

from langgraph.graph import StateGraph, END

from ..core.agent_state import AgentState
from ..core.agents import (
    PerceptionAgent,
    PlanningAgent,
    GenerationAgent,
    ValidationAgent,
    RefinementAgent
)
from ..core.llm_adapter import LangChainLLMAdapter
from ..models.schemas import (
    CodeGenerationRequest,
    CodeGenerationResponse,
    ComplexityAnalysis,
    GenerationMetadata,
    ProgrammingLanguage,
    ComplexityLevel
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CodeGeneratorAgent:
    """
    Agentic code generation system using LangGraph.
    
    This class orchestrates multiple specialized agents:
    1. Perception Agent - Understands requirements
    2. Planning Agent - Plans code structure
    3. Generation Agent - Generates code
    4. Validation Agent - Validates code
    5. Refinement Agent - Refines code if needed
    
    Attributes:
        llm: LangChain LLM instance
        provider: LLM provider name
        workflow: LangGraph workflow
    """
    
    def __init__(self, provider: Optional[str] = None, model: Optional[str] = None, temperature: float = 0.7):
        """
        Initialize the agentic code generator.
        
        Args:
            provider: LLM provider (openai, anthropic, gemini, claude, azure)
                     If None, reads from LLM_PROVIDER env var
            model: Model name (if None, uses default for provider)
            temperature: Temperature for generation
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        # Create LLM instance using adapter (reads from env if provider is None)
        self.llm = LangChainLLMAdapter.create_llm(provider=provider, model=model, temperature=temperature)
        
        # Get provider name for metadata
        if provider is None:
            import os
            self.provider = os.getenv("LLM_PROVIDER", "openai").lower()
        else:
            self.provider = provider.lower()
        
        # Get model name for metadata
        if model is None:
            import os
            if self.provider in ["openai", "azure"]:
                self.model = os.getenv("OPENAI_MODEL", "gpt-4")
            elif self.provider in ["anthropic", "claude"]:
                self.model = os.getenv("ANTHROPIC_MODEL", "claude-3-opus-20240229")
            elif self.provider in ["gemini", "google"]:
                self.model = os.getenv("GOOGLE_MODEL", "gemini-pro")
            else:
                self.model = "gpt-4"
        else:
            self.model = model
        
        self.temperature = temperature
        
        # Initialize agents
        self.perception_agent = PerceptionAgent(self.llm)
        self.planning_agent = PlanningAgent(self.llm)
        self.generation_agent = GenerationAgent(self.llm)
        self.validation_agent = ValidationAgent(self.llm)
        self.refinement_agent = RefinementAgent(self.llm)
        
        # Build workflow
        self.workflow = self._build_workflow()
        
        logger.info(f"CodeGeneratorAgent initialized with {provider}/{model}")
    
    def _build_workflow(self) -> StateGraph:
        """
        Build the LangGraph workflow with agent nodes.
        
        Returns:
            Compiled LangGraph workflow
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        # Create graph
        workflow = StateGraph(AgentState)
        
        # Add nodes (agents)
        workflow.add_node("perceive", self.perception_agent.perceive)
        workflow.add_node("plan", self.planning_agent.plan)
        workflow.add_node("generate", self.generation_agent.generate)
        workflow.add_node("validate", self.validation_agent.validate)
        workflow.add_node("refine", self.refinement_agent.refine)
        
        # Define edges
        workflow.set_entry_point("perceive")
        workflow.add_edge("perceive", "plan")
        workflow.add_edge("plan", "generate")
        workflow.add_edge("generate", "validate")
        
        # Conditional edge: refine if validation fails, else end
        workflow.add_conditional_edges(
            "validate",
            self._should_refine,
            {
                "refine": "refine",
                "end": END
            }
        )
        
        # After refinement, validate again
        workflow.add_edge("refine", "validate")
        
        # Compile workflow
        return workflow.compile()
    
    def _should_refine(self, state: AgentState) -> Literal["refine", "end"]:
        """
        Determine if code needs refinement.
        
        Args:
            state: Current agent state
        
        Returns:
            "refine" if refinement needed, "end" otherwise
        """
        if state.get("needs_refinement", False) and state.get("step_count", 0) < 10:
            return "refine"
        return "end"
    
    def _extract_response_sections(self, raw_response: str) -> Dict[str, str]:
        """
        Extract sections from LLM response.
        
        Args:
            raw_response: Raw LLM response
        
        Returns:
            Dictionary with extracted sections
        """
        result = {
            'explanation': '',
            'documentation': '',
            'test_code': '',
            'time_complexity': 'O(?)',
            'space_complexity': 'O(?)',
            'suggestions': [],
            'warnings': []
        }
        
        # Extract explanation
        explanation_pattern = r'EXPLANATION:\s*(.*?)(?=\n(?:DOCUMENTATION|TEST_CODE|COMPLEXITY|SUGGESTIONS|WARNINGS|$))'
        explanation_match = re.search(explanation_pattern, raw_response, re.DOTALL)
        if explanation_match:
            result['explanation'] = explanation_match.group(1).strip()
        
        # Extract documentation
        doc_pattern = r'DOCUMENTATION:\s*(.*?)(?=\n(?:TEST_CODE|COMPLEXITY|SUGGESTIONS|WARNINGS|$))'
        doc_match = re.search(doc_pattern, raw_response, re.DOTALL)
        if doc_match:
            result['documentation'] = doc_match.group(1).strip()
        
        # Extract test code
        test_pattern = r'TEST_CODE:\s*```[\w]*\n(.*?)```'
        test_match = re.search(test_pattern, raw_response, re.DOTALL)
        if test_match:
            result['test_code'] = test_match.group(1).strip()
        
        # Extract complexity
        time_pattern = r'Time:\s*([O\(][^\n]+)'
        time_match = re.search(time_pattern, raw_response)
        if time_match:
            result['time_complexity'] = time_match.group(1).strip()
        
        space_pattern = r'Space:\s*([O\(][^\n]+)'
        space_match = re.search(space_pattern, raw_response)
        if space_match:
            result['space_complexity'] = space_match.group(1).strip()
        
        # Extract suggestions
        suggestions_pattern = r'SUGGESTIONS:\s*(.*?)(?=\n(?:WARNINGS|$))'
        suggestions_match = re.search(suggestions_pattern, raw_response, re.DOTALL)
        if suggestions_match:
            suggestions_text = suggestions_match.group(1).strip()
            result['suggestions'] = [
                s.strip('- ').strip()
                for s in suggestions_text.split('\n')
                if s.strip() and s.strip() != '-'
            ]
        
        # Extract warnings
        warnings_pattern = r'WARNINGS:\s*(.*?)$'
        warnings_match = re.search(warnings_pattern, raw_response, re.DOTALL)
        if warnings_match:
            warnings_text = warnings_match.group(1).strip()
            result['warnings'] = [
                w.strip('- ').strip()
                for w in warnings_text.split('\n')
                if w.strip() and w.strip() != '-'
            ]
        
        return result
    
    async def generate_code(self, request: CodeGenerationRequest) -> CodeGenerationResponse:
        """
        Generate code using the agentic workflow.
        
        Args:
            request: Code generation request
        
        Returns:
            Code generation response
        
        Raises:
            Exception: If generation fails
        
        Time Complexity: O(k) where k = number of agent steps
        Space Complexity: O(m) where m = size of generated code
        """
        start_time = time.time()
        
        logger.info(f"Starting agentic code generation: {request.language.value} - {request.complexity.value}")
        
        # Initialize state
        initial_state: AgentState = {
            "request": request,
            "original_prompt": request.prompt,
            "language": request.language,
            "complexity": request.complexity,
            "perceived_intent": None,
            "parsed_requirements": None,
            "key_entities": None,
            "generation_plan": None,
            "code_structure": None,
            "approach": None,
            "generated_code": None,
            "raw_llm_response": None,
            "is_valid": False,
            "validation_errors": [],
            "syntax_check_passed": False,
            "needs_refinement": False,
            "refinement_prompt": None,
            "refined_code": None,
            "final_code": None,
            "explanation": "",
            "documentation": None,
            "test_code": None,
            "complexity_analysis": None,
            "suggestions": [],
            "warnings": [],
            "step_count": 0,
            "current_step": "start",
            "errors": [],
            "metadata": None
        }
        
        try:
            # Execute workflow
            final_state = await self.workflow.ainvoke(initial_state)
            
            # Extract final code
            final_code = final_state.get("refined_code") or final_state.get("generated_code", "")
            
            if not final_code:
                raise Exception("No code was generated")
            
            # Extract response sections from raw LLM response
            raw_response = final_state.get("raw_llm_response", "")
            sections = self._extract_response_sections(raw_response) if raw_response else {}
            
            # Build response
            generation_time = time.time() - start_time
            
            response = CodeGenerationResponse(
                success=final_state.get("is_valid", False),
                code=final_code,
                language=request.language.value,
                explanation=sections.get('explanation') or final_state.get("perceived_intent", "Code generated successfully"),
                documentation=sections.get('documentation') if request.include_docs else None,
                test_code=sections.get('test_code') if request.include_tests else None,
                complexity_analysis=ComplexityAnalysis(
                    time_complexity=sections.get('time_complexity', 'O(?)'),
                    space_complexity=sections.get('space_complexity', 'O(?)')
                ),
                suggestions=final_state.get("suggestions", []) + sections.get('suggestions', []),
                warnings=final_state.get("warnings", []) + sections.get('warnings', []),
                metadata=GenerationMetadata(
                    tokens_used=len(request.prompt.split()) + len(final_code.split()),  # Approximate
                    generation_time=round(generation_time, 2),
                    model_used=self.model,
                    provider=self.provider,
                    retry_count=final_state.get("step_count", 0) - 4  # Subtract base steps
                )
            )
            
            logger.info(f"Agentic generation completed in {generation_time:.2f}s ({final_state.get('step_count', 0)} steps)")
            return response
            
        except Exception as e:
            logger.error(f"Agentic generation failed: {e}", exc_info=True)
            raise Exception(f"Code generation failed: {str(e)}")
    
    async def refine_code(
        self,
        original_code: str,
        refinement_prompt: str,
        language: ProgrammingLanguage
    ) -> CodeGenerationResponse:
        """
        Refine existing code using the agentic workflow.
        
        Args:
            original_code: Original code to refine
            refinement_prompt: Description of desired refinements
            language: Programming language
        
        Returns:
            Refined code response
        
        Time Complexity: O(k) where k = number of agent steps
        Space Complexity: O(m) where m = size of code
        """
        start_time = time.time()
        
        logger.info(f"Starting agentic code refinement: {language.value}")
        
        # Create a request for refinement
        request = CodeGenerationRequest(
            prompt=f"Refine the following code: {refinement_prompt}\n\nOriginal Code:\n{original_code}",
            language=language,
            complexity=ComplexityLevel.MEDIUM,
            include_docs=True
        )
        
        try:
            response = await self.generate_code(request)
            response.metadata.generation_time = round(time.time() - start_time, 2)
            return response
            
        except Exception as e:
            logger.error(f"Code refinement failed: {e}")
            raise


# Backward compatibility alias
CodeGeneratorService = CodeGeneratorAgent


# Example usage
async def main():
    """Demonstrate agentic code generation system."""
    generator = CodeGeneratorAgent(provider="openai", model="gpt-4")
    
    # Example 1: Simple Python function
    request1 = CodeGenerationRequest(
        prompt="Create a function to check if a number is prime",
        language=ProgrammingLanguage.PYTHON,
        complexity=ComplexityLevel.SIMPLE,
        include_tests=True,
        include_docs=True
    )
    
    print("=" * 80)
    print("Example 1: Simple Prime Number Checker (Agentic)")
    print("=" * 80)
    
    try:
        response1 = await generator.generate_code(request1)
        print(f"\nGenerated Code:\n{response1.code}\n")
        print(f"Explanation: {response1.explanation}\n")
        print(f"Complexity: {response1.complexity_analysis.time_complexity}\n")
        print(f"Steps taken: {response1.metadata.retry_count + 4}\n")
        if response1.test_code:
            print(f"Tests:\n{response1.test_code}\n")
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 2: Medium complexity with framework
    request2 = CodeGenerationRequest(
        prompt="Create a REST API endpoint for user registration with email validation",
        language=ProgrammingLanguage.PYTHON,
        complexity=ComplexityLevel.MEDIUM,
        framework="FastAPI",
        include_docs=True
    )
    
    print("\n" + "=" * 80)
    print("Example 2: FastAPI User Registration Endpoint (Agentic)")
    print("=" * 80)
    
    try:
        response2 = await generator.generate_code(request2)
        print(f"\nGenerated Code:\n{response2.code[:500]}...\n")
        print(f"Suggestions: {', '.join(response2.suggestions[:3])}\n")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
