# FastAPI Guide for Agentic Systems

**Author:** chronosnehal

This guide covers FastAPI implementation patterns for building agentic systems in ThinkCraft.

---

## Directory Structure

Every agentic system follows this structure:

```
/app/agentic/<usecase_name>/
├── main.py                # FastAPI app initialization
├── router.py              # API routes
├── solution.py            # Agent orchestration logic
├── models.py              # Pydantic models
├── question_<usecase_name>.md
├── README.md
└── requirements.txt
```

---

## File Responsibilities

### 1. main.py - Application Entry Point

**Purpose:** Initialize FastAPI app, configure middleware, include routers.

```python
#!/usr/bin/env python3
"""
[Use Case Name] - Agentic System Main Application

Author: chronosnehal
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router import router
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="[Use Case Name] Agent",
    description="Agentic system for [purpose]",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router, prefix="/api/v1", tags=["agent"])

@app.get("/")
def root():
    """Health check endpoint."""
    return {
        "status": "active",
        "service": "[Use Case Name] Agent",
        "version": "1.0.0"
    }

@app.on_event("startup")
async def startup_event():
    """Execute on application startup."""
    logger.info("Agent starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    """Execute on application shutdown."""
    logger.info("Agent shutting down...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
```

**Key Points:**
- Keep minimal - only app initialization
- Configure CORS appropriately
- Add health check endpoint
- Use startup/shutdown events for initialization

---

### 2. router.py - API Routes

**Purpose:** Define all API endpoints for the agentic system.

```python
#!/usr/bin/env python3
"""
API Routes for [Use Case Name] Agentic System

Author: chronosnehal
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from models import InputData, OutputData, AgentStatus
from solution import AgentOrchestrator
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize orchestrator
orchestrator = AgentOrchestrator()

@router.post("/execute/", response_model=OutputData)
async def execute_agent(data: InputData):
    """
    Execute the agent workflow synchronously.
    
    Args:
        data: Input data for the agent
    
    Returns:
        Agent execution results
    
    Raises:
        HTTPException: If execution fails
    """
    logger.info(f"Received execution request: {data.query}")
    
    try:
        result = await orchestrator.execute(
            query=data.query,
            context=data.context,
            parameters=data.parameters
        )
        
        return OutputData(
            result=result,
            status="success",
            metadata={"query": data.query}
        )
        
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        logger.error(f"Execution failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status/", response_model=AgentStatus)
async def get_agent_status():
    """Get current status of the agent system."""
    try:
        status = orchestrator.get_status()
        return AgentStatus(**status)
    except Exception as e:
        logger.error(f"Error getting status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reset/")
async def reset_agent():
    """Reset the agent to initial state."""
    try:
        orchestrator.reset()
        return {"status": "success", "message": "Agent reset"}
    except Exception as e:
        logger.error(f"Error resetting agent: {e}")
        raise HTTPException(status_code=500, detail=str(e))
```

**Key Points:**
- One endpoint per agent operation
- Use Pydantic models for validation
- Proper error handling with HTTP status codes
- Comprehensive logging
- Clear docstrings

---

### 3. models.py - Pydantic Models

**Purpose:** Define data models for request/response validation.

```python
#!/usr/bin/env python3
"""
Pydantic Models for [Use Case Name] Agentic System

Author: chronosnehal
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum

class TaskStatus(str, Enum):
    """Enum for task execution status."""
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class InputData(BaseModel):
    """Input model for agent execution requests."""
    query: str = Field(
        ...,
        description="Query or task for the agent",
        min_length=1,
        max_length=5000,
        example="Analyze sales data"
    )
    
    context: Optional[str] = Field(
        None,
        description="Additional context",
        max_length=10000
    )
    
    parameters: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Additional parameters"
    )
    
    @validator("query")
    def query_not_empty(cls, v):
        """Validate query is not empty."""
        if not v or not v.strip():
            raise ValueError("Query cannot be empty")
        return v.strip()
    
    class Config:
        schema_extra = {
            "example": {
                "query": "Analyze customer feedback",
                "context": "Last 30 days",
                "parameters": {"format": "json"}
            }
        }

class OutputData(BaseModel):
    """Output model for agent execution results."""
    result: str = Field(..., description="Agent result")
    status: str = Field(..., description="Execution status")
    metadata: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Additional metadata"
    )
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="Result timestamp"
    )

class AgentStatus(BaseModel):
    """Model for agent system status."""
    is_active: bool
    current_task: Optional[str] = None
    tasks_completed: int = 0
    uptime: str = "0s"
```

**Key Points:**
- Use Field() for validation and documentation
- Add validators for complex validation
- Include examples in Config
- Use Enums for fixed choices
- Type hints on all fields

---

### 4. solution.py - Agent Logic

**Purpose:** Implement the core agent orchestration logic.

