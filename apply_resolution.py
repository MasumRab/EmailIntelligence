with open("setup/launch.py", "r") as f:
    content = f.read()

# We need to resolve conflicts by picking the new version from `=======` to `>>>>>>> ...` for most.
# Let's do it manually using regex since the file might have several blocks.
import re

# For blocks matching <<<<<<< HEAD ... ======= ... >>>>>>> [hex]
# We will use a script to replace them with the `=======` to `>>>>>>>` part.
# Let's just run git checkout --theirs setup/launch.py ?
# Wait, this file is currently committed with conflicts! It's not in a merge state.
