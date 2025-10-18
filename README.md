    # Sokoban Game with Folder-Based Levels - Complete Setup Guide

## 📁 A* Sokoban game

```
sokoban_project/
├── astar.py                      # Generic A* algorithm
├── sokoban_solver.py             # Game logic & solver
├── levels_loader.py       # Loads levels from folder
├── sokoban_ui.py           # Main game UI
├── generate_levels.py            # Script to generate level files
└── levels/                       # Folder with all level files
    ├── level_001.txt
    ├── level_002.txt
    ├── ...
    └── level_100.txt
```

## 🚀 Quick Start (4 Steps)

### Step 1: Create Python Files

Copy these 4 Python files into your project folder:
- `astar.py` - From "A* Algorithm Implementation"
- `sokoban_solver.py` - From "Sokoban Solver using A*"
- `levels_loader_folder.py` - From "Level Loader for Text Files in Folder"
- `sokoban_ui_final.py` - From "Sokoban Game UI - Final Version"
- `generate_levels.py` - From "Level Generator Script"

### Step 2: Generate Level Files

Run the level generator to create the `levels` folder with 100 text files:

```bash
python generate_levels.py
```

**Output:**
```
✓ Generated 100 level files in 'levels' folder
Files created: level_001.txt to level_100.txt
```

This creates:
- `levels/level_001.txt` through `levels/level_100.txt`
- Each file contains one 10x10 Sokoban level

### Step 3: Install Dependencies

```bash
pip install pygame
```

### Step 4: Run the Game

```bash
python sokoban_ui_final.py
```

**Output:**
```
============================================================
SOKOBAN GAME - 100 LEVELS WITH A* SOLVER
============================================================
Total levels loaded: 100
============================================================

✓ Loaded 100 levels from 'levels' folder
```

## 🎮 Game Controls

| Key | Action |
|-----|--------|
| **W/A/S/D** or **Arrow Keys** | Move player |
| **SPACE** | Auto-solve with A* |
| **R** | Reset current level |
| **N** | Next level |
| **P** | Previous level |
| **1** | Jump to Level 1 |
| **2** | Jump to Level 50 |
| **3** | Jump to Level 100 |
| **ESC** | Stop auto-solve |

## 📊 Level Difficulty

- **Levels 1-10**: Tutorial (Very Easy) ⭐
- **Levels 11-30**: Simple (Easy) ⭐⭐
- **Levels 31-50**: Intermediate (Medium) ⭐⭐⭐
- **Levels 51-70**: Advanced (Hard) ⭐⭐⭐⭐
- **Levels 71-90**: Expert (Very Hard) ⭐⭐⭐⭐⭐
- **Levels 91-100**: Master (Extremely Hard) 🔥🔥🔥

## 📝 Level File Format

Each level file is a simple text file with 10 lines:

**Example: level_001.txt**
```
##########
#        #
#  $  .  #
#        #
#   @    #
#        #
#  .  $  #
#        #
#        #
##########
```

**Legend:**
- `#` = Wall
- ` ` (space) = Floor
- `@` = Player
- `$` = Box
- `.` = Target

## 🔍 How It Works

### 1. Level Loading Process
```
generate_levels.py
    ↓
Creates 100 text files in 'levels' folder
    ↓
sokoban_ui_final.py
    ↓
LevelsFolderLoader loads files
    ↓
GameState parses level data
    ↓
Renders in Pygame
```

### 2. A* Solving Process
```
User presses SPACE
    ↓
SokobanSolver initializes
    ↓
A* algorithm explores states
    ↓
Finds optimal solution path
    ↓
Executes moves automatically
```

## 📈 Performance Metrics

When solving with A*, you'll see:
- **Moves**: Number of steps to solve
- **Time**: Seconds to find solution
- **Nodes Explored**: States evaluated
- **Nodes Expanded**: States with neighbors checked

