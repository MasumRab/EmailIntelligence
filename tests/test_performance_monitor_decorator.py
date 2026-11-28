import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.backend.python_backend import performance_monitor as pm


def _read_log(path):
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()]


def test_positional_form_names_the_operation(tmp_path, monkeypatch):
    # @log_performance("name") used to raise UnboundLocalError at decoration time,
    # because `decorator` is a local assigned only in the other branch.
    log = tmp_path / "perf.jsonl"
    monkeypatch.setattr(pm, "LOG_FILE", str(log))

    @pm.log_performance("load_data")
    def work():
        return "ok"

    assert work() == "ok"
    assert _read_log(log)[0]["operation"] == "load_data"


def test_bare_form_uses_function_name(tmp_path, monkeypatch):
    log = tmp_path / "perf.jsonl"
    monkeypatch.setattr(pm, "LOG_FILE", str(log))

    @pm.log_performance
    def work():
        return "ok"

    assert work() == "ok"
    assert _read_log(log)[0]["operation"] == "work"


def test_keyword_form_names_the_operation(tmp_path, monkeypatch):
    log = tmp_path / "perf.jsonl"
    monkeypatch.setattr(pm, "LOG_FILE", str(log))

    @pm.log_performance(operation="custom")
    def work():
        return "ok"

    assert work() == "ok"
    assert _read_log(log)[0]["operation"] == "custom"


def test_database_module_imports():
    # database.py applies the positional form at class-body scope, so the
    # decorator's failure made the whole module unimportable.
    import src.backend.python_backend.database  # noqa: F401
