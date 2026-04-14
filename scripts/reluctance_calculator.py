#!/usr/bin/env python3
"""First-pass reluctance model for a magnetic flux shunt switching device."""

from math import pi


MU_0 = 4 * pi * 1e-7
STEEL_RELUCTANCE = 1.0e6
SHUNT_B_DESIGN_LIMIT = 0.75


BASELINE = {
    "magnet_length": 5e-3,
    "magnet_area": 25e-6,
    "magnet_mu_r": 1.05,
    "magnet_hc": 850_000,
    "output_gap": 1.5e-3,
    "output_area": 25e-6,
    "shunt_gap": 0.1e-3,
    "shunt_length": 20e-3,
    "shunt_area": 37e-6,
    "shunt_mu_r": 50_000,
}


def reluctance(length_m: float, mu_r: float, area_m2: float) -> float:
    return length_m / (MU_0 * mu_r * area_m2)


def evaluate_design(
    *,
    magnet_length: float,
    magnet_area: float,
    magnet_mu_r: float,
    magnet_hc: float,
    output_gap: float,
    output_area: float,
    shunt_gap: float,
    shunt_length: float,
    shunt_area: float,
    shunt_mu_r: float,
    steel_reluctance: float = STEEL_RELUCTANCE,
) -> dict[str, float]:
    mmf = magnet_hc * magnet_length
    r_magnet = reluctance(magnet_length, magnet_mu_r, magnet_area)
    r_output = reluctance(output_gap, 1.0, output_area)
    r_shunt_gap = reluctance(shunt_gap, 1.0, shunt_area)
    r_shunt_body = reluctance(shunt_length, shunt_mu_r, shunt_area)
    r_shunt = r_shunt_gap + r_shunt_body

    r_on_total = r_magnet + steel_reluctance + r_output
    phi_on = mmf / r_on_total
    b_on = phi_on / output_area

    r_parallel = (r_output * r_shunt) / (r_output + r_shunt)
    r_off_total = r_magnet + steel_reluctance + r_parallel
    phi_total_off = mmf / r_off_total
    phi_out_off = phi_total_off * (r_shunt / (r_output + r_shunt))
    phi_shunt_off = phi_total_off - phi_out_off
    b_off = phi_out_off / output_area
    b_shunt = phi_shunt_off / shunt_area
    reduction = 1.0 - (b_off / b_on)

    return {
        "mmf": mmf,
        "r_magnet": r_magnet,
        "r_output": r_output,
        "r_shunt_gap": r_shunt_gap,
        "r_shunt_body": r_shunt_body,
        "r_shunt": r_shunt,
        "r_on_total": r_on_total,
        "phi_on": phi_on,
        "b_on": b_on,
        "r_parallel": r_parallel,
        "r_off_total": r_off_total,
        "phi_total_off": phi_total_off,
        "phi_out_off": phi_out_off,
        "phi_shunt_off": phi_shunt_off,
        "b_off": b_off,
        "b_shunt": b_shunt,
        "reduction": reduction,
    }


def main() -> None:
    results = evaluate_design(**BASELINE)

    print("Magnetic Flux Shunt Switching Device")
    print("-" * 40)
    print(f"MMF: {results['mmf']:,.1f} A-turn")
    print(f"Magnet reluctance: {results['r_magnet']:.3e} A/Wb")
    print(f"Output gap reluctance: {results['r_output']:.3e} A/Wb")
    print(f"Engaged shunt reluctance: {results['r_shunt']:.3e} A/Wb")
    print()
    print(f"ON-state flux: {results['phi_on']:.3e} Wb")
    print(f"ON-state output gap flux density: {results['b_on']:.3f} T")
    print()
    print(f"OFF-state total source flux: {results['phi_total_off']:.3e} Wb")
    print(f"OFF-state output branch flux: {results['phi_out_off']:.3e} Wb")
    print(f"OFF-state shunt branch flux: {results['phi_shunt_off']:.3e} Wb")
    print(f"OFF-state output gap flux density: {results['b_off']:.3f} T")
    print(f"Field reduction: {results['reduction'] * 100:.1f}%")
    print()
    print(f"Shunt flux density: {results['b_shunt']:.3f} T")
    if results["b_shunt"] <= SHUNT_B_DESIGN_LIMIT:
        print(
            f"Shunt saturation check: PASS "
            f"(below {SHUNT_B_DESIGN_LIMIT:.2f} T design limit)"
        )
    else:
        print(
            f"Shunt saturation check: REVIEW "
            f"(above {SHUNT_B_DESIGN_LIMIT:.2f} T design limit)"
        )


if __name__ == "__main__":
    main()
