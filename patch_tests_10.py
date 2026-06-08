with open('tests/test_launcher.py', 'r') as f:
    content = f.read()

content = content.replace('setup.launch.create_venv(', 'create_venv(')
content = content.replace('setup.launch.setup_dependencies(', 'setup_dependencies(')
content = content.replace('setup.launch.download_nltk_data(', 'download_nltk_data(')
content = content.replace('setup.launch.check_python_version()', 'check_python_version()')

with open('tests/test_launcher.py', 'w') as f:
    f.write(content)