```python
#!/usr/bin/env python3
"""
Core Agent Logic for [Use Case Name]

Implements the 4-step agentic workflow:
1. Perceive - Understand input
2. Reason - Plan approach
3. Act - Execute plan
4. Reflect - Validate results

Author: chronosnehal
"""

from app.utils.llm_client_manager import LLMClientManager
from typing import Optional, Dict, Any
from datetime import datetime
import logging
import time

logger = logging.getLogger(__name__)

class AgentOrchestrator:
    """
    Orchestrates multi-step agent workflow.
    
    Attributes:
        manager: LLMClientManager for LLM interactions
        provider: LLM provider to use
        model: Model name
        current_task: Currently executing task
    """
    
    def __init__(self, provider: str = "openai", model: Optional[str] = None):
        """Initialize agent orchestrator."""
        self.manager = LLMClientManager()
        self.provider = provider
        self.model = model or "gpt-4"
        self.current_task = None
        self.start_time = datetime.now()
        
        logger.info(f"Agent initialized with {provider}/{self.model}")
    
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
            context: Optional context
            parameters: Optional parameters
        
        Returns:
            Final result from agent execution
        
        Time Complexity: O(k) where k is number of steps
        Space Complexity: O(n) where n is data size
        """
        start_time = time.time()
        self.current_task = query
        
        logger.info(f"Starting execution: {query}")
        
        try:
            # Step 1: Perceive
            perception = await self._perceive(query, context)
            
            # Step 2: Reason
            reasoning = await self._reason(perception, parameters)
            
            # Step 3: Act
            action_result = await self._act(reasoning, parameters)
            
            # Step 4: Reflect
            final_result = await self._reflect(action_result)
            
            duration = time.time() - start_time
            logger.info(f"Execution completed in {duration:.2f}s")
            
            self.current_task = None
            return final_result
            
        except Exception as e:
            logger.error(f"Execution failed: {e}", exc_info=True)
            self.current_task = None
            raise
    
    async def _perceive(self, query: str, context: Optional[str]) -> Dict[str, Any]:
        """
        Perception step: Understand and parse input.
        
        Time Complexity: O(1) - Single LLM call
        Space Complexity: O(n) - Response size
        """
        logger.debug("Executing perception step")
        
        prompt = f"Analyze this query: {query}"
        if context:
            prompt += f"\nContext: {context}"
        
        response = await self.manager.generate_async(
            provider=self.provider,
            prompt=prompt,
            model=self.model,
            temperature=0.3
        )
        
        return {
            "original_query": query,
            "context": context,
            "parsed_intent": response
        }
    
    async def _reason(
        self,
        perception: Dict[str, Any],
        parameters: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Reasoning step: Plan the approach.
        
        Time Complexity: O(1) - Single LLM call
        Space Complexity: O(n) - Response size
        """
        logger.debug("Executing reasoning step")
        
        prompt = f"Create a plan for: {perception['parsed_intent']}"
        
        response = await self.manager.generate_async(
            provider=self.provider,
            prompt=prompt,
            model=self.model,
            temperature=0.7
        )
        
        return {
            "perception": perception,
            "plan": response,
            "parameters": parameters
        }
    
    async def _act(
        self,
        reasoning: Dict[str, Any],
        parameters: Optional[Dict[str, Any]]
    ) -> str:
        """
        Action step: Execute the plan.
        
        Time Complexity: O(1) - Single LLM call
        Space Complexity: O(n) - Response size
        """
        logger.debug("Executing action step")
        
        prompt = f"Execute this plan: {reasoning['plan']}"
        
        response = await self.manager.generate_async(
            provider=self.provider,
            prompt=prompt,
            model=self.model,
            temperature=0.5
        )
        
        return response
    
    async def _reflect(self, action_result: str) -> str:
        """
        Reflection step: Validate and refine result.
        
        Time Complexity: O(1) - Single LLM call
        Space Complexity: O(n) - Response size
        """
        logger.debug("Executing reflection step")
        
        prompt = f"Review and refine: {action_result}"
        
        try:
            response = await self.manager.generate_async(
                provider=self.provider,
                prompt=prompt,
                model=self.model,
                temperature=0.3
            )
            return response
        except Exception as e:
            logger.warning(f"Reflection failed: {e}")
            return action_result
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status."""
        uptime = datetime.now() - self.start_time
        return {
            "is_active": self.current_task is not None,
            "current_task": self.current_task,
            "tasks_completed": 0,
            "uptime": str(uptime).split('.')[0]
        }
    
    def reset(self):
        """Reset agent to initial state."""
        self.current_task = None
        logger.info("Agent reset")
```

**Key Points:**
- Implement 4-step workflow (Perceive, Reason, Act, Reflect)
- Use LLMClientManager for all LLM calls
- Comprehensive logging
- Error handling at each step
- State management

---

## Best Practices

### 1. Keep main.py Minimal
- Only app initialization
- No business logic
- Configuration only

### 2. Use router.py for Routes
- One file for all endpoints
- Group related endpoints
- Use APIRouter

### 3. Place Logic in solution.py
- All agent logic here
- Separate from API layer
- Testable independently

### 4. Use Pydantic for Validation
- Validate all inputs
- Document with Field()
- Add custom validators

### 5. Use LLMClientManager
- Centralized LLM access
- Easy provider switching
- Consistent interface

---

## Running the Application

```bash
# Development
cd app/agentic/<usecase_name>
uvicorn main:app --reload --port 8000

# Production
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# With custom settings
uvicorn main:app --reload --port 8000 --log-level debug
```

---

## Testing

```bash
# Start server
uvicorn main:app --reload

# Test with curl
curl -X POST http://localhost:8000/api/v1/execute/ \
  -H "Content-Type: application/json" \
  -d '{"query": "test query"}'

# Visit API docs
open http://localhost:8000/docs
```

---

## Quick Reference

```python
# Perfect agentic system structure
/app/agentic/my_agent/
├── main.py          # FastAPI init
├── router.py        # API routes
├── solution.py      # Agent logic (4 steps)
├── models.py        # Pydantic models
├── requirements.txt
└── README.md
```

---

**Follow this structure for all agentic systems in ThinkCraft!**
