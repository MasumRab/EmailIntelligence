import re

file_path = "src/core/smart_filter_manager.py"
with open(file_path, "r") as f:
    content = f.read()

content = content.replace("log_error,", "enhanced_error_reporter,")
content = content.replace("log_error(", "enhanced_error_reporter.log_error(")

with open(file_path, "w") as f:
    f.write(content)
