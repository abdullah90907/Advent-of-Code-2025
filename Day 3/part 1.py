import os

def solve_bank(bank_string):
    max_joltage = -1
    length = len(bank_string)
    
    for i in range(length):
        for j in range(i + 1, length):
            digit1 = bank_string[i]
            digit2 = bank_string[j]

            current_val = int(digit1 + digit2)
            
            if current_val > max_joltage:
                max_joltage = current_val
                
    return max_joltage

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

    print("Processing banks...")

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