#!/usr/bin/env python3
"""Generate tb_vco_top.sch : xschem + ngspice testbench for vco_top.

  0 .. T_EN      VCO_EN=0 : inverter mode. IN toggles, OUT must be NOT IN.
  T_EN .. TSTOP  VCO_EN=1 : ring oscillates; FOUT period/frequency measured.
  The run is repeated for every VCTRL in VCTRL_LIST (alterparam + reset).
Decoder = ideal behavioural model from ../inverter_matrix/spice (fast).

Run:  python3 gen_tb_vco.py [--ch=<0..127>]     (default channel 0)
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CH = 0
for a in sys.argv[1:]:
    if a.startswith("--ch="):
        CH = int(a.split("=", 1)[1])
VCTRL_LIST = [1.0, 1.5, 2.0, 2.5, 3.3]
T_EN = 2e-6
TSTOP = 8e-6
TB = "tb_vco_top"

lines = []
nlab = 0


def inst(sym, x, y, attrs, rot=0, flip=0):
    lines.append(f"C {{{sym}}} {x} {y} {rot} {flip} {{{attrs}}}")


def label(x, y, net, right=False):
    global nlab
    nlab += 1
    inst("devices/lab_pin.sym", x, y, f"name=l{nlab} sig_type=std_logic lab={net}",
         flip=1 if right else 0)


def wire(x1, y1, x2, y2, lab=""):
    lines.append(f"N {x1} {y1} {x2} {y2} {{lab={lab}}}")


def text(s, x, y, size=0.4):
    lines.append(f"T {{{s}}} {x} {y} 0 0 {size} {size} {{}}")


def esc(s):
    return s.replace("{", "\\{").replace("}", "\\}")


def vsrc(name, x, y, value, net):
    inst("devices/vsource.sym", x, y, f'name={name} value="{esc(value)}" savecurrent=false')
    wire(x, y - 30, x, y - 60, net)
    label(x, y - 60, net)
    inst("devices/gnd.sym", x, y + 30, "name=l_gnd_" + name.lower() + " lab=0")


def sym_pins(fname):
    pins = {}
    for line in open(os.path.join(HERE, fname)):
        m = re.match(r"B 5 (\S+) (\S+) (\S+) (\S+) \{.*?name=(\S+)", line)
        if m:
            pins[m.group(5)] = (round((float(m.group(1)) + float(m.group(3))) / 2),
                                round((float(m.group(2)) + float(m.group(4))) / 2))
    return pins


def us(t):
    return f"{t * 1e6:.6g}u"


text(f"Testbench: vco_top  (DUT channel {CH}, ideal decoder)\n"
     f"0..{us(T_EN)}s  VCO_EN=0 : inverter mode, OUT = NOT IN checked\n"
     f"{us(T_EN)}s..   VCO_EN=1 : 7-stage ring, FOUT frequency measured\n"
     f"VCTRL swept: {', '.join(str(v) for v in VCTRL_LIST)} V.  Results in the ngspice log.",
     -600, -800, 0.5)
inst("vco_top.sym", 0, 0, "name=x1")
conn = {"VCTRL": "VCTRL", "VCO_EN": "VCO_EN", "D[6:0]": "D[6:0]", "IN": "IN", "OUT": "OUT",
        "FOUT": "FOUT", "VDD_INV": "VDD_INV", "VDD_DEC": "VDD_DEC", "VSS": "0"}
for p, (px, py) in sym_pins("vco_top.sym").items():
    if abs(px) >= abs(py):
        dx, dy = (-40, 0) if px < 0 else (40, 0)
    else:
        dx, dy = (0, -40) if py < 0 else (0, 40)
    wire(px, py, px + dx, py + dy, conn[p])
    label(px + dx, py + dy, conn[p], right=dx > 0 or (dx == 0 and px > 0))

for i, net in enumerate(["OUT", "FOUT"]):
    x = 350 + 150 * i
    inst("devices/capa.sym", x, 150, f"name=C{net} m=1 value=100f footprint=1206 device=\"ceramic capacitor\"")
    wire(x, 120, x, 90, net)
    label(x, 90, net)
    inst("devices/gnd.sym", x, 180, f"name=l_gnd_c{net.lower()} lab=0")

vsrc("VDDD", -800, 400, "{VDEC}", "VDD_DEC")
vsrc("VDDI", -600, 400, "{VINV}", "VDD_INV")
vsrc("VCT", -400, 400, "{VCTRL}", "VCTRL")
vsrc("VEN", -200, 400, f"PULSE(0 {{VDEC}} {us(T_EN)} 10n 10n 1 2)", "VCO_EN")
vsrc("VIN", 0, 400, "PULSE(0 {VINV} 0.5u 10n 10n 0.5u 1u)", "IN")
for b in range(7):
    vsrc(f"VD{b}", 200 + 200 * b, 400, f"{{VDEC*{(CH >> b) & 1}}}", f"D[{b}]")

# behavioural decoder (same subckt name / ports as ../inverter_matrix decoder_7to128_xs);
# D[6:0] is static here, so the extracted std-cell decoder is not needed
dec = [".subckt decoder_7to128_xs VDD VSS " + " ".join(f"I{b}" for b in range(6, -1, -1))
       + "\n+ " + " ".join(f"O{k}" for k in range(127, -1, -1)),
       "Bcode code VSS V=" + "+".join(f"{2 ** b}*u(v(I{b},VSS)-v(VDD,VSS)/2)" for b in range(7))]
for k in range(128):
    dec += [f"B{k} o{k}i VSS V=v(VDD,VSS)*u(0.5-abs(v(code,VSS)-{k}))",
            f"R{k} o{k}i O{k} 1k", f"C{k} O{k} VSS 20f"]
dec.append(".ends")
os.makedirs(os.path.join(HERE, "spice"), exist_ok=True)
with open(os.path.join(HERE, "spice", "decoder_7to128_ideal.spice"), "w") as f:
    f.write("* Ideal (behavioural) decoder_7to128_xs, written by gen_tb_vco.py\n"
            + "\n".join(dec) + "\n")
models = ("\n.include $::180MCU_MODELS/design.ngspice\n"
          ".lib $::180MCU_MODELS/sm141064.ngspice typical\n"
          ".lib $::180MCU_MODELS/sm141064.ngspice diode_typical\n"
          ".include [xschem get current_dirname]/spice/decoder_7to128_ideal.spice\n")
inst("devices/code_shown.sym", -500, 700,
     f'name=MODELS only_toplevel=true\nformat="tcleval( @value )"\nvalue="{esc(models)}"')

t_lo, t_hi = T_EN - 0.6e-6, T_EN - 0.1e-6       # IN=0 / IN=VINV just before VCO_EN
t_meas = T_EN + 2e-6                            # skip start-up
vlist = " ".join(str(v) for v in VCTRL_LIST)
sim = f"""
.param VDEC=5.0 VINV=3.3 VCTRL=2.0
.options method=gear reltol=1e-3
.save v(in) v(out) v(fout) v(vco_en) v(vctrl) v(x1.r0) v(x1.r3) v(x1.r6) v(x1.min) v(x1.mout)
.save v(x1.vbp) v(x1.vbn) v(vdd_inv) i(vddi)
.control
let nfail = 0
foreach vc {vlist}
  alterparam VCTRL=$vc
  reset
  tran 0.1n {us(TSTOP)} 0 0.2n
  meas tran out_lo find v(out) at={us(t_lo)}
  meas tran out_hi find v(out) at={us(t_hi)}
  meas tran tr1 when v(fout)=1.65 rise=1 td={us(t_meas)}
  meas tran tr11 when v(fout)=1.65 rise=11 td={us(t_meas)}
  meas tran iavg avg i(vddi) from={us(t_meas)} to={us(TSTOP)}
  let vinv = v(vdd_inv)[0]
  if out_lo < 0.9*vinv
    echo FAIL inverter mode: VCTRL=$vc IN=0 OUT=$&out_lo
    let nfail = nfail + 1
  end
  if out_hi > 0.1*vinv
    echo FAIL inverter mode: VCTRL=$vc IN=VINV OUT=$&out_hi
    let nfail = nfail + 1
  end
  let per = (tr11 - tr1)/10
  let fmhz = 1e-6/per
  let ima = -iavg*1e3
  echo VCO: VCTRL=$vc V  period=$&per s  f=$&fmhz MHz  I(VDD_INV)=$&ima mA
  set fn = {TB}_vctrl{{$vc}}.raw
  write $fn
end
echo
echo ==================================================
if nfail = 0
  echo RESULT: inverter mode PASS
else
  echo RESULT: inverter mode FAIL ($&nfail)
end
echo ==================================================
.endc
"""
inst("devices/code_shown.sym", 400, 700,
     f'name=NGSPICE only_toplevel=true\nvalue="{esc(sim)}"')
inst("devices/launcher.sym", -600, -600,
     'name=h1\ndescr="Ctrl+click: load waveforms (VCTRL=2.0)"\n'
     f'tclcommand="xschem raw_read $netlist_dir/{TB}_vctrl2.0.raw tran"')

with open(os.path.join(HERE, f"{TB}.sch"), "w") as f:
    f.write("v {xschem version=3.4.5 file_version=1.2}\nG {}\nK {}\nV {}\nS {}\nE {}\n")
    f.write("\n".join(lines) + "\n")
print(f"{TB}.sch written (channel {CH})")
