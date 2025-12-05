#!/usr/bin/env python3
"""
Connected Components - Solution Implementation

Description: Find all connected components in an undirected graph using DFS.
A connected component is a maximal set of vertices where there's a path
between any two vertices.

Time Complexity: O(V + E) - where V is vertices, E is edges
Space Complexity: O(V) - for visited set and recursion stack

Dependencies: Standard library only
Author: ThinkCraft
"""

from typing import Dict, List, Set
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def connected_components(graph: Dict[int, List[int]]) -> List[List[int]]:
    """
    Find all connected components in undirected graph.
    
    Args:
        graph: Undirected adjacency list {vertex: [neighbors]}
    
    Returns:
        List of components, each component is a list of vertices
    
    Time Complexity: O(V + E)
    Space Complexity: O(V)
    
    Examples:
        >>> graph = {0: [1], 1: [0], 2: [3], 3: [2]}
        >>> connected_components(graph)
        [[0, 1], [2, 3]]
    """
    visited: Set[int] = set()
    components = []
    
    def dfs(vertex: int, component: List[int]) -> None:
        visited.add(vertex)
        component.append(vertex)
        
        for neighbor in graph.get(vertex, []):
            if neighbor not in visited:
                dfs(neighbor, component)
    
    # Find all components
    for vertex in graph:
        if vertex not in visited:
            component = []
            dfs(vertex, component)
            components.append(component)
    
    logger.info(f"Found {len(components)} connected components")
    return components


def count_components(graph: Dict[int, List[int]]) -> int:
    """
    Count number of connected components.
    
    Args:
        graph: Undirected adjacency list
    
    Returns:
        Number of connected components
    
    Time Complexity: O(V + E)
    Space Complexity: O(V)
    """
    return len(connected_components(graph))


def main():
    """Main function to demonstrate connected components."""
    print("=" * 70)
    print("Connected Components - Solution")
    print("=" * 70)
    
    # Example 1: Multiple components
    print("\n--- Example 1: Multiple Components ---")
    try:
        graph = {
            0: [1],
            1: [0],
            2: [3],
            3: [2],
            4: [5],
            5: [4]
        }
        components = connected_components(graph)
        print(f"Graph: {graph}")
        print(f"Connected components: {components}")
        print(f"Number of components: {len(components)}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Example 2: Single component
    print("\n--- Example 2: Single Component ---")
    try:
        graph = {
            0: [1],
            1: [0, 2],
            2: [1]
        }
        components = connected_components(graph)
        print(f"Graph: {graph}")
        print(f"Connected components: {components}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 3: Isolated vertices
    print("\n--- Example 3: Isolated Vertices ---")
    try:
        graph = {
            0: [],
            1: [],
            2: []
        }
        components = connected_components(graph)
        print(f"Graph: {graph}")
        print(f"Connected components: {components}")
        print("Note: Each isolated vertex is its own component")
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 4: Empty graph
    print("\n--- Example 4: Empty Graph ---")
    try:
        graph = {}
        components = connected_components(graph)
        print(f"Graph: {graph}")
        print(f"Connected components: {components}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "=" * 70)
    print("Connected components demonstration completed!")
    print("=" * 70)


if __name__ == "__main__":
    main()

