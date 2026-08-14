# Motion production contract

Use this contract as the stable source of truth across planning, rendering and QA.

```json
{
  "project": {"slug": "", "title": "", "purpose": "", "audience": ""},
  "takeaway": "",
  "source_copy": "",
  "claims": [
    {"id": "claim-1", "text": "", "source": "", "status": "user_supplied_unverified", "approval": "required"}
  ],
  "delivery": {
    "duration_seconds": 20,
    "fps": 30,
    "formats": [
      {"id": "vertical", "width": 1080, "height": 1920},
      {"id": "portrait", "width": 1080, "height": 1350},
      {"id": "landscape", "width": 1920, "height": 1080},
      {"id": "square", "width": 1080, "height": 1080}
    ],
    "codec": "h264",
    "audio": "optional",
    "captions": "caption-safe",
    "reduced_motion": true
  },
  "brand": {
    "source": "",
    "logo": "",
    "font": "",
    "fallback_font": "",
    "colours": {"ground": "", "ink": "", "muted": "", "accent": ""},
    "forbidden": []
  },
  "review_gates": {
    "claims": "required",
    "storyboard": "required",
    "brand": "required",
    "final": "required"
  }
}
```

Allowed claim statuses: `verified`, `user_supplied_unverified`, `superseded`, `withdrawn`.
Keep the underlying source or a durable source reference with the project; a search result is not a source record.
