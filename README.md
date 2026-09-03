# algo-sketches

A growing collection of algorithm solutions — the problems I keep coming back to
when sharpening up. Each solution lives in its own module with a docstring stating
the problem and complexity, plus a test that pins the behaviour. New problems get
added over time.

## Current problems

| Problem | File | Approach | Complexity |
|---------|------|----------|------------|
| Two Sum | `solutions/two_sum.py` | hash map | O(n) |
| Longest Substring Without Repeating Characters | `solutions/sliding_window.py` | sliding window + last-index dict | O(n) |
| Kth Largest Element | `solutions/heap.py` | min-heap of size k (+ brute reference) | O(n log k) |
| Longest Palindromic Substring | `solutions/longest_palindrome.py` | center expansion (odd + even centers) | O(n^2) |
| Merge Intervals | `solutions/merge_intervals.py` | sort + sweep (+ brute reference) | O(n log n) |

## Run the tests

```bash
python -m pytest tests/ -v
```

## Adding a solution

Drop a new module in `solutions/`, write the function, add a test in
`tests/test_solutions.py`, and add a row to the table above.

## License

MIT — see [LICENSE](LICENSE).
