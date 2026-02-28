# memory-context-pipeline

![DARKSOL](./assets/darksol-logo.svg)
Built by DARKSOL 🌑

Local-model memory/context pipeline for OpenClaw that keeps premium reasoning on the main chat path while offloading summarization and memory extraction.

![release](https://img.shields.io/badge/release-v1.2.1-informational)
![license](https://img.shields.io/badge/license-MIT-green)
![python](https://img.shields.io/badge/python-3.10%2B-blue)

## Why this exists
Long-running assistant sessions accumulate expensive context. This project adds an offload path so local workers can summarize, compress, and extract memory candidates while premium models stay focused on high-value user-facing reasoning.

## What it does
- Adds a reusable OpenClaw skill package (`skill/`)
- Provides JSON output contract + validation scripts
- Supports auto-trigger checks around context-size thresholds
- Stores optional per-channel memory records
- Includes one-command orchestrator for trigger -> route -> conditional write
- Ships docs/examples for practical integration

## Quickstart
```bash
# from repo root
python skill/scripts/validate_output.py --input examples/sample-output.json
python skill/scripts/validate_vision_tasks.py
```

```bash
# orchestrate one full cycle
python skill/scripts/orchestrate_memory_cycle.py --root . --guild-id <gid> --channel-id <cid> --task summarize --chars 25000
```

## Real example(s)
```bash
# decide whether context should trigger memory flow
python skill/scripts/auto_trigger.py --guild-id <gid> --channel-id <cid> --chars 25000

# write channel memory record when trigger=true
python skill/scripts/channel_memory_store.py --guild-id <gid> --channel-id <cid> --text "Summarized key decisions"
```

## Config/options
| Script | Key args | Description |
|---|---|---|
| `auto_trigger.py` | `--guild-id`, `--channel-id`, `--chars` | Decides whether threshold conditions should trigger pipeline work |
| `context_router.py` | task/context args | Maps task class to local/premium routing decision |
| `channel_memory_store.py` | `--guild-id`, `--channel-id`, `--text` | Persists memory snippets into channel-scoped files |
| `orchestrate_memory_cycle.py` | `--root`, `--guild-id`, `--channel-id`, `--task`, `--chars` | End-to-end orchestration helper |
| `validate_output.py` | `--input` | Validates output against contract |
| `enforcement_check.py` | `--config` | Verifies policy wiring against OpenClaw config |

## Architecture / flow
- Trigger logic evaluates context size (`auto_trigger.py`)
- Router determines suitable execution path (`context_router.py`)
- Worker output is validated against JSON contract (`skill/references/output_contract.json`)
- Memory records are optionally written by channel/day (`channel_memory_store.py`)
- Orchestrator script can chain the full flow in one command

## Performance notes
No benchmark numbers are claimed in this repo. Gains depend on your local model choice, hardware, and traffic shape.

## Limitations + roadmap
### Current limitations
- Focused on OpenClaw integration patterns, not a standalone hosted service
- Quality of summaries/extractions depends on local model behavior
- Threshold trigger is intentionally a soft guard, not a hard cutoff

### Roadmap
- Broader policy templates for different deployment risk profiles
- More examples for mixed text/vision routing
- Additional end-to-end integration tests

## Security notes
- Do not store secrets in memory files.
- Validate config before enabling automated writes in shared environments.

## License + links
- License: MIT
- Architecture docs: `docs/ARCHITECTURE.md`
- Validation notes: `docs/VALIDATION.md`
- Release notes: `docs/RELEASE_NOTES_*.md`
- GitHub: <https://github.com/darks0l/memory-context-pipeline>
