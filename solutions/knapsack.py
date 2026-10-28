"""0/1 Knapsack — maximum value achievable under a weight capacity.

Each item may be taken at most once (the "0/1" part). The bottom-up DP
fills a table where dp[w] tracks the best value using a prefix of items
and total weight at most w: for each item, either skip it (keep the old
row) or take it (add its value to the row from capacity w - weight).

  - knapsack(weights, values, capacity): maximum achievable value
  - knapsack_brute(weights, values, capacity): exhaustive subset reference

Time O(n * capacity), space O(capacity) with the rolling row.
"""


def knapsack(weights: list[int], values: list[int], capacity: int) -> int:
    """Best total value for a 0/1 knapsack under the given capacity.

    dp[w] holds the best value achievable with weight at most w using only
    items seen so far. Each item is folded in from high capacities down,
    which prevents taking the same item twice within one pass. Items whose
    weight exceeds the current capacity are simply skipped (they can never
    fit into any remaining state).
    """
    if len(weights) != len(values):
        raise ValueError("weights and values must have the same length")

    dp = [0] * (capacity + 1)
    for weight, value in zip(weights, values):
        if weight > capacity:
            continue
        for w in range(capacity, weight - 1, -1):
            candidate = dp[w - weight] + value
            if candidate > dp[w]:
                dp[w] = candidate
    return dp[capacity]


def knapsack_brute(weights: list[int], values: list[int], capacity: int) -> int:
    """Exhaustive reference: check every subset, keep the best feasible one.

    Same contract as knapsack. 2**n subsets, so tests keep item counts small
    when using this one.
    """
    n = len(weights)
    best = 0
    for mask in range(1 << n):
        total_w = sum(weights[i] for i in range(n) if mask >> i & 1)
        if total_w <= capacity:
            total_v = sum(values[i] for i in range(n) if mask >> i & 1)
            if total_v > best:
                best = total_v
    return best
