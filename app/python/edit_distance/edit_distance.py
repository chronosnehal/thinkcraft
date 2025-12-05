#!/usr/bin/env python3
"""
Edit Distance (Levenshtein Distance) - Solution Implementation

Description: Compute the minimum number of single-character edits (insertions,
deletions, or substitutions) required to transform one string into another.

Time Complexity: O(m * n) - where m and n are string lengths
Space Complexity: O(m * n) - DP table size

Dependencies: Standard library only
Author: ThinkCraft
"""

import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def edit_distance(s1: str, s2: str) -> int:
    """
    Compute Levenshtein edit distance between two strings.
    
    Args:
        s1: First string
        s2: Second string
    
    Returns:
        Minimum edit distance (number of operations needed)
    
    Raises:
        TypeError: If inputs are not strings
    
    Time Complexity: O(m * n)
    Space Complexity: O(m * n)
    
    Examples:
        >>> edit_distance("kitten", "sitting")
        3
    """
    if not isinstance(s1, str) or not isinstance(s2, str):
        raise TypeError("Both inputs must be strings")
    
    m, n = len(s1), len(s2)
    
    # Base cases
    if m == 0:
        return n
    if n == 0:
        return m
    
    dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
    
    # Initialize base cases
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    
    # Fill DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(
                    dp[i-1][j],      # Delete
                    dp[i][j-1],      # Insert
                    dp[i-1][j-1]     # Replace
                )
    
    distance = dp[m][n]
    logger.info(f"Edit distance between '{s1}' and '{s2}': {distance}")
    
    return distance


def main():
    """Main function to demonstrate edit distance solution."""
    print("=" * 70)
    print("Edit Distance (Levenshtein) - Solution")
    print("=" * 70)
    
    # Example 1: Basic case
    print("\n--- Example 1: Basic Case ---")
    try:
        s1, s2 = "kitten", "sitting"
        distance = edit_distance(s1, s2)
        print(f"String 1: {s1}")
        print(f"String 2: {s2}")
        print(f"Edit distance: {distance}")
        print("Operations: k->s (substitute), e->i (substitute), add g")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Example 2: Identical strings
    print("\n--- Example 2: Identical Strings ---")
    try:
        s1, s2 = "abc", "abc"
        distance = edit_distance(s1, s2)
        print(f"String 1: {s1}")
        print(f"String 2: {s2}")
        print(f"Edit distance: {distance}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 3: Empty strings
    print("\n--- Example 3: Empty Strings ---")
    try:
        s1, s2 = "", "abc"
        distance = edit_distance(s1, s2)
        print(f"String 1: '{s1}'")
        print(f"String 2: '{s2}'")
        print(f"Edit distance: {distance} (insert all characters)")
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 4: Completely different
    print("\n--- Example 4: Completely Different ---")
    try:
        s1, s2 = "abc", "xyz"
        distance = edit_distance(s1, s2)
        print(f"String 1: {s1}")
        print(f"String 2: {s2}")
        print(f"Edit distance: {distance} (replace all)")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "=" * 70)
    print("Edit distance solution demonstration completed!")
    print("=" * 70)


if __name__ == "__main__":
    main()

