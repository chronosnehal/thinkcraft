#!/usr/bin/env python3
"""
Longest Increasing Subsequence (LIS) - Solution Implementation

Description: Find the longest increasing subsequence in an array using
dynamic programming. A subsequence is a sequence derived by deleting some
elements without changing the order.

Time Complexity: O(n²) - where n is array length
Space Complexity: O(n) - DP array size

Dependencies: Standard library only
Author: ThinkCraft
"""

from typing import List, Tuple
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def longest_increasing_subsequence(nums: List[int]) -> Tuple[int, List[int]]:
    """
    Find longest increasing subsequence.
    
    Args:
        nums: List of integers
    
    Returns:
        Tuple of (LIS length, LIS list)
    
    Raises:
        ValueError: If input is invalid
    
    Time Complexity: O(n²)
    Space Complexity: O(n)
    
    Examples:
        >>> longest_increasing_subsequence([10, 9, 2, 5, 3, 7, 101, 18])
        (4, [2, 3, 7, 18])
    """
    if not isinstance(nums, list):
        raise TypeError("Input must be a list")
    
    if not nums:
        return 0, []
    
    n = len(nums)
    dp = [1] * n
    parent = [-1] * n
    
    # Build DP array
    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
                parent[i] = j
    
    # Find maximum length and ending index
    max_length = max(dp)
    end_idx = dp.index(max_length)
    
    # Reconstruct LIS
    lis = []
    idx = end_idx
    while idx != -1:
        lis.append(nums[idx])
        idx = parent[idx]
    
    lis.reverse()
    logger.info(f"LIS length: {max_length}, LIS: {lis}")
    
    return max_length, lis


def main():
    """Main function to demonstrate LIS solution."""
    print("=" * 70)
    print("Longest Increasing Subsequence - Solution")
    print("=" * 70)
    
    # Example 1: Basic case
    print("\n--- Example 1: Basic Case ---")
    try:
        nums = [10, 9, 2, 5, 3, 7, 101, 18]
        length, lis = longest_increasing_subsequence(nums)
        print(f"Array: {nums}")
        print(f"LIS length: {length}")
        print(f"LIS: {lis}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Example 2: Already sorted
    print("\n--- Example 2: Already Sorted ---")
    try:
        nums = [1, 2, 3, 4, 5]
        length, lis = longest_increasing_subsequence(nums)
        print(f"Array: {nums}")
        print(f"LIS length: {length}, LIS: {lis}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 3: Decreasing order
    print("\n--- Example 3: Decreasing Order ---")
    try:
        nums = [5, 4, 3, 2, 1]
        length, lis = longest_increasing_subsequence(nums)
        print(f"Array: {nums}")
        print(f"LIS length: {length}, LIS: {lis}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 4: Empty array
    print("\n--- Example 4: Empty Array ---")
    try:
        nums = []
        length, lis = longest_increasing_subsequence(nums)
        print(f"Array: {nums}")
        print(f"LIS length: {length}, LIS: {lis}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "=" * 70)
    print("LIS solution demonstration completed!")
    print("=" * 70)


if __name__ == "__main__":
    main()

