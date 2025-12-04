import os

def count_neighbors(grid, r, c):
    """
    Counts the number of '@' symbols in the 8 adjacent cells 
    surrounding (r, c).
    """
    rows = len(grid)
    cols = len(grid[0])
    count = 0
    
    # Check all 8 directions (diagonals included)
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            # Skip the center cell itself
            if dr == 0 and dc == 0:
                continue
            
            nr, nc = r + dr, c + dc
            
            # Check boundaries
            if 0 <= nr < rows and 0 <= nc < cols:
                if grid[nr][nc] == '@':
                    count += 1
    return count

def solve_puzzle():
    accessible_count = 0
    
    # Construct path to input.txt
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'input.txt')
    
    try:
        with open(file_path, 'r') as f:
            # Read lines and strip newlines
            grid = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Error: 'input.txt' not found at {file_path}")
        input("\nPress Enter to exit...")
        return

    rows = len(grid)
    cols = len(grid[0])
    
    print(f"Grid size: {rows}x{cols}")

    for r in range(rows):
        for c in range(cols):
            # We only care about rolls of paper ('@')
            if grid[r][c] == '@':
                neighbor_count = count_neighbors(grid, r, c)
                
                # The rule: access if fewer than 4 neighbors are rolls of paper
                if neighbor_count < 4:
                    accessible_count += 1

    print(f"Accessible rolls of paper: {accessible_count}")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    solve_puzzle()