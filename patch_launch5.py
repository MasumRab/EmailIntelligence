import re
with open("setup/launch.py", "r", encoding="utf-8") as f:
    text = f.read()

# Replace the specific malformed triple-quotes line entirely with a safe simple string to completely eliminate the issue
text = text.replace('        """Check for common setup issues and warn users."""', '    # Check for common setup issues and warn users.')

with open("setup/launch.py", "w", encoding="utf-8") as f:
    f.write(text)
