import subprocess
import sys

def run_git():
    subprocess.run(["git", "status"])

def run_python_variable():
    exe = sys.executable
    subprocess.run([exe, "-c", "print(1)"])

def run_python_sys():
    subprocess.run([sys.executable, "-c", "print(1)"])

def run_python_literal():
    subprocess.run(["python", "-c", "print(1)"])
