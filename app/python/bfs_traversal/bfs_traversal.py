#!/usr/bin/env python3
"""
BFS Traversal - Solution Implementation

Description: Implement Breadth-First Search (BFS) traversal for graphs.
BFS explores all vertices at the current depth level before moving to the next level.

Time Complexity: O(V + E) - where V is vertices, E is edges
Space Complexity: O(V) - for queue and visited set

Dependencies: Standard library only (collections.deque)
Author: ThinkCraft
"""

from typing import Dict, List, Set
from collections import deque, defaultdict
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def bfs_traversal(
    graph: Dict[int, List[int]],
    start: int
) -> List[int]:
    """
    Perform BFS traversal starting from given vertex.
    
    Args:
        graph: Adjacency list representation {vertex: [neighbors]}
        start: Starting vertex
    
    Returns:
        List of vertices visited in BFS order
    
    Raises:
        ValueError: If start vertex not in graph
    
    Time Complexity: O(V + E)
    Space Complexity: O(V)
    
    Examples:
        >>> graph = {0: [1, 2], 1: [0, 3], 2: [0], 3: [1]}
        >>> bfs_traversal(graph, 0)
        [0, 1, 2, 3]
    """
    if start not in graph:
        raise ValueError(f"Start vertex {start} not in graph")
    
    visited = []
    queue = deque([start])
    seen: Set[int] = {start}
    
    while queue:
        vertex = queue.popleft()
        visited.append(vertex)
        
        # Process neighbors
        for neighbor in graph.get(vertex, []):
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    
    logger.info(f"BFS traversal from {start}: {visited}")
    return visited


def bfs_level_order(
    graph: Dict[int, List[int]],
    start: int
) -> List[List[int]]:
    """
    Perform BFS and return vertices grouped by level.
    
    Args:
        graph: Adjacency list representation
        start: Starting vertex
    
    Returns:
        List of lists, where each inner list contains vertices at that level
    
    Time Complexity: O(V + E)
    Space Complexity: O(V)
    """
    if start not in graph:
        raise ValueError(f"Start vertex {start} not in graph")
    
    levels = []
    queue = deque([start])
    seen: Set[int] = {start}
    
    while queue:
        level_size = len(queue)
        level = []
        
        for _ in range(level_size):
            vertex = queue.popleft()
            level.append(vertex)
            
            for neighbor in graph.get(vertex, []):
                if neighbor not in seen:
                    seen.add(neighbor)
                    queue.append(neighbor)
        
        levels.append(level)
    
    return levels


def main():
    """Main function to demonstrate BFS traversal."""
    print("=" * 70)
    print("BFS Traversal - Solution")
    print("=" * 70)
    
    # Example 1: Basic BFS
    print("\n--- Example 1: Basic BFS Traversal ---")
    try:
        graph = {
            0: [1, 2],
            1: [0, 3, 4],
            2: [0, 5],
            3: [1],
            4: [1],
            5: [2]
        }
        result = bfs_traversal(graph, 0)
        print(f"Graph: {graph}")
        print(f"BFS from vertex 0: {result}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Example 2: Level-order BFS
    print("\n--- Example 2: Level-Order BFS ---")
    try:
        graph = {
            0: [1, 2],
            1: [0, 3],
            2: [0, 4],
            3: [1],
            4: [2]
        }
        levels = bfs_level_order(graph, 0)
        print(f"Graph: {graph}")
        print("BFS levels:")
        for i, level in enumerate(levels):
            print(f"  Level {i}: {level}")
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
        result = bfs_traversal(graph, 0)
        print(f"Graph: {graph}")
        print(f"BFS from vertex 0: {result}")
        print("Note: Only connected component starting from 0 is traversed")
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 4: Single vertex
    print("\n--- Example 4: Single Vertex ---")
    try:
        graph = {0: []}
        result = bfs_traversal(graph, 0)
        print(f"Graph: {graph}")
        print(f"BFS from vertex 0: {result}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "=" * 70)
    print("BFS traversal demonstration completed!")
    print("=" * 70)


if __name__ == "__main__":
    main()

