with open('emailintelligence_cli.py') as f:
    lines = f.readlines()
for i in [252, 264, 271]: # 0-indexed
    print(lines[i].strip())
