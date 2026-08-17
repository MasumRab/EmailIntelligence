# Jules Tools Reference

Jules Tools is a lightweight command-line interface (CLI) for interacting with Jules, Google's autonomous AI coding agent. It allows you to manage coding sessions, inspect progress, and integrate Jules into your existing development workflows and scripts directly from your terminal.

Think of Jules Tools as both a command surface and a dashboard for your coding agent, designed to keep you in your flow without needing to switch to a web browser.

## Installation

To get started, install the tool globally using npm or pnpm.

```
npm install -g @google/jules
```

Once installed, the jules command will be available in your terminal.

### Authentication
Before you can use the tool, you must authenticate with your Google account.

### Login

```
jules login
```

This command will open a browser window to guide you through the Google authentication process.

### Logout
To log out from your account:

```
jules logout
```

## Usage
The CLI is built around commands and subcommands. You can get help for any command by using the -h or --help flag.

```
# Get general help
jules help

# Get help for a specific command (e.g., remote)
jules remote --help
```

### Global Flags
- `-h`, `--help`: Displays help information for jules or a specific command.

- `--theme <string>`: Sets the theme for the terminal user interface (TUI). Options are `dark` (default) or `light`.

Example: `jules --theme light`

### Available Commands
`version`

Shows the currently installed version of the Jules Tools CLI.

```
jules version
```

`remote`

The `remote` command is the primary way to interact with Jules sessions running in the cloud. It has several subcommands.

`remote list`
Lists your connected repositories or active sessions.

- `--repo`: Flag to list all repositories connected to Jules.

- `--session`: Flag to list all your remote sessions.

_Examples:_

```
# List all connected repositories
jules remote list --repo

# List all active and past sessions
jules remote list --session
```

`remote new`

Creates a new remote session to delegate a task to Jules.

Jules can automatically infer the repository from your current working directory, so you can often omit the `--repo` flag.

- `--repo <repo_name>`: Specifies the repository for the session (e.g., torvalds/linux or . for the current directory's repo).

- `--session "<prompt>"`: A string describing the task for Jules to perform.

- `--parallel <number>`: Starts multiple parallel sessions to work on the same task.

_Example:_

```
# Start a new session to write unit tests in the 'torvalds/linux' repo
jules remote new --repo torvalds/linux --session "write unit tests"
```

`remote pull`

Pulls the results (e.g., code changes) from a completed session.

- `--session <session_id>`: The ID of the session you want to pull.

_Example:_

```
# Pull the results for session ID 123456
jules remote pull --session 123456
```

`completion`

Generates an autocompletion script for your shell (e.g., bash, zsh) to enable tab completion for jules commands.

```
# Generate completion script for bash
jules completion bash
```

## Interactive Dashboard (TUI)
For a more interactive, visual experience, you can launch the Terminal User Interface (TUI) by running the jules command without any arguments.

```
jules
```

The TUI provides a dashboard view of your sessions, a side-by-side diff viewer for reviewing changes, and guided flows for creating new ones, similar to the web UI.

---

# Jules REST API

The Jules API lets you programmatically access Jules's capabilities to automate and enhance your software development lifecycle.

> **Note:** The Jules API is in alpha (experimental). Specifications may change.

## Authentication

1. Go to **[Settings](https://jules.google.com/settings#api)** in the Jules web app to create an API key (max 3 keys)
2. Pass the key in the `X-Goog-Api-Key` header

## Base URL

```
https://jules.googleapis.com/v1alpha
```

## Core Resources

- **Source**: A GitHub repository connected to Jules (must install GitHub app first)
- **Session**: A unit of work within a specific context
- **Activity**: Single unit of work within a Session (plans, messages, progress)

## API Endpoints

### List Sources

```bash
curl 'https://jules.googleapis.com/v1alpha/sources' \
    -H 'X-Goog-Api-Key: YOUR_API_KEY'
```

### Create Session

```bash
curl 'https://jules.googleapis.com/v1alpha/sessions' \
    -X POST \
    -H "Content-Type: application/json" \
    -H 'X-Goog-Api-Key: YOUR_API_KEY' \
    -d '{
      "prompt": "Create a boba app!",
      "sourceContext": {
        "source": "sources/github/owner/repo",
        "githubRepoContext": {
          "startingBranch": "main"
        }
      },
      "automationMode": "AUTO_CREATE_PR",
      "title": "My Task"
    }'
```

Options:
- `automationMode`: `"AUTO_CREATE_PR"` to auto-create PR, or omit for manual
- `requirePlanApproval`: `true` to require explicit plan approval

### List Sessions

```bash
curl 'https://jules.googleapis.com/v1alpha/sessions?pageSize=5' \
    -H 'X-Goog-Api-Key: YOUR_API_KEY'
```

### Get Session

```bash
curl 'https://jules.googleapis.com/v1alpha/sessions/SESSION_ID' \
    -H 'X-Goog-Api-Key: YOUR_API_KEY'
```

### Approve Plan (if required)

```bash
curl 'https://jules.googleapis.com/v1alpha/sessions/SESSION_ID:approvePlan' \
    -X POST \
    -H "Content-Type: application/json" \
    -H 'X-Goog-Api-Key: YOUR_API_KEY'
```

### List Activities

```bash
curl 'https://jules.googleapis.com/v1alpha/sessions/SESSION_ID/activities?pageSize=30' \
    -H 'X-Goog-Api-Key: YOUR_API_KEY'
```

### Send Message to Agent

```bash
curl 'https://jules.googleapis.com/v1alpha/sessions/SESSION_ID:sendMessage' \
    -X POST \
    -H "Content-Type: application/json" \
    -H 'X-Goog-Api-Key: YOUR_API_KEY' \
    -d '{
      "prompt": "Can you make the app corgi themed?"
    }'
```

## Full API Reference

See [official API reference](https://developers.google.com/jules/api/reference/rest)

## REST API Reference (Detailed)

**Service Endpoint:** `https://jules.googleapis.com`

### Sessions (`v1alpha.sessions`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `create` | `POST /v1alpha/sessions` | Create a new session |
| `get` | `GET /v1alpha/{name=sessions/*}` | Get a single session |
| `list` | `GET /v1alpha/sessions` | List all sessions |
| `approvePlan` | `POST /v1alpha/{session=sessions/*}:approvePlan` | Approve a plan in a session |
| `sendMessage` | `POST /v1alpha/{session=sessions/*}:sendMessage` | Send a message to a session |

### Activities (`v1alpha.sessions.activities`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `get` | `GET /v1alpha/{name=sessions/*/activities/*}` | Get a single activity |
| `list` | `GET /v1alpha/{parent=sessions/*}/activities` | List activities for a session |

### Sources (`v1alpha.sources`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `get` | `GET /v1alpha/{name=sources/**}` | Get a single source |
| `list` | `GET /v1alpha/sources` | List sources |
