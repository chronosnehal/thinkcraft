# Model Evaluation

Comprehensive model evaluation system with metrics computation, cross-validation, and visualization.

## Overview

This solution provides extensive model evaluation capabilities for both classification and regression tasks, including standard metrics, cross-validation, and visualization.

## Features

### Classification Metrics
- Accuracy, Precision, Recall, F1-score
- ROC-AUC score
- Confusion matrix
- Classification report

### Regression Metrics
- MSE, MAE, RMSE
- R² score
- MAPE (Mean Absolute Percentage Error)

### Additional Features
- K-fold cross-validation
- Stratified cross-validation for classification
- Visualization plots (ROC curves, confusion matrices, residual plots)
- Model comparison capabilities

## Quick Start

```python
from model_evaluation import ModelEvaluator

# Initialize evaluator
evaluator = ModelEvaluator(task_type="classification", n_folds=5)

# Evaluate model
metrics = evaluator.evaluate(model, X_test, y_test, save_plots=True)

# Cross-validation
cv_scores = evaluator.cross_validate(model, X_train, y_train)
```

## Requirements

All dependencies are managed via the root `requirements.in` file. Install from root:
```bash
pip install -r requirements.txt
```

## Example Usage

Run the solution:

```bash
python model_evaluation.py
```

This demonstrates:
1. Classification model evaluation with metrics and CV
2. Regression model evaluation with metrics and CV

## Complexity Analysis

- **Time Complexity**: O(n*m) for evaluation, O(k*n*m) for k-fold CV
- **Space Complexity**: O(n) for predictions and metrics
