# Optimization Study

Once the baseline model looked reasonable, I wanted to see which parts of the geometry were really doing the work and which parts only sounded important.

So I swept two variables:

- the residual gap in the engaged shunt path
- the cross-sectional area of the shunt

Those felt like the two parameters most likely to control the tradeoff between strong OFF-state suppression and safe shunt loading.

## What Changed Most

The residual gap was the clear winner.

Small changes there moved the OFF-state field a lot. That makes sense in hindsight because the shunt branch is dominated by the air-gap term anyway. Once the branch is in that regime, mechanical control matters more than trying to squeeze more performance out of the bulk permeability.

Shunt area still mattered, but in a calmer way. Increasing it improved saturation margin and helped suppression, just not as dramatically as reducing the residual gap.

## Best Point In The Current Sweep

The strongest safe point from the current run is `0.05 mm` gap and `50 mm^2` shunt area.

At that point, the model gives:

- `0.018 T` in the output gap in the OFF state
- `97.8%` field reduction
- `0.545 T` in the shunt

Numerically, that is excellent.

## Why I Did Not Replace The Baseline

Even though the tighter geometry wins on paper, I still think the baseline is the better first build:

- `0.10 mm` engaged gap
- `37 mm^2` shunt area
- `94.4%` field reduction
- `0.711 T` in the shunt

The baseline gives up some suppression, but it asks less from the mechanical build. For a learning project, that feels like the more honest version of the design to carry forward.

## Top Candidates

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

## What I Learned

- The shunt gap is the real tuning knob.
- Bigger shunts help, but not enough to rescue a sloppy engaged gap.
- It is easy to drift into "best possible number" thinking. The more useful question is which geometry I would actually trust myself to build and test.

## Visualization

![Optimization map](../assets/optimization-map.svg)
