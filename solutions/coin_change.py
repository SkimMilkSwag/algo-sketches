"""Coin change — minimum number of coins to make an amount (LeetCode 322).

Classic bottom-up DP: dp[a] = min number of coins that sum to a. Every
sub-amount is strictly smaller than a, so filling dp left-to-right means the
transition only reads already-settled values. Also includes a brute-force
reference (exhaustive search with memoization) for cross-checking in tests.

  - coin_change(coins, amount): min coins needed, or -1 if no combination works
  - coin_change_brute(coins, amount): exhaustive reference, same contract

Time O(amount * len(coins)), space O(amount).
"""


def coin_change(coins: list[int], amount: int) -> int:
    """Fewest coins that sum to `amount`, or -1 if impossible.

    dp[0] = 0 by convention (zero coins make zero). Each state takes the
    minimum over every coin c <= a of dp[a - c] + 1, so the table is filled
    in one left-to-right pass. A state that never gets a finite value was
    unreachable from dp[0] and means no combination works.
    """
    if amount == 0:
        return 0
    inf = float("inf")
    dp = [inf] * (amount + 1)
    dp[0] = 0
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and dp[a - c] + 1 < dp[a]:
                dp[a] = dp[a - c] + 1
    return dp[amount] if dp[amount] != inf else -1


def coin_change_brute(coins: list[int], amount: int) -> int:
    """Exhaustive reference: try every coin at every sub-amount.

    Same -1 contract as coin_change. Exponential without the memo dict, so
    tests keep amounts small when using this one.
    """
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def solve(a: int) -> int:
        if a == 0:
            return 0
        best = float("inf")
        for c in coins:
            if c <= a:
                rest = solve(a - c)
                if rest != -1 and rest + 1 < best:
                    best = rest + 1
        return best if best != float("inf") else -1

    return solve(amount)
