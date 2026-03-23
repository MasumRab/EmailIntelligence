# Quickstart: Guided CLI Workflows

## Overview
The guided workflows help you navigate the repository's orchestration rules without memorizing them.

## Prerequisites
- Python 3.12+
- `launch.py` (in root)

## Usage

### 1. Development Guidance
When starting a task, determine if you need to be on a specific branch:

```bash
python launch.py guide-dev
```

Follow the prompts to select your task type (App Code vs. Shared Config).

### 2. PR Resolution Guidance
When you are ready to merge or resolve conflicts:

```bash
python launch.py guide-pr
```

Follow the prompts to select your PR type (Orchestration vs. Feature) and receive the correct merge commands.
