import re

with open('.mergify.yml', 'r') as f:
    content = f.read()

# Replace the block entirely by removing commit_message or commit_message_format
new_content = re.sub(
    r'\s*commit_message: default',
    '',
    content
)

with open('.mergify.yml', 'w') as f:
    f.write(new_content)
