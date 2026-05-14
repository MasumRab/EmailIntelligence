import subprocess
import os

env = os.environ.copy()
env['GIT_ASKPASS'] = 'echo'
subprocess.run(["git", "push", "-f", "origin", "sentinel/rate-limiter-dos-12798576168905647370-1187660136859994710"], env=env, check=True)
