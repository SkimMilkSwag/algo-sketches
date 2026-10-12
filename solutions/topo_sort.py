"""Topological Sort (Kahn's algorithm) — LeetCode 207/210.

O(V + E): count in-degrees, seed the queue with every zero-in-degree node,
then peel a node off, relax its out-neighbours, and enqueue any that reach
zero in-degree. A topological ordering exists iff every node was peeled —
if fewer than V nodes come out of the queue, the remaining subgraph is a
cycle (or is downstream of one) and we raise.

Determinism: when several nodes are ready at once, the lexicographically
smallest node id wins, so the same graph always yields the same ordering.
That makes the function testable without comparing against an exact
sequence (there can be many valid orderings); tests pin specific edges
and the cycle case instead.
"""

__all__ = ["topological_sort", "TopoCycleError"]


class TopoCycleError(ValueError):
    """Raised when the graph contains a cycle; `nodes` lists the offenders."""

    def __init__(self, nodes: list[int]):
        self.nodes = nodes
        super().__init__("cycle detected involving node(s) %s" % (sorted(nodes),))


def topological_sort(num_nodes: int, edges: list[tuple[int, int]]) -> list[int]:
    """Return a valid topological ordering of nodes 0..num_nodes-1.

    `edges` is a list of (u, v) meaning u must come before v. Nodes that
    never appear in any edge are included, so the result always has exactly
    num_nodes entries. Raises :class:`TopoCycleError` if no ordering exists;
    duplicate edges are tolerated (they just decrement twice, matching the
    two recorded out-edges).
    """
    indegree = [0] * num_nodes
    out: list[list[int]] = [[] for _ in range(num_nodes)]
    for u, v in edges:
        out[u].append(v)
        indegree[v] += 1

    ready: list[int] = [i for i in range(num_nodes) if indegree[i] == 0]
    order: list[int] = []
    placed = set(order)
    while True:
        if not ready:
            break
        # smallest AVAILABLE ready node first keeps the output deterministic;
        # min() each round so already-ready nodes never leapfrog ones that
        # just became ready (a full-list sort would reorder them)
        node = min(ready)
        ready.remove(node)
        placed.add(node)
        order.append(node)
        for v in out[node]:
            indegree[v] -= 1
            if indegree[v] == 0:
                ready.append(v)

    if len(order) != num_nodes:
        raise TopoCycleError([i for i in range(num_nodes) if i not in placed])
    return order


def topological_sort_brute(
    num_nodes: int, edges: list[tuple[int, int]]
) -> list[int] | None:
    """Reference implementation (repeatedly pick the smallest valid node).

    O(V^2 + V*E): on each of V steps scan for the smallest node whose
    predecessors are all already placed. Returns None when a cycle leaves
    no valid choice. Used by tests to validate the fast path's ordering
    against an independent construction, and to detect cycles.
    """
    preds: list[set[int]] = [set() for _ in range(num_nodes)]
    for u, v in edges:
        preds[v].add(u)

    placed: set[int] = set()
    order: list[int] = []
    while len(order) < num_nodes:
        candidate = None
        for i in range(num_nodes):
            if i not in placed and preds[i] <= placed:
                candidate = i
                break
        if candidate is None:
            return None  # nothing left to pick: a cycle holds the rest
        order.append(candidate)
        placed.add(candidate)
    return order
