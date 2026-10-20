v {xschem version=3.4.5 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {Testbench: inv_matrix_top
D[6:0] = 0,1,...,127 (1ms each).  IN = 0 (1st half) / VINV (2nd half) of every slot.
Checks every channel: DUT_IN[k] follows IN, OUT = not IN, SEL one-hot.
Result is printed in the ngspice log (PASS / FAIL).  Sim time 128ms.} -600 -900 0 0 0.5 0.5 {}
C {inv_matrix_top.sym} 0 0 0 0 {name=x1}
N -120 -30 -160 -30 {lab=IN}
C {devices/lab_pin.sym} -160 -30 0 0 {name=l1 sig_type=std_logic lab=IN}
N -120 30 -160 30 {lab=D[6:0]}
C {devices/lab_pin.sym} -160 30 0 0 {name=l2 sig_type=std_logic lab=D[6:0]}
N 120 0 160 0 {lab=OUT}
C {devices/lab_pin.sym} 160 0 0 1 {name=l3 sig_type=std_logic lab=OUT}
N -30 -80 -30 -120 {lab=VDD_INV}
C {devices/lab_pin.sym} -30 -120 0 0 {name=l4 sig_type=std_logic lab=VDD_INV}
N 30 -80 30 -120 {lab=VDD_DEC}
C {devices/lab_pin.sym} 30 -120 0 1 {name=l5 sig_type=std_logic lab=VDD_DEC}
N 0 80 0 120 {lab=0}
C {devices/lab_pin.sym} 0 120 0 0 {name=l6 sig_type=std_logic lab=0}
C {devices/capa.sym} 300 100 0 0 {name=CL m=1 value=10f footprint=1206 device="ceramic capacitor"}
N 300 70 300 40 {lab=OUT}
C {devices/lab_pin.sym} 300 40 0 0 {name=l7 sig_type=std_logic lab=OUT}
C {devices/gnd.sym} 300 130 0 0 {name=l_gnd_cl lab=0}
C {devices/vsource.sym} -800 400 0 0 {name=VDDD value="\{VDEC\}" savecurrent=false}
N -800 370 -800 340 {lab=VDD_DEC}
C {devices/lab_pin.sym} -800 340 0 0 {name=l8 sig_type=std_logic lab=VDD_DEC}
C {devices/gnd.sym} -800 430 0 0 {name=l_gnd_vddd lab=0}
C {devices/vsource.sym} -550 400 0 0 {name=VDDI value="\{VINV\}" savecurrent=false}
N -550 370 -550 340 {lab=VDD_INV}
C {devices/lab_pin.sym} -550 340 0 0 {name=l9 sig_type=std_logic lab=VDD_INV}
C {devices/gnd.sym} -550 430 0 0 {name=l_gnd_vddi lab=0}
C {devices/vsource.sym} -300 400 0 0 {name=VIN value="PULSE(0 \{VINV\} 0.5m 10n 10n 0.5m 1m)" savecurrent=false}
N -300 370 -300 340 {lab=IN}
C {devices/lab_pin.sym} -300 340 0 0 {name=l10 sig_type=std_logic lab=IN}
C {devices/gnd.sym} -300 430 0 0 {name=l_gnd_vin lab=0}
C {devices/vsource.sym} 150 400 0 0 {name=VD0 value="PULSE(0 \{VDEC\} 1m 10n 10n 1m 2m)" savecurrent=false}
N 150 370 150 340 {lab=D[0]}
C {devices/lab_pin.sym} 150 340 0 0 {name=l11 sig_type=std_logic lab=D[0]}
C {devices/gnd.sym} 150 430 0 0 {name=l_gnd_vd0 lab=0}
C {devices/vsource.sym} 480 400 0 0 {name=VD1 value="PULSE(0 \{VDEC\} 2m 10n 10n 2m 4m)" savecurrent=false}
N 480 370 480 340 {lab=D[1]}
C {devices/lab_pin.sym} 480 340 0 0 {name=l12 sig_type=std_logic lab=D[1]}
C {devices/gnd.sym} 480 430 0 0 {name=l_gnd_vd1 lab=0}
C {devices/vsource.sym} 810 400 0 0 {name=VD2 value="PULSE(0 \{VDEC\} 4m 10n 10n 4m 8m)" savecurrent=false}
N 810 370 810 340 {lab=D[2]}
C {devices/lab_pin.sym} 810 340 0 0 {name=l13 sig_type=std_logic lab=D[2]}
C {devices/gnd.sym} 810 430 0 0 {name=l_gnd_vd2 lab=0}
C {devices/vsource.sym} 1140 400 0 0 {name=VD3 value="PULSE(0 \{VDEC\} 8m 10n 10n 8m 16m)" savecurrent=false}
N 1140 370 1140 340 {lab=D[3]}
C {devices/lab_pin.sym} 1140 340 0 0 {name=l14 sig_type=std_logic lab=D[3]}
C {devices/gnd.sym} 1140 430 0 0 {name=l_gnd_vd3 lab=0}
C {devices/vsource.sym} 1470 400 0 0 {name=VD4 value="PULSE(0 \{VDEC\} 16m 10n 10n 16m 32m)" savecurrent=false}
N 1470 370 1470 340 {lab=D[4]}
C {devices/lab_pin.sym} 1470 340 0 0 {name=l15 sig_type=std_logic lab=D[4]}
C {devices/gnd.sym} 1470 430 0 0 {name=l_gnd_vd4 lab=0}
C {devices/vsource.sym} 1800 400 0 0 {name=VD5 value="PULSE(0 \{VDEC\} 32m 10n 10n 32m 64m)" savecurrent=false}
N 1800 370 1800 340 {lab=D[5]}
C {devices/lab_pin.sym} 1800 340 0 0 {name=l16 sig_type=std_logic lab=D[5]}
C {devices/gnd.sym} 1800 430 0 0 {name=l_gnd_vd5 lab=0}
C {devices/vsource.sym} 2130 400 0 0 {name=VD6 value="PULSE(0 \{VDEC\} 64m 10n 10n 64m 128m)" savecurrent=false}
N 2130 370 2130 340 {lab=D[6]}
C {devices/lab_pin.sym} 2130 340 0 0 {name=l17 sig_type=std_logic lab=D[6]}
C {devices/gnd.sym} 2130 430 0 0 {name=l_gnd_vd6 lab=0}
C {devices/code_shown.sym} -500 700 0 0 {name=MODELS only_toplevel=true
format="tcleval( @value )"
value="
.include $::180MCU_MODELS/design.ngspice
.lib $::180MCU_MODELS/sm141064.ngspice typical
.lib $::180MCU_MODELS/sm141064.ngspice diode_typical
.include $::PDK_ROOT/gf180mcuD/libs.ref/gf180mcu_fd_sc_mcu7t5v0/spice/gf180mcu_fd_sc_mcu7t5v0.spice
.include [xschem get current_dirname]/spice/decoder_7to128_xs.spice
"}
C {devices/code.sym} -700 600 0 0 {name=PROBES only_toplevel=true
value="
* sum of all SEL lines: must equal VDEC when SEL is one-hot
Bselsum selsum 0 V=v(x1.sel[0])+v(x1.sel[1])+v(x1.sel[2])+v(x1.sel[3])+v(x1.sel[4])+v(x1.sel[5])+v(x1.sel[6])+v(x1.sel[7])
+ + v(x1.sel[8])+v(x1.sel[9])+v(x1.sel[10])+v(x1.sel[11])+v(x1.sel[12])+v(x1.sel[13])+v(x1.sel[14])+v(x1.sel[15])
+ + v(x1.sel[16])+v(x1.sel[17])+v(x1.sel[18])+v(x1.sel[19])+v(x1.sel[20])+v(x1.sel[21])+v(x1.sel[22])+v(x1.sel[23])
+ + v(x1.sel[24])+v(x1.sel[25])+v(x1.sel[26])+v(x1.sel[27])+v(x1.sel[28])+v(x1.sel[29])+v(x1.sel[30])+v(x1.sel[31])
+ + v(x1.sel[32])+v(x1.sel[33])+v(x1.sel[34])+v(x1.sel[35])+v(x1.sel[36])+v(x1.sel[37])+v(x1.sel[38])+v(x1.sel[39])
+ + v(x1.sel[40])+v(x1.sel[41])+v(x1.sel[42])+v(x1.sel[43])+v(x1.sel[44])+v(x1.sel[45])+v(x1.sel[46])+v(x1.sel[47])
+ + v(x1.sel[48])+v(x1.sel[49])+v(x1.sel[50])+v(x1.sel[51])+v(x1.sel[52])+v(x1.sel[53])+v(x1.sel[54])+v(x1.sel[55])
+ + v(x1.sel[56])+v(x1.sel[57])+v(x1.sel[58])+v(x1.sel[59])+v(x1.sel[60])+v(x1.sel[61])+v(x1.sel[62])+v(x1.sel[63])
+ + v(x1.sel[64])+v(x1.sel[65])+v(x1.sel[66])+v(x1.sel[67])+v(x1.sel[68])+v(x1.sel[69])+v(x1.sel[70])+v(x1.sel[71])
+ + v(x1.sel[72])+v(x1.sel[73])+v(x1.sel[74])+v(x1.sel[75])+v(x1.sel[76])+v(x1.sel[77])+v(x1.sel[78])+v(x1.sel[79])
+ + v(x1.sel[80])+v(x1.sel[81])+v(x1.sel[82])+v(x1.sel[83])+v(x1.sel[84])+v(x1.sel[85])+v(x1.sel[86])+v(x1.sel[87])
+ + v(x1.sel[88])+v(x1.sel[89])+v(x1.sel[90])+v(x1.sel[91])+v(x1.sel[92])+v(x1.sel[93])+v(x1.sel[94])+v(x1.sel[95])
+ + v(x1.sel[96])+v(x1.sel[97])+v(x1.sel[98])+v(x1.sel[99])+v(x1.sel[100])+v(x1.sel[101])+v(x1.sel[102])+v(x1.sel[103])
+ + v(x1.sel[104])+v(x1.sel[105])+v(x1.sel[106])+v(x1.sel[107])+v(x1.sel[108])+v(x1.sel[109])+v(x1.sel[110])+v(x1.sel[111])
+ + v(x1.sel[112])+v(x1.sel[113])+v(x1.sel[114])+v(x1.sel[115])+v(x1.sel[116])+v(x1.sel[117])+v(x1.sel[118])+v(x1.sel[119])
+ + v(x1.sel[120])+v(x1.sel[121])+v(x1.sel[122])+v(x1.sel[123])+v(x1.sel[124])+v(x1.sel[125])+v(x1.sel[126])+v(x1.sel[127])
.save v(in) v(out) v(selsum) v(vdd_inv) v(vdd_dec)
.save v(d[0]) v(d[1]) v(d[2]) v(d[3]) v(d[4]) v(d[5]) v(d[6])
.save v(x1.xarr.dut_in[0]) v(x1.xarr.dut_in[1]) v(x1.xarr.dut_in[2]) v(x1.xarr.dut_in[3]) v(x1.xarr.dut_in[4]) v(x1.xarr.dut_in[5]) v(x1.xarr.dut_in[6]) v(x1.xarr.dut_in[7])
.save v(x1.xarr.dut_in[8]) v(x1.xarr.dut_in[9]) v(x1.xarr.dut_in[10]) v(x1.xarr.dut_in[11]) v(x1.xarr.dut_in[12]) v(x1.xarr.dut_in[13]) v(x1.xarr.dut_in[14]) v(x1.xarr.dut_in[15])
.save v(x1.xarr.dut_in[16]) v(x1.xarr.dut_in[17]) v(x1.xarr.dut_in[18]) v(x1.xarr.dut_in[19]) v(x1.xarr.dut_in[20]) v(x1.xarr.dut_in[21]) v(x1.xarr.dut_in[22]) v(x1.xarr.dut_in[23])
.save v(x1.xarr.dut_in[24]) v(x1.xarr.dut_in[25]) v(x1.xarr.dut_in[26]) v(x1.xarr.dut_in[27]) v(x1.xarr.dut_in[28]) v(x1.xarr.dut_in[29]) v(x1.xarr.dut_in[30]) v(x1.xarr.dut_in[31])
.save v(x1.xarr.dut_in[32]) v(x1.xarr.dut_in[33]) v(x1.xarr.dut_in[34]) v(x1.xarr.dut_in[35]) v(x1.xarr.dut_in[36]) v(x1.xarr.dut_in[37]) v(x1.xarr.dut_in[38]) v(x1.xarr.dut_in[39])
.save v(x1.xarr.dut_in[40]) v(x1.xarr.dut_in[41]) v(x1.xarr.dut_in[42]) v(x1.xarr.dut_in[43]) v(x1.xarr.dut_in[44]) v(x1.xarr.dut_in[45]) v(x1.xarr.dut_in[46]) v(x1.xarr.dut_in[47])
.save v(x1.xarr.dut_in[48]) v(x1.xarr.dut_in[49]) v(x1.xarr.dut_in[50]) v(x1.xarr.dut_in[51]) v(x1.xarr.dut_in[52]) v(x1.xarr.dut_in[53]) v(x1.xarr.dut_in[54]) v(x1.xarr.dut_in[55])
.save v(x1.xarr.dut_in[56]) v(x1.xarr.dut_in[57]) v(x1.xarr.dut_in[58]) v(x1.xarr.dut_in[59]) v(x1.xarr.dut_in[60]) v(x1.xarr.dut_in[61]) v(x1.xarr.dut_in[62]) v(x1.xarr.dut_in[63])
.save v(x1.xarr.dut_in[64]) v(x1.xarr.dut_in[65]) v(x1.xarr.dut_in[66]) v(x1.xarr.dut_in[67]) v(x1.xarr.dut_in[68]) v(x1.xarr.dut_in[69]) v(x1.xarr.dut_in[70]) v(x1.xarr.dut_in[71])
.save v(x1.xarr.dut_in[72]) v(x1.xarr.dut_in[73]) v(x1.xarr.dut_in[74]) v(x1.xarr.dut_in[75]) v(x1.xarr.dut_in[76]) v(x1.xarr.dut_in[77]) v(x1.xarr.dut_in[78]) v(x1.xarr.dut_in[79])
.save v(x1.xarr.dut_in[80]) v(x1.xarr.dut_in[81]) v(x1.xarr.dut_in[82]) v(x1.xarr.dut_in[83]) v(x1.xarr.dut_in[84]) v(x1.xarr.dut_in[85]) v(x1.xarr.dut_in[86]) v(x1.xarr.dut_in[87])
.save v(x1.xarr.dut_in[88]) v(x1.xarr.dut_in[89]) v(x1.xarr.dut_in[90]) v(x1.xarr.dut_in[91]) v(x1.xarr.dut_in[92]) v(x1.xarr.dut_in[93]) v(x1.xarr.dut_in[94]) v(x1.xarr.dut_in[95])
.save v(x1.xarr.dut_in[96]) v(x1.xarr.dut_in[97]) v(x1.xarr.dut_in[98]) v(x1.xarr.dut_in[99]) v(x1.xarr.dut_in[100]) v(x1.xarr.dut_in[101]) v(x1.xarr.dut_in[102]) v(x1.xarr.dut_in[103])
.save v(x1.xarr.dut_in[104]) v(x1.xarr.dut_in[105]) v(x1.xarr.dut_in[106]) v(x1.xarr.dut_in[107]) v(x1.xarr.dut_in[108]) v(x1.xarr.dut_in[109]) v(x1.xarr.dut_in[110]) v(x1.xarr.dut_in[111])
.save v(x1.xarr.dut_in[112]) v(x1.xarr.dut_in[113]) v(x1.xarr.dut_in[114]) v(x1.xarr.dut_in[115]) v(x1.xarr.dut_in[116]) v(x1.xarr.dut_in[117]) v(x1.xarr.dut_in[118]) v(x1.xarr.dut_in[119])
.save v(x1.xarr.dut_in[120]) v(x1.xarr.dut_in[121]) v(x1.xarr.dut_in[122]) v(x1.xarr.dut_in[123]) v(x1.xarr.dut_in[124]) v(x1.xarr.dut_in[125]) v(x1.xarr.dut_in[126]) v(x1.xarr.dut_in[127])
"}
C {devices/code_shown.sym} 400 700 0 0 {name=NGSPICE only_toplevel=true
value="
* Supplies: VDEC = decoder + MUX control (5V).  VINV = all DUT inverters
* (<= 3.3V if any DUT uses 3.3V devices).
.param VDEC=5.0 VINV=3.3
* Bselsum (= sum of SEL[127:0]) and .save lines are in the PROBES block
.options method=gear reltol=1e-3
.control
tran 1e-06 128m 0 2e-05
write tb_inv_matrix.raw
let vinv = v(vdd_inv)[0]
let vdec = v(vdd_dec)[0]
let lo_inv = 0.1*vinv
let hi_inv = 0.9*vinv
let nfail = 0
let k = 0
while k < 128
  let ta = k*0.001 + 0.00025
  let tb = k*0.001 + 0.0005
  let tc = k*0.001 + 0.00075
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
  echo RESULT: PASS  (all 128 channels OK)
else
  echo RESULT: FAIL  ($&nfail of 128 channels failed)
end
echo ==================================================
.endc
"}
C {devices/launcher.sym} -600 -650 0 0 {name=h1
descr="Ctrl+click: load waveforms (tb_inv_matrix.raw)"
tclcommand="xschem raw_read $netlist_dir/tb_inv_matrix.raw tran"}
