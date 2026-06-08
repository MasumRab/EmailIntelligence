with open('tests/test_launcher.py', 'r') as f:
    content = f.read()

content = content.replace("from setup.launch import create_venv", "from setup.environment import create_venv")
content = content.replace("from setup.launch import setup_dependencies, download_nltk_data", "from setup.services import setup_dependencies, download_nltk_data")

with open('tests/test_launcher.py', 'w') as f:
    f.write(content)
