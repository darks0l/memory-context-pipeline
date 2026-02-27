# Auto Triggers (v1.1.1)

This release adds an auto-trigger decision helper so channel memory writes can be reliably automated.

## Trigger conditions

- Estimated tokens >= threshold (default 10k)
- Explicit remember intent
- Digest interval elapsed (default 360 minutes)

## Scripts

- `skill/scripts/auto_trigger.py` -> decides whether to write
- `skill/scripts/channel_memory_store.py` -> appends daily + weekly memory files

## Suggested integration flow

1. Run `auto_trigger.py` at checkpoints (compaction event, message batch, periodic cadence)
2. If `trigger=true`, call `channel_memory_store.py`
3. Pass worker JSON when available to enrich weekly summaries

## Why this matters

- Removes manual dependency
- Prevents overlogging with state-based throttling
- Preserves original intent: automatic behavior based on context growth