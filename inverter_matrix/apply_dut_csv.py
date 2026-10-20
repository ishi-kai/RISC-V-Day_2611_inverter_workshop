#!/usr/bin/env python3
"""Replace DUT inverters (dut/inv_dut_NNN.sch) from a CSV file.

CSV format (header required, spaces after commas allowed, '#' lines ignored):

    DUT_NUM, P_MODEL, P_W, P_L, N_MODEL, N_W, N_L
    000, pfet_05v0, 0.36u, 0.50u, nfet_05v0, 0.42u, 0.60u
    001, pfet_03v3, 0.22u, 0.28u, nfet_03v3, 0.22u, 0.28u

  DUT_NUM : 0 .. 127 (leading zeros optional)
  *_MODEL : pfet_03v3 / pfet_05v0 / pfet_06v0, nfet_03v3 / nfet_05v0 / nfet_06v0
  *_W/_L  : SPICE value (0.30u, 300n, 0.3e-6 ...), must be >= the model minimum

All rows are checked first; nothing is written if any row has an error.
The previous schematic of each replaced DUT is kept as dut/inv_dut_NNN.sch.bak.

Usage:  python3 apply_dut_csv.py duts.csv [--dry-run]
"""
import csv
import os
import re
import shutil
import sys

from xsch_lib import HERE, MODEL_MIN, inv_sch, inv_sym

N_CH = 128
COLS = ["DUT_NUM", "P_MODEL", "P_W", "P_L", "N_MODEL", "N_W", "N_L"]
SCALE = {"f": 1e-15, "p": 1e-12, "n": 1e-9, "u": 1e-6, "m": 1e-3, "": 1.0}


def parse_len(s):
    """SPICE length -> metres (accepts 0.3u, 0.3um, 300n, 0.3e-6)."""
    m = re.fullmatch(r"([0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?)\s*([fpnum]?)m?", s.strip())
    if not m:
        raise ValueError(f"bad length value '{s}'")
    return float(m.group(1)) * SCALE[m.group(2)]


def check_row(row, lineno):
    """Return (dut_num, params) or raise ValueError with a readable message."""
    try:
        return _check_row(row, lineno)
    except ValueError as e:
        msg = str(e)
        raise ValueError(msg if msg.startswith("line ") else f"line {lineno}: {msg}")


def _check_row(row, lineno):
    where = f"line {lineno}"
    try:
        num = int(row["DUT_NUM"])
    except ValueError:
        raise ValueError(f"{where}: DUT_NUM '{row['DUT_NUM']}' is not a number")
    if not 0 <= num < N_CH:
        raise ValueError(f"{where}: DUT_NUM {num} out of range 0..{N_CH - 1}")
    p = {k: row[k] for k in COLS[1:]}
    for kind, col in (("p", "P_MODEL"), ("n", "N_MODEL")):
        model = p[col]
        if model not in MODEL_MIN or model[0] != kind:
            ok = ", ".join(m for m in MODEL_MIN if m[0] == kind)
            raise ValueError(f"{where}: {col} '{model}' not supported (use {ok})")
        wmin, lmin = (parse_len(v) for v in MODEL_MIN[model])
        pre = col[0]
        for dim, vmin in (("W", wmin), ("L", lmin)):
            v = parse_len(p[f"{pre}_{dim}"])
            if v < vmin * (1 - 1e-9):
                raise ValueError(f"{where}: {pre}_{dim}={p[f'{pre}_{dim}']} is below the "
                                 f"{model} minimum {MODEL_MIN[model][0 if dim == 'W' else 1]}")
    return num, p


def read_csv(path):
    """Read and check a DUT CSV -> [(num, params)]; exit with all errors on failure."""
    with open(path, newline="") as f:
        lines = [l for l in f if l.strip() and not l.lstrip().startswith("#")]
    reader = csv.DictReader(lines, skipinitialspace=True)
    reader.fieldnames = [c.strip().upper() for c in reader.fieldnames or []]
    missing = [c for c in COLS if c not in reader.fieldnames]
    if missing:
        sys.exit(f"{path}: missing column(s) {', '.join(missing)} (header: {', '.join(COLS)})")

    rows, errors, seen = [], [], {}
    for lineno, row in enumerate(reader, start=2):
        row = {k: (v or "").strip() for k, v in row.items() if k}
        try:
            num, p = check_row(row, lineno)
        except ValueError as e:
            errors.append(str(e))
            continue
        if num in seen:
            errors.append(f"line {lineno}: DUT_NUM {num} already given on line {seen[num]}")
            continue
        seen[num] = lineno
        rows.append((num, p))
    if errors:
        print("ERROR: nothing was written.", file=sys.stderr)
        for e in errors:
            print("  " + e, file=sys.stderr)
        sys.exit(1)
    return rows


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry-run" in sys.argv[1:]
    if len(args) != 1:
        sys.exit(__doc__)
    path = args[0]

    rows = read_csv(path)

    low_v = []
    for num, p in rows:
        name = f"dut/inv_dut_{num:03d}"
        vp, vn = p["P_MODEL"][-4:], p["N_MODEL"][-4:]
        note = ""
        if vp != vn:
            note = f"  (WARNING: P is {vp}, N is {vn})"
        if "03v3" in (vp, vn):
            low_v.append(num)
        print(f"{'[dry-run] ' if dry else ''}{name}: {p['P_MODEL']} W={p['P_W']} L={p['P_L']}"
              f" / {p['N_MODEL']} W={p['N_W']} L={p['N_L']}{note}")
        if dry:
            continue
        sch = os.path.join(HERE, f"{name}.sch")
        if os.path.exists(sch):
            shutil.copy2(sch, sch + ".bak")
        if not os.path.exists(os.path.join(HERE, f"{name}.sym")):
            inv_sym(name)
        inv_sch(name, f"DUT #{num} (from {os.path.basename(path)})",
                p["P_MODEL"], p["N_MODEL"], wp=p["P_W"], lp=p["P_L"], wn=p["N_W"], ln=p["N_L"])

    print(f"{len(rows)} DUT(s) {'checked' if dry else 'replaced'}.")
    if low_v:
        print(f"NOTE: 3.3V devices in DUT {', '.join(map(str, low_v))} -> "
              "keep VDD_INV and IN <= 3.3V (VINV in tb_inv_matrix.sch).")


if __name__ == "__main__":
    main()
