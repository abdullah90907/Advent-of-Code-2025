import os
import re
from pulp import *

def parse_line(line):
    """Parse machine line to extract buttons and target joltage levels."""
    target_match = re.search(r'\{([\d,]+)\}', line)
    if not target_match:
        return None
    
    targets = list(map(int, target_match.group(1).split(',')))
    button_matches = re.findall(r'\(([\d,]*)\)', line)
    buttons = []
    for btn_str in button_matches:
        if btn_str:
            buttons.append(list(map(int, btn_str.split(','))))
        else:
            buttons.append([])
    
    return buttons, targets

def min_presses(buttons, targets):
    """Find minimum button presses using integer linear programming."""
    n = len(targets)
    m = len(buttons)  
    
    if m == 0:
        return 0 if all(t == 0 for t in targets) else -1

    prob = LpProblem("MinButtonPresses", LpMinimize)
    button_presses = [LpVariable(f"button_{i}", lowBound=0, cat='Integer') for i in range(m)]
    
    prob += lpSum(button_presses)
    
    for counter_idx in range(n):
        counter_sum = lpSum([button_presses[btn_idx] 
                            for btn_idx in range(m) 
                            if counter_idx in buttons[btn_idx]])
        prob += counter_sum == targets[counter_idx], f"counter_{counter_idx}"
    
    prob.solve(PULP_CBC_CMD(msg=0))
    
    if prob.status == 1:
        total = sum(int(button_presses[i].varValue) for i in range(m))
        return total
    else:
        return -1

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
    
    for i, line in enumerate(lines, 1):
        parsed = parse_line(line)
        if parsed:
            buttons, targets = parsed
            presses = min_presses(buttons, targets)
            if presses == -1:
                print(f"Warning: No solution for machine {i}")
            else:
                total_presses += presses
    
    print(f"\nTotal fewest button presses required: {total_presses}")
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    solve_puzzle()