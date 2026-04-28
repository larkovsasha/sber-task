import json

def load_sessions(path: str = "sessions.jsonl") -> list[list[int]]:
    sessions = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                sessions.append(json.loads(line))
    return sessions


def train_test_split(
    sessions: list[list[int]],
) -> tuple[list[list[int]], list[int]]:
    histories = []
    targets = []
    for session in sessions:
        histories.append(session[:-1])
        targets.append(session[-1])
    return histories, targets