"""Word Break — can `s` be segmented into dictionary words, and how many ways?

Two answers for one DP table:

  - can_word_break(s, words): boolean.  ``dp[i]`` is True when the prefix
    ``s[:i]`` segments cleanly.  The base case ``dp[0] = True`` (the empty
    prefix) means the recurrence is purely "a longer prefix is breakable iff
    some word ends at its last character and the remainder was already
    breakable".  O(n * m) per target where n = len(s), m = max word length.

  - count_word_breaks(s, words): number of distinct segmentations (as a list
    of word strings).  ``count[i]`` is the sum of ``count[j]`` over every
    word that starts at j and ends exactly at i; the same scan direction as
    the boolean pass, so both answers come out of one helper.  Counts grow
    exponentially in n (e.g. "aaaa...a" with {"a", "aa", ...} is a Fibonacci
    count), so callers wanting bounded arithmetic can reduce on their side —
    exact integers are what this module returns.

Duplicate dictionary entries are treated as synonyms of the same token
(deduplicated before use), and empty strings are ignored: an empty word in
the dict would otherwise create spurious zero-length segments.
"""

__all__ = ["can_word_break", "count_word_breaks"]


def _normalize(words) -> set:
    """Deduplicate and drop empty tokens so the DP sees a clean word set."""
    return {w for w in words if w}


def can_word_break(s: str, words) -> bool:
    """Return True when ``s`` is a concatenation of one or more dict words.

    An empty ``s`` breaks trivially (zero segments); a non-empty ``s`` with
    an empty (or all-empty) word list cannot break.
    """
    if s == "":
        return True
    vocab = _normalize(words)
    if not vocab:
        return False

    n = len(s)
    max_word = max(len(w) for w in vocab)
    dp = [False] * (n + 1)
    dp[0] = True
    for i in range(1, n + 1):
        # a word ending at position i starts at most `max_word` chars earlier
        for j in range(max(0, i - max_word), i):
            if not dp[j]:
                continue
            if s[j:i] in vocab:
                dp[i] = True
                break  # one witness is enough for the boolean pass
    return dp[n]


def count_word_breaks(s: str, words) -> int:
    """Number of distinct ways to split ``s`` into dict-word segments.

    "Distinct" means the sequence of tokens differs; two identical tokens in
    the dictionary count once (see :func:`_normalize`).  Returns 0 when no
    segmentation exists — which is also what you get for a non-empty ``s``
    with no usable words, and 1 for the empty string (the single empty
    segmentation).
    """
    if s == "":
        return 1
    vocab = _normalize(words)
    if not vocab:
        return 0

    n = len(s)
    max_word = max(len(w) for w in vocab)
    count = [0] * (n + 1)
    count[0] = 1
    for i in range(1, n + 1):
        total = 0
        for j in range(max(0, i - max_word), i):
            if count[j] and s[j:i] in vocab:
                total += count[j]
        count[i] = total
    return count[n]
