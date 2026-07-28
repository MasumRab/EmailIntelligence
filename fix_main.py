import re
with open('src/main.py', 'r') as f:
    content = f.read()

content = content.replace('from fastapi import FastAPI, Request', 'from fastapi import FastAPI')
content = content.replace('from typing import Optional\n', '')
content = content.replace('except:\n                pass', 'except Exception:\n                pass')

with open('src/main.py', 'w') as f:
    f.write(content)
