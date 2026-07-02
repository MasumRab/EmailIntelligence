import re
with open('tests/test_launcher.py', 'r') as f:
    content = f.read()

content = content.replace("from setup.launch import ROOT_DIR, main, start_gradio_ui", "from setup.launch import ROOT_DIR, main, start_gradio_ui\nfrom setup.environment import create_venv\nfrom setup.services import setup_dependencies, download_nltk_data\nfrom setup.utils import process_manager\nfrom setup.validation import check_python_version")
content = content.replace("from setup.environment import create_venv", "from setup.environment import create_venv\nfrom setup.services import setup_dependencies, download_nltk_data")

with open('tests/test_launcher.py', 'w') as f:
    f.write(content)
