# An OpenSCAD port of the Divider for MakerWorld's Customize button

To publish the Divider on MakerWorld with a setting for the Drawer span, its Customize button (the Parametric Model Maker) needs an OpenSCAD script; it can't run build123d. src/divider.scad is a port of src/divider.py with the same geometry and names. Only the Wall changes with the Drawer span; the T-pads are the same at every span. divider.py stays the source of truth: any design change goes into both.

The script exposes the Drawer span and the printer's plate (180 or 256 mm), and lays out a print plate the way src/plate.py does: the Wall flat on the diagonal, the T-pads face-down in the back-left corner. The plate limits the Drawer span to 295.6 mm on a 256 mm plate and 188.1 mm on a 180 mm plate (1 mm clear of the edges); the Springs set the minimum at about 116 mm. The slider runs from 150 to 295.5 mm, and the script stops with a message naming the limit if a span doesn't fit the chosen plate. At shorter spans the Body is shorter, so Bowing only gets less likely.

Status: accepted and checked against divider.py on 2026-11-08 with OpenSCAD 2026.10.11: Walls at 150, 200 and 290 mm and the T-pad differ by under 0.03 mm³ (the faceting of the slot fillets). The 295.5 mm plate slices on the X2D without warnings (about 22 min, 14 g). Re-checked at v3 (Top strip 25 mm) on 2026-11-08: each Wall at 150, 200 and 290 mm differs from divider.py by +0.39 mm³ (0.004%), the same as at v2 when measured the same way (OpenSCAD's $fn = 24 slot fillets against exact arcs). The T-pad matches exactly. exports.py now rebuilds the MakerWorld bundle, including the images. The script avoids features newer than OpenSCAD 2021.01, the version MakerWorld is reported to run.

## Considered Options

- **Only fixed sizes as print profiles:** no second copy of the design, but a drawer between sizes doesn't fit, since each end only absorbs about ±0.75 mm of the span tolerance.

## Consequences

Two copies of the design can drift apart. After changing divider.py, change divider.scad to match and compare the two Walls again before republishing.
