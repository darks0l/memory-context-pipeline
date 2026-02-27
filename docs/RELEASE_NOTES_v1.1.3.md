# Release Notes v1.1.3

## Added
- Deterministic multimodal branch in `context_router.py`
  - `--has-image` flag for explicit image-bearing turns
  - vision task routing (`image-caption`, `screenshot-summary`, `ocr-extract`)
  - route output now includes `model`, `fallback_chain`, `confidence`, and `decision_trace`

## Improved
- Default local fallback behavior now explicit: local (`lfm2`) -> premium (`opus`) for local-routed turns
- Router output now includes `needs_premium_review` signal for low-confidence paths

## Tests
- Added unit tests for routing behavior in `tests/test_context_router.py`
  - premium default path
  - local task path
  - token threshold trigger
  - image/vision routing paths
