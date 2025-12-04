import os

def solve_bank(bank_string):

    length = len(bank_string)
    needed = 12
    
    if length < needed:
        print(f"Warning: Bank '{bank_string}' is too short ({length}) to pick {needed} digits.")
        return 0
        
    result = []
    current_pos = 0
    
    while needed > 0:
        
        search_limit = length - needed
        best_digit = '0'
        best_index = -1
        
        for i in range(current_pos, search_limit + 1):
            char = bank_string[i]
            if char > best_digit:
                best_digit = char
                best_index = i
                if char == '9':
                    break
        
        result.append(best_digit)
        current_pos = best_index + 1
        needed -= 1
        
    return int("".join(result))

def solve_puzzle():
    total_joltage = 0
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'input.txt')
    
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: 'input.txt' not found at {file_path}")
        input("\nPress Enter to exit...")
        return

    print("Processing banks for Part 2 (12 digits)...")

    for line in lines:
        stripped_line = line.strip()
        if not stripped_line:
            continue
            
        bank_max = solve_bank(stripped_line)
        total_joltage += bank_max

    print(f"\nTotal Output Joltage: {total_joltage}")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    solve_puzzle()