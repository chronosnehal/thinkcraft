# Datasets Directory

**Author:** chronosnehal

This directory contains sample datasets for MLOps and GenAI problems.

---

## Purpose

Datasets are used for:
- **MLOps problems** - Training, validation, and testing data
- **GenAI problems** - Sample text data for processing
- **Example demonstrations** - Realistic data for solutions

---

## Structure

```
datasets/
├── README.md           # This file
├── sample/             # Small sample datasets for quick testing
├── mlops/              # Datasets for MLOps problems
│   ├── classification/
│   ├── regression/
│   └── clustering/
├── genai/              # Datasets for GenAI problems
│   ├── text/
│   └── documents/
└── .gitkeep
```

---

## Dataset Guidelines

### 1. Size Limits
- **Sample datasets:** < 1 MB
- **Training datasets:** < 10 MB
- **Large datasets:** Use external links (not committed)

### 2. Format
- **Preferred:** CSV, JSON, TXT
- **Avoid:** Binary formats, large images, videos

### 3. Naming Convention
```
<problem_name>_<split>.csv
Example: iris_train.csv, iris_test.csv
```

### 4. Documentation
Each dataset should have:
- Description in problem's README
- Column/field descriptions
- Source attribution
- License information

---

## Using Datasets

### In MLOps Problems

```python
import pandas as pd

# Load dataset
data_path = "datasets/mlops/classification/iris_train.csv"
df = pd.read_csv(data_path)

# Use in training
X = df.drop('target', axis=1)
y = df['target']
```

### In GenAI Problems

```python
# Load text dataset
data_path = "datasets/genai/text/sample_reviews.txt"
with open(data_path, 'r') as f:
    texts = f.readlines()

# Process with LLM
for text in texts:
    response = manager.generate(provider="openai", prompt=f"Analyze: {text}")
```

---

## Adding New Datasets

### Step 1: Choose Location
- MLOps classification → `datasets/mlops/classification/`
- MLOps regression → `datasets/mlops/regression/`
- GenAI text → `datasets/genai/text/`

### Step 2: Prepare Dataset
- Clean and validate data
- Remove sensitive information
- Keep size under 10 MB
- Add appropriate headers

### Step 3: Document
Add to problem's README:
```markdown
## Dataset

**Location:** `datasets/mlops/classification/my_data.csv`
**Size:** 5 MB
**Rows:** 10,000
**Features:** 20
**Target:** Binary classification
**Source:** [Source URL or "Synthetic"]
**License:** [License type]
```

### Step 4: Reference in Code
```python
# Always use relative path from repository root
data_path = "datasets/mlops/classification/my_data.csv"
```

---

## Sample Datasets

### 1. Iris Dataset (Classification)
**Location:** `datasets/sample/iris.csv`
**Description:** Classic iris flower classification
**Size:** 5 KB
**Use:** Quick testing of classification algorithms

### 2. Boston Housing (Regression)
**Location:** `datasets/sample/boston_housing.csv`
**Description:** Housing price prediction
**Size:** 50 KB
**Use:** Regression algorithm testing

### 3. Sample Reviews (Text)
**Location:** `datasets/sample/reviews.txt`
**Description:** Product reviews for sentiment analysis
**Size:** 10 KB
**Use:** GenAI text processing examples

---

## External Datasets

For large datasets, use external links:

```python
# In your code, provide download instructions
"""
Dataset: Large Image Dataset
Size: 500 MB
Download: https://example.com/dataset.zip
Extract to: datasets/mlops/images/

Note: This dataset is not included in the repository due to size.
"""
```

---

## Best Practices

### 1. Use Synthetic Data When Possible
```python
from sklearn.datasets import make_classification

# Generate synthetic data
X, y = make_classification(n_samples=1000, n_features=20)
```

### 2. Provide Data Generation Scripts
```python
# datasets/mlops/classification/generate_data.py
def generate_sample_data():
    """Generate sample classification dataset."""
    # Data generation logic
    pass
```

### 3. Document Data Preprocessing
```python
def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess dataset.
    
    Steps:
    1. Handle missing values
    2. Encode categorical variables
    3. Scale numerical features
    """
    pass
```

### 4. Include Data Validation
```python
def validate_dataset(df: pd.DataFrame) -> bool:
    """
    Validate dataset format and content.
    
    Checks:
    - Required columns present
    - No missing values in target
    - Correct data types
    """
    pass
```

---

## .gitignore Considerations

Large or sensitive datasets should be in `.gitignore`:

```gitignore
# Large datasets
datasets/**/*.zip
datasets/**/*.tar.gz
datasets/**/large_*.csv

# Sensitive data
datasets/**/private_*
datasets/**/confidential_*
```

---

## License and Attribution

### Public Datasets
Always include attribution:
```markdown
## Dataset License

**Name:** Iris Dataset
**Source:** UCI Machine Learning Repository
**License:** CC BY 4.0
**Citation:** Fisher, R.A. (1936). "The use of multiple measurements in taxonomic problems"
```

### Synthetic Datasets
```markdown
## Dataset License

**Type:** Synthetic
**Generated:** Using sklearn.datasets.make_classification
**License:** No restrictions (generated data)
```

---

## Quick Reference

```python
# Load CSV dataset
import pandas as pd
df = pd.read_csv("datasets/mlops/classification/data.csv")

# Load text dataset
with open("datasets/genai/text/data.txt", 'r') as f:
    texts = f.readlines()

# Load JSON dataset
import json
with open("datasets/genai/documents/data.json", 'r') as f:
    data = json.load(f)
```

---

**Keep datasets small, documented, and properly licensed!**

