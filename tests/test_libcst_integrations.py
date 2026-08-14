import pytest
import ast
import tempfile
import os
from pathlib import Path
from emailintelligence_cli import EmailIntelligenceCLI
from src.cli.commands.analysis.compare import CompareCommand
from src.cli.commands.analysis.import_audit import ImportAuditCommand, ImportTransformer
from src.cli.commands.task.engine.branch_clustering import BranchAnalyzer
import libcst as cst

def test_email_cli_compliance():
    cli = EmailIntelligenceCLI()
    # Mocking metadata and conflicts to test line 646 logic
    metadata = {
        "conflicts": [
            {
                "file": "test_compliance.py"
            }
        ]
    }
    with open("test_compliance.py", "w") as f:
        f.write('def test_func():\n    """This is a valid docstring."""\n    pass')

    cli.fs_proxy = type("MockFS", (), {"exists": lambda self, x: True, "read_file": lambda self, x: open(x).read()})()

    # Requirement should pass docstring check
    req = {"name": "Code must have docstring", "type": "MUST"}
    result = cli._assess_governance_compliance(metadata.get('conflicts', []), {"requirements": [req]})

    assert len(result['conformant_requirements']) > 0
    os.remove("test_compliance.py")

def test_email_cli_alignment():
    cli = EmailIntelligenceCLI()
    with open("test_align.py", "w") as f:
        f.write('def complex_func():\n    x = 1\n    y = 2\n    return x + y\n')

    cli.fs_proxy = type("MockFS", (), {"exists": lambda self, x: True, "read_file": lambda self, x: open(x).read()})()

    # Test alignment scoring algorithm natively processes and produces a stable score
    conflicts = [{"file": "test_align.py"}]
    # We call the strategy generator logic to hit line 887
    metadata = {"conflicts": conflicts, "source_branch": "a", "target_branch": "b", "pr_number": 123}
    strategy = cli._generate_spec_kit_strategy(metadata, None)

    assert strategy['phases'][0]['steps'][0]['alignment_score'] != "0.75"
    assert strategy['phases'][0]['steps'][0]['alignment_score'] != "0%"
    os.remove("test_align.py")

def test_branch_clustering_semantics():
    analyzer = BranchAnalyzer()
    content = "import os\n\ndef test_feature():\n    '''Comment'''\n    pass\n\nclass TestClass:\n    pass"
    res = analyzer.analyze_file(content)

    # Verify libcst correctly extracted deep semantic features
    assert "test_feature" in res["functions"]
    assert "TestClass" in res["classes"]
    assert "os" in res["imports"]
    assert "Comment" in "".join(res["comments"])

def test_compare_extraction_and_drift():
    cmd = CompareCommand()
    with open("test_base.py", "w") as f:
        f.write("def foo():\n    return 1")
    with open("test_head.py", "w") as f:
        f.write("def foo():\n    return 2")

    dna_base = cmd._extract_logical_dna(Path("test_base.py"))
    dna_head = cmd._extract_logical_dna(Path("test_head.py"))

    # Signatures must be stable CST hash
    assert dna_base["foo"]["sig"] != dna_head["foo"]["sig"]

    # Drift parameterized detection
    wrapper_base = {"dna": dna_base, "file": "base", "patterns": {}}
    wrapper_head = {"dna": dna_head, "file": "head", "patterns": {}}

    res = cmd._compare_dna(wrapper_base, wrapper_head, strategy="logic-drift")
    assert res["drifts"][0]["similarity"] > 0.0 # fuzzy matching detects similarity

    res_strict = cmd._compare_dna(wrapper_base, wrapper_head, strategy="logic-compare")
    assert res_strict["drifts"][0]["similarity"] == 0.0 # Strict structural failure

    os.remove("test_base.py")
    os.remove("test_head.py")

def test_import_audit_roundtrip():
    # Test lossless round-trip CST import transformation
    source = "import os\n# Critical comment\nfrom old_module import func\n"
    expected = "import os\n# Critical comment\nfrom new_module import func\n"

    mapping = {"old_module": "new_module"}
    tree = cst.parse_module(source)
    transformer = ImportTransformer(mapping)
    modified = tree.visit(transformer)

    assert modified.code == expected
    assert transformer.modified == True
