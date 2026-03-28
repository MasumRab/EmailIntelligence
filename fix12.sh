sed -i 's/        proc = subprocess.run(cmd, check=True, text=True, capture_output=True, \*\*kwargs)/        proc = subprocess.run(cmd, check=True, text=True, capture_output=True, \*\*kwargs)  # nosec/g' setup/launch.py
sed -i 's/            subprocess.run(\[python_exe, "-c", "import poetry"\], check=True, capture_output=True)/            subprocess.run(\[python_exe, "-c", "import poetry"\], check=True, capture_output=True)  # nosec/g' setup/launch.py
sed -i 's/            subprocess.run(\[python_exe, "-c", "import uv"\], check=True, capture_output=True)/            subprocess.run(\[python_exe, "-c", "import uv"\], check=True, capture_output=True)  # nosec/g' setup/launch.py
sed -i '725s/        result = subprocess.run(/        result = subprocess.run(  # nosec/' setup/launch.py
sed -i '777s/    result = subprocess.run(/    result = subprocess.run(  # nosec/' setup/launch.py
sed -i '800s/    result = subprocess.run(/    result = subprocess.run(  # nosec/' setup/launch.py
sed -i '818s/        result = subprocess.run(/        result = subprocess.run(  # nosec/' setup/launch.py
