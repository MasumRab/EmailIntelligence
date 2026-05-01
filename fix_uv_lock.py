with open("uv.lock", "r") as f:
    lines = f.readlines()

out = []
i = 0
while i < len(lines):
    line = lines[i]
    if line.strip() == '[[package]]':
        # check if it's bandit
        if i + 1 < len(lines) and lines[i+1].strip() == 'name = "bandit"':
            # read the block
            block = []
            while i < len(lines) and lines[i].strip() != '':
                block.append(lines[i])
                i += 1
            if len(out) == 0 or 'name = "bandit"' not in "".join(out):
                # add first bandit block
                out.extend(block)
                if i < len(lines):
                    out.append(lines[i]) # add empty line
            else:
                # skip subsequent bandit blocks
                if i < len(lines):
                    pass # skip empty line
        else:
            out.append(line)
    else:
        out.append(line)
    i += 1

with open("uv.lock", "w") as f:
    f.writelines(out)
