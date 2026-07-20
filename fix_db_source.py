import re

file_path = "src/core/data/database_source.py"
with open(file_path, "r") as f:
    content = f.read()

content = content.replace("from ..database import DatabaseConfig",
"""if TYPE_CHECKING:
    from ..database import DatabaseConfig""")

with open(file_path, "w") as f:
    f.write(content)
