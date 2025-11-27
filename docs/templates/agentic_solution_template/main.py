#!/usr/bin/env python3
"""
[Use Case Name] - Agentic System Main Application

Description: [Brief description of the agentic use case]

This FastAPI application implements an agentic system that performs
[describe multi-step reasoning/planning/acting capabilities].

Author: chronosnehal
Date: [YYYY-MM-DD]
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router import router
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="[Use Case Name] Agent",
    description="Agentic system for [purpose description]",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router, prefix="/api/v1", tags=["agent"])


@app.get("/")
def root():
    """
    Root endpoint - Health check.
    
    Returns:
        Status information about the service
    """
    return {
        "status": "active",
        "service": "[Use Case Name] Agent",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "execute": "/api/v1/execute",
            "status": "/api/v1/status"
        }
    }


@app.get("/health")
def health_check():
    """
    Health check endpoint.
    
    Returns:
        Health status of the service
    """
    return {
        "status": "healthy",
        "service": "[Use Case Name] Agent"
    }


@app.on_event("startup")
async def startup_event():
    """Execute on application startup."""
    logger.info("[Use Case Name] Agent starting up...")
    logger.info("API documentation available at /docs")


@app.on_event("shutdown")
async def shutdown_event():
    """Execute on application shutdown."""
    logger.info("[Use Case Name] Agent shutting down...")


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

