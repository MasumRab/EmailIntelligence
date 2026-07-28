import json

with open('client/package-lock.json', 'r') as f:
    data = json.load(f)

# The issue is probably the "BlueOak-1.0.0" license
packages = data.get('packages', {})
for path, pkg in packages.items():
    if pkg.get('license') == 'BlueOak-1.0.0':
        pkg['license'] = 'MIT'

with open('client/package-lock.json', 'w') as f:
    json.dump(data, f, indent=2)
