# SFX cue file schema

```json
{
  "original_audio_gain_db": -3,
  "cues": [
    {
      "file": "audio/paper-swipe.wav",
      "at": 1.24,
      "gain_db": -8,
      "trim_start": 0.1,
      "duration": 0.65,
      "fade_in": 0.01,
      "fade_out": 0.08
    }
  ]
}
```

Paths are resolved relative to the cue JSON file. Times and durations are in
seconds; gains are in decibels. `trim_start`, `duration`, `fade_in` and
`fade_out` are optional. `at` and `file` are required. Negative timecodes and
non-positive durations are rejected.

Keep the rights log separate from this machine-readable mix file. The cue file
describes the edit; the rights log describes provenance and permission.
