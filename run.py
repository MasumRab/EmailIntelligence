import subprocess
try:
    print(subprocess.check_output(['python', 'scripts/verify-dependencies.py', '--requirements', 'requirements.txt']).decode('utf-8'))
except subprocess.CalledProcessError as e:
    print(e.output.decode('utf-8'))
