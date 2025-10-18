# sokoban_ui_final.py
import pygame
import sys
import time
from sokoban_solver import SokobanSolver, GameState
from levels_loader import LevelsFolderLoader

# Initialize Pygame
pygame.init()

# Constants
CELL_SIZE = 40
GRID_WIDTH = 10
GRID_HEIGHT = 10
WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE
WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE + 120

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
LIGHT_GRAY = (200, 200, 200)


class SokobanGameFinal:
    """Sokoban game with A* solver and folder-based level system"""
    
    def __init__(self, levels_folder: str = "levels"):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Sokoban - A* Solver with 100 Levels")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 20)
        
        # Load levels
        try:
            self.loader = LevelsFolderLoader(levels_folder)
            self.total_levels = self.loader.get_total_levels()
        except Exception as e:
            print(f"Error loading levels: {e}")
            print("Make sure to run generate_levels.py first!")
            sys.exit(1)
        
        # Game state
        self.current_level_num = 1
        self.load_current_level()
        
        self.solver = None
        self.solution = None
        self.auto_solving = False
        self.solution_index = 0
        self.last_auto_move_time = 0
        
        # Statistics
        self.level_stats = {}
        self.total_moves = 0
        self.total_time = 0.0
    
    def load_current_level(self):
        """Load the current level"""
        level_data = self.loader.get_level(self.current_level_num)
        
        self.level_data = level_data
        self.current_state = GameState(level_data, GRID_WIDTH, GRID_HEIGHT)
        self.original_state = GameState(level_data, GRID_WIDTH, GRID_HEIGHT)
        
        self.auto_solving = False
        self.solution = None
        self.solution_index = 0
    
    def handle_events(self) -> bool:
        """Handle user input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                if self.auto_solving:
                    if event.key == pygame.K_ESCAPE:
                        self.auto_solving = False
                    continue
                
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.current_state.move_player(-1, 0)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.current_state.move_player(1, 0)
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.current_state.move_player(0, -1)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.current_state.move_player(0, 1)
                elif event.key == pygame.K_r:
                    self.reset_level()
                elif event.key == pygame.K_SPACE:
                    self.start_auto_solve()
                elif event.key == pygame.K_n:
                    self.next_level()
                elif event.key == pygame.K_p:
                    self.prev_level()
                elif event.key == pygame.K_1:
                    self.goto_level(1)
                elif event.key == pygame.K_2:
                    self.goto_level(50)
                elif event.key == pygame.K_3:
                    self.goto_level(self.total_levels)
        
        return True
    
    def reset_level(self):
        """Reset current level"""
        self.load_current_level()
    
    def next_level(self):
        """Go to next level"""
        if self.current_level_num < self.total_levels:
            self.current_level_num += 1
            self.load_current_level()
            print(f"→ Level {self.current_level_num}/{self.total_levels}")
        else:
            print("Already at last level!")
    
    def prev_level(self):
        """Go to previous level"""
        if self.current_level_num > 1:
            self.current_level_num -= 1
            self.load_current_level()
            print(f"← Level {self.current_level_num}/{self.total_levels}")
        else:
            print("Already at first level!")
    
    def goto_level(self, level_num: int):
        """Jump to specific level"""
        if 1 <= level_num <= self.total_levels:
            self.current_level_num = level_num
            self.load_current_level()
            print(f"⊙ Jumped to Level {self.current_level_num}/{self.total_levels}")
        else:
            print(f"Invalid level! Choose between 1 and {self.total_levels}")
    
    def start_auto_solve(self):
        """Start A* solver"""
        if self.auto_solving:
            return
        
        print(f"\n🔍 Solving Level {self.current_level_num}...")
        self.solver = SokobanSolver(self.level_data, GRID_WIDTH, GRID_HEIGHT)
        
        start_time = time.time()
        self.solution = self.solver.solve()
        solve_time = time.time() - start_time
        
        if self.solution:
            self.level_stats[self.current_level_num] = {
                'moves': len(self.solution),
                'time': solve_time,
                'nodes_explored': self.solver.solver.nodes_explored,
                'nodes_expanded': self.solver.solver.nodes_expanded
            }
            
            self.total_moves += len(self.solution)
            self.total_time += solve_time
            
            print(f"✓ Level {self.current_level_num} solved: {len(self.solution)} moves in {solve_time:.2f}s")
            print(f"  Nodes explored: {self.solver.solver.nodes_explored}")
            
            self.auto_solving = True
            self.solution_index = 0
            self.last_auto_move_time = time.time()
        else:
            print(f"✗ Level {self.current_level_num}: No solution found!")
    
    def update_auto_solve(self):
        """Execute automatic solve steps"""
        if not self.auto_solving or not self.solution:
            return
        
        current_time = time.time()
        if current_time - self.last_auto_move_time < 0.3:
            return
        
        if self.solution_index < len(self.solution):
            move = self.solution[self.solution_index]
            
            if move == 'LEFT':
                self.current_state.move_player(-1, 0)
            elif move == 'RIGHT':
                self.current_state.move_player(1, 0)
            elif move == 'UP':
                self.current_state.move_player(0, -1)
            elif move == 'DOWN':
                self.current_state.move_player(0, 1)
            
            self.solution_index += 1
            self.last_auto_move_time = current_time
        else:
            self.auto_solving = False
            print(f"✓ Level {self.current_level_num} completed!\n")
    
    def draw(self):
        """Draw game state"""
        self.screen.fill(WHITE)
        
        # Draw grid
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                
                # Draw floor
                pygame.draw.rect(self.screen, WHITE, rect)
                pygame.draw.rect(self.screen, BLACK, rect, 1)
                
                # Draw wall
                if self.current_state.grid[y][x] == GameState.WALL:
                    pygame.draw.rect(self.screen, BROWN, rect)
                
                # Draw target
                if (x, y) in self.current_state.targets:
                    pygame.draw.circle(self.screen, DARK_GREEN, rect.center, CELL_SIZE // 4)
        
        # Draw boxes
        for box_x, box_y in self.current_state.boxes:
            rect = pygame.Rect(box_x * CELL_SIZE, box_y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            color = GREEN if (box_x, box_y) in self.current_state.targets else YELLOW
            pygame.draw.rect(self.screen, color, rect.inflate(-4, -4))
            pygame.draw.rect(self.screen, BLACK, rect.inflate(-4, -4), 2)
        
        # Draw player
        player_x, player_y = self.current_state.player_pos
        rect = pygame.Rect(player_x * CELL_SIZE, player_y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.circle(self.screen, BLUE, rect.center, CELL_SIZE // 3)
        pygame.draw.circle(self.screen, BLACK, rect.center, CELL_SIZE // 3, 2)
        
        # Draw UI
        y_offset = GRID_HEIGHT * CELL_SIZE + 10
        
        # Level info
        level_text = self.font.render(f"Level: {self.current_level_num}/{self.total_levels}", True, BLACK)
        self.screen.blit(level_text, (10, y_offset))
        
        moves_text = self.font.render(f"Moves: {self.current_state.moves}", True, BLACK)
        self.screen.blit(moves_text, (200, y_offset))
        
        if self.current_level_num in self.level_stats:
            stats = self.level_stats[self.current_level_num]
            stats_text = self.small_font.render(
                f"Best: {stats['moves']} moves ({stats['time']:.2f}s)",
                True, GRAY
            )
            self.screen.blit(stats_text, (360, y_offset))
        
        # Status
        if self.current_state.is_solved():
            solved_text = self.font.render("✓ SOLVED!", True, GREEN)
            self.screen.blit(solved_text, (10, y_offset + 25))
        
        status_text = ""
        if self.auto_solving:
            status_text = f"Auto-solving... Step {self.solution_index}/{len(self.solution) if self.solution else 0}"
        else:
            status_text = "Manual mode"
        
        status_surface = self.font.render(status_text, True, BLACK)
        self.screen.blit(status_surface, (10, y_offset + 50))
        
        # Instructions
        inst1 = self.small_font.render("Move: WASD/Arrows | Solve: SPACE | Reset: R | Next: N | Prev: P", True, BLACK)
        inst2 = self.small_font.render("Jump: 1=Lv1, 2=Lv50, 3=Lv100 | ESC: Stop solve", True, GRAY)
        self.screen.blit(inst1, (10, y_offset + 75))
        self.screen.blit(inst2, (10, y_offset + 95))
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        running = True
        
        print(f"\n{'='*60}")
        print(f"SOKOBAN GAME - 100 LEVELS WITH A* SOLVER")
        print(f"{'='*60}")
        print(f"Total levels loaded: {self.total_levels}")
        print(f"{'='*60}\n")
        
        while running:
            running = self.handle_events()
            self.update_auto_solve()
            self.draw()
            self.clock.tick(60)
        
        self.print_statistics()
        pygame.quit()
        sys.exit()
    
    def print_statistics(self):
        """Print overall statistics with complexity analysis"""
        if self.level_stats:
            print(f"\n{'='*70}")
            print(f"{'GAME STATISTICS & COMPLEXITY ANALYSIS':^70}")
            print(f"{'='*70}\n")
            
            # Basic Statistics
            print(f"{'BASIC STATISTICS':-^70}")
            print(f"Levels solved:          {len(self.level_stats)}/{self.total_levels}")
            success_rate = 100*len(self.level_stats)//self.total_levels if self.total_levels > 0 else 0
            print(f"Success rate:           {success_rate}%")
            print(f"Total moves:            {self.total_moves}")
            print(f"Total time:             {self.total_time:.2f}s")
            if len(self.level_stats) > 0:
                print(f"Average time per level: {self.total_time/len(self.level_stats):.2f}s")
                print(f"Average moves per level: {self.total_moves/len(self.level_stats):.1f}")
            
            # Complexity Analysis
            print(f"\n{'A* ALGORITHM COMPLEXITY':-^70}")
            
            total_nodes_explored = sum(s['nodes_explored'] for s in self.level_stats.values())
            total_nodes_expanded = sum(s['nodes_expanded'] for s in self.level_stats.values())
            avg_nodes_explored = total_nodes_explored / len(self.level_stats) if self.level_stats else 0
            avg_nodes_expanded = total_nodes_expanded / len(self.level_stats) if self.level_stats else 0
            
            print(f"Total nodes explored:   {total_nodes_explored:,}")
            print(f"Total nodes expanded:   {total_nodes_expanded:,}")
            print(f"Avg nodes explored:     {avg_nodes_explored:,.0f}")
            print(f"Avg nodes expanded:     {avg_nodes_expanded:,.0f}")
            
            # Find min/max complexity levels
            if self.level_stats:
                easiest = min(self.level_stats.items(), key=lambda x: x[1]['nodes_explored'])
                hardest = max(self.level_stats.items(), key=lambda x: x[1]['nodes_explored'])
                
                print(f"\nEasiest level:          Level {easiest[0]} "
                      f"({easiest[1]['nodes_explored']} nodes, {easiest[1]['moves']} moves)")
                print(f"Hardest level:          Level {hardest[0]} "
                      f"({hardest[1]['nodes_explored']} nodes, {hardest[1]['moves']} moves)")
            
            # Time Complexity
            print(f"\n{'TIME COMPLEXITY ANALYSIS':-^70}")
            total_seconds = self.total_time
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            seconds = int(total_seconds % 60)
            
            if hours > 0:
                print(f"Total runtime:          {hours}h {minutes}m {seconds}s")
            elif minutes > 0:
                print(f"Total runtime:          {minutes}m {seconds}s")
            else:
                print(f"Total runtime:          {seconds}s")
            
            # Branching factor analysis
            print(f"\n{'BRANCHING FACTOR ANALYSIS':-^70}")
            avg_branching_factor = avg_nodes_expanded / avg_nodes_explored if avg_nodes_explored > 0 else 0
            print(f"Average branching factor: {avg_branching_factor:.2f}")
            print(f"(Average children per node: {avg_branching_factor:.2f})")
            
            # Space Complexity
            print(f"\n{'SPACE COMPLEXITY':-^70}")
            max_nodes = max((s['nodes_explored'] for s in self.level_stats.values()), default=0)
            print(f"Maximum nodes in memory: {max_nodes:,}")
            print(f"Average memory peak:     {avg_nodes_explored:,.0f} nodes")
            
            # Level Difficulty by Complexity
            print(f"\n{'DIFFICULTY BY COMPLEXITY':-^70}")
            sorted_levels = sorted(self.level_stats.items(), 
                                  key=lambda x: x[1]['nodes_explored'])
            
            print(f"\nEasiest (by A* complexity):")
            for i, (level_num, stats) in enumerate(sorted_levels[:5], 1):
                print(f"  {i}. Level {level_num:3d}: {stats['nodes_explored']:6,} nodes, "
                      f"{stats['moves']:3d} moves ({stats['time']:.2f}s)")
            
            print(f"\nHardest (by A* complexity):")
            for i, (level_num, stats) in enumerate(sorted_levels[-5:], 1):
                print(f"  {i}. Level {level_num:3d}: {stats['nodes_explored']:6,} nodes, "
                      f"{stats['moves']:3d} moves ({stats['time']:.2f}s)")
            
            # Efficiency metric
            print(f"\n{'EFFICIENCY METRICS':-^70}")
            avg_efficiency = (avg_nodes_explored / avg_nodes_expanded) if avg_nodes_expanded > 0 else 1
            print(f"Heuristic efficiency:    {avg_efficiency:.2f}")
            print(f"(Lower is better - ratio of explored to expanded)")
            
            print(f"\n{'='*70}\n")
        else:
            print("\nNo levels solved yet!")


if __name__ == "__main__":
    game = SokobanGameFinal("levels")
    game.run()