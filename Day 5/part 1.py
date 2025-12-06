import os

def solve_puzzle():
    # Construct path to input.txt
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'input.txt')
    
    ranges = []
    ids = []
    reading_ranges = True
    
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            
        for line in lines:
            line = line.strip()
            
            # Check for the blank line separator
            if not line:
                # The first blank line switches us from reading ranges to reading IDs
                if reading_ranges and len(ranges) > 0:
                    reading_ranges = False
                continue
            
            if reading_ranges:
                # Parse range like "3-5"
                if '-' in line:
                    start_str, end_str = line.split('-')
                    ranges.append((int(start_str), int(end_str)))
                else:
                    print(f"Warning: Unexpected format in ranges section: '{line}'")
            else:
                # Parse available ID like "5"
                ids.append(int(line))
                
    except FileNotFoundError:
        print(f"Error: 'input.txt' not found at {file_path}")
        input("\nPress Enter to exit...")
        return
    except ValueError as e:
        print(f"Error parsing input: {e}")
        input("\nPress Enter to exit...")
        return

    print(f"Found {len(ranges)} ranges and {len(ids)} IDs to check.")

    fresh_count = 0
    
    for ingredient_id in ids:
        is_fresh = False
        # Check if the ID falls into ANY of the ranges
        for start, end in ranges:
            if start <= ingredient_id <= end:
                is_fresh = True
                break # Found a valid range, no need to check others for this ID
        
        if is_fresh:
            fresh_count += 1
            # print(f"ID {ingredient_id} is fresh") # Debug

    print(f"Total fresh ingredient IDs: {fresh_count}")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    solve_puzzle()