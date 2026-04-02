import gradio as gr
import os
import sys
import configparser

# Monkey-patch for notmuch compatibility with Python 3.12+
if sys.version_info >= (3, 12):
    configparser.SafeConfigParser = configparser.ConfigParser

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from modules.notmuch.ui import create_notmuch_ui

# Set a dummy secret key to satisfy any potential config checks
os.environ["SECRET_KEY"] = "temporary_secret_key_for_ui_test"
# Set the data source type to notmuch
os.environ["DATA_SOURCE_TYPE"] = "notmuch"
# Set a dummy notmuch db path - the UI doesn't need a real one to load
os.environ["NOTMUCH_DATABASE_PATH"] = "/tmp/fake-notmuch"


if __name__ == "__main__":
    try:
        print("Starting isolated Notmuch UI for verification...")
        notmuch_ui = create_notmuch_ui()
        notmuch_ui.launch(server_name="127.0.0.1", server_port=7861)
        print("Notmuch UI started on http://127.0.0.1:7861")
    finally:
        # Clean up the temporary script
        os.remove(__file__)
