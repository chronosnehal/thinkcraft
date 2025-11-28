#!/usr/bin/env python3
"""
Quick Sort Implementation - Solution Implementation

Description: Comprehensive quicksort system implementing multiple sorting
scenarios including standard quicksort, randomized quicksort, three-way partition,
custom comparator sorting, and kth smallest element finding.

Time Complexity: O(n log n) average, O(n²) worst case (standard)
Space Complexity: O(log n) for recursion stack

Dependencies: Standard library only (random for randomized version)
Author: chronosnehal
Date: 2025-11-27
"""

from typing import List, Any, Callable, Optional
import random
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class QuickSort:
    """
    Comprehensive quicksort implementation with multiple variations.
    
    This class provides methods for various quicksort scenarios:
    - Standard quicksort
    - Randomized quicksort
    - Three-way partition quicksort
    - Custom comparator sorting
    - Finding kth smallest element
    
    Attributes:
        None (stateless class)
    """
    
    @staticmethod
    def _validate_array(arr: List[Any]) -> None:
        """
        Validate that array is non-empty.
        
        Args:
            arr: Array to validate
        
        Raises:
            ValueError: If array is empty
            TypeError: If arr is not a list
        """
        if not isinstance(arr, list):
            raise TypeError("Input must be a list")
        
        if len(arr) == 0:
            raise ValueError("Array cannot be empty")
    
    @staticmethod
    def _partition(arr: List[int], low: int, high: int) -> int:
        """
        Partition array using Lomuto partition scheme.
        
        Places pivot at correct position and returns its index.
        Elements < pivot are on left, elements > pivot are on right.
        
        Args:
            arr: Array to partition
            low: Starting index
            high: Ending index
        
        Returns:
            Index of pivot after partitioning
        
        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        # Choose rightmost element as pivot
        pivot = arr[high]
        
        # Index of smaller element (indicates right position of pivot)
        i = low - 1
        
        for j in range(low, high):
            # If current element is smaller than or equal to pivot
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        
        # Place pivot at correct position
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1
    
    @staticmethod
    def _randomized_partition(arr: List[int], low: int, high: int) -> int:
        """
        Partition with random pivot selection.
        
        Args:
            arr: Array to partition
            low: Starting index
            high: Ending index
        
        Returns:
            Index of pivot after partitioning
        
        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        # Randomly select pivot and swap with last element
        random_index = random.randint(low, high)
        arr[random_index], arr[high] = arr[high], arr[random_index]
        
        return QuickSort._partition(arr, low, high)
    
    @staticmethod
    def _three_way_partition(arr: List[int], low: int, high: int) -> tuple[int, int]:
        """
        Three-way partition (Dutch National Flag algorithm).
        
        Partitions array into three groups: < pivot, = pivot, > pivot.
        
        Args:
            arr: Array to partition
            low: Starting index
            high: Ending index
        
        Returns:
            Tuple of (left boundary, right boundary) for equal elements
        
        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        pivot = arr[low]
        lt = low  # Less than pivot
        i = low   # Current element
        gt = high # Greater than pivot
        
        while i <= gt:
            if arr[i] < pivot:
                arr[lt], arr[i] = arr[i], arr[lt]
                lt += 1
                i += 1
            elif arr[i] > pivot:
                arr[i], arr[gt] = arr[gt], arr[i]
                gt -= 1
            else:
                i += 1
        
        return lt, gt
    
    @staticmethod
    def sort(arr: List[int]) -> List[int]:
        """
        Standard quicksort implementation (in-place).
        
        Args:
            arr: Array of integers to sort
        
        Returns:
            Sorted array (same reference, modified in-place)
        
        Raises:
            ValueError: If array is empty
            TypeError: If arr is not a list
        
        Time Complexity: O(n log n) average, O(n²) worst case
        Space Complexity: O(log n) for recursion stack
        
        Examples:
            >>> QuickSort.sort([64, 34, 25, 12, 22, 11, 90])
            [11, 12, 22, 25, 34, 64, 90]
        """
        QuickSort._validate_array(arr)
        
        if len(arr) == 1:
            return arr
        
        def _quicksort(low: int, high: int) -> None:
            """Internal recursive quicksort function."""
            if low < high:
                # Partition and get pivot index
                pi = QuickSort._partition(arr, low, high)
                
                # Recursively sort elements before and after partition
                _quicksort(low, pi - 1)
                _quicksort(pi + 1, high)
        
        _quicksort(0, len(arr) - 1)
        logger.info(f"Array sorted: {len(arr)} elements")
        return arr
    
    @staticmethod
    def randomized_sort(arr: List[int]) -> List[int]:
        """
        Randomized quicksort (in-place) with random pivot selection.
        
        Uses random pivot to avoid worst-case O(n²) performance.
        
        Args:
            arr: Array of integers to sort
        
        Returns:
            Sorted array (same reference, modified in-place)
        
        Raises:
            ValueError: If array is empty
            TypeError: If arr is not a list
        
        Time Complexity: O(n log n) average (better worst-case guarantee)
        Space Complexity: O(log n) for recursion stack
        
        Examples:
            >>> QuickSort.randomized_sort([5, 2, 8, 1, 9, 3])
            [1, 2, 3, 5, 8, 9]
        """
        QuickSort._validate_array(arr)
        
        if len(arr) == 1:
            return arr
        
        def _randomized_quicksort(low: int, high: int) -> None:
            """Internal recursive randomized quicksort function."""
            if low < high:
                # Use randomized partition
                pi = QuickSort._randomized_partition(arr, low, high)
                
                _randomized_quicksort(low, pi - 1)
                _randomized_quicksort(pi + 1, high)
        
        _randomized_quicksort(0, len(arr) - 1)
        logger.info(f"Array sorted with randomized quicksort: {len(arr)} elements")
        return arr
    
    @staticmethod
    def three_way_sort(arr: List[int]) -> List[int]:
        """
        Three-way partition quicksort (in-place) for arrays with many duplicates.
        
        Efficiently handles arrays with many duplicate values using Dutch
        National Flag algorithm.
        
        Args:
            arr: Array of integers to sort (may contain duplicates)
        
        Returns:
            Sorted array (same reference, modified in-place)
        
        Raises:
            ValueError: If array is empty
            TypeError: If arr is not a list
        
        Time Complexity: O(n log n) average, O(n) best case (all equal)
        Space Complexity: O(log n) for recursion stack
        
        Examples:
            >>> QuickSort.three_way_sort([2, 1, 2, 1, 2, 1, 2])
            [1, 1, 1, 2, 2, 2, 2]
        """
        QuickSort._validate_array(arr)
        
        if len(arr) == 1:
            return arr
        
        def _three_way_quicksort(low: int, high: int) -> None:
            """Internal recursive three-way quicksort function."""
            if low < high:
                lt, gt = QuickSort._three_way_partition(arr, low, high)
                
                # Recursively sort elements less than and greater than pivot
                # Elements equal to pivot are already in correct position
                _three_way_quicksort(low, lt - 1)
                _three_way_quicksort(gt + 1, high)
        
        _three_way_quicksort(0, len(arr) - 1)
        logger.info(f"Array sorted with three-way quicksort: {len(arr)} elements")
        return arr
    
    @staticmethod
    def sort_with_comparator(
        arr: List[Any],
        comparator: Callable[[Any, Any], int]
    ) -> List[Any]:
        """
        Quicksort with custom comparator function.
        
        Args:
            arr: Array of elements to sort
            comparator: Function that takes two elements and returns:
                       -1 if first < second, 0 if equal, 1 if first > second
        
        Returns:
            Sorted array (same reference, modified in-place)
        
        Raises:
            ValueError: If array is empty
            TypeError: If arr is not a list or comparator is not callable
        
        Time Complexity: O(n log n) average
        Space Complexity: O(log n) for recursion stack
        
        Examples:
            >>> arr = [("apple", 3), ("banana", 2), ("cherry", 5)]
            >>> comp = lambda a, b: -1 if a[1] < b[1] else (1 if a[1] > b[1] else 0)
            >>> QuickSort.sort_with_comparator(arr, comp)
            [("banana", 2), ("apple", 3), ("cherry", 5)]
        """
        QuickSort._validate_array(arr)
        
        if not callable(comparator):
            raise TypeError("Comparator must be a callable function")
        
        if len(arr) == 1:
            return arr
        
        def _partition_custom(low: int, high: int) -> int:
            """Partition using custom comparator."""
            pivot = arr[high]
            i = low - 1
            
            for j in range(low, high):
                if comparator(arr[j], pivot) <= 0:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
            
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            return i + 1
        
        def _quicksort_custom(low: int, high: int) -> None:
            """Internal recursive quicksort with custom comparator."""
            if low < high:
                pi = _partition_custom(low, high)
                _quicksort_custom(low, pi - 1)
                _quicksort_custom(pi + 1, high)
        
        _quicksort_custom(0, len(arr) - 1)
        logger.info(f"Array sorted with custom comparator: {len(arr)} elements")
        return arr
    
    @staticmethod
    def find_kth_smallest(arr: List[int], k: int) -> int:
        """
        Find kth smallest element using quicksort partition.
        
        Uses quickselect algorithm (modified quicksort) to find kth smallest
        element without fully sorting the array.
        
        Args:
            arr: Array of integers
            k: Position (1-indexed, so k=1 means smallest element)
        
        Returns:
            The kth smallest element
        
        Raises:
            ValueError: If array is empty or k is out of range
            TypeError: If arr is not a list or k is not an integer
        
        Time Complexity: O(n) average, O(n²) worst case
        Space Complexity: O(log n) for recursion stack
        
        Examples:
            >>> QuickSort.find_kth_smallest([7, 10, 4, 3, 20, 15], 3)
            7
        """
        QuickSort._validate_array(arr)
        
        if not isinstance(k, int):
            raise TypeError("k must be an integer")
        
        if k < 1 or k > len(arr):
            raise ValueError(f"k must be between 1 and {len(arr)}, got {k}")
        
        # Create a copy to avoid modifying original array
        arr_copy = arr.copy()
        
        def _quickselect(low: int, high: int, k_pos: int) -> int:
            """Internal quickselect function."""
            if low == high:
                return arr_copy[low]
            
            # Partition and get pivot index
            pi = QuickSort._partition(arr_copy, low, high)
            
            # Position of pivot (0-indexed)
            pivot_pos = pi - low
            
            if pivot_pos == k_pos - 1:
                return arr_copy[pi]
            elif pivot_pos > k_pos - 1:
                # kth smallest is in left partition
                return _quickselect(low, pi - 1, k_pos)
            else:
                # kth smallest is in right partition
                return _quickselect(pi + 1, high, k_pos - pivot_pos - 1)
        
        result = _quickselect(0, len(arr_copy) - 1, k)
        logger.info(f"Kth smallest element (k={k}): {result}")
        return result


def main():
    """Demonstrate quicksort variations with examples."""
    print("=" * 80)
    print("Quick Sort Variations - Examples")
    print("=" * 80)
    
    # Example 1: Standard Quick Sort
    print("\n" + "-" * 80)
    print("Example 1: Standard Quick Sort")
    print("-" * 80)
    
    arr1 = [64, 34, 25, 12, 22, 11, 90]
    print(f"Original: {arr1}")
    result1 = QuickSort.sort(arr1.copy())
    print(f"Sorted:   {result1}")
    print(f"✓ Sorted correctly: {result1 == sorted(arr1)}")
    
    # Example 2: Randomized Quick Sort
    print("\n" + "-" * 80)
    print("Example 2: Randomized Quick Sort")
    print("-" * 80)
    
    arr2 = [5, 2, 8, 1, 9, 3]
    print(f"Original: {arr2}")
    result2 = QuickSort.randomized_sort(arr2.copy())
    print(f"Sorted:   {result2}")
    print(f"✓ Sorted correctly: {result2 == sorted(arr2)}")
    
    # Example 3: Three-Way Partition
    print("\n" + "-" * 80)
    print("Example 3: Three-Way Partition (Many Duplicates)")
    print("-" * 80)
    
    arr3 = [2, 1, 2, 1, 2, 1, 2]
    print(f"Original: {arr3}")
    result3 = QuickSort.three_way_sort(arr3.copy())
    print(f"Sorted:   {result3}")
    print(f"✓ Sorted correctly: {result3 == sorted(arr3)}")
    
    # Example 4: Custom Comparator
    print("\n" + "-" * 80)
    print("Example 4: Custom Comparator Sort")
    print("-" * 80)
    
    arr4 = [("apple", 3), ("banana", 2), ("cherry", 5), ("date", 1)]
    print(f"Original: {arr4}")
    comparator = lambda a, b: -1 if a[1] < b[1] else (1 if a[1] > b[1] else 0)
    result4 = QuickSort.sort_with_comparator(arr4.copy(), comparator)
    print(f"Sorted by count: {result4}")
    print(f"✓ Sorted correctly: {result4 == sorted(arr4, key=lambda x: x[1])}")
    
    # Example 5: Kth Smallest Element
    print("\n" + "-" * 80)
    print("Example 5: Kth Smallest Element")
    print("-" * 80)
    
    arr5 = [7, 10, 4, 3, 20, 15]
    k = 3
    print(f"Array: {arr5}")
    print(f"k: {k}")
    result5 = QuickSort.find_kth_smallest(arr5.copy(), k)
    print(f"Kth smallest: {result5}")
    sorted_arr5 = sorted(arr5)
    print(f"✓ Correct: {result5 == sorted_arr5[k-1]} (sorted array: {sorted_arr5})")
    
    # Example 6: Edge Case - Already Sorted
    print("\n" + "-" * 80)
    print("Example 6: Edge Case - Already Sorted Array")
    print("-" * 80)
    
    arr6 = [1, 2, 3, 4, 5]
    print(f"Original: {arr6}")
    result6 = QuickSort.sort(arr6.copy())
    print(f"Sorted:   {result6}")
    print(f"✓ Sorted correctly: {result6 == arr6}")
    
    # Example 7: Edge Case - Reverse Sorted
    print("\n" + "-" * 80)
    print("Example 7: Edge Case - Reverse Sorted Array")
    print("-" * 80)
    
    arr7 = [5, 4, 3, 2, 1]
    print(f"Original: {arr7}")
    result7 = QuickSort.randomized_sort(arr7.copy())
    print(f"Sorted:   {result7}")
    print(f"✓ Sorted correctly: {result7 == sorted(arr7)}")
    
    # Example 8: Edge Case - All Identical
    print("\n" + "-" * 80)
    print("Example 8: Edge Case - All Elements Identical")
    print("-" * 80)
    
    arr8 = [5, 5, 5, 5, 5]
    print(f"Original: {arr8}")
    result8 = QuickSort.three_way_sort(arr8.copy())
    print(f"Sorted:   {result8}")
    print(f"✓ Sorted correctly: {result8 == arr8}")
    
    # Example 9: Edge Case - Single Element
    print("\n" + "-" * 80)
    print("Example 9: Edge Case - Single Element")
    print("-" * 80)
    
    arr9 = [42]
    print(f"Original: {arr9}")
    result9 = QuickSort.sort(arr9.copy())
    print(f"Sorted:   {result9}")
    print(f"✓ Sorted correctly: {result9 == arr9}")
    
    # Example 10: Error Case - Empty Array
    print("\n" + "-" * 80)
    print("Example 10: Error Case - Empty Array")
    print("-" * 80)
    
    try:
        result10 = QuickSort.sort([])
        print(f"Result: {result10}")
    except ValueError as e:
        print(f"✓ Caught expected error: {e}")
    
    # Example 11: Error Case - Invalid k
    print("\n" + "-" * 80)
    print("Example 11: Error Case - Invalid k for Kth Smallest")
    print("-" * 80)
    
    try:
        result11 = QuickSort.find_kth_smallest([1, 2, 3], 5)
        print(f"Result: {result11}")
    except ValueError as e:
        print(f"✓ Caught expected error: {e}")
    
    print("\n" + "=" * 80)
    print("Examples completed!")
    print("=" * 80)


if __name__ == "__main__":
    main()

