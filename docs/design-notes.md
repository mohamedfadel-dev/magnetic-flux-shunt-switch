# Design Notes

## Problem Statement

Create a magnetic switching device in which the sensing field is controlled by changing the magnetic path rather than electrically energizing a coil. The desired output is a clear high-field state and low-field state at a compact output region suitable for a reed switch or Hall-effect sensor.

This document serves as the technical backbone for a completed mu-metal switching-circuit case study.

## Functional Principle

The switching element is a movable mu-metal shunt placed near the pole faces of a permanent-magnet circuit.

- When the shunt is `retracted`, the lowest available path for useful flux includes the output air gap.
- When the shunt is `inserted`, the high-permeability shunt bridges the poles and bypasses the output gap.

This is a reluctance-switching device. The moving element does not create flux. It changes which path the existing flux prefers.

That distinction matters because it changes both the performance envelope and the manufacturing risks. The engineering problem is not only to create a strong magnetic path, but to make the path change repeatable and reliable.

## Baseline Geometry

First-pass dimensions used for this case study:

| Parameter | Symbol | Value |
| --- | --- | --- |
| Magnet length | `l_m` | `5 mm` |
| Magnet area | `A_m` | `25 mm^2` |
| Magnet relative permeability | `mu_r,m` | `1.05` |
| Magnet coercive field | `H_c` | `850 kA/m` |
| Output gap length | `g_out` | `1.5 mm` |
| Output gap area | `A_out` | `25 mm^2` |
| Shunt effective gap | `g_sh` | `0.1 mm` |
| Shunt length | `l_sh` | `20 mm` |
| Shunt area | `A_sh` | `37 mm^2` |
| Shunt relative permeability | `mu_r,sh` | `50,000` |
| Steel path equivalent reluctance allowance | `R_steel` | `1.0e6 A/Wb` |

The steel reluctance is included as a small but nonzero term so the model does not unrealistically treat the support structure as perfect.

## Design Targets

The baseline concept is judged against a practical set of switching-design targets:

- high-field state should be comfortably above a plausible reed-switch actuation threshold
- low-field state should show strong suppression relative to the ON state
- mu-metal should remain below a conservative local flux-density limit
- the concept should tolerate prototype-level manufacturing methods
- the switching mechanism should be explainable in terms a client can review quickly

## Simplified Magnetic Network

The model uses:

`R = l / (mu * A)`

and magnetomotive force:

`F = H_c * l_m`

where:

- `mu = mu_0 * mu_r`
- `mu_0 = 4 pi x 10^-7 H/m`

### Magnet MMF

Using `H_c = 850,000 A/m` and `l_m = 0.005 m`:

`F = 850,000 x 0.005 = 4,250 A-turn`

### Magnet Reluctance

`R_m = l_m / (mu_0 * mu_r,m * A_m)`

Substituting:

`R_m = 0.005 / (4 pi x 10^-7 x 1.05 x 25 x 10^-6)`

`R_m ~= 1.52 x 10^8 A/Wb`

### Output Gap Reluctance

`R_out = g_out / (mu_0 * A_out)`

`R_out = 0.0015 / (4 pi x 10^-7 x 25 x 10^-6)`

`R_out ~= 4.77 x 10^7 A/Wb`

### Engaged Shunt Reluctance

The shunt branch contains a small residual air gap and the mu-metal body itself.

Residual gap term:

`R_sh,gap = g_sh / (mu_0 * A_sh)`

`R_sh,gap = 0.0001 / (4 pi x 10^-7 x 37 x 10^-6)`

`R_sh,gap ~= 2.15 x 10^6 A/Wb`

Shunt body term:

`R_sh,body = l_sh / (mu_0 * mu_r,sh * A_sh)`

`R_sh,body = 0.02 / (4 pi x 10^-7 x 50,000 x 37 x 10^-6)`

`R_sh,body ~= 8.60 x 10^3 A/Wb`

So:

`R_sh ~= R_sh,gap + R_sh,body ~= 2.16 x 10^6 A/Wb`

The gap term dominates, which is typical and useful. It means switching performance is controlled mostly by mechanical fit and standoff.

## ON-State Estimate

With the shunt retracted, the principal circuit reluctance is approximated by:

`R_on,total = R_m + R_steel + R_out`

`R_on,total ~= 1.52 x 10^8 + 1.0 x 10^6 + 4.77 x 10^7`

`R_on,total ~= 2.007 x 10^8 A/Wb`

Resulting flux:

`Phi_on = F / R_on,total`

`Phi_on = 4,250 / 2.007 x 10^8`

`Phi_on ~= 2.12 x 10^-5 Wb`

