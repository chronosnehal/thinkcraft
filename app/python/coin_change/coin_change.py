#!/usr/bin/env python3
"""
Coin Change Problem - Solution Implementation

Description: Find the minimum number of coins needed to make a target amount
using dynamic programming. Each coin denomination can be used unlimited times.

Time Complexity: O(amount * len(coins)) - where amount is target and coins is denominations
Space Complexity: O(amount) - DP array size

Dependencies: Standard library only
Author: ThinkCraft
"""

from typing import List
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def coin_change(coins: List[int], amount: int) -> int:
    """
    Find minimum coins needed for amount.
    
    Args:
        coins: List of coin denominations (positive integers)
        amount: Target amount (non-negative integer)
    
    Returns:
        Minimum number of coins, or -1 if impossible
    
    Raises:
        ValueError: If coins contain non-positive values or amount is negative
    
    Time Complexity: O(amount * len(coins))
    Space Complexity: O(amount)
    
    Examples:
        >>> coin_change([1, 3, 4], 6)
        2
    """
    if amount < 0:
        raise ValueError("Amount must be non-negative")
    
    if amount == 0:
        return 0
    
    if not coins:
        return -1
    
    # Validate coins
    for coin in coins:
        if coin <= 0:
            raise ValueError("All coins must be positive integers")
    
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] = min(dp[i], dp[i - coin] + 1)
    
    result = dp[amount] if dp[amount] != float('inf') else -1
    logger.info(f"Minimum coins for amount {amount}: {result}")
    
    return result


def main():
    """Main function to demonstrate coin change solution."""
    print("=" * 70)
    print("Coin Change Problem - Solution")
    print("=" * 70)
    
    # Example 1: Basic case
    print("\n--- Example 1: Basic Case ---")
    try:
        coins = [1, 3, 4]
        amount = 6
        min_coins = coin_change(coins, amount)
        print(f"Coins: {coins}")
        print(f"Amount: {amount}")
        print(f"Minimum coins needed: {min_coins}")
        print("Explanation: 3 + 3 = 6 (2 coins)")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Example 2: Impossible case
    print("\n--- Example 2: Impossible Case ---")
    try:
        coins = [3, 5]
        amount = 7
        min_coins = coin_change(coins, amount)
        print(f"Coins: {coins}")
        print(f"Amount: {amount}")
        print(f"Minimum coins needed: {min_coins}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 3: Amount is 0
    print("\n--- Example 3: Amount is 0 ---")
    try:
        coins = [1, 2, 5]
        amount = 0
        min_coins = coin_change(coins, amount)
        print(f"Coins: {coins}")
        print(f"Amount: {amount}")
        print(f"Minimum coins needed: {min_coins}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 4: Standard US coins
    print("\n--- Example 4: US Coins ---")
    try:
        coins = [1, 5, 10, 25]
        amount = 67
        min_coins = coin_change(coins, amount)
        print(f"Coins: {coins}")
        print(f"Amount: {amount}")
        print(f"Minimum coins needed: {min_coins}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "=" * 70)
    print("Coin change solution demonstration completed!")
    print("=" * 70)


if __name__ == "__main__":
    main()

