"""Tests for the task-002 branch clustering pipeline.

Each test builds a throwaway git repository so the analyzers run against real
``git`` output rather than mocks.
"""

from __future__ import annotations

import json
import subprocess

import pytest


def _git(repo, *args, check=True):
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
        check=check,
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
    (path / "README.md").write_text("# app\n")
    _git(path, "add", ".")
    _git(path, "commit", "-q", "-m", "initial")
    return path


def _commit(repo, branch, files):
    _git(repo, "checkout", "-q", "-B", branch, "main")
    for rel, content in files.items():
        target = repo / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)
    _git(repo, "add", ".")
    _git(repo, "commit", "-q", "-m", f"work on {branch}")


# --------------------------------------------------------------- analyzers


def test_commit_history_reports_metrics(repo):
    from src.analysis.clustering.commit_history import CommitHistoryAnalyzer

    _commit(repo, "feature/x", {"src/app.py": "print('v2')\n"})
    result = CommitHistoryAnalyzer(str(repo)).analyze_sync("feature/x")

    assert result["branch_name"] == "feature/x"
    assert set(result["metrics"]) == {
        "commit_recency",
        "commit_frequency",
        "authorship_diversity",
        "merge_readiness",
        "stability_score",
    }
    assert 0.0 <= result["aggregate_score"] <= 1.0
    assert result["commits_behind_main"] == 0
    assert result["commit_count"] == 1  # only the branch's own commit
    # Round-trips through JSON: no numpy or datetime leaking out.
    json.dumps(result)


def test_commit_history_recency_decays_with_age(repo):
    from src.analysis.clustering.commit_history import CommitHistoryAnalyzer

    _commit(repo, "feature/old", {"src/app.py": "print('v2')\n"})
    analyzer = CommitHistoryAnalyzer(str(repo))
    fresh = analyzer.analyze_sync("feature/old")["metrics"]["commit_recency"]
    assert fresh > 0.99  # just committed


def test_commit_history_no_unique_commits_is_zero_not_an_error(repo):
    from src.analysis.clustering.commit_history import CommitHistoryAnalyzer

    _git(repo, "branch", "feature/noop", "main")
    result = CommitHistoryAnalyzer(str(repo)).analyze_sync("feature/noop")

    assert result["commit_count"] == 0
    assert result["no_unique_commits"] is True
    assert result["aggregate_score"] == 0.0


def test_structure_reports_spec_metric_names(repo):
    from src.analysis.clustering.structure import CodebaseStructureAnalyzer

    _commit(repo, "feature/src-only", {"src/extra.py": "print('v2')\n"})
    result = CodebaseStructureAnalyzer(str(repo)).analyze("feature/src-only")

    assert set(result["metrics"]) == {
        "directory_similarity",
        "file_additions",
        "core_module_stability",
        "namespace_isolation",
    }
    assert result["new_files"] == 1
    assert result["metrics"]["namespace_isolation"] == 1.0
    assert result["metrics"]["core_module_stability"] == 1.0


def test_structure_penalises_core_deletion(repo):
    from src.analysis.clustering.structure import CodebaseStructureAnalyzer

    (repo / "config").mkdir()
    (repo / "config" / "app.yaml").write_text("a: 1\n")
    _git(repo, "add", ".")
    _git(repo, "commit", "-q", "-m", "add config on main")

    _git(repo, "checkout", "-q", "-B", "feature/drop-core", "main")
    _git(repo, "rm", "-q", "config/app.yaml")
    _git(repo, "commit", "-q", "-m", "drop config file")
    result = CodebaseStructureAnalyzer(str(repo)).analyze("feature/drop-core")

    assert result["deleted_files"] == 1
    assert result["metrics"]["core_module_stability"] == 0.5


def test_structure_reports_zero_for_identical_branch(repo):
    from src.analysis.clustering.structure import CodebaseStructureAnalyzer

    _git(repo, "branch", "feature/noop", "main")
    result = CodebaseStructureAnalyzer(str(repo)).analyze("feature/noop")

    assert result["changed_files"] == 0
    assert result["aggregate_score"] == 0.0


