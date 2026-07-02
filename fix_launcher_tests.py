with open('tests/test_launcher.py', 'r') as f:
    content = f.read()

content = content.replace("create_venv(", "setup.launch.create_venv(")
content = content.replace("setup_dependencies(", "setup.launch.setup_dependencies(")
content = content.replace("download_nltk_data(", "setup.launch.download_nltk_data(")
content = content.replace("check_python_version()", "setup.launch.check_python_version()")
content = content.replace("process_manager", "setup.launch.process_manager")

with open('tests/test_launcher.py', 'w') as f:
    f.write(content)
