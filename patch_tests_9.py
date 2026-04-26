with open('tests/test_launcher.py', 'r') as f:
    content = f.read()

replacements = {
    'patch("launch.Path.exists"': 'patch("setup.launch.Path.exists"',
    'patch("launch.shutil.rmtree"': 'patch("setup.launch.shutil.rmtree"',
    'patch("launch.venv.create"': 'patch("setup.launch.venv.create"',
    'patch("launch.subprocess.run"': 'patch("setup.launch.subprocess.run"',
    'patch("launch.subprocess.Popen"': 'patch("setup.launch.subprocess.Popen"',
    'patch("launch.sys.version_info"': 'patch("setup.launch.sys.version_info"',
    'patch("launch.os.environ"': 'patch("setup.launch.os.environ"',
    'patch("launch.sys.argv"': 'patch("setup.launch.sys.argv"',
    'patch("launch.platform.system"': 'patch("setup.launch.platform.system"',
    'patch("launch.shutil.which"': 'patch("setup.launch.shutil.which"',
    'patch("launch.os.execv"': 'patch("setup.launch.os.execv"',
    'patch("launch.sys.exit"': 'patch("setup.launch.sys.exit"',
    'patch("launch.logger"': 'patch("setup.launch.logger"',
    'create_venv(': 'setup.launch.create_venv(',
    'setup_dependencies(': 'setup.launch.setup_dependencies(',
    'download_nltk_data(': 'setup.launch.download_nltk_data(',
    'check_python_version()': 'setup.launch.check_python_version()'
}

for k, v in replacements.items():
    content = content.replace(k, v)

with open('tests/test_launcher.py', 'w') as f:
    f.write(content)
