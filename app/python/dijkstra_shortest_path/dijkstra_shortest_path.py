#!/usr/bin/env python3
"""
Dijkstra's Shortest Path - Solution Implementation

Description: Find shortest paths from a source vertex to all other vertices
in a weighted graph using Dijkstra's algorithm. Works for graphs with
non-negative edge weights.

Time Complexity: O((V + E) log V) - where V is vertices, E is edges
Space Complexity: O(V) - for distances and priority queue

Dependencies: Standard library only (heapq)
Author: ThinkCraft
"""

from typing import Dict, List, Tuple, Optional, Union
from collections import defaultdict
import heapq
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def dijkstra_shortest_path(
    graph: Dict[int, List[Tuple[int, float]]],
    start: int,
    target: Optional[int] = None
) -> Union[Dict[int, float], Tuple[List[int], float]]:
    """
    Find shortest paths using Dijkstra's algorithm.
    
    Args:
        graph: Weighted adjacency list {vertex: [(neighbor, weight), ...]}
        start: Source vertex
        target: Target vertex (None for all shortest paths)
    
    Returns:
        If target is None: Dictionary of {vertex: shortest_distance}
        If target provided: Tuple of (path, distance) or ([], inf) if no path
    
    Raises:
        ValueError: If graph has negative weights or start not in graph
    
    Time Complexity: O((V + E) log V)
    Space Complexity: O(V)
    
    Examples:
        >>> graph = {0: [(1, 4), (2, 1)], 1: [(3, 1)], 2: [(1, 2), (3, 5)]}
        >>> dijkstra_shortest_path(graph, 0, 3)
        ([0, 2, 1, 3], 4)
    """
    if start not in graph:
        raise ValueError(f"Start vertex {start} not in graph")
    
    # Check for negative weights
    for edges in graph.values():
        for _, weight in edges:
            if weight < 0:
                raise ValueError("Dijkstra's algorithm requires non-negative weights")
    
    distances = defaultdict(lambda: float('inf'))
    distances[start] = 0
    previous = {}
    pq = [(0, start)]
    visited = set()
    
    while pq:
        dist, vertex = heapq.heappop(pq)
        
        if vertex in visited:
            continue
        
        visited.add(vertex)
        
        # If target found, reconstruct path
        if target is not None and vertex == target:
            path = []
            current = target
            while current is not None:
                path.append(current)
                current = previous.get(current)
            return (path[::-1], dist)
        
        # Process neighbors
        for neighbor, weight in graph.get(vertex, []):
            if neighbor in visited:
                continue
            
            new_dist = dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                previous[neighbor] = vertex
                heapq.heappush(pq, (new_dist, neighbor))
    
    if target is not None:
        return ([], float('inf'))  # No path found
    
    return dict(distances)


def main():
    """Main function to demonstrate Dijkstra's algorithm."""
    print("=" * 70)
    print("Dijkstra's Shortest Path - Solution")
    print("=" * 70)
    
    # Example 1: Basic shortest path
    print("\n--- Example 1: Shortest Path to Target ---")
    try:
        graph = {
            0: [(1, 4), (2, 1)],
            1: [(3, 1)],
            2: [(1, 2), (3, 5)],
            3: []
        }
        path, distance = dijkstra_shortest_path(graph, 0, 3)
        print(f"Graph: {graph}")
        print(f"Shortest path from 0 to 3: {path}")
        print(f"Distance: {distance}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Example 2: All shortest paths
    print("\n--- Example 2: All Shortest Paths ---")
    try:
        graph = {
            0: [(1, 4), (2, 1)],
            1: [(3, 1)],
            2: [(1, 2), (3, 5)],
            3: []
        }
        distances = dijkstra_shortest_path(graph, 0)
        print(f"Graph: {graph}")
        print(f"All shortest distances from 0:")
        for vertex, dist in sorted(distances.items()):
            print(f"  To {vertex}: {dist}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 3: No path exists
    print("\n--- Example 3: No Path Exists ---")
    try:
        graph = {
            0: [(1, 1)],
            1: [],
            2: [(3, 1)],
            3: []
        }
        path, distance = dijkstra_shortest_path(graph, 0, 3)
        print(f"Graph: {graph}")
        print(f"Path from 0 to 3: {path}, Distance: {distance}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "=" * 70)
    print("Dijkstra's algorithm demonstration completed!")
    print("=" * 70)


if __name__ == "__main__":
    main()

