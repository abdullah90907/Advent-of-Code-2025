import os

def solve_puzzle():
    # Construct path to input.txt
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'input.txt')
    
    ranges = []
    
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            
        for line in lines:
            line = line.strip()
            
            # If we hit an empty line, we can stop, as the rest is the ID list 
            # which is irrelevant for Part 2.
            if not line:
                if ranges: # If we already found ranges, we are done
                    break
                else:
                    continue # Skip leading blank lines
            
            # Parse range like "3-5"
            if '-' in line:
                try:
                    start_str, end_str = line.split('-')
                    ranges.append((int(start_str), int(end_str)))
                except ValueError:
                    print(f"Skipping malformed range: {line}")
            else:
                # This might be the start of the ID list if there was no blank line
                # But typically the format is strict. We'll ignore non-ranges.
                pass
                
    except FileNotFoundError:
        print(f"Error: 'input.txt' not found at {file_path}")
        input("\nPress Enter to exit...")
        return

    if not ranges:
        print("No ranges found.")
        input("\nPress Enter to exit...")
        return

    # Part 2 Logic: Calculate the union of all ranges
    
    # 1. Sort ranges by their start value
    ranges.sort(key=lambda x: x[0])
    
    merged_ranges = []
    
    # 2. Merge overlapping or adjacent intervals
    if ranges:
        current_start, current_end = ranges[0]
        
        for i in range(1, len(ranges)):
            next_start, next_end = ranges[i]
            
            # Check if the next range overlaps with or is adjacent to the current range.
            # Example: [10, 14] and [12, 18] overlap.
            # Example: [1, 2] and [3, 4] are adjacent and form a contiguous block [1, 4].
            if next_start <= current_end + 1:
                # Merge them by extending the current end to the max of both
                current_end = max(current_end, next_end)
            else:
                # No overlap/adjacency, finalize the current range and start a new one
                merged_ranges.append((current_start, current_end))
                current_start, current_end = next_start, next_end
        
        # Append the final range
        merged_ranges.append((current_start, current_end))

    # 3. Calculate total count of integers in the merged ranges
    total_fresh_count = 0
    for start, end in merged_ranges:
        # Range is inclusive, so count is end - start + 1
        total_fresh_count += (end - start + 1)

    print(f"Processing {len(ranges)} input ranges.")
    print(f"Total unique fresh ingredient IDs (Part 2): {total_fresh_count}")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    solve_puzzle()