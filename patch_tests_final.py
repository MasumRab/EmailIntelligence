with open('tests/test_launcher.py', 'r') as f:
    content = f.read()

content = content.replace('patch("setup.launch.Path.exists"', 'patch("pathlib.Path.exists"')
content = content.replace('patch("setup.launch.shutil.rmtree"', 'patch("shutil.rmtree"')
content = content.replace('patch("setup.launch.venv.create"', 'patch("venv.create"')
content = content.replace('patch("setup.launch.subprocess.run"', 'patch("subprocess.run"')
content = content.replace('patch("setup.launch.subprocess.Popen"', 'patch("subprocess.Popen"')
content = content.replace('patch("setup.launch.sys.version_info"', 'patch("sys.version_info"')
content = content.replace('patch("setup.launch.os.environ"', 'patch("os.environ"')
content = content.replace('patch("setup.launch.sys.argv"', 'patch("sys.argv"')
content = content.replace('patch("setup.launch.platform.system"', 'patch("platform.system"')
content = content.replace('patch("setup.launch.shutil.which"', 'patch("shutil.which"')
content = content.replace('patch("setup.launch.os.execv"', 'patch("os.execv"')
content = content.replace('patch("setup.launch.sys.exit"', 'patch("sys.exit"')

content = content.replace('patch("launch.platform.python_version"', 'patch("platform.python_version"')

with open('tests/test_launcher.py', 'w') as f:
    f.write(content)
