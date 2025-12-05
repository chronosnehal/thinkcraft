#!/usr/bin/env python3
"""
Rate Limiter - Solution Implementation

Description: Comprehensive rate limiting system with multiple algorithms
including token bucket, sliding window, and fixed window.

Time Complexity: O(1) average for allow/check operations
Space Complexity: O(n) where n is number of users

Dependencies: Standard library only (collections, threading, time)
Author: ThinkCraft
"""

from typing import Any, Dict, Deque
from collections import deque, defaultdict
from threading import Lock
import time
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TokenBucketRateLimiter:
    """
    Token Bucket rate limiter implementation.
    
    Maintains a bucket of tokens that refill at a constant rate.
    Requests consume tokens, and are rejected if bucket is empty.
    """
    
    def __init__(self, rate: float, capacity: int):
        """
        Initialize token bucket rate limiter.
        
        Args:
            rate: Tokens per second
            capacity: Maximum bucket capacity
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        self.rate = rate
        self.capacity = capacity
        self.tokens: Dict[Any, float] = defaultdict(lambda: capacity)
        self.last_update: Dict[Any, float] = defaultdict(time.time)
        self.lock = Lock()
    
    def allow(self, user_id: Any, tokens: int = 1) -> bool:
        """
        Check if request is allowed and consume tokens.
        
        Args:
            user_id: User identifier
            tokens: Number of tokens to consume
        
        Returns:
            True if allowed, False otherwise
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        with self.lock:
            now = time.time()
            last = self.last_update[user_id]
            
            # Refill tokens based on elapsed time
            elapsed = now - last
            self.tokens[user_id] = min(
                self.capacity,
                self.tokens[user_id] + elapsed * self.rate
            )
            self.last_update[user_id] = now
            
            # Check if enough tokens
            if self.tokens[user_id] >= tokens:
                self.tokens[user_id] -= tokens
                return True
            
            return False
    
    def is_allowed(self, user_id: Any, tokens: int = 1) -> bool:
        """Check if request would be allowed without consuming tokens."""
        with self.lock:
            now = time.time()
            last = self.last_update.get(user_id, now)
            
            tokens_available = min(
                self.capacity,
                self.tokens.get(user_id, self.capacity) + (now - last) * self.rate
            )
            
            return tokens_available >= tokens


class SlidingWindowRateLimiter:
    """
    Sliding Window rate limiter implementation.
    
    Tracks requests in a sliding time window.
    """
    
    def __init__(self, max_requests: int, window_seconds: float):
        """
        Initialize sliding window rate limiter.
        
        Args:
            max_requests: Maximum requests allowed
            window_seconds: Time window in seconds
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[Any, Deque] = defaultdict(deque)
        self.lock = Lock()
    
    def allow(self, user_id: Any, count: int = 1) -> bool:
        """
        Check if request is allowed.
        
        Args:
            user_id: User identifier
            count: Number of requests
        
        Returns:
            True if allowed, False otherwise
        """
        with self.lock:
            now = time.time()
            user_requests = self.requests[user_id]
            
            # Remove old requests outside window
            while user_requests and user_requests[0] < now - self.window_seconds:
                user_requests.popleft()
            
            # Check if within limit
            if len(user_requests) + count <= self.max_requests:
                for _ in range(count):
                    user_requests.append(now)
                return True
            
            return False
    
    def is_allowed(self, user_id: Any, count: int = 1) -> bool:
        """Check if request would be allowed."""
        with self.lock:
            now = time.time()
            user_requests = self.requests.get(user_id, deque())
            
            # Remove old requests
            while user_requests and user_requests[0] < now - self.window_seconds:
                user_requests.popleft()
            
            return len(user_requests) + count <= self.max_requests


class FixedWindowRateLimiter:
    """
    Fixed Window rate limiter implementation.
    
    Counts requests in fixed time windows.
    """
    
    def __init__(self, max_requests: int, window_seconds: float):
        """
        Initialize fixed window rate limiter.
        
        Args:
            max_requests: Maximum requests per window
            window_seconds: Window size in seconds
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.counts: Dict[Any, int] = defaultdict(int)
        self.window_start: Dict[Any, float] = defaultdict(time.time)
        self.lock = Lock()
    
    def allow(self, user_id: Any, count: int = 1) -> bool:
        """
        Check if request is allowed.
        
        Args:
            user_id: User identifier
            count: Number of requests
        
        Returns:
            True if allowed, False otherwise
        """
        with self.lock:
            now = time.time()
            window_start = self.window_start[user_id]
            
            # Reset window if expired
            if now - window_start >= self.window_seconds:
                self.counts[user_id] = 0
                self.window_start[user_id] = now
            
            # Check limit
            if self.counts[user_id] + count <= self.max_requests:
                self.counts[user_id] += count
                return True
            
            return False
    
    def is_allowed(self, user_id: Any, count: int = 1) -> bool:
        """Check if request would be allowed."""
        with self.lock:
            now = time.time()
            window_start = self.window_start.get(user_id, now)
            
            if now - window_start >= self.window_seconds:
                return count <= self.max_requests
            
            return self.counts.get(user_id, 0) + count <= self.max_requests


