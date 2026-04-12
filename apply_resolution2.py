import re

with open("setup/launch.py", "r") as f:
    lines = f.readlines()

new_lines = []
state = 0 # 0=normal, 1=in HEAD, 2=in new

for line in lines:
    if line.startswith("<<<<<<< HEAD"):
        state = 1
        continue
    elif line.startswith("======="):
        state = 2
        continue
    elif line.startswith(">>>>>>>"):
        state = 0
        continue
        
    if state == 0 or state == 2:
        # Keep the new changes, not the HEAD
        new_lines.append(line)

with open("setup/launch.py", "w") as f:
    f.writelines(new_lines)
