# ThinkCraft

> **Hands-on problem-solving repository for Python, MLOps, GenAI, and Agentic Systems**

A curated collection of real-world coding challenges with focus on best practices, complexity analysis, and production-ready solutions.

**Author:** chronosnehal  
**Python Version:** 3.12 (required)

---

## 🎯 Quick Start

**Python Version:** Python 3.12 is required for this repository.

```bash
# Clone and setup
git clone <repository-url>
cd thinkcraft

# Create virtual environment with Python 3.12
python3.12 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies from root requirements.txt
# (All problems use the root virtual environment)
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Add your LLM API keys to .env

# Run a problem (examples)
python app/python/binary_search/binary_search.py
python app/mlops/model_training_pipeline/model_training_pipeline.py
python app/genai/sentiment_analysis/sentiment_analysis.py
```

**Note:** All problems use the root virtual environment. Dependencies are managed centrally via `requirements.in`. Use `./scripts/generate_requirements.sh` to regenerate `requirements.txt`.

---

## 📁 Repository Structure

```
thinkcraft/
├── app/
│   ├── basic/          # One-liners (15-20 min)
│   ├── python/         # Algorithms (20-35 min)
│   ├── mlops/          # ML Training (25-45 min)
│   ├── genai/          # LLM Integration (20-40 min)
│   ├── agentic/        # Multi-step Agents (30-45 min)
│   └── utils/
│       └── llm_client_manager.py
├── datasets/           # Sample datasets for problems
│   ├── sample/         # Quick testing datasets
│   ├── mlops/          # ML training data
│   └── genai/          # Text and document data
├── docs/
│   ├── templates/      # Solution templates
│   ├── formatting_guide.md
│   ├── fastapi_guide.md
│   ├── complexity_analysis.md
│   ├── agentic_systems.md
│   └── llm_client_manager.md
├── scripts/
│   └── generate_requirements.sh  # Generate requirements.txt from requirements.in
├── requirements.in      # Source of truth for dependencies
├── requirements.txt     # Auto-generated (run ./scripts/generate_requirements.sh)
└── .github/
    └── CONTRIBUTING.md
```

---

## 🗂️ Problem Categories

### 1. Basic Python (15-20 min)
**Location:** `/app/basic/`  
**Focus:** One-liners, comprehensions, Pythonic tricks  
**Structure:** Single files, no subdirectories

```python
# Example: One-liner to find duplicates
duplicates = [x for x, count in Counter(lst).items() if count > 1]
```

### 2. Advanced Python (20-35 min)
**Location:** `/app/python/<problem_name>/`  
**Focus:** Algorithms, data structures, system design  
**Structure:** Each problem in own directory

```
/app/python/binary_search/
├── question_binary_search.md
└── binary_search.py
```

### 3. MLOps (25-45 min)
**Location:** `/app/mlops/<problem_name>/`  
**Focus:** Model training, feature engineering, deployment  
**Structure:** Complete ML pipeline  
**Datasets:** Use sample data from `/datasets/mlops/` or `/datasets/sample/`

```
/app/mlops/model_training_pipeline/
├── question_model_training_pipeline.md
├── model_training_pipeline.py
└── README.md

# Reference datasets
/datasets/mlops/classification/train_data.csv
/datasets/sample/iris.csv

# Note: Dependencies managed via root requirements.in
```

### 4. GenAI (20-40 min)
**Location:** `/app/genai/<problem_name>/`  
**Focus:** LLM integration, prompt engineering, NLP  
**Required:** Must use LLMClientManager  
**Datasets:** Use text data from `/datasets/genai/` or `/datasets/sample/`

```python
from app.utils.llm_client_manager import LLMClientManager

# Load sample data
with open("datasets/genai/text/reviews.txt", 'r') as f:
    texts = f.readlines()

# Process with LLM
manager = LLMClientManager()
response = manager.generate(
    provider="openai",
    prompt=f"Analyze: {texts[0]}",
    model="gpt-4"
)
```

### 5. Agentic Systems (30-45 min)
**Location:** `/app/agentic/<usecase_name>/`  
**Focus:** Multi-step reasoning (Perceive → Reason → Act → Reflect)  
**Structure:** Full FastAPI application

