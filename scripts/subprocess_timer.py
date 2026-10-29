#!/usr/bin/env python3
import subprocess
import time
import sys

def time_command(command: list[str]) -> float:
    if not command:
        raise ValueError("Command is empty")
    for arg in command:
        if not isinstance(arg, str):
            raise ValueError(f"Argument {arg!r} is not a string")
        
    start_time = time.perf_counter()
    subprocess.run(command, check=True)  # NOSONAR: shell is not used and argv comes from process's own command line
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
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
