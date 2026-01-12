# CLI Contracts for Toolset Additive Analysis

This document defines the command-line interface (CLI) contracts for the
`git-verifier` tool's `analyze-toolset` command, ensuring consistent behavior
and argument parsing. These contracts will be used for automated testing and documentation.

## Global Options

-   `--repo-path <path>`: Optional. Path to the Git repository. Defaults to the current working directory.
-   `--branch <name>`: Optional. The local branch to analyze. Defaults to the current branch.

## 1. `git-verifier analyze-toolset` Command

Analyzes the existing toolset within a Git repository and its local branches to
understand its components, dependencies, and functionalities, and to identify
optimal points for additive feature integration.

### Usage:
`git-verifier analyze-toolset [--repo-path <path>] [--branch <name>] [--output-file <path>]`

### Options:
-   `--repo-path <path>`: Optional. Path to the Git repository. Defaults to the current working directory.
-   `--branch <name>`: Optional. The local branch to analyze. Defaults to the current branch.
-   `--output-file <path>`: Path to save the analysis report in machine-readable format (e.g., JSON). If not provided, prints to standard output.
