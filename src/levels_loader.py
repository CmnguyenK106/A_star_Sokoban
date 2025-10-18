# levels_loader_folder.py
from pathlib import Path
from typing import List, Dict, Optional

class LevelsFolderLoader:
    """Load Sokoban levels from individual text files in a folder"""
    
    def __init__(self, folder_path: str = "levels"):
        """
        Initialize loader with folder path
        
        Args:
            folder_path: Path to folder containing level files
        """
        self.folder_path = Path(folder_path)
        self.levels: Dict[int, List[str]] = {}
        self.load_levels()
    
    def load_levels(self):
        """Load all level files from folder"""
        if not self.folder_path.exists():
            print(f"Error: Folder '{self.folder_path}' not found!")
            return
        
        # Find all level files
        level_files = sorted(self.folder_path.glob("level_*.txt"))
        
        if not level_files:
            print(f"Error: No level files found in '{self.folder_path}'")
            return
        
        for level_file in level_files:
            try:
                # Extract level number from filename (level_001.txt -> 1)
                level_num = int(level_file.stem.split('_')[1])
                
                # Read level data
                with open(level_file, 'r') as f:
                    level_data = [line.rstrip('\n') for line in f.readlines()]
                
                self.levels[level_num] = level_data
            except Exception as e:
                print(f"Error loading {level_file}: {e}")
        
        print(f"✓ Loaded {len(self.levels)} levels from '{self.folder_path}' folder")
    
    def get_level(self, level_num: int) -> List[str]:
        """
        Get a specific level
        
        Args:
            level_num: Level number (1-100)
            
        Returns:
            List of strings representing the level
        """
        if level_num not in self.levels:
            print(f"Error: Level {level_num} not found!")
            return []
        return self.levels[level_num]
    
    def get_total_levels(self) -> int:
        """Get total number of levels"""
        return len(self.levels)
    
    def get_all_levels(self) -> Dict[int, List[str]]:
        """Get all levels"""
        return self.levels
    
    def get_level_range(self, start: int, end: int) -> Dict[int, List[str]]:
        """Get a range of levels"""
        return {k: v for k, v in self.levels.items() if start <= k <= end}
    
    def print_level(self, level_num: int):
        """Print a specific level"""
        level = self.get_level(level_num)
        if level:
            print(f"\nLevel {level_num}:")
            for row in level:
                print(row)
            print()
    
    def print_level_info(self, level_num: int):
        """Print level information"""
        level = self.get_level(level_num)
        if level:
            print(f"\n--- Level {level_num} ---")
            for row in level:
                print(row)
            
            # Count elements
            boxes = sum(row.count('$') for row in level)
            targets = sum(row.count('.') for row in level)
            print(f"Boxes: {boxes}, Targets: {targets}\n")


# Example usage
if __name__ == "__main__":
    loader = LevelsFolderLoader("levels")
    print(f"Total levels: {loader.get_total_levels()}\n")
    
    # Print first few levels
    for i in range(1, 4):
        loader.print_level_info(i)