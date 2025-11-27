# Complexity Analysis Guide

**Author:** chronosnehal

Time and space complexity analysis ensures solutions are efficient and scalable. Every function in ThinkCraft must document its complexity.

---

## Big O Notation Basics

### Common Time Complexities (Best to Worst)

| Notation | Name | Example |
|----------|------|---------|
| O(1) | Constant | Array access, hash table lookup |
| O(log n) | Logarithmic | Binary search, balanced tree operations |
| O(n) | Linear | Single loop, linear search |
| O(n log n) | Linearithmic | Merge sort, heap sort |
| O(n²) | Quadratic | Nested loops, bubble sort |
| O(2ⁿ) | Exponential | Recursive fibonacci, subset generation |
| O(n!) | Factorial | Permutations, traveling salesman |

### Common Space Complexities

| Notation | Description | Example |
|----------|-------------|---------|
| O(1) | Constant space | Few variables, in-place operations |
| O(log n) | Logarithmic space | Recursive call stack (balanced tree) |
| O(n) | Linear space | Array/list of size n, hash table |
| O(n²) | Quadratic space | 2D matrix |

---

## How to Write Complexity Analysis

### Required Format

Every function must include complexity in its docstring:

```python
def function_name(param: Type) -> ReturnType:
    """
    Brief description of what the function does.
    
    Args:
        param: Description of parameter
    
    Returns:
        Description of return value
    
    Time Complexity: O(?) - Explain why
    Space Complexity: O(?) - Explain why
    """
```

---

## Examples

### Example 1: Constant Time O(1)

```python
def get_first_element(arr: list[int]) -> int:
    """
    Get the first element of an array.
    
    Args:
        arr: List of integers
    
    Returns:
        First element
    
    Time Complexity: O(1) - Direct array access
    Space Complexity: O(1) - No extra space used
    """
    return arr[0]
```

### Example 2: Linear Time O(n)

```python
def find_max(arr: list[int]) -> int:
    """
    Find maximum element in array.
    
    Args:
        arr: List of integers
    
    Returns:
        Maximum value
    
    Time Complexity: O(n) - Must check every element once
    Space Complexity: O(1) - Only stores max variable
    """
    max_val = arr[0]
    for num in arr:  # O(n) - iterate through all elements
        if num > max_val:
            max_val = num
    return max_val
```

### Example 3: Logarithmic Time O(log n)

```python
def binary_search(arr: list[int], target: int) -> int:
    """
    Perform binary search on sorted array.
    
    Args:
        arr: Sorted list of integers
        target: Value to find
    
    Returns:
        Index of target or -1 if not found
    
    Time Complexity: O(log n) - Halves search space each iteration
    Space Complexity: O(1) - Only uses constant extra variables
    """
    left, right = 0, len(arr) - 1
    
    while left <= right:  # O(log n) iterations
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1
```

### Example 4: Quadratic Time O(n²)

```python
def bubble_sort(arr: list[int]) -> list[int]:
    """
    Sort array using bubble sort.
    
    Args:
        arr: List of integers
    
    Returns:
        Sorted list
    
    Time Complexity: O(n²) - Nested loops, each O(n)
    Space Complexity: O(1) - In-place sorting
    """
    n = len(arr)
    for i in range(n):  # O(n) outer loop
        for j in range(0, n - i - 1):  # O(n) inner loop
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr
```

### Example 5: Linearithmic Time O(n log n)

```python
def merge_sort(arr: list[int]) -> list[int]:
    """
    Sort array using merge sort.
    
    Args:
        arr: List of integers
    
    Returns:
        Sorted list
    
    Time Complexity: O(n log n) - Divide (log n) and merge (n)
    Space Complexity: O(n) - Temporary arrays for merging
    """
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])   # O(log n) divisions
    right = merge_sort(arr[mid:])
    
    return merge(left, right)  # O(n) merge operation
```

---

## Analysis Tips

### 1. Count Operations
- Identify loops and their iterations
- Count recursive calls
- Consider nested structures

### 2. Focus on Dominant Term
```python
# O(n² + n + 1) simplifies to O(n²)
# O(2n + 5) simplifies to O(n)
# O(n log n + n) simplifies to O(n log n)
```

### 3. Consider Best, Average, Worst Cases
```python
def linear_search(arr: list[int], target: int) -> int:
    """
    Time Complexity:
    - Best: O(1) - Target is first element
    - Average: O(n) - Target is in middle
    - Worst: O(n) - Target is last or not present
    """
```

### 4. Amortized Analysis
```python
def dynamic_array_append(arr: list, item: Any) -> None:
    """
    Time Complexity: O(1) amortized
    - Most appends are O(1)
    - Occasional resize is O(n)
    - Averages to O(1) per operation
    """
```

---

## Common Mistakes to Avoid

### ❌ Mistake 1: Ignoring Hidden Complexity
```python
# WRONG: Claiming O(n)
def process(arr: list[str]) -> list[str]:
    return sorted(arr)  # sorted() is O(n log n), not O(n)!
```

### ❌ Mistake 2: Confusing Time and Space
```python
# WRONG: Claiming O(1) space
def create_copy(arr: list[int]) -> list[int]:
    return arr.copy()  # Creates O(n) space!
```

### ❌ Mistake 3: Missing Recursive Space
```python
# WRONG: Claiming O(1) space
def factorial(n: int) -> int:
    if n <= 1:
        return 1
    return n * factorial(n - 1)  # O(n) call stack space!
```

---

## Checklist

Before submitting code, verify:
- [ ] Every function has Time Complexity documented
- [ ] Every function has Space Complexity documented
- [ ] Complexity includes brief explanation
- [ ] Analysis considers all loops and recursion
- [ ] Hidden complexity (built-in functions) is accounted for
- [ ] Best/worst cases noted if significantly different

---

## Quick Reference

```python
# Template for complexity documentation
def function_name(param: Type) -> ReturnType:
    """
    Function description.
    
    Time Complexity: O(?) - Why this complexity
    Space Complexity: O(?) - Why this complexity
    """
    pass
```

---

**Remember:** Complexity analysis is mandatory for all ThinkCraft solutions!
