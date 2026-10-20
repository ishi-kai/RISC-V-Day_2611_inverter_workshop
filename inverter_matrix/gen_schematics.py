#!/usr/bin/env python3
"""Generate xschem schematics/symbols for the 128-inverter matrix (GF180MCU).

  dut/inv_dut_000 .. dut/inv_dut_127
                   : one DUT inverter schematic+symbol per channel (pins A, Y, VDD, VSS).
                     Initial content = minimum-size 5V inverter (nfet_05v0 W=0.42u L=0.60u /
                     pfet_05v0 W=0.36u L=0.50u).  These files are meant to be replaced
                     by the supplied DUTs and are NEVER overwritten by this script
                     (delete a file, or run with --reset-dut, to regenerate it).
  inv_ctrl_5v0     : SEL -> SELB control inverter, 5V devices (CTRL_N / CTRL_P)
  tgate_5v0        : transmission gate, nfet_05v0 // pfet_05v0 (TG_N / TG_P)
  mux_ch_5v0       : MUX for one channel: TG_in (IN -> DUT_IN), TG_out (DUT_OUT -> OUT),
                     local SELB inverter, DUT_IN pull-down (nfet_05v0) for SEL=0,
                     antenna diode on SEL (ANT_D)
  inv_array_128    : 128 x (mux_ch_5v0 + inv_dut_NNN), common IN / OUT, SEL[127:0]
  decoder_7to128   : symbol for the LibreLane-hardened 7->128 one-hot decoder
                     (gf180mcu_fd_sc_mcu7t5v0 = nfet_05v0 / pfet_05v0)
  inv_matrix_top   : decoder_7to128 + inv_array_128, antenna diodes on D[6:0] (ANT_D)

Supplies: VDD_INV = DUT inverters only (common to all 128), VDD_DEC = decoder + MUX
control (SELB inverter, TG N-well), VSS common.  VDD_DEC = 5V, VDD_INV <= VDD_DEC.
If any 3.3V-device DUT is present, keep VDD_INV and IN <= 3.3V.

Run:  python3 gen_schematics.py [--reset-dut]
"""
import os
import re
import sys

from xsch_lib import ANT_D, HERE, HEADER, MODEL_MIN, Sch, Sym, inv_sym, inv_sch
RESET_DUT = "--reset-dut" in sys.argv[1:]
N_CH = 128

# MUX device sizes (W, L), chosen for the DUT set in dut_params.csv:
#   DUTs mix 03v3 / 05v0 devices -> VDD_INV = IN <= 3.3V, TG gates swing 0 / VDD_DEC (5V).
#   TG PMOS N-well is on VDD_DEC (5V): body effect weakens it at 0..3.3V, so P = 3 x N.
#   TG_N/TG_P: Ron = 0.93k..1.5k (tt) / 1.1k..2.3k (ss) flat over 0..3.3V
#   (minimum size: 5.7k..17k tt / 28k ss).  Largest DUT gate (~90fF) -> tau ~ 0.14ns.
#   Off-TG junctions on the shared IN / OUT bus: 128 x ~3fF ~ 0.4pF.
TG_N = ("2u", "0.60u")       # nfet_05v0
TG_P = ("6u", "0.50u")       # pfet_05v0
CTRL_N = ("1u", "0.60u")     # SELB inverter: drives 2 x TG_P gates + MPD gate
CTRL_P = ("2u", "0.50u")
DECODER_SPICE = os.path.expanduser(
    "~/librelane-tg-logic/config/runs/RUN_2026-10-11_15-58-21/final/spice/decoder_7to128.spice")

# ---------------------------------------------------------------------------
# 1) inverters: DUT (3v3 / 5v0) and SELB control (5v0)
# ---------------------------------------------------------------------------
def make_inv(name, dev, title, write=True, wp=None, lp=None, wn=None, ln=None):
    sym = inv_sym(name, write=write)
    if write:
        inv_sch(name, title, f"pfet_{dev}", f"nfet_{dev}", wp=wp, lp=lp, wn=wn, ln=ln)
    return sym


# Per-channel DUTs: create only if missing so that supplied DUTs are never overwritten
dut_syms = []
n_new = 0
for i in range(N_CH):
    name = f"dut/inv_dut_{i:03d}"
    new = RESET_DUT or not os.path.exists(os.path.join(HERE, f"{name}.sch"))
    n_new += new
    dut_syms.append(make_inv(name, "05v0",
                             f"DUT #{i} (placeholder: minimum-size 5V inverter) - replace me",
                             write=new))
print(f"DUT schematics: {n_new} created, {N_CH - n_new} kept")


