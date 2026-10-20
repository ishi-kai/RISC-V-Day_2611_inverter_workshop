#!/usr/bin/env python3
"""Collect RESULT lines from tb_ch*.log into results.csv."""
import collections
import glob
import os

HERE = os.path.dirname(os.path.abspath(__file__))
VC = ("1.5", "2.0", "2.5")
d = collections.defaultdict(dict)
for fn in sorted(glob.glob(os.path.join(HERE, "tb_ch*.log"))):
    for l in open(fn):
        if l.startswith("RESULT"):
            kv = dict(x.split("=") for x in l.split()[1:])
            d[int(kv["ch"])][kv["vctrl"]] = kv
with open(os.path.join(HERE, "results.csv"), "w") as f:
    f.write("DUT," + ",".join(f"f_{v}V_MHz" for v in VC) + "," + ",".join(f"per_{v}V_s" for v in VC)
            + "," + ",".join(f"I_{v}V_mA" for v in VC) + ",A_swing_min_V\n")
    for c in sorted(d):
        r = d[c]
        g = lambda v, k: r[v][k] if v in r else ""
        sw = min(float(r[v]["aswing"]) for v in r)
        f.write(",".join([f"{c:03d}"] + [g(v, "fmhz") for v in VC] + [g(v, "per") for v in VC]
                         + [g(v, "ima") for v in VC] + [str(sw)]) + "\n")
print(f"{len(d)} channels, {sum(len(r) for r in d.values())} points")
