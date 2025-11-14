# Research for Toolset Additive Analysis

## Static Analysis and Dependency Parsing Libraries

### Decision: Initial implementation will leverage Python's built-in `ast` module for Python scripts and basic regex/string parsing for shell scripts and configuration files. For dependency manifest files, existing Python libraries like `pip-tools` or `poetry` will be explored.

### Rationale:
The `plan.md` mentions "potentially a static analysis library" and "a dependency parsing library". For initial implementation, using built-in Python capabilities (`ast` module) and basic parsing for other file types minimizes immediate external dependencies and allows for rapid prototyping.

However, for more robust and accurate analysis, especially for complex dependency resolution and deeper semantic understanding of code, dedicated external libraries will be necessary.

### Alternatives considered:
*   **Tree-sitter**: A parser generator tool and an incremental parsing library. Offers language-agnostic AST parsing, which would be ideal for semantic analysis across multiple languages. Requires integration and potentially language-specific grammars.
*   **LSP (Language Server Protocol) clients**: Could provide rich semantic information for various languages. Requires integration with LSP servers.
*   **Dedicated dependency parsers**: Libraries specifically designed for parsing `requirements.txt`, `pyproject.toml`, `package.json`, etc., to build accurate dependency graphs.

### Next Steps:
During the implementation of the `file_parser` and `dependency_analyzer` in `src/lib/` and `src/services/`, a dedicated research spike will be conducted to evaluate and select the most suitable static analysis and dependency parsing libraries, considering accuracy, performance, language support, and ease of integration.
