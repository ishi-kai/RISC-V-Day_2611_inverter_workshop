#!/usr/bin/env python3
"""Generate the top-level layout of workshop_inverter.sch (vco_top) as GDS.

Existing layouts are used as cells as-is:
  vco/vco_only.gds                            VCO + mode switch TGs
  inverter_base.gds                           DUT placeholder -> 128 cells inv_dut_000..127
  inverter_matrix/tgate_5v0_in.gds            input TG (+SELB inverter, MPD, DANT)
  inverter_matrix/tgate_5v0_out.gds           output TG (+SELB inverter)
  librelane-tg-logic/.../decoder_7to128.gds   7->128 decoder (LibreLane)
Vias (via_dev) and the D[6:0] antenna diodes (diode_nw2ps) are PCells of the GF180MCU
KLayout library; every via_dev has 2 (signal) or 4 (power) cuts per level.

Floorplan (700 x 1000 um, y up):
  top     ISHIKAI structural-colour logo (Metal5, ~/str_color/make_ishikai.py)
  upper   VCO (left, top aligned with the decoder, VCTRL / VCO_EN / FOUT pins on the top
          edge), decoder (right, D[6:0] pins on the right edge, antenna diodes above its inputs)
  middle  SEL fan-out (decoder outputs -> per-column M4 tracks)
  bottom  16 x 8 tiles of 40 x 78 um: SEL channel | mux band + 20 x 50 um DUT area
  left    M4 trunks (VSS, VDD_DEC, VDD_INV, MIN, MOUT), IN / OUT pins; power pins at the bottom

Tile (tile-local um): x 0..6 SEL tracks (M4), x 7..38 mux band (y 0..26.2) under the DUT
area (x 18..38, y 27..77).  Nothing is routed over a DUT area: A / Q / VDD / VSS are
reached by M1 stubs that abut the cell edge from outside.

Layer usage outside the cells:
  M1 rail extensions and pin stubs, M2 local verticals / power straps / fan-out verticals,
  M3 row buses (MIN, MOUT), SEL jogs, fan-out horizontals, D[6:0], IN / OUT,
  M4 SEL tracks, DUT_IN / DUT_OUT escapes, trunks, VCO pins,
  M5 per-row power stripes, decoder power, MIN / VDD_INV links to the VCO.

Usage:  python3 gen_top_layout.py [out.gds]
"""
import csv
import os
import sys

import pya

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
INV_DIR = os.path.join(ROOT, "inverter_matrix")
INV_BASE = os.path.join(ROOT, "inverter_base.gds")
VCO_GDS = os.path.join(ROOT, "vco", "vco_only.gds")
DEC_GDS = os.path.join(ROOT, "librelane-tg-logic", "config", "runs",
                       "RUN_2026-10-11_15-58-21", "final", "gds", "decoder_7to128.gds")
# PCell library (same source as inverter_matrix/gen_layout.py; the via_dev PCell of
# ~/pdk/gf180mcuD fails to produce)
PCELL_PDK = os.environ.get("GF180_PDK") or os.path.expanduser("~/src/gf180mcuD")
sys.path.insert(0, os.path.join(PCELL_PDK, "libs.tech/klayout/tech/pymacros"))
import gdsfactory as gf  # noqa: E402
# ISHIKAI logo generator
sys.path.insert(0, os.path.expanduser("~/str_color"))
import make_ishikai  # noqa: E402

gf.gpdk.PDK.activate()   # $PDK=gf180mcuD would otherwise make gdsfactory look for a python module
from cells import gf180mcu  # noqa: E402

LIB = "gf180mcu"
TOP = "workshop_inverter"
CHIP_W, CHIP_H = 700.0, 1000.0

