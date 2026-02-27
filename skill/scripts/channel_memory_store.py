#!/usr/bin/env python3
"""Append channel-scoped memory records using a lightweight folder layout.

Layout:
  memory/channels/<guild_id>/<channel_id>/YYYY-MM-DD.md
  memory/channels/<guild_id>/<channel_id>/summaries/YYYY-Www.md
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path


def ensure_path(root: Path, guild_id: str, channel_id: str) -> Path:
    p = root / "memory" / "channels" / guild_id / channel_id
    p.mkdir(parents=True, exist_ok=True)
    return p


def append_daily(base: Path, text: str, ts: dt.datetime) -> Path:
    daily = base / f"{ts.date().isoformat()}.md"
    with daily.open("a", encoding="utf-8") as f:
        f.write(f"\n[{ts.isoformat()}] {text}\n")
    return daily


def append_weekly_summary(base: Path, payload: dict, ts: dt.datetime) -> Path:
    iso = ts.isocalendar()
    summaries = base / "summaries"
    summaries.mkdir(parents=True, exist_ok=True)
    weekly = summaries / f"{iso.year}-W{iso.week:02d}.md"

    summary_short = payload.get("summary_short", "")
    memory_candidates = payload.get("memory_candidates", [])
    risk_flags = payload.get("risk_flags", [])

    with weekly.open("a", encoding="utf-8") as f:
        f.write(f"\n## {ts.isoformat()}\n")
        if summary_short:
            f.write(f"- Summary: {summary_short}\n")
        if memory_candidates:
            f.write("- Memory candidates:\n")
            for c in memory_candidates[:8]:
                txt = c.get("text", "") if isinstance(c, dict) else str(c)
                conf = c.get("confidence", "?") if isinstance(c, dict) else "?"
                f.write(f"  - ({conf}) {txt}\n")
        if risk_flags:
            f.write("- Risk flags:\n")
            for rf in risk_flags:
                f.write(f"  - {rf}\n")
    return weekly


def main() -> int:
    p = argparse.ArgumentParser(description="Channel memory append helper")
    p.add_argument("--root", default=".", help="Workspace root")
    p.add_argument("--guild-id", required=True)
    p.add_argument("--channel-id", required=True)
    p.add_argument("--text", required=True, help="Raw line to append to daily log")
    p.add_argument("--summary-json", help="Optional worker JSON payload for weekly summaries")
    args = p.parse_args()

    now = dt.datetime.now(dt.timezone.utc)
    base = ensure_path(Path(args.root), args.guild_id, args.channel_id)
    daily = append_daily(base, args.text, now)

    weekly = None
    if args.summary_json:
        payload = json.loads(args.summary_json)
        weekly = append_weekly_summary(base, payload, now)

    out = {
        "ok": True,
        "daily": str(daily),
        "weekly": str(weekly) if weekly else None,
    }
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
