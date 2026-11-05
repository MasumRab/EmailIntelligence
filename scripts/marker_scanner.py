import os
import re
import sys
from dataclasses import dataclass
from typing import List

@dataclass
class Marker:
    filepath: str
    line_number: int
    marker_type: str
    content: str
    
    @property
    def priority(self) -> int:
        return 0 if self.marker_type == "FIX" + "ME" else 1

def scan_directory(directory: str) -> List[Marker]:
    markers = []
    # Avoid flagging our own script
    target_pattern = re.compile(r'\b(FIX' + r'ME|TO' + r'DO)\b:?\s*(.*)', re.IGNORECASE)
    
    for root, _, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            # Skip this script itself and the test script just in case
            if "marker_scanner" in file:
                continue
                
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    for i, line in enumerate(f, 1):
                        match = target_pattern.search(line)
                        if match:
                            m_type = match.group(1).upper()
                            content = match.group(2).strip()
                            markers.append(Marker(
                                filepath=filepath,
                                line_number=i,
                                marker_type=m_type,
                                content=content
                            ))
            except UnicodeDecodeError:
                pass # Skip binary files
                
    return sorted(markers, key=lambda m: (m.priority, m.filepath, m.line_number))

def main():
    target_dir = sys.argv[1] if len(sys.argv) > 1 else 'scripts'
    if not os.path.isdir(target_dir):
        print(f"Error: Directory '{target_dir}' does not exist.")
        sys.exit(1)
        
    markers = scan_directory(target_dir)
    
    print(f"Found {len(markers)} markers in {target_dir}/")
    print("-" * 50)
    for m in markers:
        print(f"[{m.marker_type}] {m.filepath}:{m.line_number} - {m.content}")

if __name__ == "__main__":
    main()
