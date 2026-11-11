"""Tests for the content stage: full branch git profile and diff-vocabulary clustering."""

from __future__ import annotations

import json
import subprocess

import pytest


def _git(repo, *args, env=None):
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
        check=True,
        env=env,
    )


@pytest.fixture
def repo(tmp_path):
    path = tmp_path / "repo"
    path.mkdir()
    _git(path, "init", "-q", "-b", "main")
    _git(path, "config", "user.email", "t@example.com")
    _git(path, "config", "user.name", "Tester")
    (path / "src").mkdir()
    (path / "src" / "app.py").write_text("print('hello')\n")
    _git(path, "add", ".")
    _git(path, "commit", "-q", "-m", "initial")
    return path


def _commit(repo, branch, files, message="work", author=None):
    exists = (
        subprocess.run(
            [
                "git",
                "-C",
                str(repo),
                "rev-parse",
                "--verify",
                "--quiet",
                f"refs/heads/{branch}",
            ],
            capture_output=True,
            check=False,
        ).returncode
        == 0
    )
    if exists:
        _git(repo, "checkout", "-q", branch)
    else:
        _git(repo, "checkout", "-q", "-B", branch, "main")
    for rel, content in files.items():
        target = repo / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)
    _git(repo, "add", ".")
    env = None
    if author:
        import os

        env = dict(os.environ, GIT_AUTHOR_NAME=author, GIT_COMMITTER_NAME=author)
    _git(repo, "commit", "-q", "-m", message, env=env)


# ------------------------------------------------------------------ git profile


def test_profile_reports_history_of_the_branch_only(repo):
    from src.analysis.clustering.branch_git import BranchGitProfiler

    _commit(repo, "feature/x", {"src/payments.py": "def charge():\n    pass\n"})
    _commit(
        repo,
        "feature/x",
        {"src/payments.py": "def refund():\n    pass\n"},
        "add refund",
    )

    profile = BranchGitProfiler(str(repo)).profile("feature/x")

    assert profile["commit_count"] == 2
    assert profile["merge_base"] == _git(repo, "rev-parse", "main").stdout.strip()
    assert set(profile["files"]) == {"src/payments.py"}
    assert profile["files"]["src/payments.py"]["touches"] == 2
    assert profile["top_directories"] == {"src": 1}
    assert profile["first_commit"] <= profile["last_commit"]
    json.dumps(profile)


def test_profile_records_every_author(repo):
    from src.analysis.clustering.branch_git import BranchGitProfiler

    _commit(repo, "feature/authors", {"a.py": "x = 1\n"}, "one", author="Ada")
    _commit(repo, "feature/authors", {"b.py": "y = 2\n"}, "two", author="Grace")

    profile = BranchGitProfiler(str(repo)).profile("feature/authors")
    assert set(profile["authors"]) == {"Ada", "Grace"}


def test_profile_raises_without_a_merge_base(repo):
    from src.analysis.clustering.branch_git import BranchGitProfiler

    _git(repo, "checkout", "-q", "--orphan", "orphan")
    _git(repo, "commit", "-q", "-m", "unrelated root", "--allow-empty")

    with pytest.raises(ValueError, match="no merge base"):
        BranchGitProfiler(str(repo)).profile("orphan")


# ------------------------------------------------------------- content documents


def test_documents_carry_paths_identifiers_and_subjects(repo):
    from src.analysis.clustering.branch_git import BranchGitProfiler
    from src.analysis.clustering.content import build_documents

    _commit(
        repo,
        "feature/pay",
        {
            "src/payments/charge_handler.py": "def charge_customer(amount):\n    return 0\n"
        },
        "add charge handler",
    )
    profile = BranchGitProfiler(str(repo)).profile("feature/pay")
    tokens = build_documents(profile, str(repo))["tokens"]

    assert "path/payments" in tokens
    assert "path/charge" in tokens  # camel/snake split of charge_handler.py
    assert "id/charge" in tokens
    assert "msg/charge" in tokens
    assert tokens == [t.lower() for t in tokens]