```
/app/agentic/code_generator/
├── main.py
├── api/
│   └── routes.py
├── core/
│   ├── agents.py
│   └── agent_state.py
├── models/
│   └── schemas.py
├── services/
│   └── agent_service.py
├── question_code_generator.md
├── README.md
└── env.example

# Note: Dependencies managed via root requirements.in
```

---

## 📚 Problem Catalog

**Total Problems:** 33 (18 Advanced Python, 1 Basic Python, 9 GenAI, 4 MLOps, 1 Agentic)

### Advanced Python

#### Algorithms & Data Structures
| Problem | Difficulty | Time | Description |
|---------|------------|------|-------------|
| [Binary Search](app/python/binary_search/) | Medium-Advanced | 25-30 min | Multiple binary search variations (standard, first/last occurrence, rotated array, peak element) |
| [Quick Sort](app/python/quick_sort/) | Medium-Advanced | 25-30 min | Quick sort implementations (standard, randomized, three-way partition, custom comparator, Kth smallest) |

#### Graph Algorithms
| Problem | Difficulty | Time | Description |
|---------|------------|------|-------------|
| [BFS Traversal](app/python/bfs_traversal/) | Medium | 20-25 min | Breadth-First Search traversal for graphs using queue data structure |
| [DFS Traversal](app/python/dfs_traversal/) | Medium | 20-25 min | Depth-First Search traversal for graphs using recursion or stack |
| [Dijkstra's Shortest Path](app/python/dijkstra_shortest_path/) | Advanced | 30-35 min | Find shortest paths in weighted graphs using Dijkstra's algorithm with priority queue |
| [Topological Sort](app/python/topological_sort/) | Advanced | 25-30 min | Perform topological sorting on directed acyclic graphs using Kahn's algorithm |
| [Cycle Detection](app/python/cycle_detection/) | Advanced | 25-30 min | Detect cycles in directed and undirected graphs using DFS |
| [Connected Components](app/python/connected_components/) | Medium-Advanced | 20-25 min | Find all connected components in undirected graphs using DFS |

#### Dynamic Programming
| Problem | Difficulty | Time | Description |
|---------|------------|------|-------------|
| [0/1 Knapsack](app/python/knapsack_01/) | Advanced | 25-30 min | Solve 0/1 knapsack problem using dynamic programming to maximize value within weight constraint |
| [Longest Common Subsequence](app/python/longest_common_subsequence/) | Advanced | 25-30 min | Find longest common subsequence between two strings using dynamic programming |
| [Edit Distance](app/python/edit_distance/) | Advanced | 25-30 min | Compute Levenshtein edit distance (minimum edits to transform one string to another) |
| [Coin Change](app/python/coin_change/) | Medium-Advanced | 25-30 min | Find minimum coins needed for target amount using dynamic programming (unbounded knapsack) |
| [Fibonacci](app/python/fibonacci/) | Medium | 20-25 min | Compute nth Fibonacci number using memoization and iterative approaches |
| [Longest Increasing Subsequence](app/python/longest_increasing_subsequence/) | Advanced | 25-30 min | Find longest increasing subsequence in array using dynamic programming |

#### System Design
| Problem | Difficulty | Time | Description |
|---------|------------|------|-------------|
| [Web Scraper](app/python/web_scraper/) | Advanced | 30-35 min | Cryptocurrency price data collection from APIs and web scraping with error handling and data validation |
| [Recommendation System](app/python/recommendation_system/) | Advanced | 35-40 min | Movie recommendation engine with content-based and collaborative filtering approaches |
| [Caching System](app/python/caching_system/) | Medium-Advanced | 25-30 min | Multi-policy caching system with LRU, LFU, FIFO eviction strategies and TTL support |
| [Rate Limiter](app/python/rate_limiter/) | Medium-Advanced | 25-30 min | Rate limiting system with token bucket, sliding window, fixed window, and leaky bucket algorithms |

### Basic Python

| Problem | Difficulty | Time | Description |
|---------|------------|------|-------------|
| [Python One-Liners](app/basic/python_one_liners.py) | Simple | 15-20 min | 289 one-liner solutions for common programming tasks |

### GenAI

| Problem | Difficulty | Time | Description |
|---------|------------|------|-------------|
| [Simple Code Generator](app/genai/simple_code_generator/) | Medium | 20-25 min | LLM-powered code generation for Python and JavaScript |
| [Creative Writer](app/genai/creative_writer/) | Medium | 20-25 min | Creative content generation (stories, poems, articles) with style customization |
| [Data Analyzer](app/genai/data_analyzer/) | Medium | 25-30 min | Natural language data analysis and insights generation |
| [Data Augmentation](app/genai/data_augmentation/) | Medium | 20-25 min | Product description variant generation using GenAI |
| [Entity Extraction](app/genai/entity_extraction/) | Medium | 20-25 min | Person names and dates extraction using few-shot prompting |
| [Image Captioning](app/genai/image_captioning/) | Medium | 25-30 min | Two-stage image captioning (factual + creative) using vision models |
| [QA System](app/genai/qa_system/) | Medium | 25-30 min | Question answering system with confidence scoring and citations |
| [Sentiment Analysis](app/genai/sentiment_analysis/) | Medium | 25-30 min | Text sentiment and emotion detection with reasoning |
| [Text Summarization](app/genai/text_summarization/) | Medium | 25-30 min | Extractive and abstractive summarization with various formats |

### MLOps

| Problem | Difficulty | Time | Description |
|---------|------------|------|-------------|
| [Model Training Pipeline](app/mlops/model_training_pipeline/) | Medium-Advanced | 30-35 min | End-to-end ML training pipeline with data loading, preprocessing, model training, evaluation, and persistence |
| [Feature Engineering](app/mlops/feature_engineering/) | Medium-Advanced | 30-35 min | Comprehensive feature engineering pipeline with numeric transformations, categorical encoding, temporal features, and feature selection |
| [Model Evaluation](app/mlops/model_evaluation/) | Medium | 25-30 min | Model evaluation system with metrics computation, cross-validation, and visualization for classification and regression |
| [Model Deployment](app/mlops/model_deployment/) | Advanced | 35-40 min | Production-ready FastAPI-based model deployment system with REST API endpoints, input validation, and error handling |

### Agentic Systems

| Problem | Difficulty | Time | Description |
|---------|------------|------|-------------|
| [Code Generator](app/agentic/code_generator/) | Advanced | 35-40 min | Multi-agent code generation system using LangGraph with perception, planning, generation, validation, and refinement |

---

## 🚀 Adding New Problems

### Step 1: Choose Category
- **Basic Python** → Add to existing files in `/app/basic/`
- **Advanced Python** → Create directory `/app/python/<problem_name>/`
- **MLOps** → Create directory `/app/mlops/<problem_name>/`
- **GenAI** → Create directory `/app/genai/<problem_name>/`
- **Agentic** → Create directory `/app/agentic/<usecase_name>/`

### Step 2: Use Template
```bash
# Copy appropriate template from /docs/templates/
cp docs/templates/python_solution_template.py app/python/my_problem/my_problem.py
cp docs/templates/question_template.md app/python/my_problem/question_my_problem.md
```

**Important:** Do NOT create `requirements.txt` files in problem directories. All dependencies are managed centrally via the root `requirements.in` file. If you need new dependencies:
1. Add them to `requirements.in`
2. Run `./scripts/generate_requirements.sh` to regenerate `requirements.txt`
3. Install with `pip install -r requirements.txt`

### Step 3: Implement
- Write problem statement
- Implement solution
- Add complexity analysis
- Include examples
- Handle edge cases

### Step 4: Quality Check
```bash
black app/python/my_problem/*.py
flake8 app/python/my_problem/*.py
pylint app/python/my_problem/*.py
```

### Step 5: Test
```bash
python app/python/my_problem/my_problem.py
```

---

## 🛠️ Available Templates

| Template | Location | Use For |
|----------|----------|---------|
| Question | `docs/templates/question_template.md` | Problem statements |
| Basic Python | `docs/templates/basic_python_template.py` | One-liners |
| Advanced Python | `docs/templates/python_solution_template.py` | Algorithms |
| MLOps | `docs/templates/mlops_solution_template.py` | ML pipelines |
| GenAI | `docs/templates/genai_solution_template.py` | LLM integration |
| Agentic | `docs/templates/agentic_solution_template/` | Agent systems |

---

## 📖 Documentation

### Essential Guides
- **[Contributing Guidelines](.github/CONTRIBUTING.md)** - How to contribute
- **[Datasets Guide](datasets/README.md)** - Using and adding datasets
- **[Formatting Guide](docs/formatting_guide.md)** - Code style standards
- **[Complexity Analysis](docs/complexity_analysis.md)** - Big O notation guide
- **[FastAPI Guide](docs/fastapi_guide.md)** - Agentic system patterns
- **[Agentic Systems](docs/agentic_systems.md)** - Agent design patterns
- **[LLM Client Manager](docs/llm_client_manager.md)** - LLM provider usage

---

## 🔑 LLMClientManager

Centralized manager for multiple LLM providers:

```python
from app.utils.llm_client_manager import LLMClientManager

# Initialize
manager = LLMClientManager()

# Synchronous
response = manager.generate(
    provider="openai",  # or "azure", "gemini", "claude", "openrouter"
    prompt="Your prompt",
    model="gpt-4",
    temperature=0.7
)

# Asynchronous
response = await manager.generate_async(
    provider="openai",
    prompt="Your prompt"
)
```

**Supported Providers:**
- OpenAI (GPT-3.5, GPT-4)
- Azure OpenAI
- Google Gemini
- Anthropic Claude
- OpenRouter

---

## 📋 Code Standards

### Environment Requirements
- ✅ **Python 3.12** is required for this repository
- ✅ All problems use the **root virtual environment**
- ✅ Dependencies are managed via **root `requirements.in`** file
- ✅ Use `./scripts/generate_requirements.sh` to regenerate `requirements.txt`

### Required for All Solutions
- ✅ **Type hints** on all functions
- ✅ **Complexity analysis** (Time & Space) in docstrings
- ✅ **Comprehensive docstrings** (Google/NumPy style)
- ✅ **Input validation** and error handling
- ✅ **Logging** instead of print statements
- ✅ **Example usage** in `main()` function
- ✅ **PEP 8 compliance** (use `black` formatter)

### Example
```python
def binary_search(arr: List[int], target: int) -> int:
    """
    Perform binary search on sorted array.
    
    Args:
        arr: Sorted list of integers
        target: Value to find
    
    Returns:
        Index of target or -1 if not found
    
    Time Complexity: O(log n)
    Space Complexity: O(1)
    
    Examples:
        >>> binary_search([1, 2, 3, 4, 5], 3)
        2
    """
    # Implementation
```

---

## ⚡ Quick Commands

```bash
# Setup (Python 3.12 required)
python3.12 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Regenerate requirements.txt from requirements.in
./scripts/generate_requirements.sh

# Upgrade all packages to latest versions
./scripts/generate_requirements.sh --upgrade

# Run problems
python app/basic/python_one_liners.py
python app/python/<problem>/<problem>.py
python app/genai/<problem>/<problem>.py
python app/mlops/<problem>/<problem>.py

# Run agentic system
cd app/agentic/<usecase>
uvicorn main:app --reload --port 8000
# Visit http://localhost:8000/docs

# Code quality
black app/
flake8 app/
pylint app/

# Git workflow
git checkout -b feat/problem-name
git commit -m "feat(category): description"
git push origin feat/problem-name
```

---

## 🎓 Learning Path

### Week 1: Foundations
- Day 1-2: Basic Python one-liners
- Day 3-4: Advanced Python algorithms
- Day 5: Review and practice

### Week 2: AI Integration
- Day 1-2: GenAI problems with LLMs
- Day 3-4: MLOps pipelines
- Day 5: Testing and refinement

### Week 3: Advanced Systems
- Day 1-3: Build agentic systems
- Day 4-5: Multi-agent workflows

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](.github/CONTRIBUTING.md) for guidelines.

---

## 📜 License

This project is licensed under the terms specified in the [LICENSE](LICENSE) file.

---

## 📞 Contact

For questions or issues, please open an issue in the repository.

---

**Happy Coding!** 🚀
