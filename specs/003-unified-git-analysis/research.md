# Research for Unified Git Analysis and Verification

## Diffing Library Selection

### Decision: GitPython's built-in diffing capabilities with potential for external library integration.

### Rationale:
The `plan.md` mentions "potentially a diffing library for detailed content comparison" and "A diff parsing library will extract significant code changes." While GitPython provides basic diffing, a more robust solution for semantic code change prioritization and intent inference might require a specialized library.

For initial implementation, we will leverage GitPython's existing diffing capabilities (e.g., `git.Commit.diff()`) to extract raw diff content. This minimizes initial external dependencies.

However, for advanced "Code Change Prioritization" (as described in FR-001 and detailed in the `analysis_service.py` TODO), a more sophisticated diff parsing library will be necessary. This will be a subject of further research during implementation of T010 (core narrative synthesis logic) and the `DiffParser` methods.

### Alternatives considered:
*   **Tree-sitter**: A parser generator tool and an incremental parsing library. Offers language-agnostic AST parsing, which would be ideal for semantic diffing. Requires integration and potentially language-specific grammars.
*   **Pydiff**: A Python library for diffing. Might offer more granular control than GitPython's raw diff output.
*   **Custom parsing**: Implementing a custom diff parser from scratch. This is high effort and prone to errors.

### Next Steps:
During the implementation of the `DiffParser` in `src/lib/`, a dedicated research spike will be conducted to evaluate and select the most suitable diffing library for semantic code change analysis, considering performance, language support, and ease of integration.