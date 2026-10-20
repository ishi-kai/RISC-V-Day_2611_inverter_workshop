"""Shared xschem writing helpers for the inverter matrix generators.

Used by gen_schematics.py (whole design) and apply_dut_csv.py (DUT replacement).
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))

HEADER = "v {xschem version=3.4.5 file_version=1.2}\nG {}\n"

# ---------------------------------------------------------------------------
# Supported FET models and their minimum (W, L)  (GF180MCU DRC / PDK symbol defaults)
# ---------------------------------------------------------------------------
MODEL_MIN = {"nfet_03v3": ("0.22u", "0.28u"), "pfet_03v3": ("0.22u", "0.28u"),
             "nfet_05v0": ("0.42u", "0.60u"), "pfet_05v0": ("0.36u", "0.50u"),
             "nfet_06v0": ("0.30u", "0.70u"), "pfet_06v0": ("0.30u", "0.55u")}

# Antenna diode (Nwell/Psub, 6V) for long nets that only reach gates (SEL[i], D[6:0], VCO_EN, VCTRL).
# GF180 ANT.16_ii (thick gate): metal perimeter*0.54 / (gate + 15*diode) <= 400 per metal layer.
# e.g. SEL (XSELB + 2 x TG_N ~3.6um2): ~2.7mm perimeter without, ~21mm with a 1.4u x 1.2u diode.
ANT_D = ("diode_nw2ps_06v0", "1.4u", "1.2u")

# FET pin offsets relative to instance origin (from PDK symbols)
NFET_PINS = {"D": (20, -30), "G": (-20, 0), "S": (20, 30), "B": (20, 0)}
PFET_PINS = {"S": (20, -30), "G": (-20, 0), "D": (20, 30), "B": (20, 0)}


class Sch:
    """Minimal xschem schematic writer using label-based connections."""

    def __init__(self):
        self.lines = []
        self.nlab = 0

    def inst(self, sym, x, y, attrs, rot=0, flip=0):
        self.lines.append(f"C {{{sym}}} {x} {y} {rot} {flip} {{{attrs}}}")

    def wire(self, x1, y1, x2, y2, lab=""):
        self.lines.append(f"N {x1} {y1} {x2} {y2} {{lab={lab}}}")

    def text(self, s, x, y, size=0.4):
        self.lines.append(f"T {{{s}}} {x} {y} 0 0 {size} {size} {{}}")

    def label(self, x, y, net, right=False):
        self.nlab += 1
        self.inst("devices/lab_pin.sym", x, y,
                  f"name=l{self.nlab} sig_type=std_logic lab={net}",
                  rot=0, flip=1 if right else 0)

    def stub(self, px, py, dx, dy, net):
        """Short wire from a pin, terminated by a net label."""
        self.wire(px, py, px + dx, py + dy, net)
        self.label(px + dx, py + dy, net, right=dx > 0)

    def pin(self, kind, x, y, net, n):
        sym = {"in": "devices/ipin.sym", "out": "devices/opin.sym",
               "inout": "devices/iopin.sym"}[kind]
        self.inst(sym, x, y, f"name=p{n} lab={net}")
        # attach a label on the same net right next to the pin
        dx = 40 if kind == "in" else -40
        self.wire(x, y, x + dx, y, net)

    def fet(self, model, name, x, y, d, g, s, b, w=None, l=None):
        """PDK FET (model from MODEL_MIN). W/L default to the model minimum."""
        kind = model[0]
        sym = f"symbols/{model}.sym"
        w = w or MODEL_MIN[model][0]
        l = l or MODEL_MIN[model][1]
        attrs = (f"name={name}\nL={l}\nW={w}\nnf=1\nm=1\n"
                 "ad=\"'int((nf+1)/2) * W/nf * 0.18u'\"\n"
                 "pd=\"'2*int((nf+1)/2) * (W/nf + 0.18u)'\"\n"
                 "as=\"'int((nf+2)/2) * W/nf * 0.18u'\"\n"
                 "ps=\"'2*int((nf+2)/2) * (W/nf + 0.18u)'\"\n"
                 "nrd=\"'0.18u / W'\" nrs=\"'0.18u / W'\"\n"
                 f"sa=0 sb=0 sd=0\nmodel={model}\nspiceprefix=X\n")
        self.inst(sym, x, y, attrs)
        pins = NFET_PINS if kind == "n" else PFET_PINS
        nets = {"D": d, "G": g, "S": s, "B": b}
        for p, (ox, oy) in pins.items():
            px, py = x + ox, y + oy
            if p == "G":
                self.stub(px, py, -40, 0, nets[p])
            elif p == "B":
                self.stub(px, py, 40, 0, nets[p])
            else:
                self.stub(px, py, 0, -30 if oy < 0 else 30, nets[p])

    def diode(self, model, name, x, y, p, m, w="1u", l="1u"):
        """PDK junction diode, anode p (top pin), cathode m (bottom pin)."""
        self.inst(f"symbols/{model}.sym", x, y, f"name={name}\nmodel={model}\nr_w={w}\nr_l={l}\nm=1")
        self.stub(x, y - 30, 0, -30, p)
        self.stub(x, y + 30, 0, 30, m)

    def sub(self, symdef, name, x, y, conn):
        """Place one of our own subcircuit symbols, wiring each pin to a label."""
        self.inst(symdef.fname, x, y, f"name={name}")
        for pname, (ox, oy, side) in symdef.pins.items():
            px, py = x + ox, y + oy
            d = {"L": (-30, 0), "R": (30, 0), "T": (0, -30), "B": (0, 30)}[side]
            self.wire(px, py, px + d[0], py + d[1], conn[pname])
            self.label(px + d[0], py + d[1], conn[pname], right=d[0] > 0 or (d[0] == 0 and ox > 0))

    def save(self, fname):
        os.makedirs(os.path.dirname(os.path.join(HERE, fname)), exist_ok=True)
        with open(os.path.join(HERE, fname), "w") as f:
            f.write(HEADER + "K {}\nV {}\nS {}\nE {}\n")
            f.write("\n".join(self.lines) + "\n")


class Sym:
    """Box-style subcircuit symbol. pins: list of (name, dir, side)."""

    def __init__(self, fname, pins, w=160, pitch=20, fmt="@name @pinlist @symname",
                 extra_k="", body=None, title=None, write=True):
        self.fname = fname
        self.pins = {}
        left = [p for p in pins if p[2] == "L"]
        right = [p for p in pins if p[2] == "R"]
        top = [p for p in pins if p[2] == "T"]
        bot = [p for p in pins if p[2] == "B"]
        nside = max(len(left), len(right), 1)
        h = max(nside * pitch * 2, 60)
        hw, hh = w // 2, h // 2
        out = [HEADER.rstrip("\n"),
               f'K {{type=subcircuit\nformat="{fmt}"\ntemplate="name=x1"\n{extra_k}}}',
               "V {}", "S {}", "E {}"]
        if body is None:
            out.append(f"P 4 5 {-hw} {-hh} {hw} {-hh} {hw} {hh} {-hw} {hh} {-hw} {-hh} {{}}")
        else:
            out += body
        pin_lines = []

        def place(lst, side):
            n = len(lst)
            for i, (name, d, _) in enumerate(lst):
                if side in "LR":
                    y = int(-(n - 1) * pitch + i * 2 * pitch)
                    x0 = -hw if side == "L" else hw
                    x = x0 - 20 if side == "L" else x0 + 20
                    out.append(f"L 4 {x0} {y} {x} {y} {{}}")
                    tx = x0 + 5 if side == "L" else x0 - 5
                    out.append(f"T {{{name}}} {tx} {y - 6} 0 {0 if side == 'L' else 1} 0.2 0.2 {{}}")
                else:
                    x = int(-(n - 1) * pitch + i * 2 * pitch)
                    y0 = -hh if side == "T" else hh
                    y = y0 - 20 if side == "T" else y0 + 20
                    out.append(f"L 4 {x} {y0} {x} {y} {{}}")
                    ty = y0 + 4 if side == "T" else y0 - 16
                    out.append(f"T {{{name}}} {x + 3} {ty} 0 0 0.2 0.2 {{}}")
                pin_lines.append(
                    f"B 5 {x - 2.5} {y - 2.5} {x + 2.5} {y + 2.5} {{name={name} dir={d}}}")
                self.pins[name] = (x, y, side)

        place(left, "L")
        place(right, "R")
        place(top, "T")
        place(bot, "B")
        # Pin order in @pinlist == order of B 5 lines: keep the declared order
        order = [p[0] for p in pins]
        pin_lines.sort(key=lambda l: order.index(re.search(r"name=(\S+)", l).group(1)))
        out += pin_lines
        out.append(f"T {{{title or '@symname'}}} {-hw} {-hh - 30} 0 0 0.25 0.25 {{}}")
        out.append(f"T {{@name}} {-hw} {hh + 5} 0 0 0.2 0.2 {{}}")
        if not write:
            return
        os.makedirs(os.path.dirname(os.path.join(HERE, fname)), exist_ok=True)
        with open(os.path.join(HERE, fname), "w") as f:
            f.write("\n".join(out) + "\n")



# ---------------------------------------------------------------------------
# Inverter (symbol pins A, Y, VDD, VSS)
# ---------------------------------------------------------------------------
inv_body = ["L 4 -40 -30 -40 30 {}", "L 4 -40 -30 20 0 {}", "L 4 -40 30 20 0 {}",
            "A 4 25 0 5 0 360 {}"]


def inv_sym(name, write=True):
    return Sym(f"{name}.sym",
               [("A", "in", "L"), ("Y", "out", "R"), ("VDD", "inout", "T"), ("VSS", "inout", "B")],
               w=80, body=inv_body, write=write)


def inv_sch(name, title, p_model, n_model, wp=None, lp=None, wn=None, ln=None):
    """Write <name>.sch : CMOS inverter. W/L default to the model minimum."""
    wp, lp = wp or MODEL_MIN[p_model][0], lp or MODEL_MIN[p_model][1]
    wn, ln = wn or MODEL_MIN[n_model][0], ln or MODEL_MIN[n_model][1]
    s = Sch()
    s.text(f"{title}\n{n_model} W={wn} L={ln} / {p_model} W={wp} L={lp}", -200, -300)
    s.fet(p_model, "MP", 0, -80, d="Y", g="A", s="VDD", b="VDD", w=wp, l=lp)
    s.fet(n_model, "MN", 0, 80, d="Y", g="A", s="VSS", b="VSS", w=wn, l=ln)
    s.pin("in", -300, -150, "A", 1)
    s.pin("out", 300, -150, "Y", 2)
    s.pin("inout", 300, -100, "VDD", 3)
    s.pin("inout", 300, -50, "VSS", 4)
    s.save(f"{name}.sch")
