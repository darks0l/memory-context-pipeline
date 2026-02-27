#!/usr/bin/env python3
import argparse
import json
from typing import Dict, List

LOCAL_TASKS = {
    "summarize",
    "compress",
    "extract-memory-candidates",
    "dedupe-notes",
}

LOCAL_VISION_TASKS = {
    "image-caption",
    "screenshot-summary",
    "ocr-extract",
}


def estimate_tokens(chars: int) -> int:
    # Fast, model-agnostic heuristic for English-heavy text.
    return max(1, int(chars * 0.27))


def decide(
    task: str,
    chars: int,
    threshold: int,
    has_image: bool = False,
    local_model: str = "lfm2",
    local_vision_model: str = "qwen3-vl",
    premium_model: str = "opus",
) -> Dict:
    est_tokens = estimate_tokens(chars)
    reasons: List[str] = []

    route = "premium"
    chosen_model = premium_model
    confidence = 0.55

    if has_image or task in LOCAL_VISION_TASKS:
        route = "local"
        chosen_model = local_vision_model
        confidence = 0.92
        reasons.append("multimodal_branch")
        if has_image:
            reasons.append("has_image:true")
        if task in LOCAL_VISION_TASKS:
            reasons.append(f"vision_task:{task}")
    elif task in LOCAL_TASKS:
        route = "local"
        chosen_model = local_model
        confidence = 0.9
        reasons.append(f"task:{task}")

    if est_tokens >= threshold:
        route = "local"
        if chosen_model == premium_model:
            chosen_model = local_model
        confidence = max(confidence, 0.86)
        reasons.append(f"token_threshold:{est_tokens}>={threshold}")

    fallback_chain = [premium_model] if route == "premium" else [local_model, premium_model]

    return {
        "route": route,
        "model": chosen_model,
        "fallback_chain": fallback_chain,
        "estimated_tokens": est_tokens,
        "threshold": threshold,
        "task": task,
        "has_image": has_image,
        "confidence": round(confidence, 2),
        "needs_premium_review": confidence < 0.7,
        "decision_trace": reasons,
    }


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Deterministic routing for memory/context pipeline")
    p.add_argument("--task", default="general", help="Task type")
    p.add_argument("--chars", type=int, required=True, help="Input character count")
    p.add_argument("--threshold", type=int, default=10000, help="Token threshold for local routing")
    p.add_argument("--has-image", action="store_true", help="Mark input as multimodal/image-bearing")
    p.add_argument("--local-model", default="lfm2", help="Local text model alias")
    p.add_argument("--local-vision-model", default="qwen3-vl", help="Local vision model alias")
    p.add_argument("--premium-model", default="opus", help="Premium model alias")
    args = p.parse_args()

    print(
        json.dumps(
            decide(
                args.task,
                args.chars,
                args.threshold,
                has_image=args.has_image,
                local_model=args.local_model,
                local_vision_model=args.local_vision_model,
                premium_model=args.premium_model,
            ),
            indent=2,
        )
    )
