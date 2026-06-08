with open('tests/test_launcher.py', 'r') as f:
    content = f.read()

# Since `Path` etc. are failing to be patched because they aren't in `launch` namespace anymore probably, actually no, the test is failing because `Path` isn't imported into `launch` namespace anymore? Wait, no. `from pathlib import Path` is in `launch.py`. Wait, it's missing from `launch.py` now?
# Oh, the error says: AttributeError: module 'launch' has no attribute 'Path'
# Let's check if `Path` is in `setup/launch.py`.
