# sokoban_solver.py
from copy import deepcopy
from typing import List, Tuple, Set, Optional
from astar import AStar

class GameState:
    """Represents a Sokoban game state"""
    
    WALL = '#'
    FLOOR = ' '
    PLAYER = '@'
    BOX = '$'
    TARGET = '.'
    BOX_ON_TARGET = '*'
    PLAYER_ON_TARGET = '+'
    
    def __init__(self, level_data: List[str], grid_width: int = 10, grid_height: int = 10):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.grid = [list(row.ljust(grid_width)) for row in level_data[:grid_height]]
        
        while len(self.grid) < grid_height:
            self.grid.append([' '] * grid_width)
        
        self.player_pos = self.find_player()
        self.boxes = self.find_boxes()
        self.targets = self.find_targets()
        self.moves = 0
    
    def find_player(self) -> Tuple[int, int]:
        """Find player position in grid"""
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell in [self.PLAYER, self.PLAYER_ON_TARGET]:
                    return (x, y)
        return (0, 0)
    
    def find_boxes(self) -> Set[Tuple[int, int]]:
        """Find all box positions"""
        boxes = set()
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell in [self.BOX, self.BOX_ON_TARGET]:
                    boxes.add((x, y))
        return boxes
    
    def find_targets(self) -> Set[Tuple[int, int]]:
        """Find all target positions"""
        targets = set()
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell in [self.TARGET, self.BOX_ON_TARGET, self.PLAYER_ON_TARGET]:
                    targets.add((x, y))
        return targets
    
    def is_wall(self, x: int, y: int) -> bool:
        """Check if position is a wall"""
        if 0 <= y < self.grid_height and 0 <= x < self.grid_width:
            return self.grid[y][x] == self.WALL
        return True
    
    def move_player(self, dx: int, dy: int) -> bool:
        """
        Move player by (dx, dy)
        Returns True if move was successful
        """
        new_x, new_y = self.player_pos[0] + dx, self.player_pos[1] + dy
        
        if self.is_wall(new_x, new_y):
            return False
        
        # Check if there's a box in the new position
        if (new_x, new_y) in self.boxes:
            box_new_x, box_new_y = new_x + dx, new_y + dy
            
            # Check if the box can be pushed
            if self.is_wall(box_new_x, box_new_y) or (box_new_x, box_new_y) in self.boxes:
                return False
            
            # Move the box
            self.boxes.remove((new_x, new_y))
            self.boxes.add((box_new_x, box_new_y))
        
        # Move the player
        self.player_pos = (new_x, new_y)
        self.moves += 1
        return True
    
    def is_solved(self) -> bool:
        """Check if all boxes are on targets"""
        return self.boxes == self.targets
    
    def get_state_key(self) -> Tuple:
        """Create hashable state key for cycle detection"""
        return (self.player_pos, tuple(sorted(self.boxes)))
    
    def manhattan_distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
        """Calculate Manhattan distance between two positions"""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def heuristic(self) -> int:
        """
        Heuristic function for A*
        Sum of minimum distances from each box to any target
        """
        if not self.boxes or not self.targets:
            return 0
        
        total_distance = 0
        boxes_list = list(self.boxes)
        targets_list = list(self.targets)
        
        for box in boxes_list:
            min_dist = min(self.manhattan_distance(box, target) for target in targets_list)
            total_distance += min_dist
        
        return total_distance
    
    def get_neighbors(self) -> List[Tuple['GameState', str]]:
        """Get all possible next states and the actions that produce them"""
        neighbors = []
        directions = [
            (-1, 0, 'LEFT'),
            (1, 0, 'RIGHT'),
            (0, -1, 'UP'),
            (0, 1, 'DOWN')
        ]
        
        for dx, dy, direction in directions:
            new_state = deepcopy(self)
            if new_state.move_player(dx, dy):
                neighbors.append((new_state, direction))
        
        return neighbors


class SokobanSolver:
    """Solves Sokoban using A* algorithm"""
    
    def __init__(self, level_data: List[str], grid_width: int = 10, grid_height: int = 10):
        """
        Initialize solver with a level
        
        Args:
            level_data: List of strings representing the level
            grid_width: Width of the game grid
            grid_height: Height of the game grid
        """
        self.initial_state = GameState(level_data, grid_width, grid_height)
        self.solution = None
        self.solver = None
    
    def solve(self) -> Optional[List[str]]:
        """
        Solve the Sokoban puzzle using A*
        
        Returns:
            List of moves (UP, DOWN, LEFT, RIGHT) or None if unsolvable
        """
        self.solver = AStar(
            initial_state=self.initial_state,
            is_goal=lambda state: state.is_solved(),
            get_neighbors=lambda state: state.get_neighbors(),
            heuristic=lambda state: state.heuristic(),
            state_key=lambda state: state.get_state_key(),
            max_depth=500
        )
        
        self.solution = self.solver.solve()
        return self.solution
    
    def get_statistics(self) -> dict:
        """Get solver statistics"""
        if self.solver:
            stats = self.solver.get_statistics()
            stats['solution_length'] = len(self.solution) if self.solution else 0
            return stats
        return {}
    
    def print_solution(self):
        """Print solution in human-readable format"""
        if self.solution:
            print(f"Solution found in {len(self.solution)} moves!")
            print(f"Moves: {' -> '.join(self.solution)}")
            stats = self.get_statistics()
            print(f"Nodes explored: {stats['nodes_explored']}")
            print(f"Nodes expanded: {stats['nodes_expanded']}")
        else:
            print("No solution found!")


# Example usage
if __name__ == "__main__":
    level = [
        "##########",
        "#        #",
        "#  $  .  #",
        "#        #",
        "#   @    #",
        "#        #",
        "#  .  $  #",
        "#        #",
        "#        #",
        "##########"
    ]
    
    solver = SokobanSolver(level)
    solver.solve()
    solver.print_solution()