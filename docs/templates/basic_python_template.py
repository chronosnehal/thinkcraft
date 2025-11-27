#!/usr/bin/env python3
"""
Basic Python - One-Liners and Pythonic Solutions

This file contains powerful one-liner solutions and Pythonic approaches
for common programming tasks.

Author: chronosnehal
"""

from typing import List, Dict, Any, Set, Tuple
from collections import Counter, defaultdict
from itertools import chain, combinations, groupby
from functools import reduce
import operator


# ============================================================================
# SECTION: [Problem Category - e.g., List Operations]
# ============================================================================

def problem_name_descriptive(data: List[int]) -> Any:
    """
    [Brief description of what this one-liner accomplishes]
    
    Args:
        data: [Description]
    
    Returns:
        [Description]
    
    Time Complexity: O(?)
    Space Complexity: O(?)
    
    Examples:
        >>> problem_name_descriptive([1, 2, 3, 4, 5])
        [expected output]
    """
    # One-liner solution
    return [x * 2 for x in data if x % 2 == 0]


def find_duplicates(lst: List[Any]) -> List[Any]:
    """
    Find all duplicate elements in a list using one-liner.
    
    Args:
        lst: Input list
    
    Returns:
        List of duplicate elements
    
    Time Complexity: O(n)
    Space Complexity: O(n)
    
    Examples:
        >>> find_duplicates([1, 2, 3, 2, 4, 3, 5])
        [2, 3]
    """
    return [item for item, count in Counter(lst).items() if count > 1]


def flatten_list(nested: List[List[Any]]) -> List[Any]:
    """
    Flatten a nested list using one-liner.
    
    Args:
        nested: Nested list structure
    
    Returns:
        Flattened list
    
    Time Complexity: O(n*m) where n is outer list, m is avg inner list size
    Space Complexity: O(n*m)
    
    Examples:
        >>> flatten_list([[1, 2], [3, 4], [5]])
        [1, 2, 3, 4, 5]
    """
    return list(chain.from_iterable(nested))


def remove_duplicates_preserve_order(lst: List[Any]) -> List[Any]:
    """
    Remove duplicates while preserving order using dict.
    
    Args:
        lst: Input list
    
    Returns:
        List without duplicates
    
    Time Complexity: O(n)
    Space Complexity: O(n)
    
    Examples:
        >>> remove_duplicates_preserve_order([1, 2, 3, 2, 4, 1])
        [1, 2, 3, 4]
    """
    return list(dict.fromkeys(lst))


def transpose_matrix(matrix: List[List[Any]]) -> List[Tuple[Any, ...]]:
    """
    Transpose a matrix using zip.
    
    Args:
        matrix: 2D matrix
    
    Returns:
        Transposed matrix
    
    Time Complexity: O(n*m)
    Space Complexity: O(n*m)
    
    Examples:
        >>> transpose_matrix([[1, 2, 3], [4, 5, 6]])
        [(1, 4), (2, 5), (3, 6)]
    """
    return list(zip(*matrix))


def group_by_key(items: List[Dict[str, Any]], key: str) -> Dict[Any, List[Dict]]:
    """
    Group list of dicts by a specific key.
    
    Args:
        items: List of dictionaries
        key: Key to group by
    
    Returns:
        Dictionary with grouped items
    
    Time Complexity: O(n)
    Space Complexity: O(n)
    
    Examples:
        >>> items = [{'type': 'A', 'val': 1}, {'type': 'B', 'val': 2}, {'type': 'A', 'val': 3}]
        >>> group_by_key(items, 'type')
        {'A': [{'type': 'A', 'val': 1}, {'type': 'A', 'val': 3}], 'B': [{'type': 'B', 'val': 2}]}
    """
    result = defaultdict(list)
    [result[item[key]].append(item) for item in items]
    return dict(result)


def merge_dicts(*dicts: Dict) -> Dict:
    """
    Merge multiple dictionaries (Python 3.9+ style).
    
    Args:
        *dicts: Variable number of dictionaries
    
    Returns:
        Merged dictionary
    
    Time Complexity: O(n) where n is total keys
    Space Complexity: O(n)
    
    Examples:
        >>> merge_dicts({'a': 1}, {'b': 2}, {'c': 3})
        {'a': 1, 'b': 2, 'c': 3}
    """
    return {k: v for d in dicts for k, v in d.items()}


def filter_dict(d: Dict[str, Any], keys: Set[str]) -> Dict[str, Any]:
    """
    Filter dictionary by keys.
    
    Args:
        d: Input dictionary
        keys: Keys to keep
    
    Returns:
        Filtered dictionary
    
    Time Complexity: O(n)
    Space Complexity: O(n)
    
    Examples:
        >>> filter_dict({'a': 1, 'b': 2, 'c': 3}, {'a', 'c'})
        {'a': 1, 'c': 3}
    """
    return {k: v for k, v in d.items() if k in keys}


def invert_dict(d: Dict[Any, Any]) -> Dict[Any, Any]:
    """
    Invert dictionary (swap keys and values).
    
    Args:
        d: Input dictionary
    
    Returns:
        Inverted dictionary
    
    Time Complexity: O(n)
    Space Complexity: O(n)
    
    Examples:
        >>> invert_dict({'a': 1, 'b': 2, 'c': 3})
        {1: 'a', 2: 'b', 3: 'c'}
    """
    return {v: k for k, v in d.items()}


