#!/bin/sh
# Run all tb_chNNN.spice (JOBS in parallel, default 4).  Usage: ./run_all.sh [JOBS]
cd "$(dirname "$0")"
ls tb_ch[0-9][0-9][0-9].spice | sed 's/\.spice$//' |
  OMP_NUM_THREADS=1 xargs -P "${1:-4}" -I{} sh -c 'ngspice -b {}.spice > {}.log 2>&1'
