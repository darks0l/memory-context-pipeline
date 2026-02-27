#!/usr/bin/env python3
"""Check OpenClaw config for >10k compaction enforcement posture."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def get(d: dict, path: list[str], default=None):
    cur = d
    for k in path:
        if not isinstance(cur, dict) or k not in cur:
            return default
        cur = cur[k]
    return cur


def main() -> int:
    p = argparse.ArgumentParser(description="Check 10k compaction enforcement status")
    p.add_argument("--config", required=True, help="Path to openclaw.json")
    args = p.parse_args()

    cfg = json.loads(Path(args.config).read_text(encoding="utf-8"))

    mf = get(cfg, ["agents", "defaults", "compaction", "memoryFlush"], {}) or {}
    enabled = bool(mf.get("enabled", False))
    threshold = int(mf.get("softThresholdTokens", 0) or 0)

    out = {
        "memoryFlushEnabled": enabled,
        "softThresholdTokens": threshold,
        "enforcementMode": "soft" if enabled else "off",
        "recommendation": "Use router+auto-trigger path for practical hard behavior above 10k." if enabled else "Enable compaction.memoryFlush with 10k soft threshold.",
    }
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
