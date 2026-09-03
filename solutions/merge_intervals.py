"""Merge Intervals — LeetCode 56.

O(n log n) sort + sweep: sort by start, then walk the list merging any
interval whose start falls inside (or at the end of) the running one.
Nested intervals ([1,10] swallowing [2,3]) merge for free because they
start inside the running interval; disjoint intervals pass through.
"""


def merge_intervals(intervals: list[tuple[int, int]]) -> list[list[int]]:
    """Return a new list of non-overlapping merged intervals (as lists).

    The input is not mutated. Intervals are sorted by start before merging,
    so output order follows the sweep (by start, then by end).
    """
    if not intervals:
        return []
    ordered = sorted(intervals)  # by start, then by end (tuples compare lexicographically)
    merged = [list(ordered[0])]  # copy; don't alias the caller's tuple
    for iv in ordered[1:]:
        start, stop = iv
        if start <= merged[-1][1]:  # overlaps or is nested inside the running interval
            merged[-1][1] = max(merged[-1][1], stop)
        else:
            merged.append([start, stop])
    return merged


def merge_intervals_brute(intervals: list[tuple[int, int]]) -> list[list[int]]:
    """Reference implementation (repeatedly merge overlapping pairs) for tests.

    O(n^3) worst case; only used on small random inputs to pin behaviour.
    """
    out = [list(iv) for iv in intervals]
    changed = True
    while changed:
        changed = False
        for i, a in enumerate(out):
            for j, b in enumerate(out):
                if i < j and not (a[1] < b[0] or b[1] < a[0]):
                    out[i] = [min(a[0], b[0]), max(a[1], b[1])]
                    out.pop(j)
                    changed = True
                    break
            if changed:
                break
    return sorted(out)
