import os

def is_invalid_id(number):
    """
    Checks if a number is an 'invalid ID' based on Part Two rules.
    An invalid ID is made only of some sequence of digits repeated 
    AT LEAST twice.
    
    Examples: 
      - 55 (5 repeated 2 times) -> Valid match
      - 123123123 (123 repeated 3 times) -> Valid match
      - 1111111 (1 repeated 7 times) -> Valid match
    """
    s = str(number)
    length = len(s)
    
    # We try every possible pattern length, from 1 digit up to half the string.
    # We stop at length // 2 because a pattern must repeat at least twice,
    # so the pattern length cannot be more than half the total length.
    for pattern_len in range(1, length // 2 + 1):
        
        # Optimization: The total length must be divisible by the pattern length
        # for it to repeat perfectly.
        if length % pattern_len == 0:
            pattern = s[:pattern_len]
            repetitions = length // pattern_len
            
            # Check if repeating this pattern recreates the original string
            if pattern * repetitions == s:
                return True
                
    return False

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

    print(f"Processing {len(range_strings)} ranges with Part 2 rules...")

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

    print(f"\nSum of all invalid IDs (Part 2): {total_invalid_sum}")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    solve_puzzle()