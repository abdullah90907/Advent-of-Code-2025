import os

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
    active_beams = set()
    for c in range(width):
        if grid[0][c] == 'S':
            active_beams.add(c)
            break
            
    if not active_beams:
        print("Error: No starting point 'S' found.")
        return

    print(f"Starting simulation from column {list(active_beams)[0]}...")
    
    total_splits = 0
    
    # Simulate row by row
    # Note: We process what happens to beams currently AT row r.
    # If they hit a splitter, the new beams appear at row r+1 (conceptually).
    # If they pass through, the beam appears at row r+1.
    for r in range(height):
        next_beams = set()
        
        for c in active_beams:
            # Check boundaries just in case
            if c < 0 or c >= width:
                continue
                
            char = grid[r][c]
            
            if char == '^':
                total_splits += 1
                # Split creates beams at left and right
                # The prompt says they continue from immediate left/right.
                # Since they move "downward", they will be in the next row at c-1 and c+1.
                if c - 1 >= 0:
                    next_beams.add(c - 1)
                if c + 1 < width:
                    next_beams.add(c + 1)
            else:
                # Beam passes through '.' or 'S'
                # It continues downward to the same column in the next row
                next_beams.add(c)
        
        active_beams = next_beams
        
        # Optimization: If no beams left, we can stop early
        if not active_beams:
            break

    print(f"Total times the beam was split: {total_splits}")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    solve_puzzle()