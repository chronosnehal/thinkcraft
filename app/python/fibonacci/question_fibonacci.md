# Fibonacci Sequence

**Difficulty:** Medium  
**Time to Solve:** 20-25 min  
**Category:** Advanced Python

---

## Problem Description

Compute the nth Fibonacci number using dynamic programming with memoization. The Fibonacci sequence is defined as:
- F(0) = 0
- F(1) = 1
- F(n) = F(n-1) + F(n-2) for n > 1

This problem demonstrates understanding of:
- Memoization for recursive optimization
- Dynamic programming basics
- Space-time tradeoffs

---

## Input Specification

- **Type:** `int`
- **Format:**
  - `n`: Index of Fibonacci number (0-indexed)
- **Constraints:**
  - `0 ≤ n ≤ 100`
  - For larger n, use iterative approach

---

## Output Specification

- **Type:** `int`
- **Format:**
  - nth Fibonacci number
- **Requirements:**
  - Return 0 for n=0
  - Return 1 for n=1

---

## Examples

### Example 1: Basic Case
**Input:**
```python
n = 10
```

**Output:**
```python
55
```

**Explanation:**  
Fibonacci sequence: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, ...
F(10) = 55

---

### Example 2: First Few Numbers
**Input:**
```python
n = 5
```

**Output:**
```python
5
```

**Explanation:**  
F(5) = F(4) + F(3) = 3 + 2 = 5

---

### Example 3: Base Cases
**Input:**
```python
n = 0
```

**Output:**
```python
0
```

---

## Edge Cases to Consider

1. **n = 0:**
   - Expected behavior: Return 0

2. **n = 1:**
   - Expected behavior: Return 1

3. **Negative n:**
   - Expected behavior: Raise ValueError

---

## Constraints

- Must use memoization or iterative approach
- Must handle base cases correctly
- Should be efficient for n up to 100

---

## Solution Approach

### Memoization Strategy

1. **Base Cases**: F(0) = 0, F(1) = 1
2. **Recurrence**: F(n) = F(n-1) + F(n-2)
3. **Memoization**: Cache computed values to avoid recomputation
4. **Alternative**: Use iterative approach for O(1) space

### Algorithm Flow

```mermaid
graph TD
    A[Start] --> B{n <= 1?}
    B -->|Yes| C[Return n]
    B -->|No| D{In cache?}
    D -->|Yes| E[Return cached]
    D -->|No| F[Compute F(n-1) + F(n-2)]
    F --> G[Cache result]
    G --> H[Return result]
```

---

## Complexity Requirements

- **Target Time Complexity:** O(n) with memoization
- **Target Space Complexity:** O(n) for memoization, O(1) for iterative
- **Naive Recursive:** O(2^n) without memoization
- **Justification:** Each value computed once with memoization

---

## Additional Notes

- Classic introduction to dynamic programming
- Demonstrates importance of memoization
- Can be optimized to O(1) space iteratively
- Used in many algorithms (golden ratio, nature patterns)

---

## Related Concepts

- Dynamic Programming
- Memoization
- Recursion Optimization
- Space-Time Tradeoff

---

## Testing Hints

1. Test with small values first (0, 1, 2, 3)
2. Verify against known Fibonacci sequence
3. Test edge cases (0, 1, negative)
4. Compare memoized vs iterative performance
5. Test with larger values

---

## Success Criteria

Your solution should:
- [ ] Compute Fibonacci correctly
- [ ] Use memoization or iterative approach
- [ ] Handle base cases correctly
- [ ] Handle edge cases (negative n)
- [ ] Include comprehensive docstrings
- [ ] Have proper type hints
- [ ] Include example usage in main()

