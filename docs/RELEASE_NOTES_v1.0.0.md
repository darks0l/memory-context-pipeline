# Release Notes - v1.0.0

## Added

- Initial `memory-context-pipeline` skill
- Router script (`context_router.py`)
- Output validator (`validate_output.py`)
- Worker prompt reference
- JSON schema output contract
- Config template for local/premium routing
- Packaged skill artifact support (`.skill`)

## Operational changes

- Discord thread-bound subagent spawn support configured
- Automatic memory flush compaction policy configured at 10k soft threshold

## Recommended model strategy

- Fast path: `lfm2`
- High-quality local pass (if hardware allows): `qwen3.5:35b`

## Known limitations

- 10k behavior is a soft compaction threshold, not a hard token firewall
- Full automation quality depends on local model health/latency
