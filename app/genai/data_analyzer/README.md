# Data Analysis System

> **GenAI Problem** - Data analysis system using LLM integration

A comprehensive data analysis system that analyzes datasets and generates natural language insights, summaries, and recommendations. Supports various data formats (CSV, JSON, dict, list), identifies patterns, detects trends, and provides actionable business intelligence.

**Author:** chronosnehal  
**Category:** GenAI  
**Difficulty:** Medium  
**Time:** 25-30 minutes

---

## 🎯 Features

- ✅ **Multiple Data Formats**: CSV, JSON, dict, list support
- ✅ **Analysis Types**: Summary, Patterns, Trends, Comparison, Anomalies, Comprehensive
- ✅ **Natural Language Insights**: LLM-generated insights and summaries
- ✅ **Pattern Detection**: Identifies patterns and correlations
- ✅ **Trend Analysis**: Analyzes trends over time or categories
- ✅ **Recommendations**: Actionable business intelligence
- ✅ **Visualization Suggestions**: Chart and graph recommendations
- ✅ **Large Dataset Handling**: Automatic sampling for efficiency
- ✅ **LLM Integration**: Uses LLMClientManager for multi-provider support

---

## 📁 Project Structure

```
data_analyzer/
├── question_data_analyzer.md   # Problem description
├── data_analyzer.py             # Solution implementation
└── README.md                    # This file
```

---

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Set your LLM API key (e.g., OpenAI)
export OPENAI_API_KEY=your_api_key_here

# Or use .env file
echo "OPENAI_API_KEY=your_api_key_here" > .env

# Optional: Install pandas for better CSV handling
pip install pandas
```

### 2. Run the Solution

```bash
# From repository root
python app/genai/data_analyzer/data_analyzer.py
```

---

## 💻 Usage Examples

### Basic Usage

```python
from app.genai.data_analyzer.data_analyzer import DataAnalyzer

# Initialize analyzer
analyzer = DataAnalyzer(provider="openai")

# Analyze dictionary data
sales_data = {
    "month": ["Jan", "Feb", "Mar"],
    "sales": [10000, 12000, 15000]
}

result = analyzer.analyze(
    data=sales_data,
    analysis_type="summary",
    include_recommendations=True
)

if result["success"]:
    print(result["summary"])
    for insight in result["insights"]:
        print(f"- {insight}")
```

### Pattern Analysis

```python
employee_data = [
    {"age": 25, "salary": 50000, "department": "Engineering"},
    {"age": 30, "salary": 70000, "department": "Engineering"}
]

result = analyzer.analyze(
    data=employee_data,
    analysis_type="patterns",
    focus_areas=["salary", "department"],
    include_recommendations=True
)

print(result["patterns"])
```

### CSV File Analysis

```python
result = analyzer.analyze(
    data="datasets/sample/sales_data.csv",
    analysis_type="comprehensive",
    data_format="csv",
    include_recommendations=True,
    include_visualizations=True
)

print(result["summary"])
print(result["visualization_suggestions"])
```

---

## 📖 API Reference

### `DataAnalyzer`

#### Constructor

```python
analyzer = DataAnalyzer(
    provider: str = "openai",
    model: Optional[str] = None,
    max_rows_for_analysis: int = 1000
)
```

**Parameters:**
- `provider`: LLM provider (openai, azure, gemini, claude, openrouter)
- `model`: Model name (defaults to provider's default)
- `max_rows_for_analysis`: Maximum rows to analyze directly (default: 1000)

#### `analyze()`

```python
result = analyzer.analyze(
    data: Union[str, dict, list],
    analysis_type: str,
    data_format: Optional[str] = None,
    focus_areas: Optional[List[str]] = None,
    include_recommendations: bool = True,
    include_visualizations: bool = False,
    context: Optional[str] = None
) -> Dict[str, Any]
```

**Parameters:**
- `data`: Dataset (path to CSV/JSON, dict, list, or JSON string)
- `analysis_type`: One of ["summary", "patterns", "trends", "comparison", "anomalies", "comprehensive"]
- `data_format`: Format hint (csv, json, dict, list) - auto-detected if None
- `focus_areas`: Specific columns/fields to analyze (optional)
- `include_recommendations`: Whether to include recommendations (default: True)
- `include_visualizations`: Whether to suggest visualizations (default: False)
- `context`: Additional context about the data (max 200 characters)

**Returns:**
```python
{
    "success": bool,
    "summary": str,
    "insights": list[str],
    "patterns": list[str],
    "trends": list[str],
    "anomalies": list[str],
    "recommendations": list[str],
    "visualization_suggestions": list[str],
    "metadata": {
        "data_shape": tuple,
        "columns": list[str] | None,
        "analysis_type": str,
        "data_types": dict | None
    },
    "error": str | None
}
```

**Raises:**
- `ValueError`: If input is invalid

---

## 📊 Analysis Types

### Summary
High-level overview and key statistics of the dataset.

```python
result = analyzer.analyze(
    data=your_data,
    analysis_type="summary"
)
```

### Patterns
Identify patterns, correlations, and relationships in the data.

```python
result = analyzer.analyze(
    data=your_data,
    analysis_type="patterns",
    focus_areas=["column1", "column2"]
)
```

### Trends
Analyze trends over time or across categories.

```python
result = analyzer.analyze(
    data=your_data,
    analysis_type="trends"
)
```

### Comparison
Compare different segments or groups in the data.

```python
result = analyzer.analyze(
    data=your_data,
    analysis_type="comparison"
)
```

### Anomalies
Detect outliers and unusual values.

```python
result = analyzer.analyze(
    data=your_data,
    analysis_type="anomalies"
)
```

### Comprehensive
Full analysis with all components (summary, patterns, trends, anomalies, recommendations).

```python
result = analyzer.analyze(
    data=your_data,
    analysis_type="comprehensive",
    include_recommendations=True,
    include_visualizations=True
)
```

---

## 📁 Data Format Support

### CSV Files
```python
result = analyzer.analyze(
    data="path/to/data.csv",
    analysis_type="summary",
    data_format="csv"
)
```

### JSON Files
```python
result = analyzer.analyze(
    data="path/to/data.json",
    analysis_type="summary",
    data_format="json"
)
```

### Python Dictionary
```python
data = {
    "column1": [1, 2, 3],
    "column2": ["a", "b", "c"]
}
result = analyzer.analyze(
    data=data,
    analysis_type="summary",
    data_format="dict"
)
```

### Python List
```python
data = [
    {"key1": "value1", "key2": "value2"},
    {"key1": "value3", "key2": "value4"}
]
result = analyzer.analyze(
    data=data,
    analysis_type="summary",
    data_format="list"
)
```

---

## 🧪 Examples

### Example 1: Sales Data Analysis

```python
sales_data = {
    "month": ["Jan", "Feb", "Mar", "Apr", "May"],
    "sales": [10000, 12000, 15000, 14000, 18000],
    "region": ["North", "South", "North", "South", "North"]
}

