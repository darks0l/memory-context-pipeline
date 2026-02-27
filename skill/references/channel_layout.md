# Channel Memory Layout (v1.1)

Lean filesystem organization:

- `memory/channels/<guild_id>/<channel_id>/YYYY-MM-DD.md`
- `memory/channels/<guild_id>/<channel_id>/summaries/YYYY-Www.md`

## Write triggers

Write only when one of these occurs:
- Context compaction/memory flush event
- Explicit user request to remember
- Periodic digest cadence (recommended: every 6h or every ~100 messages)

## Why this layout

- append-only writes
- easy forensic/debug review by channel
- low retrieval noise by scoped path filtering
