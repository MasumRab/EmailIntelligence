with open("setup/services.py", "r", encoding="utf-8") as f:
    text = f.read()

import re
# Oh I see! A syntax error at line 175 of setup/services.py:
# if not re.match(r'^[a-zA-Z0-9.-]+
text = text.replace("if not re.match(r'^[a-zA-Z0-9.-]+", "if not re.match(r'^[a-zA-Z0-9.-]+$', str(host)):")

with open("setup/services.py", "w", encoding="utf-8") as f:
    f.write(text)
