with open('emailintelligence_cli.py') as f:
    lines = f.readlines()
with open('/tmp/context.txt', 'w') as out:
    for i in range(250, 275):
        out.write(f"{i+1}: {lines[i]}")
