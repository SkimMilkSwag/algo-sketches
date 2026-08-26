"""Longest substring without repeating characters — LeetCode 3.

O(n) sliding window with a dict tracking the last index of each character.
"""


def length_of_longest(s: str) -> int:
    last = {}
    left = best = 0
    for right, ch in enumerate(s):
        if ch in last and last[ch] >= left:
            left = last[ch] + 1
        last[ch] = right
        best = max(best, right - left + 1)
    return best
