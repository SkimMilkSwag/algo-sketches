import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from solutions.two_sum import two_sum
from solutions.sliding_window import length_of_longest
from solutions.heap import kth_largest, kth_largest_brute


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
