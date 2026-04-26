with open('tests/test_launcher.py', 'r') as f:
    content = f.read()

content = content.replace('patch("launch.Path.exists"', 'patch("pathlib.Path.exists"')

with open('tests/test_launcher.py', 'w') as f:
    f.write(content)
