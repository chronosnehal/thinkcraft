# Datasets Directory

**Author:** chronosnehal

This directory contains sample datasets for MLOps and GenAI problems.

---

## Purpose

Datasets are used for:
- **MLOps problems** - Training, validation, and testing data
- **GenAI problems** - Sample text data for processing
- **Data Analysis** - Business intelligence and pattern detection
- **Example demonstrations** - Realistic data for solutions
- **Quick testing** - Small sample datasets for rapid prototyping

**Directory Structure:**
- `datasets/sample/` - Small, ready-to-use datasets (< 100 KB each)
- `datasets/mlops/` - ML training datasets organized by task type
- `datasets/genai/` - Text and document datasets for LLM processing

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

**Using Sample Datasets:**
```python
import pandas as pd

# Load sample dataset
data_path = "datasets/sample/iris.csv"
df = pd.read_csv(data_path)

# Use in training
X = df.drop('species', axis=1)
y = df['species']
```

**Using MLOps-Specific Datasets:**
```python
import pandas as pd

# Load dataset from mlops directory
data_path = "datasets/mlops/classification/iris_train.csv"
df = pd.read_csv(data_path)

# Use in training
X = df.drop('target', axis=1)
y = df['target']
```

### In GenAI Problems

**Using Sample Text Datasets:**
```python
# Load sample text dataset
data_path = "datasets/sample/reviews.txt"
with open(data_path, 'r') as f:
    texts = f.readlines()

# Process with LLM
from app.utils.llm_client_manager import LLMClientManager
manager = LLMClientManager()
for text in texts[:5]:  # Process first 5
    response = manager.generate(
        provider="openai",
        prompt=f"Analyze sentiment: {text}"
    )
    print(response)
```

**Using GenAI-Specific Datasets:**
```python
# Load text dataset from genai directory
data_path = "datasets/genai/text/sample_reviews.txt"
with open(data_path, 'r') as f:
    texts = f.readlines()

# Process with LLM
for text in texts:
    response = manager.generate(provider="openai", prompt=f"Analyze: {text}")
```

### In Data Analysis Problems

**Using Sample CSV Datasets:**
```python
from app.genai.data_analyzer.data_analyzer import DataAnalyzer
import pandas as pd

# Load sample dataset
df = pd.read_csv("datasets/sample/sales_data.csv")

# Analyze with DataAnalyzer
analyzer = DataAnalyzer(provider="openai")
result = analyzer.analyze(
    data=df.to_dict('records'),
    analysis_type="summary",
    include_recommendations=True
)

print(result["summary"])
```

**Using Dictionary/List Data:**
```python
# Use dictionary data directly
sales_data = {
    "month": ["Jan", "Feb", "Mar"],
    "sales": [10000, 12000, 15000]
}

analyzer = DataAnalyzer()
result = analyzer.analyze(
    data=sales_data,
    analysis_type="trends"
)
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

> **Note:** The sample datasets listed below are recommended datasets that should be available in `datasets/sample/` for quick testing. If a dataset is missing, you can create it using the examples provided or use synthetic data generation scripts.

The `datasets/sample/` directory contains small, ready-to-use datasets for quick testing and demonstrations. These datasets are designed to be:
- **Small**: < 100 KB each
- **Self-contained**: No external dependencies
- **Well-documented**: Clear structure and purpose
- **Versatile**: Usable across multiple problem types

**Quick Access:**
- All sample datasets are in `datasets/sample/`
- Use relative paths: `datasets/sample/iris.csv`
- Perfect for quick testing and examples

### Available Sample Datasets

#### 1. Iris Dataset (Classification)
**Location:** `datasets/sample/iris.csv`  
**Description:** Classic iris flower classification dataset  
**Size:** ~5 KB  
**Rows:** 150  
**Columns:** 5 (sepal_length, sepal_width, petal_length, petal_width, species)  
**Use Cases:**
- MLOps classification problems
- Data analysis examples
- Quick algorithm testing

**Example Usage:**
```python
import pandas as pd
df = pd.read_csv("datasets/sample/iris.csv")
print(df.head())
```

#### 2. Boston Housing (Regression)
**Location:** `datasets/sample/boston_housing.csv`  
**Description:** Housing price prediction dataset  
**Size:** ~50 KB  
**Rows:** 506  
**Columns:** 14 (features + target: MEDV)  
**Use Cases:**
- MLOps regression problems
- Feature engineering examples
- Data analysis demonstrations

**Example Usage:**
```python
import pandas as pd
df = pd.read_csv("datasets/sample/boston_housing.csv")
X = df.drop('MEDV', axis=1)
y = df['MEDV']
```

#### 3. Sample Reviews (Text)
**Location:** `datasets/sample/reviews.txt`  
**Description:** Product reviews for sentiment analysis  
**Size:** ~10 KB  
**Format:** One review per line  
**Use Cases:**
- GenAI text processing
- Sentiment analysis examples
- LLM integration testing

**Example Usage:**
```python
with open("datasets/sample/reviews.txt", 'r') as f:
    reviews = [line.strip() for line in f.readlines()]

