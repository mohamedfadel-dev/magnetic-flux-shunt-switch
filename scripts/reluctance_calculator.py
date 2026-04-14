#!/usr/bin/env python3
"""First-pass reluctance model for a magnetic flux shunt switching device."""

from math import pi


MU_0 = 4 * pi * 1e-7


def reluctance(length_m: float, mu_r: float, area_m2: float) -> float:
    return length_m / (MU_0 * mu_r * area_m2)


def main() -> None:
    # Baseline geometry from the design notes.
    magnet_length = 5e-3
    magnet_area = 25e-6
    magnet_mu_r = 1.05
    magnet_hc = 850_000

    output_gap = 1.5e-3
    output_area = 25e-6

    shunt_gap = 0.1e-3
    shunt_length = 20e-3
    shunt_area = 37e-6
    shunt_mu_r = 50_000

    steel_reluctance = 1.0e6
    shunt_b_design_limit = 0.75

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

    print("Magnetic Flux Shunt Switching Device")
    print("-" * 40)
    print(f"MMF: {mmf:,.1f} A-turn")
    print(f"Magnet reluctance: {r_magnet:.3e} A/Wb")
    print(f"Output gap reluctance: {r_output:.3e} A/Wb")
    print(f"Engaged shunt reluctance: {r_shunt:.3e} A/Wb")
    print()
    print(f"ON-state flux: {phi_on:.3e} Wb")
    print(f"ON-state output gap flux density: {b_on:.3f} T")
    print()
    print(f"OFF-state total source flux: {phi_total_off:.3e} Wb")
    print(f"OFF-state output branch flux: {phi_out_off:.3e} Wb")
    print(f"OFF-state shunt branch flux: {phi_shunt_off:.3e} Wb")
    print(f"OFF-state output gap flux density: {b_off:.3f} T")
    print(f"Field reduction: {reduction * 100:.1f}%")
    print()
    print(f"Shunt flux density: {b_shunt:.3f} T")
    if b_shunt <= shunt_b_design_limit:
        print(
            f"Shunt saturation check: PASS "
            f"(below {shunt_b_design_limit:.2f} T design limit)"
        )
    else:
        print(
            f"Shunt saturation check: REVIEW "
            f"(above {shunt_b_design_limit:.2f} T design limit)"
        )


if __name__ == "__main__":
    main()
