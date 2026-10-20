#!/usr/bin/env python3
"""Generate DUT inverter layouts (layout/inv_dut_NNN.gds) from a DUT CSV.

Each DUT is the "inverter" PCell of the GF180MCU KLayout library "gf180mcu"
(~/src/gf180mcuD, cells/inverter.py): pfet + nfet PCells (bulk tie) wired on
Metal1 only.

All cells share one outline (sized for the largest DUT in the CSV):

        +------------------- VDD (Metal1 rail) -------------------+
        |   tap source  pfet  drain   (source/tap -> VDD)         |
        |               [gate]   |                                |
     A  ================ gate    ================================  Y
        |               [gate]   |                                |
        |   tap source  nfet  drain   (source/tap -> VSS)         |
        +------------------- VSS (Metal1 rail) -------------------+

Each layout/inv_dut_NNN.gds is this inverter centred in the ../inverter_base.gds frame
(20 x 50 um, origin at the centre, Metal1 pin strips A left, Q right, VDD top, VSS bottom),
strapped to the strips on Metal1, so it can replace the placeholder cell of the top level
(../layout/replace_dut.py).  --no-frame writes the bare inverter (pins A, Y) instead.

Pin labels (Metal1 label 34/10): A, Q, VDD, VSS (A, Y, VDD, VSS with --no-frame).
A reference netlist layout/inv_dut_NNN.cdl is written next to each GDS for LVS.

Set GF180_PDK to use another PDK directory than ~/src/gf180mcuD.

Usage:  python3 gen_layout.py [dut_params.csv] [--only 0,5,17] [--no-frame]
"""
import os
import sys

import pya

from apply_dut_csv import parse_len, read_csv
from xsch_lib import HERE

PDK_DIR = os.environ.get("GF180_PDK", os.path.expanduser("~/src/gf180mcuD"))
sys.path.insert(0, os.path.join(PDK_DIR, "libs.tech/klayout/tech/pymacros"))
import gdsfactory as gf  # noqa: E402

gf.gpdk.PDK.activate()   # $PDK=gf180mcuD would otherwise make gdsfactory look for a python module
from cells import gf180mcu  # noqa: E402

LIB = "gf180mcu"
OUT_DIR = os.path.join(HERE, "layout")
FRAME_GDS = os.path.join(os.path.dirname(HERE), "inverter_base.gds")
M1, M1_LBL, BND = (34, 0), (34, 10), (0, 0)


def um(v):
    return round(v * 1e6, 4)


def make_inv(ly, p, **extra):
    params = {"p_model": p["P_MODEL"], "wp": um(parse_len(p["P_W"])), "lp": um(parse_len(p["P_L"])),
              "n_model": p["N_MODEL"], "wn": um(parse_len(p["N_W"])), "ln": um(parse_len(p["N_L"])),
              **extra}
    cell = ly.create_cell("inverter", LIB, params)
    if cell is None or cell.dbbox().empty():
        sys.exit(f"cannot create inverter {params} from PCell library {LIB}")
    return cell


def write_cdl(path, name, p, out_pin="Y"):
    y = out_pin
    with open(path, "w") as f:
        f.write(f"* {name}: {p['P_MODEL']} W={p['P_W']} L={p['P_L']}"
                f" / {p['N_MODEL']} W={p['N_W']} L={p['N_L']}\n")
        f.write(f".SUBCKT {name} A {y} VDD VSS\n")
        f.write(f"MMP {y} A VDD VDD {p['P_MODEL']} W={p['P_W']} L={p['P_L']}\n")
        f.write(f"MMN {y} A VSS VSS {p['N_MODEL']} W={p['N_W']} L={p['N_L']}\n")
        f.write(".ENDS\n")


def labels(cell):
    """{text: DPoint} of the Metal1 labels of a cell (all levels)."""
    ly = cell.layout()
    li = ly.find_layer(*M1_LBL)
    out = {}
    it = cell.begin_shapes_rec(li)
    while not it.at_end():
        if it.shape().is_text():
            out[it.shape().text_string] = it.shape().dtext.transformed(it.dtrans()).position()
        it.next()
    return out


