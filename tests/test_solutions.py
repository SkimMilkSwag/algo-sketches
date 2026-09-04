import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from solutions.two_sum import two_sum
from solutions.sliding_window import length_of_longest
from solutions.heap import kth_largest, kth_largest_brute
from solutions.longest_palindrome import longest_palindromic_substring, is_palindrome
from solutions.merge_intervals import merge_intervals, merge_intervals_brute
from solutions.binary_search import first_occurrence, last_occurrence, count_occurrences
from solutions.coin_change import coin_change, coin_change_brute


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


def test_merge_intervals_known():
    # classic LeetCode examples
    assert merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]]) == [[1, 6], [8, 10], [15, 18]]
    assert merge_intervals([[1, 4], [4, 5]]) == [[1, 5]]  # touching endpoints merge
    # nested interval: [1,10] swallows [2,3]
    assert merge_intervals([[1, 10], [2, 3]]) == [[1, 10]]
    assert merge_intervals([[2, 3], [4, 5]]) == [[2, 3], [4, 5]]
    # unsorted input is sorted before the sweep
    assert merge_intervals([[8, 10], [1, 6], [2, 4]]) == [[1, 6], [8, 10]]


def test_merge_intervals_degenerate():
    assert merge_intervals([]) == []
    assert merge_intervals([[5, 5]]) == [[5, 5]]
    # input is not mutated
    orig = [(1, 3), (2, 6)]
    merge_intervals(orig)
    assert orig == [(1, 3), (2, 6)]


def test_merge_intervals_random_vs_brute():
    import random
    rng = random.Random(7)
    for _ in range(30):
        n = rng.randint(1, 8)
        intervals = [(a, b) for a, b in
                     sorted((rng.randint(0, 12), rng.randint(0, 12)) for _ in range(n)) if a <= b]
        got = merge_intervals(intervals)
        expected = merge_intervals_brute(intervals)
        assert got == expected
        # result must be disjoint and sorted by start
        for i in range(len(got) - 1):
            assert got[i][1] < got[i + 1][0]


def test_binary_search_first_last_known():
    # classic LeetCode 34 examples
    nums = [1, 2, 2, 2, 3, 4, 4, 5, 5]
    assert first_occurrence(nums, 2) == 1
    assert last_occurrence(nums, 2) == 3
    # target at the very edges of the array
    assert first_occurrence(nums, 1) == 0
    assert last_occurrence(nums, 1) == 0
    assert first_occurrence(nums, 5) == 7
    assert last_occurrence(nums, 5) == 8
    # single-element arrays and empty input
    assert first_occurrence([7], 7) == 0
    assert last_occurrence([7], 7) == 0
    assert first_occurrence([], 1) == 0
    assert last_occurrence([], 1) == -1


def test_binary_search_absent_targets():
    # when target is absent, the helpers return insertion points (or -1),
    # so count must come out exactly 0 -- including the empty-array edge case
    nums = [2, 4, 6]
    assert count_occurrences(nums, 3) == 0   # between two elements
    assert count_occurrences(nums, 1) == 0   # before the first element
    assert count_occurrences(nums, 7) == 0   # after the last element
    assert count_occurrences([], 1) == 0


def test_binary_search_random_vs_brute():
    import random
    rng = random.Random(11)
    for _ in range(30):
        n = rng.randint(0, 40)
        # non-decreasing array with deliberate duplicates
        arr = sorted(rng.choice(range(6)) for _ in range(n))
        target = rng.randint(0, 7)
        expected_first = arr.index(target) if target in arr else None
        expected_last = len(arr) - 1 - arr[::-1].index(target) if target in arr else None
        assert count_occurrences(arr, target) == arr.count(target)
        # when present, the bounds must bracket exactly the run of target
        if expected_first is not None:
            got_first = first_occurrence(arr, target)
            got_last = last_occurrence(arr, target)
            assert got_first == expected_first and got_last == expected_last
            assert arr[got_first] == arr[got_last] == target
            # everything in [first..last] is target, just outside it is not
            if got_first > 0:
                assert arr[got_first - 1] < target
            if got_last < n - 1:
                assert arr[got_last + 1] > target
        else:
            # absent: first is the insertion point, last points before it
            ins = first_occurrence(arr, target)
            assert last_occurrence(arr, target) == ins - 1


def test_coin_change_known():
    # classic LeetCode examples
    assert coin_change([1, 2, 5], 11) == 3          # 5+5+1
    assert coin_change([2], 3) == -1                # odd amount, even coins only
    assert coin_change([1], 0) == 0                 # zero amount needs zero coins
    assert coin_change([], 1) == -1                 # no coins at all
    assert coin_change([186, 419, 83, 402], 6249) == 16


def test_coin_change_degenerate():
    import random
    rng = random.Random(9)
    for _ in range(30):
        coins = sorted(set(rng.randint(1, 15) for _ in range(rng.randint(1, 5))))
        amount = rng.randint(0, 60)
        # DP answer must match the exhaustive reference exactly
        assert coin_change(coins, amount) == coin_change_brute(coins, amount)


def test_coin_change_validity():
    import random
    rng = random.Random(13)
    for _ in range(25):
        coins = sorted(set(rng.randint(1, 20) for _ in range(rng.randint(1, 4))))
        amount = rng.randint(1, 80)
        got = coin_change(coins, amount)
        if got != -1:
            # the count must be achievable: some multiset of exactly `got` coins sums to amount
            # (verified by rebuilding with the DP's own table-free brute check)
            assert got >= 1
            assert coin_change_brute(coins, amount) == got
        else:
            # no combination exists even for the reference search
            assert coin_change_brute(coins, amount) == -1



