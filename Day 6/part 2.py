import os

def solve_chunk(chunk_cols):
    """
    Part 2 Logic:
    - Each number is given in its own column, with the most significant digit at the top.
    - The operator is located at the bottom of the problem (last row).
    """
    if not chunk_cols:
        return 0
        
    numbers = []
    operator = None
    
    for col in chunk_cols:
        # Check for operator in the last row (bottom-most character of the column)
        last_char = col[-1]
        if last_char in ['+', '*']:
            operator = last_char
            
        # Extract digits from the rest of the column (top to bottom)
        # We slice col[:-1] to exclude the bottom row which contains operators/spaces
        digits = [c for c in col[:-1] if c.isdigit()]
        
        if digits:
            # Join digits to form the number (MSD is at index 0)
            number = int("".join(digits))
            numbers.append(number)
            
    if operator is None or not numbers:
        return 0
        
    # Calculate result
    result = numbers[0]
    for num in numbers[1:]:
        if operator == '+':
            result += num
        elif operator == '*':
            result *= num
            
    return result

def solve_puzzle():
    # Construct path to input.txt
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'input.txt')
    
    try:
        with open(file_path, 'r') as f:
            # Read all lines, but do not strip right-side whitespace yet
            # because we need to preserve column alignment.
            # We strip the newline character at the end though.
            lines = [line.replace('\n', '') for line in f.readlines()]
    except FileNotFoundError:
        print(f"Error: 'input.txt' not found at {file_path}")
        input("\nPress Enter to exit...")
        return

    if not lines:
        print("Input file is empty.")
        return

    # Pad all lines to the maximum length to treat it as a perfect grid
    max_len = max(len(line) for line in lines)
    grid = [line.ljust(max_len) for line in lines]
    
    grand_total = 0
    current_chunk_cols = []
    
    # Iterate through every column index (0 to max_len)
    for col_idx in range(max_len):
        # Extract the vertical column
        col_chars = [row[col_idx] for row in grid]
        
        # Check if the column is entirely spaces (separator)
        is_empty_col = all(c == ' ' for c in col_chars)
        
        if not is_empty_col:
            # It's part of a problem, add to current chunk
            current_chunk_cols.append(col_chars)
        else:
            # It's a separator. If we have a chunk built up, process it.
            if current_chunk_cols:
                grand_total += solve_chunk(current_chunk_cols)
                current_chunk_cols = []
    
    # Process the final chunk if the file didn't end with spaces
    if current_chunk_cols:
        grand_total += solve_chunk(current_chunk_cols)

    print(f"Grand Total (Part 2): {grand_total}")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    solve_puzzle()