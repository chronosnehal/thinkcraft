# Model Evaluation

**Difficulty:** Medium  
**Time to Solve:** 25-30 min  
**Category:** MLOps

---

## Problem Description

Build a comprehensive model evaluation system that computes and visualizes various performance metrics for both classification and regression models. The system should support:

- **Classification Metrics**: Accuracy, precision, recall, F1-score, ROC-AUC, confusion matrix
- **Regression Metrics**: MSE, MAE, RMSE, R², MAPE
- **Cross-Validation**: K-fold cross-validation with stratified sampling
- **Visualization**: ROC curves, precision-recall curves, residual plots, confusion matrix heatmaps
- **Model Comparison**: Compare multiple models side-by-side

This demonstrates essential MLOps skills for model assessment and validation.

---

## Input Specification

- **Type:** Trained model, test features (numpy array), test targets (numpy array)
- **Format:** 
  - Model: scikit-learn compatible model object
  - X_test: Feature array of shape (n_samples, n_features)
  - y_test: Target array of shape (n_samples,)
- **Constraints:**
  - Model must be fitted
  - X_test and y_test must have same number of samples
  - For classification: y_test must contain class labels

---

## Output Specification

- **Type:** Dictionary of metrics and optional visualization files
- **Format:** 
  - Metrics dictionary with all computed metrics
  - Optional: Saved plots (ROC curve, confusion matrix, etc.)
- **Requirements:**
  - All relevant metrics for task type
  - Metrics formatted to 4 decimal places
  - Visualizations saved if requested

---

## Examples

### Example 1: Classification Evaluation
**Input:**
```python
model = RandomForestClassifier()
model.fit(X_train, y_train)
evaluator = ModelEvaluator(task_type="classification")
metrics = evaluator.evaluate(model, X_test, y_test)
```

**Output:**
```python
{
    'accuracy': 0.9500,
    'precision': 0.9487,
    'recall': 0.9500,
    'f1_score': 0.9493,
    'roc_auc': 0.9875,
    'confusion_matrix': [[45, 2], [3, 50]]
}
```

---

### Example 2: Regression Evaluation
**Input:**
```python
model = GradientBoostingRegressor()
model.fit(X_train, y_train)
evaluator = ModelEvaluator(task_type="regression")
metrics = evaluator.evaluate(model, X_test, y_test)
```

**Output:**
```python
{
    'mse': 0.0234,
    'mae': 0.1234,
    'rmse': 0.1529,
    'r2_score': 0.8765,
    'mape': 0.0456
}
```

---

## Edge Cases to Consider

1. **Single class in predictions:**
   - Expected behavior: Handle gracefully, return appropriate metrics

2. **Perfect predictions:**
   - Expected behavior: All metrics should reflect perfect performance

3. **All predictions same:**
   - Expected behavior: Metrics should reflect poor performance

---

## Constraints

- Must support both classification and regression
- Must compute all standard metrics for each task type
- Must support cross-validation
- Must generate visualizations
- Must handle edge cases gracefully

---

## Solution Approach

1. **Predict**: Generate predictions from model
2. **Compute Metrics**: Calculate task-specific metrics
3. **Cross-Validate**: Perform k-fold cross-validation
4. **Visualize**: Create and save plots
5. **Compare**: Compare multiple models if provided

---

## Complexity Requirements

- **Target Time Complexity:** O(n*m) for evaluation, O(k*n*m) for k-fold CV
- **Target Space Complexity:** O(n) for predictions and metrics

---

## Success Criteria

Your solution should:
- [ ] Compute all relevant metrics for classification
- [ ] Compute all relevant metrics for regression
- [ ] Support cross-validation
- [ ] Generate visualizations
- [ ] Handle edge cases
- [ ] Include comprehensive logging
- [ ] Have proper type hints and docstrings

