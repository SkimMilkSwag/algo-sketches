"""Edit distance (Levenshtein) — minimum edits to transform one string into another.

Classic DP over prefix lengths: dp[i][j] is the fewest operations turning
s[:i] into t[:j]. Each state considers three moves — delete a character from
s, insert a character into s, or substitute one — and keeps the cheapest. A
single rolling row keeps the space at O(min(m, n)) instead of the full table.

  - edit_distance(s, t): minimum single-character edits (insert/delete/
    substitute) that turn s into t
  - edit_distance_brute(s, t): top-down reference with memoization, same contract

Time O(m * n), space O(min(m, n)).
"""


def edit_distance(s: str, t: str) -> int:
    """Fewest insert/delete/substitute edits that transform s into t.

    dp[j] holds the current row's value for "s[:i] -> t[:j]"; the previous row
    is kept one variable behind (prev). A substitution costs 0 when the
    characters already match, otherwise 1 — so an exact prefix match propagates
    down the diagonal for free. The shorter string drives the inner loop's
    width, which is what keeps the working row at O(min(m, n)).
    """
    if len(s) < len(t):
        s, t = t, s  # make t the shorter string; distance is symmetric
    m, n = len(s), len(t)

    prev = list(range(n + 1))  # row i=0: s[:0] -> t[:j] is j insertions
    for i in range(1, m + 1):
        cur = [i]  # row i starts at "delete all of s[:i]"
        prev_diag = prev[0]
        for j in range(1, n + 1):
            cost = 0 if s[i - 1] == t[j - 1] else 1
            cur.append(min(prev[j] + 1,      # delete s[i-1]
                           cur[j - 1] + 1,   # insert t[j-1]
                           prev_diag + cost  # substitute (or free match)
                           ))
            prev_diag = prev[j]
        prev = cur
    return prev[n]


def edit_distance_brute(s: str, t: str) -> int:
    """Exhaustive reference: memoized recursion over (i, j) prefixes.

    Same contract as edit_distance. Exponential in the worst case without the
    memo dict, so tests keep strings short when using this one.
    """
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def solve(i: int, j: int) -> int:
        if i == len(s):
            return len(t) - j
        if j == len(t):
            return len(s) - i
        if s[i] == t[j]:
            return solve(i + 1, j + 1)
        return 1 + min(solve(i + 1, j),     # delete s[i]
                       solve(i, j + 1),     # insert t[j]
                       solve(i + 1, j + 1))  # substitute

    return solve(0, 0)
