#!/usr/bin/env python3
"""
Fibonacci Sequence - Solution Implementation

Description: Compute the nth Fibonacci number using dynamic programming
with memoization. Demonstrates optimization of recursive algorithms.

Time Complexity: O(n) - with memoization
Space Complexity: O(n) - for memoization table

Dependencies: Standard library only (functools.lru_cache)
Author: ThinkCraft
"""

from functools import lru_cache
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@lru_cache(maxsize=None)
def fibonacci(n: int) -> int:
    """
    Compute nth Fibonacci number using memoization.
    
    Args:
        n: Index of Fibonacci number (0-indexed)
    
    Returns:
        nth Fibonacci number
    
    Raises:
        ValueError: If n is negative
    
    Time Complexity: O(n) with memoization
    Space Complexity: O(n) for memoization
    
    Examples:
        >>> fibonacci(10)
        55
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    
    if n <= 1:
        return n
    
    result = fibonacci(n-1) + fibonacci(n-2)
    logger.debug(f"Fibonacci({n}) = {result}")
    
    return result


def fibonacci_iterative(n: int) -> int:
    """
    Compute nth Fibonacci number iteratively (space-optimized).
    
    Args:
        n: Index of Fibonacci number
    
    Returns:
        nth Fibonacci number
    
    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    
    if n <= 1:
        return n
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    
    return b


def main():
    """Main function to demonstrate Fibonacci solution."""
    print("=" * 70)
    print("Fibonacci Sequence - Solution")
    print("=" * 70)
    
    # Example 1: Basic case
    print("\n--- Example 1: Basic Case (Memoized) ---")
    try:
        n = 10
        fib_n = fibonacci(n)
        print(f"Fibonacci({n}) = {fib_n}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Example 2: First few numbers
    print("\n--- Example 2: First 10 Fibonacci Numbers ---")
    try:
        print("Fibonacci sequence (0-9):")
        for i in range(10):
            print(f"  F({i}) = {fibonacci(i)}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 3: Large number (iterative)
    print("\n--- Example 3: Large Number (Iterative) ---")
    try:
        n = 50
        fib_n = fibonacci_iterative(n)
        print(f"Fibonacci({n}) = {fib_n}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 4: Edge cases
    print("\n--- Example 4: Edge Cases ---")
    try:
        print(f"Fibonacci(0) = {fibonacci(0)}")
        print(f"Fibonacci(1) = {fibonacci(1)}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "=" * 70)
    print("Fibonacci solution demonstration completed!")
    print("=" * 70)


if __name__ == "__main__":
    main()

