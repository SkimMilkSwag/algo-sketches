"""Longest Common Subsequence (LCS) — classic DP (LeetCode 1143 style).

A common subsequence need not be contiguous: characters may be deleted from
either input, but the relative order must survive.  The standard DP fills a
table where ``dp[i][j]`` is the length of the longest common subsequence of
the prefixes ``a[:i]`` / ``b[:j]``.  Equal characters extend the previous
diagonal by one; otherwise the best of skipping either character wins:

    dp[i][j] = dp[i-1][j-1] + 1          if a[i-1] == b[j-1]
             = max(dp[i-1][j], dp[i][j-1]) otherwise

The full table is kept so the reconstruction walk — from (m, n) back to the
origin, preferring the diagonal on equal characters and taking whichever side
has the larger value on a mismatch — can recover an actual subsequence in
O(m+n).  A brute reference (exhaustive deletion subsets via itertools
combinations over the shorter string's indices) lets tests cross-check small
random inputs.

O(m*n) time; O(m*n) space for the table plus the reconstruction walk.  The
table itself could be row-rolled for length-only queries, but then the
reconstruction would need Hirschberg's divide-and-conquer to stay
space-efficient — not worth it here.
"""

from itertools import combinations

__all__ = [
    "longest_common_subsequence",
    "longest_common_subsequence_length",
    "longest_common_subsequence_brute",
]


def longest_common_subsequence(a: str, b: str) -> str:
    """Return one longest common subsequence of `a` and `b`.

    Ties (several distinct subsequences of the same maximal length) are broken
    deterministically by the reconstruction walk: on a mismatch it takes the
    side with the larger table value, preferring the row skip over the column
    skip when they tie — which yields an earliest-occurrence-biased answer.
    Returns ``""`` when either input is empty.
    """
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        ai = a[i - 1]
        prev_row = dp[i - 1]
        row = dp[i]
        for j in range(1, n + 1):
            if ai == b[j - 1]:
                row[j] = prev_row[j - 1] + 1
            else:
                row[j] = max(prev_row[j], row[j - 1])
    # reconstruct from (m, n) back to the origin
    out: list[str] = []
    i, j = m, n
    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            out.append(a[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return "".join(reversed(out))


def longest_common_subsequence_length(a: str, b: str) -> int:
    """Length of the LCS of `a` and `b` (same DP, no reconstruction)."""
    m, n = len(a), len(b)
    prev = [0] * (n + 1)
    for i in range(1, m + 1):
        cur = [0] * (n + 1)
        ai = a[i - 1]
        for j in range(1, n + 1):
            if ai == b[j - 1]:
                cur[j] = prev[j - 1] + 1
            else:
                cur[j] = max(prev[j], cur[j - 1])
        prev = cur
    return prev[n]


def longest_common_subsequence_brute(a: str, b: str) -> str:
    """Reference implementation by exhaustive index subsets.

    Enumerates every subsequence of the shorter string (every combination of
    indices, in increasing order) and keeps the longest one that is also a
    subsequence of the other input.  O(2^min(m,n) * max(m,n)) — fine for test
    sizes, useless for real ones.  Scans index sets in lexicographic order,
    so the first maximal candidate found wins any tie — matching the fast
    path's deterministic preference on the cases the tests use.
    """
    if len(a) < len(b):
        a, b = b, a
    # `a` is now the shorter string; enumerate its subsequences longest-first
    best = ""
    for size in range(len(a), -1, -1):
        found: list[str] = []
        for idxs in combinations(range(len(a)), size):
            cand = "".join(a[k] for k in idxs)
            if _is_subsequence(cand, b):
                found.append(cand)
        if found:
            best = found[0]
            break
    return best


def _is_subsequence(needle: str, haystack: str) -> bool:
    """True when `needle` is a (not necessarily contiguous) subsequence of
    `haystack` — the standard two-pointer scan."""
    i = 0
    for ch in haystack:
        if i < len(needle) and ch == needle[i]:
            i += 1
    return i == len(needle)