def most_common_element(lst: List[Any]) -> Any:
    """
    Find most common element in list.
    
    Args:
        lst: Input list
    
    Returns:
        Most common element
    
    Time Complexity: O(n)
    Space Complexity: O(n)
    
    Examples:
        >>> most_common_element([1, 2, 3, 2, 2, 4])
        2
    """
    return Counter(lst).most_common(1)[0][0]


def all_subsets(lst: List[Any]) -> List[Tuple[Any, ...]]:
    """
    Generate all subsets (power set) of a list.
    
    Args:
        lst: Input list
    
    Returns:
        List of all subsets
    
    Time Complexity: O(2^n)
    Space Complexity: O(2^n)
    
    Examples:
        >>> all_subsets([1, 2, 3])
        [(), (1,), (2,), (3,), (1, 2), (1, 3), (2, 3), (1, 2, 3)]
    """
    return list(chain.from_iterable(combinations(lst, r) for r in range(len(lst) + 1)))


def product_except_self(nums: List[int]) -> List[int]:
    """
    Calculate product of all elements except self using reduce.
    
    Args:
        nums: List of numbers
    
    Returns:
        List of products
    
    Time Complexity: O(n^2)
    Space Complexity: O(n)
    
    Examples:
        >>> product_except_self([1, 2, 3, 4])
        [24, 12, 8, 6]
    """
    return [reduce(operator.mul, nums[:i] + nums[i+1:], 1) for i in range(len(nums))]


def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """
    Split list into chunks of specified size.
    
    Args:
        lst: Input list
        chunk_size: Size of each chunk
    
    Returns:
        List of chunks
    
    Time Complexity: O(n)
    Space Complexity: O(n)
    
    Examples:
        >>> chunk_list([1, 2, 3, 4, 5, 6, 7], 3)
        [[1, 2, 3], [4, 5, 6], [7]]
    """
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def rotate_list(lst: List[Any], k: int) -> List[Any]:
    """
    Rotate list by k positions.
    
    Args:
        lst: Input list
        k: Number of positions to rotate
    
    Returns:
        Rotated list
    
    Time Complexity: O(n)
    Space Complexity: O(n)
    
    Examples:
        >>> rotate_list([1, 2, 3, 4, 5], 2)
        [4, 5, 1, 2, 3]
    """
    k = k % len(lst) if lst else 0
    return lst[-k:] + lst[:-k] if k else lst


def is_palindrome(s: str) -> bool:
    """
    Check if string is palindrome (one-liner).
    
    Args:
        s: Input string
    
    Returns:
        True if palindrome
    
    Time Complexity: O(n)
    Space Complexity: O(n)
    
    Examples:
        >>> is_palindrome("racecar")
        True
        >>> is_palindrome("hello")
        False
    """
    return (cleaned := ''.join(c.lower() for c in s if c.isalnum())) == cleaned[::-1]


def word_frequency(text: str) -> Dict[str, int]:
    """
    Count word frequency in text.
    
    Args:
        text: Input text
    
    Returns:
        Dictionary of word frequencies
    
    Time Complexity: O(n)
    Space Complexity: O(n)
    
    Examples:
        >>> word_frequency("hello world hello")
        {'hello': 2, 'world': 1}
    """
    return dict(Counter(text.lower().split()))


def fibonacci_generator(n: int) -> List[int]:
    """
    Generate first n Fibonacci numbers using list comprehension.
    
    Args:
        n: Number of Fibonacci numbers
    
    Returns:
        List of Fibonacci numbers
    
    Time Complexity: O(n^2) - Not optimal but demonstrates one-liner
    Space Complexity: O(n)
    
    Examples:
        >>> fibonacci_generator(7)
        [0, 1, 1, 2, 3, 5, 8]
    """
    return [0, 1] + [sum((fib := [0, 1] + [sum(fib[-2:]) for _ in range(i-2)])[-2:]) 
                     for i in range(2, n)] if n > 2 else [0, 1][:n]


def main():
    """Demonstrate all one-liner solutions."""
    print("=" * 60)
    print("Basic Python - One-Liners and Pythonic Solutions")
    print("=" * 60)
    
    # Test each function
    print("\n1. Find Duplicates:")
    print(find_duplicates([1, 2, 3, 2, 4, 3, 5]))
    
    print("\n2. Flatten List:")
    print(flatten_list([[1, 2], [3, 4], [5]]))
    
    print("\n3. Remove Duplicates (Preserve Order):")
    print(remove_duplicates_preserve_order([1, 2, 3, 2, 4, 1]))
    
    print("\n4. Transpose Matrix:")
    print(transpose_matrix([[1, 2, 3], [4, 5, 6]]))
    
    print("\n5. Most Common Element:")
    print(most_common_element([1, 2, 3, 2, 2, 4]))
    
    print("\n6. Chunk List:")
    print(chunk_list([1, 2, 3, 4, 5, 6, 7], 3))
    
    print("\n7. Rotate List:")
    print(rotate_list([1, 2, 3, 4, 5], 2))
    
    print("\n8. Is Palindrome:")
    print(is_palindrome("A man a plan a canal Panama"))
    
    print("\n9. Word Frequency:")
    print(word_frequency("hello world hello python world"))
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
