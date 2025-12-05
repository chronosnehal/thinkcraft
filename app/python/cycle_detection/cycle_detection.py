#!/usr/bin/env python3
"""
Cycle Detection - Solution Implementation

Description: Detect cycles in directed and undirected graphs using DFS.
A cycle exists if there's a path from a vertex back to itself.

Time Complexity: O(V + E) - where V is vertices, E is edges
Space Complexity: O(V) - for visited sets and recursion stack

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


def has_cycle_directed(graph: Dict[int, List[int]]) -> bool:
    """
    Detect cycles in directed graph using DFS with recursion stack.
    
    Args:
        graph: Directed adjacency list {vertex: [neighbors]}
    
    Returns:
        True if cycle exists, False otherwise
    
    Time Complexity: O(V + E)
    Space Complexity: O(V)
    
    Examples:
        >>> has_cycle_directed({0: [1], 1: [2], 2: [0]})
        True
    """
    visited: Set[int] = set()
    rec_stack: Set[int] = set()
    
    def dfs(vertex: int) -> bool:
        visited.add(vertex)
        rec_stack.add(vertex)
        
        for neighbor in graph.get(vertex, []):
            if neighbor not in visited:
                if dfs(neighbor):
                    return True
            elif neighbor in rec_stack:
                return True
        
        rec_stack.remove(vertex)
        return False
    
    # Check all components
    for vertex in graph:
        if vertex not in visited:
            if dfs(vertex):
                return True
    
    return False


def has_cycle_undirected(graph: Dict[int, List[int]]) -> bool:
    """
    Detect cycles in undirected graph using DFS with parent tracking.
    
    Args:
        graph: Undirected adjacency list {vertex: [neighbors]}
    
    Returns:
        True if cycle exists, False otherwise
    
    Time Complexity: O(V + E)
    Space Complexity: O(V)
    
    Examples:
        >>> has_cycle_undirected({0: [1], 1: [0, 2], 2: [1]})
        True
    """
    visited: Set[int] = set()
    
    def dfs(vertex: int, parent: Optional[int] = None) -> bool:
        visited.add(vertex)
        
        for neighbor in graph.get(vertex, []):
            if neighbor not in visited:
                if dfs(neighbor, vertex):
                    return True
            elif neighbor != parent:
                return True
        
        return False
    
    # Check all components
    for vertex in graph:
        if vertex not in visited:
            if dfs(vertex):
                return True
    
    return False


def main():
    """Main function to demonstrate cycle detection."""
    print("=" * 70)
    print("Cycle Detection - Solution")
    print("=" * 70)
    
    # Example 1: Directed graph with cycle
    print("\n--- Example 1: Directed Graph with Cycle ---")
    try:
        graph = {
            0: [1],
            1: [2],
            2: [0]  # Cycle: 0 -> 1 -> 2 -> 0
        }
        result = has_cycle_directed(graph)
        print(f"Graph: {graph}")
        print(f"Has cycle: {result}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Example 2: Directed graph without cycle
    print("\n--- Example 2: Directed Graph without Cycle ---")
    try:
        graph = {
            0: [1],
            1: [2],
            2: []
        }
        result = has_cycle_directed(graph)
        print(f"Graph: {graph}")
        print(f"Has cycle: {result}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 3: Undirected graph with cycle
    print("\n--- Example 3: Undirected Graph with Cycle ---")
    try:
        graph = {
            0: [1],
            1: [0, 2],
            2: [1]  # Cycle: 0 - 1 - 2 - 1 (but this is just edges)
        }
        result = has_cycle_undirected(graph)
        print(f"Graph: {graph}")
        print(f"Has cycle: {result}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 4: Undirected graph without cycle (tree)
    print("\n--- Example 4: Undirected Graph without Cycle (Tree) ---")
    try:
        graph = {
            0: [1],
            1: [0, 2],
            2: [1]
        }
        result = has_cycle_undirected(graph)
        print(f"Graph: {graph}")
        print(f"Has cycle: {result}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "=" * 70)
    print("Cycle detection demonstration completed!")
    print("=" * 70)


if __name__ == "__main__":
    main()

