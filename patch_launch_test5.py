with open("tests/test_launcher.py", "r") as f:
    content = f.read()

content = content.replace("result = start_gradio_ui(venv_path, \"127.0.0.1\")", "start_gradio_ui(\"127.0.0.1\", 7860, False, False)")

with open("tests/test_launcher.py", "w") as f:
    f.write(content)
