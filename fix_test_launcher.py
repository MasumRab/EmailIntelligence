with open("tests/test_launcher.py", "r") as f:
    content = f.read()

content = content.replace("patch(\"setup.launch.check_uvicorn_installed\"", "patch(\"setup.services.check_uvicorn_installed\"")
content = content.replace("patch(\"setup.launch.check_gradio_installed\"", "patch(\"setup.services.check_gradio_installed\"")

with open("tests/test_launcher.py", "w") as f:
    f.write(content)