def test_diff_distance_metrics_and_counts(repo):
    from src.analysis.clustering.diff_distance import DiffDistanceCalculator

    _commit(repo, "feature/docs", {"docs/guide.md": "line\n" * 10})
    result = DiffDistanceCalculator(str(repo)).analyze("feature/docs")

    assert result["files_affected"] == 1
    assert result["total_lines_added"] == 10
    assert result["total_lines_changed"] == 10
    # A docs-only, one-file diff must not be reported as high risk.
    assert result["metrics"]["integration_risk"] > 0.9
    json.dumps(result)


def test_diff_distance_penalises_critical_paths(repo):
    from src.analysis.clustering.diff_distance import DiffDistanceCalculator

    _commit(repo, "feature/config", {"config/settings.yaml": "a: 1\n"})
    calc = DiffDistanceCalculator(str(repo))
    result = calc.analyze("feature/config")

    assert calc._classify_risk("config/settings.yaml") == "critical"
    assert result["metrics"]["integration_risk"] == pytest.approx(0.2)


def test_diff_distance_handles_binary_files(repo):
    from src.analysis.clustering.diff_distance import DiffDistanceCalculator

    _git(repo, "checkout", "-q", "-B", "feature/bin", "main")
    (repo / "src" / "blob.bin").write_bytes(b"\x00\x01\x02")
    _git(repo, "add", ".")
    _git(repo, "commit", "-q", "-m", "binary")

    result = DiffDistanceCalculator(str(repo)).analyze("feature/bin")
    assert result["files_affected"] == 1
    assert result["total_lines_changed"] == 0
    assert result["metrics"]["diff_complexity"] == 0.0


def test_diff_distance_rejects_non_repository(tmp_path):
    from src.analysis.clustering.diff_distance import DiffDistanceCalculator

    with pytest.raises(ValueError):
        DiffDistanceCalculator(str(tmp_path))


# ---------------------------------------------------------------- clusterer


def _blocks(history, structure, diff):
    return {
        "commit_history": {"aggregate_score": history},
        "codebase_structure": {"aggregate_score": structure},
        "diff_distance": {"aggregate_score": diff},
    }


def test_clusterer_weights_are_applied(repo):
    from src.analysis.clustering.clusterer import BranchClusterer

    outputs = {
        "a": _blocks(1.0, 0.0, 0.0),
        "b": _blocks(0.0, 1.0, 0.0),
        "c": _blocks(0.0, 0.0, 1.0),
    }
    result = BranchClusterer(str(repo)).cluster(outputs)

    centers = {c["cluster_id"]: c["cluster_center"] for c in result["clusters"]}
    assert len(result["branch_assignments"]) == 3
    for center in centers.values():
        expected = (
            0.35 * center["commit_history_weight"]
            + 0.35 * center["codebase_structure_weight"]
            + 0.30 * center["diff_distance_weight"]
        )
        assert center["combined_score"] == pytest.approx(expected)


def test_clusterer_output_is_json_serialisable(repo):
    from src.analysis.clustering.clusterer import BranchClusterer

    outputs = {f"b{i}": _blocks(i / 10, 1 - i / 10, 0.5) for i in range(10)}
    result = BranchClusterer(str(repo)).cluster(outputs)
    json.dumps(result)
    assert result["dendogram_data"]["branch_indices"] == list(range(10))
    assert len(result["dendogram_data"]["linkage_matrix"]) == 9


def test_clusterer_single_branch_does_not_raise(repo):
    from src.analysis.clustering.clusterer import BranchClusterer

    result = BranchClusterer(str(repo)).cluster({"only": _blocks(0.5, 0.5, 0.5)})
    assert result["quality_metrics"]["total_clusters"] == 1
    assert result["branch_assignments"] == {"only": 1}
    json.dumps(result)


def test_clusterer_identical_vectors_does_not_raise(repo):
    from src.analysis.clustering.clusterer import BranchClusterer

    outputs = {f"b{i}": _blocks(0.4, 0.4, 0.4) for i in range(5)}
    result = BranchClusterer(str(repo)).cluster(outputs)
    assert result["quality_metrics"]["total_clusters"] == 1
    assert result["quality_metrics"]["silhouette_avg"] == 0.0


