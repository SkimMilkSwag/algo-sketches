"""Two Sum — LeetCode 1.

Given an array of integers and a target, return the indices of the two elements
that add up to target. O(n) using a hash map.
"""
from typing import List


def two_sum(nums: List[int], target: int) -> List[int]:
    seen = {}
    for i, n in enumerate(nums):
        need = target - n
        if need in seen:
            return [seen[need], i]
        seen[n] = i
    raise ValueError("no solution")
