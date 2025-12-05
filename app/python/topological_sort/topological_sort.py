#!/usr/bin/env python3
"""
Topological Sort - Solution Implementation

Description: Perform topological sorting on a directed acyclic graph (DAG).
Topological sort orders vertices such that for every directed edge (u, v),
vertex u comes before v in the ordering.

Time Complexity: O(V + E) - where V is vertices, E is edges
Space Complexity: O(V) - for in-degree tracking and queue

Dependencies: Standard library only (collections.deque)
Author: ThinkCraft
"""

from typing import Dict, List
from collections import deque, defaultdict
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def topological_sort(graph: Dict[int, List[int]]) -> List[int]:
    """
    Perform topological sort using Kahn's algorithm.
    
    Args:
        graph: Directed adjacency list {vertex: [neighbors]}
    
    Returns:
        List of vertices in topological order
    
    Raises:
        ValueError: If graph contains cycles (not a DAG)
    
    Time Complexity: O(V + E)
    Space Complexity: O(V)
    
    Examples:
        >>> graph = {0: [1, 2], 1: [3], 2: [3], 3: []}
        >>> topological_sort(graph)
        [0, 1, 2, 3] or [0, 2, 1, 3]
    """
    # Calculate in-degrees
    in_degree = defaultdict(int)
    vertices = set()
    
    # Collect all vertices
    for u in graph:
        vertices.add(u)
        for v in graph[u]:
            vertices.add(v)
            in_degree[v] += 1
    
    # Initialize in-degrees for vertices with no incoming edges
    for v in vertices:
        if v not in in_degree:
            in_degree[v] = 0
    
    # Find vertices with no incoming edges
    queue = deque([v for v in vertices if in_degree[v] == 0])
    result = []
    
    while queue:
        vertex = queue.popleft()
        result.append(vertex)
        
        # Process neighbors
        for neighbor in graph.get(vertex, []):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Check for cycles
    if len(result) != len(vertices):
        raise ValueError("Graph contains cycles, cannot perform topological sort")
    
    logger.info(f"Topological order: {result}")
    return result


def main():
    """Main function to demonstrate topological sort."""
    print("=" * 70)
    print("Topological Sort - Solution")
    print("=" * 70)
    
    # Example 1: Basic DAG
    print("\n--- Example 1: Basic DAG ---")
    try:
        graph = {
            0: [1, 2],
            1: [3],
            2: [3],
            3: []
        }
        result = topological_sort(graph)
        print(f"Graph: {graph}")
        print(f"Topological order: {result}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Example 2: Linear DAG
    print("\n--- Example 2: Linear DAG ---")
    try:
        graph = {
            0: [1],
            1: [2],
            2: [3],
            3: []
        }
        result = topological_sort(graph)
        print(f"Graph: {graph}")
        print(f"Topological order: {result}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 3: Graph with cycle
    print("\n--- Example 3: Graph with Cycle ---")
    try:
        graph = {
            0: [1],
            1: [2],
            2: [0]  # Cycle!
        }
        result = topological_sort(graph)
        print(f"Graph: {graph}")
        print(f"Topological order: {result}")
    except ValueError as e:
        print(f"Expected error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 4: Multiple valid orders
    print("\n--- Example 4: Multiple Valid Orders ---")
    try:
        graph = {
            0: [1, 2],
            1: [3],
            2: [3],
            3: [4],
            4: []
        }
        result = topological_sort(graph)
        print(f"Graph: {graph}")
        print(f"Topological order: {result}")
        print("Note: Multiple valid orders exist (e.g., [0,1,2,3,4] or [0,2,1,3,4])")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "=" * 70)
    print("Topological sort demonstration completed!")
    print("=" * 70)


if __name__ == "__main__":
    main()

