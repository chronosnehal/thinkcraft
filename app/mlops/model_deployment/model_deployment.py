#!/usr/bin/env python3
"""
Model Deployment - MLOps Solution Implementation

Description: Production-ready model deployment system using FastAPI
for serving machine learning models via REST API.

Time Complexity: O(n*m) for predictions
Space Complexity: O(n) for batch predictions

Dependencies: fastapi, uvicorn, pydantic, joblib, numpy
Author: ThinkCraft
"""

from typing import Any, Dict, List, Optional, Union
import logging
import os
from pathlib import Path
import numpy as np
import joblib
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
import uvicorn

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Pydantic models for request/response validation
class PredictionRequest(BaseModel):
    """Request model for single prediction."""
    features: List[float] = Field(..., description="Feature vector")
    
    @validator('features')
    def validate_features(cls, v):
        if len(v) == 0:
            raise ValueError("Features cannot be empty")
        if len(v) > 1000:
            raise ValueError("Feature vector too long (max 1000)")
        return v


class BatchPredictionRequest(BaseModel):
    """Request model for batch prediction."""
    features: List[List[float]] = Field(..., description="Batch of feature vectors")
    
    @validator('features')
    def validate_features(cls, v):
        if len(v) == 0:
            raise ValueError("Features cannot be empty")
        if len(v) > 1000:
            raise ValueError("Batch size too large (max 1000)")
        for i, feat in enumerate(v):
            if len(feat) == 0:
                raise ValueError(f"Feature vector {i} is empty")
        return v


class PredictionResponse(BaseModel):
    """Response model for single prediction."""
    prediction: Union[int, float] = Field(..., description="Prediction")
    confidence: Optional[float] = Field(None, description="Prediction confidence")
    model_version: str = Field(..., description="Model version")


class BatchPredictionResponse(BaseModel):
    """Response model for batch prediction."""
    predictions: List[Union[int, float]] = Field(..., description="Predictions")
    confidences: Optional[List[float]] = Field(None, description="Confidences")
    model_version: str = Field(..., description="Model version")
    batch_size: int = Field(..., description="Number of predictions")


