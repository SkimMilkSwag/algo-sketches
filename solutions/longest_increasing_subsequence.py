"""Longest increasing subsequence — longest strictly-increasing subsequence.

Patience sorting: sweep left to right keeping piles of cards; each new element
goes on the leftmost pile whose top is >= it (bisect_left), or starts a new
pile if none qualifies. The pile count at the end equals the LIS length, and
the number of piles an element lands on pins its position in some LIS — which
is how reconstruction works (follow the pile-of-first-occurrence back).

  - longest_increasing_subsequence(a): length of the longest strictly
    increasing subsequence of `a`
  - longest_increasing_subsequence_with_reconstruction(a): the length plus
    one actual subsequence achieving it (leftmost-biased, deterministic)

Time O(n log n), space O(n).
"""
from bisect import bisect_left


def longest_increasing_subsequence(a: list[int]) -> int:
    """Length of the longest strictly increasing subsequence.

    piles[i] holds the smallest tail value of any increasing subsequence of
    length i + 1 seen so far. Because tails are kept minimal, the array stays
    sorted, which is what lets each placement binary-search in O(log n).
    """
    piles: list[int] = []
    for x in a:
        i = bisect_left(piles, x)
        if i == len(piles):
            piles.append(x)
        else:
            piles[i] = x
    return len(piles)


def longest_increasing_subsequence_with_reconstruction(a: list[int]):
    """Return (length, subsequence) for the longest strictly increasing subsequence.

    Same sweep as longest_increasing_subsequence, but each element also records
    the length of the subsequence that placed it (the pile number it landed on
    — a replacement keeps the same pile, so the value is unchanged). Replaying
    that map in reverse: scan positions from last to first keeping the longest
    recorded length still reachable, and append an element only when its
    recorded length equals one less than the length we are filling. This yields
    a valid LIS; ties break toward the earliest occurrence.

    Time O(n log n), space O(n).
    """
    if not a:
        return 0, []
    piles: list[int] = []          # minimal tail per pile (kept sorted)
    length_at: list[int] = []      # length_at[i]: subsequence length x at index i lands on
    for x in a:
        i = bisect_left(piles, x)
        if i == len(piles):
            piles.append(x)
        else:
            piles[i] = x
        length_at.append(i + 1)

    best = max(length_at)
    sub: list[int] = []
    need = best
    for idx in range(len(a) - 1, -1, -1):
        if length_at[idx] == need and (not sub or a[idx] < sub[-1]):
            sub.append(a[idx])
            need -= 1
    sub.reverse()
    return best, sub
