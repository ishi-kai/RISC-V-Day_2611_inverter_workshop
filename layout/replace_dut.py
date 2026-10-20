#!/usr/bin/env python3
"""Replace DUT cells (inv_dut_NNN) in workshop_inverter.gds with layouts from other GDS files.

The cell to replace is named after each source file (inv_dut_000.gds -> inv_dut_000); its
contents are swapped, the instance placement in the top cell is kept.  A replacement must
use the inverter_base.gds frame: origin at the centre of the 20 x 50 um area, pins A (left
edge), Q (right edge), VDD (top edge), VSS (bottom edge), since the top level reaches
them with M1 stubs that abut the frame from outside.  A layout outside the frame or
missing a pin label is reported (and refused unless --force).

The LVS reference netlist <out>.cdl is rewritten at the same time (gen_lvs_netlist.py): the
replaced DUTs get their transistors from dut_params.csv (--csv to use another file).

Usage:  python3 replace_dut.py [--gds in.gds] [-o out.gds] [--csv dut_params.csv] [--force]
                               inv_dut_000.gds [...]
        (default: layout/workshop_inverter.gds / .cdl, updated in place)
"""
import os
import sys

import klayout.db as db

from gen_lvs_netlist import DUT_CSV, write_netlist

HERE = os.path.dirname(os.path.abspath(__file__))
PINS = {"A", "Q", "VDD", "VSS"}


def pin_labels(cell):
    ly = cell.layout()
    names = set()
    for li in ly.layer_indexes():
        it = cell.begin_shapes_rec(li)
        while not it.at_end():
            if it.shape().is_text():
                names.add(it.shape().text_string)
            it.next()
    return names


def replace(tgt, path):
    """Check the replacement for the cell named after `path` (the swap happens in main)."""
    name = os.path.splitext(os.path.basename(path))[0]
    tcell = tgt.cell(name)
    if tcell is None:
        raise SystemExit(f"{name}: no such cell in the target GDS")
    src = db.Layout()
    src.read(path)
    scell = src.cell(name)
    if scell is None:
        tops = src.top_cells()
        if len(tops) != 1:
            raise SystemExit(f"{path}: no cell {name} and not a single top cell")
        scell = tops[0]
    if abs(src.dbu - tgt.dbu) > 1e-12:
        raise SystemExit(f"{path}: dbu {src.dbu} differs from the target ({tgt.dbu})")

    problems = []
    frame = tcell.dbbox()
    bb = scell.dbbox()
    if not frame.contains(bb.p1) or not frame.contains(bb.p2):
        problems.append(f"bbox {bb} is outside the frame {frame}")
    missing = PINS - pin_labels(scell)
    if missing:
        problems.append("missing pin labels " + ", ".join(sorted(missing)))
    return name, tcell, (src, scell), problems   # src keeps scell's layout alive


def main():
    args = sys.argv[1:]
    gds = os.path.join(HERE, "workshop_inverter.gds")
    out = None
    csv_path = DUT_CSV
    force = "--force" in args
    args = [a for a in args if a != "--force"]
    for opt in ("--gds", "-o", "--csv"):
        if opt in args:
            i = args.index(opt)
            if opt == "--gds":
                gds = args[i + 1]
            elif opt == "-o":
                out = args[i + 1]
            else:
                csv_path = args[i + 1]
            del args[i:i + 2]
    if not args:
        sys.exit(__doc__)
    out = out or gds

    tgt = db.Layout()
    tgt.read(gds)
    jobs = [replace(tgt, p) for p in args]
    bad = [(n, p) for n, _, _, p in jobs if p]
    for n, p in bad:
        print(f"{n}: " + "; ".join(p))
    if bad and not force:
        sys.exit("nothing written (use --force to replace anyway)")

    for name, tcell, (_, scell), _ in jobs:
        old = list(tcell.each_child_cell())
        tcell.clear()                   # shapes and instances; the cell and its placement stay
        for ci in old:                  # drop the old sub-cells nobody else uses
            if tgt.is_valid_cell_index(ci) and tgt.cell(ci).parent_cells() == 0:
                tgt.prune_cell(ci, -1)
        tcell.copy_tree(scell)
        print(f"{name}: replaced ({tcell.dbbox()})")
    names = [c.name for c in tgt.each_cell()]
    dup = {n for n in names if names.count(n) > 1}
    if dup:
        sys.exit("duplicate cell names after the replacement: " + ", ".join(sorted(dup)))
    tgt.write(out)
    print("wrote", out)
    cdl = os.path.splitext(out)[0] + ".cdl"
    n = write_netlist(cdl, out, csv_path)
    print(f"wrote {cdl} ({n} DUT(s) from {csv_path}, {128 - n} placeholder(s))")


if __name__ == "__main__":
    main()
