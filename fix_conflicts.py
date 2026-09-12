import re
import subprocess
import os

# We will resolve conflicts in client/package.json
with open("client/package.json", "r") as f:
    text = f.read()

# I want to KEEP base's changes (origin/main) but also ADD the lodash change.
# Base has:
#    "input-otp": "^1.5.0",
#    "lucide-react": "^1.41.0",
# I need to keep those, but add:
#    "lodash": "^4.18.0",

text = text.replace("""<<<<<<< HEAD
    "input-otp": "^1.4.2",
    "lodash": "^4.18.0",
    "lucide-react": "^0.468.0",
=======
    "input-otp": "^1.5.0",
    "lucide-react": "^1.41.0",
>>>>>>> origin/main""", """    "input-otp": "^1.5.0",
    "lodash": "^4.18.0",
    "lucide-react": "^1.41.0",""")

with open("client/package.json", "w") as f:
    f.write(text)

# We will resolve conflicts in package.json
with open("package.json", "r") as f:
    text = f.read()

text = text.replace("""<<<<<<< HEAD
    "input-otp": "^1.4.2",
    "lodash": "^4.18.0",
    "lucide-react": "^0.453.0",
=======
    "input-otp": "^1.5.0",
    "lucide-react": "^1.41.0",
>>>>>>> origin/main""", """    "input-otp": "^1.5.0",
    "lodash": "^4.18.0",
    "lucide-react": "^1.41.0",""")

with open("package.json", "w") as f:
    f.write(text)

# We'll just run npm install to fix package-lock.json and client/package-lock.json automatically
subprocess.run(["git", "checkout", "--ours", "package-lock.json", "client/package-lock.json"])
subprocess.run(["npm", "install", "--legacy-peer-deps"])
subprocess.run(["npm", "install", "--legacy-peer-deps"], cwd="client")
subprocess.run(["git", "add", "client/package.json", "package.json", "package-lock.json", "client/package-lock.json"])
