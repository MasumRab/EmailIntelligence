with open("setup/launch.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Ah I see it, lines 17-29 is completely outside of a docstring correctly or it's duplicated.
# Let's just fix the top of the file cleanly.

new_lines = lines[:13] + lines[30:]

with open("setup/launch.py", "w", encoding="utf-8") as f:
    f.writelines(new_lines)
