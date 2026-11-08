"""Print layout for the X2D's 256 mm plate, in bed coordinates (mm, origin at the plate's
front-left corner): the Wall flat and diagonal, the two T-pads face-down in the free corners.

write_project() turns it into a Bambu Studio project 3MF with the Bambu Studio command line:
X2D 0.4 nozzle, stock 0.20mm Standard, Bambu PLA Matte on the main (left, direct-drive) hotend,
Textured PEI. Changes from the stock process, per the shared print defaults for functional
parts: 3 walls, 25% gyroid infill. Unsliced: open it in Bambu Studio, pick the AMS slot, slice.
"""

import json
import subprocess
import tempfile
from pathlib import Path

import build123d as bd
from cadgen import model

import divider as d

BAMBU = Path("/Applications/BambuStudio.app/Contents/MacOS/BambuStudio")
PROFILES = Path("/Applications/BambuStudio.app/Contents/Resources/profiles/BBL")
PRESETS = {
    "machine": "Bambu Lab X2D 0.4 nozzle",
    "process": "0.20mm Standard @BBL X2D",
    "filament": "Bambu PLA Matte @BBL X2D 0.4 nozzle",
}
OVERRIDES = {
    "machine": {"curr_bed_type": "Textured PEI Plate"},
    "process": {"wall_loops": "3", "sparse_infill_density": "25%",
                "sparse_infill_pattern": "gyroid",
                "filament_map_mode": "Manual", "filament_map": ["1"]},  # 1 = main hotend
    "filament": {},
}

BED = 256.0
PAD_SPOTS = ((40.0, 224.0), (40.0, 210.0))   # side by side, 4 mm apart, in the back-left corner


def plate_parts():
    wall = d.wall().shape
    # Lay it flat (thickness Y -> Z, resting on z=0), centre it, turn it onto the diagonal.
    flat = bd.Rot(90, 0, 0) * wall
    bb = flat.bounding_box()
    flat = bd.Pos(-bb.center().X, -bb.center().Y, -bb.min.Z) * flat
    wall_on_bed = bd.Pos(BED / 2, BED / 2, 0) * bd.Rot(0, 0, 45) * flat
    wall_on_bed.label = "wall"

    # Face-down: the contact face on the bed, the clip jaws rising 3 mm with the slot open
    # upward. A short, stable print with no overhang, and the face gets the plate's finish.
    pad = bd.Rot(0, 90, 0) * d.t_pad().shape
    pads = []
    for i, (x, y) in enumerate(PAD_SPOTS):
        pbb = pad.bounding_box()
        p = bd.Pos(x - pbb.center().X, y - pbb.center().Y, -pbb.min.Z) * pad
        p.label = f"t_pad_{i + 1}"
        pads.append(p)

    for part in [wall_on_bed, *pads]:
        b = part.bounding_box()
        assert b.min.X >= 0 and b.min.Y >= 0 and b.max.X <= BED and b.max.Y <= BED, (part.label, b)
        assert abs(b.min.Z) < 1e-6, part.label
    for p in pads:
        assert wall_on_bed.distance_to(p) > 5, "pad too close to the wall"
    return [wall_on_bed, *pads]


def _flat_preset(kind, name):
    """A system preset with its `inherits` chain merged in; the CLI does not resolve it."""
    data = json.loads((PROFILES / kind / f"{name}.json").read_text())
    if data.get("inherits"):
        merged = _flat_preset(kind, data["inherits"])
        merged.update(data)
        data = merged
    data.pop("inherits", None)
    data["name"] = name
    return data


def write_project(path, slice_check=False):
    """Write the plate as a Bambu Studio project 3MF at `path`. With slice_check, also slice
    it (into a temporary folder) and return the CLI's result, to prove the plate slices."""
    path = Path(path).resolve()
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        stls = []
        for part in plate_parts():
            stl = tmp / f"{part.label}.stl"
            bd.export_stl(part, str(stl), tolerance=0.01, angular_tolerance=0.1)
            stls.append(str(stl))
        files = {}
        for kind, name in PRESETS.items():
            data = _flat_preset(kind, name)
            data.update(OVERRIDES[kind])
            files[kind] = tmp / f"{kind}.json"
            files[kind].write_text(json.dumps(data))
        base = [str(BAMBU), "--load-settings", f"{files['machine']};{files['process']}",
                "--load-filaments", str(files["filament"]), "--arrange", "0", "--orient", "0"]
        # --outputdir keeps the CLI's result.json out of the working folder; it also
        # prefixes --export-3mf, so pass the bare name.
        subprocess.run(base + ["--outputdir", str(path.parent), "--export-3mf", path.name, *stls],
                       check=True, capture_output=True, text=True)
        (path.parent / "result.json").unlink(missing_ok=True)
        assert path.exists(), "Bambu Studio wrote no 3MF"
        if slice_check:
            sliced = tmp / "sliced.gcode.3mf"   # --outputdir prefixes --export-3mf
            run = subprocess.run(base + ["--slice", "0", "--outputdir", str(tmp),
                                         "--export-3mf", sliced.name, *stls],
                                 capture_output=True, text=True)
            info = ""
            if sliced.exists():
                import zipfile
                with zipfile.ZipFile(sliced) as z:
                    info = z.read("Metadata/slice_info.config").decode()
            return run.returncode, info
    return 0, ""


@model
def plate():
    parts = plate_parts()
    wb = parts[0].bounding_box()
    print(f"wall on bed: x {wb.min.X:.1f}..{wb.max.X:.1f}, y {wb.min.Y:.1f}..{wb.max.Y:.1f}, "
          f"margin {min(wb.min.X, wb.min.Y, BED - wb.max.X, BED - wb.max.Y):.1f} mm")
    return bd.Compound(children=parts, label="plate")


if __name__ == "__main__":
    plate()
