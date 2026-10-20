#!/usr/bin/env python3
"""Write the LVS reference netlist (workshop_inverter.cdl) for gen_top_layout.py's GDS.

Top level = vco_top: vco_only + decoder_7to128 + 128 x (tgate_5v0_in + tgate_5v0_out + inv_dut_NNN)
+ antenna diodes on D[6:0].  Subcircuits come from the existing netlists:
  vco/vco_only.spice (VDD_INV added to the port list), inverter_matrix/tgate_5v0_{in,out}.spice,
  LibreLane final/spice/decoder_7to128.spice,
  PDK gf180mcu_fd_sc_mcu7t5v0.cdl (standard cells used by the decoder).
inv_dut_NNN (pins A Q VDD VSS) follow the GDS: a cell that is still the device-less
inverter_base placeholder gets an empty subcircuit, a replaced one (it has COMP shapes) an
inverter built from its row of dut_params.csv.  replace_dut.py calls this after a swap.

Usage:  python3 gen_lvs_netlist.py [--gds workshop_inverter.gds] [--csv dut_params.csv] [out.cdl]
"""
import os
import re
import sys

import klayout.db as db

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PDK = os.environ.get("GF180_PDK", os.path.expanduser("~/pdk/gf180mcuD"))
STD_CDL = os.path.join(PDK, "libs.ref/gf180mcu_fd_sc_mcu7t5v0/cdl/gf180mcu_fd_sc_mcu7t5v0.cdl")
DEC_SPICE = os.path.join(ROOT, "librelane-tg-logic/config/runs/RUN_2026-10-11_15-58-21/final/spice/decoder_7to128.spice")
TOP = "workshop_inverter"
N = 128
ANT = "A='1.4u * 1.2u ' P='2*1.4u + 2*1.2u '"
DUT_CSV = os.path.join(ROOT, "inverter_matrix", "dut_params.csv")
COMP = (22, 0)

sys.path.insert(0, os.path.join(ROOT, "inverter_matrix"))
from apply_dut_csv import read_csv  # noqa: E402


def subckts(path, keep_empty=False):
    """Return {name: [lines]} for every .subckt in a SPICE file (continuations joined).

    Empty (black-box) subcircuits are skipped unless keep_empty."""
    lines = []
    for raw in open(path):
        raw = raw.rstrip("\n")
        if raw.startswith("+") and lines:
            lines[-1] += " " + raw[1:].strip()
        else:
            lines.append(raw)
    out, cur = {}, None
    for l in lines:
        low = l.strip().lower()
        if low.startswith(".subckt"):
            cur = [l]
        elif cur is not None:
            cur.append(l)
            if low.startswith(".ends"):
                body = [x for x in cur[1:-1] if x.strip() and not x.lstrip().startswith("*")]
                if body or keep_empty:
                    out.setdefault(cur[0].split()[1], cur)
                cur = None
    return out


def dut_subckts(gds, csv_path):
    """{inv_dut_NNN: lines}: empty for placeholders, from dut_params.csv for replaced cells."""
    ly = db.Layout()
    ly.read(gds)
    comp = ly.find_layer(*COMP)
    params = dict(read_csv(csv_path))
    out, missing = {}, []
    for n in range(N):
        name = f"inv_dut_{n:03d}"
        cell = ly.cell(name)
        if cell is None:
            sys.exit(f"{gds}: no cell {name}")
        lines = [f".subckt {name} A Q VDD VSS"]
        if comp is not None and not cell.begin_shapes_rec(comp).at_end():
            p = params.get(n)
            if p is None:
                missing.append(name)
                continue
            lines.insert(0, f"* {name}: {p['P_MODEL']} W={p['P_W']} L={p['P_L']}"
                            f" / {p['N_MODEL']} W={p['N_W']} L={p['N_L']}")
            lines += [f"MMP Q A VDD VDD {p['P_MODEL']} W={p['P_W']} L={p['P_L']}",
                      f"MMN Q A VSS VSS {p['N_MODEL']} W={p['N_W']} L={p['N_L']}"]
        out[name] = lines + [".ends"]
    if missing:
        sys.exit(f"{csv_path}: no row for the replaced DUT(s) " + ", ".join(missing))
    return out


