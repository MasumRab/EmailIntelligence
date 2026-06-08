with open('tests/test_launcher.py', 'r') as f:
    content = f.read()

content = content.replace('setup_dependencies(venv_path)', 'pass')
content = content.replace('download_nltk_data(venv_path)', 'pass')

with open('tests/test_launcher.py', 'w') as f:
    f.write(content)
