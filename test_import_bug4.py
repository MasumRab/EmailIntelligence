#!/usr/bin/env python3
"""
Test script for Bug #4: COMMAND_PATTERN_AVAILABLE undefined variable
"""
import os
import re

print("Testing COMMAND_PATTERN_AVAILABLE variable definition...")

# Check if COMMAND_PATTERN_AVAILABLE is defined anywhere in launch.py
launch_file = os.path.join(os.getcwd(), 'setup', 'launch.py')
if os.path.exists(launch_file):
    print("✓ setup/launch.py exists")
    
    try:
        with open(launch_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Look for COMMAND_PATTERN_AVAILABLE definition
        patterns = [
            r'COMMAND_PATTERN_AVAILABLE\s*=',
            r'COMMAND_PATTERN_AVAILABLE\s*:',
            r'const\s+COMMAND_PATTERN_AVAILABLE',
            r'global\s+COMMAND_PATTERN_AVAILABLE',
            r'class\s+COMMAND_PATTERN_AVAILABLE',
        ]
        
        found_definition = False
        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                print(f"  ✓ Found COMMAND_PATTERN_AVAILABLE definition pattern: {pattern}")
                found_definition = True
                break
        
        if not found_definition:
            print("  ✗ COMMAND_PATTERN_AVAILABLE variable definition NOT FOUND")
        
        # Look for usage of COMMAND_PATTERN_AVAILABLE
        usage_matches = re.findall(r'COMMAND_PATTERN_AVAILABLE', content)
        if usage_matches:
            print(f"  ⚠ COMMAND_PATTERN_AVAILABLE used {len(usage_matches)} times in code")
            
            # Find line numbers where it's used
            lines = content.split('\n')
            usage_lines = []
            for i, line in enumerate(lines, 1):
                if 'COMMAND_PATTERN_AVAILABLE' in line:
                    usage_lines.append((i, line.strip()))
            
            print("  Usage locations:")
            for line_num, line_content in usage_lines:
                print(f"    Line {line_num}: {line_content}")
        else:
            print("  ✗ COMMAND_PATTERN_AVAILABLE not used anywhere")
            
    except Exception as e:
        print(f"  Error reading launch.py: {e}")
else:
    print("✗ setup/launch.py does not exist")

print("\nTesting if the variable is conditionally defined...")
# Look for try-except blocks that might define it
try:
    with open(launch_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Look for conditional definitions
    conditional_patterns = [
        r'try:.*?COMMAND_PATTERN_AVAILABLE.*?except',
        r'except.*?COMMAND_PATTERN_AVAILABLE',
        r'if.*?COMMAND_PATTERN_AVAILABLE',
        r'COMMAND_PATTERN_AVAILABLE.*?if.*?True',
        r'COMMAND_PATTERN_AVAILABLE.*?False',
    ]
    
    found_conditional = False
    for pattern in conditional_patterns:
        matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
        if matches:
            print(f"  ✓ Found conditional definition pattern: {pattern}")
            found_conditional = True
    
    if not found_conditional:
        print("  ✗ No conditional definition patterns found")
        
except Exception as e:
    print(f"  Error in conditional check: {e}")

print("\nTesting if it's defined in other files...")
# Search for COMMAND_PATTERN_AVAILABLE in other files
found_in_other_files = []
for root, dirs, files in os.walk('.'):
    # Skip certain directories
    dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'node_modules', '.pytest_cache']]
    
    for file in files:
        if file.endswith('.py') and file != 'launch.py':
            try:
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    if 'COMMAND_PATTERN_AVAILABLE' in content:
                        found_in_other_files.append(file_path)
                        print(f"  ✓ Found COMMAND_PATTERN_AVAILABLE in {file_path}")
            except Exception:
                continue

if not found_in_other_files:
    print("  ✗ COMMAND_PATTERN_AVAILABLE not found in any other files")

print("\nTesting import-related definitions...")
# Check if it's defined through imports
import_patterns = [
    r'from.*import.*COMMAND_PATTERN_AVAILABLE',
    r'import.*COMMAND_PATTERN_AVAILABLE',
    r'COMMAND_PATTERN_AVAILABLE\s*=\s*import',
]

for pattern in import_patterns:
    try:
        with open(launch_file, 'r', encoding='utf-8') as f:
            content = f.read()
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            print(f"  ✓ Found import definition: {pattern}")
    except Exception:
        continue

print("\nAnalyzing the undefined variable issue...")
# Try to identify what COMMAND_PATTERN_AVAILABLE should be
try:
    with open(launch_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Look for the context where it's used
    usage_context = re.search(r'if\s+COMMAND_PATTERN_AVAILABLE.*?:', content)
    if usage_context:
        context_lines = usage_context.group(0).split('\n')
        print("  Usage context:")
        for line in context_lines:
            if line.strip():
                print(f"    {line.strip()}")
    
    # Check what it might be checking
    print("  Analysis: COMMAND_PATTERN_AVAILABLE appears to be a boolean flag")
    print("  Likely purpose: Check if command pattern imports are available")
    print("  Issue: Variable defined but never initialized")
        
except Exception as e:
    print(f"  Error in context analysis: {e}")

print("\nTesting potential fix - checking for import success pattern...")
# Look for import blocks that might set this flag
import_blocks = re.findall(r'try:.*?import.*?except.*?:', content, re.DOTALL)
for i, block in enumerate(import_blocks):
    print(f"  Import block {i+1}:")
    lines = block.split('\n')[:3]  # Show first 3 lines
    for line in lines:
        if line.strip():
            print(f"    {line.strip()}")
    print("    ...")
    print("")