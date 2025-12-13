import os
import re
import itertools

def solve_linear_system_gf2(matrix, target):
    """
    Solves Ax = b over GF(2).
    Returns (solution found?, min_presses)
    
    matrix: list of lists (rows are lights, cols are buttons)
    target: list (vector of target light states)
    """
    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0
    
    if rows == 0:
        return True, 0
    m = [row[:] + [target[r]] for r, row in enumerate(matrix)]

    pivot_row = 0
    pivots = [] 
    pivot_cols = set()
    
    for c in range(cols):
        if pivot_row >= rows:
            break

        swap_r = -1
        if m[pivot_row][c] == 1:
            swap_r = pivot_row
        else:
            for r in range(pivot_row + 1, rows):
                if m[r][c] == 1:
                    swap_r = r
                    break
        
        if swap_r == -1:
            continue
            
        m[pivot_row], m[swap_r] = m[swap_r], m[pivot_row]

        for r in range(rows):
            if r != pivot_row and m[r][c] == 1:
                for k in range(c, cols + 1):
                    m[r][k] ^= m[pivot_row][k]
                    
        pivots.append((pivot_row, c))
        pivot_cols.add(c)
        pivot_row += 1
    for r in range(pivot_row, rows):
        if m[r][cols] == 1:
            return False, 0
    free_vars = [c for c in range(cols) if c not in pivot_cols]
    
    min_presses = float('inf')
    for free_vals in itertools.product([0, 1], repeat=len(free_vars)):
        x = [0] * cols

        for i, val in enumerate(free_vals):
            x[free_vars[i]] = val

        for r, c in reversed(pivots):
            row_sum = 0
            for k in range(c + 1, cols):
                if m[r][k] == 1:
                    row_sum ^= x[k]
            
            x[c] = m[r][cols] ^ row_sum

        presses = sum(x)
        if presses < min_presses:
            min_presses = presses
            
    return True, min_presses

def solve_machine(line):
    pattern_match = re.search(r'\[([.#]+)\]', line)
    if not pattern_match:
        return 0
    pattern_str = pattern_match.group(1)
    target_vec = [1 if c == '#' else 0 for c in pattern_str]
    num_lights = len(target_vec)
    
    button_matches = re.findall(r'\(([\d,]+)\)', line)
    
    num_buttons = len(button_matches)
    matrix = [[0] * num_buttons for _ in range(num_lights)]
    
    for btn_idx, btn_str in enumerate(button_matches):
        indices = list(map(int, btn_str.split(',')))
        for light_idx in indices:
            if light_idx < num_lights:
                matrix[light_idx][btn_idx] = 1

    solvable, presses = solve_linear_system_gf2(matrix, target_vec)
    
    if solvable:
        return presses
    else:
        print(f"Warning: Machine with pattern {pattern_str} has no solution.")
        return 0

def solve_puzzle():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'input.txt')
    
    try:
        with open(file_path, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: 'input.txt' not found at {file_path}")
        input("\nPress Enter to exit...")
        return

    total_presses = 0
    print(f"Processing {len(lines)} machines...")
    
    for i, line in enumerate(lines):
        presses = solve_machine(line)
        total_presses += presses

    print(f"Total fewest button presses required: {total_presses}")
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    solve_puzzle()