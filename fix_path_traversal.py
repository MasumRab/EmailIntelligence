import os

file_path = 'src/main.py'

with open(file_path, 'r') as f:
    lines = f.readlines()

new_logic = """        # Catch-all for SPA routing (excluding API and UI)
        @app.get("/{full_path:path}")
        async def catch_all(full_path: str):
            if full_path.startswith("api") or full_path.startswith("ui"):
                raise HTTPException(status_code=404, detail="Not found")

            # Sanitize and validate path to prevent directory traversal
            clean_path = os.path.normpath(full_path).lstrip('/')
            file_path = os.path.join(static_dir, clean_path)

            # Ensure file_path is within static_dir
            if not os.path.commonpath([file_path, static_dir]) == static_dir:
                 raise HTTPException(status_code=403, detail="Access denied")

            # Check if file exists in static dir
            if os.path.exists(file_path) and os.path.isfile(file_path):
                 return FileResponse(file_path)

            # Otherwise return index.html
            return FileResponse(os.path.join(static_dir, "index.html"))
"""

# Find the catch_all function block to replace
start_idx = -1
end_idx = -1

for i, line in enumerate(lines):
    if '@app.get("/{full_path:path}")' in line:
        start_idx = i
    if start_idx != -1 and 'return FileResponse(os.path.join(static_dir, "index.html"))' in line:
        end_idx = i
        break

if start_idx != -1 and end_idx != -1:
    # Remove old block
    del lines[start_idx:end_idx+1]
    # Insert new block
    lines.insert(start_idx, new_logic)

    with open(file_path, 'w') as f:
        f.writelines(lines)
    print("Fixed path traversal in src/main.py")
else:
    print("Could not find catch_all block")
