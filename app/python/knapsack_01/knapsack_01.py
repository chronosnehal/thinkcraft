#!/usr/bin/env python3
"""
0/1 Knapsack Problem - Solution Implementation

Description: Solve the 0/1 knapsack problem using dynamic programming.
Given items with weights and values, maximize value without exceeding capacity.

Time Complexity: O(n * capacity) - where n is number of items
Space Complexity: O(n * capacity) - DP table size

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


def knapsack_01(
    weights: List[int],
    values: List[int],
    capacity: int
) -> Tuple[int, List[int]]:
    """
    Solve 0/1 Knapsack problem using dynamic programming.
    
    Args:
        weights: List of item weights
        values: List of item values
        capacity: Maximum weight capacity
    
    Returns:
        Tuple of (maximum value, list of selected item indices)
    
    Raises:
        ValueError: If weights and values have different lengths or invalid inputs
    
    Time Complexity: O(n * capacity)
    Space Complexity: O(n * capacity)
    
    Examples:
        >>> knapsack_01([1, 3, 4, 5], [1, 4, 5, 7], 7)
        (9, [0, 1, 2])
    """
    if len(weights) != len(values):
        raise ValueError("Weights and values must have same length")
    
    if capacity < 0:
        raise ValueError("Capacity must be non-negative")
    
    if not weights:
        return 0, []
    
    n = len(weights)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
    
    # Build DP table
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            if weights[i-1] <= w:
                dp[i][w] = max(
                    dp[i-1][w],
                    dp[i-1][w - weights[i-1]] + values[i-1]
                )
            else:
                dp[i][w] = dp[i-1][w]
    
    # Reconstruct solution
    max_value = dp[n][capacity]
    selected_items = []
    w = capacity
    
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            selected_items.append(i-1)
            w -= weights[i-1]
    
    selected_items.reverse()
    logger.info(f"Maximum value: {max_value}, Selected items: {selected_items}")
    
    return max_value, selected_items


def main():
    """Main function to demonstrate knapsack solution."""
    print("=" * 70)
    print("0/1 Knapsack Problem - Solution")
    print("=" * 70)
    
    # Example 1: Basic case
    print("\n--- Example 1: Basic Case ---")
    try:
        weights = [1, 3, 4, 5]
        values = [1, 4, 5, 7]
        capacity = 7
        max_val, items = knapsack_01(weights, values, capacity)
        print(f"Weights: {weights}")
        print(f"Values: {values}")
        print(f"Capacity: {capacity}")
        print(f"\nMaximum value: {max_val}")
        print(f"Selected items (indices): {items}")
        print(f"Selected weights: {[weights[i] for i in items]}")
        print(f"Selected values: {[values[i] for i in items]}")
        print(f"Total weight: {sum(weights[i] for i in items)}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Example 2: Edge case - empty input
    print("\n--- Example 2: Empty Input ---")
    try:
        max_val, items = knapsack_01([], [], 10)
        print(f"Maximum value: {max_val}, Selected items: {items}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 3: No solution possible
    print("\n--- Example 3: Capacity Too Small ---")
    try:
        weights = [10, 20, 30]
        values = [60, 100, 120]
        capacity = 5
        max_val, items = knapsack_01(weights, values, capacity)
        print(f"Maximum value: {max_val}, Selected items: {items}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "=" * 70)
    print("Knapsack solution demonstration completed!")
    print("=" * 70)


if __name__ == "__main__":
    main()

