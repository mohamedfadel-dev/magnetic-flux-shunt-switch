#!/usr/bin/env python3
"""Sweep key parameters and generate optimization artifacts for the case study."""

from __future__ import annotations

from pathlib import Path

from reluctance_calculator import BASELINE, SHUNT_B_DESIGN_LIMIT, evaluate_design


ROOT = Path(__file__).resolve().parent.parent
DOC_PATH = ROOT / "docs" / "optimization-study.md"
SVG_PATH = ROOT / "assets" / "optimization-map.svg"


def score(result: dict[str, float]) -> float:
    reduction_weight = result["reduction"] * 100.0
    on_field_bonus = min(result["b_on"], 1.0) * 8.0
    saturation_penalty = max(0.0, result["b_shunt"] - SHUNT_B_DESIGN_LIMIT) * 180.0
    return reduction_weight + on_field_bonus - saturation_penalty


def fmt_mm2(area_m2: float) -> str:
    return f"{area_m2 * 1e6:.0f}"


def fmt_mm(length_m: float) -> str:
    return f"{length_m * 1e3:.2f}"


def run_sweep() -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for gap_mm in [0.05, 0.08, 0.10, 0.12, 0.15, 0.20, 0.25]:
        for area_mm2 in [28, 31, 34, 37, 40, 45, 50]:
            params = dict(BASELINE)
            params["shunt_gap"] = gap_mm * 1e-3
            params["shunt_area"] = area_mm2 * 1e-6
            result = evaluate_design(**params)
            rows.append(
                {
                    "gap_mm": gap_mm,
                    "area_mm2": area_mm2,
                    "b_on": result["b_on"],
                    "b_off": result["b_off"],
                    "b_shunt": result["b_shunt"],
                    "reduction_pct": result["reduction"] * 100.0,
                    "score": score(result),
                }
            )
    rows.sort(key=lambda row: row["score"], reverse=True)
    return rows


