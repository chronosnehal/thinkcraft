#!/usr/bin/env python3
"""
DFS Traversal - Solution Implementation

Description: Implement Depth-First Search (DFS) traversal for graphs.
DFS explores as far as possible along each branch before backtracking.

Time Complexity: O(V + E) - where V is vertices, E is edges
Space Complexity: O(V) - for recursion stack and visited set

Dependencies: Standard library only
Author: ThinkCraft
"""

from typing import Dict, List, Set, Optional
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def dfs_traversal_recursive(
    graph: Dict[int, List[int]],
    start: int,
    visited: Optional[Set[int]] = None
) -> List[int]:
    """
    Perform DFS traversal recursively starting from given vertex.
    
    Args:
        graph: Adjacency list representation {vertex: [neighbors]}
        start: Starting vertex
        visited: Set of visited vertices (for recursion)
    
    Returns:
        List of vertices visited in DFS order
    
    Raises:
        ValueError: If start vertex not in graph
    
    Time Complexity: O(V + E)
    Space Complexity: O(V) for recursion stack
    
    Examples:
        >>> graph = {0: [1, 2], 1: [0, 3], 2: [0], 3: [1]}
        >>> dfs_traversal_recursive(graph, 0)
        [0, 1, 3, 2]
    """
    if start not in graph:
        raise ValueError(f"Start vertex {start} not in graph")
    
    if visited is None:
        visited = set()
    
    result = []
    
    def dfs_helper(vertex: int):
        visited.add(vertex)
        result.append(vertex)
        
        for neighbor in graph.get(vertex, []):
            if neighbor not in visited:
                dfs_helper(neighbor)
    
    dfs_helper(start)
    logger.info(f"DFS traversal from {start}: {result}")
    return result


def dfs_traversal_iterative(
    graph: Dict[int, List[int]],
    start: int
) -> List[int]:
    """
    Perform DFS traversal iteratively using stack.
    
    Args:
        graph: Adjacency list representation
        start: Starting vertex
    
    Returns:
        List of vertices visited in DFS order
    
    Time Complexity: O(V + E)
    Space Complexity: O(V)
    """
    if start not in graph:
        raise ValueError(f"Start vertex {start} not in graph")
    
    visited = []
    stack = [start]
    seen: Set[int] = {start}
    
    while stack:
        vertex = stack.pop()
        visited.append(vertex)
        
        # Process neighbors in reverse to maintain order
        for neighbor in reversed(graph.get(vertex, [])):
            if neighbor not in seen:
                seen.add(neighbor)
                stack.append(neighbor)
    
    return visited


def main():
    """Main function to demonstrate DFS traversal."""
    print("=" * 70)
    print("DFS Traversal - Solution")
    print("=" * 70)
    
    # Example 1: Basic DFS (recursive)
    print("\n--- Example 1: Basic DFS (Recursive) ---")
    try:
        graph = {
            0: [1, 2],
            1: [0, 3, 4],
            2: [0, 5],
            3: [1],
            4: [1],
            5: [2]
        }
        result = dfs_traversal_recursive(graph, 0)
        print(f"Graph: {graph}")
        print(f"DFS from vertex 0 (recursive): {result}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Example 2: DFS (iterative)
    print("\n--- Example 2: DFS (Iterative) ---")
    try:
        graph = {
            0: [1, 2],
            1: [0, 3],
            2: [0, 4],
            3: [1],
            4: [2]
        }
        result = dfs_traversal_iterative(graph, 0)
        print(f"Graph: {graph}")
        print(f"DFS from vertex 0 (iterative): {result}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 3: Disconnected graph
    print("\n--- Example 3: Disconnected Graph ---")
    try:
        graph = {
            0: [1],
            1: [0],
            2: [3],
            3: [2]
        }
        result = dfs_traversal_recursive(graph, 0)
        print(f"Graph: {graph}")
        print(f"DFS from vertex 0: {result}")
        print("Note: Only connected component starting from 0 is traversed")
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 4: Single vertex
    print("\n--- Example 4: Single Vertex ---")
    try:
        graph = {0: []}
        result = dfs_traversal_recursive(graph, 0)
        print(f"Graph: {graph}")
        print(f"DFS from vertex 0: {result}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "=" * 70)
    print("DFS traversal demonstration completed!")
    print("=" * 70)


if __name__ == "__main__":
    main()

