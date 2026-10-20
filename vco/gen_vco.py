#!/usr/bin/env python3
"""Generate the ring-oscillator VCO that uses the selected DUT inverter of
../inverter_matrix as its 7th stage.

  R0 -[CS1]- R1 -[CS2]- R2 -[CS3]- R3 -[CS4]- R4 -[CS5]- R5 -[CS6]- R6
  ^                                  |                                |
  |                                  +--> buffer --> FOUT             |
  |                                                                   |
  +-- TG_VO --- MOUT <-[ inv_matrix_top : selected DUT ]<- MIN --- TG_VI
               |                                          |
  OUT ------ TG_EO-+                                      +-TG_EI -- IN

  VCO_EN=1 : TG_VI/TG_VO on, TG_EI/TG_EO off -> 7-stage ring (6 CS + DUT)
  VCO_EN=0 : TG_EI/TG_EO on, TG_VI/TG_VO off -> plain inverter matrix (IN/OUT)

Files written (all in this directory):
  cs_inv_5v0.sch/.sym      current-starved inverter (one VCO stage)
  cs_inv_x4_5v0.sch/.sym   same, 4x (CS6: drives the MIN bus)
  vco_bias_5v0.sch/.sym    VCTRL -> VBP/VBN bias generator
  vco_buf1_5v0, vco_buf2_5v0  FOUT buffer inverters
  vco_top.sch/.sym         VCO + mode switch (4 TG, each with its own VCO_EN
                           inverter) + inv_matrix_top
"""
import os
import re
import sys
from types import SimpleNamespace

HERE = os.path.dirname(os.path.abspath(__file__))
MATRIX = os.path.join(HERE, "..", "inverter_matrix")
sys.path.insert(0, MATRIX)
import xsch_lib  # noqa: E402
from xsch_lib import ANT_D, Sch, Sym, inv_sch, inv_sym  # noqa: E402

xsch_lib.HERE = HERE  # write into this directory, not ../inverter_matrix

# ---------------------------------------------------------------------------
# Device sizes (GF180MCU 5V devices; work for VDD_INV = 1.8 .. 5 V)
# Current sources use L=1u for output resistance; 1:1 mirrors from the bias.
# Bias: wide PMOS diode (MPB) + long MNI keep MNI saturated up to VCTRL = VDD,
# so the bias current (and f) keeps rising instead of saturating at ~2 V.
# CS6 drives MIN (TG + 0.6 pF bus of the 128-ch matrix) -> 4x stage.
CS = dict(wpc="16u", lpc="1u", wp="4u", lp="0.50u", wn="2u", ln="0.60u", wnc="4u", lnc="1u")
CS_X4 = dict(wpc="64u", lpc="1u", wp="12u", lp="0.50u", wn="6u", ln="0.60u", wnc="16u", lnc="1u")
BIAS = dict(wpb="16u", lpb="1u", wni="2u", lni="2u", wnm="4u", lnm="1u")
MPD_W, MPD_L = "0.42u", "0.60u"


def ext_sym(path):
    """Read pin positions of an existing symbol (left/right/top/bottom by position)."""
    pins = {}
    for line in open(path):
        m = re.match(r"B 5 (\S+) (\S+) (\S+) (\S+) \{.*?name=(\S+)", line)
        if m:
            x = round((float(m.group(1)) + float(m.group(3))) / 2)
            y = round((float(m.group(2)) + float(m.group(4))) / 2)
            side = ("L" if x < 0 else "R") if abs(x) > abs(y) else ("T" if y < 0 else "B")
            pins[m.group(5)] = (x, y, side)
    return SimpleNamespace(fname=os.path.basename(path), pins=pins)


# ---------------------------------------------------------------------------
# Current-starved inverter
# ---------------------------------------------------------------------------
def cs_cell(name, title, sz):
    sym = Sym(f"{name}.sym",
              [("A", "in", "L"), ("Y", "out", "R"), ("VBP", "in", "T"), ("VDD", "inout", "T"),
               ("VBN", "in", "B"), ("VSS", "inout", "B")], w=100)
    s = Sch()
    s.text(f"{title}, 5V devices\n"
           f"MPC pfet_05v0 W={sz['wpc']} L={sz['lpc']} (gate VBP)   MP pfet_05v0 W={sz['wp']} L={sz['lp']}\n"
           f"MN nfet_05v0 W={sz['wn']} L={sz['ln']}   MNC nfet_05v0 W={sz['wnc']} L={sz['lnc']} (gate VBN)\n"
           f"Stage current = {sz['wpc']}/{BIAS['wpb']} x bias current from vco_bias_5v0", -300, -500)
    s.fet("pfet_05v0", "MPC", 0, -230, d="NP", g="VBP", s="VDD", b="VDD", w=sz["wpc"], l=sz["lpc"])
    s.fet("pfet_05v0", "MP", 0, -80, d="Y", g="A", s="NP", b="VDD", w=sz["wp"], l=sz["lp"])
    s.fet("nfet_05v0", "MN", 0, 80, d="Y", g="A", s="NN", b="VSS", w=sz["wn"], l=sz["ln"])
    s.fet("nfet_05v0", "MNC", 0, 230, d="NN", g="VBN", s="VSS", b="VSS", w=sz["wnc"], l=sz["lnc"])
    s.pin("in", -400, -300, "A", 1)
    s.pin("out", 400, -300, "Y", 2)
    s.pin("in", -400, -250, "VBP", 3)
    s.pin("inout", 400, -250, "VDD", 4)
    s.pin("in", -400, -200, "VBN", 5)
    s.pin("inout", 400, -200, "VSS", 6)
    s.save(f"{name}.sch")
    return sym


