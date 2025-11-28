#!/usr/bin/env python3
"""
Code Generator - LangGraph State Model

Defines the state structure for the agentic code generation workflow.

Author: chronosnehal
Date: 2025-11-27
"""

from typing import TypedDict, List, Optional, Dict, Any, Annotated
from operator import add
from .models import (
    CodeGenerationRequest,
    ProgrammingLanguage,
    ComplexityLevel
)


class AgentState(TypedDict):
    """
    State structure for the code generation agent workflow.
    
    This state is passed between agent nodes in the LangGraph workflow.
    """
    # Input from user request
    request: CodeGenerationRequest
    original_prompt: str
    language: ProgrammingLanguage
    complexity: ComplexityLevel
    
    # Perception phase
    perceived_intent: Optional[str]
    parsed_requirements: Optional[Dict[str, Any]]
    key_entities: Optional[List[str]]
    
    # Planning phase
    generation_plan: Optional[str]
    code_structure: Optional[Dict[str, Any]]
    approach: Optional[str]
    
    # Generation phase
    generated_code: Optional[str]
    raw_llm_response: Optional[str]
    
    # Validation phase
    is_valid: bool
    validation_errors: List[str]
    syntax_check_passed: bool
    
    # Refinement phase (if needed)
    needs_refinement: bool
    refinement_prompt: Optional[str]
    refined_code: Optional[str]
    
    # Final output
    final_code: Optional[str]
    explanation: Optional[str]
    documentation: Optional[str]
    test_code: Optional[str]
    complexity_analysis: Optional[Dict[str, str]]
    suggestions: Annotated[List[str], add]
    warnings: Annotated[List[str], add]
    
    # Metadata
    step_count: int
    current_step: str
    errors: Annotated[List[str], add]
    metadata: Optional[Dict[str, Any]]