# --------------------------------------------------------------- content clusters


def _two_communities(repo):
    """Six branches in two content communities, built from real diffs."""
    for i in range(3):
        _commit(
            repo,
            f"payments/{i}",
            {
                f"src/payments/gateway_{i}.py": (
                    f"def settle_invoice_{i}(invoice):\n"
                    f"    gateway_capture(invoice)\n"
                    f"    ledger_reconcile(invoice)\n"
                )
            },
            f"settle invoices via gateway {i}",
        )
        _commit(
            repo,
            f"ui/{i}",
            {
                f"src/ui/widget_{i}.jsx": (
                    f"export function renderWidget{i}(props) {{\n"
                    f"  return <Panel layout={{props}} />;\n"
                    f"}}\n"
                )
            },
            f"render widget {i}",
        )


def test_content_clustering_separates_unrelated_changes(repo):
    from src.analysis.clustering.branch_git import BranchGitProfiler
    from src.analysis.clustering.content import build_documents, cluster_content

    _two_communities(repo)
    profiler = BranchGitProfiler(str(repo))
    documents = {
        name: build_documents(profiler.profile(name), str(repo))["tokens"]
        for name in ["payments/0", "payments/1", "payments/2", "ui/0", "ui/1", "ui/2"]
    }

    result = cluster_content(documents, min_df=1)
    assignments = result["branch_assignments"]

    assert (
        len({assignments[name] for name in ["payments/0", "payments/1", "payments/2"]})
        == 1
    )
    assert len({assignments[name] for name in ["ui/0", "ui/1", "ui/2"]}) == 1
    assert assignments["payments/0"] != assignments["ui/0"]
    assert result["quality_metrics"]["total_clusters"] == 2
    json.dumps(result)


def test_content_clusters_are_interpretable(repo):
    from src.analysis.clustering.branch_git import BranchGitProfiler
    from src.analysis.clustering.content import build_documents, cluster_content

    _two_communities(repo)
    profiler = BranchGitProfiler(str(repo))
    documents = {
        name: build_documents(profiler.profile(name), str(repo))["tokens"]
        for name in ["payments/0", "payments/1", "payments/2", "ui/0", "ui/1", "ui/2"]
    }

    result = cluster_content(documents, min_df=1)
    payload = {tuple(sorted(c["branches"])): c for c in result["clusters"]}
    payments_cluster = next(
        c for c in result["clusters"] if "payments/0" in c["branches"]
    )
    ui_cluster = next(c for c in result["clusters"] if "ui/0" in c["branches"])

    assert any(
        "invoice" in term or "settle" in term
        for term in payments_cluster["signature_terms"]
    )
    assert any(
        "widget" in term or "render" in term for term in ui_cluster["signature_terms"]
    )
    assert payload  # every cluster is addressable by its membership


def test_content_excludes_branches_with_no_diff(repo):
    from src.analysis.clustering.content import cluster_content

    result = cluster_content({"empty": [], "also-empty": []})
    assert result["clusters"] == []
    assert result["excluded_no_content"] == ["also-empty", "empty"]
    assert result["quality_metrics"]["total_clusters"] == 0


def test_content_single_document_does_not_raise(repo):
    from src.analysis.clustering.content import cluster_content

    result = cluster_content({"one": ["id/alpha", "id/beta"]}, min_df=1)
    assert result["quality_metrics"]["total_clusters"] == 1
    assert result["branch_assignments"] == {} or result["document_count"] == 1
    json.dumps(result)


def test_compare_clusterings_reports_agreement(repo):
    from src.analysis.clustering.content import compare_clusterings

    same = {"a": 1, "b": 1, "c": 2}
    assert compare_clusterings(same, same)["adjusted_rand_index"] == 1.0

    different = {"a": 1, "b": 1, "c": 2}
    flipped = {"a": 1, "b": 2, "c": 2}
    out = compare_clusterings(different, flipped)
    assert out["shared_branches"] == 3
    assert out["adjusted_rand_index"] < 1.0

    assert compare_clusterings({"a": 1}, {"a": 1})["adjusted_rand_index"] is None


