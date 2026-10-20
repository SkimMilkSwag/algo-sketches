"""Streaming Median — maintain the median of a growing stream.

Classic two-heap design: a max-heap ``low`` holds the smaller half of the
stream and a min-heap ``high`` holds the larger half, with the invariant
``len(low) >= len(high)`` and ``len(low) - len(high) <= 1``. The median is
then always available in O(1):

- odd total  -> top of ``low`` (the exact middle element),
- even total -> average of both tops.

Python only ships a min-heap, so ``low`` stores negated values to act as a
max-heap. Every inserted value lands in the right heap and at most one
rebalance is needed per operation, which keeps add O(log n) while the
median query stays O(1). A brute reference (sort + middle) pins behaviour
in the tests, including the tie-breaking on even-sized streams.
"""

import heapq

__all__ = ["MedianStream", "median_brute"]


class MedianStream:
    """Incremental median maintenance over a stream of numbers.

    ``add(x)`` is O(log n), ``median()`` is O(1). ``median()`` before any
    ``add`` raises ``ValueError`` (the empty stream has no median). Duplicates
    are allowed and count as separate observations, matching the brute
    reference's behaviour.
    """

    def __init__(self) -> None:
        self._low: list[float] = []   # max-heap via negation: smaller half
        self._high: list[float] = []  # min-heap: larger half

    def add(self, x: float) -> None:
        """Insert ``x`` into the stream and rebalance to O(log n)."""
        if self._low and x <= -self._low[0]:
            heapq.heappush(self._low, -x)
        else:
            heapq.heappush(self._high, x)
        # restore len(low) in {len(high), len(high) + 1}
        if len(self._low) > len(self._high) + 1:
            heapq.heappush(self._high, -heapq.heappop(self._low))
        elif len(self._high) > len(self._low):
            heapq.heappush(self._low, -heapq.heappop(self._high))

    def median(self) -> float:
        """Current median: exact middle (odd) or mean of two middles (even)."""
        if not self._low:
            raise ValueError("median() on an empty stream")
        if len(self._low) == len(self._high):
            return (-self._low[0] + self._high[0]) / 2.0
        return -self._low[0]

    def __len__(self) -> int:
        return len(self._low) + len(self._high)


def median_brute(values: list[float]) -> float | None:
    """Reference median: sort and take the middle (or mean of two middles)."""
    if not values:
        return None
    s = sorted(values)
    n = len(s)
    if n % 2:
        return s[n // 2]
    return (s[n // 2 - 1] + s[n // 2]) / 2.0
