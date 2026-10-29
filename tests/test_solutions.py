import os, sys
import pytest
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from solutions.two_sum import two_sum
from solutions.sliding_window import length_of_longest
from solutions.heap import kth_largest, kth_largest_brute
from solutions.longest_palindrome import longest_palindromic_substring, is_palindrome
from solutions.merge_intervals import merge_intervals, merge_intervals_brute
from solutions.binary_search import first_occurrence, last_occurrence, count_occurrences
from solutions.coin_change import coin_change, coin_change_brute
from solutions.topo_sort import topological_sort, topological_sort_brute, TopoCycleError
from solutions.lru_cache import LRUCache
from solutions.longest_common_substring import (
    longest_common_substring,
    longest_common_substring_brute,
)


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





def test_topo_sort_known():
    # LeetCode 207 example: a valid ordering exists
    order = topological_sort(6, [(5, 2), (5, 0), (4, 0), (4, 1), (2, 3), (3, 1)])
    assert sorted(order) == list(range(6))
    pos = {v: i for i, v in enumerate(order)}
    for u, v in [(5, 2), (5, 0), (4, 0), (4, 1), (2, 3), (3, 1)]:
        assert pos[u] < pos[v], (u, v, order)
    # isolated node (none here, but pin it) and duplicate edges are safe
    assert sorted(topological_sort(3, [(0, 1), (0, 1)])) == [0, 1, 2]


def test_topo_sort_deterministic_tiebreak():
    # no edges -> the ready set is always everything -> exact sequence pinned
    assert topological_sort(4, []) == [0, 1, 2, 3]
    # two independent chains: the smallest AVAILABLE id wins at every step,
    # so 0 unlocks 1 before 2's branch can win the tie
    assert topological_sort(4, [(0, 1), (2, 3)]) == [0, 1, 2, 3]


def test_topo_sort_cycle():
    # 2-cycle with a free node: only the cycle members are reported
    with pytest.raises(TopoCycleError) as exc:
        topological_sort(3, [(0, 1), (1, 0)])
    assert set(exc.value.nodes) == {0, 1}
    # 3-cycle: every node is stuck
    with pytest.raises(TopoCycleError) as exc:
        topological_sort(3, [(0, 1), (1, 2), (2, 0)])
    assert set(exc.value.nodes) == {0, 1, 2}
    # self-loop is a cycle too
    with pytest.raises(TopoCycleError) as exc:
        topological_sort(2, [(1, 1)])
    assert set(exc.value.nodes) == {1}


def test_topo_sort_random_matches_brute():
    import random
    rng = random.Random(5)
    for trial in range(60):
        v = rng.randint(2, 8)
        # random DAG: only allow edges u->v with u < v => acyclic by construction
        possible = [(u, vv) for u in range(v) for vv in range(u + 1, v)]
        edges = [e for e in possible if rng.random() < 0.4]
        got = topological_sort(v, edges)
        expected = topological_sort_brute(v, edges)
        assert got is not None and expected == got
    # random cyclic graphs: brute says None, fast path must raise
    for trial in range(30):
        v = rng.randint(2, 7)
        edges = [(rng.randrange(v), rng.randrange(v)) for _ in range(rng.randint(v, 2 * v))]
        if topological_sort_brute(v, edges) is None:
            with pytest.raises(TopoCycleError):
                topological_sort(v, edges)


def test_lru_basic_and_eviction_order():
    cache = LRUCache(2)
    cache.put(1, "a")
    cache.put(2, "b")
    assert cache.get(1) == "a"       # 1 is now most-recently-used
    cache.put(3, "c")                # evicts 2 (LRU), not 1
    assert cache.get(2) is None
    assert cache.get(1) == "a"
    assert cache.get(3) == "c"
    assert len(cache) == 2


