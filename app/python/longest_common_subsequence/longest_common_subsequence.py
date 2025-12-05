#!/usr/bin/env python3
"""
Longest Common Subsequence (LCS) - Solution Implementation

Description: Find the longest common subsequence between two strings using
dynamic programming. A subsequence is a sequence that appears in the same
relative order but not necessarily contiguous.

Time Complexity: O(m * n) - where m and n are string lengths
Space Complexity: O(m * n) - DP table size

Dependencies: Standard library only
Author: ThinkCraft
"""

from typing import Tuple
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def longest_common_subsequence(s1: str, s2: str) -> Tuple[int, str]:
    """
    Find longest common subsequence between two strings.
    
    Args:
        s1: First string
        s2: Second string
    
    Returns:
        Tuple of (LCS length, LCS string)
    
    Raises:
        ValueError: If inputs are invalid
    
    Time Complexity: O(m * n)
    Space Complexity: O(m * n)
    
    Examples:
        >>> longest_common_subsequence("ABCDGH", "AEDFHR")
        (3, "ADH")
    """
    if not isinstance(s1, str) or not isinstance(s2, str):
        raise TypeError("Both inputs must be strings")
    
    m, n = len(s1), len(s2)
    
    if m == 0 or n == 0:
        return 0, ""
    
    dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
    
    # Build DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    # Reconstruct LCS
    lcs_length = dp[m][n]
    lcs = []
    i, j = m, n
    
    while i > 0 and j > 0:
        if s1[i-1] == s2[j-1]:
            lcs.append(s1[i-1])
            i -= 1
            j -= 1
        elif dp[i-1][j] > dp[i][j-1]:
            i -= 1
        else:
            j -= 1
    
    lcs_str = ''.join(reversed(lcs))
    logger.info(f"LCS length: {lcs_length}, LCS: {lcs_str}")
    
    return lcs_length, lcs_str


def main():
    """Main function to demonstrate LCS solution."""
    print("=" * 70)
    print("Longest Common Subsequence - Solution")
    print("=" * 70)
    
    # Example 1: Basic case
    print("\n--- Example 1: Basic Case ---")
    try:
        s1, s2 = "ABCDGH", "AEDFHR"
        length, lcs = longest_common_subsequence(s1, s2)
        print(f"String 1: {s1}")
        print(f"String 2: {s2}")
        print(f"LCS length: {length}")
        print(f"LCS: {lcs}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Example 2: No common subsequence
    print("\n--- Example 2: No Common Subsequence ---")
    try:
        s1, s2 = "ABC", "XYZ"
        length, lcs = longest_common_subsequence(s1, s2)
        print(f"String 1: {s1}")
        print(f"String 2: {s2}")
        print(f"LCS length: {length}, LCS: '{lcs}'")
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 3: Identical strings
    print("\n--- Example 3: Identical Strings ---")
    try:
        s1, s2 = "ABCD", "ABCD"
        length, lcs = longest_common_subsequence(s1, s2)
        print(f"String 1: {s1}")
        print(f"String 2: {s2}")
        print(f"LCS length: {length}, LCS: '{lcs}'")
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 4: Empty strings
    print("\n--- Example 4: Empty Strings ---")
    try:
        s1, s2 = "", "ABC"
        length, lcs = longest_common_subsequence(s1, s2)
        print(f"String 1: '{s1}'")
        print(f"String 2: '{s2}'")
        print(f"LCS length: {length}, LCS: '{lcs}'")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "=" * 70)
    print("LCS solution demonstration completed!")
    print("=" * 70)


if __name__ == "__main__":
    main()

