# Magnetic Flux Shunt Switching Device

Portfolio case study for a compact magnetic switching mechanism that uses a movable mu-metal shunt to redirect flux away from an output gap.

## Project Summary

This project demonstrates a practical magnetic circuit for switching applications where an output field must be turned on and off without changing the permanent magnet itself. The switching action is achieved by inserting or retracting a high-permeability mu-metal shunt that changes the preferred flux path.

![Device overview](assets/device-overview.svg)

The concept is intended for:

- low-power magnetic switching
- reed switch or Hall sensor actuation
- instrumentation interlocks
- compact latching or gating mechanisms

![Flux-path comparison](assets/flux-paths.svg)

## Engineering Objective

Design a magnetic circuit that satisfies the following targets:

- output state must provide enough field at the sensing region to trip a reed switch
- shunted state must reduce the field by at least 80 percent
- geometry must remain compact enough for bench-top prototyping
- the shunt should operate below a conservative mu-metal saturation threshold
- design should be manufacturable from standard machined or laser-cut parts

## Device Concept

The circuit uses five functional elements:

1. `NdFeB permanent magnet`
2. `soft steel pole pieces`
3. `controlled output air gap`
4. `movable mu-metal shunt`
5. `reed switch or Hall sensor near the output gap`

In the `ON` state, the shunt is retracted, so flux crosses the output gap and creates a usable fringe field at the sensor.

In the `OFF` state, the mu-metal shunt bridges the pole pieces and offers a much lower reluctance path than the output gap. Most of the flux is diverted through the shunt, sharply reducing the field at the sensing region.

## Quick Result

Using the baseline geometry documented in [docs/design-notes.md](/home/fadali/magnetic-flux-shunt-switch/docs/design-notes.md):

- estimated output-gap flux density, `ON`: about `0.85 T`
- estimated output-gap flux density, `OFF`: about `0.05 T`
- estimated field reduction at the output gap: about `94 percent`
- estimated shunt flux density in the diverted state: about `0.71 T`

That shunt flux density remains below a conservative mu-metal design ceiling of roughly `0.75 T`, which keeps the concept within a credible operating region for a portfolio-level design study.

## Repository Contents

- [docs/design-notes.md](/home/fadali/magnetic-flux-shunt-switch/docs/design-notes.md): full problem definition, assumptions, and magnetic calculations
- [scripts/reluctance_calculator.py](/home/fadali/magnetic-flux-shunt-switch/scripts/reluctance_calculator.py): simple reluctance-network calculator for the baseline design
- [assets/device-overview.svg](/home/fadali/magnetic-flux-shunt-switch/assets/device-overview.svg): visual overview of the switching concept
- [assets/flux-paths.svg](/home/fadali/magnetic-flux-shunt-switch/assets/flux-paths.svg): ON and OFF flux-path comparison

## Design Inputs

Baseline assumptions used in this study:

- magnet material: `NdFeB`
- magnet cross-section: `5 mm x 5 mm`
- magnet length along magnetization axis: `5 mm`
- magnet coercive field used for first-pass model: `850 kA/m`
- output gap length: `1.5 mm`
- output gap cross-section: `25 mm^2`
- shunt effective gap when engaged: `0.1 mm`
- shunt body length: `20 mm`
- shunt cross-section: `37 mm^2`
- mu-metal relative permeability for first-pass estimate: `50,000`

## Why Mu-Metal Here

Mu-metal is not treated as a universal core material in this design. It is used specifically where its very high permeability is valuable: as a low-reluctance flux shunt that can strongly divert magnetic flux when engaged.

That choice is defensible because:

- the shunt works in a moderate flux-density regime
- low reluctance matters more than high saturation margin in this part
- the switching function benefits from a dramatic path-preference change

For the pole pieces and return path, soft magnetic steel remains the more practical choice.

## Portfolio Value

This case study is useful as a showcase project because it demonstrates:

- magnetic circuit modeling
- engineering judgment in material selection
- quantitative switching analysis
- saturation checks
- design-for-manufacture thinking
- communication through diagrams and reproducible calculations

## How To Run The Calculator

From the repository root:

```bash
python3 scripts/reluctance_calculator.py
```

The script prints the modeled reluctances, estimated flux split, gap flux density in each state, and a simple saturation check for the mu-metal shunt.

## Next Expansion Options

This repository is intentionally scoped as a strong first portfolio artifact. Natural follow-up work would be:

- FEMM or COMSOL field simulation snapshots
- a parametric sweep of shunt gap and pole area
- CAD renders and fabrication drawings
- prototype test data against a reed switch pickup threshold

## Author

Prepared by `Mohamed Fadel` as an engineering portfolio project focused on magnetic switching design.
