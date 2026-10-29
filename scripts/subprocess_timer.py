#!/usr/bin/env python3
import subprocess
import time
import sys

def time_command(command: list[str]) -> float:
    start_time = time.perf_counter()
    subprocess.run(command, check=True)
    end_time = time.perf_counter()
    return (end_time - start_time) * 1000.0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python subprocess_timer.py <command...>")
        sys.exit(1)
        
    cmd = sys.argv[1:]
    
    # Simple restriction to only allow running echo for testing/timing purposes safely
    if cmd[0] not in ['echo', 'ls', 'sleep']:
         print("Error: Only specific safe commands (echo, ls, sleep) are permitted.", file=sys.stderr)
         sys.exit(1)
         
    try:
        elapsed_ms = time_command(cmd)
        print(f"Elapsed: {elapsed_ms:.2f} ms")
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)
