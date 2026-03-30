import re
import glob
files = glob.glob("src/**/*.py", recursive=True)

for file_path in files:
    try:
        with open(file_path, "r") as f:
            content = f.read()

        if "<<<<<<< HEAD" in content:
            # simple replacement taking the HEAD version
            content = re.sub(r'<<<<<<< HEAD\n(.*?)\n=======\n.*?\n>>>>>>> .*?\n', r'\1\n', content, flags=re.DOTALL)

            with open(file_path, "w") as f:
                f.write(content)
    except Exception as e:
        print(e)
