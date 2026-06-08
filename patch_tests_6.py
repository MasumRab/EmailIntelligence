import re

with open('tests/test_launcher.py', 'r') as f:
    content = f.read()

content = re.sub(r'from setup\.environment import create_venv.*', 'from setup.launch import create_venv', content, flags=re.DOTALL)
content = re.sub(r'from setup\.services import setup_dependencies, download_nltk_data', 'from setup.launch import setup_dependencies, download_nltk_data', content)

with open('tests/test_launcher.py', 'w') as f:
    f.write(content)
