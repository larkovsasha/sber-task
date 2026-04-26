def hit_at_k(
    recommendations: list[list[int]],
    targets: list[int],
    k: int = 10,
) -> float:
    hits = sum(
        1 for recs, t in zip(recommendations, targets) if t in recs[:k]
    )
    return hits / len(targets)


def baseline_recommendations(
    popularity: list[int],
    n: int,
    top_k: int = 10,
) -> list[list[int]]:
    return [popularity[:top_k]] * n
