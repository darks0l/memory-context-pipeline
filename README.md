# Memory Context Pipeline for OpenClaw

Local-model memory/context pipeline that keeps premium reasoning in the main chat and offloads compression + memory extraction to a sub-agent.

## What this gives you

- Premium model stays focused on high-value reasoning
- Automatic context compaction around a 10k-token **soft** threshold
- Local worker (`lfm2` by default) for summarize/compress/extract tasks
- Strict JSON output contract for predictable downstream handling
- Reusable skill package for other OpenClaw users

## Important behavior note

- `10k` is a **soft compaction trigger**, not a hard firewall.
- The system will flush/compact context around the threshold to keep premium context lean.
- You can still explicitly request full context when needed.

## Repo layout

- `skill/` - drop-in OpenClaw skill
- `docs/` - setup, architecture, release notes
- `examples/` - config + output examples

## Channel organization (v1.1)

Optional lean channel-memory layout is now included:

- `memory/channels/<guild_id>/<channel_id>/YYYY-MM-DD.md`
- `memory/channels/<guild_id>/<channel_id>/summaries/YYYY-Www.md`

Writer utility:

```bash
python skill/scripts/channel_memory_store.py --guild-id <gid> --channel-id <cid> --text "..."
```

Use it on compaction events, explicit "remember this" requests, or periodic digest cadence.

## Auto-trigger support (v1.1.1)

Automation helper added:

```bash
python skill/scripts/auto_trigger.py --guild-id <gid> --channel-id <cid> --chars <char_count>
```

If `trigger=true`, then run `channel_memory_store.py` to append records.

This preserves original intent: automatic operation when context grows beyond threshold.

## One-command orchestrator (v1.2.1)

Run full cycle in one command:

```bash
python skill/scripts/orchestrate_memory_cycle.py --root . --guild-id <gid> --channel-id <cid> --task summarize --chars 25000
```

This chains: trigger decision -> routing decision -> conditional memory write.

## Quick start

1. Copy/install skill contents from `skill/` into `~/.openclaw/skills/memory-context-pipeline`.
2. Apply the policy example from `examples/openclaw-config.patch.json`.
3. Restart gateway.
4. Spawn worker session (optional persistent mode):

```json
{
  "task": "You are memory-worker...",
  "label": "memory-worker",
  "model": "lfm2",
  "mode": "session",
  "thread": true
}
```

## Recommended models

- **Default fast path (text):** `lfm2` (`ollama/lfm2:latest`)
- **Vision-aware path (multimodal):** `qwen3-vl` (`ollama/qwen3-vl:latest`)

### Hardware guidance (practical)

- **lfm2 (24B):** best for low-latency summarize/compress/extract flows
- **qwen3-vl (8.8B):** best for image+text understanding, OCR-like extraction, and visual context notes

Rule of thumb:
- If task is text-only and speed matters -> `lfm2`
- If task includes images/screenshots/docs -> `qwen3-vl:latest`

## Suggested routing policy

- Route local when:
  - task type is summarize/compress/extract-memory-candidates/dedupe-notes
  - estimated input >= 10k tokens
- Keep premium for strategic decisions and user-facing final reasoning
- Escalate to premium review only when risk flags/low confidence exist

## Validation

```bash
python skill/scripts/validate_output.py --input examples/sample-output.json
python skill/scripts/validate_vision_tasks.py
python skill/scripts/enforcement_check.py --config C:\\Users\\favcr\\.openclaw\\openclaw.json
```

## Windows publishing note

If `gh` is installed but not in PATH, use full path:

```powershell
& "C:\Program Files\GitHub CLI\gh.exe" auth status
```

## License

MIT
