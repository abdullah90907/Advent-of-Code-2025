import os

def solve_puzzle():
    current_pos = 50
    zero_hits = 0
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'input.txt')
    
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: 'input.txt' not found at {file_path}")
        print("Please create the file with your puzzle input in the same folder.")
        input("\nPress Enter to exit...")
        return

    print(f"Starting Position: {current_pos}")

    for line in lines:
        instruction = line.strip()
        if not instruction:
            continue
            
        direction = instruction[0]
        amount = int(instruction[1:])
        
        zero_hits += amount // 100
        
        remainder = amount % 100
        
        if direction == 'L':
            if current_pos > 0 and remainder >= current_pos:
                zero_hits += 1
            
            current_pos = (current_pos - remainder) % 100
            
        elif direction == 'R':
            if current_pos + remainder >= 100:
                zero_hits += 1
                
            current_pos = (current_pos + remainder) % 100

    print(f"Final Password (Part 2): {zero_hits}")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    solve_puzzle()