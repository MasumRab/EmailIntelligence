import sys

with open('src/core/security.py', 'r') as f:
    content = f.read()

val_old = """    if base_dir is None:
        # Without a base_dir, perform strict validation of the path structure
        str_path = str(path).replace('\\\\', '/')

        # Check for dangerous characters (cross-platform)
        if re.search(r'[<>"|?*]', str_path):
            return False

        # Reject UNC-like paths (starting with //)
        if str_path.startswith('//'):
             return False

        # Split path into components to check for traversal and dot segments
        parts = str_path.split('/')

        # Check for traversal components
        if '..' in parts:
            return False

        # Reject absolute paths containing '.' segments (e.g. /./etc/passwd)
        # This is often used for obfuscation.
        if str_path.startswith('/') and '.' in parts:
            return False

        return True

    try:
        base_path = pathlib.Path(base_dir).resolve()
        # Ensure we don't accidentally resolve relative paths against CWD implicitly if not intended,
        # but here we join with base_path, so relative paths are resolved against base_path.
        requested_path = (base_path / path).resolve()
        return requested_path.is_relative_to(base_path)
    except (ValueError, TypeError):
        return False"""

val_new = """    str_path = str(path).replace('\\\\', '/')

    # Check for dangerous characters (cross-platform)
    if re.search(r'[<>"|?*]', str_path):
        return False

    # Reject UNC-like paths (starting with //)
    if str_path.startswith('//'):
         return False

    # Split path into components to check for traversal and dot segments
    parts = str_path.split('/')

    # Check for traversal components
    if '..' in parts:
        return False

    # Reject absolute paths containing '.' segments (e.g. /./etc/passwd)
    # This is often used for obfuscation.
    if str_path.startswith('/') and '.' in parts:
        return False

    return True"""

content = content.replace(val_old, val_new)

with open('src/core/security.py', 'w') as f:
    f.write(content)
print("Patched successfully")
