# Orchestrator (v1.2.1)

`orchestrate_memory_cycle.py` chains the full practical flow:

1. `auto_trigger.py` (should we write?)
2. `context_router.py` (which model path?)
3. `channel_memory_store.py` (append if triggered)

## Run

```bash
python skill/scripts/orchestrate_memory_cycle.py --root . --guild-id <gid> --channel-id <cid> --task summarize --chars 25000
```

Output includes `trigger`, `route`, and `stored` sections for easy automation plumbing.
