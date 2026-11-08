# The Wall prints flat, diagonally across the bed

The Wall is 293.6 mm long and the X2D bed is 256 mm square, so it only fits flat across the diagonal. The 293.6 × 60 mm outline needs about 250 mm of the bed's 362 mm diagonal, leaving about 6 mm of margin. The Wall has to print flat anyway (ADR 0002), and keeping it in one piece keeps the Body stiff.

Status: accepted and checked. The X2D profile has no excluded zones; the Wall sits 3 mm from each edge, and the plate (src/plate.py, exports/divider_plate.3mf) slices without warnings.

## Considered Options

- **Longer T-pads that take up about 20 mm of length each:** the Wall would fit straight, but the T-pads get bulkier, against the minimal-T goal.
- **A Wall in two halves joined in the middle:** adds a joint that can flex where the Body most needs to be stiff.
