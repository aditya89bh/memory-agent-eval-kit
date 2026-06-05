"""Dependency-free SVG benchmark visualizations."""

from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any

DEFAULT_VISUAL_DIR = Path("assets/benchmark_visuals")


def generate_visual_assets(
    report_path: Path = Path("reports/results.json"),
    leaderboard_path: Path = Path("leaderboards/results.json"),
    output_dir: Path = DEFAULT_VISUAL_DIR,
) -> list[Path]:
    """Generate benchmark summary, category, and leaderboard SVG charts."""

    output_dir.mkdir(parents=True, exist_ok=True)
    report = _load_json(report_path)
    leaderboard = _load_json(leaderboard_path) if leaderboard_path.exists() else []
    paths = [
        output_dir / "category_score_chart.svg",
        output_dir / "leaderboard_chart.svg",
        output_dir / "benchmark_summary_chart.svg",
    ]
    paths[0].write_text(_category_chart(report), encoding="utf-8")
    paths[1].write_text(_leaderboard_chart(leaderboard), encoding="utf-8")
    paths[2].write_text(_summary_chart(report), encoding="utf-8")
    return paths


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _category_chart(report: dict[str, Any]) -> str:
    breakdown = report.get("category_breakdown", {})
    rows = [
        (str(category), float(values.get("score", 0.0)))
        for category, values in sorted(breakdown.items())
        if isinstance(values, dict)
    ]
    return _bar_chart("Category Scores", rows, width=900)


def _leaderboard_chart(leaderboard: Any) -> str:
    entries = leaderboard if isinstance(leaderboard, list) else []
    rows = [
        (str(entry.get("agent_name", "agent")), float(entry.get("overall_score", 0.0)))
        for entry in entries
        if isinstance(entry, dict)
    ]
    return _bar_chart("Leaderboard Overall Scores", rows, width=700)


def _summary_chart(report: dict[str, Any]) -> str:
    metrics = report.get("metrics", {})
    rows = [
        ("Overall", float(metrics.get("overall_score", 0.0))),
        ("Recall", float(metrics.get("recall_accuracy", 0.0))),
        ("Forgetting", float(metrics.get("forgetting_accuracy", 0.0))),
        ("Poisoning", float(metrics.get("poisoning_resistance", 0.0))),
        ("Timeline", float(metrics.get("timeline_reasoning_accuracy", 0.0))),
        ("Drift", float(metrics.get("drift_accuracy", 0.0))),
    ]
    return _bar_chart("Benchmark Summary", rows, width=760)


def _bar_chart(title: str, rows: list[tuple[str, float]], *, width: int) -> str:
    bar_height = 22
    gap = 12
    left = 190
    max_bar = width - left - 80
    height = 80 + max(1, len(rows)) * (bar_height + gap)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        'viewBox="0 0 {width} {height}" role="img">'.format(width=width, height=height),
        "<style>text{font-family:Inter,Arial,sans-serif}.title{font-size:22px;font-weight:700}"
        ".label{font-size:13px}.value{font-size:12px;fill:#334155}.bar{fill:#6366f1}"
        ".bg{fill:#eef2ff}</style>",
        f'<text class="title" x="24" y="36">{html.escape(title)}</text>',
    ]
    if not rows:
        parts.append('<text class="label" x="24" y="72">No data available</text>')
    for index, (label, value) in enumerate(rows):
        y = 64 + index * (bar_height + gap)
        clamped = max(0.0, min(1.0, value))
        bar_width = max_bar * clamped
        parts.extend(
            [
                f'<text class="label" x="24" y="{y + 16}">{html.escape(label)}</text>',
                _rect("bg", left, y, max_bar, bar_height),
                _rect("bar", left, y, bar_width, bar_height),
                _text("value", left + max_bar + 12, y + 16, f"{value * 100:.0f}%"),
            ]
        )
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def _rect(css_class: str, x: float, y: float, width: float, height: float) -> str:
    return (
        f'<rect class="{css_class}" x="{x}" y="{y}" width="{width:.1f}" '
        f'height="{height:.1f}" rx="5"/>'
    )


def _text(css_class: str, x: float, y: float, value: str) -> str:
    return f'<text class="{css_class}" x="{x:.1f}" y="{y:.1f}">{html.escape(value)}</text>'
