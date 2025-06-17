import logging
import signal
import sys


def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting EmailIntelligence...")

    try:
        # Import and run your main application logic here
        import main  # Replace with your actual entry point

        main.run()  # Replace with your actual run method
    except Exception as e:
        logging.error(f"Error: {e}")
        sys.exit(1)


def handle_exit(signum, frame):
    logging.info("Shutting down EmailIntelligence gracefully...")
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)
    main()
