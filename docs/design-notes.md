# Design Notes

This document is the working backbone of the project. It is not meant to be polished marketing copy. It is the place where the magnetic circuit gets pinned down enough to see whether the idea deserves further effort.

## Starting Point

The concept is a permanent-magnet circuit with two competing paths:

- an output path through an air gap
- a bypass path through a movable mu-metal shunt

The switching action comes from changing the reluctance landscape. Nothing is being electrically driven in this first pass. The only question is whether the geometry gives a meaningful difference between the two states.

## Baseline Geometry

I used the following first-pass dimensions:

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
| Steel path allowance | `R_steel` | `1.0e6 A/Wb` |

The steel path is not treated as perfect, but I also did not want it to dominate the model. So I kept it as a small nonzero reluctance term.

## Model

The basic relation is:

`R = l / (mu * A)`

and the magnetomotive force is:

`F = H_c * l_m`

with:

- `mu = mu_0 * mu_r`
- `mu_0 = 4 pi x 10^-7 H/m`

This is a simple reluctance-network model. It is useful because it makes the first-order design logic visible. It is not a substitute for field simulation near the sensing region.

## Magnet MMF

Using `H_c = 850,000 A/m` and `l_m = 0.005 m`:

`F = 850,000 x 0.005 = 4,250 A-turn`

## Main Reluctances

### Magnet

`R_m = l_m / (mu_0 * mu_r,m * A_m)`

`R_m = 0.005 / (4 pi x 10^-7 x 1.05 x 25 x 10^-6)`

`R_m ~= 1.52 x 10^8 A/Wb`

### Output gap

`R_out = g_out / (mu_0 * A_out)`

`R_out = 0.0015 / (4 pi x 10^-7 x 25 x 10^-6)`

`R_out ~= 4.77 x 10^7 A/Wb`

### Engaged shunt

The shunt path has two pieces:

- a tiny residual air gap
- the mu-metal body

Residual gap:

`R_sh,gap = g_sh / (mu_0 * A_sh)`

`R_sh,gap = 0.0001 / (4 pi x 10^-7 x 37 x 10^-6)`

`R_sh,gap ~= 2.15 x 10^6 A/Wb`

Shunt body:

`R_sh,body = l_sh / (mu_0 * mu_r,sh * A_sh)`

`R_sh,body = 0.02 / (4 pi x 10^-7 x 50,000 x 37 x 10^-6)`

`R_sh,body ~= 8.60 x 10^3 A/Wb`

So:

`R_sh ~= 2.16 x 10^6 A/Wb`

The important thing here is not the exact last digit. It is the fact that the residual gap dominates the shunt branch. That immediately tells me this design will care much more about contact geometry and repeatable standoff than about shaving a bit more bulk reluctance out of the mu-metal body.

## ON State

With the shunt retracted:

`R_on,total = R_m + R_steel + R_out`

`R_on,total ~= 2.007 x 10^8 A/Wb`

`Phi_on = F / R_on,total`

`Phi_on ~= 2.12 x 10^-5 Wb`

`B_on = Phi_on / A_out`

`B_on ~= 0.85 T`

That is the local gap flux density. It is not automatically the field that a real sensor would see a few millimeters away, but it is a useful anchor for the switching contrast.

## OFF State

With the shunt engaged, the output path and shunt path sit in parallel after the source reluctance.

Branch reluctances:

- `R_out = 4.77 x 10^7 A/Wb`
- `R_sh = 2.16 x 10^6 A/Wb`

Equivalent branch reluctance:

`R_parallel = (R_out x R_sh) / (R_out + R_sh)`

`R_parallel ~= 2.06 x 10^6 A/Wb`

Total reluctance:

`R_off,total = R_m + R_steel + R_parallel`

`R_off,total ~= 1.55 x 10^8 A/Wb`

Source flux:

`Phi_total,off = F / R_off,total`

`Phi_total,off ~= 2.74 x 10^-5 Wb`

Output branch flux:

`Phi_out,off = Phi_total,off x (R_sh / (R_out + R_sh))`

`Phi_out,off ~= 1.19 x 10^-6 Wb`

Output-gap flux density:

`B_off = Phi_out,off / A_out`

`B_off ~= 0.048 T`

So the first-pass switching ratio becomes:

`1 - (B_off / B_on) ~= 94.4 percent`

That is strong enough to make the concept feel worth keeping.

## Shunt Flux Density

Most of the diverted flux goes through the shunt:

`Phi_sh,off = Phi_total,off - Phi_out,off`

`Phi_sh,off ~= 2.63 x 10^-5 Wb`

`B_sh = Phi_sh,off / A_sh`

`B_sh ~= 0.71 T`

I treated `0.75 T` as a conservative internal ceiling for this project. That gave the baseline some margin without pretending the shunt could carry arbitrary flux just because its permeability is high.

## What I Took From The Numbers

Three things stood out right away.

First, the concept does actually switch in a meaningful way. The OFF state is not just slightly weaker. It is much weaker.

Second, the shunt gap matters more than almost anything else. Once that became clear, the rest of the project naturally moved toward a geometry sweep.

Third, mu-metal makes sense here only as a local element. I would not want to build the whole return structure around it. The shunt benefits from extremely high permeability, but the rest of the circuit is better served by ordinary soft magnetic steel.

## Practical Notes

- If this were ever built, I would want annealed mu-metal after final forming if possible.
- I would not trust uncontrolled metal-to-metal contact as the only way of setting the engaged position.
- A fixed stop or known spacer would probably make the results more repeatable, even if it gives away a bit of peak performance.
- The next honest step is not more algebra. It is a field model near the real switching location.
