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
    def count_paths(start_node, end_node):
        memo = {}

        def _dfs(node):
            if node == end_node:
                return 1
            if node in memo:
                return memo[node]
            if node not in graph:
                return 0
            
            total = 0
            for neighbor in graph[node]:
                total += _dfs(neighbor)
            
            memo[node] = total
            return total

        return _dfs(start_node)
    required_nodes = ['svr', 'dac', 'fft', 'out']
    
    print("Calculating paths for sequence: svr -> dac -> fft -> out")
    paths_svr_dac = count_paths('svr', 'dac')
    paths_dac_fft = count_paths('dac', 'fft')
    paths_fft_out = count_paths('fft', 'out')
    total_case_a = paths_svr_dac * paths_dac_fft * paths_fft_out
    
    print("Calculating paths for sequence: svr -> fft -> dac -> out")
    paths_svr_fft = count_paths('svr', 'fft')
    paths_fft_dac = count_paths('fft', 'dac')
    paths_dac_out = count_paths('dac', 'out')
    total_case_b = paths_svr_fft * paths_fft_dac * paths_dac_out
    total_valid_paths = total_case_a + total_case_b
    
    print(f"\nPath Counts:")
    print(f"  svr -> dac: {paths_svr_dac}")
    print(f"  dac -> fft: {paths_dac_fft}")
    print(f"  fft -> out: {paths_fft_out}")
    print(f"  --> Sequence A Total: {total_case_a}")
    print(f"")
    print(f"  svr -> fft: {paths_svr_fft}")
    print(f"  fft -> dac: {paths_fft_dac}")
    print(f"  dac -> out: {paths_dac_out}")
    print(f"  --> Sequence B Total: {total_case_b}")
    
    print(f"\nTotal paths visiting both 'dac' and 'fft': {total_valid_paths}")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    solve_puzzle()