def test_clusterer_rejects_missing_block(repo):
    from src.analysis.clustering.clusterer import BranchClusterer

    with pytest.raises(ValueError, match="diff_distance"):
        BranchClusterer(str(repo)).cluster(
            {
                "a": {
                    "commit_history": {"aggregate_score": 0.1},
                    "codebase_structure": {"aggregate_score": 0.1},
                },
            }
        )


def test_clusterer_empty_input(repo):
    from src.analysis.clustering.clusterer import BranchClusterer

    result = BranchClusterer(str(repo)).cluster({})
    assert result["clusters"] == []
    assert result["quality_metrics"]["total_clusters"] == 0


# ------------------------------------------------------------------ targets


def test_assigner_heuristic_prefers_main_for_ready_branch(repo):
    from src.analysis.clustering.targets import IntegrationTargetAssigner

    outputs = {
        "feature/x": {
            "commit_history": {
                "aggregate_score": 0.9,
                "metrics": {
                    "merge_readiness": 0.95,
                    "commit_recency": 0.9,
                    "authorship_diversity": 0.1,
                },
            },
            "codebase_structure": {"aggregate_score": 0.9, "metrics": {}},
            "diff_distance": {
                "aggregate_score": 0.9,
                "files_affected": 2,
                "metrics": {"integration_risk": 0.1, "code_churn": 0.9},
            },
        }
    }
    cluster_data = {"branch_assignments": {"feature/x": 0}}
    out = IntegrationTargetAssigner(str(repo)).assign(cluster_data, outputs)
    row = out["categorized_branches"]["feature/x"]

    assert row["integration_target"] == "main"
    assert row["confidence"] == 0.95
    assert "ready-for-merge" in row["tags"]


def test_assigner_matches_domain_on_segments_not_substrings(repo):
    from src.analysis.clustering.targets import IntegrationTargetAssigner

    assigner = IntegrationTargetAssigner(str(repo))
    metrics = {
        "codebase_structure": 0.5,
        "files_affected": 3,
        "code_churn": 0.5,
        "integration_risk": 0.5,
        "diff_complexity": 0.5,
        "commit_history": 0.5,
        "diff_distance": 0.5,
        "commit_recency": 0.5,
        "merge_readiness": 0.5,
        "authorship_diversity": 0.5,
        "core_module_stability": 1.0,
    }

    # "update-database" must not read as a data-science branch.
    tags = assigner._generate_tags("chore/update-database", metrics, "main")
    assert "data-science" not in tags

    tags = assigner._generate_tags("feature/auth-login", metrics, "main")
    assert "authentication" in tags


def test_assigner_scientific_heuristic(repo):
    from src.analysis.clustering.targets import IntegrationTargetAssigner

    outputs = {
        "science/dataset": {
            "commit_history": {"aggregate_score": 0.5, "metrics": {}},
            "codebase_structure": {"aggregate_score": 0.5, "metrics": {}},
            "diff_distance": {
                "aggregate_score": 0.5,
                "files_affected": 20,
                "metrics": {},
            },
        }
    }
    out = IntegrationTargetAssigner(str(repo)).assign(
        {"branch_assignments": {"science/dataset": 1}}, outputs
    )
    row = out["categorized_branches"]["science/dataset"]
    assert row["integration_target"] == "scientific"
    assert "scientific-branch" in row["tags"]


def test_assigner_default_when_nothing_matches(repo):
    from src.analysis.clustering.targets import IntegrationTargetAssigner

    outputs = {
        "chore/misc": {
            "commit_history": {"aggregate_score": 0.3, "metrics": {}},
            "codebase_structure": {"aggregate_score": 0.3, "metrics": {}},
            "diff_distance": {
                "aggregate_score": 0.3,
                "files_affected": 40,
                "metrics": {},
            },
        }
    }
    out = IntegrationTargetAssigner(str(repo)).assign(
        {"branch_assignments": {"chore/misc": 1}}, outputs
    )
    row = out["categorized_branches"]["chore/misc"]
    assert row["integration_target"] == "main"
    assert row["confidence"] == 0.65
    assert row["decision_rationale"] == "Default assignment (no rule matched)"


