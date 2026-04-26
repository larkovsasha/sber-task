from collections import Counter, defaultdict
TOP_K = 10


def build_transition_graph(
    histories: list[list[int]],
    min_count: int = 2,
) -> dict[int, dict[int, float]]:
    raw: dict[int, Counter] = defaultdict(Counter)
    for history in histories:
        for i in range(len(history) - 1):
            raw[history[i]][history[i + 1]] += 1

    graph: dict[int, dict[int, float]] = {}
    for src, neighbors in raw.items():
        kept = {j: c for j, c in neighbors.items() if c >= min_count}
        if not kept:
            continue
        total = sum(kept.values())
        graph[src] = {j: c / total for j, c in kept.items()}
    return graph


def build_popularity(histories: list[list[int]]) -> list[int]:
    counts: Counter = Counter()
    for history in histories:
        counts.update(history)
    return [item for item, _ in counts.most_common()]


class Graph:
    def __init__(
        self,
        graph: dict[int, dict[int, float]],
        popularity: list[int],
        top_k: int = TOP_K,
    ) -> None:
        self.graph = graph
        self.fallback = popularity[:top_k]
        self.top_k = top_k

    def recommend(self, history: list[int]) -> list[int]:
        last_item = history[-1]
        if last_item not in self.graph:
            return self.fallback

        neighbors = self.graph[last_item]
        ranked = sorted(neighbors.items(), key=lambda x: x[1], reverse=True)
        recs = [item for item, _ in ranked[: self.top_k]]

        if len(recs) < self.top_k:
            seen = set(recs)
            for item in self.fallback:
                if item not in seen:
                    recs.append(item)
                if len(recs) == self.top_k:
                    break

        return recs
