"""Branch clustering pipeline (task 002).

Stage one analyzers produce one score vector per branch:

* :class:`~src.analysis.clustering.commit_history.CommitHistoryAnalyzer`
* :class:`~src.analysis.clustering.structure.CodebaseStructureAnalyzer`
* :class:`~src.analysis.clustering.diff_distance.DiffDistanceCalculator`

:class:`~src.analysis.clustering.clusterer.BranchClusterer` combines them with
the specified 35/35/30 weighting and performs HAC (Ward linkage).
:class:`~src.analysis.clustering.targets.IntegrationTargetAssigner` turns the
clusters into per-branch integration targets.

Stage two clusters on what the branches actually contain, not on their scores:

* :class:`~src.analysis.clustering.branch_git.BranchGitProfiler` keeps the raw
  git history of each branch (commits, authors, files, merge base)
* :func:`~src.analysis.clustering.content.cluster_content` clusters branches on
  the vocabulary of their diffs (paths, added identifiers, commit subjects)

``python -m src.analysis.clustering`` runs the whole pipeline against a real
repository and prints the clusters it actually forms.
"""

from .branch_git import BranchGitProfiler
from .clusterer import BranchClusterer
from .commit_history import CommitHistoryAnalyzer
from .content import build_documents, cluster_content, compare_clusterings
from .diff_distance import DiffDistanceCalculator
from .structure import CodebaseStructureAnalyzer
from .targets import IntegrationTargetAssigner

__all__ = [
    "BranchClusterer",
    "BranchGitProfiler",
    "CodebaseStructureAnalyzer",
    "CommitHistoryAnalyzer",
    "DiffDistanceCalculator",
    "IntegrationTargetAssigner",
    "build_documents",
    "cluster_content",
    "compare_clusterings",
]
