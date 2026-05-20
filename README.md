# Local Gemma 4 Content Radar

Local Gemma 4 Content Radar is a small editorial intelligence demo for the
DEV Gemma 4 Challenge. It uses a local Gemma 4 model through Ollama to compare
a batch of content signals and produce a structured publishing decision report.

The project is intentionally simple: no cloud API key, no external database, and
no private source text leaving the machine by default.

## Why This Exists

Content teams, indie builders, and cross-border media operators often collect
many weak signals: article ideas, social trends, competitor claims, risk notes,
and audience hooks. The hard part is not generating one more idea. The hard part
is deciding which idea deserves attention, why it matters now, and how to frame
it responsibly.

Gemma 4 is useful here because the model can reason across a long batch of
signals locally. That makes it a good fit for private editorial workflows where
drafts, screenshots, notes, or client material should not be sent to a hosted
API just to decide what to publish next.

## Demo

Prerequisites:

- Ollama running locally
- A Gemma 4 model available as `gemma4:e4b`, or pass another model with `--model`
- Python 3.10+

Run the sample radar:

```bash
python3 scripts/content_radar.py examples/signals.json \
  --out examples/radar-output.json \
  --markdown examples/radar-output.md
```

The script sends the candidate signals to local Ollama:

```text
http://127.0.0.1:11434/api/generate
```

Example output is included in:

- `examples/radar-output.json`
- `examples/radar-output.md`

## How It Uses Gemma 4

This demo uses `gemma4:e4b` locally through Ollama.

Model details from the local setup:

- Architecture: `gemma4`
- Effective parameters: `8.0B`
- Context length: `131072`
- Capabilities reported by Ollama: completion, vision, audio, tools, thinking
- License: Apache License 2.0

I chose E4B because this project values accessibility and privacy over raw
benchmark chasing. The goal is to show a useful workflow that can run on a local
machine and still perform meaningful ranking, synthesis, and risk-aware
editorial planning.

## Project Shape

```text
.
+-- examples/
|   +-- signals.json
|   +-- radar-output.json
|   +-- radar-output.md
+-- scripts/
|   +-- content_radar.py
+-- assets/
    +-- hero.svg
    +-- hero.png
```

## Notes

The example signals are intentionally lightweight so the repository is easy to
inspect. In a real workflow, the same pattern can be extended to compare larger
source batches, long research notes, screenshots, draft outlines, or
pre-publication risk checks.

## License

MIT