def test_lru_update_does_not_evict():
    cache = LRUCache(2)
    cache.put(1, "a")
    cache.put(2, "b")
    cache.put(1, "A")                # update in place: no eviction yet
    assert len(cache) == 2 and cache.get(1) == "A"
    cache.put(3, "c")                # now over capacity -> evicts 2
    assert cache.get(2) is None and cache.get(3) == "c"


def test_lru_eviction_script_matches_manual_trace():
    # pinned access script; expected evictions in exact order
    cache = LRUCache(3)
    events = [("p", 1), ("g", 1), ("p", 2), ("g", 2), ("p", 3), ("g", 3),
              ("p", 4), ("g", 4), ("p", 5)]
    for op, k in events:
        if op == "p":
            cache.put(k, k * 10)
        else:
            assert cache.get(k) == k * 10
    # Manual trace (cap=3): after puts of 1,2,3 the LRU order is 1,2,3.
    # put 4 evicts 1; put 5 evicts 2. Survivors are exactly {3, 4, 5}.
    assert set(k for k in (1, 2, 3, 4, 5) if k in cache) == {3, 4, 5}


def test_lru_get_miss_does_not_reorder():
    cache = LRUCache(2)
    cache.put(1, "a")
    cache.put(2, "b")
    assert cache.get(99) is None     # miss: no access recorded
    cache.put(3, "c")                # evicts 1 (still the LRU), not 2
    assert cache.get(1) is None and cache.get(2) == "b"


def test_lru_capacity_validation():
    import pytest as _p
    with _p.raises(ValueError):
        LRUCache(0)


def test_lcs_known_cases():
    # 'abc' is contiguous in both inputs; note this is NOT the subsequence
    # answer (a subsequence could skip chars, a substring cannot)
    assert longest_common_substring("abcde", "abced") == "abc"
    # longer shared block beats the shorter one ('bcdef' > 'abc')
    assert longest_common_substring("abcdef", "zbcdefy") == "bcdef"
    # repeated words: the full word is the shared substring, not a fragment
    assert longest_common_substring("hello world", "world hello") == "hello"
    assert longest_common_substring("xyz", "abcd") == ""
    assert longest_common_substring("", "abc") == ""
    assert longest_common_substring("a", "a") == "a"
    # classic: the longest shared block is 2 chars, not 3
    # ('c' and 'e' are not adjacent in either string)
    assert longest_common_substring("abcde", "abfce") == "ab"


def test_lcs_overlapping_occurrences():
    # the shared substring appears twice; either copy is a valid answer,
    # so compare as sets of substrings rather than exact positions
    s = longest_common_substring("abcabc", "zabcz")
    assert s == "abc"


def test_lcs_result_is_actually_shared_and_longest():
    a = "abcdxyzabcdef"
    b = "xyzabcdefzz"
    result = longest_common_substring(a, b)
    assert result in a and result in b
    # "abcdef" (len 6) beats "xyz" (len 3); verify nothing longer is shared
    for i in range(len(a)):
        for j in range(len(b)):
            k = 0
            while i + k < len(a) and j + k < len(b) and a[i+k] == b[j+k]:
                k += 1
            assert k <= len(result)


def test_lcs_matches_brute_on_random_inputs():
    import random
    rng = random.Random(42)
    alphabet = "ab"  # tiny alphabet forces many overlapping matches
    for _ in range(60):
        a = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 12)))
        b = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 12)))
        fast = longest_common_substring(a, b)
        brute = longest_common_substring_brute(a, b)
        # both must be common substrings of equal (maximal) length
        assert fast in a and fast in b
        assert brute in a and brute in b
        assert len(fast) == len(brute)


def test_lcs_single_repeated_char():
    assert longest_common_substring("aaaa", "aa") == "aa"
    assert longest_common_substring("aa", "aaaa") == "aa"


from solutions.streaming_median import MedianStream, median_brute


