"""Run the task-002 clustering pipeline against a real repository.

    python -m src.analysis.clustering --repo PATH [--limit N] [--jobs J] [--out FILE]

Enumerates every ``refs/remotes/origin/*`` branch (excluding ``origin/HEAD`` and
the integration baseline), runs the three stage-one analyzers over it,
clusters the survivors and assigns integration targets. Branches that cannot be
analyzed are counted and named in the report rather than silently dropped.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from typing import Any

from .branch_git import BranchGitProfiler
from .clusterer import BranchClusterer
from .commit_history import CommitHistoryAnalyzer
from .content import build_documents, cluster_content, compare_clusterings
from .diff_distance import DiffDistanceCalculator
from .structure import CodebaseStructureAnalyzer
from .targets import IntegrationTargetAssigner

EXCLUDED_SUFFIXES = {"HEAD", "main"}


def list_branches(repo_path: str, remote: str = "origin") -> list[str]:
    """Return short branch names under ``refs/remotes/<remote>``."""
    result = subprocess.run(
        [
            "git",
            "-C",
            repo_path,
            "for-each-ref",
            "--format=%(refname:short)",
            f"refs/remotes/{remote}",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit(f"cannot list refs in {repo_path}: {result.stderr.strip()}")

    names = []
    prefix = f"{remote}/"
    for line in result.stdout.splitlines():
        ref = line.strip()
        if not ref.startswith(prefix):
            continue
        short = ref[len(prefix) :]
        if short in EXCLUDED_SUFFIXES:
            continue
        names.append(short)
    return sorted(names)


def analyze_branch(
    repo_path: str, branch: str, main_ref: str = "main"
) -> tuple[str, dict[str, Any]]:
    """Run all three analyzers for one branch; raise on any failure."""
    history = CommitHistoryAnalyzer(repo_path, main_branch=main_ref).analyze_sync(
        branch
    )
    structure = CodebaseStructureAnalyzer(repo_path, main_branch=main_ref).analyze(
        branch
    )
    diff = DiffDistanceCalculator(repo_path, main_branch=main_ref).analyze(branch)
    return branch, {
        "commit_history": history,
        "codebase_structure": structure,
        "diff_distance": diff,
    }


def _profile_and_tokenize(
    repo_path: str, branch: str, main_ref: str
) -> tuple[str, dict[str, Any], dict[str, Any]]:
    """Full git profile plus the multi-level content document for one branch."""
    profile = BranchGitProfiler(repo_path, main_branch=main_ref).profile(branch)
    document = build_documents(profile, repo_path)
    summary = {
        "commit_count": profile["commit_count"],
        "authors": profile["authors"],
        "first_commit": profile["first_commit"],
        "last_commit": profile["last_commit"],
        "merge_base": profile["merge_base"],
        "top_directories": profile["top_directories"],
        "total_added": profile["total_added"],
        "total_deleted": profile["total_deleted"],
    }
    return branch, summary, document


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, help="path to a git repository")
    parser.add_argument("--remote", default="origin")
    parser.add_argument(
        "--main", default="main", help="ref to measure branches against (default: main)"
    )
    parser.add_argument(
        "--limit", type=int, default=0, help="analyze at most N branches"
    )
    parser.add_argument("--jobs", type=int, default=16)
    parser.add_argument("--threshold", type=float, default=0.5)
    parser.add_argument(
        "--no-content",
        action="store_true",
        help="skip the content stage (git profile + diff-vocabulary clustering)",
    )
    parser.add_argument("--out", default="", help="write the full JSON report here")
    args = parser.parse_args(argv)

    branches = list_branches(args.repo, args.remote)
    if args.limit:
        branches = branches[: args.limit]
    if not branches:
        print(f"no branches found under refs/remotes/{args.remote}", file=sys.stderr)
        return 2

    print(
        f"analyzing {len(branches)} branches with {args.jobs} workers...",
        file=sys.stderr,
    )

    outputs: dict[str, dict[str, Any]] = {}
    failures: list[dict[str, str]] = []
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures = {
            pool.submit(analyze_branch, args.repo, b, args.main): b for b in branches
        }
        for done, future in enumerate(futures, start=1):
            branch = futures[future]
            try:
                name, blocks = future.result()
                outputs[name] = blocks
            except Exception as exc:  # noqa: BLE001 - report all failures, never hide them
                failures.append({"branch": branch, "error": str(exc)})
            if done % 100 == 0:
                print(f"  {done}/{len(branches)}", file=sys.stderr)

    print(f"analyzed={len(outputs)} failed={len(failures)}", file=sys.stderr)
    if not outputs:
        print("no branch produced analyzer output", file=sys.stderr)
        return 1

    clustered = BranchClusterer(args.repo, threshold=args.threshold).cluster(outputs)
    assigned = IntegrationTargetAssigner(args.repo, main_branch=args.main).assign(
        clustered, outputs
    )

    content: dict[str, Any] = {}
    git_profiles: dict[str, dict[str, Any]] = {}
    if not args.no_content:
        print(
            f"\nprofiling branch git history and diff content "
            f"for {len(outputs)} branches...",
            file=sys.stderr,
        )
        documents: dict[str, dict[str, Any]] = {}
        with ThreadPoolExecutor(max_workers=args.jobs) as pool:
            futures = {
                pool.submit(_profile_and_tokenize, args.repo, branch, args.main): branch
                for branch in outputs
            }
            for done, future in enumerate(futures, start=1):
                branch = futures[future]
                try:
                    name, summary, document = future.result()
                    git_profiles[name] = summary
                    documents[name] = document
                except Exception as exc:  # noqa: BLE001 - content stage is additive
                    failures.append({"branch": branch, "error": f"content: {exc}"})
                if done % 200 == 0:
                    print(f"  profiled {done}/{len(futures)}", file=sys.stderr)

        content = cluster_content(documents)
        content["agreement_with_metric_clustering"] = compare_clusterings(
            clustered["branch_assignments"], content["branch_assignments"]
        )
        cq = content["quality_metrics"]
        print(
            f"content: documents={content['document_count']} "
            f"clusters={cq['total_clusters']} silhouette={cq['silhouette_avg']:.4f} "
            f"cut={cq['threshold']} vocab={cq['vocabulary_size']} "
            f"ari={content['agreement_with_metric_clustering']['adjusted_rand_index']}",
            file=sys.stderr,
        )
        print("\ncontent clusters (largest first):")
        for cluster in content["clusters"][:15]:
            terms = ", ".join(cluster["signature_terms"][:6])
            print(
                f"  c{cluster['cluster_id']:>3}  size={cluster['size']:<4} "
                f"cohesion={cluster['cohesion']:.3f}  {terms}"
            )

    order = sorted(clustered["clusters"], key=lambda c: (-c["size"], c["cluster_id"]))
    print("\nclusters:")
    for cluster in order:
        cid = cluster["cluster_id"]
        names = cluster["branches"]
        sample = ", ".join(names[:5]) + (" ..." if len(names) > 5 else "")
        print(
            f"  cluster {cid:>3}  size={cluster['size']:<4} "
            f"cohesion={cluster['cohesion']:.3f}  "
            f"combined={cluster['cluster_center']['combined_score']:.3f}  {sample}"
        )

    q = clustered["quality_metrics"]
    print(
        f"\nquality: clusters={q['total_clusters']} "
        f"silhouette={q['silhouette_avg']:.4f} "
        f"davies_bouldin={q['davies_bouldin_index']:.4f} "
        f"calinski_harabasz={q['calinski_harabasz_index']:.2f}"
    )

    print("\nintegration targets:")
    for target, summary in assigned["integration_target_summary"].items():
        if summary["branch_count"] or target == "main":
            print(
                f"  {target:<20} branches={summary['branch_count']:<4} "
                f"avg_confidence={summary['total_confidence']:.3f}  "
                f"key_tags={', '.join(summary['key_tags'])}"
            )

    report = {
        "pipeline": "task-002-clustering",
        "repo": args.repo,
        "remote": args.remote,
        "main_ref": args.main,
        "threshold": args.threshold,
        "branches_considered": len(branches),
        "branches_analyzed": len(outputs),
        "branches_failed": failures,
        "clustering": clustered,
        "integration_targets": assigned,
        "content_clustering": content,
        "branch_git": git_profiles,
    }

    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump(report, fh, indent=2)
        print(f"\nreport written to {args.out}", file=sys.stderr)
    else:
        # Keep stdout machine-readable only when no file was requested.
        print(
            json.dumps(
                report["integration_targets"]["integration_target_summary"], indent=2
            )
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
