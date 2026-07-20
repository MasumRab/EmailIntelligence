with open('tests/test_launcher.py', 'r') as f:
    content = f.read()

content = content.replace("if False: as mock_add_process:", "if False:")

with open('tests/test_launcher.py', 'w') as f:
    f.write(content)
