#!/usr/bin/env python3
"""DRC and LVS of workshop_inverter.gds with the GF180MCU KLayout decks.

LVS runs on a copy (lvs/workshop_inverter_lvs.gds) where every cell except the top,
decoder_7to128, the standard cells and inv_dut_NNN is flattened one level at a time:
the reused analog cells (tgate, cs_inv, ...) do not line up 1:1 with the schematic
subcircuits and fail a cell-by-cell compare, although each passes LVS on its own.
--combine merges multi-finger devices (e.g. the 16u / 64u VCO PMOS) before comparing.

Usage:  python3 check_top.py [--gds workshop_inverter.gds] [--no-drc] [--no-lvs] [--threads N]
        (the netlist is the .cdl next to the GDS; reports go to drc/ and lvs/ next to it)
"""
import os
import re
import subprocess
import sys

import klayout.db as db
import klayout.rdb as rdb

HERE = os.path.dirname(os.path.abspath(__file__))
PDK = os.environ.get("GF180_PDK", os.path.expanduser("~/pdk/gf180mcuD"))
TECH = os.path.join(PDK, "libs.tech/klayout/tech")
TOP = "workshop_inverter"
GDS = os.path.join(HERE, f"{TOP}.gds")
CDL = os.path.join(HERE, f"{TOP}.cdl")


def keep(name):
    return name in (TOP, "decoder_7to128") or name.startswith(("gf180mcu_fd_sc", "inv_dut_"))


def run_drc(threads):
    out = os.path.join(os.path.dirname(GDS), "drc")
    os.makedirs(out, exist_ok=True)
    rdb_path = os.path.join(out, f"{TOP}.lyrdb")
    with open(os.path.join(out, "drc.log"), "w") as log:
        subprocess.run(["klayout", "-b", "-r", os.path.join(TECH, "drc/gf180mcu.drc"),
                        "-rd", f"input={GDS}", "-rd", f"report={rdb_path}", "-rd", "variant=D",
                        "-rd", "decks=all,-density", "-rd", f"threads={threads}",
                        "-rd", "run_mode=deep"], stdout=log, stderr=subprocess.STDOUT)
    r = rdb.ReportDatabase("drc")
    r.load(rdb_path)
    return {c.name(): c.num_items() for c in r.each_category() if c.num_items()}


def run_lvs(threads):
    out = os.path.join(os.path.dirname(GDS), "lvs")
    os.makedirs(out, exist_ok=True)
    ly = db.Layout()
    ly.read(GDS)
    changed = True
    while changed:
        changed = False
        for c in list(ly.each_cell()):
            if keep(c.name):
                for inst in list(c.each_inst()):
                    if not keep(inst.cell.name):
                        inst.flatten(1)
                        changed = True
    gds = os.path.join(out, f"{TOP}_lvs.gds")
    ly.write(gds)
    with open(os.path.join(out, "lvs.log"), "w") as log:
        subprocess.run([sys.executable, os.path.join(TECH, "lvs/run_lvs.py"), f"--layout={gds}",
                        f"--netlist={CDL}", "--variant=D", f"--topcell={TOP}",
                        f"--run_dir={out}", f"--thr={threads}", "--combine"],
                       stdout=log, stderr=subprocess.STDOUT)
    text = open(os.path.join(out, "lvs.log")).read()
    if re.search(r"Congratulations! Netlists match", text):
        return True
    if re.search(r"Netlists don't match", text):
        return False
    return None


def main():
    global GDS, CDL
    args = sys.argv[1:]
    if "--gds" in args:
        GDS = os.path.abspath(args[args.index("--gds") + 1])
        CDL = os.path.splitext(GDS)[0] + ".cdl"
    threads = int(args[args.index("--threads") + 1]) if "--threads" in args else os.cpu_count() or 1
    ok = True
    if "--no-drc" not in args:
        drc = run_drc(threads)
        print("DRC clean" if not drc else "DRC " + ", ".join(f"{k}:{v}" for k, v in sorted(drc.items())))
        ok &= not drc
    if "--no-lvs" not in args:
        lvs = run_lvs(threads)
        print({True: "LVS match", False: "LVS MISMATCH", None: "LVS FAILED TO RUN"}[lvs])
        ok &= lvs is True
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
