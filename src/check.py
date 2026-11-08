"""Measure the built divider: masses, pad/wall fit, and the spring and stiffness estimates."""

from cadgen.geometry import closest_points, overlap_volume

import divider as d

parts = {p.label: p for p in d.divider().shape.leaves}
wall = parts["wall"]

PLA = 1.24e-3  # g/mm^3
for label in ("wall", "t_pad_right"):
    v = parts[label].volume
    print(f"{label:12s} {v / 1000:6.2f} cm^3  {v * PLA:5.1f} g")

for side in ("t_pad_right", "t_pad_left"):
    pad = parts[side]
    print(f"{side}: overlap {overlap_volume(wall, pad):.3f} mm^3, "
          f"contact {closest_points(wall, pad).distance:.3f} mm")
print("wall length", round(wall.bounding_box().size.X, 2), "mm")

E = 3500.0
L = d.HEIGHT - 2 * d.BAR_H
k_x = d.BEAMS * 12 * E * (d.WALL * d.BEAM_T**3 / 12) / L**3
k_y = d.BEAMS * 12 * E * (d.BEAM_T * d.WALL**3 / 12) / L**3
print(f"spring along wall {k_x:.3f} N/mm, sideways {k_y:.2f} N/mm per end "
      f"({k_y / k_x:.0f}x stiffer sideways)")
for delta in (2.25, 3.0, 3.75):
    stress = 3 * E * d.BEAM_T * delta / L**2
    print(f"  compression {delta:4.2f} mm/end: {k_x * delta:4.2f} N, root stress {stress:4.1f} MPa")

# Bowing: the Springs' push enters the Body at the top corner, so the top strip carries it.
# Its sideways buckling load lies between pinned ends (lower bound) and fixed ends (x4).
body_end = d.spring_layout(d._wall_half(), d.UPRIGHT_W, d.BEAMS, d.BEAM_T, d.BEAM_GAP,
                           d.TRAVEL_GAP)[0]
span = 2 * body_end
I_top = d.TOP_STRIP * d.WALL**3 / 12
P_pin = 3.1416**2 * E * I_top / span**2
max_push = k_x * (d.COMPRESSION + 0.75)
print(f"Body {span:.0f} mm long; top strip {d.TOP_STRIP:.0f} mm bows at {P_pin:.1f} N (pinned) "
      f"to {4 * P_pin:.1f} N (fixed); max push {max_push:.2f} N")
print(f"travel gap {d.TRAVEL_GAP} mm vs max travel 3.75 mm; "
      f"wall thickness {wall.bounding_box().size.Y:.2f} mm")
