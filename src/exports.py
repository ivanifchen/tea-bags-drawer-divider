"""Deliverables, rebuilt from the models:
  divider_plate.3mf  the print: Bambu Studio project, plate laid out and settings set
  divider.step       every part, exact geometry, for other CAD or a remix
  makerworld/        the publishing bundle the listing (makerworld/listing.md) names:
                     per-part STL and STEP, the assembly STEP, the plate, the Customize
                     script, and the listing's images

STLs live only in the publishing bundle: they are the same meshes the plate 3MF holds.
Tested versions live in exports/archive/.
"""

import shutil
import subprocess
from pathlib import Path

from cadgen import export

from divider import divider, t_pad, wall
from plate import plate, write_project

SRC = Path(__file__).resolve().parent
OUT = SRC.parent / "exports"
MW = OUT / "makerworld"
CADGEN = ["cadgen", "+0.8.0"]


def snapshot(doc, png, *args):
    subprocess.run(CADGEN + ["snapshot", doc.id, str(png), "--preview", *args], check=True,
                   capture_output=True)


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    MW.mkdir(exist_ok=True)
    assembly = divider()
    export(assembly, OUT / "divider.step")
    write_project(OUT / "divider_plate.3mf")

    export(wall(), MW / "wall.stl", MW / "wall.step")
    export(t_pad(), MW / "t_pad.stl", MW / "t_pad.step")
    export(assembly, MW / "divider_assembly.step")
    shutil.copy(OUT / "divider_plate.3mf", MW / "divider_plate.3mf")
    shutil.copy(SRC / "divider.scad", MW / "divider.scad")
    snapshot(assembly, MW / "01_divider.png", "--camera", "25:22", "--width", "1600", "--height", "1200")
    snapshot(assembly, MW / "03_front.png", "--camera", "front", "--width", "1600", "--height", "1200")
    snapshot(plate(), MW / "04_plate.png", "--camera", "top", "--width", "1600", "--height", "1600")
    print("wrote", OUT / "divider_plate.3mf", "and", MW)
