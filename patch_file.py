with open("src/core/database.py", "r") as f:
    lines = f.readlines()
with open("src/core/database.py", "w") as f:
    for line in lines:
        if "from .data.data_source import DataSource" in line:
            f.write("from .data.data_source import DataSource  # noqa: E402\n")
        else:
            f.write(line)
