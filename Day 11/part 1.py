import os
import sys

# Increase recursion depth just in case the path is very long
sys.setrecursionlimit(5000)

def solve_puzzle():
    # Construct path to input.txt
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'input.txt')
    
    graph = {}
    
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                # Parse format "node: dest1 dest2 ..."
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
    
    # Memoization cache to store path counts from a specific node to 'out'
    memo = {}

    def count_paths(node):
        # Base Case: We reached the target
        if node == 'out':
            return 1
        
        # If we've already computed the paths from this node, return cached value
        if node in memo:
            return memo[node]
        
        # If this node has no outgoing connections (dead end)
        if node not in graph:
            return 0
        
        total_paths = 0
        for neighbor in graph[node]:
            total_paths += count_paths(neighbor)
            
        # Cache and return
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