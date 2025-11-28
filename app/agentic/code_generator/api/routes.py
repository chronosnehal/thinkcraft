#!/usr/bin/env python3
"""
Code Generator - FastAPI Router

API routes for the code generation system with comprehensive error handling
and validation.

Author: chronosnehal
Date: 2025-11-27
"""

import time
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
import logging

from ..models.schemas import (
    CodeGenerationRequest,
    CodeGenerationResponse,
    ErrorResponse,
    CodeRefinementRequest,
    HealthCheckResponse
)
from ..services.agent_service import CodeGeneratorAgent

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

# Initialize service (will be created per request for better resource management)
service_start_time = time.time()


def get_generator_service() -> CodeGeneratorAgent:
    """
    Factory function to create code generator agent.
    
    Uses LLM_PROVIDER from environment to select provider.
    Falls back to OpenAI if not specified.
    
    Returns:
        CodeGeneratorAgent instance
    """
    # Provider will be read from LLM_PROVIDER env var if None
    return CodeGeneratorAgent(provider=None, model=None, temperature=0.7)


@router.get("/", response_model=dict)
async def root():
    """
    Root endpoint with API information.
    
    Returns:
        API information and available endpoints
    """
    return {
        "service": "AI Code Generator (Agentic)",
        "version": "2.0.0",
        "status": "active",
        "architecture": "Multi-agent system using LangGraph",
        "agents": [
            "Perception Agent - Understands requirements",
            "Planning Agent - Plans code structure",
            "Generation Agent - Generates code",
            "Validation Agent - Validates code",
            "Refinement Agent - Refines code if needed"
        ],
        "endpoints": {
            "generate": "/api/v1/generate - POST - Generate code from prompt (agentic workflow)",
            "refine": "/api/v1/refine - POST - Refine existing code (agentic workflow)",
            "health": "/api/v1/health - GET - Health check"
        },
        "documentation": "/docs"
    }


@router.post("/generate", response_model=CodeGenerationResponse)
async def generate_code(request: CodeGenerationRequest):
    """
    Generate code based on natural language prompt.
    
    This endpoint uses LLM to generate code in the specified programming language
    with proper documentation, tests (optional), and complexity analysis.
    
    Args:
        request: Code generation request with prompt, language, and options
    
    Returns:
        Generated code with documentation and metadata
    
    Raises:
        HTTPException: If generation fails or validation errors occur
    
    Example:
        ```python
        POST /api/v1/generate
        {
            "prompt": "Create a function to sort an array using quicksort",
            "language": "python",
            "complexity": "medium",
            "include_tests": true
        }
        ```
    """
    try:
        logger.info(f"Agentic code generation request: {request.language.value} - {request.complexity.value}")
        
        # Create agent instance
        agent = get_generator_service()
        
        # Generate code using agentic workflow
        response = await agent.generate_code(request)
        
        logger.info(f"Agentic code generation successful: {response.metadata.generation_time}s ({response.metadata.retry_count + 4} agent steps)")
        return response
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "ValidationError",
                "message": str(e),
                "suggestions": ["Check your input parameters and try again"]
            }
        )
    
    except TimeoutError as e:
        logger.error(f"Timeout error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail={
                "error": "TimeoutError",
                "message": "Code generation timed out. Please try with a simpler prompt.",
                "suggestions": [
                    "Simplify your prompt",
                    "Reduce complexity level",
                    "Try again in a moment"
                ]
            }
        )
    
    except Exception as e:
        logger.error(f"Code generation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "GenerationError",
                "message": f"Failed to generate code: {str(e)}",
                "suggestions": [
                    "Check if your prompt is clear and specific",
                    "Try a different programming language",
                    "Reduce complexity level",
                    "Contact support if the issue persists"
                ]
            }
        )


@router.post("/refine", response_model=CodeGenerationResponse)
async def refine_code(request: CodeRefinementRequest):
    """
    Refine existing code based on feedback or requirements.
    
    This endpoint takes existing code and refines it based on the provided
    refinement prompt while optionally preserving original functionality.
    
    Args:
        request: Code refinement request with original code and refinement prompt
    
    Returns:
        Refined code with explanation of changes
    
    Raises:
        HTTPException: If refinement fails
    
    Example:
        ```python
        POST /api/v1/refine
        {
            "original_code": "def add(a, b): return a + b",
            "refinement_prompt": "Add type hints and docstring",
            "language": "python",
            "preserve_functionality": true
        }
        ```
    """
    try:
        logger.info(f"Agentic code refinement request: {request.language.value}")
        
        # Create agent instance
        agent = get_generator_service()
        
        # Refine code using agentic workflow
        response = await agent.refine_code(
            original_code=request.original_code,
            refinement_prompt=request.refinement_prompt,
            language=request.language
        )
        
        logger.info(f"Agentic code refinement successful: {response.metadata.generation_time}s")
        return response
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "ValidationError",
                "message": str(e),
                "suggestions": ["Check your input code and refinement prompt"]
            }
        )
    
    except Exception as e:
        logger.error(f"Code refinement error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "RefinementError",
                "message": f"Failed to refine code: {str(e)}",
                "suggestions": [
                    "Ensure original code is valid",
                    "Make refinement prompt more specific",
                    "Try again with simpler changes"
                ]
            }
        )


