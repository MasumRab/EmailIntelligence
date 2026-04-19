import sys

def main():
    with open("uv.lock", "r") as f:
        lines = f.readlines()

    out = []
    i = 0
    bandit_blocks_seen = 0

    while i < len(lines):
        if lines[i].strip() == "[[package]]":
            if i + 1 < len(lines) and lines[i+1].strip() == 'name = "bandit"':
                bandit_blocks_seen += 1
                if bandit_blocks_seen > 1:
                    # Skip this block until the next empty line or next block
                    i += 1
                    while i < len(lines) and lines[i].strip() != "" and not lines[i].startswith("[["):
                        i += 1
                    continue
        out.append(lines[i])
        i += 1

    with open("uv.lock", "w") as f:
        f.writelines(out)

if __name__ == "__main__":
    main()
