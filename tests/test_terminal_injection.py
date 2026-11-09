import subprocess
import os
import unittest
import tempfile
from pathlib import Path

class TestTerminalInjection(unittest.TestCase):
    def setUp(self):
        self.repo_root = Path(__file__).parent.parent.resolve()
        # This payload matches the original vulnerable test assertion
        self.payload = "This is \\x1b]0;pwned\\x07 safe"

    def run_and_assert_script(self, label, script_content):
        with tempfile.TemporaryDirectory() as tempdir:
            temp_test_script = os.path.join(tempdir, "temp_test_echo.sh")
            with open(temp_test_script, "w") as f:
                f.write(script_content)
                
            os.chmod(temp_test_script, 0o755)
            
            result = subprocess.run([temp_test_script], capture_output=True, text=True)
            
            self.assertEqual(result.returncode, 0, f"[{label}] Script failed with exit code {result.returncode}\nSTDERR: {result.stderr}")
            self.assertEqual(result.stderr, "", f"[{label}] Expected empty stderr but got: {result.stderr}")
            
            # Use raw byte representation directly mapped to the vulnerability
            self.assertIn("\\x1b]0;pwned\\x07", result.stdout, f"[{label}] OSC injection was expanded, the raw sequence is missing from output")
            self.assertIn("pwned", result.stdout, f"[{label}] Output is missing the expected text payload")

    def test_osc_injection_prevented_setup_env(self):
        script = f"""#!/bin/bash
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'
PAYLOAD="{self.payload}"
eval "$(sed -n '/^log_info() {{/,/^}}/p' '{self.repo_root}/setup/setup_environment_system.sh')"
log_info "$PAYLOAD"
eval "$(sed -n '/^log_success() {{/,/^}}/p' '{self.repo_root}/setup/setup_environment_system.sh')"
log_success "$PAYLOAD"
eval "$(sed -n '/^log_warning() {{/,/^}}/p' '{self.repo_root}/setup/setup_environment_system.sh')"
log_warning "$PAYLOAD"
eval "$(sed -n '/^log_error() {{/,/^}}/p' '{self.repo_root}/setup/setup_environment_system.sh')"
log_error "$PAYLOAD"
"""
        self.run_and_assert_script("setup_environment_system.sh", script)

    def test_osc_injection_prevented_setup_wsl(self):
        script = f"""#!/bin/bash
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'
PAYLOAD="{self.payload}"
eval "$(sed -n '/^log_info() {{/,/^}}/p' '{self.repo_root}/setup/setup_environment_wsl.sh')"
log_info "$PAYLOAD"
eval "$(sed -n '/^log_success() {{/,/^}}/p' '{self.repo_root}/setup/setup_environment_wsl.sh')"
log_success "$PAYLOAD"
eval "$(sed -n '/^log_warning() {{/,/^}}/p' '{self.repo_root}/setup/setup_environment_wsl.sh')"
log_warning "$PAYLOAD"
eval "$(sed -n '/^log_error() {{/,/^}}/p' '{self.repo_root}/setup/setup_environment_wsl.sh')"
log_error "$PAYLOAD"
"""
        self.run_and_assert_script("setup_environment_wsl.sh", script)

    def test_osc_injection_prevented_backup(self):
        script = f"""#!/bin/bash
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'
PAYLOAD="{self.payload}"
eval "$(sed -n '/^log_info() {{/,/^}}/p' '{self.repo_root}/backup.sh')"
log_info "$PAYLOAD"
eval "$(sed -n '/^log_success() {{/,/^}}/p' '{self.repo_root}/backup.sh')"
log_success "$PAYLOAD"
eval "$(sed -n '/^log_warning() {{/,/^}}/p' '{self.repo_root}/backup.sh')"
log_warning "$PAYLOAD"
eval "$(sed -n '/^log_error() {{/,/^}}/p' '{self.repo_root}/backup.sh')"
log_error "$PAYLOAD"
"""
        self.run_and_assert_script("backup.sh", script)

    def test_osc_injection_prevented_deploy(self):
        script = f"""#!/bin/bash
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'
PAYLOAD="{self.payload}"
eval "$(sed -n '/^log_info() {{/,/^}}/p' '{self.repo_root}/deploy.sh')"
log_info "$PAYLOAD"
eval "$(sed -n '/^log_success() {{/,/^}}/p' '{self.repo_root}/deploy.sh')"
log_success "$PAYLOAD"
eval "$(sed -n '/^log_warning() {{/,/^}}/p' '{self.repo_root}/deploy.sh')"
log_warning "$PAYLOAD"
eval "$(sed -n '/^log_error() {{/,/^}}/p' '{self.repo_root}/deploy.sh')"
log_error "$PAYLOAD"
"""
        self.run_and_assert_script("deploy.sh", script)

    def test_osc_injection_prevented_test_orch(self):
        script = f"""#!/bin/bash
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'
PAYLOAD="{self.payload}"
eval "$(sed -n '/^log_info() {{/,/^}}/p' '{self.repo_root}/scripts/test_orchestration.sh')"
log_info "$PAYLOAD"
eval "$(sed -n '/^log_success() {{/,/^}}/p' '{self.repo_root}/scripts/test_orchestration.sh')"
log_success "$PAYLOAD"
eval "$(sed -n '/^log_warning() {{/,/^}}/p' '{self.repo_root}/scripts/test_orchestration.sh')"
log_warning "$PAYLOAD"
eval "$(sed -n '/^log_error() {{/,/^}}/p' '{self.repo_root}/scripts/test_orchestration.sh')"
log_error "$PAYLOAD"
"""
        self.run_and_assert_script("test_orchestration.sh", script)

    def test_osc_injection_prevented_setup_auto(self):
        script = f"""#!/bin/bash
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'
PAYLOAD="{self.payload}"
eval "$(sed -n '/^print_status() {{/,/^}}/p' '{self.repo_root}/scripts/setup_automation.sh')"
print_status "$PAYLOAD"
eval "$(sed -n '/^print_success() {{/,/^}}/p' '{self.repo_root}/scripts/setup_automation.sh')"
print_success "$PAYLOAD"
eval "$(sed -n '/^print_warning() {{/,/^}}/p' '{self.repo_root}/scripts/setup_automation.sh')"
print_warning "$PAYLOAD"
eval "$(sed -n '/^print_error() {{/,/^}}/p' '{self.repo_root}/scripts/setup_automation.sh')"
print_error "$PAYLOAD"
"""
        self.run_and_assert_script("setup_automation.sh", script)

    def test_osc_injection_prevented_sync_docs(self):
        script = f"""#!/bin/bash
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'
PAYLOAD="{self.payload}"
eval "$(sed -n '/^print_status() {{/,/^}}/p' '{self.repo_root}/scripts/sync-common-docs.sh')"
print_status "$PAYLOAD"
eval "$(sed -n '/^print_success() {{/,/^}}/p' '{self.repo_root}/scripts/sync-common-docs.sh')"
print_success "$PAYLOAD"
eval "$(sed -n '/^print_warning() {{/,/^}}/p' '{self.repo_root}/scripts/sync-common-docs.sh')"
print_warning "$PAYLOAD"
eval "$(sed -n '/^print_error() {{/,/^}}/p' '{self.repo_root}/scripts/sync-common-docs.sh')"
print_error "$PAYLOAD"
"""
        self.run_and_assert_script("sync-common-docs.sh", script)
        text = (self.repo_root / "scripts/sync-common-docs.sh").read_text()
        self.assertNotIn("echo -e", text, "sync-common-docs.sh still uses echo -e")

    def test_osc_injection_prevented_orch_status(self):
        script = f"""#!/bin/bash
WHITE='\033[1;37m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'
CHECK="[OK]"
CROSS="[FAIL]"
WARNING="[WARN]"
INFO="[INFO]"
STATUS_PASSED=5
STATUS_WARNINGS=2
STATUS_FAILED=1
ORCHESTRATION_BRANCH="my_branch"

PAYLOAD="{self.payload}"

eval "$(sed -n '/^log_header() {{/,/^}}/p' '{self.repo_root}/scripts/orchestration_status.sh')"
log_header "$PAYLOAD"

eval "$(sed -n '/^log_section() {{/,/^}}/p' '{self.repo_root}/scripts/orchestration_status.sh')"
log_section "$PAYLOAD"

eval "$(sed -n '/^log_item() {{/,/^}}/p' '{self.repo_root}/scripts/orchestration_status.sh')"
log_item "pass" "$PAYLOAD"
log_item "fail" "$PAYLOAD"
log_item "warn" "$PAYLOAD"
log_item "info" "$PAYLOAD"
log_item "unknown" "$PAYLOAD"
"""
        self.run_and_assert_script("orchestration_status.sh", script)

    def test_osc_injection_prevented_reverse_sync(self):
        text = (self.repo_root / "scripts/reverse_sync_orchestration.sh").read_text()
        self.assertNotIn("echo -e", text, "reverse_sync_orchestration.sh still uses echo -e")

    def test_osc_injection_prevented_sync_setup(self):
        text = (self.repo_root / "scripts/sync_setup_worktrees.sh").read_text()
        self.assertNotIn("echo -e", text, "sync_setup_worktrees.sh still uses echo -e")

if __name__ == '__main__':
    unittest.main()
