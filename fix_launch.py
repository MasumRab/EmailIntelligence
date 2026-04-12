with open("setup/launch.py", "r") as f:
    content = f.read()

# Looks like it's a conflict marker issue!
# "setup/launch.py" has conflict markers.
# Oh, the PR 636 has this issue? No, `setup/launch.py` is in `main`.

import re
# Let's fix the conflict markers in `setup/launch.py` since it's breaking pytest for ALL PRs right now.