# ---- tile geometry (tile-local um) ----
NCOL, NROW = 16, 8
TILE_W, TILE_H = 40.0, 78.0
ARR_X0, ARR_Y0 = 36.0, 20.0           # array bottom-left (bottom row band)
INV_C = (28.0, 52.0)                  # DUT cell centre; DUT area x 18..38, y 27..77
INV_W, INV_H = 20.0, 50.0
TRK_X0, TRK_P, TRK_W = 0.8, 0.7, 0.3  # SEL tracks (M4), track k = row k
XA, XQ = 7.5, 38.9                    # DUT_IN / DUT_OUT escapes (M4)
XS, XD = 9.4, 11.1                    # VSS / VDD_DEC straps (M2)
TGX, TGIN_Y, TGOUT_Y = 16.08, 4.0, 15.2   # tgate origins (cell-local origin)
X_IN, X_OUT = 25.63, 27.23            # IN / OUT verticals (M2)
SEL_JOG_Y = 13.2                      # M3 SEL jog between tgate_in and tgate_out
MIN_BUS_Y, MOUT_BUS_Y = 2.4, 24.0     # M3 row buses
STRIPES = {"VDD_INV": (0.0, 1.2), "VDD_DEC": (8.0, 9.6), "VSS": (24.6, 26.2)}  # M5
STUB_X = (30.0, 36.0)                 # VSS / VDD_INV M1 stubs of the DUT area
TG_W = (-3.68, 8.65)                  # tgate cell x extent (cell-local)

# ---- global placement ----
TRUNK = {"VSS": (3.0, 7.0), "VDD_DEC": (9.0, 13.0), "VDD_INV": (15.0, 19.0),
         "MIN": (22.0, 23.5), "MOUT": (26.0, 27.5)}   # M4 verticals
DEC_O = (480.0, 756.0)
FAN_Y0, FAN_P = 752.0, 0.8            # fan-out track of dec_out[i] at FAN_Y0 - FAN_P * i
VCO_O = (60.0, 842.5)                 # VCO top (842.5 + 13.32) ~ decoder top (856)
X_EN, X_CTRL = 40.0, 44.0             # VCO_EN / VCTRL M4 verticals to the top edge
Y_OUT, Y_IN = VCO_O[1] - 20.0, VCO_O[1] - 23.0   # OUT / IN M3 lines to the left edge
MIN_LINK_Y = VCO_O[1] - 27.0          # M5 from VCO INV_IN to the MIN trunk
DIODE_DY = 101.3                      # antenna diode origin above the decoder (decoder-local)
DIODE_VSS_X = 690.0                   # M4 feeder from decoder VSS stripe to the diode anodes
# ISHIKAI logo (Metal5 gratings, 45 deg illumination) between the FOUT pin and the right
# edge, above the VCO / decoder D[6:0] lines; same proportions as the 500 x 100 um original
LOGO_LAYER, LOGO_THETA = "Metal5", 45.0
LOGO_PX, LOGO_W, LOGO_H = 11.0, 550.0, 110.0
LOGO_O = (137.5, 878.0)

gf180mcu()
ly = pya.Layout()
ly.dbu = 0.001
LAY = {n: ly.layer(l, d) for n, (l, d) in {
    "M1": (34, 0), "M2": (36, 0), "M3": (42, 0), "M4": (46, 0), "M5": (81, 0),
    "M1L": (34, 10), "M2L": (36, 10), "M3L": (42, 10), "M4L": (46, 10), "M5L": (81, 10),
    "BND": (0, 0)}.items()}
V2 = (1.2, 0.4)      # 2-cut via, horizontal
V2V = (0.4, 1.2)     # 2-cut via, vertical
V4 = (1.2, 1.2)      # 2 x 2 cuts


def box(cell, layer, x1, y1, x2, y2):
    cell.shapes(LAY[layer]).insert(pya.DBox(min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)))


def hline(cell, layer, x1, x2, y, w):
    box(cell, layer, x1, y - w / 2, x2, y + w / 2)


def vline(cell, layer, x, y1, y2, w):
    box(cell, layer, x - w / 2, y1, x + w / 2, y2)


