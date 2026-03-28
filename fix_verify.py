import re

with open('scripts/verify-dependencies.py', 'r') as f:
    content = f.read()

# Replace the get_installed_packages function with one that catches exceptions from malformed packages
content = re.sub(
    r'def get_installed_packages\(\) -> Dict\[str, str\]:[\s\S]*?return installed',
    '''def get_installed_packages() -> Dict[str, str]:
    """Get a dictionary of installed packages and their versions."""
    installed = {}
    for dist in importlib.metadata.distributions():
        try:
            name = dist.metadata["Name"].lower()
            version = dist.version
            installed[name] = version
            # Handle normalized names (e.g. python-multipart -> python_multipart)
            normalized_name = name.replace("-", "_")
            if normalized_name != name:
                installed[normalized_name] = version
        except Exception:
            pass
    return installed''',
    content
)

with open('scripts/verify-dependencies.py', 'w') as f:
    f.write(content)
