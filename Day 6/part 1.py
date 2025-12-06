import os

def solve_chunk(chunk_cols):
    """
    Takes a list of strings, where each string is a vertical column from the file.
    We need to parse this block to find numbers and the operator.
    """
    if not chunk_cols:
        return 0
        
    num_rows = len(chunk_cols[0])
    numbers = []
    operator = None
    
    for r in range(num_rows):
        row_str = "".join(col[r] for col in chunk_cols).strip()
        
        if not row_str:
            continue
            
        if row_str == '+':
            operator = '+'
        elif row_str == '*':
            operator = '*'
        else:
            try:
                numbers.append(int(row_str))
            except ValueError:
                pass
    
    if operator is None or not numbers:
        return 0
        
    result = numbers[0]
    for num in numbers[1:]:
        if operator == '+':
            result += num
        elif operator == '*':
            result *= num
            
    return result

def solve_puzzle():
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
    max_len = max(len(line) for line in lines)
    grid = [line.ljust(max_len) for line in lines]
    
    grand_total = 0
    current_chunk_cols = []
    
    for col_idx in range(max_len):
        col_chars = [row[col_idx] for row in grid]
        
        is_empty_col = all(c == ' ' for c in col_chars)
        
        if not is_empty_col:
            current_chunk_cols.append(col_chars)
        else:
            if current_chunk_cols:
                grand_total += solve_chunk(current_chunk_cols)
                current_chunk_cols = []
    
    if current_chunk_cols:
        grand_total += solve_chunk(current_chunk_cols)

    print(f"Grand Total: {grand_total}")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    solve_puzzle()