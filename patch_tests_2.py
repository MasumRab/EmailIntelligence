import re

def fix_file(filepath, replacements):
    try:
        with open(filepath, 'r') as f:
            content = f.read()

        original = content
        for search, replace in replacements:
            content = content.replace(search, replace)

        if original != content:
            with open(filepath, 'w') as f:
                f.write(content)
            print(f"Patched {filepath}")
    except Exception as e:
        print(f"Error patching {filepath}: {e}")

# Fix tests/test_launcher.py
fix_file('tests/test_launcher.py', [
    ('from setup.launch import ROOT_DIR, main, start_gradio_ui', 'from setup.launch import ROOT_DIR, main, start_gradio_ui\nfrom setup.environment import create_venv\nfrom setup.services import setup_dependencies, download_nltk_data\nfrom setup.utils import process_manager\nfrom setup.validation import check_python_version')
])
