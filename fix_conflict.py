with open('.github/workflows/ci.yml', 'rb') as f:
    content = f.read()

old = b'''<<<<<<< HEAD
          uv run pytest backend/ src/ modules/ -v --tb=short --cov=backend --cov=src --cov=modules --cov-report=xml --cov-report=term-missing --cov-fail-under=80

      - name: Run Security Scans
        run: |
          uv run bandit -r backend/ src/ modules/
          uv run safety check
          \n=======
          uv run pytest tests/ src/ modules/ -v --tb=short \\
            --cov=src --cov=modules --cov-report=xml --cov-report=term-missing \\
            --cov-fail-under=70
      - name: Run Security Scans
        run: uv run bandit -r src/ modules/
>>>>>>> scientific'''

new = b'''          uv run pytest tests/ src/ modules/ -v --tb=short \\
            --cov=src --cov=modules --cov-report=xml --cov-report=term-missing \\
            --cov-fail-under=70

      - name: Run Security Scans
        run: |
          uv run bandit -r backend/ src/ modules/
          uv run safety check'''

if old not in content:
    print("Trying with literal trailing spaces...")
    # Read lines to debug
    with open('.github/workflows/ci.yml') as f:
        lines = f.readlines()
    for i in range(41, 57):
        print(f'{i}: {repr(lines[i-1])}')

print(repr(old))
assert old in content, 'Conflict block not found!'
content = content.replace(old, new)
with open('.github/workflows/ci.yml', 'wb') as f:
    f.write(content)
print('Done: Fixed ci.yml merge conflict')

with open('.github/workflows/ci.yml', 'rb') as f:
    content2 = f.read()
assert b'<<<<<<<' not in content2, 'Still has conflict markers!'
assert b'=======' not in content2, 'Still has conflict markers!'
assert b'>>>>>>>' not in content2, 'Still has conflict markers!'
print('Done: No conflict markers remain')
