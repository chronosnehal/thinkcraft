# Longest Increasing Subsequence (LIS)

**Difficulty:** Advanced  
**Time to Solve:** 25-30 min  
**Category:** Advanced Python

---

## Problem Description

Find the longest increasing subsequence (LIS) in an array using dynamic programming. A subsequence is a sequence derived by deleting some elements without changing the order of remaining elements.

This problem demonstrates understanding of:
- Dynamic programming for sequence problems
- Subsequence reconstruction
- Optimization problems

---

## Input Specification

- **Type:** `List[int]`
- **Format:**
  - `nums`: List of integers
- **Constraints:**
  - `1 ≤ len(nums) ≤ 2500`
  - `-10^4 ≤ nums[i] ≤ 10^4`
  - Array may contain duplicates

---

## Output Specification

- **Type:** `Tuple[int, List[int]]`
- **Format:**
  - First element: Length of LIS
  - Second element: The LIS itself
- **Requirements:**
  - LIS must be strictly increasing
  - Return (0, []) for empty array

---

## Examples

### Example 1: Basic Case
**Input:**
```python
nums = [10, 9, 2, 5, 3, 7, 101, 18]
```

**Output:**
```python
(4, [2, 3, 7, 18])
```

**Explanation:**  
The LIS [2, 3, 7, 18] has length 4. Other possible LIS: [2, 5, 7, 18] or [2, 3, 7, 101].

---

### Example 2: Already Sorted
**Input:**
```python
nums = [1, 2, 3, 4, 5]
```

**Output:**
```python
(5, [1, 2, 3, 4, 5])
```

**Explanation:**  
Entire array is increasing, so LIS is the whole array.

---

### Example 3: Decreasing Order
**Input:**
```python
nums = [5, 4, 3, 2, 1]
```

**Output:**
```python
(1, [1])
```

**Explanation:**  
No increasing subsequence longer than 1.

---

## Edge Cases to Consider

1. **Empty array:**
   - Expected behavior: Return (0, [])

2. **Single element:**
   - Expected behavior: Return (1, [element])

3. **All elements same:**
   - Expected behavior: Return (1, [first_element])

4. **All decreasing:**
   - Expected behavior: Return (1, [smallest_element])

---

## Constraints

- Must use dynamic programming
- Must reconstruct the actual LIS, not just length
- Must handle duplicates correctly

---

## Solution Approach

### Dynamic Programming Strategy

1. **State Definition**: `dp[i]` = length of LIS ending at index `i`
2. **Base Case**: `dp[i] = 1` for all i (each element is LIS of length 1)
3. **Recurrence Relation**: 
   - For each i, check all j < i
   - If `nums[j] < nums[i]`: `dp[i] = max(dp[i], dp[j] + 1)`
4. **Reconstruction**: Use parent array to trace back LIS

### Algorithm Flow

```mermaid
graph TD
    A[Start] --> B[Initialize dp and parent arrays]
    B --> C[For each index i]
    C --> D[For each j < i]
    D --> E{nums[j] < nums[i]?}
    E -->|Yes| F[Update dp[i] and parent[i]]
    E -->|No| G[Continue]
    F --> G
    G --> H{More j?}
    H -->|Yes| D
    H -->|No| I{More i?}
    I -->|Yes| C
    I -->|No| J[Find max length]
    J --> K[Reconstruct LIS]
    K --> L[Return Result]
```

---

## Complexity Requirements

- **Target Time Complexity:** O(n²)
- **Target Space Complexity:** O(n)
- **Optimization:** Can be optimized to O(n log n) using binary search
- **Justification:** Must check each element against all previous elements

---

## Additional Notes

- Classic DP problem
- Can be optimized to O(n log n) with binary search + patience sorting
- Used in many applications (longest chain, scheduling)
- Multiple LIS solutions may exist (implementation returns one)

---

## Related Concepts

- Dynamic Programming
- Subsequence Problems
- Binary Search (for optimization)
- Patience Sorting

---

## Testing Hints

1. Test with simple examples first
2. Verify LIS is actually increasing
3. Test edge cases (empty, single, all same)
4. Test with duplicates
5. Verify reconstruction is correct

---

## Success Criteria

Your solution should:
- [ ] Find LIS length correctly
- [ ] Reconstruct LIS correctly
- [ ] Use dynamic programming approach
- [ ] Handle all edge cases
- [ ] Include comprehensive docstrings
- [ ] Have proper type hints
- [ ] Include example usage in main()

