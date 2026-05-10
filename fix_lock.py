with open("uv.lock", "r") as f:
    content = f.read()

import re
content = re.sub(r'<<<<<<<.*?\n', '', content)
content = re.sub(r'=======\n', '', content)
content = re.sub(r'>>>>>>>.*?\n', '', content)

with open("uv.lock", "w") as f:
    f.write(content)
