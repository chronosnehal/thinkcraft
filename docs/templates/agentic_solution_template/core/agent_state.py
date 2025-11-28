#!/usr/bin/env python3
"""
Agent State Model for LangGraph

Defines the state structure for the agentic workflow.

Author: chronosnehal
Date: [YYYY-MM-DD]
"""

from typing import TypedDict, List, Optional, Dict, Any, Annotated
from operator import add


class AgentState(TypedDict):
    """
    State structure for the agentic workflow.
    
    This state is passed between agent nodes in the LangGraph workflow.
    Customize fields based on your specific use case.
    """
    # Input from user request
    query: str
    context: Optional[str]
    parameters: Optional[Dict[str, Any]]
    
    # Perception phase
    perceived_intent: Optional[str]
    parsed_data: Optional[Dict[str, Any]]
    key_entities: Optional[List[str]]
    
    # Planning phase
    plan: Optional[str]
    approach: Optional[str]
    steps: Optional[List[str]]
    
    # Execution phase
    intermediate_results: Optional[List[str]]
    current_result: Optional[str]
    
    # Validation phase
    is_valid: bool
    validation_errors: List[str]
    
    # Final output
    final_result: Optional[str]
    explanation: Optional[str]
    
    # Metadata
    step_count: int
    current_step: str
    errors: Annotated[List[str], add]
    metadata: Optional[Dict[str, Any]]

