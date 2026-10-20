#!/usr/bin/env python3
"""Inverter-mode DC testbenches on the layout-extracted workshop_inverter (all 128 channels).

tb_chNNN.spice : D[6:0] = NNN (static), VCO_EN = VCTRL = 0 (inverter mode).
  VDD_INV and the IN swing follow the DUT's device rating (from dut_params.csv):
  5V devices (*_05v0) -> 0..5.0 V, 3.3V devices (*_03v3) -> 0..3.3 V.
  Transient (a DC sweep of the full chip needs gmin stepping at every point and takes hours):
  IN = 0 -> VINV -> 0, slow (0.5 V/us) only across VM_ref +- 0.4 V.  VOH (IN=0), VOL (IN=VINV),
  VM (OUT=IN) on both ramps (their mean cancels the lag of the ~0.4 pF OUT bus).
  At IN=VINV the A (input) node of all 128 DUTs is printed, so the decoder check is
  "only inv_dut_NNN's A follows IN, the other 127 stay at VSS".
tb_ref.spice   : the same extracted inv_dut_NNN subcircuits alone (no decoder/MUX), same
  VDD/IN, DC sweep: reference VM, VIL/VIH (gain = -1) and max gain.
Usage: python3 gen_tb.py   (tb_ref.log must exist for tb_chNNN; run tb_ref.spice first)
"""
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PDK = "/home/noritsuna/pdk/gf180mcuD/libs.tech/ngspice"
VDEC = 5.0
STEP = 0.005
N_CH = 128

nodes = {n: (a, q) for n, a, q in (l.split() for l in open(os.path.join(HERE, "dut_nodes.txt")))}
rows = list(csv.reader(open(os.path.join(HERE, "../dut_params.csv")), skipinitialspace=True))[1:]
vinv = {int(r[0]): 5.0 if r[1].endswith("05v0") else 3.3 for r in rows}
models = f""".include {HERE}/workshop_inverter_layout.cir
.include {PDK}/design.ngspice
.lib {PDK}/sm141064.ngspice typical
.lib {PDK}/sm141064.ngspice diode_typical
.options method=gear reltol=1e-4 abstol=1e-13 vntol=1e-7 rshunt=1e12
"""
# Reference VM (bare DUT, DC) from tb_ref.log: IN ramps slowly only across VMref +- WIN, so
# the lag of OUT (OUT bus ~0.4 pF behind TG_out) stays small; elsewhere IN moves in TF.
REF_LOG = os.path.join(HERE, "tb_ref.log")
vm_ref = {int(l.split()[1][3:]): float(l.split()[3][3:])
          for l in (open(REF_LOG) if os.path.exists(REF_LOG) else []) if l.startswith("REF ")}
WIN, TSLOW, TF, THOLD = 0.4, 1.6e-6, 100e-9, 200e-9


def ns(t):
    return f"{t * 1e9:.6g}n"


