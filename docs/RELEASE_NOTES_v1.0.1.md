# Release Notes - v1.0.1

## Changed

- Clarified 10k behavior as a **soft compaction threshold** (not a hard cap)
- Added practical model guidance for choosing `lfm2` vs `qwen3.5:35b`
- Added Windows `gh` CLI path note for environments where GitHub CLI is installed but not on PATH

## Why this matters

- Prevents confusion about strict token limits
- Helps operators pick the best local model for speed vs quality
- Reduces friction when publishing releases from Windows hosts