class LeakyBucketRateLimiter:
    """
    Leaky Bucket rate limiter implementation.
    
    Requests are added to a bucket that leaks at a constant rate.
    """
    
    def __init__(self, capacity: int, leak_rate: float):
        """
        Initialize leaky bucket rate limiter.
        
        Args:
            capacity: Maximum bucket capacity
            leak_rate: Leak rate (requests per second)
        """
        self.capacity = capacity
        self.leak_rate = leak_rate
        self.buckets: Dict[Any, float] = defaultdict(float)
        self.last_leak: Dict[Any, float] = defaultdict(time.time)
        self.lock = Lock()
    
    def allow(self, user_id: Any, count: int = 1) -> bool:
        """
        Check if request is allowed.
        
        Args:
            user_id: User identifier
            count: Number of requests
        
        Returns:
            True if allowed, False otherwise
        """
        with self.lock:
            now = time.time()
            last = self.last_leak[user_id]
            
            # Leak bucket
            elapsed = now - last
            self.buckets[user_id] = max(
                0,
                self.buckets[user_id] - elapsed * self.leak_rate
            )
            self.last_leak[user_id] = now
            
            # Check capacity
            if self.buckets[user_id] + count <= self.capacity:
                self.buckets[user_id] += count
                return True
            
            return False


def main():
    """Main function to demonstrate rate limiting."""
    print("=" * 70)
    print("Rate Limiter - Solution")
    print("=" * 70)
    
    # Example 1: Token Bucket
    print("\n--- Example 1: Token Bucket ---")
    try:
        limiter = TokenBucketRateLimiter(rate=2.0, capacity=5)
        print("Rate: 2 tokens/sec, Capacity: 5")
        for i in range(7):
            allowed = limiter.allow("user1")
            print(f"Request {i+1}: {'Allowed' if allowed else 'Denied'}")
            time.sleep(0.1)
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 2: Sliding Window
    print("\n--- Example 2: Sliding Window ---")
    try:
        limiter = SlidingWindowRateLimiter(max_requests=5, window_seconds=1.0)
        print("Max: 5 requests, Window: 1 second")
        for i in range(7):
            allowed = limiter.allow("user1")
            print(f"Request {i+1}: {'Allowed' if allowed else 'Denied'}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 3: Fixed Window
    print("\n--- Example 3: Fixed Window ---")
    try:
        limiter = FixedWindowRateLimiter(max_requests=3, window_seconds=2.0)
        print("Max: 3 requests, Window: 2 seconds")
        for i in range(5):
            allowed = limiter.allow("user1")
            print(f"Request {i+1}: {'Allowed' if allowed else 'Denied'}")
        print("Waiting 2 seconds...")
        time.sleep(2.1)
        print("After window reset:")
        for i in range(2):
            allowed = limiter.allow("user1")
            print(f"Request {i+1}: {'Allowed' if allowed else 'Denied'}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "=" * 70)
    print("Rate limiter demonstration completed!")
    print("=" * 70)


if __name__ == "__main__":
    main()

