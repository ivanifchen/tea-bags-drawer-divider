"""Tension-fit tea bag drawer divider.

Three printed parts:
  wall   one flat WALL-thick sheet, both faces flat: a slotted spring at each end joined by
         a single strip along the top; prints flat on the bed
  t_pad  x2, a small T that slides down onto each end's upright; prints face-down

X runs along the wall, Y is its thickness, Z is up; the bottom edge sits on z=0.
Nothing on the wall is thicker than WALL; the hard limit is 1.5 mm.

Each spring is a parallel-guided flexure in the sheet's own plane: a top bar hangs off the
wall body, N thin vertical beams hang from it, and a bottom bar ties the beams' feet to an
upright that the T-pad clips onto. The beams stay parallel, so the pad slides straight in and
out along X without tilting; the upright rises ~0.1 mm at full travel instead of dragging.
The beams are thinner along X than the sheet is deep, so they give along the wall more
readily than across it. Printed flat, they bend along their filament lines, not across
layer bonds.

The middle (the Body) is just a Top strip, open below. Sideways flex there doesn't matter in
use, but the Springs' push must not bow it. That push enters the Body through the Top bars,
so the strip carries all of it and is sized for that. Spring, stiffness and bowing
estimates: check.py.

v2 (after the first test print): stronger Beams (0.95 mm), wider Travel gaps (7 mm) so they
no longer bottom out, the Body cut down to a Top strip, and a tighter T-pad clip with looser ends to start it on.

v3 (after the v2 test): Top strip 21 -> 25 mm, for margin against the slight bend v2 showed.
"""

import build123d as bd
from cadgen import model

WALL_COLOR = "#7a9a6b"
PAD_COLOR = "#c9b98f"

DRAWER_SPAN = 290.0   # measured inside width, +/- 1.5 mm
COMPRESSION = 3.0     # compression per end at the nominal span
HEIGHT = 60.0
WALL = 1.2            # sheet thickness (Y), everywhere on the wall (limit: 1.5)

UPRIGHT_W = 3.0       # Upright the T-pad clips onto, along X
BEAMS = 18
BEAM_T = 0.95         # beam thickness along X (the bending direction): 2 lines
BEAM_GAP = 1.5        # slot between neighbouring beams
BAR_H = 6.0           # top and bottom bar height; tall enough that the pad barely tilts
TRAVEL_GAP = 7.0      # slots the moving side closes into; 5 mm bottomed out in v1
SLOT_R = 0.5          # root fillet at every slot corner

TOP_STRIP = 25.0      # the Body: carries the Springs' push, sized against bowing

PAD_W = 10.0          # contact face across the wall (Y)
PAD_T = 1.2           # contact plate thickness (X)
JAW_T = 1.2           # clip jaws either side of the upright
PRESS = 0.05          # fit per side on the upright, middle; 0.1 loose in v1, 0.05 right in v2
PRESS_ENDS = 0.1      # fit per side at the clip's top and bottom, so it starts on easily
ENDS_L = 8.0          # length of each looser end section


def _rect(x0, x1, z0, z1, r=0.0):
    w, h = x1 - x0, z1 - z0
    shape = bd.RectangleRounded(w, h, r) if r else bd.Rectangle(w, h)
    return bd.Pos((x0 + x1) / 2, (z0 + z1) / 2) * shape


def spring_layout(wall_half, upright_w, beams, beam_t, beam_gap, travel_gap):
    """X positions of the right-hand spring: (body_end, beams_in, beams_out, upright_in)."""
    upright_in = wall_half - upright_w
    beams_out = upright_in - travel_gap   # outer edge of the last beam (= end of the top bar)
    beams_in = beams_out - (beams * beam_t + (beams - 1) * beam_gap)
    body_end = beams_in - travel_gap   # end face of the rigid wall body
    return body_end, beams_in, beams_out, upright_in


