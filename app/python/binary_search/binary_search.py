#!/usr/bin/env python3
"""
Binary Search Variations - Solution Implementation

Description: Comprehensive binary search system implementing multiple search
scenarios including standard search, first/last occurrence, insertion point,
rotated array search, and peak element finding.

Time Complexity: O(log n) - Binary search divides search space in half each iteration
Space Complexity: O(1) - Iterative approach uses constant extra space

Dependencies: Standard library only
Author: chronosnehal
Date: 2025-11-27
"""

from typing import List, Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BinarySearch:
    """
    Comprehensive binary search implementation with multiple variations.
    
    This class provides methods for various binary search scenarios:
    - Standard binary search
    - Finding first/last occurrences
    - Finding insertion points
    - Searching in rotated arrays
    - Finding peak elements
    
    Attributes:
        None (stateless class)
    """
    
    @staticmethod
    def _validate_array(arr: List[int]) -> None:
        """
        Validate that array is non-empty and sorted.
        
        Args:
            arr: Array to validate
        
        Raises:
            ValueError: If array is empty or not sorted
            TypeError: If arr is not a list
        """
        if not isinstance(arr, list):
            raise TypeError("Input must be a list")
        
        if len(arr) == 0:
            raise ValueError("Array cannot be empty")
        
        # Check if sorted (ascending)
        for i in range(len(arr) - 1):
            if arr[i] > arr[i + 1]:
                raise ValueError(f"Array is not sorted: element at index {i} > element at index {i+1}")
    
    @staticmethod
    def search(arr: List[int], target: int) -> Optional[int]:
        """
        Standard binary search for exact match.
        
        Args:
            arr: Sorted array of integers (ascending order)
            target: Integer to search for
        
        Returns:
            Index of target if found, None otherwise
        
        Raises:
            ValueError: If array is empty or not sorted
            TypeError: If inputs have wrong types
        
        Time Complexity: O(log n)
        Space Complexity: O(1)
        
        Examples:
            >>> BinarySearch.search([1, 3, 5, 7, 9], 5)
            2
            >>> BinarySearch.search([1, 3, 5, 7, 9], 6)
            None
        """
        BinarySearch._validate_array(arr)
        
        if not isinstance(target, int):
            raise TypeError("Target must be an integer")
        
        left, right = 0, len(arr) - 1
        
        while left <= right:
            # Avoid integer overflow
            mid = left + (right - left) // 2
            
            logger.debug(f"Searching: left={left}, right={right}, mid={mid}, arr[mid]={arr[mid]}")
            
            if arr[mid] == target:
                logger.info(f"Target {target} found at index {mid}")
                return mid
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        
        logger.info(f"Target {target} not found")
        return None
    
    @staticmethod
    def find_first(arr: List[int], target: int) -> Optional[int]:
        """
        Find first occurrence of target in sorted array (may contain duplicates).
        
        Args:
            arr: Sorted array of integers (may contain duplicates)
            target: Integer to search for
        
        Returns:
            Index of first occurrence if found, None otherwise
        
        Raises:
            ValueError: If array is empty or not sorted
            TypeError: If inputs have wrong types
        
        Time Complexity: O(log n)
        Space Complexity: O(1)
        
        Examples:
            >>> BinarySearch.find_first([1, 2, 2, 2, 3], 2)
            1
            >>> BinarySearch.find_first([1, 2, 2, 2, 3], 4)
            None
        """
        BinarySearch._validate_array(arr)
        
        if not isinstance(target, int):
            raise TypeError("Target must be an integer")
        
        left, right = 0, len(arr) - 1
        result = None
        
        while left <= right:
            mid = left + (right - left) // 2
            
            if arr[mid] == target:
                result = mid
                # Continue searching left half for first occurrence
                right = mid - 1
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        
        if result is not None:
            logger.info(f"First occurrence of {target} found at index {result}")
        else:
            logger.info(f"Target {target} not found")
        
        return result
    
    @staticmethod
    def find_last(arr: List[int], target: int) -> Optional[int]:
        """
        Find last occurrence of target in sorted array (may contain duplicates).
        
        Args:
            arr: Sorted array of integers (may contain duplicates)
            target: Integer to search for
        
        Returns:
            Index of last occurrence if found, None otherwise
        
        Raises:
            ValueError: If array is empty or not sorted
            TypeError: If inputs have wrong types
        
        Time Complexity: O(log n)
        Space Complexity: O(1)
        
        Examples:
            >>> BinarySearch.find_last([1, 2, 2, 2, 3], 2)
            3
            >>> BinarySearch.find_last([1, 2, 2, 2, 3], 4)
            None
        """
        BinarySearch._validate_array(arr)
        
        if not isinstance(target, int):
            raise TypeError("Target must be an integer")
        
        left, right = 0, len(arr) - 1
        result = None
        
        while left <= right:
            mid = left + (right - left) // 2
            
            if arr[mid] == target:
                result = mid
                # Continue searching right half for last occurrence
                left = mid + 1
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        
        if result is not None:
            logger.info(f"Last occurrence of {target} found at index {result}")
        else:
            logger.info(f"Target {target} not found")
        
        return result
    
    @staticmethod
    def find_insertion_point(arr: List[int], target: int) -> int:
        """
        Find insertion point for target to maintain sorted order.
        
        Args:
            arr: Sorted array of integers
            target: Integer to insert
        
        Returns:
            Index where target should be inserted
        
        Raises:
            ValueError: If array is empty or not sorted
            TypeError: If inputs have wrong types
        
        Time Complexity: O(log n)
        Space Complexity: O(1)
        
        Examples:
            >>> BinarySearch.find_insertion_point([1, 3, 5, 7], 4)
            2
            >>> BinarySearch.find_insertion_point([1, 3, 5, 7], 0)
            0
            >>> BinarySearch.find_insertion_point([1, 3, 5, 7], 10)
            4
        """
        BinarySearch._validate_array(arr)
        
        if not isinstance(target, int):
            raise TypeError("Target must be an integer")
        
        left, right = 0, len(arr)
        
        while left < right:
            mid = left + (right - left) // 2
            
            if arr[mid] < target:
                left = mid + 1
            else:
                right = mid
        
        logger.info(f"Insertion point for {target} is at index {left}")
        return left
    
    @staticmethod
    def search_rotated(arr: List[int], target: int) -> Optional[int]:
        """
        Search for target in rotated sorted array.
        
        Args:
            arr: Rotated sorted array (originally sorted, then rotated)
            target: Integer to search for
        
        Returns:
            Index of target if found, None otherwise
        
        Raises:
            ValueError: If array is empty
            TypeError: If inputs have wrong types
        
        Time Complexity: O(log n)
        Space Complexity: O(1)
        
        Examples:
            >>> BinarySearch.search_rotated([4, 5, 6, 7, 0, 1, 2], 0)
            4
            >>> BinarySearch.search_rotated([4, 5, 6, 7, 0, 1, 2], 3)
            None
        """
        if not isinstance(arr, list):
            raise TypeError("Input must be a list")
        
        if len(arr) == 0:
            raise ValueError("Array cannot be empty")
        
        if not isinstance(target, int):
            raise TypeError("Target must be an integer")
        
        left, right = 0, len(arr) - 1
        
        while left <= right:
            mid = left + (right - left) // 2
            
            if arr[mid] == target:
                logger.info(f"Target {target} found at index {mid}")
                return mid
            
            # Determine which half is sorted
            if arr[left] <= arr[mid]:
                # Left half is sorted
                if arr[left] <= target < arr[mid]:
                    right = mid - 1
                else:
                    left = mid + 1
            else:
                # Right half is sorted
                if arr[mid] < target <= arr[right]:
                    left = mid + 1
                else:
                    right = mid - 1
        
        logger.info(f"Target {target} not found in rotated array")
        return None
    
    @staticmethod
    def find_peak(arr: List[int]) -> int:
        """
        Find any peak element in array.
        
        A peak element is greater than its neighbors. For boundary elements,
        compare with only one neighbor.
        
        Args:
            arr: Array of integers (not necessarily sorted)
        
        Returns:
            Index of any peak element
        
        Raises:
            ValueError: If array is empty or has less than 1 element
            TypeError: If arr is not a list
        
        Time Complexity: O(log n)
        Space Complexity: O(1)
        
        Examples:
            >>> BinarySearch.find_peak([1, 2, 3, 1])
            2
            >>> BinarySearch.find_peak([1, 2, 1, 3, 5, 6, 4])
            5
        """
        if not isinstance(arr, list):
            raise TypeError("Input must be a list")
        
        if len(arr) == 0:
            raise ValueError("Array cannot be empty")
        
        if len(arr) == 1:
            return 0
        
        left, right = 0, len(arr) - 1
        
        while left < right:
            mid = left + (right - left) // 2
            
            # Compare with right neighbor
            if arr[mid] > arr[mid + 1]:
                # Peak is in left half (including mid)
                right = mid
            else:
                # Peak is in right half
                left = mid + 1
        
        logger.info(f"Peak element found at index {left} with value {arr[left]}")
        return left


