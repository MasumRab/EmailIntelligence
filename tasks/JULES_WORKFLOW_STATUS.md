# 🤖 Jules PR Audit: Workflow & Current Status
**Last Synced:** 2026-03-24 15:00 UTC

## 🎯 Global Objectives
1. **CI Repair**: Fix failing CI checks on non-draft PRs.
2. **Logic Parity**: Forensic audit of legacy PRs (Nov 2025).
3. **Context Awareness**: Sync with `tasks/open_pr_manifest.json`.

---

## 🛑 Critical Constraints & Quota Management
1. **Concurrent Session Limit: 15**. 
   - NEVER spawn more than 15 concurrent Jules sessions per project.
   - If a session fails or pauses, **DO NOT** automatically create a new session if the limit is reached.
   - Wait for Phase A/B tasks to complete or transition to `COMPLETED` before initiating restarts.

2. **Environment Isolation (Mandatory)**
   - All agents MUST ignore: `tasks/`, `workspace/`, `.beads/`, `.ck/`, and `.trunk/`.
   - Command: `pytest --ignore=tasks --ignore=workspace --ignore=.beads`.

---

## 🧬 Atomic Repair & Resumption Strategy
To avoid overwhelming agents with logic drift or "massive diff" warnings, follow this sequencing for all repairs:

### 1. Pre-Resumption Analysis
Before restarting a failed or paused session:
- **Diff Baseline**: Run `git diff origin/main...head_branch` to identify the number of files changed.
- **Identify Drift**: If >50 files are modified, the agent will likely crash. Break the task into sub-directories (e.g., "Fix imports in `src/core` only").

### 2. Atomic Task Sequencing
Instead of a broad "Fix CI" prompt, send discrete, sequential messages:
- **Step 1 (Discovery)**: Identify failing line numbers and specific error messages.
- **Step 2 (Logic Fix)**: Apply the code change to a specific file.
- **Step 3 (Sync)**: Merge the target branch and resolve conflicts using "Logic Preservation."
- **Step 4 (Verify)**: Run local tests with isolation flags.

### 3. Failure Recovery
- If a session fails with "unusually large diff":
  - **Action**: Manually clean the local environment or instruct the bot to `git clean -fd`.
  - **Correction**: Re-send the isolation instruction before restarting.

---

## 📊 High-Priority Commit Activity
| PR # | Latest Commit SHA | Author | Activity |
| :--- | :--- | :--- | :--- |
| **236** | `298382fc` | google-labs-jules | **Pushed Documentation** |
| **286** | `298382fc` | google-labs-jules | **Pushed Documentation** |
| **300** | `298382fc` | google-labs-jules | **Pushed Documentation** |
| **211** | `2c54c466` | google-labs-jules | Active (Yesterday) |

---

## 🛠️ Active Execution Registry
| PR # | Task ID | Goal | Current Status | Console Link |
| :--- | :--- | :--- | :--- | :--- |
| **271** | `14410989945895259602` | Database Lazy Loading | **Executing** | [View](https://jules.google.com/session/14410989945895259602) |
| **236** | `13091824377716859301` | Regex OR Fix | **Executing** | [View](https://jules.google.com/session/13091824377716859301) |
| **286** | `8645133856938915124` | 5x speedup optimization | **Executing** | [View](https://jules.google.com/session/8645133856938915124) |
| **300** | `17065719860896443446` | Regex grouping fix | **Executing** | [View](https://jules.google.com/session/17065719860896443446) |
| **440** | `7592875515078415283` | Packaging dependency | **Executing** | [View](https://jules.google.com/session/7592875515078415283) |
| **527** | `804955492758980486` | Nested IF logic | Discovery | [View](https://jules.google.com/session/804955492758980486) |
| **169** | `5822195393171532158` | Modular AI imports | **FAILED** (Retry Pending) | [View](https://jules.google.com/session/5822195393171532158) |

---
**Restoration Command:** `jules remote list --session` to refresh this context.
