import os
from collections import defaultdict


def get_file_category(filepath):
    """Categorizes a file based on its path and extension."""
    if "test" in filepath.lower():
        return "Testing"
    if filepath.endswith(".md"):
        return "Documentation"
    if "config" in filepath.lower() or filepath.endswith(
        (".yml", ".yaml", ".json", ".toml")
    ):
        return "Configuration"
    if "script" in filepath.lower() or filepath.endswith((".sh", ".bat")):
        return "Scripting"
    if filepath.endswith(".py"):
        return "Core Logic"
    if filepath.endswith((".js", ".ts", ".tsx", ".jsx", ".html", ".css")):
        return "Frontend"
    if "notebook" in filepath.lower() or filepath.endswith(".ipynb"):
        return "Notebook"
    if "data" in filepath.lower() or filepath.endswith(
        (".csv", ".jsonl", ".db", ".sqlite")
    ):
        return "Data"
    if "docker" in filepath.lower() or "dockerfile" in filepath.lower():
        return "Containerization"
    if "github" in filepath.lower() or "gitlab" in filepath.lower():
        return "CI/CD"
    if "docs" in filepath.lower():
        return "Documentation"
    if "assets" in filepath.lower() or filepath.endswith(
        (".png", ".jpg", ".svg", ".ico")
    ):
        return "Asset"
    return "Other"


import ast


def analyze_file(filepath):
    """Analyzes a single file for metrics using AST."""
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            lines = content.splitlines()
    except Exception:
        return 0, 0, 0, 0, []

    loc = len(lines)
    imports = []
    functions = 0
    classes = 0

    if filepath.endswith(".py"):
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)
                elif isinstance(node, ast.FunctionDef):
                    functions += 1
                elif isinstance(node, ast.ClassDef):
                    classes += 1
        except SyntaxError:
            # Fallback for files that can't be parsed
            return loc, 0, 0, 0, []

    return loc, len(imports), functions, classes, imports


def resolve_import_path(import_name, current_file_path, root_dir):
    """Resolves an import name to a file path."""
    # Convert import name to path format
    rel_path = import_name.replace(".", os.path.sep)

    # Check for absolute import from root
    abs_path_py = os.path.join(root_dir, rel_path + ".py")
    abs_path_init = os.path.join(root_dir, rel_path, "__init__.py")

    if os.path.exists(abs_path_py):
        return os.path.relpath(abs_path_py, root_dir)
    if os.path.exists(abs_path_init):
        return os.path.relpath(abs_path_init, root_dir)

    # Simple relative import logic (can be expanded)
    # from . import foo -> from current_dir import foo
    if import_name.startswith("."):
        current_dir = os.path.dirname(current_file_path)
        rel_import_path = import_name.lstrip(".")
        rel_path = rel_import_path.replace(".", os.path.sep)

        rel_path_py = os.path.join(current_dir, rel_path + ".py")
        rel_path_init = os.path.join(current_dir, rel_path, "__init__.py")

        if os.path.exists(rel_path_py):
            return os.path.relpath(rel_path_py, root_dir)
        if os.path.exists(rel_path_init):
            return os.path.relpath(rel_path_init, root_dir)

    return None  # External library or couldn't resolve


def analyze_repository(root_dir):
    """Analyzes all files in the repository."""
    file_metrics = defaultdict(list)
    dependency_graph = defaultdict(list)

    py_files = []
    for subdir, _, files in os.walk(root_dir):
        if ".git" in subdir.split(os.path.sep):
            continue
        for file in files:
            py_files.append(os.path.join(subdir, file))

    for filepath in py_files:
        loc, num_imports, functions, classes, raw_imports = analyze_file(filepath)
        category = get_file_category(filepath)
        relative_filepath = os.path.relpath(filepath, root_dir)

        file_metrics[os.path.dirname(relative_filepath)].append(
            {
                "filename": os.path.basename(relative_filepath),
                "loc": loc,
                "imports": num_imports,
                "functions": functions,
                "classes": classes,
                "category": category,
            }
        )

        if relative_filepath.endswith(".py"):
            for imp in raw_imports:
                resolved_path = resolve_import_path(imp, filepath, root_dir)
                if resolved_path:
                    dependency_graph[relative_filepath].append(resolved_path)

    return file_metrics, dependency_graph


