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
        target_path = (base_path / path).resolve()
        # Only allow paths strictly inside the base_dir
        if target_path != base_path and base_path not in target_path.parents:
            return False
        return True
    except (ValueError, RuntimeError):
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

sanitize_old = """    if not validate_path_safety(path, base_dir):
        return None

    base_path = (pathlib.Path(base_dir) if base_dir else pathlib.Path.cwd()).resolve()
    return (base_path / path).resolve()"""

sanitize_new = """    try:
        if not validate_path_safety(path, base_dir):
            return None

        import urllib.parse
        str_path = str(path)
        decoded_path = urllib.parse.unquote(str_path)
        if "\\x00" in decoded_path:
            return None
            
        path_obj = pathlib.Path(decoded_path)
        base_path = (pathlib.Path(base_dir) if base_dir else pathlib.Path.cwd()).resolve()
        
        # Prevent absolute paths from replacing the base directory entirely
        if path_obj.is_absolute():
            resolved_path = path_obj.resolve()
        else:
            safe_str = decoded_path.lstrip('/')
            resolved_path = (base_path / safe_str).resolve()
            
        if resolved_path != base_path and base_path not in resolved_path.parents:
            return None
            
        return resolved_path
    except Exception as e:
        logger.warning(f"Error sanitizing path '{path}': {e}")
        return None"""

content = content.replace(sanitize_old, sanitize_new)

with open('src/core/security.py', 'w') as f:
    f.write(content)
print("Patched successfully")
