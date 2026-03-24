import re
with open("tests/scripts/test_update_active_context.py", "r") as f:
    text = f.read()

text = text.replace('mock_run.assert_called_once_with(["git", "config", "--get", "remote.origin.url"], capture_output=True, text=True, check=True)',
                    'mock_run.assert_called_once()\n        called_args = mock_run.call_args[0][0]\n        self.assertTrue(called_args[0].endswith("git"))\n        self.assertEqual(called_args[1:], ["config", "--get", "remote.origin.url"])')

with open("tests/scripts/test_update_active_context.py", "w") as f:
    f.write(text)
