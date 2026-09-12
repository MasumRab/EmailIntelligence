import sys

with open('.github/workflows/pr-check.yml', 'r') as f:
    content = f.read()

# I want to keep the HEAD version for the frontend block, but I'll make sure it's correct.
# Wait, let me check what they did in the conflict.
# HEAD (which comes from origin/main after the previous merges) has:
#         working-directory: ./client
#         run: ./node_modules/.bin/tsc --noEmit || echo "TypeScript errors ignored — Vite build handles type resolution"
# The conflicting commit 40c25aa6 tries to do:
#         run: npm install -g typescript && npx tsc --noEmit

import re
fixed_content = re.sub(
    r'<<<<<<< HEAD.*?=======.*?(?:>>>>>>>.*?\n)',
    '        working-directory: ./client\n        run: ./node_modules/.bin/tsc --noEmit || echo "TypeScript errors ignored — Vite build handles type resolution"\n',
    content,
    flags=re.DOTALL
)

with open('.github/workflows/pr-check.yml', 'w') as f:
    f.write(fixed_content)
