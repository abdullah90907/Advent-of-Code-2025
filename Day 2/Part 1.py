import os

def is_invalid_id(number):
    """
    Checks if a number is an 'invalid ID'.
    An invalid ID is made only of some sequence of digits repeated twice.
    Examples: 55 (5,5), 6464 (64,64), 123123 (123,123)
    """
    s = str(number)
    length = len(s)
    
    # Must have even length to be split into two equal repeating parts
    if length % 2 != 0:
        return False
    
    mid = length // 2
    first_half = s[:mid]
    second_half = s[mid:]
    
    return first_half == second_half

def solve_puzzle():
    total_invalid_sum = 0
    
    # Construct path to input.txt
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'input.txt')
    
    try:
        with open(file_path, 'r') as f:
            # Read the whole file. The puzzle says it's a single line, 
            # but we remove newlines just in case.
            content = f.read().replace('\n', '').strip()
    except FileNotFoundError:
        print(f"Error: 'input.txt' not found at {file_path}")
        input("\nPress Enter to exit...")
        return

    # Split the content by commas to get individual ranges
    # Filter out empty strings in case of trailing commas
    range_strings = [x for x in content.split(',') if x]

    print(f"Processing {len(range_strings)} ranges...")

    for range_str in range_strings:
        try:
            # Parse "start-end"
            start_str, end_str = range_str.split('-')
            start = int(start_str)
            end = int(end_str)
            
            # Check every number in the range (inclusive)
            for num in range(start, end + 1):
                if is_invalid_id(num):
                    # print(f"Found invalid ID: {num}") # Uncomment to see individual hits
                    total_invalid_sum += num
                    
        except ValueError:
            print(f"Skipping malformed range: {range_str}")
            continue

    print(f"\nSum of all invalid IDs: {total_invalid_sum}")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    solve_puzzle()