@router.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """
    Health check endpoint to verify service status.
    
    Returns:
        Service health status including LLM provider availability
    
    Example:
        ```python
        GET /api/v1/health
        ```
    """
    try:
        # Check LLM providers
        llm_providers = {
            "openai": True,  # Would check actual connectivity in production
            "anthropic": False,  # Example: not configured
            "gemini": False
        }
        
        uptime = time.time() - service_start_time
        
        return HealthCheckResponse(
            status="healthy",
            version="1.0.0",
            llm_providers=llm_providers,
            uptime=round(uptime, 2)
        )
        
    except Exception as e:
        logger.error(f"Health check error: {str(e)}")
        return HealthCheckResponse(
            status="degraded",
            version="1.0.0",
            llm_providers={"openai": False, "anthropic": False, "gemini": False},
            uptime=round(time.time() - service_start_time, 2)
        )


@router.get("/languages", response_model=dict)
async def list_supported_languages():
    """
    List all supported programming languages.
    
    Returns:
        Dictionary of supported languages with descriptions
    
    Example:
        ```python
        GET /api/v1/languages
        ```
    """
    return {
        "languages": {
            "python": {
                "name": "Python",
                "description": "General-purpose programming language",
                "default_style": "functional or OOP",
                "supports_tests": True
            },
            "javascript": {
                "name": "JavaScript",
                "description": "Web and Node.js programming",
                "default_style": "functional",
                "supports_tests": True
            },
            "typescript": {
                "name": "TypeScript",
                "description": "Typed superset of JavaScript",
                "default_style": "functional with types",
                "supports_tests": True
            },
            "java": {
                "name": "Java",
                "description": "Enterprise and Android development",
                "default_style": "OOP",
                "supports_tests": True
            },
            "go": {
                "name": "Go",
                "description": "Systems and backend programming",
                "default_style": "procedural",
                "supports_tests": True
            },
            "rust": {
                "name": "Rust",
                "description": "Systems programming with safety",
                "default_style": "functional",
                "supports_tests": True
            },
            "cpp": {
                "name": "C++",
                "description": "Systems and performance-critical applications",
                "default_style": "OOP or procedural",
                "supports_tests": True
            },
            "csharp": {
                "name": "C#",
                "description": ".NET and Unity development",
                "default_style": "OOP",
                "supports_tests": True
            },
            "ruby": {
                "name": "Ruby",
                "description": "Web development with Rails",
                "default_style": "OOP",
                "supports_tests": True
            },
            "php": {
                "name": "PHP",
                "description": "Web backend development",
                "default_style": "procedural or OOP",
                "supports_tests": True
            }
        },
        "total": 10
    }


@router.get("/examples", response_model=dict)
async def get_examples():
    """
    Get example requests for different use cases.
    
    Returns:
        Dictionary of example requests
    
    Example:
        ```python
        GET /api/v1/examples
        ```
    """
    return {
        "examples": {
            "simple_function": {
                "prompt": "Create a function to calculate factorial of a number",
                "language": "python",
                "complexity": "simple",
                "include_tests": True
            },
            "data_structure": {
                "prompt": "Implement a binary search tree with insert and search methods",
                "language": "python",
                "complexity": "medium",
                "style": "oop",
                "include_tests": True
            },
            "api_endpoint": {
                "prompt": "Create a REST API endpoint for user authentication with JWT",
                "language": "python",
                "complexity": "advanced",
                "framework": "FastAPI",
                "include_docs": True
            },
            "algorithm": {
                "prompt": "Implement merge sort algorithm",
                "language": "javascript",
                "complexity": "medium",
                "style": "functional",
                "include_tests": True
            },
            "web_component": {
                "prompt": "Create a React component for a todo list with add/delete functionality",
                "language": "typescript",
                "complexity": "medium",
                "framework": "React",
                "include_docs": True
            }
        }
    }


# Error handlers
@router.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """
    Custom HTTP exception handler.
    
    Args:
        request: FastAPI request
        exc: HTTP exception
    
    Returns:
        JSON error response
    """
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail
    )


@router.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """
    General exception handler for unexpected errors.
    
    Args:
        request: FastAPI request
        exc: Exception
    
    Returns:
        JSON error response
    """
    logger.error(f"Unexpected error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "InternalServerError",
            "message": "An unexpected error occurred",
            "suggestions": ["Please try again later or contact support"]
        }
    )

