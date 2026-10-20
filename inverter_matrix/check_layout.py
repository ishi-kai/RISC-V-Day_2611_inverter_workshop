#!/usr/bin/env python3
"""Run GF180MCU KLayout DRC and LVS on layout/inv_dut_NNN.gds (from gen_layout.py).

Results go to layout/drc/ and layout/lvs/; a one-line summary per DUT is printed.
Density checks are skipped (they only make sense on a full chip).

Usage:  python3 check_layout.py [--only 0,5,17] [--jobs N] [--no-drc] [--no-lvs]
"""
import glob
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

import pya

from xsch_lib import HERE

PDK_DIR = os.environ.get("GF180_PDK", os.path.expanduser("~/src/gf180mcuD"))
VARIANT = os.path.basename(os.path.normpath(PDK_DIR))[-1]   # gf180mcuD -> D
TECH = os.path.join(PDK_DIR, "libs.tech/klayout/tech")
LAYOUT = os.path.join(HERE, "layout")
DRC_DECKS = "all,-density"


def run_drc(name):
    out = os.path.join(LAYOUT, "drc")
    rdb = os.path.join(out, f"{name}.lyrdb")
    with open(os.path.join(out, f"{name}.log"), "w") as log:
        subprocess.run(["klayout", "-b", "-r", os.path.join(TECH, "drc/gf180mcu.drc"),
                        "-rd", f"input={os.path.join(LAYOUT, name + '.gds')}",
                        "-rd", f"report={rdb}", "-rd", f"variant={VARIANT}",
                        "-rd", f"decks={DRC_DECKS}", "-rd", "threads=1"],
                       stdout=log, stderr=subprocess.STDOUT)
    if not os.path.exists(rdb):
        return None
    db = pya.ReportDatabase("drc")
    db.load(rdb)
    return {c.name(): c.num_items() for c in db.each_category() if c.num_items()}


def run_lvs(name):
    out = os.path.join(LAYOUT, "lvs", name)
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "lvs.log"), "w") as log:
        subprocess.run([sys.executable, os.path.join(TECH, "lvs/run_lvs.py"),
                        f"--layout={os.path.join(LAYOUT, name + '.gds')}",
                        f"--netlist={os.path.join(LAYOUT, name + '.cdl')}",
                        f"--variant={VARIANT}", f"--topcell={name}", f"--run_dir={out}",
                        "--thr=1"], stdout=log, stderr=subprocess.STDOUT)
    text = open(os.path.join(out, "lvs.log")).read()
    if re.search(r"Congratulations! Netlists match", text):
        return True
    if re.search(r"ERROR : Netlists don't match|Netlists don't match", text):
        return False
    return None


def check(name, do_drc, do_lvs):
    drc = run_drc(name) if do_drc else "skip"
    lvs = run_lvs(name) if do_lvs else "skip"
    return name, drc, lvs


def main():
    args = sys.argv[1:]
    only, jobs = None, os.cpu_count() or 1
    if "--only" in args:
        only = {int(v) for v in args[args.index("--only") + 1].split(",")}
    if "--jobs" in args:
        jobs = int(args[args.index("--jobs") + 1])
    names = sorted(os.path.basename(p)[:-4] for p in glob.glob(os.path.join(LAYOUT, "inv_dut_*.gds")))
    if only is not None:
        names = [n for n in names if int(n[-3:]) in only]
    if not names:
        sys.exit("no layout/inv_dut_*.gds found (run gen_layout.py first)")
    os.makedirs(os.path.join(LAYOUT, "drc"), exist_ok=True)

    bad = 0
    with ThreadPoolExecutor(jobs) as ex:
        for name, drc, lvs in ex.map(lambda n: check(n, "--no-drc" not in args,
                                                     "--no-lvs" not in args), names):
            if drc == "skip":
                d = "DRC skipped"
            elif drc is None:
                d = "DRC FAILED TO RUN"
            else:
                d = "DRC clean" if not drc else \
                    "DRC " + ", ".join(f"{k}:{v}" for k, v in sorted(drc.items()))
            l = {True: "LVS match", False: "LVS MISMATCH", None: "LVS FAILED TO RUN",
                 "skip": "LVS skipped"}[lvs]
            ok = drc in ({}, "skip") and lvs in (True, "skip")
            bad += not ok
            print(f"{'OK ' if ok else 'NG '} {name}: {d} / {l}", flush=True)
    print(f"{len(names) - bad}/{len(names)} DUT(s) clean.")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