def make_framed(out, name, inv):
    """inverter_base frame + the inverter (flattened, centred) + Metal1 straps to the pin strips."""
    src = pya.Layout()
    src.read(FRAME_GDS)
    base = src.top_cell()
    cell = out.create_cell(name)
    cell.copy_tree(base)
    m1 = out.layer(*M1)
    strip = {}                                   # pin -> frame Metal1 strip (DBox)
    for pin, pt in labels(base).items():
        for s in cell.shapes(m1).each():
            if s.dbox.contains(pt):
                strip[pin] = s.dbox
    assert set(strip) == {"A", "Q", "VDD", "VSS"}, f"{FRAME_GDS}: pin strips {sorted(strip)}"

    ily = inv.layout()
    bb = inv.dbbox()
    dv = pya.DVector(round(-bb.center().x, 3), round(-bb.center().y, 3))
    for li in ily.layer_indexes():
        info = ily.get_info(li)
        if (info.layer, info.datatype) in (M1_LBL, BND):
            continue                             # the frame brings the labels and the outline
        r = pya.Region(inv.begin_shapes_rec(li))
        if not r.is_empty():
            cell.shapes(out.layer(info)).insert(r.moved(dv.to_itype(out.dbu)))
    pins = {k: v + dv for k, v in labels(inv).items()}
    x0, y0, x1, y1 = bb.left + dv.x, bb.bottom + dv.y, bb.right + dv.x, bb.top + dv.y
    # A / Y on the cell edges at their label height, VDD / VSS rails at the top / bottom
    ya, yq = pins["A"].y, pins["Y"].y
    cell.shapes(m1).insert(pya.DBox(strip["A"].right, ya - 0.2, x0 + 0.3, ya + 0.2))
    cell.shapes(m1).insert(pya.DBox(x1 - 0.3, yq - 0.2, strip["Q"].left, yq + 0.2))
    cell.shapes(m1).insert(pya.DBox(x0, y1 - 0.3, x1, strip["VDD"].bottom))
    cell.shapes(m1).insert(pya.DBox(x0, strip["VSS"].top, x1, y0 + 0.3))
    return cell


def main():
    args = sys.argv[1:]
    only = None
    frame = "--no-frame" not in args
    args = [a for a in args if a != "--no-frame"]
    if "--only" in args:
        i = args.index("--only")
        only = {int(v) for v in args[i + 1].split(",")}
        del args[i:i + 2]
    path = args[0] if args else os.path.join(HERE, "dut_params.csv")
    rows = read_csv(path)

    gf180mcu()
    ly = pya.Layout()
    ly.dbu = 0.001

    # Common outline: reserve the largest nfet / pfet W and the widest cell of all DUTs
    wn_slot = max(um(parse_len(p["N_W"])) for _, p in rows)
    wp_slot = max(um(parse_len(p["P_W"])) for _, p in rows)
    cell_w = max(make_inv(ly, p).dbbox().width() for _, p in rows)

    os.makedirs(OUT_DIR, exist_ok=True)
    first = True
    for num, p in rows:
        if only is not None and num not in only:
            continue
        inv = make_inv(ly, p, wn_slot=wn_slot, wp_slot=wp_slot, cell_w=cell_w)
        if first:
            bb = inv.dbbox()
            print(f"cell outline {bb.width():.2f} x {bb.height():.2f} um"
                  f" (nfet W<={wn_slot:.2f}, pfet W<={wp_slot:.2f})")
            first = False
        name = f"inv_dut_{num:03d}"
        out = pya.Layout()
        out.dbu = ly.dbu
        if frame:
            make_framed(out, name, inv)
        else:
            out.create_cell(name).copy_tree(inv)
        out.write(os.path.join(OUT_DIR, f"{name}.gds"))
        write_cdl(os.path.join(OUT_DIR, f"{name}.cdl"), name, p, "Q" if frame else "Y")
        print(f"layout/{name}.gds: {p['P_MODEL']} W={p['P_W']} L={p['P_L']}"
              f" / {p['N_MODEL']} W={p['N_W']} L={p['N_L']}")


if __name__ == "__main__":
    main()
