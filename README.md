# ThinkCraft

> **Hands-on problem-solving repository for Python, MLOps, GenAI, and Agentic Systems**

A curated collection of real-world coding challenges with focus on best practices, complexity analysis, and production-ready solutions.

**Author:** chronosnehal

---

## 🎯 Quick Start

```bash
# Clone and setup
git clone <repository-url>
cd thinkcraft
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Add your LLM API keys to .env

# Run a problem
python app/python/binary_search/binary_search.py
```

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
/app/mlops/model_training/
├── question_model_training.md
├── model_training.py
├── requirements.txt
└── README.md

# Reference datasets
/datasets/mlops/classification/train_data.csv
/datasets/sample/iris.csv
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
/app/agentic/research_assistant/
├── main.py
├── router.py
├── solution.py
├── models.py
├── question_research_assistant.md
├── README.md
└── requirements.txt
```

---

## 📚 Problem Catalog

| Problem | Category | Difficulty | Time | Description |
|---------|----------|------------|------|-------------|
| [Coming Soon] | Basic Python | Simple | 15 min | One-liner solutions |
| [Coming Soon] | Advanced Python | Medium | 25 min | Algorithm implementation |
| [Coming Soon] | MLOps | Advanced | 35 min | Model training pipeline |
| [Coming Soon] | GenAI | Medium | 30 min | LLM-powered solution |
| [Coming Soon] | Agentic | Advanced | 40 min | Multi-step agent system |

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
# Setup
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Run problems
python app/basic/one_liners.py
python app/python/<problem>/<problem>.py
python app/genai/<problem>/<problem>.py

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

**Quick checklist:**
- [ ] Problem statement is clear
- [ ] Solution has complexity analysis
- [ ] Code passes linting (`black`, `flake8`, `pylint`)
- [ ] Examples are included
- [ ] Documentation is updated
- [ ] Time limit is 15-45 minutes

---

## 📜 License

[Your License Here]

---

## 📞 Contact

**Author:** chronosnehal  
**Repository:** [GitHub URL]

For questions or issues, please open an issue in the repository.

---

**Happy Coding!** 🚀
