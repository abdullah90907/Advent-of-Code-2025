import os
import sys
from collections import deque

def solve_puzzle():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'input.txt')
    
    points = []
    
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                # Parse "X,Y"
                parts = list(map(int, line.split(',')))
                points.append(tuple(parts))
    except FileNotFoundError:
        print(f"Error: 'input.txt' not found at {file_path}")
        input("\nPress Enter to exit...")
        return
    except ValueError:
        print("Error: Invalid input format. Expected X,Y integers.")
        return

    n = len(points)
    print(f"Found {n} red tiles.")
    
    if n < 2:
        print("Not enough tiles to form a rectangle.")
        return

    raw_xs = set(p[0] for p in points)
    raw_ys = set(p[1] for p in points)

    min_x, max_x = min(raw_xs), max(raw_xs)
    min_y, max_y = min(raw_ys), max(raw_ys)
    raw_xs.add(min_x - 1)
    raw_xs.add(max_x + 1)
    raw_ys.add(min_y - 1)
    raw_ys.add(max_y + 1)
    

    sorted_xs = sorted(list(raw_xs))
    sorted_ys = sorted(list(raw_ys))

    x_map = {val: i for i, val in enumerate(sorted_xs)}
    y_map = {val: i for i, val in enumerate(sorted_ys)}
    
    col_widths = []
    for i in range(len(sorted_xs)):
        col_widths.append(1) 
        if i < len(sorted_xs) - 1:
            gap = sorted_xs[i+1] - sorted_xs[i] - 1
            col_widths.append(gap)
            
    row_heights = []
    for i in range(len(sorted_ys)):
        row_heights.append(1) 
        if i < len(sorted_ys) - 1:
            gap = sorted_ys[i+1] - sorted_ys[i] - 1
            row_heights.append(gap) 

    grid_w = len(col_widths)
    grid_h = len(row_heights)
    
    grid = [[0 for _ in range(grid_w)] for _ in range(grid_h)]
    def get_compressed_idx(real_val, mapping):
        return mapping[real_val] * 2

    for i in range(n):
        curr_p = points[i]
        next_p = points[(i + 1) % n]
        
        c1 = get_compressed_idx(curr_p[0], x_map)
        r1 = get_compressed_idx(curr_p[1], y_map)
        c2 = get_compressed_idx(next_p[0], x_map)
        r2 = get_compressed_idx(next_p[1], y_map)
        
        if c1 == c2: 
            r_start, r_end = min(r1, r2), max(r1, r2)
            for r in range(r_start, r_end + 1):
                grid[r][c1] = 1
        else: 
            c_start, c_end = min(c1, c2), max(c1, c2)
            for c in range(c_start, c_end + 1):
                grid[r1][c] = 1

    q = deque([(0, 0)])
    grid[0][0] = 2 
    
    while q:
        r, c = q.popleft()
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < grid_h and 0 <= nc < grid_w:
                if grid[nr][nc] == 0:
                    grid[nr][nc] = 2 
                    q.append((nr, nc))
    
    integral_area = [[0 for _ in range(grid_w + 1)] for _ in range(grid_h + 1)]
    
    for r in range(grid_h):
        for c in range(grid_w):
            is_valid = grid[r][c] != 2
            cell_area = (col_widths[c] * row_heights[r]) if is_valid else 0
            
            integral_area[r+1][c+1] = cell_area + \
                                      integral_area[r][c+1] + \
                                      integral_area[r+1][c] - \
                                      integral_area[r][c]

    def get_valid_area_in_rect(c_start, r_start, c_end, r_end):
        c_min, c_max = min(c_start, c_end), max(c_start, c_end)
        r_min, r_max = min(r_start, r_end), max(r_start, r_end)
        
        return integral_area[r_max+1][c_max+1] - \
               integral_area[r_min][c_max+1] - \
               integral_area[r_max+1][c_min] + \
               integral_area[r_min][c_min]


    max_area = 0
    print("Checking rectangles with compressed grid...")

    for i in range(n):
        x1, y1 = points[i]
        c1 = get_compressed_idx(x1, x_map)
        r1 = get_compressed_idx(y1, y_map)
        
        for j in range(i + 1, n):
            x2, y2 = points[j]
            c2 = get_compressed_idx(x2, x_map)
            r2 = get_compressed_idx(y2, y_map)
            width = abs(x1 - x2) + 1
            height = abs(y1 - y2) + 1
            total_geo_area = width * height
            
            valid_area = get_valid_area_in_rect(c1, r1, c2, r2)
            
            if valid_area == total_geo_area:
                if total_geo_area > max_area:
                    max_area = total_geo_area

    print(f"Largest valid rectangle area (Red/Green only): {max_area}")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    solve_puzzle()