def find_circular_dependencies(graph):
    """Finds circular dependencies in the graph using DFS."""
    cycles = []
    path = []
    visiting = set()
    visited = set()

    def dfs(node):
        visiting.add(node)
        path.append(node)
        for neighbor in graph.get(node, []):
            if neighbor in path:
                try:
                    cycle_start_index = path.index(neighbor)
                    cycle = path[cycle_start_index:]
                    sorted_cycle = tuple(sorted(cycle))
                    if sorted_cycle not in [tuple(sorted(c)) for c in cycles]:
                        cycles.append(cycle)
                except ValueError:
                    pass
            elif neighbor not in visited:
                dfs(neighbor)
        path.pop()
        visiting.remove(node)
        visited.add(node)

    for node in sorted(list(graph.keys())):
        if node not in visited:
            dfs(node)
    return cycles


def calculate_coupling(graph):
    """Calculates afferent (incoming) and efferent (outgoing) coupling."""
    efferent_coupling = {node: len(deps) for node, deps in graph.items()}
    afferent_coupling = defaultdict(int)
    all_nodes = set(graph.keys())

    for node, deps in graph.items():
        for dep in deps:
            afferent_coupling[dep] += 1
            all_nodes.add(dep)

    for node in all_nodes:
        if node not in efferent_coupling:
            efferent_coupling[node] = 0  # Files that import nothing

    return afferent_coupling, efferent_coupling


def find_orphan_files(graph, all_py_files):
    """Finds python files that are not imported by any other file."""
    afferent_coupling, _ = calculate_coupling(graph)
    orphans = [
        f
        for f in all_py_files
        if afferent_coupling.get(f, 0) == 0 and not f.endswith("__init__.py")
    ]
    return orphans


def generate_comprehensive_report(
    file_metrics, graph, all_py_files, output_file="comprehensive_analysis_report.md"
):
    """Generates a comprehensive markdown report."""
    with open(output_file, "w") as f:
        f.write("# Comprehensive Repository Analysis Report\n\n")

        # Part 1: Architectural Analysis
        f.write("## Part 1: Architectural Analysis\n\n")

        # Circular Dependencies
        cycles = find_circular_dependencies(graph)
        f.write("### Circular Dependencies\n\n")
        if cycles:
            f.write("Found {} circular dependencies:\n".format(len(cycles)))
            for i, cycle in enumerate(cycles):
                f.write(f"- Cycle {i + 1}: `{' -> '.join(cycle)} -> {cycle[0]}`\n")
        else:
            f.write("No circular dependencies found. Excellent!\n")
        f.write("\n")

        # Coupling Metrics
        afferent, efferent = calculate_coupling(graph)
        f.write("### Module Coupling\n\n")
        f.write("#### Top 10 Most Depended-Upon Modules (Highest Afferent Coupling)\n")
        sorted_afferent = sorted(
            afferent.items(), key=lambda item: item[1], reverse=True
        )
        f.write("| Module | Imported By # Files |\n")
        f.write("|--------|---------------------|\n")
        for module, count in sorted_afferent[:10]:
            f.write(f"| `{module}` | {count} |\n")
        f.write("\n")

        f.write("#### Top 10 Most Dependent Modules (Highest Efferent Coupling)\n")
        sorted_efferent = sorted(
            efferent.items(), key=lambda item: item[1], reverse=True
        )
        f.write("| Module | Imports # Files |\n")
        f.write("|--------|-----------------|\n")
        for module, count in sorted_efferent[:10]:
            f.write(f"| `{module}` | {count} |\n")
        f.write("\n")

        # Orphan Files
        orphans = find_orphan_files(graph, all_py_files)
        f.write("### Orphan Files (Potential Unused Code or Entrypoints)\n\n")
        if orphans:
            f.write("Found {} potential orphan files:\n".format(len(orphans)))
            for orphan in orphans:
                f.write(f"- `{orphan}`\n")
        else:
            f.write("No orphan files found.\n")
        f.write("\n")

        # Part 2: Detailed File Metrics
        f.write("---\n\n## Part 2: Detailed File Metrics\n\n")
        sorted_directories = sorted(file_metrics.keys())

        for directory in sorted_directories:
            metrics = file_metrics[directory]
            f.write(f"### Directory: `{directory or './'}`\n\n")
            f.write("| File | LOC | Imports | Functions | Classes | Category |\n")
            f.write("|------|-----|---------|-----------|---------|----------|\n")
            for metric in sorted(metrics, key=lambda x: x["filename"]):
                f.write(
                    f"| {metric['filename']} | {metric['loc']} | {metric['imports']} | {metric['functions']} | {metric['classes']} | {metric['category']} |\n"
                )
            f.write("\n")


if __name__ == "__main__":
    repo_root = "."
    metrics, dependency_graph = analyze_repository(repo_root)
    all_py_files = [f for f in dependency_graph.keys()]
    generate_comprehensive_report(metrics, dependency_graph, all_py_files)
    print("Analysis complete. Report generated in 'comprehensive_analysis_report.md'.")
