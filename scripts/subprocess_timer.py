#!/usr/bin/env python3
import subprocess
import time
import sys
import shutil

def time_command(command: list[str]) -> float:
    if not command:
        raise ValueError("Command is empty")
    for arg in command:
        if not isinstance(arg, str):
            raise ValueError(f"Argument {arg!r} is not a string")
        if arg.startswith('-'):
            raise ValueError(f"Argument {arg!r} starts with a hyphen (-)")
    if shutil.which(command[0]) is None:
        raise ValueError(f"Executable {command[0]!r} not found in PATH")
        
    start_time = time.perf_counter()
    subprocess.run(command, check=True)  # NOSONAR
    end_time = time.perf_counter()
    return (end_time - start_time) * 1000.0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python subprocess_timer.py <command...>")
        sys.exit(1)
    cmd = sys.argv[1:]
    try:
        elapsed_ms = time_command(cmd)
        print(f"Elapsed: {elapsed_ms:.2f} ms")
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)
