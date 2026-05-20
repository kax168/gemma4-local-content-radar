#!/usr/bin/env python3
"""Local Gemma 4 Content Radar.

This script sends a batch of candidate content signals to a local Gemma 4 model
through Ollama and asks it to produce a structured editorial decision report.
It is intentionally small, inspectable, and privacy-friendly: the model call
stays on localhost by default.
"""

from __future__ import annotations

import argparse
import json
import textwrap
import urllib.request
from pathlib import Path
from typing import Any


DEFAULT_MODEL = "gemma4:e4b"
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"


SYSTEM_PROMPT = """You are a local editorial intelligence model.
Analyze candidate content signals for an AI / cross-border growth media account.
Return strict JSON with:
- top_pick: title, why_now, audience_hook, risk_notes
- ranked_candidates: list of title, score_0_100, angle, evidence
- safe_summary: concise summary that avoids leaking private credentials
- next_actions: 3 practical steps
Prefer useful, current, specific topics over generic AI hype.
"""


def load_signals(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("signals file must be a JSON list")
    return data


def build_prompt(signals: list[dict[str, Any]]) -> str:
    return textwrap.dedent(
        f"""
        {SYSTEM_PROMPT}

        Candidate signals:
        {json.dumps(signals, ensure_ascii=False, indent=2)}

        Constraints:
        - Use Gemma 4's long-context reasoning to compare the whole batch.
        - Do not invent dates, sources, metrics, or quotes.
        - If evidence is weak, say so in risk_notes.
        - Output JSON only.
        """
    ).strip()


def call_ollama(prompt: str, model: str) -> str:
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.2},
    }
    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["response"]


def parse_json_response(response: str) -> dict[str, Any]:
    cleaned = response.strip()
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        cleaned = "\n".join(lines).strip()
    return json.loads(cleaned)


def write_markdown_report(report: dict[str, Any], path: Path) -> None:
    top_pick = report["top_pick"]
    ranked = report["ranked_candidates"]
    actions = report["next_actions"]
    lines = [
        "# Local Gemma 4 Content Radar Output",
        "",
        f"## Top Pick: {top_pick['title']}",
        "",
        f"**Why now:** {top_pick['why_now']}",
        "",
        f"**Audience hook:** {top_pick['audience_hook']}",
        "",
        f"**Risk notes:** {top_pick['risk_notes']}",
        "",
        "## Ranked Candidates",
        "",
    ]
    for item in ranked:
        lines.extend(
            [
                f"### {item['score_0_100']}/100 - {item['title']}",
                "",
                f"- Angle: {item['angle']}",
                f"- Evidence: {item['evidence']}",
                "",
            ]
        )
    lines.extend(["## Safe Summary", "", report["safe_summary"], "", "## Next Actions", ""])
    lines.extend(f"- {action}" for action in actions)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Rank content ideas with local Gemma 4")
    parser.add_argument("signals", type=Path, help="JSON file containing candidate signals")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Ollama model name")
    parser.add_argument("--out", type=Path, default=Path("examples/radar-output.json"))
    parser.add_argument("--markdown", type=Path, default=Path("examples/radar-output.md"))
    args = parser.parse_args()

    signals = load_signals(args.signals)
    response = call_ollama(build_prompt(signals), args.model)
    report = parse_json_response(response)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_markdown_report(report, args.markdown)
    print(
        json.dumps(
            {
                "model": args.model,
                "signals": len(signals),
                "out": str(args.out),
                "markdown": str(args.markdown),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
