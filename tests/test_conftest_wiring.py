import ast
import pathlib

CONFTEST = (pathlib.Path(__file__).resolve().parents[1]
            / "src" / "backend" / "python_backend" / "tests" / "conftest.py")

def test_fixture_resets_engine_after_yield():
    tree = ast.parse(CONFTEST.read_text())
    fn = next(n for n in tree.body
              if isinstance(n, ast.FunctionDef) and n.name == "client_with_real_workflows")

    yields = [n for n in ast.walk(fn) if isinstance(n, ast.Yield)]
    assert len(yields) == 1, f"expected one yield in the fixture, found {len(yields)}"

    resets = [n for n in ast.walk(fn)
              if isinstance(n, ast.Call)
              and isinstance(n.func, ast.Attribute)
              and n.func.attr == "reset_workflow_engine"]
    assert resets, "client_with_real_workflows no longer calls reset_workflow_engine()"
    assert min(c.lineno for c in resets) > yields[0].lineno, (
        "reset_workflow_engine() runs before the yield; it must run on teardown")
