import subprocess
try:
    out = subprocess.check_output(['git', 'diff', '--name-only', 'HEAD']).decode('utf-8')
    for line in out.split('\n'):
        if line.startswith('src/') or line.startswith('scripts/') or line.startswith('tests/'):
            print(line)
except Exception as e:
    pass
