# Edit Distance (Levenshtein Distance)

**Difficulty:** Advanced  
**Time to Solve:** 25-30 min  
**Category:** Advanced Python

---

## Problem Description

Compute the minimum number of single-character edits (insertions, deletions, or substitutions) required to transform one string into another. This is also known as the Levenshtein distance.

This problem demonstrates understanding of:
- Dynamic programming for string transformation
- Edit operations (insert, delete, substitute)
- Minimum cost path problems

---

## Input Specification

- **Type:** `str`, `str`
- **Format:**
  - `s1`: Source string
  - `s2`: Target string
- **Constraints:**
  - `0 ≤ len(s1) ≤ 1000`
  - `0 ≤ len(s2) ≤ 1000`
  - Strings may contain any characters

---

## Output Specification

- **Type:** `int`
- **Format:**
  - Minimum number of edit operations required
- **Requirements:**
  - Return 0 if strings are identical
  - Return length of other string if one is empty

---

## Examples

### Example 1: Basic Case
**Input:**
```python
s1 = "kitten"
s2 = "sitting"
```

**Output:**
```python
3
```

**Explanation:**  
Transform "kitten" to "sitting":
1. k → s (substitute)
2. e → i (substitute)
3. Add g at end (insert)
Total: 3 operations

---

### Example 2: Identical Strings
**Input:**
```python
s1 = "abc"
s2 = "abc"
```

**Output:**
```python
0
```

**Explanation:**  
No edits needed for identical strings.

---

### Example 3: Empty String
**Input:**
```python
s1 = ""
s2 = "abc"
```

**Output:**
```python
3
```

**Explanation:**  
Need to insert all 3 characters.

---

## Edge Cases to Consider

1. **Empty strings:**
   - Expected behavior: Return length of non-empty string

2. **Identical strings:**
   - Expected behavior: Return 0

3. **One character difference:**
   - Expected behavior: Return 1

---

## Constraints

- Must use dynamic programming
- All operations (insert, delete, substitute) cost 1
- Must handle edge cases gracefully

---

## Solution Approach

### Dynamic Programming Strategy

1. **State Definition**: `dp[i][j]` = edit distance between `s1[0:i]` and `s2[0:j]`
2. **Base Cases**: 
   - `dp[i][0] = i` (delete all characters from s1)
   - `dp[0][j] = j` (insert all characters from s2)
3. **Recurrence Relation**:
   - If `s1[i-1] == s2[j-1]`: `dp[i][j] = dp[i-1][j-1]` (no operation)
   - Otherwise: `dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])`
     - `dp[i-1][j]`: Delete from s1
     - `dp[i][j-1]`: Insert into s1
     - `dp[i-1][j-1]`: Substitute

### Algorithm Flow

```mermaid
graph TD
    A[Start] --> B[Initialize Base Cases]
    B --> C[Fill DP Table]
    C --> D{Characters match?}
    D -->|Yes| E[No operation needed]
    D -->|No| F[Choose min of 3 operations]
    E --> G[Next Cell]
    F --> G
    G --> H{More cells?}
    H -->|Yes| C
    H -->|No| I[Return dp[m][n]]
```

---

## Complexity Requirements

- **Target Time Complexity:** O(m * n)
- **Target Space Complexity:** O(m * n) for tabulation
- **Optimization:** Can be optimized to O(min(m, n)) space
- **Justification:** Must consider all character pairs

---

## Additional Notes

- Classic string DP problem
- Used in spell checkers, DNA sequence alignment
- Can be extended with different costs for operations
- Can reconstruct the actual sequence of operations

---

## Related Concepts

- Dynamic Programming
- String Algorithms
- Levenshtein Distance
- Sequence Alignment
- Minimum Edit Distance

---

## Testing Hints

1. Test with simple examples first
2. Verify with known edit distances
3. Test edge cases (empty, identical, one char)
4. Test with strings of different lengths
5. Verify operations are counted correctly

---

## Success Criteria

Your solution should:
- [ ] Compute edit distance correctly
- [ ] Use dynamic programming approach
- [ ] Handle all edge cases
- [ ] Include comprehensive docstrings
- [ ] Have proper type hints
- [ ] Include example usage in main()

