# Architecture

## Core principle

Split workloads by value:
- Premium model: deep reasoning + final user response quality
- Local worker: context compression, memory candidate extraction, cleanup

## Components

1. **Router policy**
   - Deterministic threshold + task-type checks
   - Implemented via `skill/scripts/context_router.py`

2. **Worker prompt**
   - Narrow scope (no broad strategic reasoning)
   - Implemented via `skill/references/worker_prompt.md`

3. **Output contract**
   - Strict JSON keys with confidence/risk markers
   - Implemented via `skill/references/output_contract.json`

4. **Compaction integration**
   - OpenClaw `compaction.memoryFlush` soft threshold at 10k tokens
   - Keeps premium context tight unless explicitly overridden

## Quality controls

- Candidate confidence threshold (example: 0.72)
- Risk flags force optional premium review
- Graceful skip if local worker unavailable

## Why this scales

- Portable config and skill package
- Local-first cost profile
- Predictable behavior due to deterministic routing