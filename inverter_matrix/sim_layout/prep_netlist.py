#!/usr/bin/env python3
"""Convert the KLayout-extracted netlist of workshop_inverter.gds for ngspice.

Same conversion as ../../vco/sim_layout/prep_netlist.py ('\\$I123' -> n_I123, M -> XM, diode
A=/P= -> area=/pj=), written here so this directory does not depend on the VCO run.
Also writes dut_nodes.txt (DUT name, A net, Q net).
Usage: python3 prep_netlist.py [../../layout/workshop_inverter_extracted.cir]
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "../../layout/workshop_inverter_extracted.cir")

out, duts = [], []
for line in open(src):
    line = line.replace("\\$", "n_").replace("$", "_")
    if line.startswith("M"):
        line = "X" + line  # PDK MOS models are subcircuits
    if line.startswith("D"):
        line = re.sub(r"\bA=", "area=", line)
        line = re.sub(r"\bP=", "pj=", line)
    m = re.match(r"X\S+ (\S+) (\S+) VDD_INV VSS (inv_dut_\d{3})\s*$", line)
    if m:
        duts.append((m.group(3), m.group(2), m.group(1)))  # name, A, Q
    out.append(line)
open(os.path.join(HERE, "workshop_inverter_layout.cir"), "w").writelines(out)
with open(os.path.join(HERE, "dut_nodes.txt"), "w") as f:
    for d in sorted(duts):
        f.write(" ".join(d) + "\n")
print(f"{len(duts)} DUT instances")
