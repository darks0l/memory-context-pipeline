#!/usr/bin/env python3
"""One-command memory cycle orchestrator.

Flow:
1) auto_trigger decision
2) context_router model route decision
3) optional channel_memory_store append (if trigger=true)
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
from pathlib import Path


def run_json(cmd: list[str]) -> dict:
    p = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return json.loads(p.stdout)


def main() -> int:
    ap = argparse.ArgumentParser(description="Run full memory orchestration cycle")
    ap.add_argument("--root", default=".")
    ap.add_argument("--guild-id", required=True)
    ap.add_argument("--channel-id", required=True)
    ap.add_argument("--task", default="summarize")
    ap.add_argument("--chars", type=int, required=True)
    ap.add_argument("--threshold", type=int, default=10000)
    ap.add_argument("--digest-minutes", type=int, default=360)
    ap.add_argument("--remember", action="store_true")
    ap.add_argument("--has-image", action="store_true")
    ap.add_argument("--text", default="Auto-cycle checkpoint")
    ap.add_argument("--summary-json", default="")
    args = ap.parse_args()

    root = Path(args.root)
    auto_trigger = root / "skill" / "scripts" / "auto_trigger.py"
    router = root / "skill" / "scripts" / "context_router.py"
    store = root / "skill" / "scripts" / "channel_memory_store.py"

    trigger_cmd = [
        "python", str(auto_trigger),
        "--root", str(root),
        "--guild-id", args.guild_id,
        "--channel-id", args.channel_id,
        "--chars", str(args.chars),
        "--threshold", str(args.threshold),
        "--digest-minutes", str(args.digest_minutes),
    ]
    if args.remember:
        trigger_cmd.append("--remember")

    route_cmd = [
        "python", str(router),
        "--task", args.task,
        "--chars", str(args.chars),
        "--threshold", str(args.threshold),
    ]
    if args.has_image:
        route_cmd.append("--has-image")

    trig = run_json(trigger_cmd)
    route = run_json(route_cmd)

    stored = None
    if trig.get("trigger"):
        store_cmd = [
            "python", str(store),
            "--root", str(root),
            "--guild-id", args.guild_id,
            "--channel-id", args.channel_id,
            "--text", f"{args.text} | route={route.get('route')} model={route.get('model')}",
        ]
        if args.summary_json:
            store_cmd.extend(["--summary-json", args.summary_json])
        stored = run_json(store_cmd)

    out = {
        "ok": True,
        "at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "trigger": trig,
        "route": route,
        "stored": stored,
    }
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
