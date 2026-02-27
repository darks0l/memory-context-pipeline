# Validation + Tuning (v1.2)

This doc tracks three outcomes:

1. Vision task routing validation
2. Confidence threshold tuning guidance
3. >10k enforcement posture checks

## 1) Vision routing validation

Run:

```bash
python skill/scripts/validate_vision_tasks.py
```

Expected:
- route = `local`
- model = `qwen3-vl`
- decision trace contains `multimodal_branch`

## 2) Confidence threshold tuning

Recommended starting values:
- `candidate_min_confidence_text`: 0.72
- `candidate_min_confidence_vision`: 0.78

Raise thresholds when:
- hallucination flags increase
- OCR extraction quality drifts

Lower slightly when:
- high false-negative rejection
- too many premium escalations on obviously correct outputs

## 3) >10k enforcement checks

Run:

```bash
python skill/scripts/enforcement_check.py --config C:\\Users\\favcr\\.openclaw\\openclaw.json
```

Interpretation:
- `enforcementMode=soft`: compaction is active but not a strict firewall
- practical hard behavior is achieved by routing + auto-trigger policies above threshold
