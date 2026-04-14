# Past Work Summary

## Engagement Type

Concept and first-pass engineering design for a compact magnetic switching mechanism using mu-metal as the active flux-shunting element.

## Client Need

The work addressed a switching-oriented magnetic design problem with three priorities:

- use mu-metal where it provides real value in the magnetic circuit
- achieve strong switching contrast between active and suppressed field states
- keep the concept practical enough for prototype fabrication and reliability review

## Constraints Addressed

- compact geometry suitable for bench-scale prototyping
- strong ON-state field at the switching region
- strong OFF-state field suppression
- conservative saturation margin in the mu-metal shunt
- realistic mechanical tolerance considerations around shunt engagement

## Work Completed

1. Selected a magnetic architecture based on a permanent magnet, steel pole pieces, controlled output gap, and movable mu-metal shunt.
2. Built a reluctance-based magnetic model for ON and OFF states.
3. Evaluated the mu-metal shunt against a conservative flux-density limit.
4. Performed a parameter sweep across shunt gap and shunt area.
5. Documented fabrication and repeatability risks relevant to switching reliability.
6. Prepared visual and written deliverables suitable for technical review and prototype planning.

## Main Outcome

Baseline concept outcome:

- ON-state output-gap flux density: about `0.849 T`
- OFF-state output-gap flux density: about `0.048 T`
- field reduction: about `94.4%`
- shunt flux density: about `0.711 T`

Optimized safe point from the sweep:

- engaged shunt gap: `0.05 mm`
- shunt cross-sectional area: `50 mm^2`
- OFF-state output-gap flux density: about `0.018 T`
- field reduction: about `97.8%`
- shunt flux density: about `0.545 T`

## Engineering Decisions

- `mu-metal was used locally as the shunt`
  This captured the benefit of very high permeability without forcing the larger return path to depend on a material with tighter handling and saturation constraints.
- `soft magnetic steel was retained for the pole and return structure`
  This supported practicality, manufacturability, and flux-carrying margin.
- `the baseline was kept at 0.10 mm engaged gap`
  Although a tighter gap improved suppression, the chosen baseline was more realistic for repeatable prototype fabrication.

## Reliability Considerations Covered

- residual gap sensitivity in the shunt path
- mu-metal property retention after forming and handling
- repeatability of engaged and disengaged positions
- local saturation margin in the shunt
- field variation at the actual switching location

## Deliverables Produced

- concept overview diagrams
- ON and OFF flux-path explanation
- reluctance-based calculations
- optimization study
- reliability and fabrication notes

## Why It Matters For Similar Clients

This work is relevant prior experience for clients seeking:

- magnetic circuit design for switching
- mu-metal flux-guidance or shunting solutions
- performance optimization with quantified tradeoffs
- practical prototype-oriented electromagnetic design support
