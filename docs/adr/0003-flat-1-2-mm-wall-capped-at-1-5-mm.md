---
status: partly superseded by ADR 0006 (the Body is now a single Top strip; thickness unchanged)
---

# The Wall is a plain flat 1.2 mm sheet, never over 1.5 mm

The user wants the Divider as thin as possible (it replaces folded paper and tape), with a hard cap of 1.5 mm on Wall thickness. Under that cap a plain solid sheet is the stiffest Wall there is; any pattern or opening removes stiffness. The user chose 1.2 mm over 1.5 mm, accepting about 1.6x more sideways flex and less margin against Bowing (about 3.5 N vs about 1.3 N of Spring push) for less filament.

## Considered Options

- **4 mm deep Springs (Beams 25x stiffer sideways):** fixed the Spring wobble but added lumps the user found ugly, and breaks the 1.5 mm cap.
- **Top-edge rib on the Body:** about 4x stiffer sideways, but breaks the 1.5 mm cap.
- **1.5 mm sheet:** about 2x stiffer and 5x margin against Bowing, at about 6 g more filament.

## Consequences

The Springs are only about 2x stiffer sideways than along the Wall, so the ends can shift and lean a little. If the Wall bows in use, first reduce the Spring force (fewer Beams), then go back to 1.5 mm.