def main():
    """Demonstrate binary search variations with examples."""
    print("=" * 80)
    print("Binary Search Variations - Examples")
    print("=" * 80)
    
    # Example 1: Standard Binary Search
    print("\n" + "-" * 80)
    print("Example 1: Standard Binary Search")
    print("-" * 80)
    
    arr1 = [1, 3, 5, 7, 9, 11, 13]
    target1 = 7
    result1 = BinarySearch.search(arr1, target1)
    print(f"Array: {arr1}")
    print(f"Target: {target1}")
    print(f"Result: Index {result1}")
    print(f"Verification: arr[{result1}] = {arr1[result1] if result1 is not None else 'N/A'}")
    
    # Example 2: First Occurrence
    print("\n" + "-" * 80)
    print("Example 2: First Occurrence")
    print("-" * 80)
    
    arr2 = [1, 2, 2, 2, 3, 4, 5]
    target2 = 2
    result2 = BinarySearch.find_first(arr2, target2)
    print(f"Array: {arr2}")
    print(f"Target: {target2}")
    print(f"Result: First occurrence at index {result2}")
    
    # Example 3: Last Occurrence
    print("\n" + "-" * 80)
    print("Example 3: Last Occurrence")
    print("-" * 80)
    
    arr3 = [1, 2, 2, 2, 3, 4, 5]
    target3 = 2
    result3 = BinarySearch.find_last(arr3, target3)
    print(f"Array: {arr3}")
    print(f"Target: {target3}")
    print(f"Result: Last occurrence at index {result3}")
    
    # Example 4: Insertion Point
    print("\n" + "-" * 80)
    print("Example 4: Insertion Point")
    print("-" * 80)
    
    arr4 = [1, 3, 5, 7, 9]
    target4 = 6
    result4 = BinarySearch.find_insertion_point(arr4, target4)
    print(f"Array: {arr4}")
    print(f"Target: {target4}")
    print(f"Result: Insert at index {result4}")
    print(f"After insertion: {arr4[:result4] + [target4] + arr4[result4:]}")
    
    # Example 5: Rotated Array Search
    print("\n" + "-" * 80)
    print("Example 5: Rotated Array Search")
    print("-" * 80)
    
    arr5 = [4, 5, 6, 7, 0, 1, 2]
    target5 = 0
    result5 = BinarySearch.search_rotated(arr5, target5)
    print(f"Rotated Array: {arr5}")
    print(f"Target: {target5}")
    print(f"Result: Index {result5}")
    
    # Example 6: Peak Element
    print("\n" + "-" * 80)
    print("Example 6: Peak Element")
    print("-" * 80)
    
    arr6 = [1, 2, 3, 1]
    result6 = BinarySearch.find_peak(arr6)
    print(f"Array: {arr6}")
    print(f"Result: Peak at index {result6} (value: {arr6[result6]})")
    
    # Example 7: Edge Case - Target Not Found
    print("\n" + "-" * 80)
    print("Example 7: Edge Case - Target Not Found")
    print("-" * 80)
    
    arr7 = [1, 3, 5, 7, 9]
    target7 = 6
    result7 = BinarySearch.search(arr7, target7)
    print(f"Array: {arr7}")
    print(f"Target: {target7}")
    print(f"Result: {result7}")
    
    # Example 8: Edge Case - Single Element
    print("\n" + "-" * 80)
    print("Example 8: Edge Case - Single Element")
    print("-" * 80)
    
    arr8 = [5]
    target8 = 5
    result8 = BinarySearch.search(arr8, target8)
    print(f"Array: {arr8}")
    print(f"Target: {target8}")
    print(f"Result: Index {result8}")
    
    # Example 9: Error Case - Empty Array
    print("\n" + "-" * 80)
    print("Example 9: Error Case - Empty Array")
    print("-" * 80)
    
    try:
        result9 = BinarySearch.search([], 5)
        print(f"Result: {result9}")
    except ValueError as e:
        print(f"✓ Caught expected error: {e}")
    
    # Example 10: Error Case - Unsorted Array
    print("\n" + "-" * 80)
    print("Example 10: Error Case - Unsorted Array")
    print("-" * 80)
    
    try:
        result10 = BinarySearch.search([3, 1, 2], 2)
        print(f"Result: {result10}")
    except ValueError as e:
        print(f"✓ Caught expected error: {e}")
    
    print("\n" + "=" * 80)
    print("Examples completed!")
    print("=" * 80)


if __name__ == "__main__":
    main()

