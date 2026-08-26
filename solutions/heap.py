"""Kth largest element — LeetCode 215.

O(n log k) using a min-heap of size k. Also includes a brute-force reference.
"""
import heapq


def kth_largest(nums: list[int], k: int) -> int:
    heap = []
    for n in nums:
        if len(heap) < k:
            heapq.heappush(heap, n)
        elif n > heap[0]:
            heapq.heapreplace(heap, n)
    return heap[0]


def kth_largest_brute(nums: list[int], k: int) -> int:
    return sorted(nums, reverse=True)[k - 1]
