with open("src/core/data/database_source.py", "r") as f:
    content = f.read()

content = content.replace("from ..factory import get_data_source\n", "")

with open("src/core/data/database_source.py", "w") as f:
    f.write(content)
