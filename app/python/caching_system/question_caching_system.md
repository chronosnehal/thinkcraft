# Caching System

**Difficulty:** Medium-Advanced  
**Time to Solve:** 25-30 min  
**Category:** Advanced Python

---

## Problem Description

Implement a comprehensive caching system with multiple eviction policies. The system should support:

- **LRU Cache**: Least Recently Used eviction
- **LFU Cache**: Least Frequently Used eviction
- **FIFO Cache**: First In First Out eviction
- **TTL Cache**: Time-To-Live expiration
- **Thread-safe operations**: Support concurrent access

This demonstrates advanced understanding of data structures, algorithms, and concurrency patterns.

---

## Input Specification

- **Type:** Key-value pairs, cache capacity, TTL (optional)
- **Format:** 
  - `put(key, value, ttl=None)`: Add item to cache
  - `get(key)`: Retrieve item from cache
  - `remove(key)`: Remove item from cache
- **Constraints:**
  - Keys must be hashable
  - Capacity > 0
  - TTL in seconds (if provided)

---

## Output Specification

- **Type:** Cached value or None
- **Format:** 
  - `get(key)` returns value if exists and not expired, None otherwise
  - `put(key, value)` returns evicted key-value if cache full, None otherwise
- **Requirements:**
  - Must respect capacity limits
  - Must handle expiration
  - Must be thread-safe

---

## Examples

### Example 1: LRU Cache
**Input:**
```python
cache = LRUCache(capacity=3)
cache.put(1, "a")
cache.put(2, "b")
cache.put(3, "c")
cache.get(1)  # Access 1, makes it recently used
cache.put(4, "d")  # Evicts 2 (least recently used)
```

**Output:**
```python
cache.get(2)  # None (evicted)
cache.get(1)  # "a" (still in cache)
```

---

## Edge Cases to Consider

1. **Cache at capacity:**
   - Expected behavior: Evict according to policy

2. **Expired items:**
   - Expected behavior: Return None, remove from cache

3. **Concurrent access:**
   - Expected behavior: Thread-safe operations

---

## Constraints

- Must support at least 3 eviction policies
- Must handle TTL expiration
- Must be thread-safe
- Must maintain O(1) average time complexity for get/put

---

## Solution Approach

1. **Data Structures**: Use hash map + doubly linked list for LRU
2. **Eviction**: Implement policy-specific eviction logic
3. **TTL**: Track expiration times and clean expired items
4. **Thread Safety**: Use locks for concurrent access

---

## Complexity Requirements

- **Time Complexity:** O(1) average for get/put operations
- **Space Complexity:** O(capacity) for cache storage

---

## Success Criteria

Your solution should:
- [ ] Implement LRU, LFU, FIFO caches
- [ ] Support TTL expiration
- [ ] Be thread-safe
- [ ] Handle edge cases
- [ ] Maintain O(1) operations
- [ ] Include comprehensive docstrings

