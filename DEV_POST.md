---
title: I Built a Local Gemma 4 Content Radar for Private Editorial Decisions
published: false
tags: devchallenge, gemmachallenge, gemma
---

*This is a submission for the [Gemma 4 Challenge: Build with Gemma 4](https://dev.to/challenges/google-gemma-2026-05-06).*

![Local Gemma 4 Content Radar hero](https://raw.githubusercontent.com/kax168/gemma4-local-content-radar/main/assets/hero.png?v=1)

## What I Built

I built **Local Gemma 4 Content Radar**, a small but practical editorial intelligence tool that runs Gemma 4 locally and turns a messy batch of content signals into a structured publishing decision report.

The problem I wanted to solve is simple: creators and technical media operators do not need one more random idea generator. They need a way to compare signals, choose the strongest angle, explain why it matters now, and flag risks before something gets published.

The tool takes a JSON file of candidate signals like trend notes, draft ideas, source snippets, audience hooks, or risk observations. It sends the full batch to a local Gemma 4 model through Ollama and returns:

- the strongest topic to pursue
- why that topic matters now
- a reader-facing hook
- ranked alternative candidates
- evidence notes
- risk notes
- practical next actions

The project is designed around privacy. The default endpoint is `http://127.0.0.1:11434/api/generate`, so the editorial notes stay on the local machine unless the user chooses otherwise.

## Demo

Repository:

https://github.com/kax168/gemma4-local-content-radar

Run it locally:

```bash
python3 scripts/content_radar.py examples/signals.json \
  --out examples/radar-output.json \
  --markdown examples/radar-output.md
```

Example output from Gemma 4 selected this top topic:

> Developers are testing local multimodal models for private document review

Gemma 4 explained that this is timely because teams increasingly want to process proprietary PDFs, screenshots, internal docs, and research notes without sending sensitive data to cloud APIs. It also produced a hook, risk notes, ranked alternatives, and follow-up actions.

That is the core user experience: local Gemma 4 acts as a private editorial reasoning layer, not just a text generator.

## Code

The implementation is intentionally small and inspectable.

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
```

The script does four things:

- loads candidate signals from JSON
- builds a prompt that asks for strict structured output
- calls local Ollama with Gemma 4
- writes both JSON and Markdown reports

I kept the project dependency-light on purpose. It uses Python's standard library so the workflow is easy to audit, clone, and adapt.

## How I Used Gemma 4

I used `gemma4:e4b` locally through Ollama.

From my local setup:

- Architecture: `gemma4`
- Effective parameters: `8.0B`
- Context length: `131072`
- Capabilities reported by Ollama: completion, vision, audio, tools, thinking
- License: Apache License 2.0

I chose E4B because this project is about practical local AI, not winning a benchmark screenshot. E4B is small enough to run locally, but capable enough to compare a batch of signals, rank competing angles, and explain the tradeoffs.

Gemma 4 is doing the central work here:

- long-context comparison across all candidate signals
- editorial prioritization
- hook generation
- risk-aware summarization
- next-step planning

The part I like most is that the model is not being used as a cloud chatbot bolted onto a workflow. It is the local reasoning engine at the center of the product.

## What Gemma 4 Unlocked

The useful unlock is privacy-friendly judgment.

For content operations, the sensitive material is often not a final article. It is the messy middle: private notes, early research, screenshots, customer language, internal docs, and unverified claims. Sending all of that to a hosted API is not always acceptable.

A local Gemma 4 workflow changes the shape of the product. It lets the user perform the first editorial pass on private material before anything is sanitized, summarized, or published.

That makes this pattern useful beyond content marketing. The same approach could support:

- private research triage
- local document review
- pre-publication safety checks
- creator workflow planning
- multilingual editorial planning
- internal knowledge synthesis

## What I Would Build Next

The next version would add a small browser UI, source importers, and an optional multimodal path where Gemma 4 can inspect screenshots or visual drafts before producing the editorial report.

I would also add a "claim hygiene" mode that forces every generated angle to include what is known, what is inferred, and what still needs verification.

For this submission, I wanted the core to be honest and reproducible: local model in, structured decision report out.
