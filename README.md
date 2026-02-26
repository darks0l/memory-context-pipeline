# Memory Context Pipeline for OpenClaw

Local-model memory/context pipeline that keeps premium reasoning in the main chat and offloads compression + memory extraction to a sub-agent.

## What this gives you

- Premium model stays focused on high-value reasoning
- Automatic context compaction around a 10k-token soft threshold
- Local worker (`lfm2` by default) for summarize/compress/extract tasks
- Strict JSON output contract for predictable downstream handling
- Reusable skill package for other OpenClaw users

## Repo layout

- `skill/` - drop-in OpenClaw skill
- `docs/` - setup, architecture, release notes
- `examples/` - config + output examples

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

- **Default fast path:** `lfm2` (`ollama/lfm2:24b`)
- **Heavier local path:** `qwen3.5:35b` when your host can handle larger VRAM/RAM demand

If your box can run qwen3.5 comfortably, use it for higher-quality compression passes and keep `lfm2` as low-latency fallback.

## Suggested routing policy

- Route local when:
  - task type is summarize/compress/extract-memory-candidates/dedupe-notes
  - estimated input >= 10k tokens
- Keep premium for strategic decisions and user-facing final reasoning
- Escalate to premium review only when risk flags/low confidence exist

## Validation

```bash
python skill/scripts/validate_output.py --input examples/sample-output.json
```

## License

MIT
