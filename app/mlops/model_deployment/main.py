"""
FastAPI application entry point for model deployment.
"""
from model_deployment import ModelDeployment
import os

if __name__ == "__main__":
    # Get model path from environment or use default
    model_path = os.getenv("MODEL_PATH", "models/model.pkl")
    task_type = os.getenv("TASK_TYPE", "classification")
    
    deployment = ModelDeployment(model_path=model_path, task_type=task_type)
    
    # Try to load model if it exists
    if os.path.exists(model_path):
        try:
            deployment.load_model()
        except Exception as e:
            print(f"Warning: Could not load model: {e}")
            print("Server will start but predictions will fail until model is loaded")
    
    # Run server
    deployment.run(host="0.0.0.0", port=8000)

