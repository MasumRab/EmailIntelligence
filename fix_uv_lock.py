with open("uv.lock", "r") as f:
    content = f.read()

# Replace the block that has missing source with the correct one, or just delete the ones that don't have source.
# It seems there are multiple 'bandit' packages declared in uv.lock, and some don't have a source.
# Let's write a script to filter out package definitions named "bandit" that are missing the 'source = ' line.
lines = content.split('\n')
new_lines = []
in_package = False
current_pkg_lines = []
has_source = False
pkg_name = ""

for line in lines:
    if line.strip() == "[[package]]":
        if in_package:
            if pkg_name != '"bandit"' or has_source:
                new_lines.extend(current_pkg_lines)
        in_package = True
        current_pkg_lines = [line]
        has_source = False
        pkg_name = ""
    elif in_package:
        current_pkg_lines.append(line)
        if line.startswith("name = "):
            pkg_name = line.split("=")[1].strip()
        elif line.startswith("source = "):
            has_source = True
    else:
        new_lines.append(line)

if in_package:
    if pkg_name != '"bandit"' or has_source:
        new_lines.extend(current_pkg_lines)

with open("uv.lock", "w") as f:
    f.write('\n'.join(new_lines))
