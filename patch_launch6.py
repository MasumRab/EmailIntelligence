with open("setup/launch.py", "r", encoding="utf-8") as f:
    text = f.read()

# Replace all potential problematic docstrings with comments just to be safe
text = text.replace('"""Handle legacy argument parsing for backward compatibility."""', '# Handle legacy argument parsing for backward compatibility.')

with open("setup/launch.py", "w", encoding="utf-8") as f:
    f.write(text)
