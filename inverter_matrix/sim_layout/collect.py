#!/usr/bin/env python3
"""Collect tb_chNNN.log / tb_ref.log into results.csv and print the checks (summary.txt).

Checks (all 128 channels)
  1. inverter    : VOH >= VINV - 10 mV (IN=0), VOL <= 10 mV (IN=VINV), selected DUT's A follows IN
  2. decoder     : at IN=VINV only inv_dut_<D>'s A is high (> 0.99 VINV), the other 127 < 10 mV
  3. VM          : matrix VM (mean of up/down ramps) within 10 mV of the bare-DUT DC VM
  4. period 32   : ch k, k+32, k+64, k+96 (same DUT sizes) give the same VOH / VOL / VM (<= 2 mV)
  5. P/N ratio   : per (model, L), VM depends on Wp/Wn only (same ratio -> same VM within 30 mV)
                   and rises with Wp/Wn
"""
import collections
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))
N_CH = 128
um = lambda s: float(s.rstrip("u"))


def kv(line):
    return dict(x.split("=") for x in line.split()[1:] if "=" in x)


params = {int(r[0]): r for r in
          list(csv.reader(open(os.path.join(HERE, "../dut_params.csv")), skipinitialspace=True))[1:]}
ref = {int(d["ch"]): d for d in (kv(l) for l in open(os.path.join(HERE, "tb_ref.log")) if l.startswith("REF "))}
res, alist = {}, {}
for ch in range(N_CH):
    fn = os.path.join(HERE, f"tb_ch{ch:03d}.log")
    for l in open(fn) if os.path.exists(fn) else []:
        if l.startswith("RESULT"):
            res[ch] = {k: float(v) for k, v in kv(l).items()}
        elif l.startswith("ALIST"):
            alist[ch] = [float(x) for x in l.split()[2:]]

out, fails = [], collections.defaultdict(list)
rows = []
for ch in range(N_CH):
    p = params[ch]
    if ch not in res or ch not in alist:
        fails["missing"].append(ch)
        continue
    r, v = res[ch], res[ch]["vinv"]
    vm = (r["vm_r"] + r["vm_f"]) / 2
    a = alist[ch]
    others = max(x for k, x in enumerate(a) if k != ch)
    sel = max(range(N_CH), key=lambda k: a[k])
    rf = ref[ch]
    row = dict(DUT=f"{ch:03d}", MODEL=p[1][-4:], P_W=um(p[2]), P_L=um(p[3]), N_W=um(p[5]), N_L=um(p[6]),
               WP_WN=round(um(p[2]) / um(p[5]), 4), VINV=v, VOH=r["voh"], VOL=r["vol"],
               DUT_IN_lo=r["ain_lo"], DUT_IN_hi=r["ain_hi"], VM_up=r["vm_r"], VM_down=r["vm_f"],
               VM=vm, VM_ref=float(rf["vm"]), dVM_mV=(vm - float(rf["vm"])) * 1e3,
               gain_ref=float(rf["gain"]), VIL_ref=float(rf["vil"]), VIH_ref=float(rf["vih"]),
               selected=sel, other_A_max=others, I_VDD_INV_uA=-r["i_lo"] * 1e6)
    rows.append(row)
    if not (r["voh"] >= v - 0.01 and r["vol"] <= 0.01 and abs(r["ain_hi"] - v) <= 0.01 and r["ain_lo"] <= 0.01):
        fails["inverter"].append(ch)
    if not (sel == ch and a[ch] > 0.99 * v and others < 0.01):
        fails["decoder"].append(ch)
    if abs(row["dVM_mV"]) > 10:
        fails["VM vs ref"].append(ch)

with open(os.path.join(HERE, "results.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    for row in rows:
        w.writerow({k: (f"{x:.6g}" if isinstance(x, float) else x) for k, x in row.items()})

by = {int(r["DUT"]): r for r in rows}
lines = ["== period-32 repeat (ch k, k+32, k+64, k+96) =="]
lines.append(" k  model  Wp/Wn   L    VOH spread  VOL spread  VM [V]: k     k+32    k+64    k+96   spread")
worst = 0
for k in range(32):
    g = [by[k + 32 * j] for j in range(4) if k + 32 * j in by]
    if len(g) < 4:
        fails["period-32"].append(k)
        continue
    sp = {q: (max(x[q] for x in g) - min(x[q] for x in g)) * 1e3 for q in ("VOH", "VOL", "VM")}
    worst = max(worst, sp["VM"])
    if max(sp.values()) > 2:
        fails["period-32"].append(k)
    lines.append(f"{k:2d}  {g[0]['MODEL']}  {g[0]['WP_WN']:5.3g}  {g[0]['P_L']:4.2g}   {sp['VOH']:6.3f} mV   "
                 f"{sp['VOL']:6.3f} mV   " + " ".join(f"{x['VM']:.4f}" for x in g) + f"  {sp['VM']:5.2f} mV")
lines.append(f"worst VM spread: {worst:.2f} mV")

lines += ["", "== VM vs P/N ratio (ch 0-31; mean over the 4 repeats) =="]
lines.append("model  L     Wp/Wn  DUTs (Wp/Wn um)                       VM [V]           VM/VINV")
groups = collections.defaultdict(list)
for k in range(32):
    if k in by:
        groups[(by[k]["MODEL"], by[k]["P_L"])].append(k)
for (model, L), ks in groups.items():
    ratios = collections.defaultdict(list)
    for k in ks:
        ratios[round(by[k]["WP_WN"], 1)].append(k)
    prev = None
    for rt in sorted(ratios):
        vms = [sum(by[k + 32 * j]["VM"] for j in range(4)) / 4 for k in ratios[rt]]
        if max(vms) - min(vms) > 0.03:
            fails["P/N ratio"].append(f"{model} L={L} Wp/Wn={rt}: VM {min(vms):.3f}..{max(vms):.3f}")
        if prev is not None and min(vms) <= prev:
            fails["P/N ratio"].append(f"{model} L={L}: VM not rising at Wp/Wn={rt}")
        prev = max(vms)
        sizes = ", ".join(f"{k:03d}({by[k]['P_W']:g}/{by[k]['N_W']:g})" for k in ratios[rt])
        v = by[ratios[rt][0]]["VINV"]
        lines.append(f"{model}  {L:4.2g}  {rt:4.2g}   {sizes:36s}  "
                     + " ".join(f"{x:.3f}" for x in vms) + f"   {sum(vms) / len(vms) / v:.3f}")

lines += ["", "== summary =="]
lines.append(f"channels simulated: {len(rows)} / {N_CH}")
lines.append(f"VOH min: {min(r['VOH'] - r['VINV'] for r in rows) * 1e3:+.3f} mV from VINV, "
             f"VOL max: {max(r['VOL'] for r in rows) * 1e3:.4f} mV")
lines.append(f"unselected DUT inputs at IN=VINV: max {max(r['other_A_max'] for r in rows) * 1e6:.3f} uV")
lines.append(f"VM - VM_ref: {min(r['dVM_mV'] for r in rows):+.2f} .. {max(r['dVM_mV'] for r in rows):+.2f} mV")
for c in ("missing", "inverter", "decoder", "VM vs ref", "period-32", "P/N ratio"):
    lines.append(f"{c:10s}: {'OK' if not fails[c] else 'FAIL ' + str(fails[c])}")
lines.append("RESULT: " + ("PASS" if not any(fails.values()) else "FAIL"))
txt = "\n".join(lines)
open(os.path.join(HERE, "summary.txt"), "w").write(txt + "\n")
print(txt)
