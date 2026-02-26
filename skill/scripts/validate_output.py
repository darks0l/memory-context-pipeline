#!/usr/bin/env python3
import argparse
import json
import sys

REQUIRED_KEYS = [
    "summary_short",
    "summary_full",
    "memory_candidates",
    "drop_candidates",
    "risk_flags",
    "needs_premium_review",
]


def main(path: str) -> int:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    missing = [k for k in REQUIRED_KEYS if k not in data]
    if missing:
        print(json.dumps({"ok": False, "missing": missing}, indent=2))
        return 1

    if not isinstance(data["memory_candidates"], list):
        print(json.dumps({"ok": False, "error": "memory_candidates must be array"}, indent=2))
        return 1

    print(json.dumps({"ok": True}, indent=2))
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate worker JSON contract")
    parser.add_argument("--input", required=True, help="Path to JSON output")
    args = parser.parse_args()
    sys.exit(main(args.input))