for ch in range(N_CH if vm_ref else 0):
    v = vinv[ch]
    dut = f"inv_dut_{ch:03d}"
    a, q = nodes[dut]
    lo, hi = vm_ref[ch] - WIN, vm_ref[ch] + WIN
    # breakpoints (t, V): hold 0 / fast to lo / slow to hi / fast to v / hold / back the same way
    pts, t = [(0, 0), (THOLD, 0)], THOLD
    for vv, dt in ((lo, TF), (hi, TSLOW), (v, TF), (v, THOLD), (hi, TF), (lo, TSLOW), (0, TF), (0, THOLD)):
        t += dt
        pts.append((t, vv))
    tlo, thi = THOLD - 10e-9, THOLD + TSLOW + 2 * TF + THOLD - 10e-9   # IN=0, IN=VINV
    tup, tdn = THOLD + TF, THOLD + TSLOW + 3 * TF + THOLD             # start of the slow ramps
    pwl = " ".join(f"{ns(tt)} {vv:.6g}" for tt, vv in pts)
    d_src = "\n".join(f"VD{i} D[{i}] 0 {VDEC if ch >> i & 1 else 0}" for i in range(7))
    a_meas = "\n".join(f"meas tran a{k:03d} find v(xtop.{nodes[f'inv_dut_{k:03d}'][0]}) at={ns(thi)}"
                       for k in range(N_CH))
    a_echo = " ".join(f"$&a{k:03d}" for k in range(N_CH))
    tb = f"""* Inverter mode test on layout-extracted workshop_inverter, {dut} (VINV={v})
{models}XTOP {" ".join(f"D[{i}]" for i in range(7))} FOUT IN OUT VCO_EN VCTRL VDD_DEC VDD_INV 0 workshop_inverter
VDDD VDD_DEC 0 {VDEC}
VDDI VDD_INV 0 {v}
VCT VCTRL 0 0
VEN VCO_EN 0 0
VIN IN 0 PWL({pwl})
{d_src}
.control
tran 1n {ns(pts[-1][0])} 0 5n
let d = v(out)-v(in)
meas tran voh find v(out) at={ns(tlo)}
meas tran vol find v(out) at={ns(thi)}
meas tran q_lo find v(xtop.{q}) at={ns(tlo)}
meas tran q_hi find v(xtop.{q}) at={ns(thi)}
meas tran ain_lo find v(xtop.{a}) at={ns(tlo)}
meas tran ain_hi find v(xtop.{a}) at={ns(thi)}
meas tran i_lo find i(vddi) at={ns(tlo)}
meas tran i_hi find i(vddi) at={ns(thi)}
meas tran t_vmr when d=0 fall=1 td={ns(tup)}
meas tran t_vmf when d=0 rise=1 td={ns(tdn)}
meas tran vm_r find v(in) at=t_vmr
meas tran vm_f find v(in) at=t_vmf
echo RESULT ch={ch} vinv={v} voh=$&voh vol=$&vol q_lo=$&q_lo q_hi=$&q_hi ain_lo=$&ain_lo ain_hi=$&ain_hi i_lo=$&i_lo i_hi=$&i_hi vm_r=$&vm_r vm_f=$&vm_f
{a_meas}
echo ALIST ch={ch} {a_echo}
.endc
.end
"""
    open(os.path.join(HERE, f"tb_ch{ch:03d}.spice"), "w").write(tb)

# reference: bare DUT subcircuits, one sweep per supply
ref = [f"* Reference: extracted inv_dut_NNN alone (no decoder / MUX)\n{models}"]
for v, tag in ((5.0, "5"), (3.3, "3")):
    ref.append(f"VDD{tag} VDD{tag} 0 {v}\nVIN{tag} IN{tag} 0 0")
    for ch in range(N_CH):
        if vinv[ch] == v:
            ref.append(f"XR{ch:03d} Q{ch:03d} IN{tag} VDD{tag} 0 inv_dut_{ch:03d}")
ctl = [".control"]
for v, tag in ((5.0, "5"), (3.3, "3")):
    ctl.append(f"dc VIN{tag} 0 {v} {STEP}")
    for ch in range(N_CH):
        if vinv[ch] == v:
            ctl += [f"let d = v(q{ch:03d})-v(in{tag})",
                    f"let g = deriv(v(q{ch:03d}))",
                    "meas dc vm when d=0",
                    "meas dc gmax min g",
                    "meas dc vil when g=-1 fall=1",
                    "meas dc vih when g=-1 rise=1",
                    f"echo REF ch={ch} vinv={v} vm=$&vm gain=$&gmax vil=$&vil vih=$&vih"]
ctl += [".endc", ".end"]
open(os.path.join(HERE, "tb_ref.spice"), "w").write("\n".join(ref + ctl) + "\n")
print(f"tb_ref.spice written; {N_CH if vm_ref else 0} channel testbenches written"
      + ("" if vm_ref else " (run ngspice -b tb_ref.spice > tb_ref.log first)"))