def read_sym_pins(fname):
    """Pin positions from an existing .sym (supplied DUT symbols may differ from ours)."""
    pins = {}
    for line in open(os.path.join(HERE, fname)):
        m = re.match(r"B 5 (\S+) (\S+) (\S+) (\S+) \{.*?name=(\S+)", line)
        if m:
            x = (float(m.group(1)) + float(m.group(3))) / 2
            y = (float(m.group(2)) + float(m.group(4))) / 2
            side = ("L" if x < 0 else "R") if abs(x) >= abs(y) else ("T" if y < 0 else "B")
            pins[m.group(5)] = (round(x, 4), round(y, 4), side)
    return pins


for i, ds in enumerate(dut_syms):
    ds.pins = read_sym_pins(ds.fname)
    if set(ds.pins) != {"A", "Y", "VDD", "VSS"}:
        sys.exit(f"{ds.fname}: pins must be A, Y, VDD, VSS (found {sorted(ds.pins)})")
ctrl_sym = make_inv("inv_ctrl_5v0", "05v0", "SEL -> SELB control inverter, 5V devices",
                    wp=CTRL_P[0], lp=CTRL_P[1], wn=CTRL_N[0], ln=CTRL_N[1])

# ---------------------------------------------------------------------------
# 2) tgate_5v0
# ---------------------------------------------------------------------------
tg_body = ["L 4 -30 -20 30 20 {}", "L 4 -30 20 30 -20 {}", "L 4 -30 -20 -30 20 {}",
           "L 4 30 -20 30 20 {}", "A 4 0 -25 5 0 360 {}",
           "L 4 -40 0 -30 0 {}", "L 4 30 0 40 0 {}"]
tg_sym = Sym("tgate_5v0.sym",
             [("A", "inout", "L"), ("B", "inout", "R"),
              ("EN", "in", "B"), ("ENB", "in", "T"),
              ("VDD", "inout", "T"), ("VSS", "inout", "B")],
             w=80, pitch=30, body=tg_body)

s = Sch()
(wn, ln), (wp, lp) = TG_N, TG_P
s.text("Transmission gate, 5V devices (P = 3 x N: PMOS N-well on VDD_DEC=5V)\n"
       f"nfet_05v0 W={wn} L={ln} // pfet_05v0 W={wp} L={lp}\n"
       "EN=1 / ENB=0 : A <-> B ON   Ron ~1-1.5k (0..3.3V, tt)", -200, -340)
s.fet("nfet_05v0", "MN", 0, 100, d="A", g="EN", s="B", b="VSS", w=wn, l=ln)
s.fet("pfet_05v0", "MP", 0, -100, d="B", g="ENB", s="A", b="VDD", w=wp, l=lp)
s.pin("inout", -300, -200, "A", 1)
s.pin("inout", 300, -200, "B", 2)
s.pin("in", -300, -150, "EN", 3)
s.pin("in", -300, -100, "ENB", 4)
s.pin("inout", 300, -150, "VDD", 5)
s.pin("inout", 300, -100, "VSS", 6)
s.save("tgate_5v0.sch")

# ---------------------------------------------------------------------------
# 3) mux_ch_5v0 : MUX part of one channel (DUT is placed outside, in the array)
# ---------------------------------------------------------------------------
mux_sym = Sym("mux_ch_5v0.sym",
              [("IN", "inout", "L"), ("SEL", "in", "L"),
               ("OUT", "inout", "R"), ("DUT_IN", "inout", "R"), ("DUT_OUT", "inout", "R"),
               ("VDD_DEC", "inout", "T"), ("VSS", "inout", "B")],
              w=140, pitch=20)

s = Sch()
s.text("MUX for one channel:  IN --[TG_in]-- DUT_IN    DUT_OUT --[TG_out]-- OUT\n"
       "SEL=1 : channel selected.  SELB is generated locally.\n"
       "SEL=0 : MPD pulls DUT_IN to VSS (no shoot-through in unselected DUTs).\n"
       "All devices 5V (05v0).  VDD_DEC : SELB inverter + TG N-well (VDD_DEC >= VDD_INV).\n"
       "DANT : antenna diode on the long SEL line (reverse biased, place next to the SEL gates).",
       -300, -480)
s.sub(ctrl_sym, "XSELB", -300, -200, {"A": "SEL", "Y": "SELB", "VDD": "VDD_DEC", "VSS": "VSS"})
s.sub(tg_sym, "XTGIN", -300, 50,
      {"A": "IN", "B": "DUT_IN", "EN": "SEL", "ENB": "SELB", "VDD": "VDD_DEC", "VSS": "VSS"})
