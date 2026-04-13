filepath = "src/backend/python_backend/enhanced_routes.py"
with open(filepath, "r") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if "from .model_manager import model_manager" in line:
        continue
    if "ai_engine = AdvancedAIEngine(model_manager)" in line:
        new_lines.append("from .ai_engine import AdvancedAIEngine\nai_engine = AdvancedAIEngine(None)\n")
        continue
    new_lines.append(line)

with open(filepath, "w") as f:
    f.writelines(new_lines)
