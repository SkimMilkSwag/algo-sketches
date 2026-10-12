"""LRU Cache — LeetCode 146.

O(1) get/put via OrderedDict: most-recently-used at the end of the dict,
least-recently-used at the front. get() moves the key to the back (it just
became "used"); put() updates or appends, and when capacity is exceeded the
front item — the longest-idle one — is evicted.

The eviction *order* is the interesting bit and is what tests pin: a fixed
access script must eject keys in exactly the order the class predicts, so
a wrong ordering (e.g. FIFO instead of LRU) fails loudly.
"""

from collections import OrderedDict

__all__ = ["LRUCache"]


class LRUCache:
    """Fixed-capacity cache with least-recently-used eviction.

    `capacity` must be >= 1; both get() and put() are O(1). A get() on a
    missing key returns None and does NOT count as an access (no reordering).
    """

    def __init__(self, capacity: int):
        if capacity < 1:
            raise ValueError("capacity must be >= 1")
        self._cap = capacity
        self._data: OrderedDict = OrderedDict()

    def get(self, key) -> "object | None":
        """Return the cached value for `key`, marking it most-recently-used."""
        if key not in self._data:
            return None
        self._data.move_to_end(key)
        return self._data[key]

    def put(self, key, value) -> None:
        """Insert or update `key`; evict the LRU entry when over capacity."""
        if key in self._data:
            self._data[key] = value
            self._data.move_to_end(key)
        else:
            if len(self._data) == self._cap:
                self._data.popitem(last=False)  # drop the oldest-used item
            self._data[key] = value

    def __contains__(self, key) -> bool:
        return key in self._data

    def __len__(self) -> int:
        return len(self._data)
