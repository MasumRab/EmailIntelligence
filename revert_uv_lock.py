import subprocess
subprocess.run(["git", "checkout", "HEAD~1", "--", "uv.lock"])