def test_assigner_summary_and_catalog(repo):
    from src.analysis.clustering.targets import IntegrationTargetAssigner

    outputs = {
        "a": {
            "commit_history": {"aggregate_score": 0.9, "metrics": {}},
            "codebase_structure": {"aggregate_score": 0.9, "metrics": {}},
            "diff_distance": {
                "aggregate_score": 0.9,
                "files_affected": 1,
                "metrics": {},
            },
        },
        "science/b": {
            "commit_history": {"aggregate_score": 0.9, "metrics": {}},
            "codebase_structure": {"aggregate_score": 0.9, "metrics": {}},
            "diff_distance": {
                "aggregate_score": 0.9,
                "files_affected": 1,
                "metrics": {},
            },
        },
    }
    out = IntegrationTargetAssigner(str(repo)).assign(
        {"branch_assignments": {"a": 0, "science/b": 1}}, outputs
    )

    assert out["integration_target_summary"]["main"]["branch_count"] == 1
    assert out["integration_target_summary"]["scientific"]["branch_count"] == 1
    assert set(out["tag_catalog"]["by_category"]) == {
        "scope",
        "risk_level",
        "complexity",
        "dev_status",
        "file_impact",
        "domain",
        "validation",
        "target",
        "special_flags",
    }
    # 30+ distinct tags across the catalog.
    total = sum(len(v) for v in out["tag_catalog"]["by_category"].values())
    assert total >= 30
    assert all(
        row["tags"] == list(dict.fromkeys(row["tags"]))
        for row in out["categorized_branches"].values()
    )
    json.dumps(out)


# ------------------------------------------------------------------- runner


def test_runner_end_to_end_on_real_repo(repo, tmp_path):
    from src.analysis.clustering.__main__ import main

    _commit(repo, "feature/one", {"src/app.py": "print('v2')\n"})
    _git(repo, "checkout", "-q", "main")
    _commit(repo, "feature/two", {"src/other.py": "x = 1\n"})
    _git(repo, "checkout", "-q", "main")
    # Present the branches as origin/* refs, which is what the runner reads.
    _git(repo, "update-ref", "refs/remotes/origin/feature/one", "feature/one")
    _git(repo, "update-ref", "refs/remotes/origin/feature/two", "feature/two")
    _git(repo, "update-ref", "refs/remotes/origin/main", "main")

    out_file = tmp_path / "report.json"
    rc = main(["--repo", str(repo), "--jobs", "2", "--out", str(out_file)])

    assert rc == 0
    report = json.loads(out_file.read_text())
    assert report["branches_considered"] == 2
    assert report["branches_analyzed"] == 2
    assert report["branches_failed"] == []
    assert set(report["clustering"]["branch_assignments"]) == {
        "feature/one",
        "feature/two",
    }
    assert "main" in report["integration_targets"]["integration_target_summary"]


# ------------------------------------------------------------------- report


def _tiny_report():
    return {
        "pipeline": "task-002-clustering",
        "repo": "/tmp/repo",
        "remote": "origin",
        "main_ref": "refs/remotes/origin/main",
        "threshold": 0.5,
        "branches_considered": 3,
        "branches_analyzed": 2,
        "branches_failed": [{"branch": "master", "error": "no merge base"}],
        "clustering": {
            "clusters": [
                {
                    "cluster_id": 1,
                    "branches": ["feature/a"],
                    "size": 1,
                    "cohesion": 1.0,
                    "silhouette_score": 0.0,
                    "cluster_center": {
                        "commit_history_weight": 0.9,
                        "codebase_structure_weight": 0.8,
                        "diff_distance_weight": 0.7,
                        "combined_score": 0.805,
                    },
                },
                {
                    "cluster_id": 2,
                    "branches": ["stale/b"],
                    "size": 1,
                    "cohesion": 1.0,
                    "silhouette_score": 0.0,
                    "cluster_center": {
                        "commit_history_weight": 0.0,
                        "codebase_structure_weight": 0.0,
                        "diff_distance_weight": 0.0,
                        "combined_score": 0.0,
                    },
                },
            ],
            "branch_assignments": {"feature/a": 1, "stale/b": 2},
            "quality_metrics": {
                "total_clusters": 2,
                "silhouette_avg": 0.5,
                "davies_bouldin_index": 0.8,
                "calinski_harabasz_index": 12.0,
            },
            "dendogram_data": {"linkage_matrix": [], "branch_indices": [0, 1]},
        },
        "integration_targets": {
            "categorized_branches": {
                "feature/a": {
                    "integration_target": "main",
                    "decision_rationale": "Heuristic rule match (low churn, few files)",
                    "tags": ["main-ready", "ready-for-merge"],
                },
                "stale/b": {
                    "integration_target": "main",
                    "decision_rationale": "Default assignment (no rule matched)",
                    "tags": ["stale", "main-ready"],
                },
            },
            "integration_target_summary": {
                "main": {
                    "branch_count": 2,
                    "total_confidence": 0.8,
                    "key_tags": ["main-ready"],
                },
                "scientific": {
                    "branch_count": 0,
                    "total_confidence": 0.0,
                    "key_tags": [],
                },
                "orchestration-tools": {
                    "branch_count": 0,
                    "total_confidence": 0.0,
                    "key_tags": [],
                },
            },
        },
    }


