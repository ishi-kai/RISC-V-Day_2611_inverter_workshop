#!/usr/bin/env python3
"""Generate tb_inv_matrix.sch : xschem + ngspice testbench for inv_matrix_top.

Stimulus
  D[6:0]  : counts 0,1,2,...,127, one step per 1 ms (D = k during k ms .. k+1 ms)
  IN      : 0 for the first half of every 1 ms slot, VINV for the second half
Checks, for every slot k (= channel k)
  t = k+0.25 ms (IN=0)    : DUT_IN[k] low,  OUT high
  t = k+0.50 ms           : SEL[127:0] one-hot (sum of all SEL == VDEC)
  t = k+0.75 ms (IN=VINV) : DUT_IN[k] high, OUT low
Prints FAIL lines per channel and a final PASS/FAIL summary.

Run:  python3 gen_tb.py                 -> tb_inv_matrix.sch (extracted std-cell decoder, 1 ms slots)
      python3 gen_tb.py --ideal-dec     -> tb_inv_matrix_idealdec.sch (behavioural decoder,
                                           20 us slots; ~5 min instead of hours)
      --slot=<seconds> overrides the slot length (e.g. --slot=50e-6)
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
N_CH = 128
IDEAL_DEC = "--ideal-dec" in sys.argv[1:]
SLOT = 20e-6 if IDEAL_DEC else 1e-3   # time per dec_in value
for a in sys.argv[1:]:
    if a.startswith("--slot="):
        SLOT = float(a.split("=", 1)[1])
TR = "10n"           # rise/fall time of all stimulus edges
TB = "tb_inv_matrix_idealdec" if IDEAL_DEC else "tb_inv_matrix"

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
    """Escape braces inside an xschem attribute value."""
    return s.replace("{", "\\{").replace("}", "\\}")


def vsrc(name, x, y, value, net):
    """Voltage source: p -> net (label), m -> ground."""
    inst("devices/vsource.sym", x, y, f'name={name} value="{esc(value)}" savecurrent=false')
    wire(x, y - 30, x, y - 60, net)
    label(x, y - 60, net)
    inst("devices/gnd.sym", x, y + 30, "name=l_gnd_" + name.lower() + " lab=0")


def sym_pins(fname):
    pins = {}
    for line in open(os.path.join(HERE, fname)):
        m = re.match(r"B 5 (\S+) (\S+) (\S+) (\S+) \{.*?name=(\S+)", line)
        if m:
            x = (float(m.group(1)) + float(m.group(3))) / 2
            y = (float(m.group(2)) + float(m.group(4))) / 2
            pins[m.group(5)] = (round(x), round(y))
    return pins


def ms(t):
    return f"{t * 1e3:.6g}m"


# ---------------------------------------------------------------------------
# DUT: inv_matrix_top
# ---------------------------------------------------------------------------
text(f"Testbench: inv_matrix_top{'  (IDEAL behavioural decoder)' if IDEAL_DEC else ''}\n"
     f"D[6:0] = 0,1,...,127 ({ms(SLOT)}s each).  IN = 0 (1st half) / VINV (2nd half) of every slot.\n"
     "Checks every channel: DUT_IN[k] follows IN, OUT = not IN, SEL one-hot.\n"
     f"Result is printed in the ngspice log (PASS / FAIL).  Sim time {ms(N_CH * SLOT)}s.",
     -600, -900, 0.5)
X0, Y0 = 0, 0
inst("inv_matrix_top.sym", X0, Y0, "name=x1")
conn = {"IN": "IN", "D[6:0]": "D[6:0]", "OUT": "OUT",
        "VDD_INV": "VDD_INV", "VDD_DEC": "VDD_DEC", "VSS": "0"}
for p, (px, py) in sym_pins("inv_matrix_top.sym").items():
    ax, ay = X0 + px, Y0 + py
    if abs(px) >= abs(py):
        dx, dy = (-40, 0) if px < 0 else (40, 0)
    else:
        dx, dy = (0, -40) if py < 0 else (0, 40)
    wire(ax, ay, ax + dx, ay + dy, conn[p])
    label(ax + dx, ay + dy, conn[p], right=dx > 0 or (dx == 0 and px > 0))

# load on OUT
inst("devices/capa.sym", 300, 100, "name=CL m=1 value=10f footprint=1206 device=\"ceramic capacitor\"")
wire(300, 70, 300, 40, "OUT")
label(300, 40, "OUT")
inst("devices/gnd.sym", 300, 130, "name=l_gnd_cl lab=0")

# ---------------------------------------------------------------------------
# Sources
# ---------------------------------------------------------------------------
vsrc("VDDD", -800, 400, "{VDEC}", "VDD_DEC")
vsrc("VDDI", -550, 400, "{VINV}", "VDD_INV")
half = SLOT / 2
vsrc("VIN", -300, 400, f"PULSE(0 {{VINV}} {ms(half)} {TR} {TR} {ms(half)} {ms(SLOT)})", "IN")
for b in range(7):
    w = SLOT * 2 ** b
    vsrc(f"VD{b}", 150 + 330 * b, 400,
         f"PULSE(0 {{VDEC}} {ms(w)} {TR} {TR} {ms(w)} {ms(2 * w)})", f"D[{b}]")

# ---------------------------------------------------------------------------
# Netlist code blocks
# ---------------------------------------------------------------------------
if IDEAL_DEC:
    # behavioural stand-in with the same subckt name / ports as decoder_7to128_xs.spice
    dec = [".subckt decoder_7to128_xs VDD VSS "
           + " ".join(f"I{b}" for b in range(6, -1, -1)) + "\n+ "
           + " ".join(f"O{k}" for k in range(127, -1, -1)),
           "* code = binary value of I[6:0] (threshold VDD/2); O[k] = VDD when code == k",
           "Bcode code VSS V=" + "+".join(f"{2 ** b}*u(v(I{b},VSS)-v(VDD,VSS)/2)"
                                          for b in range(7))]
    for k in range(N_CH):
        # 1k / 20f smooths the step (~20 ns edges, like a std-cell output)
        dec += [f"B{k} o{k}i VSS V=v(VDD,VSS)*u(0.5-abs(v(code,VSS)-{k}))",
                f"R{k} o{k}i O{k} 1k", f"C{k} O{k} VSS 20f"]
    dec.append(".ends")
    os.makedirs(os.path.join(HERE, "spice"), exist_ok=True)
    with open(os.path.join(HERE, "spice", "decoder_7to128_ideal.spice"), "w") as f:
        f.write("* Ideal (behavioural) decoder_7to128_xs, written by gen_tb.py --ideal-dec\n"
                + "\n".join(dec) + "\n")
    dec_inc = ".include [xschem get current_dirname]/spice/decoder_7to128_ideal.spice\n"
else:
    dec_inc = (".include $::PDK_ROOT/gf180mcuD/libs.ref/gf180mcu_fd_sc_mcu7t5v0/spice/"
               "gf180mcu_fd_sc_mcu7t5v0.spice\n"
               ".include [xschem get current_dirname]/spice/decoder_7to128_xs.spice\n")
models = ("\n.include $::180MCU_MODELS/design.ngspice\n"
          ".lib $::180MCU_MODELS/sm141064.ngspice typical\n"
          ".lib $::180MCU_MODELS/sm141064.ngspice diode_typical\n" + dec_inc)
inst("devices/code_shown.sym", -500, 700,
     f'name=MODELS only_toplevel=true\nformat="tcleval( @value )"\nvalue="{esc(models)}"')

tstop = ms(N_CH * SLOT)
selsum = "\n+ + ".join("+".join(f"v(x1.sel[{i}])" for i in range(j, j + 8))
                       for j in range(0, N_CH, 8))
saves = "\n".join(".save " + " ".join(f"v(x1.xarr.dut_in[{i}])" for i in range(j, j + 8))
                  for j in range(0, N_CH, 8))
probes = f"""
* sum of all SEL lines: must equal VDEC when SEL is one-hot
Bselsum selsum 0 V={selsum}
.save v(in) v(out) v(selsum) v(vdd_inv) v(vdd_dec)
.save v(d[0]) v(d[1]) v(d[2]) v(d[3]) v(d[4]) v(d[5]) v(d[6])
{saves}
"""
inst("devices/code.sym", -700, 600,
     f'name=PROBES only_toplevel=true\nvalue="{esc(probes)}"')
sim = f"""
* Supplies: VDEC = decoder + MUX control (5V).  VINV = all DUT inverters
* (<= 3.3V if any DUT uses 3.3V devices).
.param VDEC=5.0 VINV=3.3
* Bselsum (= sum of SEL[127:0]) and .save lines are in the PROBES block
.options method=gear reltol=1e-3
.control
tran {SLOT / 1000:.6g} {tstop} 0 {SLOT / 50:.6g}
write {TB}.raw
let vinv = v(vdd_inv)[0]
let vdec = v(vdd_dec)[0]
let lo_inv = 0.1*vinv
let hi_inv = 0.9*vinv
let nfail = 0
let k = 0
while k < {N_CH}
  let ta = k*{SLOT} + {SLOT * 0.25:.6g}
  let tb = k*{SLOT} + {SLOT * 0.50:.6g}
  let tc = k*{SLOT} + {SLOT * 0.75:.6g}
  meas tran din_a find v(x1.xarr.dut_in[$&k]) at=$&ta
  meas tran out_a find v(out) at=$&ta
  meas tran ssum  find v(selsum) at=$&tb
  meas tran din_c find v(x1.xarr.dut_in[$&k]) at=$&tc
  meas tran out_c find v(out) at=$&tc
  let bad = 0
  if din_a > lo_inv
    let bad = 1
  end
  if out_a < hi_inv
    let bad = 1
  end
  if din_c < hi_inv
    let bad = 1
  end
  if out_c > lo_inv
    let bad = 1
  end
  if abs(ssum - vdec) > 0.1*vdec
    let bad = 1
  end
  if bad > 0
    echo FAIL ch=$&k : [IN=0] DUT_IN=$&din_a OUT=$&out_a  [IN=VINV] DUT_IN=$&din_c OUT=$&out_c  sum_SEL=$&ssum
    let nfail = nfail + 1
  end
  let k = k + 1
end
echo
echo ==================================================
if nfail = 0
  echo RESULT: PASS  (all {N_CH} channels OK)
else
  echo RESULT: FAIL  ($&nfail of {N_CH} channels failed)
end
echo ==================================================
.endc
"""
inst("devices/code_shown.sym", 400, 700,
     f'name=NGSPICE only_toplevel=true\nvalue="{esc(sim)}"')

inst("devices/launcher.sym", -600, -650,
     'name=h1\n'
     f'descr="Ctrl+click: load waveforms ({TB}.raw)"\n'
     f'tclcommand="xschem raw_read $netlist_dir/{TB}.raw tran"')

with open(os.path.join(HERE, f"{TB}.sch"), "w") as f:
    f.write("v {xschem version=3.4.5 file_version=1.2}\nG {}\nK {}\nV {}\nS {}\nE {}\n")
    f.write("\n".join(lines) + "\n")
print(f"{TB}.sch written")
