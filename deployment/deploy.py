import argparse
import subprocess
import sys

# Define paths to docker-compose files
BASE_COMPOSE_FILE = "deployment/docker-compose.yml"
DEV_COMPOSE_FILE = "deployment/docker-compose.dev.yml"
PROD_COMPOSE_FILE = "deployment/docker-compose.prod.yml"


def run_compose_command(environment, command, service=None):
    compose_files = [BASE_COMPOSE_FILE]
    if environment == "dev":
        compose_files.append(DEV_COMPOSE_FILE)
    elif environment == "prod":
        compose_files.append(PROD_COMPOSE_FILE)

    cmd = ["docker-compose"]
    for f in compose_files:
        cmd.extend(["-f", f])
    cmd.append(command)
    if service:
        cmd.append(service)

    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)


def main():
    parser = argparse.ArgumentParser(
        description="Manage EmailIntelligence Docker deployments."
    )
    parser.add_argument(
        "environment", choices=["dev", "prod"], help="Deployment environment."
    )
    parser.add_argument(
        "command",
        choices=["up", "down", "build", "logs"],
        help="Docker Compose command.",
    )
    parser.add_argument(
        "service", nargs="?", help="Optional service name to apply command to."
    )

    args = parser.parse_args()

    try:
        run_compose_command(args.environment, args.command, args.service)
    except subprocess.CalledProcessError as e:
        print(f"Error executing Docker Compose command: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