# Use with LLM
from app.utils.llm_client_manager import LLMClientManager
manager = LLMClientManager()
response = manager.generate(
    provider="openai",
    prompt=f"Analyze sentiment: {reviews[0]}"
)
```

#### 4. Sales Data (Business Analytics)
**Location:** `datasets/sample/sales_data.csv`  
**Description:** Sample sales data for business analysis  
**Size:** ~8 KB  
**Rows:** 100  
**Columns:** 5 (date, product, sales, region, profit)  
**Use Cases:**
- Data analysis problems
- Business intelligence examples
- Pattern detection demonstrations

**Example Usage:**
```python
import pandas as pd
df = pd.read_csv("datasets/sample/sales_data.csv")
# Use with data_analyzer
from app.genai.data_analyzer.data_analyzer import DataAnalyzer
analyzer = DataAnalyzer()
result = analyzer.analyze(df, analysis_type="summary")
```

#### 5. Employee Data (HR Analytics)
**Location:** `datasets/sample/employee_data.csv`  
**Description:** Sample employee data for HR analysis  
**Size:** ~6 KB  
**Rows:** 50  
**Columns:** 5 (name, age, department, salary, experience_years)  
**Use Cases:**
- Data analysis examples
- Pattern detection
- Comparison analysis

**Example Usage:**
```python
import pandas as pd
df = pd.read_csv("datasets/sample/employee_data.csv")
# Analyze patterns
from app.genai.data_analyzer.data_analyzer import DataAnalyzer
analyzer = DataAnalyzer()
result = analyzer.analyze(
    df.to_dict('records'),
    analysis_type="patterns",
    focus_areas=["salary", "department"]
)
```

### Creating Your Own Sample Datasets

If you need to create sample datasets for testing:

```python
# Generate synthetic classification data
from sklearn.datasets import make_classification
import pandas as pd

X, y = make_classification(n_samples=100, n_features=4, random_state=42)
df = pd.DataFrame(X, columns=['feature1', 'feature2', 'feature3', 'feature4'])
df['target'] = y
df.to_csv("datasets/sample/my_classification_data.csv", index=False)
```

### Sample Dataset Guidelines

When adding new sample datasets:

1. **Keep it small**: < 100 KB
2. **Make it realistic**: Use realistic values and patterns
3. **Document it**: Add entry to this README
4. **Include headers**: CSV files should have column names
5. **Clean data**: No missing values or obvious errors
6. **License**: Use public domain or clearly licensed data

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

### Loading Sample Datasets

```python
# Load sample CSV dataset
import pandas as pd
df = pd.read_csv("datasets/sample/iris.csv")

# Load sample text dataset
with open("datasets/sample/reviews.txt", 'r') as f:
    texts = [line.strip() for line in f.readlines()]

# Load sample JSON dataset (if available)
import json
with open("datasets/sample/data.json", 'r') as f:
    data = json.load(f)
```

### Loading MLOps Datasets

```python
# Load CSV dataset
import pandas as pd
df = pd.read_csv("datasets/mlops/classification/data.csv")

# Split features and target
X = df.drop('target', axis=1)
y = df['target']
```

### Loading GenAI Datasets

```python
# Load text dataset
with open("datasets/genai/text/data.txt", 'r') as f:
    texts = f.readlines()

# Load JSON dataset
import json
with open("datasets/genai/documents/data.json", 'r') as f:
    data = json.load(f)
```

### Using with Data Analyzer

```python
from app.genai.data_analyzer.data_analyzer import DataAnalyzer

analyzer = DataAnalyzer()

# From CSV file
result = analyzer.analyze(
    data="datasets/sample/sales_data.csv",
    analysis_type="summary",
    data_format="csv"
)

# From dictionary
result = analyzer.analyze(
    data={"sales": [100, 200, 300], "month": ["Jan", "Feb", "Mar"]},
    analysis_type="trends"
)
```

---

**Keep datasets small, documented, and properly licensed!**

