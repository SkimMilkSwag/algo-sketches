"""Binary Search variants — first / last occurrence (LeetCode 34, 852).

Given a sorted array that may contain duplicates, find where a value's run of
equal elements starts and ends in O(log n) instead of a linear scan. The two
searches are the same bisect loop with different "which side to push on":
  - first: when nums[mid] >= target, the answer is at mid or left -> hi = mid
  - last:  when nums[mid] <= target, the answer is at mid or right -> lo = mid
`count` composes them: (last - first + 1) if present, else 0.
"""


def first_occurrence(nums: list[int], target: int) -> int:
    """Index of the first element >= target (leftmost insertion point).

    Returns len(nums) if every element is < target. The caller checks
    nums[idx] == target to distinguish "found" from "insertion point".
    """
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] >= target:
            hi = mid
        else:
            lo = mid + 1
    return lo


def last_occurrence(nums: list[int], target: int) -> int:
    """Index of the last element <= target (rightmost insertion point - 1).

    Returns -1 if every element is > target. The caller checks
    nums[idx] == target to distinguish "found" from "insertion point".
    """
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] <= target:
            lo = mid + 1
        else:
            hi = mid
    return lo - 1


def count_occurrences(nums: list[int], target: int) -> int:
    """How many times target appears in the sorted array, or 0 if absent."""
    first = first_occurrence(nums, target)
    if first == len(nums) or nums[first] != target:
        return 0
    last = last_occurrence(nums, target)
    return last - first + 1
