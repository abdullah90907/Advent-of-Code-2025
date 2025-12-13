import os

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
                # Parse "X,Y"
                parts = list(map(int, line.split(',')))
                points.append(tuple(parts))
    except FileNotFoundError:
        print(f"Error: 'input.txt' not found at {file_path}")
        input("\nPress Enter to exit...")
        return
    except ValueError:
        print("Error: Invalid input format. Expected X,Y integers.")
        return

    n = len(points)
    print(f"Found {n} red tiles.")
    
    if n < 2:
        print("Not enough tiles to form a rectangle.")
        return

    max_area = 0

    for i in range(n):
        x1, y1 = points[i]
        for j in range(i + 1, n):
            x2, y2 = points[j]
            width = abs(x1 - x2) + 1
            height = abs(y1 - y2) + 1
            
            area = width * height
            
            if area > max_area:
                max_area = area
    print(f"Largest rectangle area: {max_area}")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    solve_puzzle()