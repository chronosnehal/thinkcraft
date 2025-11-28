#!/usr/bin/env python3
"""
Agent Orchestration Service

Implements the agentic workflow using LangGraph for orchestration.
Agents: Perception → Planning → Execution → Validation

Time Complexity: O(k) where k = number of agent steps
Space Complexity: O(n) where n = size of data processed

Author: chronosnehal
Date: [YYYY-MM-DD]
"""

import logging
from typing import Optional, Dict, Any
from langgraph.graph import StateGraph, END

from ..core.agent_state import AgentState
from ..core.agents import (
    PerceptionAgent,
    PlanningAgent,
    ExecutionAgent,
    ValidationAgent
)
from ..core.llm_adapter import LangChainLLMAdapter

logger = logging.getLogger(__name__)


class AgentOrchestrator:
    """
    Orchestrates multi-step agent workflow using LangGraph.
    
    This class implements the core agentic behavior:
    1. Perceive: Understand and parse the input
    2. Plan: Analyze and plan the approach
    3. Execute: Execute the plan
    4. Validate: Validate the results
    
    Attributes:
        llm: LangChain LLM instance
        provider: LLM provider name
        workflow: LangGraph workflow
    """
    
    def __init__(
        self,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7
    ):
        """
        Initialize agent orchestrator.
        
        Args:
            provider: LLM provider (openai, anthropic, gemini, claude, azure)
                     If None, reads from LLM_PROVIDER env var
            model: Model name (if None, uses default for provider)
            temperature: Temperature for generation
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        # Create LLM instance using adapter
        self.llm = LangChainLLMAdapter.create_llm(
            provider=provider,
            model=model,
            temperature=temperature
        )
        
        # Get provider name for metadata
        if provider is None:
            import os
            self.provider = os.getenv("LLM_PROVIDER", "openai").lower()
        else:
            self.provider = provider.lower()
        
        # Initialize agents
        self.perception_agent = PerceptionAgent(self.llm)
        self.planning_agent = PlanningAgent(self.llm)
        self.execution_agent = ExecutionAgent(self.llm)
        self.validation_agent = ValidationAgent(self.llm)
        
        # Build workflow
        self.workflow = self._build_workflow()
        
        # State tracking
        from datetime import datetime
        self.start_time = datetime.now()
        
        logger.info(f"Agent orchestrator initialized with {self.provider}")
    
    def _build_workflow(self) -> StateGraph:
        """
        Build the LangGraph workflow with agent nodes.
        
        Returns:
            Compiled LangGraph workflow
        """
        # Create graph
        workflow = StateGraph(AgentState)
        
        # Add nodes (agents)
        workflow.add_node("perceive", self.perception_agent.perceive)
        workflow.add_node("plan", self.planning_agent.plan)
        workflow.add_node("execute", self.execution_agent.execute)
        workflow.add_node("validate", self.validation_agent.validate)
        
        # Define edges
        workflow.set_entry_point("perceive")
        workflow.add_edge("perceive", "plan")
        workflow.add_edge("plan", "execute")
        workflow.add_edge("execute", "validate")
        workflow.add_edge("validate", END)
        
        # Compile workflow
        return workflow.compile()
    
    async def execute(
        self,
        query: str,
        context: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Execute the complete agent workflow.
        
        Args:
            query: User query or task
            context: Optional context information
            parameters: Optional execution parameters
        
        Returns:
            Final result from agent execution
        
        Raises:
            ValueError: If query is invalid
            RuntimeError: If execution fails
        
        Time Complexity: O(k) where k = number of agent steps
        Space Complexity: O(n) where n = data size
        """
        # Validate input
        if not query or not query.strip():
            raise ValueError("Query cannot be empty")
        
        logger.info(f"Starting agent execution for: {query}")
        
        # Initialize state
        initial_state: AgentState = {
            "query": query,
            "context": context,
            "parameters": parameters or {},
            "perceived_intent": None,
            "parsed_data": None,
            "key_entities": None,
            "plan": None,
            "approach": None,
            "steps": None,
            "intermediate_results": None,
            "current_result": None,
            "is_valid": False,
            "validation_errors": [],
            "final_result": None,
            "explanation": None,
            "step_count": 0,
            "current_step": "start",
            "errors": [],
            "metadata": None
        }
        
        try:
            # Execute workflow
            final_state = await self.workflow.ainvoke(initial_state)
            
            # Extract final result
            final_result = final_state.get("final_result", "")
            
            if not final_result:
                raise RuntimeError("No result generated from agent workflow")
            
            logger.info(f"Agent execution completed successfully ({final_state.get('step_count', 0)} steps)")
            return final_result
            
        except Exception as e:
            logger.error(f"Agent execution failed: {e}", exc_info=True)
            raise RuntimeError(f"Agent execution failed: {str(e)}")
    
    async def execute_background(
        self,
        task_id: str,
        query: str,
        context: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None
    ):
        """
        Execute agent workflow in background.
        
        Args:
            task_id: Unique task identifier
            query: User query
            context: Optional context
            parameters: Optional parameters
        """
        # This would typically store task status in a database or cache
        # For template, we'll just execute synchronously
        try:
            result = await self.execute(query, context, parameters)
            logger.info(f"Background task {task_id} completed")
            return result
        except Exception as e:
            logger.error(f"Background task {task_id} failed: {e}")
            raise
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get current agent status.
        
        Returns:
            Status information
        """
        from datetime import datetime
        uptime = datetime.now() - self.start_time
        
        return {
            "is_active": False,  # Would track active tasks in production
            "current_task": None,
            "tasks_completed": 0,  # Would track in production
            "uptime": str(uptime).split('.')[0]  # Remove microseconds
        }
    
    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get status of specific task."""
        # Would implement task tracking in production
        return None
    
    def get_execution_steps(self) -> int:
        """Get number of steps in last execution."""
        return 4  # perceive, plan, execute, validate
    
    def get_capabilities(self) -> list[str]:
        """Get list of agent capabilities."""
        return [
            "Query understanding and parsing",
            "Multi-step reasoning and planning",
            "Task execution and action",
            "Result validation",
            "Async execution support"
        ]
    
    def reset(self):
        """Reset agent to initial state."""
        logger.info("Agent orchestrator reset")


# Backward compatibility
AgentService = AgentOrchestrator