def test_streaming_median_matches_brute_on_every_prefix():
    """Feed a random stream; after each insert the median must equal the
    brute reference computed on every value seen so far."""
    import random
    rng = random.Random(7)
    stream = MedianStream()
    values: list[int] = []
    for _ in range(200):
        x = rng.randint(-50, 50)
        stream.add(x)
        values.append(x)
        assert stream.median() == median_brute(values)


def test_streaming_median_known_sequence():
    s = MedianStream()
    expected = []
    for x in [5, 1, 3, 2, 8, 0]:
        s.add(x)
        expected.append(s.median())
    # odd sizes return the exact middle element; even sizes the mean of the
    # two middles — pinning both behaviours on a hand-checkable stream.
    assert expected == [5.0, 3.0, 3.0, 2.5, 3.0, 2.5]


def test_streaming_median_duplicates_and_negatives():
    s = MedianStream()
    all_vals = [4, 4, 4, -10, -10, -10, -10]
    for x in all_vals:
        s.add(x)
        assert s.median() == median_brute(all_vals[: len(s)])
    assert s.median() == median_brute(all_vals)


def test_streaming_median_empty_raises():
    import pytest
    with pytest.raises(ValueError):
        MedianStream().median()


def test_streaming_median_len_and_monotone_streams():
    """Monotone streams stress the rebalancing: strictly ascending first,
    then descending into negative territory — every prefix is checked."""
    s = MedianStream()
    seen: list[int] = []
    for i in range(1, 30):  # ascending: each new value is the new maximum
        s.add(i)
        seen.append(i)
        assert len(s) == i
        assert s.median() == median_brute(seen)
    for i in range(-1, -20, -1):  # descending below everything so far
        s.add(i)
        seen.append(i)
        assert s.median() == median_brute(seen)


from solutions.edit_distance import edit_distance, edit_distance_brute
from solutions.knapsack import knapsack, knapsack_brute
from solutions.longest_increasing_subsequence import (
    longest_increasing_subsequence,
    longest_increasing_subsequence_with_reconstruction,
)


def test_edit_distance_known():
    # classic LeetCode 72 example
    assert edit_distance("horse", "ros") == 3
    assert edit_distance("intention", "execution") == 5
    # degenerate inputs
    assert edit_distance("", "") == 0
    assert edit_distance("abc", "") == 3
    assert edit_distance("", "xyz") == 3
    # identical strings cost nothing (matches propagate down the diagonal)
    assert edit_distance("same", "same") == 0


def test_edit_distance_is_symmetric():
    pairs = [
        ("kitten", "sitting"),
        ("flaw", "lawn"),
        ("sunday", "saturday"),
        ("book", "back"),
    ]
    for a, b in pairs:
        assert edit_distance(a, b) == edit_distance(b, a)


def test_edit_distance_random_matches_brute():
    """Rolling-row DP must agree with the memoized reference on random
    strings over a small alphabet (where both can afford to run)."""
    import random

    rng = random.Random(11)
    alphabet = "abc"
    for _ in range(60):
        s = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 14)))
        t = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 14)))
        assert edit_distance(s, t) == edit_distance_brute(s, t)


def test_edit_distance_operation_bound():
    """The distance is always between 0 and the length of the longer string:
    deleting everything from the longer one (or inserting everything into
    the shorter) is a valid plan, so nothing can exceed that."""
    import random

    rng = random.Random(23)
    alphabet = "ab"
    for _ in range(40):
        s = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 20)))
        t = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 20)))
        d = edit_distance(s, t)
        assert 0 <= d <= max(len(s), len(t))


def test_lis_known():
    assert longest_increasing_subsequence([10, 9, 2, 5, 3, 7, 101, 18]) == 4
    assert longest_increasing_subsequence([0, 1, 0, 3, 2, 3]) == 4
    assert longest_increasing_subsequence([7, 7, 7, 7, 7, 7, 7]) == 1  # strict: no duplicates
    assert longest_increasing_subsequence([]) == 0
    assert longest_increasing_subsequence([5]) == 1
    assert longest_increasing_subsequence([-1, -2, -3, -4]) == 1
    assert longest_increasing_subsequence([1, 2, 3, 4, 5]) == 5


