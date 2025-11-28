#!/usr/bin/env python3
"""
Code Generator - FastAPI Application

Main FastAPI application for the AI-powered code generation system.

Author: chronosnehal
Date: 2025-11-27
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
import logging

from api.routes import router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="AI Code Generator",
    description="""
    # AI-Powered Code Generation System
    
    Generate high-quality code from natural language descriptions using advanced LLMs.
    
    ## Features
    
    - **Multi-Language Support**: Python, JavaScript, TypeScript, Java, Go, Rust, C++, C#, Ruby, PHP
    - **Complexity Levels**: Simple, Medium, Advanced
    - **Framework Integration**: FastAPI, React, Spring Boot, and more
    - **Test Generation**: Automatic unit test generation
    - **Documentation**: Comprehensive docstrings and comments
    - **Complexity Analysis**: Big O time and space complexity
    - **Code Refinement**: Improve existing code with AI suggestions
    
    ## Quick Start
    
    1. **Generate Code**: POST to `/api/v1/generate` with your prompt
    2. **Refine Code**: POST to `/api/v1/refine` to improve existing code
    3. **Check Health**: GET `/api/v1/health` for service status
    
    ## Example Request
    
    ```json
    {
        "prompt": "Create a function to sort an array using quicksort",
        "language": "python",
        "complexity": "medium",
        "include_tests": true,
        "include_docs": true
    }
    ```
    
    ## Supported Languages
    
    - Python (functional, OOP)
    - JavaScript/TypeScript (functional, React, Node.js)
    - Java (OOP, Spring Boot)
    - Go (procedural, concurrent)
    - Rust (functional, systems)
    - C++ (OOP, systems)
    - C# (.NET, Unity)
    - Ruby (Rails, OOP)
    - PHP (Laravel, WordPress)
    
    ## Rate Limits
    
    - 100 requests per minute per IP
    - 1000 requests per hour per API key
    
    ## Support
    
    For issues or questions, contact: chronosnehal
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include router with prefix
app.include_router(router, prefix="/api/v1", tags=["code-generation"])


@app.get("/", include_in_schema=False)
async def root_redirect():
    """
    Redirect root to API documentation.
    
    Returns:
        Redirect response to /docs
    """
    return RedirectResponse(url="/docs")


@app.on_event("startup")
async def startup_event():
    """
    Startup event handler.
    
    Initializes services and logs startup information.
    """
    logger.info("=" * 80)
    logger.info("AI Code Generator Service Starting...")
    logger.info("=" * 80)
    logger.info("Version: 1.0.0")
    logger.info("Documentation: http://localhost:8000/docs")
    logger.info("Health Check: http://localhost:8000/api/v1/health")
    logger.info("=" * 80)


@app.on_event("shutdown")
async def shutdown_event():
    """
    Shutdown event handler.
    
    Performs cleanup operations before shutdown.
    """
    logger.info("=" * 80)
    logger.info("AI Code Generator Service Shutting Down...")
    logger.info("=" * 80)


# Health check at root level
@app.get("/health", tags=["health"])
async def root_health():
    """
    Root-level health check endpoint.
    
    Returns:
        Service status
    """
    return {
        "status": "healthy",
        "service": "AI Code Generator",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    
    # Run the application
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

