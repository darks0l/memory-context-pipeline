# Release Notes - v1.1.1

## Added

- `skill/scripts/auto_trigger.py`
  - Auto-trigger decisions for channel-memory writes using:
    - context-length threshold
    - explicit remember intent
    - periodic digest interval
  - Per-channel trigger state file for throttling and consistency

- `docs/AUTO_TRIGGERS.md`
- `examples/auto-trigger-example.ps1`

## Improved

- Clarified automation flow from trigger decision -> memory append
- Strengthened practical path toward fully automatic channel organization
