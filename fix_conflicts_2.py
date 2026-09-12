import re

with open("package.json", "r") as f:
    text = f.read()

text = text.replace("""<<<<<<< HEAD
    "postcss": "^8.4.47",
    "prettier": "^3.4.0",
    "tailwindcss": "^3.4.17",
=======
    "prettier": "^3.4.0",
    "postcss": "^8.5.26",
    "tailwindcss": "^4.3.3",
>>>>>>> origin/main""", """    "prettier": "^3.4.0",
    "postcss": "^8.5.26",
    "tailwindcss": "^4.3.3",""")

with open("package.json", "w") as f:
    f.write(text)

with open("client/package.json", "r") as f:
    text = f.read()

text = text.replace("""<<<<<<< HEAD
    "postcss": "^8.4.47",
    "tailwindcss": "^3.4.14",
=======
    "postcss": "^8.5.26",
    "tailwindcss": "^4.3.3",
>>>>>>> origin/main""", """    "postcss": "^8.5.26",
    "tailwindcss": "^4.3.3",""")

with open("client/package.json", "w") as f:
    f.write(text)
