# Model Training Pipeline

Complete end-to-end machine learning training pipeline with data loading, preprocessing, model training, evaluation, and persistence.

## Overview

This solution demonstrates production-ready MLOps practices for training machine learning models. It supports both classification and regression tasks with multiple model types.

## Features

- **Data Loading & Validation**: Load CSV files or DataFrames with comprehensive validation
- **Data Preprocessing**: Handle missing values, encode categorical variables
- **Model Training**: Support for Random Forest, Logistic Regression, and Gradient Boosting
- **Model Evaluation**: Task-specific metrics (classification: accuracy, precision, recall, F1; regression: MSE, MAE, R²)
- **Model Persistence**: Save and load models with versioning
- **Reproducibility**: Random seed control for all operations
- **Comprehensive Logging**: Track all pipeline steps

## Quick Start

```python
from model_training_pipeline import ModelTrainingPipeline, ModelConfig

# Configure model
config = ModelConfig(
    model_type="random_forest",
    task_type="classification",
    hyperparameters={"n_estimators": 100, "max_depth": 10},
    random_state=42
)

# Initialize pipeline
pipeline = ModelTrainingPipeline(config)

# Load data
X, y = pipeline.load_data("datasets/mlops/classification/train.csv")

# Split data
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Preprocess
X_train_proc, y_train_proc = pipeline.preprocess_data(X_train, y_train, fit=True)
X_test_proc, y_test_proc = pipeline.preprocess_data(X_test, y_test, fit=False)

# Train
pipeline.train_model(X_train_proc, y_train_proc)

# Evaluate
metrics = pipeline.evaluate_model(X_test_proc, y_test_proc)

# Save model
model_path = pipeline.save_model("models/")
```

## Supported Models

### Classification
- Random Forest Classifier
- Logistic Regression
- Gradient Boosting Classifier

### Regression
- Random Forest Regressor
- Gradient Boosting Regressor

## Data Format

CSV file with:
- Features: numeric or categorical columns
- Target: column named `target` (classification) or `price` (regression)
- Minimum 100 samples required

## Output

- Trained model saved as `.pkl` file
- Evaluation metrics dictionary
- Model metadata (version, config, feature names)

## Requirements

All dependencies are managed via the root `requirements.in` file. Install from root:
```bash
pip install -r requirements.txt
```

## Example Usage

Run the solution:

```bash
python model_training_pipeline.py
```

This will demonstrate:
1. Classification pipeline with synthetic data
2. Regression pipeline with synthetic data

## Complexity Analysis

- **Time Complexity**: O(n*m*k) where n=samples, m=features, k=iterations (model-dependent)
- **Space Complexity**: O(n*m) for data + O(m) for model parameters