#!/usr/bin/env python3
"""
Caching System - Solution Implementation

Description: Comprehensive caching system with LRU, LFU, FIFO eviction
policies and TTL support.

Time Complexity: O(1) average for get/put operations
Space Complexity: O(capacity) for cache storage

Dependencies: Standard library only (collections, threading, time)
Author: ThinkCraft
"""

from typing import Any, Optional, Dict
from collections import OrderedDict, defaultdict
from threading import Lock
import time
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class LRUCache:
    """
    Least Recently Used (LRU) Cache implementation.
    
    Evicts least recently used items when capacity is reached.
    
    Attributes:
        capacity: Maximum number of items
        cache: Dictionary storing key-value pairs
        access_order: OrderedDict tracking access order
        lock: Thread lock for thread safety
    """
    
    def __init__(self, capacity: int, ttl: Optional[float] = None):
        """
        Initialize LRU cache.
        
        Args:
            capacity: Maximum cache size
            ttl: Time-to-live in seconds (None for no expiration)
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        
        self.capacity = capacity
        self.cache: Dict[Any, tuple] = {}
        self.access_order = OrderedDict()
        self.ttl = ttl
        self.lock = Lock()
        
        logger.info(f"Initialized LRU cache with capacity {capacity}")
    
    def get(self, key: Any) -> Optional[Any]:
        """
        Get value from cache.
        
        Args:
            key: Cache key
        
        Returns:
            Cached value or None if not found/expired
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        with self.lock:
            if key not in self.cache:
                return None
            
            value, timestamp = self.cache[key]
            
            # Check expiration
            if self.ttl and time.time() - timestamp > self.ttl:
                del self.cache[key]
                del self.access_order[key]
                return None
            
            # Move to end (most recently used)
            self.access_order.move_to_end(key)
            
            return value
    
    def put(self, key: Any, value: Any) -> Optional[tuple]:
        """
        Put value into cache.
        
        Args:
            key: Cache key
            value: Cache value
        
        Returns:
            Evicted (key, value) if cache was full, None otherwise
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        with self.lock:
            evicted = None
            
            # If key exists, update it
            if key in self.cache:
                self.cache[key] = (value, time.time())
                self.access_order.move_to_end(key)
                return None
            
            # If at capacity, evict LRU
            if len(self.cache) >= self.capacity:
                lru_key = next(iter(self.access_order))
                evicted = (lru_key, self.cache[lru_key][0])
                del self.cache[lru_key]
                del self.access_order[lru_key]
            
            # Add new item
            self.cache[key] = (value, time.time())
            self.access_order[key] = None
            
            return evicted
    
    def remove(self, key: Any) -> bool:
        """
        Remove key from cache.
        
        Args:
            key: Cache key
        
        Returns:
            True if removed, False if not found
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        with self.lock:
            if key in self.cache:
                del self.cache[key]
                del self.access_order[key]
                return True
            return False
    
    def clear(self) -> None:
        """Clear all cache entries."""
        with self.lock:
            self.cache.clear()
            self.access_order.clear()
    
    def size(self) -> int:
        """Get current cache size."""
        return len(self.cache)


class LFUCache:
    """
    Least Frequently Used (LFU) Cache implementation.
    
    Evicts least frequently used items when capacity is reached.
    """
    
    def __init__(self, capacity: int, ttl: Optional[float] = None):
        """Initialize LFU cache."""
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        
        self.capacity = capacity
        self.cache: Dict[Any, tuple] = {}
        self.frequency: Dict[Any, int] = defaultdict(int)
        self.freq_buckets: Dict[int, OrderedDict] = defaultdict(OrderedDict)
        self.min_freq = 0
        self.ttl = ttl
        self.lock = Lock()
    
    def get(self, key: Any) -> Optional[Any]:
        """Get value from cache."""
        with self.lock:
            if key not in self.cache:
                return None
            
            value, timestamp = self.cache[key]
            
            # Check expiration
            if self.ttl and time.time() - timestamp > self.ttl:
                self._remove_key(key)
                return None
            
            # Update frequency
            freq = self.frequency[key]
            self.frequency[key] = freq + 1
            
            # Move to new frequency bucket
            del self.freq_buckets[freq][key]
            if not self.freq_buckets[freq] and freq == self.min_freq:
                self.min_freq += 1
            
            self.freq_buckets[freq + 1][key] = None
            
            return value
    
    def put(self, key: Any, value: Any) -> Optional[tuple]:
        """Put value into cache."""
        with self.lock:
            evicted = None
            
            if key in self.cache:
                self.cache[key] = (value, time.time())
                self.get(key)  # Update frequency
                return None
            
            if len(self.cache) >= self.capacity:
                # Evict LFU
                lfu_key = next(iter(self.freq_buckets[self.min_freq]))
                evicted = (lfu_key, self.cache[lfu_key][0])
                self._remove_key(lfu_key)
            
            # Add new item
            self.cache[key] = (value, time.time())
            self.frequency[key] = 1
            self.freq_buckets[1][key] = None
            self.min_freq = 1
            
            return evicted
    
    def _remove_key(self, key: Any) -> None:
        """Remove key from cache."""
        freq = self.frequency[key]
        del self.cache[key]
        del self.frequency[key]
        del self.freq_buckets[freq][key]
    
    def remove(self, key: Any) -> bool:
        """Remove key from cache."""
        with self.lock:
            if key in self.cache:
                self._remove_key(key)
                return True
            return False


