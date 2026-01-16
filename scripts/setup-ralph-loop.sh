#!/bin/bash

# Ralph Wiggum Loop Setup Script
# Creates the loop state file for iterative development

# Default values
TASK_PROMPT=""
MAX_ITERATIONS=""
COMPLETION_PROMISE=""
EXTENSION_PATH="$(cd "$(dirname "$0")" && pwd)"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --max-iterations)
            MAX_ITERATIONS="$2"
            shift 2
            ;;
        --completion-promise)
            COMPLETION_PROMISE="$2"
            shift 2
            ;;
        *)
            # If TASK_PROMPT is empty, assign the first non-option argument
            if [ -z "$TASK_PROMPT" ]; then
                TASK_PROMPT="$1"
            fi
            shift
            ;;
    esac
done

# Validate required argument
if [ -z "$TASK_PROMPT" ]; then
    echo "Error: Task prompt is required"
    echo "Usage: $0 <task_prompt> [--max-iterations <n>] [--completion-promise '<text>']"
    exit 1
fi

# Set default max iterations if not provided
if [ -z "$MAX_ITERATIONS" ]; then
    MAX_ITERATIONS=20
fi

# Create state file
STATE_FILE=".gemini/ralph-loop.local.md"

cat > "$STATE_FILE" << EOF
# Ralph Loop State

## Configuration
- **Task Prompt**: $TASK_PROMPT
- **Max Iterations**: $MAX_ITERATIONS
- **Completion Promise**: ${COMPLETION_PROMISE:-None}

## Status
- **Current Status**: initialized
- **Current Iteration**: 0
- **Started At**: $(date -u +"%Y-%m-%dT%H:%M:%SZ")

## Results
- **Best Distance Achieved**: N/A
- **Best Similarity Achieved**: N/A
- **Convergence Threshold**: 0.01

## Instructions
This loop is designed to iteratively improve the task structure process to enhance PRD to task.json fidelity without losing the original task specification fidelity.

Current iteration: 0/$MAX_ITERATIONS

EOF

echo "Ralph loop state file created at $STATE_FILE"
echo "Task: $TASK_PROMPT"
echo "Max iterations: $MAX_ITERATIONS"
if [ -n "$COMPLETION_PROMISE" ]; then
    echo "Completion promise: $COMPLETION_PROMISE"
fi