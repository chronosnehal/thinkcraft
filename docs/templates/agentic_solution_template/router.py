#!/usr/bin/env python3
"""
API Routes for [Use Case Name] Agentic System

This module defines all API endpoints for the agentic system.
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from models import (
    InputData,
    OutputData,
    AgentStatus,
    ErrorResponse
)
from solution import AgentOrchestrator
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

# Global orchestrator instance (consider using dependency injection in production)
orchestrator = AgentOrchestrator()


@router.post("/execute/", response_model=OutputData)
async def execute_agent(data: InputData):
    """
    Execute the agent workflow.
    
    This endpoint triggers the agent to perform its multi-step reasoning,
    planning, and acting process based on the provided input.
    
    Args:
        data: Input data for the agent
    
    Returns:
        Agent execution results with status
    
    Raises:
        HTTPException: If execution fails
    
    Example:
        ```
        POST /api/v1/execute/
        {
            "query": "Analyze sales data and generate report",
            "context": "Q4 2024 sales",
            "parameters": {"format": "pdf"}
        }
        ```
    """
    logger.info(f"Received execution request: {data.query}")
    
    try:
        # Execute agent workflow
        result = await orchestrator.execute(
            query=data.query,
            context=data.context,
            parameters=data.parameters
        )
        
        logger.info("Agent execution completed successfully")
        
        return OutputData(
            result=result,
            status="success",
            metadata={
                "query": data.query,
                "steps_executed": orchestrator.get_execution_steps()
            }
        )
        
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        logger.error(f"Agent execution failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Agent execution failed: {str(e)}"
        )


@router.post("/execute-async/", response_model=Dict[str, str])
async def execute_agent_async(data: InputData, background_tasks: BackgroundTasks):
    """
    Execute agent workflow asynchronously in background.
    
    This endpoint queues the agent execution and returns immediately
    with a task ID. Use /status/{task_id} to check progress.
    
    Args:
        data: Input data for the agent
        background_tasks: FastAPI background tasks
    
    Returns:
        Task ID for tracking execution
    
    Example:
        ```
        POST /api/v1/execute-async/
        {
            "query": "Process large dataset",
            "context": "Monthly reports"
        }
        ```
    """
    import uuid
    
    task_id = str(uuid.uuid4())
    logger.info(f"Queuing async execution with task_id: {task_id}")
    
    # Add task to background
    background_tasks.add_task(
        orchestrator.execute_background,
        task_id=task_id,
        query=data.query,
        context=data.context,
        parameters=data.parameters
    )
    
    return {
        "task_id": task_id,
        "status": "queued",
        "message": "Agent execution queued. Use /status/{task_id} to check progress."
    }


@router.get("/status/", response_model=AgentStatus)
async def get_agent_status():
    """
    Get current status of the agent system.
    
    Returns:
        Current agent status and statistics
    
    Example:
        ```
        GET /api/v1/status/
        ```
    """
    try:
        status = orchestrator.get_status()
        
        return AgentStatus(
            is_active=status["is_active"],
            current_task=status.get("current_task"),
            tasks_completed=status.get("tasks_completed", 0),
            uptime=status.get("uptime", "0s")
        )
        
    except Exception as e:
        logger.error(f"Error getting status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status/{task_id}", response_model=Dict[str, Any])
async def get_task_status(task_id: str):
    """
    Get status of a specific async task.
    
    Args:
        task_id: Task ID returned from /execute-async/
    
    Returns:
        Task status and result if completed
    
    Example:
        ```
        GET /api/v1/status/abc-123-def
        ```
    """
    try:
        task_status = orchestrator.get_task_status(task_id)
        
        if not task_status:
            raise HTTPException(
                status_code=404,
                detail=f"Task {task_id} not found"
            )
        
        return task_status
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting task status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reset/")
async def reset_agent():
    """
    Reset the agent to initial state.
    
    This clears any cached state, task history, and resets
    the agent to its initial configuration.
    
    Returns:
        Confirmation message
    
    Example:
        ```
        POST /api/v1/reset/
        ```
    """
    try:
        orchestrator.reset()
        logger.info("Agent reset successfully")
        
        return {
            "status": "success",
            "message": "Agent reset to initial state"
        }
        
    except Exception as e:
        logger.error(f"Error resetting agent: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/capabilities/")
async def get_capabilities():
    """
    Get agent capabilities and supported operations.
    
    Returns:
        List of agent capabilities
    
    Example:
        ```
        GET /api/v1/capabilities/
        ```
    """
    return {
        "capabilities": orchestrator.get_capabilities(),
        "supported_providers": ["openai", "azure", "gemini", "claude"],
        "max_steps": 10,
        "supports_async": True
    }

