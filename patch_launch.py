import re

with open('setup/launch.py', 'r') as f:
    content = f.read()

# remove merge conflict markers from the file
content = re.sub(r'<<<<<<< HEAD\n', '', content)
content = re.sub(r'=======\n', '', content)
content = re.sub(r'>>>>>>> .+\n', '', content)

with open('setup/launch.py', 'w') as f:
    f.write(content)