def write_netlist(out, gds, csv_path=DUT_CSV):
    """Write the reference netlist for `gds`; return the number of DUTs with devices."""
    lib = {}
    vco = subckts(os.path.join(ROOT, "vco/vco_only.spice"))
    vco["vco_only"][0] += " VDD_INV"
    for src in (vco,
                subckts(os.path.join(ROOT, "inverter_matrix/tgate_5v0_in.spice")),
                subckts(os.path.join(ROOT, "inverter_matrix/tgate_5v0_out.spice")),
                subckts(DEC_SPICE)):
        for k, v in src.items():
            lib.setdefault(k, v)
    duts = dut_subckts(gds, csv_path)
    lib.update(duts)
    used = {l.split()[-1] for l in lib["decoder_7to128"][1:] if l.startswith("X")}
    std = subckts(STD_CDL, keep_empty=True)
    dec_bb = subckts(DEC_SPICE, keep_empty=True)
    for k in sorted(used):
        # device-less cells (endcap): keep magic's pin list, which may differ from the CDL
        empty = len(std[k]) <= 2
        lib[k] = dec_bb[k] if empty else std[k]

    dec_pins = lib["decoder_7to128"][0].split()[2:]
    def dec_net(p):
        m = re.fullmatch(r"dec_(in|out)\[(\d+)\]", p)
        if m:
            return f"D[{m.group(2)}]" if m.group(1) == "in" else f"SEL[{m.group(2)}]"
        return {"VDD": "VDD_DEC", "VSS": "VSS"}[p]

    d = " ".join(f"D[{k}]" for k in range(7))
    top = [f".subckt {TOP} VCTRL VCO_EN {d} IN OUT FOUT VDD_INV VDD_DEC VSS",
           "XVCO VCTRL VCO_EN IN OUT FOUT MIN VDD_DEC VSS MOUT VDD_INV vco_only",
           "XDEC " + " ".join(dec_net(p) for p in dec_pins) + " decoder_7to128"]
    top += [f"DANT{k} VSS D[{k}] diode_nw2ps_06v0 {ANT}" for k in range(7)]
    for n in range(N):
        top += [f"XTGI{n:03d} MIN SEL[{n}] VDD_DEC VSS DIN{n:03d} tgate_5v0_in",
                f"XTGO{n:03d} MOUT SEL[{n}] VDD_DEC VSS DOUT{n:03d} tgate_5v0_out",
                f"XDUT{n:03d} DIN{n:03d} DOUT{n:03d} VDD_INV VSS inv_dut_{n:03d}"]
    top.append(".ends")

    # The KLayout LVS schematic translation (gf180_xschem_klayout_spice_convert.py) drops a
    # leading X not followed by a digit (XTGI000 -> TGI000 = unknown element 'T'), so give
    # such instances the X0_ prefix, as gf180_lvs_make does.
    def fix(l):
        return re.sub(r"^(\s*)X(?=[^\d\s])", r"\1X0_", l)

    with open(out, "w") as f:
        f.write(f"* {TOP}: LVS reference netlist (generated by gen_lvs_netlist.py)\n\n")
        for k, v in lib.items():
            f.write("\n".join(map(fix, v)) + "\n\n")
        f.write("\n".join(map(fix, top)) + "\n")
    return sum(len(v) > 2 for v in duts.values())


def main():
    args = sys.argv[1:]
    opts = {"--gds": os.path.join(HERE, f"{TOP}.gds"), "--csv": DUT_CSV}
    for opt in opts:
        if opt in args:
            i = args.index(opt)
            opts[opt] = args[i + 1]
            del args[i:i + 2]
    out = args[0] if args else os.path.join(HERE, f"{TOP}.cdl")
    n = write_netlist(out, opts["--gds"], opts["--csv"])
    print(f"wrote {out} ({n} DUT(s) from {opts['--csv']}, {N - n} placeholder(s))")


if __name__ == "__main__":
    main()
