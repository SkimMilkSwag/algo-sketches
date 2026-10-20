# algo-sketches

A growing collection of algorithm solutions — the problems I keep coming back to
when sharpening up. Each solution lives in its own module with a docstring stating
the problem and complexity, plus a test that pins the behaviour. New problems get
added over time.

## Current problems

| Problem | File | Approach | Complexity |
|---------|------|----------|------------|
| Two Sum | `solutions/two_sum.py` | hash map of value -> index | O(n) time, O(n) space |
| Longest Substring Without Repeating Characters | `solutions/sliding_window.py` | sliding window + last-index dict | O(n) time, O(min(n, alphabet)) space |
| Kth Largest Element | `solutions/heap.py` | min-heap of size k (+ brute reference) | O(n log k) time, O(k) space |
| Longest Palindromic Substring | `solutions/longest_palindrome.py` | center expansion (odd + even centers) | O(n^2) time, O(1) space |
| Merge Intervals | `solutions/merge_intervals.py` | sort by start + sweep (+ brute reference) | O(n log n) time, O(n) space |
| Binary Search — first / last occurrence | `solutions/binary_search.py` | two-sided binary search (+ count helper) | O(log n) time, O(1) space |
| Coin Change (min coins) | `solutions/coin_change.py` | bottom-up DP over sub-amounts (+ brute reference) | O(amount * len(coins)) time, O(amount) space |
| Topological Sort | `solutions/topo_sort.py` | Kahn's algorithm (in-degree queue, cycle detection) + brute reference | O(V + E) time, O(V + E) space |
| LRU Cache | `solutions/lru_cache.py` | OrderedDict: MRU at the back, evict from the front | O(1) get/put, O(capacity) space |
| Longest Common Substring | `solutions/longest_common_substring.py` | DP over suffix lengths, single rolling row (+ brute reference) | O(m*n) time, O(min(m,n)) space |
| Streaming Median Maintenance | `solutions/streaming_median.py` | two heaps (max-heap low / min-heap high, O(1) median query) + brute reference | O(n log n) total for n adds, O(1) per median |

## Run the tests

```bash
python -m pytest tests/ -v
```

## Adding a solution

Drop a new module in `solutions/`, write the function, add a test in
`tests/test_solutions.py`, and add a row to the table above.

## License

MIT — see [LICENSE](LICENSE).
