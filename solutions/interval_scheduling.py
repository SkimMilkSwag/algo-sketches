"""Interval Scheduling — maximum number of mutually compatible intervals.

Given a set of tasks each occupying [start, end), find the largest subset of
tasks that never overlap (a task ending at time t is compatible with one
starting at t — "non-overlapping" in the half-open sense). The greedy answer:
sort by END time and repeatedly take the earliest-finishing task that starts
at or after the last chosen one's end.

Exchange argument (why this is optimal): consider the earliest-finishing
task among ALL tasks, call it t1. Any optimal schedule's first task finishes
no earlier than t1 (t1 is the minimum), so swapping the optimal schedule's
first task for t1 leaves every later task compatible — the swap can't break
the schedule and preserves its size. Induct on the remaining tasks: the same
argument applies to whatever remains after each pick, so a greedy that always
takes the earliest finish among the still-available tasks produces a maximum
cardinality schedule.

  - interval_scheduling(intervals): max number of non-overlapping intervals
  - interval_scheduling_brute(intervals): exhaustive subset reference

Time O(n log n) (sort dominates), space O(1) beyond the sorted copy.
"""


def interval_scheduling(intervals: list[tuple[int, int]]) -> int:
    """Maximum size of a non-overlapping subset of `intervals` (greedy).

    Half-open convention: [s, e) does not overlap [e, f), so touching
    endpoints are compatible. The input is not mutated; intervals are sorted
    by end (ties broken by start for determinism) before the sweep.
    """
    count = 0
    last_end = None  # end time of the last chosen interval
    for start, stop in sorted(intervals, key=lambda iv: (iv[1], iv[0])):
        if last_end is None or start >= last_end:
            count += 1
            last_end = stop
    return count


def interval_scheduling_brute(intervals: list[tuple[int, int]]) -> int:
    """Exhaustive reference: check every subset, keep the largest compatible one.

    Same contract as :func:`interval_scheduling`. 2**n subsets, so tests keep
    interval counts small when using this one.
    """
    n = len(intervals)
    best = 0
    for mask in range(1 << n):
        chosen: list[tuple[int, int]] = []
        ok = True
        for i in range(n):
            if mask >> i & 1:
                s, e = intervals[i]
                # must be compatible with every already-chosen interval
                if any(not (e <= cs or ce <= s) for cs, ce in chosen):
                    ok = False
                    break
                chosen.append((s, e))
        if ok and len(chosen) > best:
            best = len(chosen)
    return best
