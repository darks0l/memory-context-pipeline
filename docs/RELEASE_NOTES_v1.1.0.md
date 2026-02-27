# Release Notes - v1.1.0

## Added

- `skill/scripts/channel_memory_store.py` for automatic channel-scoped append logs
- `skill/references/channel_layout.md` documenting the lean folder structure
- `examples/channel-memory-example.ps1` for Windows usage

## Channel memory layout

- `memory/channels/<guild_id>/<channel_id>/YYYY-MM-DD.md`
- `memory/channels/<guild_id>/<channel_id>/summaries/YYYY-Www.md`

## Design intent

- Better long-run organization for active Discord environments
- Lower retrieval noise by scoping memory per channel
- Keep writes efficient via append-only + trigger-based events