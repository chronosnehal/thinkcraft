# Longest Common Subsequence (LCS)

**Difficulty:** Advanced  
**Time to Solve:** 25-30 min  
**Category:** Advanced Python

---

## Problem Description

Find the longest common subsequence (LCS) between two strings using dynamic programming. A subsequence is a sequence that appears in the same relative order in both strings, but not necessarily contiguous.

This problem demonstrates understanding of:
- Dynamic programming for string problems
- Subsequence vs substring concepts
- Solution reconstruction from DP table

---

## Input Specification

- **Type:** `str`, `str`
- **Format:**
  - `s1`: First string
  - `s2`: Second string
- **Constraints:**
  - `0 ≤ len(s1) ≤ 1000`
  - `0 ≤ len(s2) ≤ 1000`
  - Strings may contain any characters

---

## Output Specification

- **Type:** `Tuple[int, str]`
- **Format:**
  - First element: Length of LCS
  - Second element: The LCS string itself
- **Requirements:**
  - LCS must be a valid subsequence of both strings
  - If no common subsequence exists, return (0, "")

---

## Examples

### Example 1: Basic Case
**Input:**
```python
s1 = "ABCDGH"
s2 = "AEDFHR"
```

**Output:**
```python
(3, "ADH")
```

**Explanation:**  
The LCS "ADH" appears in both strings:
- In "ABCDGH": A, D, H (positions 0, 3, 5)
- In "AEDFHR": A, D, H (positions 0, 2, 5)

---

### Example 2: No Common Subsequence
**Input:**
```python
s1 = "ABC"
s2 = "XYZ"
```

**Output:**
```python
(0, "")
```

**Explanation:**  
No common characters, so LCS length is 0.

---

### Example 3: Identical Strings
**Input:**
```python
s1 = "ABCD"
s2 = "ABCD"
```

**Output:**
```python
(4, "ABCD")
```

**Explanation:**  
Identical strings have LCS equal to the string itself.

---

## Edge Cases to Consider

1. **Empty strings:**
   - Expected behavior: Return (0, "")

2. **One empty string:**
   - Expected behavior: Return (0, "")

3. **No common characters:**
   - Expected behavior: Return (0, "")

4. **Single character strings:**
   - Expected behavior: Return (1, char) if same, (0, "") if different

---

## Constraints

- Must use dynamic programming
- Must reconstruct the actual LCS string, not just length
- Must handle edge cases gracefully

---

## Solution Approach

### Dynamic Programming Strategy

1. **State Definition**: `dp[i][j]` = length of LCS of `s1[0:i]` and `s2[0:j]`
2. **Base Case**: `dp[0][j] = 0` and `dp[i][0] = 0` (empty strings)
3. **Recurrence Relation**:
   - If `s1[i-1] == s2[j-1]`: `dp[i][j] = dp[i-1][j-1] + 1`
   - Otherwise: `dp[i][j] = max(dp[i-1][j], dp[i][j-1])`
4. **Reconstruction**: Trace back through DP table to build LCS string

### Algorithm Flow

```mermaid
graph TD
    A[Start] --> B[Initialize DP Table]
    B --> C[Fill DP Table]
    C --> D{Characters match?}
    D -->|Yes| E[dp[i][j] = dp[i-1][j-1] + 1]
    D -->|No| F[dp[i][j] = max of above/left]
    E --> G[Next Cell]
    F --> G
    G --> H{More cells?}
    H -->|Yes| C
    H -->|No| I[Reconstruct LCS]
    I --> J[Return Result]
```

---

## Complexity Requirements

- **Target Time Complexity:** O(m * n)
- **Target Space Complexity:** O(m * n) for tabulation
- **Optimization:** Can be optimized to O(min(m, n)) space
- **Justification:** Must compare each character pair

---

## Additional Notes

- Classic string DP problem
- Different from longest common substring (must be contiguous)
- Can be optimized for space using rolling array
- Multiple LCS solutions may exist (implementation returns one)

---

## Related Concepts

- Dynamic Programming
- String Algorithms
- Subsequence vs Substring
- Edit Distance (related problem)
- Sequence Alignment

---

## Testing Hints

1. Test with simple examples first
2. Verify LCS is actually a subsequence of both strings
3. Test edge cases (empty strings, no common chars)
4. Test with strings of different lengths
5. Test with repeated characters

---

## Success Criteria

Your solution should:
- [ ] Find LCS length correctly
- [ ] Reconstruct LCS string correctly
- [ ] Use dynamic programming approach
- [ ] Handle all edge cases
- [ ] Include comprehensive docstrings
- [ ] Have proper type hints
- [ ] Include example usage in main()