def label(cell, layer, text, x, y):
    cell.shapes(LAY[layer]).insert(pya.DText(text, pya.DTrans(pya.DVector(x, y))))


def place(parent, child, x, y, rot=0):
    parent.insert(pya.DCellInstArray(child.cell_index(), pya.DCplxTrans(1, rot, False, x, y)))


_vias = {}


def via(cell, x, y, lo, hi, size):
    """via_dev PCell (Mlo .. Mhi, all levels size[0] x size[1]) centred at (x, y)."""
    w, h = size
    key = (lo, hi, w, h)
    if key not in _vias:
        c = ly.create_cell("via_dev", LIB, {"base_layer": f"M{lo}", "metal_level": f"M{hi}",
                                            "x_max": w, "y_max": h})
        if c is None or c.dbbox().empty():
            sys.exit(f"cannot create via_dev {key} from PCell library {LIB}")
        _vias[key] = c
    place(cell, _vias[key], x - w / 2, y - h / 2)


def load(path):
    src = pya.Layout()
    src.read(path)
    s = src.top_cell()
    c = ly.create_cell(s.name)
    c.copy_tree(s)
    return c


def read_dut_list():
    with open(os.path.join(INV_DIR, "dut_params.csv")) as f:
        rows = [r for r in csv.reader(f) if r and r[0].strip().isdigit()]
    return [int(r[0]) for r in rows]


# ------------------------------------------------------------------ cells
def make_duts(duts):
    """inv_dut_NNN: copies of inverter_base (to be replaced by the real DUT layouts)."""
    src = pya.Layout()
    src.read(INV_BASE)
    base = src.top_cell()
    bb = base.dbbox()
    assert abs(bb.width() - INV_W) < 1e-6 and abs(bb.height() - INV_H) < 1e-6, bb
    assert bb.center() == pya.DPoint(0, 0), "inverter_base origin must be its centre"
    cells = []
    for n in duts:
        c = ly.create_cell(f"inv_dut_{n:03d}")
        c.copy_tree(base)
        cells.append(c)
    return cells


