import os
from collections import defaultdict

def solve_puzzle():
    # Construct path to input.txt
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'input.txt')
    
    try:
        with open(file_path, 'r') as f:
            lines = [line.replace('\n', '') for line in f.readlines()]
    except FileNotFoundError:
        print(f"Error: 'input.txt' not found at {file_path}")
        input("\nPress Enter to exit...")
        return

    if not lines:
        print("Input file is empty.")
        return

    # Normalize grid width
    width = max(len(line) for line in lines)
    grid = [line.ljust(width, '.') for line in lines]
    height = len(grid)
    
    # Find start position 'S'
    # For Part 2, we track the number of timelines at each column.
    # Key: Column Index, Value: Count of timelines
    timeline_counts = defaultdict(int)
    
    found_start = False
    for c in range(width):
        if grid[0][c] == 'S':
            timeline_counts[c] = 1
            found_start = True
            break
            
    if not found_start:
        print("Error: No starting point 'S' found.")
        return

    print(f"Starting simulation from column {list(timeline_counts.keys())[0]}...")
    
    # Simulate row by row
    # We process the grid cell at (r, c) to determine where the timeline goes in row r+1
    for r in range(height):
        next_counts = defaultdict(int)
        
        for c, count in timeline_counts.items():
            # Check boundaries just in case
            if c < 0 or c >= width:
                continue
                
            char = grid[r][c]
            
            if char == '^':
                # Splitter: The timeline splits into two distinct timelines.
                # One goes left, one goes right. Both inherit the history (count) of the parent.
                
                # Left branch
                if c - 1 >= 0:
                    next_counts[c - 1] += count
                
                # Right branch
                if c + 1 < width:
                    next_counts[c + 1] += count
            else:
                # Empty space or Start: The timeline continues straight down.
                next_counts[c] += count
        
        timeline_counts = next_counts
        
        # Optimization: If no timelines left (all hit walls?), stop early
        if not timeline_counts:
            break

    # The result is the total number of timelines that made it out of the bottom of the grid
    total_timelines = sum(timeline_counts.values())
    print(f"Total active timelines (Part 2): {total_timelines}")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    solve_puzzle()