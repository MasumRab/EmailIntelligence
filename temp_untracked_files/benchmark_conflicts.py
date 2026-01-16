
import os
import time
import tracemalloc
from pathlib import Path

# Mocking the constants and logic for the benchmark
ROOT_DIR = Path(".")
CRITICAL_FILE = "large_test_file.txt"
CONFLICT_MARKERS = ["<<<<<<< ", "======= ", ">>>>>>> "]

def create_large_file():
    """Creates a 100MB file with no conflicts."""
    print("Creating large file (100MB)...")
    with open(CRITICAL_FILE, "w") as f:
        # Write chunks to be faster
        chunk = "line of code " * 10 + "\n"
        # 100MB approx
        for _ in range(1000000):
            f.write(chunk)
    print("File created.")

def cleanup():
    if os.path.exists(CRITICAL_FILE):
        os.remove(CRITICAL_FILE)

def check_old():
    """Original implementation using read()"""
    with open(CRITICAL_FILE, "r", encoding="utf-8") as f:
        content = f.read()
        for marker in CONFLICT_MARKERS:
            if marker in content:
                return False
    return True

def check_new():
    """Optimized implementation using line-by-line iteration"""
    with open(CRITICAL_FILE, "r", encoding="utf-8") as f:
        for line in f:
            for marker in CONFLICT_MARKERS:
                if marker in line:
                    return False
    return True

def run_benchmark():
    create_large_file()

    try:
        # Benchmark Old
        tracemalloc.start()
        start_time = time.time()
        check_old()
        duration_old = time.time() - start_time
        current, peak_old = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        print(f"Old Implementation: Time = {duration_old:.4f}s, Peak Memory = {peak_old / 1024 / 1024:.2f} MB")

        # Benchmark New
        tracemalloc.start()
        start_time = time.time()
        check_new()
        duration_new = time.time() - start_time
        current, peak_new = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        print(f"New Implementation: Time = {duration_new:.4f}s, Peak Memory = {peak_new / 1024 / 1024:.2f} MB")

        print(f"Memory Savings: {(peak_old - peak_new) / 1024 / 1024:.2f} MB")

    finally:
        cleanup()

if __name__ == "__main__":
    run_benchmark()
