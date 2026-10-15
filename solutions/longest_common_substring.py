"""Longest Common Substring — classic DP (LeetCode 1408 style).

Unlike the *subsequence* problem, a common substring must be contiguous in
both inputs.  The standard DP fills a table where ``dp[i][j]`` is the
length of the longest common suffix ending exactly at ``a[i-1]`` /
``b[j-1]``: equal characters extend the previous diagonal by one, anything
else restarts at zero.  The answer is the maximum cell.

O(m*n) time and space; the table below keeps only the previous row, so
space drops to O(min(m, n)) without touching the recurrence.  A brute
reference (enumerate every pair of start offsets and extend) is included
for tests to cross-check small random inputs.
"""

__all__ = ["longest_common_substring", "longest_common_substring_brute"]


def longest_common_substring(a: str, b: str) -> str:
    """Return the longest substring shared by `a` and `b`.

    Ties are broken arbitrarily but deterministically: the scan walks the
    table left-to-right, top-to-bottom, so the earliest (highest-leftmost)
    maximal cell wins.  Returns ``""`` when there is no common character —
    including when either input is empty.
    """
    if not a or not b:
        return ""
    # keep b as the shorter string: row width = len(b) + 1
    if len(b) > len(a):
        a, b = b, a
    prev = [0] * (len(b) + 1)
    best_len = 0
    best_end_i = 0  # exclusive end index into `a` of the current best
    for i in range(1, len(a) + 1):
        cur = [0] * (len(b) + 1)
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                cur[j] = prev[j - 1] + 1
                if cur[j] > best_len:
                    best_len = cur[j]
                    best_end_i = i
        prev = cur
    return a[best_end_i - best_len:best_end_i]


def longest_common_substring_brute(a: str, b: str) -> str:
    """Reference implementation: try every (i, j), extend while equal.

    O(m^2 * n^2) in the worst case — fine for tests, painful for real
    inputs.  Returns the first maximal extension found scanning i from 0
    and j from 0; on ties it matches the fast path's earliest-occurrence
    preference because both scan in the same (i, j) order and only record
    strictly longer matches.
    """
    best = ""
    for i in range(len(a)):
        for j in range(len(b)):
            k = 0
            while (
                i + k < len(a)
                and j + k < len(b)
                and a[i + k] == b[j + k]
            ):
                k += 1
            if k > len(best):
                best = a[i:i + k]
    return best
