# Example usage for channel memory append helper
# Run from repo root

python .\skill\scripts\channel_memory_store.py `
  --root . `
  --guild-id 1476617419488497737 `
  --channel-id 1476718730624110602 `
  --text "Compaction event: summarized active design decisions." `
  --summary-json '{"summary_short":"Design decisions captured","memory_candidates":[{"text":"Use lfm2 default","confidence":0.92}],"risk_flags":[]}'