class FIFOCache:
    """
    First In First Out (FIFO) Cache implementation.
    
    Evicts oldest items when capacity is reached.
    """
    
    def __init__(self, capacity: int, ttl: Optional[float] = None):
        """Initialize FIFO cache."""
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        
        self.capacity = capacity
        self.cache: Dict[Any, tuple] = {}
        self.queue = []
        self.ttl = ttl
        self.lock = Lock()
    
    def get(self, key: Any) -> Optional[Any]:
        """Get value from cache."""
        with self.lock:
            if key not in self.cache:
                return None
            
            value, timestamp = self.cache[key]
            
            if self.ttl and time.time() - timestamp > self.ttl:
                self.remove(key)
                return None
            
            return value
    
    def put(self, key: Any, value: Any) -> Optional[tuple]:
        """Put value into cache."""
        with self.lock:
            evicted = None
            
            if key in self.cache:
                self.cache[key] = (value, time.time())
                return None
            
            if len(self.cache) >= self.capacity:
                # Evict oldest (first in queue)
                oldest_key = self.queue.pop(0)
                evicted = (oldest_key, self.cache[oldest_key][0])
                del self.cache[oldest_key]
            
            self.cache[key] = (value, time.time())
            self.queue.append(key)
            
            return evicted
    
    def remove(self, key: Any) -> bool:
        """Remove key from cache."""
        with self.lock:
            if key in self.cache:
                del self.cache[key]
                self.queue.remove(key)
                return True
            return False


def main():
    """Main function to demonstrate caching systems."""
    print("=" * 70)
    print("Caching System - Solution")
    print("=" * 70)
    
    # Example 1: LRU Cache
    print("\n--- Example 1: LRU Cache ---")
    try:
        cache = LRUCache(capacity=3)
        cache.put(1, "a")
        cache.put(2, "b")
        cache.put(3, "c")
        print(f"After adding 1,2,3: {[cache.get(k) for k in [1,2,3]]}")
        
        cache.get(1)  # Access 1
        cache.put(4, "d")  # Should evict 2
        print(f"After accessing 1 and adding 4:")
        print(f"  get(1): {cache.get(1)}")
        print(f"  get(2): {cache.get(2)}")  # Should be None
        print(f"  get(3): {cache.get(3)}")
        print(f"  get(4): {cache.get(4)}")
        
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 2: LFU Cache
    print("\n--- Example 2: LFU Cache ---")
    try:
        cache = LFUCache(capacity=3)
        cache.put(1, "a")
        cache.put(2, "b")
        cache.get(1)  # Access 1 twice
        cache.get(1)
        cache.put(3, "c")
        cache.put(4, "d")  # Should evict 2 (least frequently used)
        print(f"After operations:")
        print(f"  get(1): {cache.get(1)}")
        print(f"  get(2): {cache.get(2)}")  # Should be None
        print(f"  get(3): {cache.get(3)}")
        print(f"  get(4): {cache.get(4)}")
        
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 3: FIFO Cache
    print("\n--- Example 3: FIFO Cache ---")
    try:
        cache = FIFOCache(capacity=3)
        cache.put(1, "a")
        cache.put(2, "b")
        cache.put(3, "c")
        cache.get(1)  # Access doesn't change order
        cache.put(4, "d")  # Should evict 1 (oldest)
        print(f"After operations:")
        print(f"  get(1): {cache.get(1)}")  # Should be None
        print(f"  get(2): {cache.get(2)}")
        print(f"  get(3): {cache.get(3)}")
        print(f"  get(4): {cache.get(4)}")
        
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 4: TTL Cache
    print("\n--- Example 4: TTL Cache ---")
    try:
        cache = LRUCache(capacity=3, ttl=1.0)  # 1 second TTL
        cache.put(1, "a")
        print(f"Immediately: get(1) = {cache.get(1)}")
        time.sleep(1.1)
        print(f"After 1.1s: get(1) = {cache.get(1)}")  # Should be None
        
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "=" * 70)
    print("Caching system demonstration completed!")
    print("=" * 70)


if __name__ == "__main__":
    main()

