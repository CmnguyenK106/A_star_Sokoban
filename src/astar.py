# astar.py
import heapq
from typing import List, Tuple, TypeVar, Generic, Callable, Optional, Set

T = TypeVar('T')

class Node(Generic[T]):
    """Represents a node in the search tree"""
    def __init__(self, state: T, g_score: int, h_score: int, parent: Optional['Node[T]'] = None, action: Optional[str] = None):
        self.state = state
        self.g_score = g_score  # Cost from start
        self.h_score = h_score  # Heuristic estimate to goal
        self.f_score = g_score + h_score  # Total estimated cost
        self.parent = parent
        self.action = action
    
    def __lt__(self, other: 'Node[T]') -> bool:
        """For heap comparison"""
        return self.f_score < other.f_score

class AStar(Generic[T]):
    """Generic A* algorithm implementation"""
    
    def __init__(self,
                 initial_state: T,
                 is_goal: Callable[[T], bool],
                 get_neighbors: Callable[[T], List[Tuple[T, str]]],
                 heuristic: Callable[[T], int],
                 state_key: Callable[[T], tuple] = None,
                 max_depth: int = 1000):
        """
        Initialize A* solver
        
        Args:
            initial_state: Starting state
            is_goal: Function to check if state is goal
            get_neighbors: Function to get (next_state, action) pairs
            heuristic: Function to estimate distance to goal
            state_key: Function to create hashable state identifier (for cycle detection)
            max_depth: Maximum search depth to prevent infinite loops
        """
        self.initial_state = initial_state
        self.is_goal = is_goal
        self.get_neighbors = get_neighbors
        self.heuristic = heuristic
        self.state_key = state_key if state_key else lambda s: s
        self.max_depth = max_depth
        self.nodes_explored = 0
        self.nodes_expanded = 0
    
    def solve(self) -> Optional[List[str]]:
        """
        Solve using A* algorithm
        
        Returns:
            List of actions to reach goal, or None if no solution found
        """
        counter = 0
        initial_h = self.heuristic(self.initial_state)
        start_node = Node(self.initial_state, 0, initial_h)
        
        heap = [(start_node.f_score, counter, start_node)]
        visited: Set[tuple] = set()
        
        while heap:
            _, _, current_node = heapq.heappop(heap)
            self.nodes_explored += 1
            
            # Check if goal
            if self.is_goal(current_node.state):
                return self._reconstruct_path(current_node)
            
            # Cycle detection
            state_key = self.state_key(current_node.state)
            if state_key in visited:
                continue
            visited.add(state_key)
            self.nodes_expanded += 1
            
            # Depth limit check
            if current_node.g_score >= self.max_depth:
                continue
            
            # Explore neighbors
            for next_state, action in self.get_neighbors(current_node.state):
                next_state_key = self.state_key(next_state)
                
                if next_state_key not in visited:
                    g_score = current_node.g_score + 1
                    h_score = self.heuristic(next_state)
                    next_node = Node(next_state, g_score, h_score, current_node, action)
                    
                    counter += 1
                    heapq.heappush(heap, (next_node.f_score, counter, next_node))
        
        return None  # No solution found
    
    def _reconstruct_path(self, node: Node[T]) -> List[str]:
        """Reconstruct path from start to goal"""
        path = []
        current = node
        
        while current.parent is not None:
            if current.action:
                path.append(current.action)
            current = current.parent
        
        path.reverse()
        return path
    
    def get_statistics(self) -> dict:
        """Return search statistics"""
        return {
            'nodes_explored': self.nodes_explored,
            'nodes_expanded': self.nodes_expanded
        }