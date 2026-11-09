# Tea Bag Drawer Divider

A spring-loaded wall that stands across a kitchen drawer to keep tea bags sorted. A spring at
each end pushes a clip-on pad against the drawer's side walls: no glue, screws or tape. The
ready-made parts fit a 290 mm drawer.

- Page: https://ivanifchen.github.io/tea-bags-drawer-divider/
- Print (Bambu Studio project): [exports/divider_plate.3mf](exports/divider_plate.3mf)
- STEP: [exports/divider.step](exports/divider.step)
- Customize (OpenSCAD): [exports/makerworld/divider.scad](exports/makerworld/divider.scad)

The wall prints flat on the diagonal with the pads face-down beside it. PLA, 0.20 mm layers,
3 walls, 25% gyroid, no supports. About 23 minutes and 15 g on an X2D.

## Source

The model is Python ([build123d](https://github.com/gumyr/build123d), built with cadgen):

- `src/divider.py`: the wall and T-pad
- `src/check.py`: masses, fit, spring stiffness and bowing estimates
- `src/plate.py`: the print layout and Bambu Studio project writer
- `src/exports.py`: rebuilds the 3MF and STEP in `exports/`
- `src/divider.scad`: the OpenSCAD port used for MakerWorld's Customize
- `docs/adr/`: design decisions
