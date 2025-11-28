#!/usr/bin/env python3
"""
Agent Nodes for LangGraph Workflow

Individual agent nodes for the agentic workflow:
- Perception Agent: Understands requirements
- Planning Agent: Plans approach
- Execution Agent: Executes plan
- Validation Agent: Validates results

Author: chronosnehal
Date: [YYYY-MM-DD]
"""

import logging
from typing import Dict, Any
from langchain_core.messages import HumanMessage, SystemMessage

from .agent_state import AgentState

logger = logging.getLogger(__name__)


class PerceptionAgent:
    """Agent responsible for understanding and parsing user requirements."""
    
    def __init__(self, llm):
        self.llm = llm
    
    async def perceive(self, state: AgentState) -> AgentState:
        """
        Perceive and understand the user's request.
        
        Args:
            state: Current agent state
        
        Returns:
            Updated state with perceived intent
        
        Time Complexity: O(1) - Single LLM call
        Space Complexity: O(n) - Response size
        """
        logger.info("Perception Agent: Analyzing requirements...")
        
        query = state["query"]
        context = state.get("context", "")
        
        prompt = f"""You are an expert analysis agent. Analyze the following request:

Query: {query}
Context: {context if context else "None"}

Analyze this request and provide:
1. Main intent/goal
2. Key entities/concepts mentioned
3. Implicit requirements or constraints
4. Suggested approach

Format your response as:
INTENT: [main goal]
ENTITIES: [comma-separated list]
REQUIREMENTS: [key requirements]
APPROACH: [suggested approach]
"""
        
        try:
            messages = [
                SystemMessage(content="You are an expert at analyzing user requests."),
                HumanMessage(content=prompt)
            ]
            response = await self.llm.ainvoke(messages)
            response_text = response.content if hasattr(response, 'content') else str(response)
            
            # Parse response (simplified - customize based on your needs)
            state["perceived_intent"] = response_text[:500]  # Simplified parsing
            state["parsed_data"] = {"raw_response": response_text}
            state["current_step"] = "perception"
            state["step_count"] += 1
            
            logger.info("Perception complete")
            
        except Exception as e:
            logger.error(f"Perception failed: {e}")
            state["errors"].append(f"Perception error: {str(e)}")
            state["perceived_intent"] = query  # Fallback
        
        return state


class PlanningAgent:
    """Agent responsible for planning the approach."""
    
    def __init__(self, llm):
        self.llm = llm
    
    async def plan(self, state: AgentState) -> AgentState:
        """
        Plan the execution approach.
        
        Args:
            state: Current agent state
        
        Returns:
            Updated state with execution plan
        
        Time Complexity: O(1) - Single LLM call
        Space Complexity: O(n) - Response size
        """
        logger.info("Planning Agent: Creating execution plan...")
        
        perceived_intent = state.get("perceived_intent", state["query"])
        
        prompt = f"""You are an expert planning agent. Create a detailed plan for:

Perceived Intent: {perceived_intent}
Original Query: {state['query']}

Create a detailed plan including:
1. Step-by-step approach
2. Required resources or information
3. Potential challenges
4. Execution strategy

Format your response as:
PLAN: [detailed plan]
STEPS: [numbered steps]
STRATEGY: [execution strategy]
"""
        
        try:
            messages = [
                SystemMessage(content="You are an expert at creating execution plans."),
                HumanMessage(content=prompt)
            ]
            response = await self.llm.ainvoke(messages)
            response_text = response.content if hasattr(response, 'content') else str(response)
            
            state["plan"] = response_text
            state["approach"] = response_text[:200]  # Simplified
            state["current_step"] = "planning"
            state["step_count"] += 1
            
            logger.info("Planning complete")
            
        except Exception as e:
            logger.error(f"Planning failed: {e}")
            state["errors"].append(f"Planning error: {str(e)}")
            state["plan"] = "Execute based on requirements"
        
        return state


class ExecutionAgent:
    """Agent responsible for executing the plan."""
    
    def __init__(self, llm):
        self.llm = llm
    
    async def execute(self, state: AgentState) -> AgentState:
        """
        Execute the plan.
        
        Args:
            state: Current agent state
        
        Returns:
            Updated state with execution results
        
        Time Complexity: O(1) - Single LLM call
        Space Complexity: O(n) - Response size
        """
        logger.info("Execution Agent: Executing plan...")
        
        plan = state.get("plan", "")
        query = state["query"]
        
        prompt = f"""You are an expert execution agent. Execute the following plan:

Plan: {plan}
Original Query: {query}

Execute the plan and provide:
1. The complete result
2. Any relevant details or explanations
3. Confidence level in the result

Provide your response with:
RESULT: [complete result]
EXPLANATION: [explanation]
"""
        
        try:
            messages = [
                SystemMessage(content="You are an expert at executing plans."),
                HumanMessage(content=prompt)
            ]
            response = await self.llm.ainvoke(messages)
            response_text = response.content if hasattr(response, 'content') else str(response)
            
            state["current_result"] = response_text
            state["final_result"] = response_text  # Simplified - customize parsing
            state["current_step"] = "execution"
            state["step_count"] += 1
            
            logger.info("Execution complete")
            
        except Exception as e:
            logger.error(f"Execution failed: {e}")
            state["errors"].append(f"Execution error: {str(e)}")
            state["final_result"] = ""
        
        return state


class ValidationAgent:
    """Agent responsible for validating results."""
    
    def __init__(self, llm):
        self.llm = llm
    
    async def validate(self, state: AgentState) -> AgentState:
        """
        Validate the execution results.
        
        Args:
            state: Current agent state
        
        Returns:
            Updated state with validation results
        
        Time Complexity: O(1) - Single LLM call
        Space Complexity: O(1)
        """
        logger.info("Validation Agent: Validating results...")
        
        result = state.get("final_result", "")
        query = state["query"]
        
        if not result:
            state["is_valid"] = False
            state["validation_errors"].append("No result generated")
            return state
        
        # Basic validation
        state["is_valid"] = True
        state["current_step"] = "validation"
        state["step_count"] += 1
        
        logger.info("Validation complete")
        
        return state

