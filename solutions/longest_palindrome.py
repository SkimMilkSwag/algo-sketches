"""Longest Palindromic Substring — LeetCode 5.

O(n^2) center expansion: grow a palindrome outward from every center
(odd length from a single char, even length from a gap between two chars).
Worst case is O(n^2); average input is much cheaper because most centers
stop expanding after a few steps.
"""


def longest_palindromic_substring(s: str) -> str:
    """Return the longest palindromic substring of s (any one if tied)."""
    n = len(s)
    best_start, best_len = 0, -1

    def expand(left: int, right: int) -> tuple[int, int]:
        """Grow [left, right] while it is a palindrome; return its bounds."""
        while left >= 0 and right < n and s[left] == s[right]:
            left -= 1
            right += 1
        return left + 1, right - 1

    for center in range(n):
        # odd-length palindromes centered at `center`
        start, end = expand(center, center)
        if end - start + 1 > best_len:
            best_start, best_len = start, end - start + 1
        # even-length palindromes centered between `center` and `center+1`
        if center + 1 < n:
            start, end = expand(center, center + 1)
            if end - start + 1 > best_len:
                best_start, best_len = start, end - start + 1

    return s[best_start : best_start + best_len]


def is_palindrome(s: str) -> bool:
    """Brute-force reference check used by the tests."""
    return s == s[::-1]
