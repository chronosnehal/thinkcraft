#!/usr/bin/env python3
"""
Core Agent Logic for [Use Case Name]

This module implements the agent orchestration logic including
perception, reasoning, and action steps.

Time Complexity: O(k) where k is number of agent steps
Space Complexity: O(n) where n is total data processed
"""

from app.utils.llm_client_manager import LLMClientManager
from models import AgentStep, AgentExecutionLog, TaskStatus
from typing import Optional, Dict, Any, List
from datetime import datetime
import logging
import time
import asyncio

logger = logging.getLogger(__name__)


class AgentOrchestrator:
    """
    Orchestrates multi-step agent workflow.
    
    This class implements the core agentic behavior:
    1. Perceive: Understand and parse the input
    2. Reason: Analyze and plan the approach
    3. Act: Execute the plan and generate results
    
    Attributes:
        manager: LLMClientManager for LLM interactions
        provider: LLM provider to use
        model: Model name
        max_steps: Maximum number of steps allowed
        execution_history: History of executions
        current_task: Currently executing task
    """
    
    def __init__(
        self,
        provider: str = "openai",
        model: Optional[str] = None,
        max_steps: int = 10
    ):
        """
        Initialize agent orchestrator.
        
        Args:
            provider: LLM provider name
            model: Model name (uses default if None)
            max_steps: Maximum steps per execution
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        self.manager = LLMClientManager()
        self.provider = provider
        self.model = model or self._get_default_model(provider)
        self.max_steps = max_steps
        
        # State management
        self.execution_history: List[AgentExecutionLog] = []
        self.current_task: Optional[str] = None
        self.task_registry: Dict[str, AgentExecutionLog] = {}
        self.start_time = datetime.now()
        
        logger.info(f"Agent orchestrator initialized with {provider}/{self.model}")
    
    def _get_default_model(self, provider: str) -> str:
        """Get default model for provider."""
        defaults = {
            "openai": "gpt-4",
            "azure": "gpt-4",
            "gemini": "gemini-pro",
            "claude": "claude-3-opus-20240229",
            "openrouter": "openai/gpt-4"
        }
        return defaults.get(provider, "gpt-4")
    
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
        
        Time Complexity: O(k) where k is number of steps
        Space Complexity: O(n) where n is data size
        
        Examples:
            >>> orchestrator = AgentOrchestrator()
            >>> result = await orchestrator.execute("Analyze sales data")
            >>> print(result)
        """
        start_time = time.time()
        
        # Validate input
        if not query or not query.strip():
            raise ValueError("Query cannot be empty")
        
        self.current_task = query
        logger.info(f"Starting agent execution for: {query}")
        
        try:
            # Step 1: Perceive - Understand the input
            perception = await self._perceive(query, context)
            logger.info("Perception step completed")
            
            # Step 2: Reason - Plan the approach
            reasoning = await self._reason(perception, parameters)
            logger.info("Reasoning step completed")
            
            # Step 3: Act - Execute the plan
            action_result = await self._act(reasoning, parameters)
            logger.info("Action step completed")
            
            # Step 4: Reflect - Validate and refine result
            final_result = await self._reflect(action_result)
            logger.info("Reflection step completed")
            
            duration = time.time() - start_time
            logger.info(f"Agent execution completed in {duration:.2f}s")
            
            self.current_task = None
            return final_result
            
        except Exception as e:
            logger.error(f"Agent execution failed: {e}", exc_info=True)
            self.current_task = None
            raise RuntimeError(f"Agent execution failed: {str(e)}")
    
    async def _perceive(
        self,
        query: str,
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Perception step: Understand and parse the input.
        
        Args:
            query: User query
            context: Optional context
        
        Returns:
            Structured perception data
        
        Time Complexity: O(1) - Single LLM call
        Space Complexity: O(n) - Response size
        """
        logger.debug("Executing perception step")
        
        prompt = self._build_perception_prompt(query, context)
        
        try:
            response = await self.manager.generate_async(
                provider=self.provider,
                prompt=prompt,
                model=self.model,
                temperature=0.3  # Lower temperature for parsing
            )
            
            # Parse response into structured format
            perception_data = {
                "original_query": query,
                "context": context,
                "parsed_intent": response,
                "timestamp": datetime.now().isoformat()
            }
            
            logger.debug(f"Perception result: {perception_data}")
            return perception_data
            
        except Exception as e:
            logger.error(f"Perception step failed: {e}")
            raise
    
    async def _reason(
        self,
        perception: Dict[str, Any],
        parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Reasoning step: Analyze and plan the approach.
        
        Args:
            perception: Output from perception step
            parameters: Optional parameters
        
        Returns:
            Reasoning plan and strategy
        
        Time Complexity: O(1) - Single LLM call
        Space Complexity: O(n) - Response size
        """
        logger.debug("Executing reasoning step")
        
        prompt = self._build_reasoning_prompt(perception, parameters)
        
        try:
            response = await self.manager.generate_async(
                provider=self.provider,
                prompt=prompt,
                model=self.model,
                temperature=0.7  # Moderate temperature for reasoning
            )
            
            reasoning_data = {
                "perception": perception,
                "plan": response,
                "parameters": parameters,
                "timestamp": datetime.now().isoformat()
            }
            
            logger.debug(f"Reasoning result: {reasoning_data}")
            return reasoning_data
            
        except Exception as e:
            logger.error(f"Reasoning step failed: {e}")
            raise
    
    async def _act(
        self,
        reasoning: Dict[str, Any],
        parameters: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Action step: Execute the plan.
        
        Args:
            reasoning: Output from reasoning step
            parameters: Optional parameters
        
        Returns:
            Action result
        
        Time Complexity: O(1) - Single LLM call
        Space Complexity: O(n) - Response size
        """
        logger.debug("Executing action step")
        
        prompt = self._build_action_prompt(reasoning, parameters)
        
        try:
            response = await self.manager.generate_async(
                provider=self.provider,
                prompt=prompt,
                model=self.model,
                temperature=0.5  # Balanced temperature for action
            )
            
            logger.debug(f"Action result: {response[:100]}...")
            return response
            
        except Exception as e:
            logger.error(f"Action step failed: {e}")
            raise
    
    async def _reflect(self, action_result: str) -> str:
        """
        Reflection step: Validate and refine the result.
        
        Args:
            action_result: Output from action step
        
        Returns:
            Refined final result
        
        Time Complexity: O(1) - Single LLM call
        Space Complexity: O(n) - Response size
        """
        logger.debug("Executing reflection step")
        
        prompt = self._build_reflection_prompt(action_result)
        
        try:
            response = await self.manager.generate_async(
                provider=self.provider,
                prompt=prompt,
                model=self.model,
                temperature=0.3  # Lower temperature for validation
            )
            
            logger.debug(f"Reflection result: {response[:100]}...")
            return response
            
        except Exception as e:
            logger.warning(f"Reflection step failed, returning action result: {e}")
            # If reflection fails, return action result
            return action_result
    
    def _build_perception_prompt(
        self,
        query: str,
        context: Optional[str]
    ) -> str:
        """Build prompt for perception step."""
        prompt = f"""You are an intelligent agent analyzing a user query.

Query: {query}
"""
        if context:
            prompt += f"\nContext: {context}"
        
        prompt += """

Analyze this query and provide:
1. The main intent or goal
2. Key entities or concepts mentioned
3. Any implicit requirements or constraints
4. Suggested approach to address the query

Be concise and structured in your response."""
        
        return prompt
    
    def _build_reasoning_prompt(
        self,
        perception: Dict[str, Any],
        parameters: Optional[Dict[str, Any]]
    ) -> str:
        """Build prompt for reasoning step."""
        prompt = f"""You are an intelligent agent planning how to accomplish a task.

Perceived Intent: {perception.get('parsed_intent', '')}
Original Query: {perception.get('original_query', '')}
"""
        if parameters:
            prompt += f"\nParameters: {parameters}"
        
        prompt += """

Create a detailed plan to accomplish this task:
1. Break down the task into logical steps
2. Identify required resources or information
3. Anticipate potential challenges
4. Outline the execution strategy

Provide a clear, actionable plan."""
        
        return prompt
    
    def _build_action_prompt(
        self,
        reasoning: Dict[str, Any],
        parameters: Optional[Dict[str, Any]]
    ) -> str:
        """Build prompt for action step."""
        prompt = f"""You are an intelligent agent executing a planned task.

Plan: {reasoning.get('plan', '')}
Original Query: {reasoning.get('perception', {}).get('original_query', '')}
"""
        if parameters:
            prompt += f"\nParameters: {parameters}"
        
        prompt += """

Execute the plan and provide:
1. The complete result or solution
2. Any relevant details or explanations
3. Confidence level in the result

Be thorough and accurate in your execution."""
        
        return prompt
    
    def _build_reflection_prompt(self, action_result: str) -> str:
        """Build prompt for reflection step."""
        return f"""You are an intelligent agent reviewing your work.

Result: {action_result}

Review this result and:
1. Verify it addresses the original query
2. Check for any errors or inconsistencies
3. Refine or improve the result if needed
4. Provide the final, polished version

Return the refined result."""
    
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
        log = AgentExecutionLog(
            task_id=task_id,
            query=query,
            status=TaskStatus.RUNNING
        )
        
        self.task_registry[task_id] = log
        
        try:
            result = await self.execute(query, context, parameters)
            log.final_result = result
            log.status = TaskStatus.COMPLETED
            
        except Exception as e:
            logger.error(f"Background task {task_id} failed: {e}")
            log.status = TaskStatus.FAILED
            log.final_result = f"Error: {str(e)}"
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get current agent status.
        
        Returns:
            Status information
        """
        uptime = datetime.now() - self.start_time
        
        return {
            "is_active": self.current_task is not None,
            "current_task": self.current_task,
            "tasks_completed": len(self.execution_history),
            "uptime": str(uptime).split('.')[0]  # Remove microseconds
        }
    
    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get status of specific task."""
        log = self.task_registry.get(task_id)
        
        if not log:
            return None
        
        return {
            "task_id": task_id,
            "status": log.status.value,
            "query": log.query,
            "result": log.final_result,
            "timestamp": log.timestamp.isoformat()
        }
    
    def get_execution_steps(self) -> int:
        """Get number of steps in last execution."""
        return 4  # perceive, reason, act, reflect
    
    def get_capabilities(self) -> List[str]:
        """Get list of agent capabilities."""
        return [
            "Query understanding and parsing",
            "Multi-step reasoning and planning",
            "Task execution and action",
            "Result validation and refinement",
            "Async execution support"
        ]
    
    def reset(self):
        """Reset agent to initial state."""
        self.execution_history.clear()
        self.task_registry.clear()
        self.current_task = None
        logger.info("Agent orchestrator reset")

