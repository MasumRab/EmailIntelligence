with open('tests/test_launcher.py', 'r') as f:
    content = f.read()

content = content.replace("from setup.environment import create_venv", "")

with open('tests/test_launcher.py', 'w') as f:
    f.write(content)
