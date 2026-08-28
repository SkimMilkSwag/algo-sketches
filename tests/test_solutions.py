import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from solutions.two_sum import two_sum
from solutions.sliding_window import length_of_longest
from solutions.heap import kth_largest, kth_largest_brute
from solutions.longest_palindrome import longest_palindromic_substring, is_palindrome


def test_two_sum():
    assert two_sum([2, 7, 11, 15], 9) == [0, 1]
    assert sorted(two_sum([3, 2, 4], 6)) == [1, 2]


def test_longest_substring():
    assert length_of_longest("abcabcbb") == 3
    assert length_of_longest("bbbbb") == 1
    assert length_of_longest("") == 0


def test_kth_largest():
    assert kth_largest([3, 2, 1, 5, 6, 4], 2) == 5
    # brute and heap agree across a range
    import random
    rng = random.Random(1)
    for _ in range(20):
        arr = [rng.randint(0, 100) for _ in range(rng.randint(3, 50))]
        k = rng.randint(1, len(arr))
        assert kth_largest(arr, k) == kth_largest_brute(arr, k)


def test_longest_palindrome_known():
    # classic LeetCode examples
    assert longest_palindromic_substring("babad") in ("bab", "aba")
    assert longest_palindromic_substring("cbbd") == "bb"
    # degenerate inputs
    assert longest_palindromic_substring("") == ""
    assert longest_palindromic_substring("a") == "a"


def test_longest_palindrome_random():
    # result must be a real substring of s and actually palindromic,
    # and no longer palindromic substring may exist (brute-force check)
    import random

    def brute(s):
        best = ""
        for i in range(len(s)):
            for j in range(i + 1, len(s) + 1):
                t = s[i:j]
                if is_palindrome(t) and len(t) > len(best):
                    best = t
        return best

    rng = random.Random(42)
    alphabet = "ab"
    for _ in range(25):
        s = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 28)))
        got = longest_palindromic_substring(s)
        expected_len = len(brute(s))
        assert is_palindrome(got) and len(got) == expected_len
        # must be a contiguous substring of the input
        assert s.find(got) != -1 or got == ""

