with open("setup/launch.py", "r", encoding="utf-8") as f:
    text = f.read()

# Replace trailing `<<<<<<< HEAD` blocks and the un-terminated strings if they still exist
text = text.replace("<<<<<<< HEAD\n", "")
text = text.replace("=======\n", "")
text = text.replace(">>>>>>> a7da61cf1f697de3c8c81f536bf579d36d88e613\n", "")

with open("setup/launch.py", "w", encoding="utf-8") as f:
    f.write(text)
