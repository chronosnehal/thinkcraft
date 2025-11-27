# Formatting Guide

**Author:** chronosnehal

This guide defines the formatting standards for all code and documentation in ThinkCraft.

---

## Python Code Formatting

### 1. Code Formatter: Black

**Required:** All Python code must be formatted with `black`.

```bash
# Format single file
black app/python/problem/solution.py

# Format entire directory
black app/

# Check without modifying
black --check app/
```

**Configuration:** Use default black settings (88 character line length).

---

### 2. PEP 8 Compliance

Follow [PEP 8](https://pep8.org/) style guide:

#### Naming Conventions

```python
# Variables and functions: snake_case
user_name = "John"
def calculate_total(items: list) -> float:
    pass

# Classes: PascalCase
class UserAccount:
    pass

# Constants: UPPER_CASE
MAX_RETRIES = 3
API_TIMEOUT = 30

# Private members: _leading_underscore
class MyClass:
    def __init__(self):
        self._private_var = 10
    
    def _private_method(self):
        pass
```

#### Indentation

```python
# Use 4 spaces (not tabs)
def example():
    if condition:
        do_something()
        do_another_thing()
```

#### Line Length

```python
# Prefer 88 characters (black default)
# Maximum 120 characters for documentation

# Good: Break long lines
result = some_function(
    parameter1=value1,
    parameter2=value2,
    parameter3=value3
)

# Good: Use parentheses for line continuation
total = (
    first_value
    + second_value
    + third_value
)
```

---

### 3. Imports

```python
# Order: Standard library, third-party, local
import os
import sys
from typing import List, Dict, Optional

import numpy as np
import pandas as pd

from app.utils.llm_client_manager import LLMClientManager
from app.python.helpers import utility_function

# Group and sort alphabetically within groups
# One import per line for 'from' imports
from typing import (
    Any,
    Dict,
    List,
    Optional,
)
```

---

### 4. Type Hints

**Required:** All functions must have type hints.

```python
# Good: Complete type hints
def process_data(
    data: List[int],
    threshold: float = 0.5,
    options: Optional[Dict[str, Any]] = None
) -> Tuple[List[int], Dict[str, float]]:
    """Process data with threshold."""
    pass

# Bad: No type hints
def process_data(data, threshold=0.5, options=None):
    pass
```

**Modern Type Hints (Python 3.10+):**

```python
# Use | for Union
def func(value: int | str) -> bool:
    pass

# Use list, dict directly (no typing.List, typing.Dict)
def func(items: list[int]) -> dict[str, float]:
    pass
```

---

### 5. Docstrings

**Required:** All functions and classes must have docstrings.

**Style:** Google or NumPy style (be consistent).

#### Google Style (Recommended)

```python
def calculate_metrics(
    predictions: list[float],
    targets: list[float],
    threshold: float = 0.5
) -> dict[str, float]:
    """
    Calculate evaluation metrics for predictions.
    
    This function computes accuracy, precision, recall, and F1 score
    for binary classification predictions.
    
    Args:
        predictions: List of predicted probabilities
        targets: List of true labels (0 or 1)
        threshold: Classification threshold (default: 0.5)
    
    Returns:
        Dictionary containing metrics:
            - accuracy: Overall accuracy
            - precision: Precision score
            - recall: Recall score
            - f1: F1 score
    
    Raises:
        ValueError: If predictions and targets have different lengths
        TypeError: If inputs are not lists
    
    Time Complexity: O(n) where n is number of predictions
    Space Complexity: O(1) - only stores metric values
    
    Examples:
        >>> preds = [0.9, 0.1, 0.8, 0.3]
        >>> targets = [1, 0, 1, 0]
        >>> metrics = calculate_metrics(preds, targets)
        >>> print(metrics['accuracy'])
        1.0
    """
    pass
```

#### NumPy Style (Alternative)

```python
def calculate_metrics(predictions, targets, threshold=0.5):
    """
    Calculate evaluation metrics for predictions.
    
    Parameters
    ----------
    predictions : list[float]
        List of predicted probabilities
    targets : list[float]
        List of true labels (0 or 1)
    threshold : float, optional
        Classification threshold (default is 0.5)
    
    Returns
    -------
    dict[str, float]
        Dictionary containing accuracy, precision, recall, F1
    
    Raises
    ------
    ValueError
        If predictions and targets have different lengths
    
    Notes
    -----
    Time Complexity: O(n)
    Space Complexity: O(1)
    
    Examples
    --------
    >>> preds = [0.9, 0.1, 0.8, 0.3]
    >>> targets = [1, 0, 1, 0]
    >>> metrics = calculate_metrics(preds, targets)
    """
    pass
```

---

### 6. Comments

```python
# Good: Explain WHY, not WHAT
# Use binary search because data is sorted and we need O(log n)
result = binary_search(data, target)

# Bad: Obvious comment
# Loop through items
for item in items:
    process(item)

# Good: Complex logic explanation
# Calculate weighted average using exponential decay
# More recent values get higher weights
weights = [0.5 ** i for i in range(len(values))]
```

---

### 7. Logging vs Print

```python
import logging

logger = logging.getLogger(__name__)

# Good: Use logging
logger.info("Processing started")
logger.debug(f"Processing {len(data)} items")
logger.warning("Threshold below recommended value")
logger.error(f"Failed to process item: {error}")

# Bad: Use print for diagnostics
print("Processing started")  # Don't do this!
```

---

## Markdown Formatting

### 1. Headings

```markdown
# Main Title (H1) - Use once per file

## Section (H2)

### Subsection (H3)

#### Minor Section (H4)
```

### 2. Lists

```markdown
## Unordered Lists
- Item 1
- Item 2
  - Nested item
  - Another nested item
- Item 3

## Ordered Lists
1. First step
2. Second step
3. Third step

## Task Lists
- [x] Completed task
- [ ] Pending task
```

### 3. Code Blocks

````markdown
## Inline Code
Use `inline code` for short snippets, function names, or variables.

## Code Blocks
```python
def example():
    return "Hello"
```

## With Line Numbers (for references)
```python
1  def example():
2      return "Hello"
```
````

### 4. Links and References

```markdown
## External Links
[Python Documentation](https://docs.python.org/)

## Internal Links
See [Complexity Analysis](complexity_analysis.md) for details.

## Relative Links
[Templates](templates/python_solution_template.py)
```

### 5. Tables

```markdown
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Value 1  | Value 2  | Value 3  |
| Value 4  | Value 5  | Value 6  |

## Alignment
| Left | Center | Right |
|:-----|:------:|------:|
| L1   |   C1   |    R1 |
```

### 6. Emphasis

```markdown
**Bold text** for emphasis
*Italic text* for subtle emphasis
`code` for technical terms
> Blockquote for important notes
```

---

## File Structure

### Python Files

```python
#!/usr/bin/env python3
"""
[Problem Title] - Solution Implementation

Description: Brief description
Time Complexity: O(?)
Space Complexity: O(?)
Dependencies: List dependencies
Author: chronosnehal
Date: YYYY-MM-DD
"""

# Imports
import standard_library
from typing import Type

import third_party

from local_module import function

# Constants
MAX_VALUE = 100

# Classes
class MyClass:
    pass

# Functions
def my_function():
    pass

# Main execution
def main():
    pass

if __name__ == "__main__":
    main()
```

### Markdown Files

```markdown
# Title

**Author:** chronosnehal

Brief introduction paragraph.

---

## Section 1

Content...

### Subsection 1.1

Content...

---

## Section 2

Content...

---

## Summary

Final thoughts...
```

---

## Quality Checklist

Before committing code:

- [ ] Code formatted with `black`
- [ ] Passes `flake8` linting
- [ ] Passes `pylint` with score > 8.0
- [ ] All functions have type hints
- [ ] All functions have docstrings with complexity
- [ ] Imports are organized and sorted
- [ ] No print statements (use logging)
- [ ] Comments explain WHY, not WHAT
- [ ] Line length < 88 characters (code) or < 120 (docs)
- [ ] Markdown is properly formatted

---

## Tools

```bash
# Format
black app/

# Lint
flake8 app/
pylint app/

# Type check
mypy app/

# All at once
black app/ && flake8 app/ && pylint app/
```

---

## Quick Reference

```python
# Perfect function example
def process_data(
    data: list[int],
    threshold: float = 0.5
) -> dict[str, Any]:
    """
    Process data with threshold.
    
    Args:
        data: Input data list
        threshold: Processing threshold
    
    Returns:
        Processing results
    
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    logger.info(f"Processing {len(data)} items")
    
    # Process with threshold
    result = [x for x in data if x > threshold]
    
    return {"processed": result, "count": len(result)}
```

---

**Consistency is key! Follow these standards for all ThinkCraft code.**