Output gap flux density:

`B_on = Phi_on / A_out`

`B_on = 2.12 x 10^-5 / 25 x 10^-6`

`B_on ~= 0.85 T`

This is the local gap flux density, not necessarily the field seen by a sensor offset from the gap. The actual sensor field depends on fringe geometry and placement.

## OFF-State Estimate

When the shunt is engaged, the output path and shunt path exist in parallel after the source reluctance. A first-pass split can be estimated from branch permeances.

Branch reluctances:

- `R_out = 4.77 x 10^7 A/Wb`
- `R_sh = 2.16 x 10^6 A/Wb`

Equivalent branch reluctance:

`R_parallel = (R_out x R_sh) / (R_out + R_sh)`

`R_parallel ~= 2.06 x 10^6 A/Wb`

Total reluctance in the diverted state:

`R_off,total = R_m + R_steel + R_parallel`

`R_off,total ~= 1.55 x 10^8 A/Wb`

Total source flux:

`Phi_total,off = F / R_off,total`

`Phi_total,off ~= 2.74 x 10^-5 Wb`

Flux division into output branch:

`Phi_out,off = Phi_total,off x (R_sh / (R_out + R_sh))`

`Phi_out,off ~= 2.75 x 10^-5 x 0.0433`

`Phi_out,off ~= 1.19 x 10^-6 Wb`

Output-gap flux density in OFF state:

`B_off = Phi_out,off / A_out`

`B_off = 1.19 x 10^-6 / 25 x 10^-6`

`B_off ~= 0.048 T`

### Switching Ratio

`Reduction = 1 - (B_off / B_on)`

`Reduction = 1 - (0.048 / 0.85)`

`Reduction ~= 94.4 percent`

That meets the target of at least 80 percent field reduction.

## Mu-Metal Saturation Check

The shunt branch carries most of the diverted flux:

`Phi_sh,off = Phi_total,off - Phi_out,off`

`Phi_sh,off ~= 2.63 x 10^-5 Wb`

Shunt flux density:

`B_sh = Phi_sh,off / A_sh`

`B_sh = 2.63 x 10^-5 / 37 x 10^-6`

`B_sh ~= 0.71 T`

That keeps the shunt below the conservative `0.75 T` design ceiling used in this study.

This was treated as one of the main reliability gates in the concept. A design that only works by pushing mu-metal too close to its limit is not robust enough to recommend for a switching application without further verification.

## Design Interpretation

The analysis leads to three useful engineering conclusions:

1. `Mechanical gap control is critical.`
The engaged shunt reluctance is dominated by residual air gap, not by the mu-metal bulk. Surface finish, flatness, and fixture repeatability matter.

2. `Mu-metal should be local, not structural.`
The shunt element benefits from very high permeability, but the larger return path should remain conventional soft magnetic steel for cost, robustness, and saturation margin.

3. `Output field reduction is strong even with a simple mechanism.`
A modestly moving shunt can create a large ratio between ON and OFF field at the sensing region.

## Optimization Direction

The follow-on sweep in [optimization-study.md](/home/fadali/magnetic-flux-shunt-switch/docs/optimization-study.md) confirms that:

- reducing the engaged shunt residual gap is the strongest lever for improving OFF-state suppression
- increasing shunt area mainly helps saturation margin and gives secondary suppression gains
- the baseline `0.10 mm` gap and `37 mm^2` area is not the absolute optimum, but it is a more fabrication-tolerant choice than the tighter `0.05 mm` best-case option

## Practical Fabrication Notes

- Use annealed mu-metal stock after final forming if possible.
- Avoid hard mechanical deformation after magnetic-property-critical processing.
- Keep engaged faces flat and parallel.
- If vibration is expected, include a hard mechanical stop to control the residual gap.
- If repeatability matters more than absolute minimum reluctance, design around a known thin spacer instead of relying on metal-to-metal contact.

## Validation Strategy

The recommended validation sequence after concept completion was:

1. Verify sensor-side field threshold against an actual switch or Hall part number.
2. Build a 2D field model to confirm fringe field in the real sensing location.
3. Prototype the shunt geometry with controlled engaged-stop spacing.
4. Measure ON and OFF switching repeatability over repeated cycles.
5. Compare prototype behavior against the reluctance model and update the geometry if needed.

## Recommended Next Steps

- build a 2D FEMM model to validate fringe field at the actual sensor location
- compare mu-metal against permalloy and soft iron shunts
- prototype two shunt thicknesses to test sensitivity to saturation margin
- add an actuation mechanism, either spring-return manual slide or pulse-coil latch