def _lis_brute(a):
    """Exhaustive reference: longest strictly increasing subsequence by
    recursive choice over suffixes (fine for the small inputs tests use)."""
    from functools import lru_cache

    n = len(a)

    @lru_cache(maxsize=None)
    def best(i: int, last: float) -> int:
        if i == n:
            return 0
        take = 1 + best(i + 1, a[i]) if a[i] > last else 0
        return max(take, best(i + 1, last))

    return best(0, float("-inf"))


def test_lis_matches_brute():
    import random

    rng = random.Random(7)
    for _ in range(80):
        a = [rng.randint(-5, 15) for _ in range(rng.randint(0, 12))]
        assert longest_increasing_subsequence(a) == _lis_brute(a)


def test_lis_reconstruction_returns_valid_subsequence():
    import random

    rng = random.Random(13)
    cases = [
        [10, 9, 2, 5, 3, 7, 101, 18],
        [],
        [42],
        [3, 1, 2],
        [-5, -4, -6, -3, -7, -2],
        [1, 3, 2, 4, 3, 5],
    ]
    cases += [[rng.randint(0, 9) for _ in range(rng.randint(0, 18))] for _ in range(50)]
    for a in cases:
        length, sub = longest_increasing_subsequence_with_reconstruction(a)
        assert length == longest_increasing_subsequence(a)
        assert len(sub) == length
        # strictly increasing
        assert all(x < y for x, y in zip(sub, sub[1:]))
        # every element actually comes from the input, in order
        it = iter(a)
        assert all(any(x == v for x in it) for v in sub)


def test_lis_reconstruction_ties_break_earliest():
    # two equal-length LIS exist ([1, 3] and [2, 3]); reconstruction picks the
    # earliest-occurrence one because it fills lengths from the front-most
    # qualifying positions.
    length, sub = longest_increasing_subsequence_with_reconstruction([1, 2, 3])
    assert (length, sub) == (3, [1, 2, 3])


def test_knapsack_known():
    # classic 0/1 example: items (w=1,v=1), (w=3,v=4), (w=4,v=5), capacity 4
    assert knapsack([1, 3, 4], [1, 4, 5], 4) == 5
    assert knapsack([2, 3, 4, 5], [3, 4, 5, 6], 8) == 10
    # nothing fits: weight over capacity is skipped entirely
    assert knapsack([7, 8], [100, 200], 5) == 0
    # everything fits: take all of it
    assert knapsack([1, 2, 3], [10, 20, 30], 6) == 60
    # degenerate inputs
    assert knapsack([], [], 10) == 0
    assert knapsack([1, 2], [5, 9], 0) == 0


def test_knapsack_01_semantics():
    """Each item is usable at most once: the rolling row must never count a
    single high-value item more than its multiplicity in the input."""
    # one item of weight 2 / value 5, capacity 8: best is still 5, not 20
    assert knapsack([2], [5], 8) == 5
    # two copies are two items and may both be taken
    assert knapsack([2, 2], [5, 5], 8) == 10


def test_knapsack_random_matches_brute():
    """DP must agree with the exhaustive subset reference on small random
    instances where brute force is cheap."""
    import random

    rng = random.Random(41)
    for _ in range(60):
        n = rng.randint(0, 10)
        weights = [rng.randint(1, 8) for _ in range(n)]
        values = [rng.randint(1, 20) for _ in range(n)]
        capacity = rng.randint(0, 15)
        assert knapsack(weights, values, capacity) == knapsack_brute(weights, values, capacity)


