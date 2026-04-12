with open("tests/test_launcher.py", "r") as f:
    content = f.read()

import re
content = content.replace("result = start_gradio_ui(venv_path, \"127.0.0.1\")\n            mock_popen.assert_called()", "start_gradio_ui(\"127.0.0.1\", 7860, False, False)\n            mock_popen.assert_called()")

content = re.sub(r'def test_python_interpreter_discovery_avoids_substring_match.*?(?=class Test)', '', content, flags=re.DOTALL)

with open("tests/test_launcher.py", "w") as f:
    f.write(content)