def make_mux(tg_in, tg_out):
    """Everything of a tile except the DUT and its SEL track (identical for all channels)."""
    c = ly.create_cell("mux_ch")
    place(c, tg_in, TGX, TGIN_Y)
    place(c, tg_out, TGX, TGOUT_Y)
    x0, x1 = TGX + TG_W[0], TGX + TG_W[1]
    # SEL: tgate_in SEL (M2, top edge) <-> tgate_out SEL (M2, bottom edge), M3 jog lands here
    sx = TGX - 0.57
    vline(c, "M2", sx, SEL_JOG_Y - 0.6, SEL_JOG_Y + 0.6, 0.4)
    via(c, sx, SEL_JOG_Y, 2, 3, V2V)
    # rails -> M2 straps on the left -> M5 stripes
    for oy in (TGIN_Y, TGOUT_Y):
        box(c, "M1", XD - 0.6, oy + 6.145, x0, oy + 7.145)   # VDD_DEC
        box(c, "M1", XS - 0.6, oy + 7.39, x0, oy + 7.99)     # VSS
        via(c, XD, oy + 6.645, 1, 2, (1.2, 0.8))
        via(c, XS, oy + 7.69, 1, 2, (1.2, 0.6))
    vss_y, vdd_y = sum(STRIPES["VSS"]) / 2, sum(STRIPES["VDD_DEC"]) / 2
    vline(c, "M2", XS, TGIN_Y + 7.69, vss_y, 0.6)
    vline(c, "M2", XD, vdd_y, TGOUT_Y + 6.645, 0.6)
    via(c, XS, vss_y, 2, 5, V4)
    via(c, XD, vdd_y, 2, 5, V4)
    # IN: tgate_in IN bus (M1, top edge) -> M2 down -> M3 row bus MIN
    box(c, "M1", x1 - 0.1, TGIN_Y + 8.285, X_IN + 0.6, TGIN_Y + 8.785)
    via(c, X_IN, TGIN_Y + 8.535, 1, 2, (1.2, 0.5))
    vline(c, "M2", X_IN, MIN_BUS_Y, TGIN_Y + 8.535, 0.4)
    via(c, X_IN, MIN_BUS_Y, 2, 3, V2)
    # OUT: tgate_out OUT bus (M1, bottom edge) -> M2 up -> M3 row bus MOUT
    box(c, "M1", x1 - 0.1, TGOUT_Y - 2.085, X_OUT + 0.6, TGOUT_Y - 1.585)
    via(c, X_OUT, TGOUT_Y - 1.835, 1, 2, (1.2, 0.5))
    vline(c, "M2", X_OUT, TGOUT_Y - 1.835, MOUT_BUS_Y, 0.4)
    via(c, X_OUT, MOUT_BUS_Y, 2, 3, V2)
    # DUT_IN pad (M2-M5 stack in tgate_in) -> M4 left -> M4 up the channel -> M1 stub to A
    ix, iy = INV_C
    y = TGIN_Y - 0.485
    hline(c, "M4", XA - 0.25, TGX + 3.155, y, 0.6)
    vline(c, "M4", XA, y - 0.3, iy + 0.2, 0.5)
    via(c, XA, iy, 1, 4, V2)
    hline(c, "M1", XA, ix - INV_W / 2, iy, 0.4)
    # DUT_OUT pad (M2-M5 stack in tgate_out) -> M4 right -> M4 up the gap -> M1 stub to Q
    y = TGOUT_Y + 4.515
    hline(c, "M4", TGX + 3.255, XQ + 0.25, y, 0.6)
    vline(c, "M4", XQ, y - 0.3, iy + 0.2, 0.5)
    via(c, XQ, iy, 1, 4, V2)
    hline(c, "M1", ix + INV_W / 2, XQ, iy, 0.4)
    # DUT VSS strip (bottom edge) -> own VSS stripe; DUT VDD strip (top edge) -> VDD_INV
    # stripe of the band above (tile-local y TILE_H + 0..1.2)
    sx0, sx1 = STUB_X
    xm = (sx0 + sx1) / 2
    ybot, ytop = iy - INV_H / 2, iy + INV_H / 2
    box(c, "M1", sx0, STRIPES["VSS"][0] + 0.2, sx1, ybot)
    via(c, xm, vss_y, 1, 5, V4)
    vdd_y = TILE_H + sum(STRIPES["VDD_INV"]) / 2
    box(c, "M1", sx0, ytop, sx1, TILE_H + STRIPES["VDD_INV"][1])
    via(c, xm, vdd_y, 1, 5, V4)
    return c


def make_diodes(top, diode, dec):
    """D[6:0]: pins on the right edge, antenna diode next to each decoder input."""
    dx, dy = DEC_O
    m1 = sorted((p.bbox() for p in pya.Region(diode.begin_shapes_rec(LAY["M1"])).each()),
                key=lambda b: b.left)
    an, ca = (b.to_dtype(ly.dbu) for b in m1)        # P+ tap (VSS), N+ in Nwell (D)
    yc = dy + DIODE_DY + an.center().y
    vss_y = yc - 0.9
    xs = []
    for k in range(7):
        px = dx + 15.96 + 28 * k                      # dec_in[k] pin centre (M2, top edge)
        yk = dy + 103.4 + 1.0 * (6 - k)
        ox = px - 3.0
        place(top, diode, ox, dy + DIODE_DY)
        # cathode -> D
        hline(top, "M1", ox + ca.left, px + 0.6, yc, 0.4)
        via(top, px, yc, 1, 2, V2)
        # anode -> VSS line
        ax = ox + an.center().x
        via(top, ax, yc, 1, 3, V2V)
        xs.append(ax)
        # D[k]: pin -> M2 up -> M3 to the right edge
        vline(top, "M2", px, dy + 99.44, yk + 0.25, 0.56)
        via(top, px + 0.32, yk, 2, 3, (1.2, 0.5))
        hline(top, "M3", px - 0.28, CHIP_W, yk, 0.5)
        label(top, "M3L", f"D[{k}]", CHIP_W - 0.3, yk)
    hline(top, "M3", xs[0] - 0.2, DIODE_VSS_X + 0.6, vss_y, 0.6)
    via(top, DIODE_VSS_X, vss_y, 3, 4, (1.2, 0.6))
    vline(top, "M4", DIODE_VSS_X, dy + 35.63, vss_y, 0.6)
    via(top, DIODE_VSS_X, dy + 35.63, 4, 5, V4)
    box(top, "M5", dx + 190.0, dy + 34.83, DIODE_VSS_X + 0.6, dy + 36.43)