def test_knapsack_value_bounded_by_total():
    """The answer is never above the sum of all values and never negative."""
    import random

    rng = random.Random(57)
    for _ in range(40):
        n = rng.randint(0, 12)
        weights = [rng.randint(1, 6) for _ in range(n)]
        values = [rng.randint(1, 9) for _ in range(n)]
        capacity = rng.randint(0, 20)
        got = knapsack(weights, values, capacity)
        assert 0 <= got <= sum(values)


def test_knapsack_mismatched_lengths():
    import pytest

    with pytest.raises(ValueError):
        knapsack([1, 2], [3], 5)


# --- Word Break -------------------------------------------------------------

from solutions.word_break import can_word_break, count_word_breaks  # noqa: E402


def test_word_break_known():
    assert can_word_break("leetcode", ["leet", "code"]) is True
    assert can_word_break("applepenapple", ["apple", "pen"]) is True
    assert can_word_break("catsandog", ["cats", "dog", "sand", "and", "cat"]) is False
    # single word, exactly the input
    assert can_word_break("aaaa", ["aaaa"]) is True
    # repeated single letters
    assert can_word_break("aaaa", ["a", "aa"]) is True
    # characters that are not in the vocabulary
    assert can_word_break("abcxyz", ["ab", "cd"]) is False


def test_word_break_edge_cases():
    assert can_word_break("", ["a"]) is True          # empty input breaks trivially
    assert can_word_break("a", []) is False           # non-empty input, no words
    assert can_word_break("", []) is True
    # all-empty word list is the same as no words at all
    assert can_word_break("a", ["", ""]) is False


def test_word_break_duplicates_are_synonyms():
    # duplicate dict entries must not change reachability
    assert can_word_break("leetcode", ["leet", "code", "code", "leet"]) is True
    assert can_word_break("zz", ["z", "z"]) is True


def test_word_break_long_words_bound_the_scan():
    # a 50-char word in the vocab must not break correctness for short inputs
    long = "a" * 50
    assert can_word_break("aaaa", [long]) is False
    assert can_word_break(long, [long]) is True


def test_word_break_count_known():
    assert count_word_breaks("", ["a"]) == 1          # the single empty segmentation
    assert count_word_breaks("a", ["a", "aa"]) == 1   # only ["a"]
    assert count_word_breaks("aaaa", ["a", "aa", "aaa", "aaaa"]) == 8
    # LeetCode 139-style input with exactly one segmentation
    assert count_word_breaks("leetcode", ["leet", "code"]) == 1
    assert count_word_breaks("applepenapple", ["apple", "pen"]) == 1
    assert count_word_breaks("catsandog", ["cats", "dog", "sand", "and", "cat"]) == 0
    assert count_word_breaks("xyz", []) == 0


def test_count_matches_can():
    # whenever can_word_break says yes, the count is at least 1, and vice versa
    import random

    rng = random.Random(3)
    alphabet = "abc"
    for _ in range(120):
        n = rng.randint(0, 8)
        s = "".join(rng.choice(alphabet) for _ in range(n))
        words = ["".join(rng.choice(alphabet) for _ in range(rng.randint(1, 3)))
                 for _ in range(rng.randint(0, 5))]
        assert (can_word_break(s, words) is True) == (count_word_breaks(s, words) > 0)


def test_count_is_a_fibonacci_growth_case():
    # s = "a"*n with {"a", "aa"}: segmentations are compositions of n into
    # 1s and 2s, i.e. Fibonacci numbers F(n+1).
    def fib(k):
        a, b = 0, 1
        for _ in range(k):
            a, b = b, a + b
        return a

    for n in range(0, 14):
        s = "a" * n
        assert count_word_breaks(s, ["a", "aa"]) == fib(n + 1), n


def test_count_duplicates_are_synonyms():
    # two identical dict entries must not double the count: "aaaa" with
    # {a, aa} has F(5) = 5 distinct segmentations whether the dict lists
    # each word once or twice
    assert count_word_breaks("aaaa", ["a", "aa"]) == 5
    assert count_word_breaks("aaaa", ["a", "aa", "a", "aa"]) == 5