result = analyzer.analyze(
    data=sales_data,
    analysis_type="summary",
    include_recommendations=True,
    context="Monthly sales data for Q1-Q2"
)

print(result["summary"])
print("\nInsights:")
for insight in result["insights"]:
    print(f"- {insight}")
```

### Example 2: Employee Data Patterns

```python
employee_data = [
    {"age": 25, "salary": 50000, "department": "Engineering"},
    {"age": 30, "salary": 70000, "department": "Engineering"},
    {"age": 28, "salary": 45000, "department": "Marketing"}
]

result = analyzer.analyze(
    data=employee_data,
    analysis_type="patterns",
    focus_areas=["salary", "department"],
    include_recommendations=True
)

print("Patterns identified:")
for pattern in result["patterns"]:
    print(f"- {pattern}")
```

### Example 3: Comprehensive Analysis with Visualizations

```python
result = analyzer.analyze(
    data="datasets/sample/data.csv",
    analysis_type="comprehensive",
    data_format="csv",
    include_recommendations=True,
    include_visualizations=True
)

print("Visualization Suggestions:")
for viz in result["visualization_suggestions"]:
    print(f"- {viz}")
```

---

## 🏗️ Architecture

### Simple Flow

```
User Request → Data Loading → Format Detection → Data Sampling → Prompt Engineering → LLM Call → Insight Extraction → Structured Output
```

### Key Components

1. **Data Loading**: Loads data from CSV, JSON, dict, or list formats
2. **Format Detection**: Auto-detects data format if not specified
3. **Data Sampling**: Samples large datasets (>1000 rows) for efficiency
4. **Prompt Engineering**: Builds analysis-specific prompts with context
5. **LLM Integration**: Uses LLMClientManager for insight generation
6. **Insight Extraction**: Parses structured insights from LLM response
7. **Metadata Calculation**: Tracks data shape, columns, types

---

## 🔧 Configuration

### Supported Providers

- **OpenAI**: GPT-4, GPT-3.5-turbo
- **Azure OpenAI**: GPT-4
- **Google Gemini**: gemini-pro
- **Anthropic Claude**: claude-3-opus-20240229
- **OpenRouter**: Various models

### Environment Variables

```bash
# Required for OpenAI
OPENAI_API_KEY=your_key

# Optional - other providers
ANTHROPIC_API_KEY=your_key
GOOGLE_API_KEY=your_key
AZURE_OPENAI_API_KEY=your_key
AZURE_OPENAI_ENDPOINT=your_endpoint
```

### Optional Dependencies

```bash
# For better CSV handling
pip install pandas
```

---

## ⚠️ Limitations

- **Large Datasets**: Automatically samples datasets >1000 rows
- **Data Types**: Basic type detection (enhanced with pandas)
- **Complex Analysis**: Best for structured, tabular data
- **No Execution**: Analysis is LLM-based, not statistical computation

---

## 💡 Tips

1. **Use Focus Areas**: Specify columns to focus analysis
2. **Provide Context**: Add context for better insights
3. **Choose Right Type**: Select appropriate analysis type
4. **Enable Visualizations**: Get chart suggestions for better understanding
5. **Sample Large Data**: System auto-samples, but consider pre-processing

---

## 📝 Notes

- Uses pandas if available for better CSV handling
- Automatically samples large datasets for efficiency
- Structured output format for easy parsing
- Metadata includes data shape and column information
- Error handling for invalid data formats

---

## 🤝 Contributing

When extending this solution:
1. Keep it simple (no multi-agent workflow)
2. Use LLMClientManager for all LLM calls
3. Add proper error handling
4. Include example usage
5. Document complexity analysis

---

**Built with ❤️ by chronosnehal**

