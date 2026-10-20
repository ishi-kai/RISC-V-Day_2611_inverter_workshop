#!/usr/bin/env python3
"""Generate a VCO-mode testbench on the layout-extracted netlist for one DUT channel.

D[6:0] = channel number selects inv_dut_NNN; VCO_EN rises at 100 ns and FOUT's period is
measured at each VCTRL.  The selected DUT's input (A) swing is measured too, to confirm
that the decoder in the layout really picked that DUT.
Usage: python3 gen_tb.py CH [VCTRL ...]   -> tb_ch<CH>.spice
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PDK = "/home/noritsuna/pdk/gf180mcuD/libs.tech/ngspice"
VDEC, VINV = 5.0, 3.3
TSTOP, TMEAS = "2u", "0.8u"

ch = int(sys.argv[1])
vctrls = sys.argv[2:] or ["1.5", "2.0", "2.5"]
nodes = {n: (a, q) for n, a, q in (l.split() for l in open(os.path.join(HERE, "dut_nodes.txt")))}
dut = f"inv_dut_{ch:03d}"
a, q = nodes[dut]
d_src = "\n".join(f"VD{i} D[{i}] 0 {VDEC if ch >> i & 1 else 0}" for i in range(7))

tb = f"""* VCO on layout-extracted workshop_inverter, {dut}
.include {HERE}/workshop_inverter_layout.cir
.include {PDK}/design.ngspice
.lib {PDK}/sm141064.ngspice typical
.lib {PDK}/sm141064.ngspice diode_typical
.param VCTRL={vctrls[0]}
XTOP {" ".join(f"D[{i}]" for i in range(7))} FOUT IN OUT VCO_EN VCTRL VDD_DEC VDD_INV 0 workshop_inverter
COUT OUT 0 100f
CFOUT FOUT 0 100f
VDDD VDD_DEC 0 {VDEC}
VDDI VDD_INV 0 {VINV}
VCT VCTRL 0 {{VCTRL}}
VEN VCO_EN 0 PULSE(0 {VDEC} 100n 10n 10n 1 2)
VIN IN 0 0
{d_src}
.options method=gear reltol=1e-3
.save v(fout) v(xtop.{a}) i(vddi)
.control
foreach vc {" ".join(vctrls)}
  alterparam VCTRL=$vc
  reset
  tran 0.1n {TSTOP} 0 0.2n
  meas tran tr1 when v(fout)={VINV/2} rise=1 td={TMEAS}
  meas tran tr11 when v(fout)={VINV/2} rise=11 td={TMEAS}
  meas tran iavg avg i(vddi) from={TMEAS} to={TSTOP}
  meas tran amax max v(xtop.{a}) from={TMEAS} to={TSTOP}
  meas tran amin min v(xtop.{a}) from={TMEAS} to={TSTOP}
  let per = (tr11 - tr1)/10
  let fmhz = 1e-6/per
  let ima = -iavg*1e3
  let aswing = amax - amin
  echo RESULT ch={ch} vctrl=$vc per=$&per fmhz=$&fmhz ima=$&ima aswing=$&aswing
end
.endc
.end
"""
open(os.path.join(HERE, f"tb_ch{ch:03d}.spice"), "w").write(tb)
