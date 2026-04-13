with open('tests/test_launcher.py', 'r') as f:
    content = f.read()

content = content.replace("from setup.services import start_gradio_ui, start_backend, setup_dependencies, download_nltk_data", "from setup.services import start_gradio_ui, start_backend")

with open('tests/test_launcher.py', 'w') as f:
    f.write(content)
