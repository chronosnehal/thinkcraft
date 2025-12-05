# Feature Engineering

Comprehensive feature engineering pipeline with automatic feature creation, transformation, and selection.

## Overview

This solution demonstrates production-ready feature engineering patterns for preparing data for machine learning models. It supports numeric transformations, categorical encoding, temporal feature extraction, and feature selection.

## Features

- **Numeric Transformations**: Scaling (standard, minmax, robust), normalization
- **Categorical Encoding**: One-hot, label, and target encoding
- **Temporal Features**: Date/time extraction, cyclical encoding
- **Polynomial Features**: Automatic polynomial feature creation
- **Interaction Features**: Feature combinations and interactions
- **Feature Selection**: Statistical methods for feature importance
- **Missing Value Handling**: Automatic imputation
- **Fit/Transform Pattern**: Prevents data leakage

## Quick Start

```python
from feature_engineering import FeatureEngineeringPipeline

# Initialize pipeline
pipeline = FeatureEngineeringPipeline(
    scale_numeric=True,
    encode_categorical="onehot",
    create_polynomial=True,
    create_interactions=True,
    select_features=True,
    task_type="classification"
)

# Fit and transform
X_transformed = pipeline.fit_transform(X_train, y_train)

# Transform test data
X_test_transformed = pipeline.transform(X_test)
```

## Supported Transformations

### Numeric Features
- Standard scaling
- Min-max scaling
- Robust scaling
- Polynomial features
- Interaction features

### Categorical Features
- One-hot encoding
- Label encoding
- Target encoding (requires target)

### Temporal Features
- Year, month, day, weekday extraction
- Cyclical encoding (sin/cos)
- Hour extraction (if available)

## Requirements

All dependencies are managed via the root `requirements.in` file. Install from root:
```bash
pip install -r requirements.txt
```

## Example Usage

Run the solution:

```bash
python feature_engineering.py
```

This demonstrates:
1. Feature engineering with mixed data types
2. Feature selection with importance scores

## Complexity Analysis

- **Time Complexity**: O(n*m) for basic transformations, O(n*m²) for interactions
- **Space Complexity**: O(n*m) for transformed data