def make_wall(wall_half, height, wall, upright_w, beams, beam_t, beam_gap, bar_h,
              travel_gap, slot_r, top_strip):
    """The wall and both springs as one flat sheet, centred on x=0, spanning +/- wall_half."""
    body_end, beams_in, beams_out, upright_in = spring_layout(
        wall_half, upright_w, beams, beam_t, beam_gap, travel_gap)
    assert body_end > 0, "springs overlap in the middle"
    assert top_strip >= bar_h, "Top strip must cover the Top bars"

    # Side profile in the XZ plane, sketched in local XY: the whole sheet minus the right
    # spring's slots, mirrored for the left.
    slots = [
        # body | first beam and bottom bar; open at the bottom
        _rect(body_end, beams_in, -1.0, height - bar_h, slot_r),
        # last beam | upright; open at the top
        _rect(beams_out, upright_in, bar_h, height + 1.0, slot_r),
    ]
    for i in range(beams - 1):
        x0 = beams_in + i * (beam_t + beam_gap) + beam_t
        slots.append(_rect(x0, x0 + beam_gap, bar_h, height - bar_h, slot_r))
    right = bd.Sketch() + slots
    # Everything under the Top strip, out into the first Travel gap on each side so the
    # cut's corners fall inside openings already there.
    under = _rect(-(body_end + travel_gap / 2), body_end + travel_gap / 2,
                  -1.0, height - top_strip)
    profile = (_rect(-wall_half, wall_half, 0, height)
               - right - bd.mirror(right, bd.Plane.YZ) - under)

    part = bd.extrude(bd.Plane.XZ * profile, amount=wall / 2, both=True)
    part.label = "wall"
    part.color = WALL_COLOR
    return part


def t_pad_body(height, wall, upright_w, pad_w, pad_t, jaw_t, press, press_ends, ends_l):
    """A T seen from above: contact plate at x in [0, pad_t], clip jaws reaching -X either
    side of the upright. The clip grips at `press` per side in the middle and opens to
    `press_ends` over `ends_l` at the top and bottom, so it starts sliding on easily; the
    jaws' outer faces stay flush. Prints face-down (contact face on the bed, jaws up), with
    no overhang."""
    jaw_y = wall / 2 + press + jaw_t / 2
    assert jaw_y + jaw_t / 2 <= pad_w / 2, "jaws wider than the pad"
    assert press_ends >= press and 2 * ends_l < height
    plan = _rect(0, pad_t, -pad_w / 2, pad_w / 2) + [
        _rect(-upright_w, 0, y - jaw_t / 2, y + jaw_t / 2) for y in (jaw_y, -jaw_y)
    ]
    part = bd.extrude(plan, amount=height)
    if press_ends > press:
        half = wall / 2 + press_ends
        for z0 in (0, height - ends_l):
            part -= bd.Pos(-upright_w / 2 - 0.5, 0, z0 + ends_l / 2) * bd.Box(
                upright_w + 1, 2 * half, ends_l)
    part.label = "t_pad"
    part.color = PAD_COLOR
    return part


def _wall_half():
    return DRAWER_SPAN / 2 + COMPRESSION - PAD_T


@model
def wall():
    part = make_wall(_wall_half(), HEIGHT, WALL, UPRIGHT_W, BEAMS, BEAM_T, BEAM_GAP, BAR_H,
                     TRAVEL_GAP, SLOT_R, TOP_STRIP)
    assert part.bounding_box().size.Y <= 1.5 + 1e-9, "wall thicker than 1.5 mm"
    return part


@model
def t_pad():
    return t_pad_body(HEIGHT, WALL, UPRIGHT_W, PAD_W, PAD_T, JAW_T, PRESS, PRESS_ENDS, ENDS_L)


@model
def divider():
    """Assembly, uncompressed: the same pad on both ends, the left one turned around."""
    wall_part = wall().shape
    pad = t_pad().shape
    right = bd.Pos(_wall_half(), 0, 0) * pad
    left = bd.Pos(-_wall_half(), 0, 0) * bd.Rot(0, 0, 180) * pad
    right.label, left.label = "t_pad_right", "t_pad_left"
    kit = bd.Compound(children=[wall_part, right, left], label="divider")

    size = kit.bounding_box().size
    assert abs(size.X - (DRAWER_SPAN + 2 * COMPRESSION)) < 1e-6, size
    assert abs(size.Y - PAD_W) < 1e-6 and abs(size.Z - HEIGHT) < 1e-6, size
    return kit


if __name__ == "__main__":
    divider()
