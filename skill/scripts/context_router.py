#!/usr/bin/env python3
import argparse
import json

LOCAL_TASKS = {
    "summarize",
    "compress",
    "extract-memory-candidates",
    "dedupe-notes",
}

def estimate_tokens(chars: int) -> int:
    # Fast, model-agnostic heuristic for English-heavy text.
    return max(1, int(chars * 0.27))


def decide(task: str, chars: int, threshold: int):
    est_tokens = estimate_tokens(chars)
    reasons = []

    route = "premium"
    if task in LOCAL_TASKS:
        route = "local"
        reasons.append(f"task:{task}")
    if est_tokens >= threshold:
        route = "local"
        reasons.append(f"token_threshold:{est_tokens}>={threshold}")

    return {
        "route": route,
        "estimated_tokens": est_tokens,
        "threshold": threshold,
        "task": task,
        "reasons": reasons,
    }


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Deterministic routing for memory/context pipeline")
    p.add_argument("--task", default="general", help="Task type")
    p.add_argument("--chars", type=int, required=True, help="Input character count")
    p.add_argument("--threshold", type=int, default=10000, help="Token threshold for local routing")
    args = p.parse_args()

    print(json.dumps(decide(args.task, args.chars, args.threshold), indent=2))
