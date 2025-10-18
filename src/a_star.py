import pygame
import sys
import heapq
from copy import deepcopy
from typing import List, Tuple, Set, Optional, Dict
import time

# Initialize Pygame
pygame.init()

# Constants
CELL_SIZE = 40
GRID_WIDTH = 21
GRID_HEIGHT = 11
WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE
WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE + 100  # Extra space for UI

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
DARK_GREEN = (0, 128, 0)

# Game elements
WALL = '#'
FLOOR = ' '
PLAYER = '@'
BOX = '$'
TARGET = '.'
BOX_ON_TARGET = '*'
PLAYER_ON_TARGET = '+'

class GameState:
    def __init__(self, level_data: List[str]):
        self.grid = [list(row.ljust(GRID_WIDTH)) for row in level_data[:GRID_HEIGHT]]
        while len(self.grid) < GRID_HEIGHT:
            self.grid.append([' '] * GRID_WIDTH)
        
        self.player_pos = self.find_player()
        self.boxes = self.find_boxes()
        self.targets = self.find_targets()
        self.moves = 0
        
    def find_player(self) -> Tuple[int, int]:
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell in [PLAYER, PLAYER_ON_TARGET]:
                    return (x, y)
        return (0, 0)
    
    def find_boxes(self) -> Set[Tuple[int, int]]:
        boxes = set()
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell in [BOX, BOX_ON_TARGET]:
                    boxes.add((x, y))
        return boxes
    
    def find_targets(self) -> Set[Tuple[int, int]]:
        targets = set()
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell in [TARGET, BOX_ON_TARGET, PLAYER_ON_TARGET]:
                    targets.add((x, y))
        return targets
    
    def is_wall(self, x: int, y: int) -> bool:
        if 0 <= y < len(self.grid) and 0 <= x < len(self.grid[0]):
            return self.grid[y][x] == WALL
        return True
    
    def is_valid_move(self, x: int, y: int) -> bool:
        return not self.is_wall(x, y)
    
    def move_player(self, dx: int, dy: int) -> bool:
        new_x, new_y = self.player_pos[0] + dx, self.player_pos[1] + dy
        
        if not self.is_valid_move(new_x, new_y):
            return False
        
        # Check if there's a box in the new position
        if (new_x, new_y) in self.boxes:
            box_new_x, box_new_y = new_x + dx, new_y + dy
            
            # Check if the box can be pushed
            if not self.is_valid_move(box_new_x, box_new_y) or (box_new_x, box_new_y) in self.boxes:
                return False
            
            # Move the box
            self.boxes.remove((new_x, new_y))
            self.boxes.add((box_new_x, box_new_y))
        
        # Move the player
        self.player_pos = (new_x, new_y)
        self.moves += 1
        return True
    
    def is_solved(self) -> bool:
        return self.boxes == self.targets
    
    def get_state_key(self) -> Tuple:
        return (self.player_pos, tuple(sorted(self.boxes)))
    
    def manhattan_distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def heuristic(self) -> int:
        """Heuristic function for A* - sum of distances from boxes to nearest targets"""
        if not self.boxes or not self.targets:
            return 0
        
        total_distance = 0
        boxes_list = list(self.boxes)
        targets_list = list(self.targets)
        
        # Simple heuristic: sum of minimum distances from each box to any target
        for box in boxes_list:
            min_dist = min(self.manhattan_distance(box, target) for target in targets_list)
            total_distance += min_dist
        
        return total_distance

class SokobanSolver:
    def __init__(self, initial_state: GameState):
        self.initial_state = deepcopy(initial_state)
        
    def get_neighbors(self, state: GameState) -> List[Tuple[GameState, str]]:
        """Get all possible next states from current state"""
        neighbors = []
        directions = [(-1, 0, 'LEFT'), (1, 0, 'RIGHT'), (0, -1, 'UP'), (0, 1, 'DOWN')]
        
        for dx, dy, direction in directions:
            new_state = deepcopy(state)
            if new_state.move_player(dx, dy):
                neighbors.append((new_state, direction))
        
        return neighbors
    
    def solve(self) -> Optional[List[str]]:
        """Solve using A* algorithm"""
        counter = 0  # Unique counter to break ties
        heap = [(0, counter, self.initial_state, [])]  # (f_score, counter, state, path)
        visited = set()
        
        while heap:
            f_score, _, current_state, path = heapq.heappop(heap)
            
            if current_state.is_solved():
                return path
            
            state_key = current_state.get_state_key()
            if state_key in visited:
                continue
            
            visited.add(state_key)
            
            # Prevent infinite loops by limiting search depth
            if len(path) > 200:
                continue
            
            for next_state, move in self.get_neighbors(current_state):
                next_state_key = next_state.get_state_key()
                if next_state_key not in visited:
                    new_g_score = len(path) + 1
                    new_f_score = new_g_score + next_state.heuristic()
                    new_path = path + [move]
                    
                    counter += 1
                    heapq.heappush(heap, (new_f_score, counter, next_state, new_path))
        
        return None  # No solution found

class SokobanGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Sokoban with A* Solver")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        
        # Simple level
        self.level = [
            "#####################",
            "#     #             #",
            "#  $  .  #####    ###",
            "##           #      #",
            "#   @        #    ###",
            "#          $        #",
            "#  .  $             #",
            "#   #       ##   .  #",
            "#   #        #      #",
            "#                   #",
            "#####################"
        ]
        
        self.game_state = GameState(self.level)
        self.solver = None
        self.solution = None
        self.auto_solving = False
        self.solution_index = 0
        self.last_auto_move_time = 0
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                if self.auto_solving:
                    continue
                    
                moved = False
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    moved = self.game_state.move_player(-1, 0)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    moved = self.game_state.move_player(1, 0)
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    moved = self.game_state.move_player(0, -1)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    moved = self.game_state.move_player(0, 1)
                elif event.key == pygame.K_r:
                    self.reset_game()
                elif event.key == pygame.K_SPACE:
                    self.start_auto_solve()
                
        return True
    
    def reset_game(self):
        self.game_state = GameState(self.level)
        self.auto_solving = False
        self.solution = None
        self.solution_index = 0
        
    def start_auto_solve(self):
        if self.auto_solving:
            return
            
        print("Starting A* solver...")
        self.solver = SokobanSolver(self.game_state)
        self.solution = self.solver.solve()
        
        if self.solution:
            print(f"Solution found in {len(self.solution)} moves!")
            print("Solution:", " -> ".join(self.solution))
            self.auto_solving = True
            self.solution_index = 0
            self.last_auto_move_time = time.time()
        else:
            print("No solution found!")
    
    def update_auto_solve(self):
        if not self.auto_solving or not self.solution:
            return
            
        current_time = time.time()
        if current_time - self.last_auto_move_time < 0.5:  # Move every 0.5 seconds
            return
            
        if self.solution_index < len(self.solution):
            move = self.solution[self.solution_index]
            
            if move == 'LEFT':
                self.game_state.move_player(-1, 0)
            elif move == 'RIGHT':
                self.game_state.move_player(1, 0)
            elif move == 'UP':
                self.game_state.move_player(0, -1)
            elif move == 'DOWN':
                self.game_state.move_player(0, 1)
            
            self.solution_index += 1
            self.last_auto_move_time = current_time
        else:
            self.auto_solving = False
            print("Auto-solve completed!")
    
    def draw(self):
        self.screen.fill(WHITE)
        
        # Draw grid
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                
                # Draw floor
                pygame.draw.rect(self.screen, WHITE, rect)
                pygame.draw.rect(self.screen, BLACK, rect, 1)
                
                # Draw wall
                if self.game_state.grid[y][x] == WALL:
                    pygame.draw.rect(self.screen, BROWN, rect)
                
                # Draw target
                if (x, y) in self.game_state.targets:
                    pygame.draw.circle(self.screen, DARK_GREEN, rect.center, CELL_SIZE // 4)
        
        # Draw boxes
        for box_x, box_y in self.game_state.boxes:
            rect = pygame.Rect(box_x * CELL_SIZE, box_y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            color = GREEN if (box_x, box_y) in self.game_state.targets else YELLOW
            pygame.draw.rect(self.screen, color, rect.inflate(-4, -4))
            pygame.draw.rect(self.screen, BLACK, rect.inflate(-4, -4), 2)
        
        # Draw player
        player_x, player_y = self.game_state.player_pos
        rect = pygame.Rect(player_x * CELL_SIZE, player_y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.circle(self.screen, BLUE, rect.center, CELL_SIZE // 3)
        pygame.draw.circle(self.screen, BLACK, rect.center, CELL_SIZE // 3, 2)
        
        # Draw UI
        y_offset = GRID_HEIGHT * CELL_SIZE + 10
        
        moves_text = self.font.render(f"Moves: {self.game_state.moves}", True, BLACK)
        self.screen.blit(moves_text, (10, y_offset))
        
        if self.game_state.is_solved():
            solved_text = self.font.render("SOLVED!", True, GREEN)
            self.screen.blit(solved_text, (10, y_offset + 25))
        
        status_text = ""
        if self.auto_solving:
            status_text = f"Auto-solving... Step {self.solution_index}/{len(self.solution) if self.solution else 0}"
        else:
            status_text = "Manual mode"
        
        status_surface = self.font.render(status_text, True, BLACK)
        self.screen.blit(status_surface, (10, y_offset + 50))
        
        # Instructions
        inst1 = self.font.render("WASD/Arrows: Move, SPACE: Auto-solve, R: Reset", True, BLACK)
        self.screen.blit(inst1, (10, y_offset + 75))
        
        pygame.display.flip()
    
    def run(self):
        running = True
        
        while running:
            running = self.handle_events()
            self.update_auto_solve()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = SokobanGame()
    game.run()