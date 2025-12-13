import os
import sys

# Increase recursion depth for deep backtracking
sys.setrecursionlimit(5000)

def parse_shape(lines):
    """
    Parses a shape definition into a set of (r, c) coordinates.
    Normalizes coordinates so the top-left of the bounding box is (0,0).
    """
    coords = set()
    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            if char == '#':
                coords.add((r, c))
    
    if not coords:
        return frozenset()

    # Normalize
    min_r = min(r for r, c in coords)
    min_c = min(c for r, c in coords)
    normalized = set()
    for r, c in coords:
        normalized.add((r - min_r, c - min_c))
    
    return frozenset(normalized)

def get_variations(shape_coords):
    """
    Generates all unique rotations and flips of a shape.
    Returns a list of shapes (each shape is a set of coords).
    """
    variations = set()
    
    current = shape_coords
    
    # Try all 4 rotations for the original
    for _ in range(4):
        # Normalize current
        if not current:
            variations.add(frozenset())
            break
            
        min_r = min(r for r, c in current)
        min_c = min(c for r, c in current)
        norm = frozenset((r - min_r, c - min_c) for r, c in current)
        variations.add(norm)
        
        # Rotate 90 deg clockwise: (r, c) -> (c, -r)
        current = set((c, -r) for r, c in current)

    # Flip horizontally: (r, c) -> (r, -c)
    flipped = set((r, -c) for r, c in shape_coords)
    current = flipped
    
    # Try all 4 rotations for the flipped version
    for _ in range(4):
        if not current:
            variations.add(frozenset())
            break
            
        min_r = min(r for r, c in current)
        min_c = min(c for r, c in current)
        norm = frozenset((r - min_r, c - min_c) for r, c in current)
        variations.add(norm)
        
        # Rotate
        current = set((c, -r) for r, c in current)
        
    return list(variations)

def solve_region(width, height, presents_to_fit, shapes_variations):
    """
    Backtracking solver to check if presents fit.
    
    width, height: dimensions of region
    presents_to_fit: list of shape_indices (e.g., [4, 4, 0, 2, ...])
    shapes_variations: dict {shape_index: list of variation_sets}
    """
    
    # Grid state: 1D boolean array
    # True = occupied, False = empty
    grid = [False] * (width * height)
    
    # Sort presents by size (area) descending to fail fast
    # Each item in `presents` is (shape_index, area)
    # Actually, we just need the shape_index, but sorting helps.
    
    # Calculate area for sorting
    present_areas = []
    for p_idx in presents_to_fit:
        # Area is len of any variation
        area = len(shapes_variations[p_idx][0])
        present_areas.append((p_idx, area))
    
    # Sort: Largest area first
    present_areas.sort(key=lambda x: x[1], reverse=True)
    sorted_presents = [p[0] for p in present_areas]
    
    # Optimization: Check if total area > grid area
    total_area = sum(p[1] for p in present_areas)
    if total_area > width * height:
        return False
        
    num_presents = len(sorted_presents)
    
    def can_fit(idx, start_pos_hint):
        """
        idx: index in sorted_presents
        start_pos_hint: optimization for identical pieces
        """
        if idx == num_presents:
            return True
            
        shape_idx = sorted_presents[idx]
        variations = shapes_variations[shape_idx]
        
        # Optimization: If this piece is same as previous, ensure we place it
        # after the previous one to avoid symmetric duplicate searches.
        start_pos = 0
        if idx > 0 and sorted_presents[idx] == sorted_presents[idx-1]:
            start_pos = start_pos_hint
            
        # Try to place this present
        # Iterate over all grid positions (top-left of bounding box)
        for pos in range(start_pos, width * height):
            # Convert 1D pos to r, c
            r_origin = pos // width
            c_origin = pos % width
            
            # Try all variations
            for var in variations:
                # Check if this variation fits at (r_origin, c_origin)
                fits = True
                
                # We also need to check boundaries.
                # Since var coords are normalized (0,0 is min), we add r_origin, c_origin
                
                # Pre-check bounds of bounding box to save time?
                # var has max_r, max_c.
                # if r_origin + max_r >= height or c_origin + max_c >= width: continue
                
                occupied_indices = []
                
                for pr, pc in var:
                    nr, nc = r_origin + pr, c_origin + pc
                    
                    if not (0 <= nr < height and 0 <= nc < width):
                        fits = False
                        break
                        
                    grid_idx = nr * width + nc
                    if grid[grid_idx]:
                        fits = False
                        break
                    
                    occupied_indices.append(grid_idx)
                
                if fits:
                    # Place it
                    for g_idx in occupied_indices:
                        grid[g_idx] = True
                    
                    # Recurse
                    # Pass 'pos' as hint for next piece if it's identical
                    if can_fit(idx + 1, pos): 
                        return True
                    
                    # Backtrack
                    for g_idx in occupied_indices:
                        grid[g_idx] = False
                        
        return False

    return can_fit(0, 0)

def solve_puzzle():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'input.txt')
    
    raw_shapes = {} # id -> list of strings
    regions = [] # (w, h, present_counts)
    
    try:
        with open(file_path, 'r') as f:
            lines = [line.rstrip() for line in f]
            
        i = 0
        while i < len(lines):
            line = lines[i]
            if not line:
                i += 1
                continue
                
            if ':' in line:
                header = line.split(':')[0]
                
                if 'x' in header:
                    # It's a region: "12x5: 1 0 1..."
                    dims, counts_str = line.split(':')
                    w_str, h_str = dims.split('x')
                    width, height = int(w_str), int(h_str)
                    counts = list(map(int, counts_str.strip().split()))
                    regions.append((width, height, counts))
                    i += 1
                else:
                    # It's a shape: "0:"
                    shape_id = int(header)
                    shape_lines = []
                    i += 1
                    while i < len(lines) and lines[i].strip() and ':' not in lines[i]:
                        shape_lines.append(lines[i])
                        i += 1
                    raw_shapes[shape_id] = shape_lines
            else:
                i += 1
                
    except FileNotFoundError:
        print(f"Error: 'input.txt' not found at {file_path}")
        return

    print(f"Parsed {len(raw_shapes)} shapes and {len(regions)} regions.")
    
    # 1. Precompute Variations
    shapes_variations = {}
    for sid, lines in raw_shapes.items():
        base_shape = parse_shape(lines)
        vars_list = get_variations(base_shape)
        shapes_variations[sid] = vars_list
        # print(f"Shape {sid}: {len(vars_list)} variations")

    success_count = 0
    
    # 2. Solve Each Region
    for r_idx, (w, h, counts) in enumerate(regions):
        # Construct list of presents to place
        presents_to_fit = []
        for shape_id, count in enumerate(counts):
            # Check if shape_id exists in our shapes
            if count > 0:
                if shape_id not in shapes_variations:
                    print(f"Warning: Region asks for shape {shape_id} which is not defined.")
                    # Treat as impossible? Or ignore? Assuming impossible if shape missing.
                    presents_to_fit = None 
                    break
                presents_to_fit.extend([shape_id] * count)
        
        if presents_to_fit is None:
            print(f"Region {r_idx} ({w}x{h}): Impossible (missing shape def)")
            continue
            
        print(f"Checking Region {r_idx} ({w}x{h})... ", end='', flush=True)
        
        if solve_region(w, h, presents_to_fit, shapes_variations):
            print("Fits!")
            success_count += 1
        else:
            print("Does not fit.")
            
    print(f"\nTotal regions that can fit all presents: {success_count}")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    solve_puzzle()