**Example Output:**
```
✓ Level 25 solved: 47 moves in 0.23s
  Nodes explored: 1,234
```

## 🛠️ Troubleshooting

### "No level files found" Error
**Problem:** `Error: No level files found in 'levels'`

**Solution:**
1. Make sure `generate_levels.py` is in same directory as other files
2. Run: `python generate_levels.py`
3. Verify `levels` folder was created with 100 files

### Pygame Not Found
**Problem:** `ModuleNotFoundError: No module named 'pygame'`

**Solution:**
```bash
pip install pygame
```

### Level File Issues
**Problem:** Levels not displaying correctly

**Solution:**
1. Check that `level_*.txt` files have exactly 10 lines
2. Each line should be exactly 10 characters
3. Valid characters: `#`, ` `, `@`, `$`, `.`

## 🎯 Testing All Levels

Create `test_all_levels.py`:

```python
from levels_loader_folder import LevelsFolderLoader
from sokoban_solver import SokobanSolver
import time

loader = LevelsFolderLoader("levels")
solved = 0
total_time = 0

for level_num in range(1, loader.get_total_levels() + 1):
    level_data = loader.get_level(level_num)
    solver = SokobanSolver(level_data)
    
    start = time.time()
    solution = solver.solve()
    elapsed = time.time() - start
    
    if solution:
        solved += 1
        total_time += elapsed
        print(f"✓ Lv{level_num:3d}: {len(solution):3d} moves ({elapsed:6.2f}s)")
    else:
        print(f"✗ Lv{level_num:3d}: No solution")

print(f"\nSolved: {solved}/{loader.get_total_levels()}")
print(f"Total time: {total_time:.2f}s")
```

Run it:
```bash
python test_all_levels.py
```

## 🔧 Customization

### Add More Levels

1. Create new level file: `levels/level_101.txt`
2. Write 10x10 Sokoban level
3. Restart game - loads automatically!

### Change Game Speed

In `sokoban_ui_final.py`, modify:
```python
if current_time - self.last_auto_move_time < 0.3:  # Change 0.3 to speed
```
- Lower value = Faster execution
- Higher value = Slower execution

### Change Board Size

In `sokoban_ui_final.py`, modify:
```python
CELL_SIZE = 40      # Pixel size per cell
GRID_WIDTH = 10     # Change to your width
GRID_HEIGHT = 10    # Change to your height
```

## 📚 File Descriptions

| File | Purpose |
|------|---------|
| `astar.py` | Generic A* pathfinding algorithm |
| `sokoban_solver.py` | Sokoban game logic & A* integration |
| `levels_loader_folder.py` | Loads level files from folder |
| `sokoban_ui_final.py` | Pygame UI & main game loop |
| `generate_levels.py` | Creates 100 level text files |

## 🎓 Learning Resources

### How A* Works
1. Start state = player position + box positions
2. Goal state = all boxes on targets
3. Heuristic = sum of distances (box to nearest target)
4. Exploration = priority queue ordered by f(n) = g(n) + h(n)

### State Representation
```python
state = (
    (player_x, player_y),
    ((box1_x, box1_y), (box2_x, box2_y), ...)
)
```

## 💡 Tips for Better Performance

1. **Early Termination**: A* stops when goal found
2. **Good Heuristic**: Manhattan distance is effective
3. **Cycle Detection**: Tracks visited states
4. **Depth Limiting**: Prevents infinite search

## 🚀 Next Steps

- [ ] Beat all 100 levels manually
- [ ] Watch A* solve them automatically
- [ ] Create difficulty rating system
- [ ] Implement dead-lock detection
- [ ] Add level editor
- [ ] Create your own levels
- [ ] Optimize A* heuristic

## 📞 Support

If something doesn't work:
1. Check all 5 Python files are in same directory
2. Verify `levels` folder with 100 files exists
3. Ensure pygame is installed: `pip install pygame`

4. Check Python version: `python --version` (need 3.6+)


