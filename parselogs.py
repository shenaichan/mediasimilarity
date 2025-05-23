def process_file_preview(input_file):
    """
    Find lines that would be removed and convert them to numbers for printing.
    Accumulates all lines to be deleted in an array.
    """
    
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    lines_to_delete = []  # Array to accumulate lines to be deleted
    i = 0
    
    while i + 2 < len(lines):
        next_line = lines[i + 1].strip()
        line_after_next = lines[i + 2].strip().lower()
        
        if next_line == "404" and line_after_next.startswith("deleted"):
            lines_to_delete.append(int(lines[i].strip()))  # Add the line content to array
            i += 3
            continue
        
        i += 1
    
    print(f"Total lines found: {len(lines_to_delete)}")
    return lines_to_delete

# Example usage:
if __name__ == "__main__":
    file_path = 'logs.txt'
    deleted_lines_array = process_file_preview(file_path)
    print(deleted_lines_array)