import subprocess
import sys

def test_executable():
    res = subprocess.run(["python", "-c", "import sys; print(sys.executable)"], executable=sys.executable, capture_output=True, text=True)
    print("OUTPUT:", res.stdout.strip())

test_executable()
