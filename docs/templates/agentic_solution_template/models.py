#!/usr/bin/env python3
"""
Pydantic Models for [Use Case Name] Agentic System

This module defines all data models used for request/response validation
and internal data structures.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum


class TaskStatus(str, Enum):
    """Enum for task execution status."""
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class InputData(BaseModel):
    """
    Input model for agent execution requests.
    
    Attributes:
        query: Main query or task for the agent
        context: Optional context information
        parameters: Optional additional parameters
    """
    query: str = Field(
        ...,
        description="Query or task for the agent to execute",
        min_length=1,
        max_length=5000,
        example="Analyze sales data and generate insights"
    )
    
    context: Optional[str] = Field(
        None,
        description="Additional context for the query",
        max_length=10000,
        example="Q4 2024 sales data for North America region"
    )
    
    parameters: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Additional parameters for execution",
        example={"format": "json", "detail_level": "high"}
    )
    
    @validator("query")
    def query_not_empty(cls, v):
        """Validate that query is not empty or whitespace."""
        if not v or not v.strip():
            raise ValueError("Query cannot be empty or whitespace")
        return v.strip()
    
    @validator("parameters")
    def validate_parameters(cls, v):
        """Validate parameters dictionary."""
        if v is None:
            return {}
        
        # Add custom parameter validation here
        allowed_keys = {"format", "detail_level", "max_steps", "temperature"}
        invalid_keys = set(v.keys()) - allowed_keys
        
        if invalid_keys:
            raise ValueError(f"Invalid parameters: {invalid_keys}")
        
        return v
    
    class Config:
        """Pydantic config."""
        schema_extra = {
            "example": {
                "query": "Analyze customer feedback and identify trends",
                "context": "Last 30 days of customer reviews",
                "parameters": {
                    "format": "json",
                    "detail_level": "high"
                }
            }
        }


class OutputData(BaseModel):
    """
    Output model for agent execution results.
    
    Attributes:
        result: Main result from agent execution
        status: Execution status
        metadata: Additional metadata about execution
        timestamp: When the result was generated
    """
    result: str = Field(
        ...,
        description="Result from agent execution",
        example="Analysis complete: 3 key trends identified"
    )
    
    status: str = Field(
        ...,
        description="Execution status",
        example="success"
    )
    
    metadata: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Additional metadata about execution",
        example={
            "steps_executed": 5,
            "execution_time": "2.3s",
            "tokens_used": 1500
        }
    )
    
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="Timestamp of result generation"
    )
    
    class Config:
        """Pydantic config."""
        schema_extra = {
            "example": {
                "result": "Analysis complete with 3 key insights",
                "status": "success",
                "metadata": {
                    "steps_executed": 5,
                    "execution_time": "2.3s"
                },
                "timestamp": "2024-01-01T12:00:00"
            }
        }


class AgentStatus(BaseModel):
    """
    Model for agent system status.
    
    Attributes:
        is_active: Whether agent is currently active
        current_task: Description of current task if any
        tasks_completed: Number of tasks completed
        uptime: System uptime
    """
    is_active: bool = Field(
        ...,
        description="Whether agent is currently processing a task"
    )
    
    current_task: Optional[str] = Field(
        None,
        description="Description of current task if active"
    )
    
    tasks_completed: int = Field(
        default=0,
        description="Total number of tasks completed",
        ge=0
    )
    
    uptime: str = Field(
        default="0s",
        description="System uptime",
        example="2h 30m"
    )
    
    class Config:
        """Pydantic config."""
        schema_extra = {
            "example": {
                "is_active": True,
                "current_task": "Analyzing data",
                "tasks_completed": 42,
                "uptime": "2h 30m"
            }
        }


class ErrorResponse(BaseModel):
    """
    Model for error responses.
    
    Attributes:
        error: Error type
        message: Error message
        details: Additional error details
        timestamp: When error occurred
    """
    error: str = Field(
        ...,
        description="Error type",
        example="ValidationError"
    )
    
    message: str = Field(
        ...,
        description="Error message",
        example="Invalid input data"
    )
    
    details: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional error details"
    )
    
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="When error occurred"
    )
    
    class Config:
        """Pydantic config."""
        schema_extra = {
            "example": {
                "error": "ValidationError",
                "message": "Query cannot be empty",
                "details": {"field": "query"},
                "timestamp": "2024-01-01T12:00:00"
            }
        }


class AgentStep(BaseModel):
    """
    Model for individual agent execution step.
    
    Attributes:
        step_number: Sequential step number
        step_type: Type of step (perceive, reason, act)
        description: Description of what happened
        input_data: Input to this step
        output_data: Output from this step
        duration: How long step took
        success: Whether step succeeded
    """
    step_number: int = Field(
        ...,
        description="Sequential step number",
        ge=1
    )
    
    step_type: str = Field(
        ...,
        description="Type of step",
        example="reason"
    )
    
    description: str = Field(
        ...,
        description="What this step does",
        example="Analyzing input data"
    )
    
    input_data: Optional[str] = Field(
        None,
        description="Input to this step"
    )
    
    output_data: Optional[str] = Field(
        None,
        description="Output from this step"
    )
    
    duration: Optional[float] = Field(
        None,
        description="Duration in seconds",
        ge=0
    )
    
    success: bool = Field(
        default=True,
        description="Whether step succeeded"
    )
    
    class Config:
        """Pydantic config."""
        schema_extra = {
            "example": {
                "step_number": 1,
                "step_type": "perceive",
                "description": "Analyzing input query",
                "input_data": "Analyze sales data",
                "output_data": "Query parsed successfully",
                "duration": 0.5,
                "success": True
            }
        }


class AgentExecutionLog(BaseModel):
    """
    Complete execution log for agent workflow.
    
    Attributes:
        task_id: Unique task identifier
        query: Original query
        steps: List of execution steps
        final_result: Final result
        total_duration: Total execution time
        status: Final status
        timestamp: When execution started
    """
    task_id: str = Field(
        ...,
        description="Unique task identifier"
    )
    
    query: str = Field(
        ...,
        description="Original query"
    )
    
    steps: List[AgentStep] = Field(
        default_factory=list,
        description="List of execution steps"
    )
    
    final_result: Optional[str] = Field(
        None,
        description="Final result"
    )
    
    total_duration: Optional[float] = Field(
        None,
        description="Total execution time in seconds",
        ge=0
    )
    
    status: TaskStatus = Field(
        default=TaskStatus.QUEUED,
        description="Final execution status"
    )
    
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="When execution started"
    )
    
    class Config:
        """Pydantic config."""
        schema_extra = {
            "example": {
                "task_id": "abc-123-def",
                "query": "Analyze sales data",
                "steps": [
                    {
                        "step_number": 1,
                        "step_type": "perceive",
                        "description": "Parse query",
                        "success": True
                    }
                ],
                "final_result": "Analysis complete",
                "total_duration": 2.5,
                "status": "completed",
                "timestamp": "2024-01-01T12:00:00"
            }
        }

