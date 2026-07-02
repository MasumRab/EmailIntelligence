with open('tests/test_launcher.py', 'r') as f:
    content = f.read()

content = content.replace('patch("launch.Path.exists"', 'patch("pathlib.Path.exists"')
content = content.replace('patch("launch.shutil.rmtree"', 'patch("shutil.rmtree"')
content = content.replace('patch("launch.venv.create"', 'patch("venv.create"')
content = content.replace('patch("launch.subprocess.run"', 'patch("subprocess.run"')
content = content.replace('patch("launch.subprocess.Popen"', 'patch("subprocess.Popen"')
content = content.replace('patch("launch.sys.version_info"', 'patch("sys.version_info"')
content = content.replace('patch("launch.os.environ"', 'patch("os.environ"')
content = content.replace('patch("launch.sys.argv"', 'patch("sys.argv"')
content = content.replace('patch("launch.platform.system"', 'patch("platform.system"')
content = content.replace('patch("launch.shutil.which"', 'patch("shutil.which"')
content = content.replace('patch("launch.os.execv"', 'patch("os.execv"')
content = content.replace('patch("launch.sys.exit"', 'patch("sys.exit"')
content = content.replace('patch("launch.logger"', 'patch("setup.launch.logger"')
content = content.replace('patch("launch.platform.python_version"', 'patch("platform.python_version"')
content = content.replace('from setup.launch import ROOT_DIR, main, start_gradio_ui', 'from setup.launch import ROOT_DIR, main, start_gradio_ui\nfrom setup.launch import create_venv, setup_dependencies, download_nltk_data')

with open('tests/test_launcher.py', 'w') as f:
    f.write(content)
