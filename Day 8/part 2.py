import os
import math

class UnionFind:
    def __init__(self, size):
        self.parent = list(range(size))
        self.size = [1] * size
        self.num_components = size

    def find(self, i):
        if self.parent[i] != i:
            self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i, j):
        root_i = self.find(i)
        root_j = self.find(j)

        if root_i != root_j:
            if self.size[root_i] < self.size[root_j]:
                root_i, root_j = root_j, root_i
            
            self.parent[root_j] = root_i
            self.size[root_i] += self.size[root_j]
            self.num_components -= 1
            return True
        return False

def solve_puzzle():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'input.txt')
    
    points = []
    
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                # Parse "X,Y,Z"
                parts = list(map(int, line.split(',')))
                points.append(tuple(parts))
    except FileNotFoundError:
        print(f"Error: 'input.txt' not found at {file_path}")
        input("\nPress Enter to exit...")
        return
    except ValueError:
        print("Error: Invalid input format. Expected X,Y,Z integers.")
        return

    n = len(points)
    print(f"Found {n} junction boxes.")
    
    if n < 2:
        print("Not enough points to form connections.")
        return

    edges = []
    for i in range(n):
        p1 = points[i]
        for j in range(i + 1, n):
            p2 = points[j]
            dist_sq = (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2
            edges.append((dist_sq, i, j))

    print(f"Generated {len(edges)} possible connections. Sorting...")
    
    edges.sort(key=lambda x: x[0])
    
    uf = UnionFind(n)
    
    for dist_sq, u, v in edges:
        if uf.union(u, v):
            if uf.num_components == 1:
                p1 = points[u]
                p2 = points[v]
                print(f"\nFinal connection made between:")
                print(f"Box {u}: {p1}")
                print(f"Box {v}: {p2}")
            
                ans = p1[0] * p2[0]
                print(f"Product of X coordinates (Part 2 Answer): {ans}")
                break
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    solve_puzzle()