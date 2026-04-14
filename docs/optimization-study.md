# Optimization Study

This study explores how the flux-shunt switch responds to changes in two practical design variables:

- engaged shunt residual gap
- mu-metal shunt cross-sectional area

The goal is to keep the ON state strong, suppress the OFF state aggressively, and avoid pushing the shunt past the conservative saturation ceiling used in the project.

## Key Findings

- Best overall score in the sweep: `gap = 0.05 mm`, `area = 50 mm^2`.
- Best safe design under the `0.75 T` shunt limit: `gap = 0.05 mm`, `area = 50 mm^2`.
- Baseline design remains competitive: `gap = 0.10 mm`, `area = 37 mm^2`.

## Interpretation

- Residual shunt gap is the dominant control variable. Small increases in gap degrade OFF-state suppression quickly.
- Increasing shunt area lowers shunt flux density and improves saturation margin, but with diminishing returns once the residual gap term dominates branch reluctance.
- The baseline choice of `0.10 mm` engaged gap and `37 mm^2` area is a balanced point rather than a peak-only choice. That makes it a credible engineering selection for a portfolio project.

## Top Candidate Designs

| Rank | Gap (mm) | Area (mm^2) | ON B (T) | OFF B (T) | Reduction (%) | Shunt B (T) |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0.05 | 50 | 0.849 | 0.018 | 97.8 | 0.545 |
| 2 | 0.05 | 45 | 0.849 | 0.020 | 97.6 | 0.604 |
| 3 | 0.05 | 40 | 0.849 | 0.023 | 97.3 | 0.678 |
| 4 | 0.05 | 37 | 0.849 | 0.025 | 97.1 | 0.731 |
| 5 | 0.08 | 50 | 0.849 | 0.029 | 96.6 | 0.538 |
| 6 | 0.08 | 45 | 0.849 | 0.032 | 96.2 | 0.596 |
| 7 | 0.10 | 50 | 0.849 | 0.036 | 95.8 | 0.534 |
| 8 | 0.08 | 40 | 0.849 | 0.036 | 95.8 | 0.667 |
| 9 | 0.08 | 37 | 0.849 | 0.039 | 95.5 | 0.719 |
| 10 | 0.10 | 45 | 0.849 | 0.040 | 95.3 | 0.590 |

## Baseline Versus Best Safe Design

- Baseline: `OFF B = 0.048 T`, `reduction = 94.4%`, `shunt B = 0.711 T`.
- Best safe: `OFF B = 0.018 T`, `reduction = 97.8%`, `shunt B = 0.545 T`.

The best safe point in the sweep is slightly more aggressive than the baseline, but the baseline keeps the mechanical gap at a realistic tolerance target while preserving strong suppression performance.

## Generated Visualization

![Optimization map](../assets/optimization-map.svg)
