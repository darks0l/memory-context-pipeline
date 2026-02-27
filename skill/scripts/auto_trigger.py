#!/usr/bin/env python3
"""Auto-trigger helper for channel memory pipeline.

This script decides when to persist channel memory based on:
- estimated token threshold
- explicit remember flag
- periodic digest interval

It writes a small state file to avoid noisy repeat writes.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path


def utcnow() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def estimate_tokens(chars: int) -> int:
    return max(1, int(chars * 0.27))


def state_path(root: Path, guild_id: str, channel_id: str) -> Path:
    p = root / "memory" / "channels" / guild_id / channel_id
    p.mkdir(parents=True, exist_ok=True)
    return p / ".trigger_state.json"


def load_state(path: Path) -> dict:
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def save_state(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def should_trigger(now: dt.datetime, st: dict, *, remember: bool, est_tokens: int, threshold: int, digest_minutes: int) -> tuple[bool, list[str]]:
    reasons: list[str] = []

    if remember:
        reasons.append("explicit_remember")

    if est_tokens >= threshold:
        reasons.append(f"threshold:{est_tokens}>={threshold}")

    last_digest = st.get("lastDigestAt")
    if digest_minutes > 0:
        if not last_digest:
            reasons.append("digest_initial")
        else:
            try:
                last_dt = dt.datetime.fromisoformat(last_digest)
                elapsed = (now - last_dt).total_seconds() / 60
                if elapsed >= digest_minutes:
                    reasons.append(f"digest_interval:{int(elapsed)}m")
            except Exception:
                reasons.append("digest_state_reset")

    return (len(reasons) > 0, reasons)


def main() -> int:
    ap = argparse.ArgumentParser(description="Auto trigger decision helper")
    ap.add_argument("--root", default=".")
    ap.add_argument("--guild-id", required=True)
    ap.add_argument("--channel-id", required=True)
    ap.add_argument("--chars", type=int, required=True)
    ap.add_argument("--threshold", type=int, default=10000)
    ap.add_argument("--digest-minutes", type=int, default=360)
    ap.add_argument("--remember", action="store_true")
    args = ap.parse_args()

    now = utcnow()
    est = estimate_tokens(args.chars)

    st_path = state_path(Path(args.root), args.guild_id, args.channel_id)
    st = load_state(st_path)

    trigger, reasons = should_trigger(
        now,
        st,
        remember=args.remember,
        est_tokens=est,
        threshold=args.threshold,
        digest_minutes=args.digest_minutes,
    )

    out = {
        "trigger": trigger,
        "reasons": reasons,
        "estimated_tokens": est,
        "threshold": args.threshold,
        "stateFile": str(st_path),
        "now": now.isoformat(),
    }

    if trigger:
        st["lastDigestAt"] = now.isoformat()
        st["lastEstimatedTokens"] = est
        st["lastReasons"] = reasons
        save_state(st_path, st)

    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