class ModelDeployment:
    """
    Model deployment system using FastAPI.
    
    This class manages model loading, serving, and prediction handling
    for production ML model deployment.
    
    Attributes:
        app: FastAPI application instance
        model: Loaded ML model
        model_version: Current model version
        model_path: Path to model file
        task_type: Task type ("classification" or "regression")
    """
    
    def __init__(
        self,
        model_path: Optional[str] = None,
        task_type: str = "classification"
    ):
        """
        Initialize model deployment system.
        
        Args:
            model_path: Path to saved model file
            task_type: Task type ("classification" or "regression")
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        self.app = FastAPI(
            title="ML Model Deployment API",
            description="Production-ready ML model serving API",
            version="1.0.0"
        )
        self.model = None
        self.model_version = "unknown"
        self.model_path = model_path
        self.task_type = task_type
        
        # Setup routes
        self._setup_routes()
        
        logger.info("Model deployment system initialized")
    
    def _setup_routes(self) -> None:
        """Setup API routes."""
        
        @self.app.get("/")
        async def root():
            """Root endpoint."""
            return {
                "status": "active",
                "service": "ML Model Deployment API",
                "model_loaded": self.model is not None
            }
        
        @self.app.get("/health")
        async def health_check():
            """Health check endpoint."""
            if self.model is None:
                return JSONResponse(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    content={"status": "unhealthy", "reason": "Model not loaded"}
                )
            return {"status": "healthy", "model_version": self.model_version}
        
        @self.app.get("/model/info")
        async def model_info():
            """Get model information."""
            if self.model is None:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Model not loaded"
                )
            
            model_data = self.model if isinstance(self.model, dict) else {}
            config = model_data.get('config', {})
            
            return {
                "model_version": self.model_version,
                "task_type": self.task_type,
                "model_type": config.get('model_type', 'unknown'),
                "feature_count": len(model_data.get('feature_names', []))
            }
        
        @self.app.post("/api/v1/predict", response_model=PredictionResponse)
        async def predict(request: PredictionRequest):
            """Single prediction endpoint."""
            if self.model is None:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Model not loaded"
                )
            
            try:
                # Convert to numpy array
                features = np.array(request.features).reshape(1, -1)
                
                # Validate feature count
                model_data = self.model if isinstance(self.model, dict) else {}
                expected_features = len(model_data.get('feature_names', []))
                if features.shape[1] != expected_features:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=(
                            f"Expected {expected_features} features, "
                            f"got {features.shape[1]}"
                        )
                    )
                
                # Get model
                model = model_data.get('model', self.model)
                
                # Make prediction
                prediction = model.predict(features)[0]
                
                # Get confidence/probability if available
                confidence = None
                if self.task_type == "classification" and hasattr(model, "predict_proba"):
                    try:
                        proba = model.predict_proba(features)[0]
                        confidence = float(np.max(proba))
                    except:
                        pass
                
                return PredictionResponse(
                    prediction=float(prediction) if isinstance(prediction, np.number) else prediction,
                    confidence=confidence,
                    model_version=self.model_version
                )
            
            except HTTPException:
                raise
            except Exception as e:
                logger.error(f"Prediction error: {e}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Prediction failed: {str(e)}"
                )
        
        @self.app.post("/api/v1/predict/batch", response_model=BatchPredictionResponse)
        async def predict_batch(request: BatchPredictionRequest):
            """Batch prediction endpoint."""
            if self.model is None:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Model not loaded"
                )
            
            try:
                # Convert to numpy array
                features = np.array(request.features)
                
                # Validate feature count
                model_data = self.model if isinstance(self.model, dict) else {}
                expected_features = len(model_data.get('feature_names', []))
                if features.shape[1] != expected_features:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=(
                            f"Expected {expected_features} features per sample, "
                            f"got {features.shape[1]}"
                        )
                    )
                
                # Get model
                model = model_data.get('model', self.model)
                
                # Make predictions
                predictions = model.predict(features)
                
                # Get confidences if available
                confidences = None
                if self.task_type == "classification" and hasattr(model, "predict_proba"):
                    try:
                        proba = model.predict_proba(features)
                        confidences = [float(np.max(p)) for p in proba]
                    except:
                        pass
                
                # Convert predictions to list
                pred_list = [
                    float(p) if isinstance(p, np.number) else p
                    for p in predictions
                ]
                
                return BatchPredictionResponse(
                    predictions=pred_list,
                    confidences=confidences,
                    model_version=self.model_version,
                    batch_size=len(pred_list)
                )
            
            except HTTPException:
                raise
            except Exception as e:
                logger.error(f"Batch prediction error: {e}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Batch prediction failed: {str(e)}"
                )
    
    def load_model(self, model_path: Optional[str] = None) -> None:
        """
        Load model from disk.
        
        Args:
            model_path: Path to model file (uses self.model_path if None)
        
        Time Complexity: O(m) where m is model size
        Space Complexity: O(m)
        """
        path = model_path or self.model_path
        if path is None:
            raise ValueError("Model path not provided")
        
        if not os.path.exists(path):
            raise FileNotFoundError(f"Model file not found: {path}")
        
        logger.info(f"Loading model from {path}")
        
        try:
            self.model = joblib.load(path)
            
            # Extract metadata if model is a dictionary
            if isinstance(self.model, dict):
                self.model_version = self.model.get('version', 'unknown')
                config = self.model.get('config', {})
                self.task_type = config.get('task_type', 'classification')
            else:
                self.model_version = Path(path).stem
            
            logger.info(f"Model loaded successfully (version: {self.model_version})")
        
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise
    
    def run(self, host: str = "0.0.0.0", port: int = 8000) -> None:
        """
        Run the FastAPI server.
        
        Args:
            host: Host to bind to
            port: Port to bind to
        """
        logger.info(f"Starting server on {host}:{port}")
        uvicorn.run(self.app, host=host, port=port)


def main():
    """Main function to demonstrate model deployment."""
    print("=" * 70)
    print("Model Deployment - MLOps Solution")
    print("=" * 70)
    
    print("\nTo use this deployment system:")
    print("1. Train and save a model using model_training_pipeline.py")
    print("2. Initialize ModelDeployment with model path")
    print("3. Load the model")
    print("4. Run the server")
    print("\nExample:")
    print("""
    from model_deployment import ModelDeployment
    
    deployment = ModelDeployment(
        model_path="models/random_forest_classifier_v1.pkl",
        task_type="classification"
    )
    deployment.load_model()
    deployment.run(host="0.0.0.0", port=8000)
    """)
    
    print("\nAPI Endpoints:")
    print("  GET  /              - Root endpoint")
    print("  GET  /health        - Health check")
    print("  GET  /model/info    - Model information")
    print("  POST /api/v1/predict      - Single prediction")
    print("  POST /api/v1/predict/batch - Batch prediction")
    
    print("\nExample request:")
    print("""
    curl -X POST "http://localhost:8000/api/v1/predict" \\
         -H "Content-Type: application/json" \\
         -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
    """)
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()