# ------------------------------------------------------------------ build
def tile_origin(n):
    """DUT n at row n // 16 (row 0 = top), column n % 16."""
    r, col = divmod(n, NCOL)
    return ARR_X0 + TILE_W * col, ARR_Y0 + TILE_H * (NROW - 1 - r)


def build():
    top = ly.create_cell(TOP)
    duts = read_dut_list()
    assert duts == list(range(NCOL * NROW)), "dut_params.csv must list DUT 000..127"

    tg_in = load(os.path.join(INV_DIR, "tgate_5v0_in.gds"))
    tg_out = load(os.path.join(INV_DIR, "tgate_5v0_out.gds"))
    mux = make_mux(tg_in, tg_out)
    vco = load(VCO_GDS)
    dec = load(DEC_GDS)
    diode = ly.create_cell("diode_nw2ps", LIB, {"la": 1.4, "wa": 1.2, "volt": "5/6V"})

    for n, inv in zip(duts, make_duts(duts)):
        tx, ty = tile_origin(n)
        place(top, mux, tx, ty)
        place(top, inv, tx + INV_C[0], ty + INV_C[1])

    arr_x1 = ARR_X0 + TILE_W * NCOL
    for r in range(NROW + 1):              # band NROW = VDD_INV stripe above the top row
        ty = ARR_Y0 + TILE_H * (NROW - 1 - r) if r < NROW else ARR_Y0 + TILE_H * NROW
        # VDD_INV of a band feeds the row below it: none in the bottom band, only it in the top one
        nets = ["VDD_INV"] if r == NROW else ["VDD_DEC", "VSS"] + (["VDD_INV"] if r < NROW - 1 else [])
        for net in nets:
            y1, y2 = STRIPES[net]
            box(top, "M5", TRUNK[net][0], ty + y1, arr_x1, ty + y2)
            via(top, sum(TRUNK[net]) / 2, ty + (y1 + y2) / 2, 4, 5, V4)
        if r == NROW:
            continue
        hline(top, "M3", TRUNK["MIN"][0], arr_x1, ty + MIN_BUS_Y, 0.4)
        via(top, sum(TRUNK["MIN"]) / 2, ty + MIN_BUS_Y, 3, 4, V2)
        hline(top, "M3", TRUNK["MOUT"][0], arr_x1, ty + MOUT_BUS_Y, 0.4)
        via(top, sum(TRUNK["MOUT"]) / 2, ty + MOUT_BUS_Y, 3, 4, V2)

    # ---- decoder and SEL fan-out
    place(top, dec, *DEC_O)
    dx, dy = DEC_O
    for i in range(NCOL * NROW):
        r = i // NCOL
        tx, ty = tile_origin(i)
        xp = dx + 28.28 + 1.12 * i                 # dec_out[i] pin centre (M2, bottom edge)
        xt = tx + TRK_X0 + TRK_P * r               # M4 track of this channel
        yi = FAN_Y0 - FAN_P * i
        # M2 down; the via pad sticks out to the left (dec_out[i-1] ends higher)
        vline(top, "M2", xp, yi - 0.2, dy + 0.56, 0.56)
        via(top, xp - 0.32, yi, 2, 3, V2)
        hline(top, "M3", min(xp - 0.92, xt - 0.15), max(xp + 0.28, xt + 1.05), yi, 0.4)
        # track top: the pad sticks out to the right (tracks of lower rows start lower)
        via(top, xt + 0.45, yi, 3, 4, V2)
        vline(top, "M4", xt, ty + SEL_JOG_Y - 0.2, yi + 0.2, TRK_W)
        # track bottom: the pad sticks out to the left (tracks of upper rows ended higher)
        via(top, xt - 0.45, ty + SEL_JOG_Y, 3, 4, V2)
        hline(top, "M3", xt - 1.05, tx + TGX - 0.37, ty + SEL_JOG_Y, 0.4)

    # decoder power (M5 stripes, local y 31.53..33.13 VDD, 34.83..36.43 VSS)
    box(top, "M5", TRUNK["VDD_DEC"][0], dy + 31.53, dx + 7.0, dy + 33.13)
    via(top, sum(TRUNK["VDD_DEC"]) / 2, dy + 32.33, 4, 5, V4)
    box(top, "M5", TRUNK["VSS"][0], dy + 34.83, dx + 7.0, dy + 36.43)
    via(top, sum(TRUNK["VSS"]) / 2, dy + 35.63, 4, 5, V4)
    make_diodes(top, diode, dec)

    # ---- VCO
    place(top, vco, *VCO_O)
    vx, vy = VCO_O
    # left side M1 hookups (VCO-local y): VDD_DEC, VSS rails, INV_OUT (=MOUT), VCO_EN
    lx = vx + 16.3
    for net, y1, y2, xt in (("VDD_DEC", -6.575, -5.575, sum(TRUNK["VDD_DEC"]) / 2),
                            ("VSS", -5.33, -4.73, sum(TRUNK["VSS"]) / 2),
                            ("MOUT", -4.435, -3.935, sum(TRUNK["MOUT"]) / 2),
                            ("VCO_EN", -3.6, -3.1, X_EN)):
        box(top, "M1", xt - 0.6, vy + y1, lx, vy + y2)
        via(top, xt, vy + (y1 + y2) / 2, 1, 4, (1.2, y2 - y1))
    vline(top, "M4", X_EN, vy - 3.35, CHIP_H, 0.5)
    label(top, "M4L", "VCO_EN", X_EN, CHIP_H - 0.3)
    # VCTRL (M3, left edge)
    box(top, "M3", X_CTRL - 0.6, vy + 3.725, vx - 0.7, vy + 4.925)
    via(top, X_CTRL, vy + 4.325, 3, 4, V4)
    vline(top, "M4", X_CTRL, vy + 4.325, CHIP_H, 0.5)
    label(top, "M4L", "VCTRL", X_CTRL, CHIP_H - 0.3)
    # FOUT (M4, top edge)
    box(top, "M4", vx + 64.8, vy + 13.0, vx + 66.8, CHIP_H)
    label(top, "M4L", "FOUT", vx + 65.8, CHIP_H - 0.3)
    # IN / OUT pads (M3, bottom edge) -> M3 down -> M3 to the left edge
    for name, xc, yl in (("IN", vx + 115.105, Y_IN), ("OUT", vx + 35.45, Y_OUT)):
        vline(top, "M3", xc, yl - 0.25, vy - 15.0, 1.0)
        hline(top, "M3", 0.0, xc + 0.5, yl, 0.5)
        label(top, "M3L", name, 0.3, yl)
    # INV_IN (=MIN, tgate_out OUT bus at the bottom right) -> M5 -> MIN trunk
    box(top, "M1", vx + 132.8, vy - 14.805, vx + 134.9, vy - 14.305)
    via(top, vx + 134.3, vy - 14.555, 1, 5, (1.2, 0.5))
    vline(top, "M5", vx + 134.3, MIN_LINK_Y - 0.6, vy - 14.305, 1.2)
    hline(top, "M5", TRUNK["MIN"][0], vx + 134.9, MIN_LINK_Y, 1.2)
    via(top, sum(TRUNK["MIN"]) / 2, MIN_LINK_Y, 4, 5, V2V)
    # VDD_INV (M2 top rail) -> M5 -> VDD_INV trunk
    yv = vy + 16.0
    box(top, "M2", vx + 131.0, vy + 13.0, vx + 132.0, yv)
    via(top, vx + 131.5, yv, 2, 5, V4)
    hline(top, "M5", TRUNK["VDD_INV"][0], vx + 132.1, yv, 1.2)
    via(top, sum(TRUNK["VDD_INV"]) / 2, yv, 4, 5, V4)

    # ---- trunks (M4) and power pins (bottom edge)
    tops = {"VSS": vy - 4.73, "VDD_DEC": vy - 5.575, "VDD_INV": yv + 0.6,
            "MIN": MIN_LINK_Y + 0.6, "MOUT": vy - 3.935}
    for net, (x1, x2) in TRUNK.items():
        y0 = 0.0 if net.startswith("V") else ARR_Y0 + MIN_BUS_Y - 0.6
        box(top, "M4", x1, y0, x2, tops[net])
        if y0 == 0.0:
            label(top, "M4L", net, (x1 + x2) / 2, 0.3)

    # ---- ISHIKAI logo (dummy fill excluded by its PMNDMY marker)
    logo, *_ = make_ishikai.build_cell(ly, LOGO_LAYER, "ISHIKAI", LOGO_THETA, LOGO_PX,
                                       LOGO_W, LOGO_H)
    logo.shapes(ly.layer(*make_ishikai.PMNDMY)).insert(
        pya.DBox(0, 0, LOGO_W, LOGO_H).to_itype(ly.dbu))
    place(top, logo, *LOGO_O)

    box(top, "BND", 0, 0, CHIP_W, CHIP_H)
    return top


