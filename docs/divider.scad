// Tension-fit tea bag drawer divider: the OpenSCAD port of divider.py, for MakerWorld's
// Customize button. Same geometry and names as divider.py, which stays the source of truth:
// change both together.
//
// Three printed parts: one Wall and two T-pads. The Wall stands across the drawer and its
// two Springs push the T-pads against the drawer's side walls, so nothing is glued or screwed.
//
// Kept to features the OpenSCAD 2021.01 release has, since MakerWorld runs that version.

/* [Your drawer] */

// Inside width of the drawer, between the two side walls the divider presses on (mm). Measure it to within about 1 mm.
drawer_span = 290; // [150:0.5:295.5]

// Your printer's plate. The Wall prints flat, corner to corner, so the plate sets the longest drawer span you can print: 295.5 mm on a 256 mm plate, 188 mm on the A1 mini.
bed_size = 256; // [180:A1 mini (180 mm), 256:A1 / P1 / X1 / X2D (256 mm)]

/* [Output] */

// What to make. "plate" lays out the Wall and both T-pads ready to print.
part = "plate"; // [plate, wall, t_pad, assembly]

/* [Hidden] */

COMPRESSION = 3.0;    // compression per end at the nominal span
HEIGHT = 60.0;
WALL = 1.2;           // sheet thickness, everywhere on the Wall (limit: 1.5)

UPRIGHT_W = 3.0;      // Upright the T-pad clips onto, along the wall
BEAMS = 18;
BEAM_T = 0.95;        // beam thickness in the bending direction: 2 lines
BEAM_GAP = 1.5;       // slot between neighbouring beams
BAR_H = 6.0;          // top and bottom bar height
TRAVEL_GAP = 7.0;     // slots the moving side closes into
SLOT_R = 0.5;         // root fillet at every slot corner

TOP_STRIP = 25.0;     // the Body: carries the Springs' push, sized against Bowing

PAD_W = 10.0;         // contact face across the wall
PAD_T = 1.2;          // contact plate thickness
JAW_T = 1.2;          // clip jaws either side of the upright
PRESS = 0.05;         // fit per side on the upright, middle
PRESS_ENDS = 0.1;     // fit per side at the clip's top and bottom
ENDS_L = 8.0;         // length of each looser end section

BED_MARGIN = 1.0;     // clearance from the plate's edge, all round

$fn = 24;

wall_half = drawer_span / 2 + COMPRESSION - PAD_T;

// Right-hand Spring, along the wall: the Upright's inner face, the outer edge of the last
// Beam, the inner edge of the first Beam, and the end face of the Body.
upright_in = wall_half - UPRIGHT_W;
beams_out = upright_in - TRAVEL_GAP;
beams_in = beams_out - (BEAMS * BEAM_T + (BEAMS - 1) * BEAM_GAP);
body_end = beams_in - TRAVEL_GAP;

assert(body_end > 0, "drawer span too short: the Springs would overlap in the middle");
assert(TOP_STRIP >= BAR_H, "Top strip must cover the Top bars");

// The Wall lies on the plate's diagonal: its 2 * wall_half by HEIGHT outline, turned 45
// degrees, has to fit inside the plate less BED_MARGIN all round.
max_span = (bed_size - 2 * BED_MARGIN) * sqrt(2) - HEIGHT - 2 * (COMPRESSION - PAD_T);
assert(drawer_span <= max_span,
       str("drawer span too long: a ", bed_size, " mm plate fits drawer spans up to ",
           floor(max_span * 10) / 10, " mm"));

module rect(x0, x1, y0, y1, r = 0) {
    translate([x0, y0])
        if (r > 0)
            offset(r = r) offset(delta = -r) square([x1 - x0, y1 - y0]);
        else
            square([x1 - x0, y1 - y0]);
}

// The right Spring's slots, in the wall's side view (x along it, y up).
module right_slots() {
    // Body | first Beam and Bottom bar; open at the bottom
    rect(body_end, beams_in, -1, HEIGHT - BAR_H, SLOT_R);
    // last Beam | Upright; open at the top
    rect(beams_out, upright_in, BAR_H, HEIGHT + 1, SLOT_R);
    for (i = [0 : BEAMS - 2]) {
        x0 = beams_in + i * (BEAM_T + BEAM_GAP) + BEAM_T;
        rect(x0, x0 + BEAM_GAP, BAR_H, HEIGHT - BAR_H, SLOT_R);
    }
}

// Side view of the Wall, centred on x = 0, bottom edge on y = 0.
module wall_profile() {
    difference() {
        rect(-wall_half, wall_half, 0, HEIGHT);
        right_slots();
        mirror([1, 0]) right_slots();
        // Everything under the Top strip, out into the first Travel gap on each side.
        rect(-(body_end + TRAVEL_GAP / 2), body_end + TRAVEL_GAP / 2, -1, HEIGHT - TOP_STRIP);
    }
}

// The Wall standing up: x along it, y through its thickness, z up.
module wall() {
    rotate([90, 0, 0]) linear_extrude(height = WALL, center = true) wall_profile();
}

// A T seen from above: contact plate at x in [0, PAD_T], clip jaws reaching -x either side
// of the Upright. The clip opens to PRESS_ENDS over ENDS_L at the top and bottom so it
// starts sliding on easily.
module t_pad() {
    jaw_y = WALL / 2 + PRESS + JAW_T / 2;
    assert(jaw_y + JAW_T / 2 <= PAD_W / 2, "jaws wider than the pad");
    assert(PRESS_ENDS >= PRESS && 2 * ENDS_L < HEIGHT);
    half = WALL / 2 + PRESS_ENDS;
    difference() {
        linear_extrude(height = HEIGHT) {
            rect(0, PAD_T, -PAD_W / 2, PAD_W / 2);
            for (y = [jaw_y, -jaw_y])
                rect(-UPRIGHT_W, 0, y - JAW_T / 2, y + JAW_T / 2);
        }
        if (PRESS_ENDS > PRESS)
            for (z0 = [0, HEIGHT - ENDS_L])
                translate([-UPRIGHT_W - 1, -half, z0])
                    cube([UPRIGHT_W + 1, 2 * half, ENDS_L]);
    }
}

// Assembled and uncompressed: the same T-pad on both ends, the left one turned around.
module assembly() {
    color("#7a9a6b") wall();
    color("#c9b98f") {
        translate([wall_half, 0, 0]) t_pad();
        translate([-wall_half, 0, 0]) rotate([0, 0, 180]) t_pad();
    }
}

// Print layout, origin at the plate's front-left corner: the Wall flat on the diagonal,
// the two T-pads face-down (contact face on the plate, jaws up) side by side in the back-left
// corner.
module plate() {
    translate([bed_size / 2, bed_size / 2, 0]) rotate([0, 0, 45])
        translate([0, -HEIGHT / 2, 0]) linear_extrude(height = WALL) wall_profile();
    for (y = [bed_size - 32, bed_size - 46])
        translate([40 - HEIGHT / 2, y, PAD_T]) rotate([0, 90, 0]) t_pad();
}

if (part == "plate") plate();
else if (part == "wall") wall();
else if (part == "t_pad") t_pad();
else assembly();
