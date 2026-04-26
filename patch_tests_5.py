import os
import re

with open('tests/test_launcher.py', 'r') as f:
    content = f.read()

content = content.replace("from setup.environment import create_venv\nfrom setup.services import setup_dependencies, download_nltk_data\nfrom setup.environment import create_venv\nfrom setup.services import setup_dependencies, download_nltk_data\nfrom setup.utils import process_manager\nfrom setup.validation import check_python_version", "from setup.launch import create_venv\nfrom setup.launch import setup_dependencies, download_nltk_data\nfrom setup.utils import process_manager\nfrom setup.validation import check_python_version")
with open('tests/test_launcher.py', 'w') as f:
    f.write(content)
