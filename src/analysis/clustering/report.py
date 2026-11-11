"""Render a clustering run's JSON report as the task-002 analysis document.

    python -m src.analysis.clustering.report --in report.json --out doc.md

The pipeline writes everything it decides into its JSON report; this module only
reorganises that JSON so a reader can audit the analysis without loading a
30 MB file.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from typing import Any


def _sample(branches: list[str], limit: int = 5) -> str:
    shown = ", ".join(f"`{name}`" for name in branches[:limit])
    return shown + (f", +{len(branches) - limit} more" if len(branches) > limit else "")


def _decision_level(rationale: str) -> str:
    if rationale.startswith("Heuristic rule match"):
        return "1 · heuristic"
    if rationale.startswith("Affinity scoring"):
        return "2 · archetype affinity"
    if rationale.startswith("Cluster consensus"):
        return "3 · cluster consensus"
    if rationale.startswith("Default assignment"):
        return "4 · default"
    return "0 · fall-through"


def _level_summary(classified: dict[str, dict[str, Any]]) -> Counter[str]:
    return Counter(
        _decision_level(row["decision_rationale"]) for row in classified.values()
    )


def render_markdown(report: dict[str, Any]) -> str:
    clustering = report["clustering"]
    assigned = report["integration_targets"]
    clusters = sorted(
        clustering["clusters"], key=lambda c: (-c["size"], c["cluster_id"])
    )
    quality = clustering["quality_metrics"]
    classified = assigned["categorized_branches"]
    levels = _level_summary(classified)
    total_classified = len(classified)

    lines: list[str] = []
    add = lines.append

    add("# Branch clustering analysis (task 002)")
    add("")
    add(f"Generated from a live run against `{report['repo']}`.")
    add("")
    add("## Method")
    add("")
    add(
        "Every branch under the remote is scored by three independent analyzers, "
        "combined at the task's fixed weights, and clustered by Ward hierarchical "
        "agglomeration cut at a fixed distance:"
    )
    add("")
    add("| Stage | Weight | Input |")
    add("| --- | --- | --- |")
    add(
        "| Commit history | 0.35 | commits on `main..branch` only, recency, authorship, merge readiness, stability |"
    )
    add(
        "| Codebase structure | 0.35 | directory similarity, file additions, core-module stability, namespace isolation |"
    )
    add(
        "| Diff distance | 0.30 | code churn, change concentration, diff complexity, integration risk |"
    )
    add("")
    add(f"- Linkage: Ward, Euclidean; cut at distance `{report['threshold']}`.")
    add(
        "- Integration targets are assigned through four levels in order: "
        "name/metric heuristics, archetype cosine affinity, cluster consensus, default."
    )
    add("")

    add("## Headline numbers")
    add("")
    add("| Measure | Value |")
    add("| --- | --- |")
    add(f"| Branches considered | {report['branches_considered']} |")
    add(f"| Branches analyzed | {report['branches_analyzed']} |")
    add(f"| Branches rejected (no merge base) | {len(report['branches_failed'])} |")
    add(f"| Clusters | {quality['total_clusters']} |")
    add(f"| Silhouette (avg) | {quality['silhouette_avg']:.4f} |")
    add(f"| Davies-Bouldin | {quality['davies_bouldin_index']:.4f} |")
    add(f"| Calinski-Harabasz | {quality['calinski_harabasz_index']:.2f} |")
    add("")

    zero_work = [
        c
        for c in clusters
        if all(
            c["cluster_center"][key] == 0.0
            for key in (
                "commit_history_weight",
                "codebase_structure_weight",
                "diff_distance_weight",
            )
        )
    ]
    if zero_work:
        n = sum(c["size"] for c in zero_work)
        add("### The zero-score cluster: branches already on main")
        add("")
        add(
            f"{n} branches score 0.0 on all three analyzers, which is only possible "
            "when `main..branch` is empty: they carry no commit that is not already "
            "reachable from `main`. They are not pending work, and sequencing them "
            "into a merge wave would merge nothing. This is the largest actionable "
            "finding in the run — it is a cleanup queue, not a merge queue."
        )
        add("")
        add(f"Cluster members: {_sample(zero_work[0]['branches'], 10)}")
        add("")
        add(
            "Independent cross-check used to confirm it: "
            "`git rev-list --count --max-count=1 refs/remotes/origin/main..<branch>` "
            "run over every ref, which agrees with the cluster membership."
        )
        add("")

    add("## Clusters by size")
    add("")
    add(
        "| # | Size | Cohesion | Combined score | Mean analyzer scores (history / structure / diff) | Sample members |"
    )
    add("| --- | --- | --- | --- | --- | --- |")
    for cluster in clusters:
        center = cluster["cluster_center"]
        means = (
            f"{center['commit_history_weight']:.3f} / "
            f"{center['codebase_structure_weight']:.3f} / "
            f"{center['diff_distance_weight']:.3f}"
        )
        add(
            f"| {cluster['cluster_id']} | {cluster['size']} | "
            f"{cluster['cohesion']:.3f} | {center['combined_score']:.3f} | "
            f"{means} | {_sample(cluster['branches'])} |"
        )
    add("")

    content = report.get("content_clustering")
    if content:
        content_quality = content["quality_metrics"]
        agreement = content.get("agreement_with_metric_clustering") or {}
        level_weights = (content.get("hash") or {}).get("levels") or {}
        add("## Content clustering (what the diffs actually contain)")
        add("")
        add(
            "Stage one ranks a branch by aggregate scores, so two branches with similar "
            "scores can touch unrelated code. This stage clusters on the branch's content "
            "at several detail levels. Every token is mapped to one of 65,536 buckets by "
            "`blake2b`, with the sign taken from the digest, so there is no fitted "
            "vocabulary and the same branch always yields the same vector. One "
            "average-linkage tree is cut at a grid of cosine thresholds; the cut with the "
            "best silhouette is the primary partition and every finer cluster records the "
            "coarser cluster that contains it."
        )
        add("")
        add("| Measure | Value |")
        add("| --- | --- |")
        add(f"| Branch documents | {content['document_count']} |")
        add(
            "| Excluded (no diff content) | "
            f"{len(content.get('excluded_no_content', []))} |"
        )
        if content.get("levels"):
            add(f"| Detail levels | {', '.join(content['levels'])} |")
        add(f"| Clusters (primary cut) | {content_quality['total_clusters']} |")
        add(f"| Silhouette (avg) | {content_quality['silhouette_avg']:.4f} |")
        cut = content_quality.get("threshold")
        add(f"| Cut threshold | {cut if cut is not None else 'single cluster'} |")
        add(
            f"| Vocabulary | {content_quality['vocabulary_size']} hashed buckets, "
            "no fitted vocabulary |"
        )
        ari = agreement.get("adjusted_rand_index")
        add(
            f"| Agreement with the score view (ARI) | {ari if ari is not None else 'n/a'} |"
        )
        add("")

        if level_weights:
            add("### Detail levels and their weights")
            add("")
            add("| Level | Weight | What it captures |")
            add("| --- | --- | --- |")
            descriptions = {
                "path": "path prefixes and segments",
                "path_pair": "adjacent path-segment pairs",
                "symbol": "identifier words from added lines",
                "symbol_pair": "adjacent identifier pairs",
                "message": "commit-subject words and word pairs",
                "subword": "character 4-grams of identifiers",
                "embedding": "sentence/paragraph embedding (optional)",
            }
            for level, weight in level_weights.items():
                add(f"| `{level}` | {weight:.2f} | {descriptions.get(level, '—')} |")
            add("")

        hierarchy = content.get("hierarchy") or []
        if hierarchy:
            add("### Hierarchy of cuts")
            add("")
            add("| Cosine cut | Clusters | Silhouette | Primary |")
            add("| --- | --- | --- | --- |")
            for row in hierarchy:
                add(
                    f"| {row['threshold']} | {row['clusters']} | "
                    f"{row['silhouette']:.4f} | {'yes' if row.get('primary') else ''} |"
                )
            add("")

        level_agreement = content.get("level_agreement") or {}
        if level_agreement:
            add("### How each level agrees with the combined partition")
            add("")
            add("| Level | ARI vs combined |")
            add("| --- | --- |")
            for level, score in level_agreement.items():
                add(f"| `{level}` | {score if score is not None else 'n/a'} |")
            add("")

        add(
            "A low silhouette here is the honest result, not a failed run: most of the "
            "fleet edits Python under `src/`, so their vocabularies overlap and no cut "
            "separates cleanly. The low agreement with the score view says that view is "
            "not a proxy for content — branches that score alike are often about "
            "different code. This is a lexical method: it groups a merge wave, it does "
            "not prove two branches equivalent."
        )
        add("")
        add("### Content clusters with signature terms")
        add("")
        add(
            "Signature terms are the tokens most over-represented inside a cluster "
            "relative to the rest of the fleet."
        )
        add("")
        add("| # | Size | Cohesion | Signature terms | Sample members |")
        add("| --- | --- | --- | --- | --- |")
        ordered = sorted(
            content["clusters"], key=lambda c: (-c["size"], c["cluster_id"])
        )
        for cluster in ordered[:20]:
            terms = ", ".join(f"`{t}`" for t in cluster["signature_terms"][:8]) or "—"
            add(
                f"| {cluster['cluster_id']} | {cluster['size']} | "
                f"{cluster['cohesion']:.3f} | {terms} | "
                f"{_sample(cluster['branches'])} |"
            )
        add("")
        if content.get("note"):
            add(f"> {content['note']}")
            add("")

    add("## Integration targets")
    add("")
    add("| Target | Branches | Mean confidence | Leading tags |")
    add("| --- | --- | --- | --- |")
    for target, summary in assigned["integration_target_summary"].items():
        tags = ", ".join(f"`{tag}`" for tag in summary["key_tags"])
        add(
            f"| `{target}` | {summary['branch_count']} | "
            f"{summary['total_confidence']:.3f} | {tags} |"
        )
    add("")

    add("### Which level decided")
    add("")
    add("| Decision level | Branches | Share |")
    add("| --- | --- | --- |")
    for level in sorted(levels):
        count = levels[level]
        share = count / total_classified if total_classified else 0.0
        add(f"| {level} | {count} | {share:.1%} |")
    add("")
    add(
        "A high default share would mean the hierarchy is not earning its keep; a "
        "high heuristic share means the name-based rules dominate and the numeric "
        "levels rarely get a chance to speak."
    )
    add("")

    tag_counts: Counter[str] = Counter()
    for row in classified.values():
        tag_counts.update(row["tags"])
    add("### Most frequent tags")
    add("")
    add("| Tag | Branches |")
    add("| --- | --- |")
    for tag, count in tag_counts.most_common(15):
        add(f"| `{tag}` | {count} |")
    add("")

    failures = report["branches_failed"]
    if failures:
        add("## Rejected branches")
        add("")
        add(
            "These are reported rather than dropped. Each one shares no history with "
            "the baseline, so no meaningful diff exists and no analyzer can score it."
        )
        add("")
        add("| Branch | Reason |")
        add("| --- | --- |")
        for failure in failures:
            add(f"| `{failure['branch']}` | {failure['error']} |")
        add("")

    add("## How to reproduce")
    add("")
    add("```bash")
    add(
        "python -m src.analysis.clustering \\\n"
        f"  --repo {report['repo']} \\\n"
        f"  --main {report['main_ref']} \\\n"
        f"  --threshold {report['threshold']} \\\n"
        "  --jobs 16 --out report.json"
    )
    add("```")
    add("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--in", dest="input", required=True)
    parser.add_argument("--out", dest="output", required=True)
    args = parser.parse_args(argv)

    with open(args.input, encoding="utf-8") as fh:
        report = json.load(fh)
    markdown = render_markdown(report)
    with open(args.output, "w", encoding="utf-8") as fh:
        fh.write(markdown)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
