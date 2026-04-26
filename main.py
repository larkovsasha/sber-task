import sys

from utils import load_sessions, train_test_split
from graph import build_transition_graph, build_popularity, Graph
from evaluate import baseline_recommendations, hit_at_k

MIN_COUNT = 2
TOP_K = 10


def main(data_path: str = "sessions.jsonl") -> None:
    sessions = load_sessions(data_path)

    histories, targets = train_test_split(sessions)

    graph = build_transition_graph(histories, min_count=MIN_COUNT)
    popularity = build_popularity(histories)

    rec = Graph(graph, popularity, top_k=TOP_K)
    predictions = [rec.recommend(h) for h in histories]

    model_score = hit_at_k(predictions, targets, k=TOP_K)
    base_score = hit_at_k(
        baseline_recommendations(popularity, len(targets), TOP_K), targets, k=TOP_K
    )

    print(f"Baseline = {base_score:.4f}")
    print(f"Final model Hit@{TOP_K} = {model_score:.4f}")


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "sessions.jsonl"
    main(path)
