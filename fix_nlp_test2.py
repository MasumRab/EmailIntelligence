with open("src/backend/python_nlp/tests/test_nlp_engine.py", "r") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.startswith("def test_"):
        new_lines.append("@patch('backend.python_nlp.nlp_engine.pipeline')\n")
        new_lines.append(line.replace("():", "(mock_pipeline):"))
    else:
        new_lines.append(line)

with open("src/backend/python_nlp/tests/test_nlp_engine.py", "w") as f:
    f.writelines(new_lines)
