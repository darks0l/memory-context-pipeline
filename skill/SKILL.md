---
name: memory-context-pipeline
description: Build and run a local-model memory/context pipeline that keeps premium models on the main chat path while offloading summarization, compression, and memory-candidate extraction to a spawned sub-agent. Use when designing routing thresholds, creating JSON output contracts, or packaging a reusable drop-in memory pipeline for OpenClaw.
---

# Memory Context Pipeline

Create a split-path architecture:
- Keep the main conversation on premium models.
- Spawn a local/cheap sub-agent only for context compression and memory prep.

## Workflow

1. Define routing policy with deterministic thresholds.
2. Run local worker prompt for compression/memory extraction.
3. Validate worker output against a strict JSON contract.
4. Escalate only flagged/uncertain items to premium review.

## 1) Routing Policy

Use `scripts/context_router.py` to make predictable routing decisions.

Default policy:
- Route to local worker when estimated input tokens >= 10000.
- Route to local worker for task types: `summarize`, `compress`, `extract-memory-candidates`, `dedupe-notes`.
- Keep premium path for strategic reasoning and high-stakes decisions.

Example:
```bash
python scripts/context_router.py --task summarize --chars 52000
```

## 2) Local Worker Prompt

Use `references/worker_prompt.md` as the sub-agent task prompt.

Recommended spawn model aliases:
- `lfm2` (fast local)
- `qwen` (higher local depth when needed)

Use `lfm2` as default if latency matters.

## 3) Output Contract

Require worker output to match `references/output_contract.json`.

Validate with:
```bash
python scripts/validate_output.py --input result.json
```

Required keys:
- `summary_short`
- `summary_full`
- `memory_candidates[]`
- `drop_candidates[]`
- `risk_flags[]`
- `needs_premium_review`

## 4) Escalation Rules

Escalate to premium review when any is true:
- `needs_premium_review == true`
- any memory candidate confidence < configured threshold
- `risk_flags` contains hallucination or ambiguity

Keep escalation minimal; do not replace the premium main path.

## Configuration Template

Use `references/pipeline_config.example.json` as baseline defaults.

Suggested defaults:
- summarize threshold: 10000 tokens
- local model: `lfm2`
- premium model: `opus`
- candidate minimum confidence: 0.72
- fail mode: `graceful_skip`

## 5) Channel Memory Organization (Optional, v1.1)

Use `scripts/channel_memory_store.py` to maintain lean per-channel logs:
- `memory/channels/<guild>/<channel>/YYYY-MM-DD.md`
- `memory/channels/<guild>/<channel>/summaries/YYYY-Www.md`

Recommended write triggers:
- compaction flush
- explicit "remember this"
- periodic digest cadence

## Notes

- Favor deterministic routing over hidden heuristics.
- Keep the local worker narrow (compression/extraction), not broad reasoning.
- Preserve privacy: redact sensitive snippets before storing long-term memory.
- Avoid per-message overlogging; summarize on meaningful checkpoints.