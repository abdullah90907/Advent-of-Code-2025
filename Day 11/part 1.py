import os
import sys
sys.setrecursionlimit(5000)

def solve_puzzle():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'input.txt')
    
    graph = {}
    
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if ':' in line:
                    source, dests_str = line.split(':')
                    source = source.strip()
                    dests = [d.strip() for d in dests_str.strip().split(' ') if d.strip()]
                    graph[source] = dests
                else:
                    print(f"Skipping malformed line: {line}")
                    
    except FileNotFoundError:
        print(f"Error: 'input.txt' not found at {file_path}")
        input("\nPress Enter to exit...")
        return

    print(f"Graph built with {len(graph)} nodes.")
    memo = {}

    def count_paths(node):
        if node == 'out':
            return 1
        
        if node in memo:
            return memo[node]
        if node not in graph:
            return 0
        
        total_paths = 0
        for neighbor in graph[node]:
            total_paths += count_paths(neighbor)
        memo[node] = total_paths
        return total_paths

    if 'you' not in graph:
        print("Error: Start node 'you' not found in input.")
        return

    result = count_paths('you')
    
    print(f"Total paths from 'you' to 'out': {result}")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    solve_puzzle()