s.sub(tg_sym, "XTGOUT", 300, 50,
      {"A": "DUT_OUT", "B": "OUT", "EN": "SEL", "ENB": "SELB", "VDD": "VDD_DEC", "VSS": "VSS"})
s.fet("nfet_05v0", "MPD", -100, 300, d="DUT_IN", g="SELB", s="VSS", b="VSS")
s.diode(ANT_D[0], "DANT", -450, 300, p="VSS", m="SEL", w=ANT_D[1], l=ANT_D[2])
s.pin("inout", -600, -300, "IN", 1)
s.pin("in", -600, -250, "SEL", 2)
s.pin("inout", 600, -300, "OUT", 3)
s.pin("inout", 600, -250, "DUT_IN", 4)
s.pin("inout", 600, -200, "DUT_OUT", 5)
s.pin("inout", 600, -150, "VDD_DEC", 6)
s.pin("inout", 600, -100, "VSS", 7)
s.save("mux_ch_5v0.sch")

# ---------------------------------------------------------------------------
# 4) inv_array_128 : 128 x (mux_ch_5v0 + dut/inv_dut_NNN)
# ---------------------------------------------------------------------------
arr_sym = Sym("inv_array_128.sym",
              [("IN", "inout", "L"), ("SEL[127:0]", "in", "L"), ("OUT", "inout", "R"),
               ("VDD_INV", "inout", "T"), ("VDD_DEC", "inout", "T"), ("VSS", "inout", "B")],
              w=200, pitch=30)
s = Sch()
s.text("128-channel inverter array.  Channel i = mux_ch_5v0 (XMUXi) + dut/inv_dut_i (XDUTi).\n"
       "IN / OUT / VDD_INV / VDD_DEC / VSS common, SEL[127:0] one-hot.", 0, -300, 0.6)
