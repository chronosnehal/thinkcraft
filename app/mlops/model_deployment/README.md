# Model Deployment

Production-ready model deployment system using FastAPI for serving machine learning models via REST API.

## Overview

This solution provides a complete FastAPI-based deployment system for ML models with comprehensive input validation, error handling, and async support.

## Features

- **REST API**: FastAPI-based model serving
- **Single & Batch Predictions**: Support for both single and batch predictions
- **Input Validation**: Pydantic models for request validation
- **Error Handling**: Comprehensive error handling with proper HTTP status codes
- **Health Checks**: Health check and model info endpoints
- **Async Support**: Async operations for better throughput
- **Model Management**: Support for model versioning

## Quick Start

```python
from model_deployment import ModelDeployment

# Initialize deployment
deployment = ModelDeployment(
    model_path="models/model.pkl",
    task_type="classification"
)

# Load model
deployment.load_model()

# Run server
deployment.run(host="0.0.0.0", port=8000)
```

## API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /model/info` - Model information
- `POST /api/v1/predict` - Single prediction
- `POST /api/v1/predict/batch` - Batch prediction

## Example Requests

### Single Prediction
```bash
curl -X POST "http://localhost:8000/api/v1/predict" \\
     -H "Content-Type: application/json" \\
     -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
```

### Batch Prediction
```bash
curl -X POST "http://localhost:8000/api/v1/predict/batch" \\
     -H "Content-Type: application/json" \\
     -d '{"features": [[5.1, 3.5, 1.4, 0.2], [6.2, 3.4, 5.4, 2.3]]}'
```

## Requirements

All dependencies are managed via the root `requirements.in` file. Install from root:
```bash
pip install -r requirements.txt
```

## Running the Server

```bash
python model_deployment.py
# Or use uvicorn directly:
uvicorn model_deployment:app --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Complexity Analysis

- **Time Complexity**: O(n*m) for predictions
- **Space Complexity**: O(n) for batch predictions