# ------------------------------------------------- multi-level + deterministic


def test_documents_extract_every_detail_level(repo):
    from src.analysis.clustering.branch_git import BranchGitProfiler
    from src.analysis.clustering.content import LEVEL_WEIGHTS, build_documents

    _commit(
        repo,
        "feature/levels",
        {"src/payments/charge_handler.py": "def charge_customer(amount):\n    pass\n"},
        "settle invoice via gateway",
    )
    profile = BranchGitProfiler(str(repo)).profile("feature/levels")
    document = build_documents(profile, str(repo))

    assert set(document["levels"]) == set(LEVEL_WEIGHTS)
    assert any(token.startswith("prefix/src") for token in document["levels"]["path"])
    assert any(token.startswith("pair/") for token in document["levels"]["path_pair"])
    assert any(token.startswith("id/charge") for token in document["levels"]["symbol"])
    assert any(token.startswith("cg/") for token in document["levels"]["subword"])
    assert document["tokens"] == [
        token for level in document["levels"].values() for token in level
    ]


def test_hash_mapping_is_stable_across_processes(tmp_path):
    """The bucket for a token may not depend on PYTHONHASHSEED or the process."""
    import os
    import sys

    snippet = (
        "import sys; sys.path.insert(0, sys.argv[1]);"
        "from src.analysis.clustering.content import stable_bucket;"
        "print(stable_bucket('id/invoice'))"
    )
    root = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    )
    outputs = []
    for seed in ("1", "12345"):
        env = dict(os.environ, PYTHONHASHSEED=seed)
        outputs.append(
            subprocess.run(
                [sys.executable, "-c", snippet, root],
                capture_output=True,
                text=True,
                check=True,
                env=env,
            ).stdout.strip()
        )
    assert outputs[0] == outputs[1]

    from src.analysis.clustering.content import stable_bucket

    assert outputs[0] == str(stable_bucket("id/invoice"))


def test_content_clustering_is_repeatable(repo):
    from src.analysis.clustering.branch_git import BranchGitProfiler
    from src.analysis.clustering.content import build_documents, cluster_content

    _two_communities(repo)
    profiler = BranchGitProfiler(str(repo))
    documents = {
        name: build_documents(profiler.profile(name), str(repo))
        for name in ["payments/0", "payments/1", "payments/2", "ui/0", "ui/1", "ui/2"]
    }

    first = cluster_content(documents)
    second = cluster_content(documents)

    assert first["branch_assignments"] == second["branch_assignments"]
    assert [c["signature_terms"] for c in first["clusters"]] == [
        c["signature_terms"] for c in second["clusters"]
    ]
    assert first["hierarchy"] == second["hierarchy"]


def test_hierarchy_reports_coarse_to_fine_cuts(repo):
    from src.analysis.clustering.branch_git import BranchGitProfiler
    from src.analysis.clustering.content import build_documents, cluster_content

    _two_communities(repo)
    profiler = BranchGitProfiler(str(repo))
    documents = {
        name: build_documents(profiler.profile(name), str(repo))
        for name in ["payments/0", "payments/1", "payments/2", "ui/0", "ui/1", "ui/2"]
    }

    result = cluster_content(documents)

    hierarchy = result["hierarchy"]
    assert hierarchy
    thresholds = [row["threshold"] for row in hierarchy]
    assert thresholds == sorted(thresholds)
    assert sum(1 for row in hierarchy if row["primary"]) == 1
    assert set(result["level_agreement"]) == set(result["levels"])
    for cluster in result["clusters"]:
        assert cluster["signature_terms"]
        assert len(cluster["branches"]) == cluster["size"]
    json.dumps(result)