s.pin("inout", 0, -150, "IN", 1)
s.pin("in", 0, -100, "SEL[127:0]", 2)
s.pin("inout", 400, -150, "OUT", 3)
s.pin("inout", 400, -100, "VDD_INV", 4)
s.pin("inout", 400, -50, "VDD_DEC", 5)
s.pin("inout", 700, -150, "VSS", 6)
COLS, DX, DY = 8, 850, 250
for i in range(N_CH):
    cx = 150 + (i % COLS) * DX
    cy = 100 + (i // COLS) * DY
    s.sub(mux_sym, f"XMUX{i}", cx, cy,
          {"IN": "IN", "SEL": f"SEL[{i}]", "OUT": "OUT",
           "DUT_IN": f"DUT_IN[{i}]", "DUT_OUT": f"DUT_OUT[{i}]",
           "VDD_DEC": "VDD_DEC", "VSS": "VSS"})
    s.sub(dut_syms[i], f"XDUT{i}", cx + 300, cy + 20,
          {"A": f"DUT_IN[{i}]", "Y": f"DUT_OUT[{i}]", "VDD": "VDD_INV", "VSS": "VSS"})
s.save("inv_array_128.sch")

# ---------------------------------------------------------------------------
# 5) decoder_7to128 symbol (hardened block, netlisted as primitive)
#    The port order of the extracted .subckt is lexicographic, so a wrapper
#    subckt with xschem's bus order is generated in decoder_7to128_xs.spice.
# ---------------------------------------------------------------------------
dec_pins = [("VDD", "inout", "T"), ("VSS", "inout", "B"),
            ("dec_in[6:0]", "in", "L"), ("dec_out[127:0]", "out", "R")]
dec_fmt = "@name @pinlist decoder_7to128_xs"
Sym("decoder_7to128.sym", dec_pins, w=200, fmt=dec_fmt, title="decoder_7to128")
# make it a primitive (no schematic below it)
p = os.path.join(HERE, "decoder_7to128.sym")
txt = open(p).read().replace("K {type=subcircuit", "K {type=primitive", 1)
open(p, "w").write(txt)
dec_sym_pins = {}
for line in txt.splitlines():
    m = re.match(r"B 5 (\S+) (\S+) (\S+) (\S+) \{name=(\S+)", line)
    if m:
        x = (float(m.group(1)) + float(m.group(3))) / 2
        y = (float(m.group(2)) + float(m.group(4))) / 2
        dec_sym_pins[m.group(5)] = (int(x), int(y))


class _DecSym:
    fname = "decoder_7to128.sym"
    pins = {n: (*dec_sym_pins[n], side) for n, _, side in dec_pins}


# wrapper spice: extract only the decoder subckt (drop black-box std-cell stubs)
with open(DECODER_SPICE) as f:
    src = f.read()
m = re.search(r"^\.subckt decoder_7to128 .*?^\.ends", src, re.S | re.M | re.I)
body = m.group(0)
# drop physical-only cells (endcap/tap/fill/decap) that have no SPICE model in the PDK
body = re.sub(r"\n\+", " \x00", body)
body = "\n".join(l for l in body.splitlines()
                 if not re.search(r"__(endcap|filltie|fill_\d+|fillcap_\d+)\s*$", l))
body = body.replace(" \x00", "\n+")
ports = re.sub(r"\n\+", " ", body.splitlines()[0] + "\n" +
               "\n".join(l for l in body.splitlines()[1:] if l.startswith("+"))).split()[2:]
xs_ports = (["VDD", "VSS"] + [f"dec_in[{i}]" for i in range(6, -1, -1)]
            + [f"dec_out[{i}]" for i in range(127, -1, -1)])
assert sorted(ports) == sorted(xs_ports), "unexpected decoder port list"


def wrap(tokens, prefix):
    out, line = [], prefix
    for t in tokens:
        if len(line) + len(t) + 1 > 100:
            out.append(line)
            line = "+"
        line += " " + t
    out.append(line)
    return "\n".join(out)


os.makedirs(os.path.join(HERE, "spice"), exist_ok=True)
with open(os.path.join(HERE, "spice", "decoder_7to128_xs.spice"), "w") as f:
    f.write("* decoder_7to128 (LibreLane extracted netlist) + xschem port-order wrapper\n"
            "* Needs: .include $PDK_ROOT/gf180mcuD/libs.ref/gf180mcu_fd_sc_mcu7t5v0/spice/"
            "gf180mcu_fd_sc_mcu7t5v0.spice\n\n")
    f.write(body + "\n\n")
    f.write(wrap(xs_ports, ".subckt decoder_7to128_xs") + "\n")
    f.write(wrap(ports + ["decoder_7to128"], "Xdec") + "\n.ends\n")

# ---------------------------------------------------------------------------
# 6) inv_matrix_top
# ---------------------------------------------------------------------------
Sym("inv_matrix_top.sym",
    [("IN", "inout", "L"), ("D[6:0]", "in", "L"), ("OUT", "inout", "R"),
     ("VDD_INV", "inout", "T"), ("VDD_DEC", "inout", "T"), ("VSS", "inout", "B")],
    w=200, pitch=30)
s = Sch()
s.text("Inverter matrix top:  D[6:0] -> decoder_7to128 -> SEL[127:0] -> 128ch TG MUX (in/out)\n"
       "VDD_DEC = 5V : decoder + MUX control + TG N-well     VDD_INV : all DUT inverters     VSS common\n"
       "If any DUT uses 3.3V devices: VDD_INV <= 3.3V and IN <= 3.3V\n"
       "DANT0..6 : antenna diodes on D[6:0] (place next to the decoder input pins)", -400, -450, 0.5)
s.sub(_DecSym, "XDEC", -250, 0,
      {"VDD": "VDD_DEC", "VSS": "VSS", "dec_in[6:0]": "D[6:0]", "dec_out[127:0]": "SEL[127:0]"})
s.sub(arr_sym, "XARR", 250, 0,
      {"IN": "IN", "SEL[127:0]": "SEL[127:0]", "OUT": "OUT",
       "VDD_INV": "VDD_INV", "VDD_DEC": "VDD_DEC", "VSS": "VSS"})
# antenna diodes on the decoder inputs (hard macro: LibreLane only checks routing inside it)
for i in range(7):
    s.diode(ANT_D[0], f"DANT{i}", -1000 + 180 * i, 300, p="VSS", m=f"D[{i}]", w=ANT_D[1], l=ANT_D[2])
s.pin("inout", -650, -250, "IN", 1)
s.pin("in", -650, -200, "D[6:0]", 2)
s.pin("inout", 650, -250, "OUT", 3)
s.pin("inout", 650, -200, "VDD_INV", 4)
s.pin("inout", 650, -150, "VDD_DEC", 5)
s.pin("inout", 650, -100, "VSS", 6)
s.save("inv_matrix_top.sch")

# ---------------------------------------------------------------------------
# xschemrc
# ---------------------------------------------------------------------------
with open(os.path.join(HERE, "xschemrc"), "w") as f:
    f.write("# Load GF180MCU PDK settings, then add this directory\n"
            "source $env(PDK_ROOT)/$env(PDK)/libs.tech/xschem/xschemrc\n"
            "append XSCHEM_LIBRARY_PATH :[file dirname [info script]]\n"
            "set XSCHEM_START_WINDOW [file dirname [info script]]/inv_matrix_top.sch\n")
print("done")
