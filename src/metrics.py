"""
Metrics computation helpers.

Provides small, testable functions to compute metrics from commit data.
"""

from collections import Counter
from typing import Iterable, Dict, List, Tuple, Any


def _extract_author(commit: Any) -> str:
    """
    Extract author name from different possible commit representations.
    Supports:
    - commit.author (str)
    - commit.author.name (object)
    - missing/None values
    """
    author = getattr(commit, "author", None)

    if author is None:
        return "<unknown>"

    # Case: author is already a string
    if isinstance(author, str):
        return author or "<unknown>"

    # Case: author is an object with `.name`
    name = getattr(author, "name", None)
    if name:
        return name

    return "<unknown>"


def compute_author_stats(commits: Iterable[object]) -> Dict[str, int]:
    """
    Count commits per author.

    Args:
        commits: Iterable of commit-like objects.

    Returns:
        Dict mapping author name to number of commits.
    """
    return dict(Counter(_extract_author(c) for c in commits))


def sort_author_stats(stats: Dict[str, int]) -> List[Tuple[str, int]]:
    """
    Sort authors by number of commits (descending).

    Args:
        stats: Dict of {author: commit_count}

    Returns:
        List of tuples sorted by contribution.
    """
    return sorted(stats.items(), key=lambda x: x[1], reverse=True)