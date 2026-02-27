# Auto-trigger decision (returns trigger=true/false + reasons)
python .\skill\scripts\auto_trigger.py `
  --root . `
  --guild-id 1476617419488497737 `
  --channel-id 1476718730624110602 `
  --chars 48000 `
  --threshold 10000 `
  --digest-minutes 360

# If trigger=true, call channel writer
python .\skill\scripts\channel_memory_store.py `
  --root . `
  --guild-id 1476617419488497737 `
  --channel-id 1476718730624110602 `
  --text "Auto-trigger flush: context compaction event"