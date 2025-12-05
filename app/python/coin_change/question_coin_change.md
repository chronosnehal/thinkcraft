# Coin Change Problem

**Difficulty:** Medium-Advanced  
**Time to Solve:** 25-30 min  
**Category:** Advanced Python

---

## Problem Description

Find the minimum number of coins needed to make a target amount using dynamic programming. Each coin denomination can be used unlimited times (unbounded knapsack variant).

This problem demonstrates understanding of:
- Dynamic programming with 1D array
- Unbounded knapsack pattern
- Optimization problems

---

## Input Specification

- **Type:** `List[int]`, `int`
- **Format:**
  - `coins`: List of coin denominations (positive integers)
  - `amount`: Target amount (non-negative integer)
- **Constraints:**
  - `1 ≤ len(coins) ≤ 12`
  - `1 ≤ coins[i] ≤ 2^31 - 1`
  - `0 ≤ amount ≤ 10^4`
  - Coins can be used unlimited times

---

## Output Specification

- **Type:** `int`
- **Format:**
  - Minimum number of coins needed
  - Return -1 if amount cannot be made
- **Requirements:**
  - Return 0 if amount is 0
  - Return -1 if impossible

---

## Examples

### Example 1: Basic Case
**Input:**
```python
coins = [1, 3, 4]
amount = 6
```

**Output:**
```python
2
```

**Explanation:**  
Use 2 coins: 3 + 3 = 6 (minimum possible)

---

### Example 2: Impossible Case
**Input:**
```python
coins = [3, 5]
amount = 7
```

**Output:**
```python
-1
```

**Explanation:**  
Cannot make 7 with coins 3 and 5.

---

### Example 3: Amount is 0
**Input:**
```python
coins = [1, 2, 5]
amount = 0
```

**Output:**
```python
0
```

**Explanation:**  
No coins needed for amount 0.

---

## Edge Cases to Consider

1. **Amount is 0:**
   - Expected behavior: Return 0

2. **Impossible to make amount:**
   - Expected behavior: Return -1

3. **Single coin:**
   - Expected behavior: Return amount/coin if divisible, else -1

4. **Coin value greater than amount:**
   - Expected behavior: Skip that coin

---

## Constraints

- Must use dynamic programming
- Must handle impossible cases
- Coins can be used unlimited times

---

## Solution Approach

### Dynamic Programming Strategy

1. **State Definition**: `dp[i]` = minimum coins needed to make amount `i`
2. **Base Case**: `dp[0] = 0` (0 coins for amount 0)
3. **Recurrence Relation**: `dp[i] = min(dp[i], dp[i - coin] + 1)` for each coin
4. **Initialization**: `dp[i] = infinity` for all i > 0

### Algorithm Flow

```mermaid
graph TD
    A[Start] --> B[Initialize dp array]
    B --> C[Set dp[0] = 0]
    C --> D[For each coin]
    D --> E[For each amount >= coin]
    E --> F[Update dp[amount] = min]
    F --> G{More amounts?}
    G -->|Yes| E
    G -->|No| H{More coins?}
    H -->|Yes| D
    H -->|No| I[Return dp[target]]
```

---

## Complexity Requirements

- **Target Time Complexity:** O(amount * len(coins))
- **Target Space Complexity:** O(amount)
- **Justification:** Must consider each coin for each possible amount

---

## Additional Notes

- Classic DP problem (unbounded knapsack variant)
- Greedy algorithm doesn't work for arbitrary coin systems
- Can be extended to return actual coins used
- Used in vending machines, currency exchange

---

## Related Concepts

- Dynamic Programming
- Unbounded Knapsack
- Optimization Problems
- Greedy Algorithms (when applicable)

---

## Testing Hints

1. Test with simple examples first
2. Verify with known coin systems (US coins)
3. Test edge cases (amount 0, impossible)
4. Test with single coin
5. Test with coins larger than amount

---

## Success Criteria

Your solution should:
- [ ] Find minimum coins correctly
- [ ] Use dynamic programming approach
- [ ] Handle impossible cases (return -1)
- [ ] Handle amount 0 (return 0)
- [ ] Include comprehensive docstrings
- [ ] Have proper type hints
- [ ] Include example usage in main()