cs_sym = cs_cell("cs_inv_5v0", "Current-starved inverter (VCO stage)", CS)
cs4_sym = cs_cell("cs_inv_x4_5v0", "Current-starved inverter x4 (last VCO stage, drives MIN bus)", CS_X4)

# ---------------------------------------------------------------------------
# Bias generator: VCTRL -> I -> VBP (PMOS diode) -> mirror -> VBN (NMOS diode)
# ---------------------------------------------------------------------------
bias_sym = Sym("vco_bias_5v0.sym",
               [("VCTRL", "in", "L"), ("VBP", "out", "R"), ("VBN", "out", "R"),
                ("VDD", "inout", "T"), ("VSS", "inout", "B")], w=140)
s = Sch()
s.text("VCO bias (current-starved VCO), 5V devices\n"
       f"MNI: VCTRL -> I  (nfet_05v0 W={BIAS['wni']} L={BIAS['lni']}, long L: stays saturated)\n"
       f"MPB: PMOS diode -> VBP   MPM/MNM: mirror -> NMOS diode -> VBN\n"
       f"MPB/MPM pfet_05v0 W={BIAS['wpb']} L={BIAS['lpb']}   MNM nfet_05v0 W={BIAS['wnm']} L={BIAS['lnm']}\n"
       "VCTRL = 0 -> I = 0 (VCO off)", -300, -500)
s.fet("pfet_05v0", "MPB", -150, -80, d="VBP", g="VBP", s="VDD", b="VDD", w=BIAS["wpb"], l=BIAS["lpb"])
s.fet("nfet_05v0", "MNI", -150, 80, d="VBP", g="VCTRL", s="VSS", b="VSS", w=BIAS["wni"], l=BIAS["lni"])
s.fet("pfet_05v0", "MPM", 150, -80, d="VBN", g="VBP", s="VDD", b="VDD", w=BIAS["wpb"], l=BIAS["lpb"])
s.fet("nfet_05v0", "MNM", 150, 80, d="VBN", g="VBN", s="VSS", b="VSS", w=BIAS["wnm"], l=BIAS["lnm"])
s.pin("in", -450, -300, "VCTRL", 1)
s.pin("out", 450, -300, "VBP", 2)
s.pin("out", 450, -250, "VBN", 3)
s.pin("inout", 450, -200, "VDD", 4)
s.pin("inout", 450, -150, "VSS", 5)
s.save("vco_bias_5v0.sch")

# ---------------------------------------------------------------------------
# FOUT buffer (restores the slow CS-stage edges, isolates the ring from the pad)
# ---------------------------------------------------------------------------
inv_sch("vco_buf1_5v0", "FOUT buffer stage 1 (small: light load on ring node R3)",
        "pfet_05v0", "nfet_05v0", wp="2u", lp="0.50u", wn="1u", ln="0.60u")
inv_sch("vco_buf2_5v0", "FOUT buffer stage 2 (pad driver)",
        "pfet_05v0", "nfet_05v0", wp="8u", lp="0.50u", wn="4u", ln="0.60u")
buf1_sym = inv_sym("vco_buf1_5v0")
buf2_sym = inv_sym("vco_buf2_5v0")

# ---------------------------------------------------------------------------
# Top: 6 CS stages + mode-switch TGs + inv_matrix_top (7th stage = selected DUT)
# ---------------------------------------------------------------------------
tg = ext_sym(os.path.join(MATRIX, "tgate_5v0.sym"))
ictl = ext_sym(os.path.join(MATRIX, "inv_ctrl_5v0.sym"))
mtx = ext_sym(os.path.join(MATRIX, "inv_matrix_top.sym"))

s = Sch()
s.text("VCO top: 7-stage ring = 6 current-starved stages (CS1..CS5, CS6 = x4) + selected DUT of inv_matrix_top\n"
       "VCO_EN=1 : R6 -> TG_VI -> MIN -> [DUT] -> MOUT -> TG_VO -> R0   (ring, FOUT = buffered R3)\n"
       "VCO_EN=0 : IN -> TG_EI -> MIN -> [DUT] -> MOUT -> TG_EO -> OUT  (inverter mode), MPD holds R0 low\n"
       "VDD_INV : CS stages, bias, FOUT buffer and DUTs (same swing on the whole ring)\n"
       "VDD_DEC (5V) : VCO_EN logic, TG gates/N-well, decoder.   Inverter mode: VCTRL = 0 -> VCO current 0\n"
       "Each TG has its own VCO_EN inverter (VCO_ENB1..4) = TG + inv_ctrl pair of the matrix MUX (layout reuse)\n"
       "DANT2 : antenna diode on VCTRL, DANT3..6 : on VCO_EN, one per inverter (place next to the gates they feed)",
       -900, -930, 0.5)