def check_keepout(top):
    """No routing over a DUT area: only the DUT cells themselves may be inside."""
    areas = pya.Region()
    for n in range(NCOL * NROW):
        tx, ty = tile_origin(n)
        cx, cy = tx + INV_C[0], ty + INV_C[1]
        areas.insert(pya.DBox(cx - INV_W / 2, cy - INV_H / 2,
                              cx + INV_W / 2, cy + INV_H / 2).to_itype(ly.dbu))
    bad = 0
    for name in ("M1", "M2", "M3", "M4", "M5"):
        it = top.begin_shapes_rec(LAY[name])
        it.unselect_cells("inv_dut_*")
        r = pya.Region(it)
        bad += (r & areas).count()
    return bad


def check_vias():
    """Every via_dev must have 2..4 cuts on each via level."""
    cuts = [ly.layer(35, 0), ly.layer(38, 0), ly.layer(40, 0), ly.layer(41, 0)]
    bad = []
    for key, c in _vias.items():
        for li in cuts:
            n = c.shapes(li).size()
            if n and not 2 <= n <= 4:
                bad.append((key, ly.get_info(li), n))
    return bad


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, f"{TOP}.gds")
    top = build()
    bb = top.dbbox()
    print(f"{TOP}: bbox {bb}  ({bb.width():.2f} x {bb.height():.2f} um)")
    assert bb.left >= 0 and bb.bottom >= 0 and bb.right <= CHIP_W and bb.top <= CHIP_H, bb
    bad = check_keepout(top)
    print("routing over DUT areas:", bad)
    vbad = check_vias()
    print("via_dev variants:", len(_vias), " bad cut counts:", vbad)
    names = [c.name for c in ly.each_cell()]
    assert len(names) == len(set(names)), "duplicate cell names"
    if bad or vbad:
        sys.exit(1)
    ly.write(out)
    print("wrote", out)


if __name__ == "__main__":
    main()