def generate_markdown(rows: list[dict[str, float]]) -> str:
    best = rows[0]
    baseline = next(
        row for row in rows if row["gap_mm"] == 0.10 and row["area_mm2"] == 37
    )
    best_safe = next(row for row in rows if row["b_shunt"] <= SHUNT_B_DESIGN_LIMIT)

    top_rows = rows[:10]

    lines = [
        "# Optimization Study",
        "",
        "This study explores how the flux-shunt switch responds to changes in two practical design variables:",
        "",
        "- engaged shunt residual gap",
        "- mu-metal shunt cross-sectional area",
        "",
        "The goal is to keep the ON state strong, suppress the OFF state aggressively, and avoid pushing the shunt past the conservative saturation ceiling used in the project.",
        "",
        "## Key Findings",
        "",
        f"- Best overall score in the sweep: `gap = {best['gap_mm']:.2f} mm`, `area = {best['area_mm2']:.0f} mm^2`.",
        f"- Best safe design under the `0.75 T` shunt limit: `gap = {best_safe['gap_mm']:.2f} mm`, `area = {best_safe['area_mm2']:.0f} mm^2`.",
        f"- Baseline design remains competitive: `gap = {baseline['gap_mm']:.2f} mm`, `area = {baseline['area_mm2']:.0f} mm^2`.",
        "",
        "## Interpretation",
        "",
        "- Residual shunt gap is the dominant control variable. Small increases in gap degrade OFF-state suppression quickly.",
        "- Increasing shunt area lowers shunt flux density and improves saturation margin, but with diminishing returns once the residual gap term dominates branch reluctance.",
        "- The baseline choice of `0.10 mm` engaged gap and `37 mm^2` area is a balanced point rather than a peak-only choice. That makes it a credible engineering selection for a portfolio project.",
        "",
        "## Top Candidate Designs",
        "",
        "| Rank | Gap (mm) | Area (mm^2) | ON B (T) | OFF B (T) | Reduction (%) | Shunt B (T) |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]

    for idx, row in enumerate(top_rows, start=1):
        lines.append(
            f"| {idx} | {row['gap_mm']:.2f} | {row['area_mm2']:.0f} | "
            f"{row['b_on']:.3f} | {row['b_off']:.3f} | {row['reduction_pct']:.1f} | {row['b_shunt']:.3f} |"
        )

    lines.extend(
        [
            "",
            "## Baseline Versus Best Safe Design",
            "",
            f"- Baseline: `OFF B = {baseline['b_off']:.3f} T`, `reduction = {baseline['reduction_pct']:.1f}%`, `shunt B = {baseline['b_shunt']:.3f} T`.",
            f"- Best safe: `OFF B = {best_safe['b_off']:.3f} T`, `reduction = {best_safe['reduction_pct']:.1f}%`, `shunt B = {best_safe['b_shunt']:.3f} T`.",
            "",
            "The best safe point in the sweep is slightly more aggressive than the baseline, but the baseline keeps the mechanical gap at a realistic tolerance target while preserving strong suppression performance.",
            "",
            "## Generated Visualization",
            "",
            "![Optimization map](../assets/optimization-map.svg)",
        ]
    )

    return "\n".join(lines) + "\n"


def generate_svg(rows: list[dict[str, float]]) -> str:
    width = 980
    height = 640
    left = 110
    top = 90
    chart_w = 760
    chart_h = 420
    min_gap = 0.05
    max_gap = 0.25
    min_area = 28
    max_area = 50

    safe_rows = [row for row in rows if row["b_shunt"] <= SHUNT_B_DESIGN_LIMIT]
    max_reduction = max(row["reduction_pct"] for row in safe_rows)
    min_reduction = min(row["reduction_pct"] for row in safe_rows)

    def x_pos(gap_mm: float) -> float:
        return left + ((gap_mm - min_gap) / (max_gap - min_gap)) * chart_w

    def y_pos(area_mm2: float) -> float:
        return top + chart_h - ((area_mm2 - min_area) / (max_area - min_area)) * chart_h

    def color_for(reduction_pct: float, safe: bool) -> str:
        if not safe:
            return "#c9cdd3"
        t = (reduction_pct - min_reduction) / (max_reduction - min_reduction or 1.0)
        red = int(222 - 112 * t)
        green = int(120 + 85 * t)
        blue = int(86 + 66 * t)
        return f"#{red:02x}{green:02x}{blue:02x}"

    best_safe = next(row for row in rows if row["b_shunt"] <= SHUNT_B_DESIGN_LIMIT)
    baseline = next(
        row for row in rows if row["gap_mm"] == 0.10 and row["area_mm2"] == 37
    )

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '  <rect width="100%" height="100%" fill="#f6f2ea"/>',
        '  <text x="70" y="55" font-family="Arial, Helvetica, sans-serif" font-size="30" fill="#1f2a44">Optimization Map</text>',
        '  <text x="70" y="82" font-family="Arial, Helvetica, sans-serif" font-size="18" fill="#55657a">Safe-region field reduction versus shunt residual gap and shunt area</text>',
        f'  <rect x="{left}" y="{top}" width="{chart_w}" height="{chart_h}" fill="#fffdf8" stroke="#cfd8e3" stroke-width="2"/>',
    ]

    for gap in [0.05, 0.10, 0.15, 0.20, 0.25]:
        x = x_pos(gap)
        parts.append(
            f'  <line x1="{x:.1f}" y1="{top}" x2="{x:.1f}" y2="{top + chart_h}" stroke="#e2e8f0" stroke-width="1"/>'
        )
        parts.append(
            f'  <text x="{x:.1f}" y="{top + chart_h + 28}" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="15" fill="#475569">{gap:.2f}</text>'
        )

    for area in [28, 34, 40, 45, 50]:
        y = y_pos(area)
        parts.append(
            f'  <line x1="{left}" y1="{y:.1f}" x2="{left + chart_w}" y2="{y:.1f}" stroke="#e2e8f0" stroke-width="1"/>'
        )
        parts.append(
            f'  <text x="{left - 18}" y="{y + 5:.1f}" text-anchor="end" font-family="Arial, Helvetica, sans-serif" font-size="15" fill="#475569">{area}</text>'
        )

    parts.extend(
        [
            f'  <text x="{left + chart_w / 2:.1f}" y="{top + chart_h + 60}" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="18" fill="#1f2a44">Engaged shunt residual gap (mm)</text>',
            f'  <text x="35" y="{top + chart_h / 2:.1f}" transform="rotate(-90 35 {top + chart_h / 2:.1f})" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="18" fill="#1f2a44">Shunt cross-sectional area (mm^2)</text>',
        ]
    )

    for row in rows:
        safe = row["b_shunt"] <= SHUNT_B_DESIGN_LIMIT
        x = x_pos(row["gap_mm"])
        y = y_pos(row["area_mm2"])
        color = color_for(row["reduction_pct"], safe)
        radius = 11 if safe else 8
        parts.append(
            f'  <circle cx="{x:.1f}" cy="{y:.1f}" r="{radius}" fill="{color}" stroke="#334155" stroke-width="1.2"/>'
        )

    for row, label, dy in [(baseline, "Baseline", -18), (best_safe, "Best safe", 24)]:
        x = x_pos(row["gap_mm"])
        y = y_pos(row["area_mm2"])
        parts.append(
            f'  <circle cx="{x:.1f}" cy="{y:.1f}" r="14" fill="none" stroke="#111827" stroke-width="2.2"/>'
        )
        parts.append(
            f'  <text x="{x + 18:.1f}" y="{y + dy:.1f}" font-family="Arial, Helvetica, sans-serif" font-size="16" fill="#111827">{label}</text>'
        )

    legend_x = 650
    legend_y = 540
    parts.append(
        f'  <rect x="{legend_x}" y="{legend_y - 26}" width="240" height="72" rx="10" fill="#fffdf8" stroke="#cfd8e3" stroke-width="1.5"/>'
    )
    parts.append(
        f'  <circle cx="{legend_x + 22}" cy="{legend_y}" r="10" fill="#87b6ac" stroke="#334155" stroke-width="1"/>'
    )
    parts.append(
        f'  <text x="{legend_x + 42}" y="{legend_y + 5}" font-family="Arial, Helvetica, sans-serif" font-size="15" fill="#334155">Safe design, higher reduction shown in darker green</text>'
    )
    parts.append(
        f'  <circle cx="{legend_x + 22}" cy="{legend_y + 28}" r="8" fill="#c9cdd3" stroke="#334155" stroke-width="1"/>'
    )
    parts.append(
        f'  <text x="{legend_x + 42}" y="{legend_y + 33}" font-family="Arial, Helvetica, sans-serif" font-size="15" fill="#334155">Grey point exceeds shunt design limit</text>'
    )
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def main() -> None:
    rows = run_sweep()
    DOC_PATH.write_text(generate_markdown(rows), encoding="utf-8")
    SVG_PATH.write_text(generate_svg(rows), encoding="utf-8")
    print(f"Wrote {DOC_PATH}")
    print(f"Wrote {SVG_PATH}")


if __name__ == "__main__":
    main()