# bias
s.sub(bias_sym, "X2", -400, -500,
      {"VCTRL": "VCTRL", "VBP": "VBP", "VBN": "VBN", "VDD": "VDD_INV", "VSS": "VSS"})

# six current-starved stages (CS6 = x4: drives the MIN bus through TG_VI)
for i in range(6):
    s.sub(cs4_sym if i == 5 else cs_sym, f"X{i + 3}", -750 + i * 250, -200,
          {"A": f"R{i}", "Y": f"R{i + 1}", "VBP": "VBP", "VDD": "VDD_INV",
           "VBN": "VBN", "VSS": "VSS"})

# ring-input hold: VCO_EN=0 -> R0 = VSS (ring stopped in a defined state);
# gate shares VCO_ENB1 with TG_VO (the TG on R0)
s.fet("nfet_05v0", "MPD", -950, -50, d="R0", g="VCO_ENB1", s="VSS", b="VSS", w=MPD_W, l=MPD_L)

# FOUT buffer from the ring middle (R3), away from the DUT nodes
s.sub(buf1_sym, "X9", 300, -450, {"A": "R3", "Y": "FB", "VDD": "VDD_INV", "VSS": "VSS"})
s.sub(buf2_sym, "X10", 550, -450, {"A": "FB", "Y": "FOUT", "VDD": "VDD_INV", "VSS": "VSS"})

# inverter matrix (7th stage = DUT selected by D[6:0])
s.sub(mtx, "X15", 0, 300,
      {"IN": "MIN", "D[6:0]": "D[6:0]", "OUT": "MOUT",
       "VDD_INV": "VDD_INV", "VDD_DEC": "VDD_DEC", "VSS": "VSS"})

# antenna diode on VCTRL (gate-only input from the pad: MNI gate 4um2)
s.diode(ANT_D[0], "DANT2", -1040, 100, p="VSS", m="VCTRL", w=ANT_D[1], l=ANT_D[2])


# mode-switch transmission gates (same 5V TG as the matrix MUX). Every TG has its
# own VCO_EN inverter, like the TG + inv_ctrl pair in mux_ch_5v0, so the matrix
# TG layout can be reused as is.
def tgate(name, x, y, a, b, en, enb):
    s.sub(tg, name, x, y, {"A": a, "B": b, "EN": en, "ENB": enb, "VDD": "VDD_DEC", "VSS": "VSS"})


tgate("X16", 650, 660, "R6", "MIN", "VCO_EN", "VCO_ENB3")      # TG_VI: ring -> DUT input
tgate("X17", 650, 920, "IN", "MIN", "VCO_ENB4", "VCO_EN")      # TG_EI: pad  -> DUT input
tgate("X18", -650, 670, "MOUT", "R0", "VCO_EN", "VCO_ENB1")    # TG_VO: DUT output -> ring
tgate("X19", -650, 910, "MOUT", "OUT", "VCO_ENB2", "VCO_EN")   # TG_EO: DUT output -> pad
for name, x, y, enb in [("X20", 320, 660, "VCO_ENB3"), ("X21", 320, 920, "VCO_ENB4"),
                        ("X22", -330, 670, "VCO_ENB1"), ("X23", -330, 910, "VCO_ENB2")]:
    s.sub(ictl, name, x, y, {"A": "VCO_EN", "Y": enb, "VDD": "VDD_DEC", "VSS": "VSS"})

# antenna diodes on VCO_EN (4 inverters + 4 TG gates): one per inverter, as in mux_ch_5v0
# (VBP/VBN/VCO_ENB1..4 have drains on them -> no diode)
for name, x, y in [("DANT3", -80, 670), ("DANT4", 100, 670), ("DANT5", -90, 920), ("DANT6", 90, 920)]:
    s.diode(ANT_D[0], name, x, y, p="VSS", m="VCO_EN", w=ANT_D[1], l=ANT_D[2])

ports = [("in", "VCTRL"), ("in", "VCO_EN"), ("in", "D[6:0]"), ("inout", "IN"),
         ("inout", "OUT"), ("out", "FOUT"), ("inout", "VDD_INV"), ("inout", "VDD_DEC"),
         ("inout", "VSS")]
for n, (kind, net) in enumerate(ports, 1):
    x = -1300 if kind == "in" else 1300
    s.pin(kind, x, -700 + 50 * n, net, n)
s.save("vco_top.sch")

Sym("vco_top.sym",
    [("VCTRL", "in", "L"), ("VCO_EN", "in", "L"), ("D[6:0]", "in", "L"), ("IN", "inout", "L"),
     ("OUT", "inout", "R"), ("FOUT", "out", "R"),
     ("VDD_INV", "inout", "T"), ("VDD_DEC", "inout", "T"), ("VSS", "inout", "B")], w=200)

print("written: cs_inv_5v0, cs_inv_x4_5v0, vco_bias_5v0, vco_buf1_5v0, vco_buf2_5v0, vco_top (.sch/.sym)")
