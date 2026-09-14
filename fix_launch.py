import re

filepaths = ["setup/launch.py", "setup/services.py"]

for filepath in filepaths:
    with open(filepath, "r") as f:
        content = f.read()

    # Revert my previous regex which introduced syntax errors
    content = content.replace("subprocess.run([str(x) for x in cmd]],", "subprocess.run(cmd,")
    content = re.sub(r'subprocess.run\(\[str\(x\) for x in \[([^\]]+)\]\],', r'subprocess.run([\1],', content)
    content = re.sub(r'subprocess.run\(\[str\(x\) for x in \[([^\]]+)\]\]\)', r'subprocess.run([\1])', content)

    with open(filepath, "w") as f:
        f.write(content)
