#!/usr/bin/env python3
"""Quick validation runner for multimodal routing decisions.

Runs the router against recommended vision task types and prints a compact report.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


VISION_TASKS = ["image-caption", "screenshot-summary", "ocr-extract"]


def run_router(router_path: Path, task: str, chars: int, has_image: bool) -> dict:
    cmd = [
        "python",
        str(router_path),
        "--task",
        task,
        "--chars",
        str(chars),
    ]
    if has_image:
        cmd.append("--has-image")

    proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return json.loads(proc.stdout)


def main() -> int:
    p = argparse.ArgumentParser(description="Validate vision task routing behavior")
    p.add_argument("--router", default="skill/scripts/context_router.py")
    p.add_argument("--chars", type=int, default=1200)
    args = p.parse_args()

    router = Path(args.router)
    rows = []

    for t in VISION_TASKS:
        d = run_router(router, t, args.chars, has_image=True)
        rows.append({
            "task": t,
            "route": d.get("route"),
            "model": d.get("model"),
            "confidence": d.get("confidence"),
            "trace": d.get("decision_trace", []),
        })

    out = {
        "ok": all(r["route"] == "local" and "qwen3-vl" in str(r["model"]) for r in rows),
        "rows": rows,
    }
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