def test_report_renders_every_section():
    from src.analysis.clustering.report import render_markdown

    md = render_markdown(_tiny_report())

    assert "# Branch clustering analysis" in md
    assert "| Branches analyzed | 2 |" in md
    assert "zero-score cluster" in md
    assert "| 1 | 1 |" in md
    assert "`main` | 2 | 0.800" in md
    assert "1 · heuristic" in md and "4 · default" in md
    assert "| `master` | no merge base |" in md
    assert "--threshold 0.5" in md


def test_report_renders_the_content_stage():
    from src.analysis.clustering.report import render_markdown

    report = _tiny_report()
    report["content_clustering"] = {
        "method": "tfidf-cosine-average-linkage",
        "note": "Lexical content clustering over paths, identifiers and subjects.",
        "document_count": 2,
        "excluded_no_content": ["stale/b", "empty/c"],
        "clusters": [
            {
                "cluster_id": 1,
                "size": 2,
                "branches": ["feature/a", "feature/b"],
                "cohesion": 0.91,
                "signature_terms": ["path/payments", "id/settle"],
            }
        ],
        "branch_assignments": {"feature/a": 1, "feature/b": 1},
        "quality_metrics": {
            "total_clusters": 1,
            "silhouette_avg": 0.2035,
            "threshold": 0.9,
            "vocabulary_size": 23465,
        },
        "agreement_with_metric_clustering": {
            "shared_branches": 2,
            "adjusted_rand_index": 0.2059,
        },
    }

    md = render_markdown(report)

    assert "## Content clustering" in md
    assert "| Branch documents | 2 |" in md
    assert "| Excluded (no diff content) | 2 |" in md
    assert "| Cut threshold | 0.9 |" in md
    assert "| Agreement with the score view (ARI) | 0.2059 |" in md
    assert "`path/payments`" in md and "`id/settle`" in md
    assert "Lexical content clustering" in md


def test_report_omits_the_content_section_when_absent():
    from src.analysis.clustering.report import render_markdown

    md = render_markdown(_tiny_report())
    assert "## Content clustering" not in md


def test_report_levels_are_counted_per_branch():
    from src.analysis.clustering.report import _level_summary

    counts = _level_summary(
        _tiny_report()["integration_targets"]["categorized_branches"]
    )
    assert counts["1 · heuristic"] == 1
    assert counts["4 · default"] == 1
    assert sum(counts.values()) == 2


# ----------------------------------------------------------------- resolvers


def test_resolver_finds_remote_only_ref(repo):
    from src.analysis.clustering._repo import resolve_rev

    _commit(repo, "feature/remote-only", {"src/app.py": "print('v3')\n"})
    _git(repo, "checkout", "-q", "main")
    _git(
        repo,
        "update-ref",
        "refs/remotes/origin/feature/remote-only",
        "feature/remote-only",
    )
    _git(repo, "branch", "-q", "-D", "feature/remote-only")

    assert (
        resolve_rev(str(repo), "feature/remote-only")
        == "refs/remotes/origin/feature/remote-only"
    )


def test_resolver_raises_for_unknown_ref(repo):
    from src.analysis.clustering._repo import resolve_rev

    with pytest.raises(ValueError, match="cannot resolve"):
        resolve_rev(str(repo), "no/such/branch")
