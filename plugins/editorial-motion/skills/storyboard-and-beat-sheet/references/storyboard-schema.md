# Renderer-neutral storyboard schema

Top-level fields:

```json
{
  "schema_version": "1.0",
  "fps": 30,
  "duration_frames": 600,
  "takeaway": "",
  "beats": []
}
```

Each beat:

```json
{
  "id": "proof",
  "start_frame": 180,
  "end_frame": 360,
  "function": "proof",
  "screen_copy": ["71%", "want an opt-in for algorithms"],
  "narration": "",
  "before": "phone image and question",
  "after": "100 marks with 71 emphasised",
  "focal_object": "percentage field",
  "persistent_objects": ["phone-frame"],
  "continuity_action": "phone-frame becomes the denominator field",
  "motion": {
    "register": "eased",
    "path": "short-arc",
    "distance_px_at_1080": 24,
    "duration_frames": 24,
    "stagger_frames": 12,
    "hold_frames": 90,
    "easing": "cubic-out"
  },
  "image": {"asset_id": "", "treatment": "", "crop_anchor": ""},
  "data": {"value": 71, "denominator": 100, "unit": "per cent", "encoding": "100 marks"},
  "sound": {"role": "impact", "sync_frame": 210, "required": false},
  "reduced_motion": {"substitute": "static 100-mark grid with 71 highlighted"},
  "evidence": "user-supplied claim",
  "interpretation": "the percentage is the proof beat",
  "recommendation": "make 71 of 100 countable",
  "approval": "awaiting_claim_source"
}
```

Rules:

- `start_frame` is inclusive and `end_frame` is exclusive.
- Beats must be ordered and cannot overlap.
- Gaps are allowed only when explicitly marked as deliberate silence or empty-frame punctuation.
- The final beat must end at `duration_frames`.
- Motion measurements use the master 1080-wide canvas and scale proportionally for other formats.
