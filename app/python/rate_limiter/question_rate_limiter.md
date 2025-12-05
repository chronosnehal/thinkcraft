# Rate Limiter

**Difficulty:** Medium-Advanced  
**Time to Solve:** 25-30 min  
**Category:** Advanced Python

---

## Problem Description

Implement a comprehensive rate limiting system with multiple algorithms. The system should support:

- **Token Bucket**: Token-based rate limiting
- **Sliding Window**: Sliding window rate limiting
- **Fixed Window**: Fixed time window rate limiting
- **Leaky Bucket**: Leaky bucket algorithm
- **Per-user limiting**: Rate limit per user/identifier
- **Thread-safe**: Support concurrent access

This demonstrates advanced understanding of algorithms, data structures, and concurrency patterns for API rate limiting.

---

## Input Specification

- **Type:** User identifier, request count, time window
- **Format:** 
  - `is_allowed(user_id, count=1)`: Check if request is allowed
  - `allow(user_id, count=1)`: Record request and check if allowed
- **Constraints:**
  - Rate limit > 0
  - Time window > 0
  - User ID must be hashable

---

## Output Specification

- **Type:** Boolean
- **Format:** 
  - `True` if request allowed, `False` if rate limit exceeded
- **Requirements:**
  - Must track requests per user
  - Must respect rate limits
  - Must be thread-safe

---

## Examples

### Example 1: Token Bucket
**Input:**
```python
limiter = TokenBucketRateLimiter(rate=5, capacity=10)
limiter.allow("user1")  # True
limiter.allow("user1")  # True
# ... 5 times total
limiter.allow("user1")  # False (rate limit exceeded)
```

**Output:**
```python
True, True, ..., False
```

---

## Edge Cases to Consider

1. **Burst requests:**
   - Expected behavior: Handle according to algorithm

2. **Concurrent requests:**
   - Expected behavior: Thread-safe handling

3. **Time window boundaries:**
   - Expected behavior: Reset appropriately

---

## Constraints

- Must support at least 3 rate limiting algorithms
- Must be thread-safe
- Must handle time-based windows correctly
- Must support per-user limiting

---

## Solution Approach

1. **Token Bucket**: Maintain token count, refill at rate
2. **Sliding Window**: Track requests in time windows
3. **Fixed Window**: Count requests in fixed time windows
4. **Thread Safety**: Use locks for concurrent access

---

## Complexity Requirements

- **Time Complexity:** O(1) average for allow/check operations
- **Space Complexity:** O(n) where n is number of users

---

## Success Criteria

Your solution should:
- [ ] Implement multiple rate limiting algorithms
- [ ] Support per-user limiting
- [ ] Be thread-safe
- [ ] Handle edge cases
- [ ] Maintain O(1) operations
- [ ] Include comprehensive docstrings

