#!/usr/bin/env python3
import subprocess
import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def run_validation(command):
    logging.info(f"Running validation: {command}")
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode != 0:
            logging.error(f"Validation failed: {command}")
            logging.error(f"Output:\n{result.stdout}\n{result.stderr}")
            return False
        logging.info(f"Validation succeeded: {command}")
        return True
    except Exception:
        logging.exception("Error running %s", command)
        return False

def main():
    scripts_to_run = [
        "scripts/incremental_validator.py",
        "scripts/parallel_validator.py"
    ]
    
    for script in scripts_to_run:
        command = [sys.executable, script]
        if not run_validation(command):
            logging.error("Pipeline stopped due to validation failure.")
            sys.exit(1)
            
    logging.info("All validations passed successfully.")
    sys.exit(0)

if __name__ == "__main__":
    main()
