# Model Deployment

**Difficulty:** Advanced  
**Time to Solve:** 35-40 min  
**Category:** MLOps

---

## Problem Description

Build a production-ready model deployment system using FastAPI that serves machine learning models via REST API. The system should:

- **Model Serving**: Load and serve trained models via API endpoints
- **Prediction Endpoints**: Single and batch prediction endpoints
- **Model Management**: Support multiple model versions, model switching
- **Input Validation**: Validate input data using Pydantic models
- **Error Handling**: Comprehensive error handling and logging
- **Health Checks**: Health check and model info endpoints
- **Performance**: Async support for better throughput

This demonstrates essential MLOps skills for deploying ML models in production.

---

## Input Specification

- **Type:** HTTP POST requests with JSON payload
- **Format:** 
  - Single prediction: `{"features": [1.0, 2.0, 3.0]}`
  - Batch prediction: `{"features": [[1.0, 2.0], [3.0, 4.0]]}`
- **Constraints:**
  - Features must match model input shape
  - JSON format required
  - Maximum batch size: 1000 samples

---

## Output Specification

- **Type:** JSON response
- **Format:** 
  - Single: `{"prediction": 1, "confidence": 0.95}`
  - Batch: `{"predictions": [1, 0], "confidences": [0.95, 0.87]}`
- **Requirements:**
  - Response time < 100ms for single prediction
  - Proper HTTP status codes
  - Error messages in response

---

## Examples

### Example 1: Single Prediction
**Request:**
```bash
POST /api/v1/predict
{
  "features": [5.1, 3.5, 1.4, 0.2]
}
```

**Response:**
```json
{
  "prediction": 0,
  "confidence": 0.9876,
  "model_version": "v1"
}
```

---

### Example 2: Batch Prediction
**Request:**
```bash
POST /api/v1/predict/batch
{
  "features": [
    [5.1, 3.5, 1.4, 0.2],
    [6.2, 3.4, 5.4, 2.3]
  ]
}
```

**Response:**
```json
{
  "predictions": [0, 2],
  "confidences": [0.9876, 0.9234],
  "model_version": "v1",
  "batch_size": 2
}
```

---

## Edge Cases to Consider

1. **Invalid feature count:**
   - Expected behavior: Return 400 Bad Request with error message

2. **Model not loaded:**
   - Expected behavior: Return 503 Service Unavailable

3. **Large batch size:**
   - Expected behavior: Return 400 if exceeds limit

---

## Constraints

- Must use FastAPI framework
- Must support async operations
- Must validate all inputs
- Must handle errors gracefully
- Must log all requests
- Must provide health check endpoint

---

## Solution Approach

1. **FastAPI App**: Initialize FastAPI application
2. **Model Loader**: Load models from disk
3. **Endpoints**: Create prediction endpoints
4. **Validation**: Validate inputs with Pydantic
5. **Error Handling**: Comprehensive error handling
6. **Logging**: Request/response logging

---

## Complexity Requirements

- **Target Time Complexity:** O(n*m) for predictions
- **Target Space Complexity:** O(n) for batch predictions

---

## Success Criteria

Your solution should:
- [ ] Serve models via REST API
- [ ] Support single and batch predictions
- [ ] Validate all inputs
- [ ] Handle errors gracefully
- [ ] Include health checks
- [ ] Support async operations
- [ ] Include comprehensive logging
- [ ] Have proper type hints and docstrings

