with open("src/core/models.py", "r") as f:
    content = f.read()

import re

# Fix IndentationError
old_block = """    @validator("preview", pre=True)
    @classmethod
    def set_preview(cls, v, values):
        \"\"\"Sets the preview from the content if not provided.\"\"\"
        if not v and "content" in values:
        if not v and values and "content" in values:
            content = values["content"]
            return content[:200] + "..." if len(content) > 200 else content
        return v"""

new_block = """    @validator("preview", pre=True)
    @classmethod
    def set_preview(cls, v, values):
        \"\"\"Sets the preview from the content if not provided.\"\"\"
        if not v and getattr(values, "content", None):
            content = values.data.get("content")
            if content:
                return content[:200] + "..." if len(content) > 200 else content
        return v"""

content = content.replace(old_block, new_block)

with open("src/core/models.py", "w") as f:
    f.write(content)
