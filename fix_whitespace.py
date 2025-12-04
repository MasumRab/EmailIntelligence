
import sys
import os

def strip_trailing_whitespace(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = [line.rstrip() + '\n' for line in lines]
    
    # Preserve the last line if it doesn't have a newline (though rstrip() + '\n' adds it)
    # Actually, standard text files should end with newline.
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print(f"Processed {file_path}")

if __name__ == "__main__":
    for file_path in sys.argv[1:]:
        strip_trailing_whitespace(file_path)
