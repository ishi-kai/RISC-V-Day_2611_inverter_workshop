v {xschem version=3.4.5 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {Testbench: vco_top  (DUT channel 0, ideal decoder)
0..2us  VCO_EN=0 : inverter mode, OUT = NOT IN checked
2us..   VCO_EN=1 : 7-stage ring, FOUT frequency measured
VCTRL swept: 1.0, 1.5, 2.0, 2.5, 3.3 V.  Results in the ngspice log.} -600 -800 0 0 0.5 0.5 {}
C {vco_top.sym} 0 0 0 0 {name=x1}
N -120 -60 -160 -60 {lab=VCTRL}
C {devices/lab_pin.sym} -160 -60 0 0 {name=l1 sig_type=std_logic lab=VCTRL}
N -120 -20 -160 -20 {lab=VCO_EN}
C {devices/lab_pin.sym} -160 -20 0 0 {name=l2 sig_type=std_logic lab=VCO_EN}
N -120 20 -160 20 {lab=D[6:0]}
C {devices/lab_pin.sym} -160 20 0 0 {name=l3 sig_type=std_logic lab=D[6:0]}
N -120 60 -160 60 {lab=IN}
C {devices/lab_pin.sym} -160 60 0 0 {name=l4 sig_type=std_logic lab=IN}
N 120 -20 160 -20 {lab=OUT}
C {devices/lab_pin.sym} 160 -20 0 1 {name=l5 sig_type=std_logic lab=OUT}
N 120 20 160 20 {lab=FOUT}
C {devices/lab_pin.sym} 160 20 0 1 {name=l6 sig_type=std_logic lab=FOUT}
N -20 -100 -20 -140 {lab=VDD_INV}
C {devices/lab_pin.sym} -20 -140 0 0 {name=l7 sig_type=std_logic lab=VDD_INV}
N 20 -100 20 -140 {lab=VDD_DEC}
C {devices/lab_pin.sym} 20 -140 0 1 {name=l8 sig_type=std_logic lab=VDD_DEC}
N 0 100 0 140 {lab=0}
C {devices/lab_pin.sym} 0 140 0 0 {name=l9 sig_type=std_logic lab=0}
C {devices/capa.sym} 350 150 0 0 {name=COUT m=1 value=100f footprint=1206 device="ceramic capacitor"}
N 350 120 350 90 {lab=OUT}
C {devices/lab_pin.sym} 350 90 0 0 {name=l10 sig_type=std_logic lab=OUT}
C {devices/gnd.sym} 350 180 0 0 {name=l_gnd_cout lab=0}
C {devices/capa.sym} 500 150 0 0 {name=CFOUT m=1 value=100f footprint=1206 device="ceramic capacitor"}
N 500 120 500 90 {lab=FOUT}
C {devices/lab_pin.sym} 500 90 0 0 {name=l11 sig_type=std_logic lab=FOUT}
C {devices/gnd.sym} 500 180 0 0 {name=l_gnd_cfout lab=0}
C {devices/vsource.sym} -800 400 0 0 {name=VDDD value="\{VDEC\}" savecurrent=false}
N -800 370 -800 340 {lab=VDD_DEC}
C {devices/lab_pin.sym} -800 340 0 0 {name=l12 sig_type=std_logic lab=VDD_DEC}
C {devices/gnd.sym} -800 430 0 0 {name=l_gnd_vddd lab=0}
C {devices/vsource.sym} -600 400 0 0 {name=VDDI value="\{VINV\}" savecurrent=false}
N -600 370 -600 340 {lab=VDD_INV}
C {devices/lab_pin.sym} -600 340 0 0 {name=l13 sig_type=std_logic lab=VDD_INV}
C {devices/gnd.sym} -600 430 0 0 {name=l_gnd_vddi lab=0}
C {devices/vsource.sym} -400 400 0 0 {name=VCT value="\{VCTRL\}" savecurrent=false}
N -400 370 -400 340 {lab=VCTRL}
C {devices/lab_pin.sym} -400 340 0 0 {name=l14 sig_type=std_logic lab=VCTRL}
C {devices/gnd.sym} -400 430 0 0 {name=l_gnd_vct lab=0}
C {devices/vsource.sym} -200 400 0 0 {name=VEN value="PULSE(0 \{VDEC\} 2u 10n 10n 1 2)" savecurrent=false}
N -200 370 -200 340 {lab=VCO_EN}
C {devices/lab_pin.sym} -200 340 0 0 {name=l15 sig_type=std_logic lab=VCO_EN}
C {devices/gnd.sym} -200 430 0 0 {name=l_gnd_ven lab=0}
C {devices/vsource.sym} 0 400 0 0 {name=VIN value="PULSE(0 \{VINV\} 0.5u 10n 10n 0.5u 1u)" savecurrent=false}
N 0 370 0 340 {lab=IN}
C {devices/lab_pin.sym} 0 340 0 0 {name=l16 sig_type=std_logic lab=IN}
C {devices/gnd.sym} 0 430 0 0 {name=l_gnd_vin lab=0}
C {devices/vsource.sym} 200 400 0 0 {name=VD0 value="\{VDEC*0\}" savecurrent=false}
N 200 370 200 340 {lab=D[0]}
C {devices/lab_pin.sym} 200 340 0 0 {name=l17 sig_type=std_logic lab=D[0]}
C {devices/gnd.sym} 200 430 0 0 {name=l_gnd_vd0 lab=0}
C {devices/vsource.sym} 400 400 0 0 {name=VD1 value="\{VDEC*0\}" savecurrent=false}
N 400 370 400 340 {lab=D[1]}
C {devices/lab_pin.sym} 400 340 0 0 {name=l18 sig_type=std_logic lab=D[1]}
C {devices/gnd.sym} 400 430 0 0 {name=l_gnd_vd1 lab=0}
C {devices/vsource.sym} 600 400 0 0 {name=VD2 value="\{VDEC*0\}" savecurrent=false}
N 600 370 600 340 {lab=D[2]}
C {devices/lab_pin.sym} 600 340 0 0 {name=l19 sig_type=std_logic lab=D[2]}
C {devices/gnd.sym} 600 430 0 0 {name=l_gnd_vd2 lab=0}
C {devices/vsource.sym} 800 400 0 0 {name=VD3 value="\{VDEC*0\}" savecurrent=false}
N 800 370 800 340 {lab=D[3]}
C {devices/lab_pin.sym} 800 340 0 0 {name=l20 sig_type=std_logic lab=D[3]}
C {devices/gnd.sym} 800 430 0 0 {name=l_gnd_vd3 lab=0}
C {devices/vsource.sym} 1000 400 0 0 {name=VD4 value="\{VDEC*0\}" savecurrent=false}
N 1000 370 1000 340 {lab=D[4]}
C {devices/lab_pin.sym} 1000 340 0 0 {name=l21 sig_type=std_logic lab=D[4]}
C {devices/gnd.sym} 1000 430 0 0 {name=l_gnd_vd4 lab=0}
C {devices/vsource.sym} 1200 400 0 0 {name=VD5 value="\{VDEC*0\}" savecurrent=false}
N 1200 370 1200 340 {lab=D[5]}
C {devices/lab_pin.sym} 1200 340 0 0 {name=l22 sig_type=std_logic lab=D[5]}
C {devices/gnd.sym} 1200 430 0 0 {name=l_gnd_vd5 lab=0}
C {devices/vsource.sym} 1400 400 0 0 {name=VD6 value="\{VDEC*0\}" savecurrent=false}
N 1400 370 1400 340 {lab=D[6]}
C {devices/lab_pin.sym} 1400 340 0 0 {name=l23 sig_type=std_logic lab=D[6]}
C {devices/gnd.sym} 1400 430 0 0 {name=l_gnd_vd6 lab=0}
C {devices/code_shown.sym} -500 700 0 0 {name=MODELS only_toplevel=true
format="tcleval( @value )"
value="
.include $::180MCU_MODELS/design.ngspice
.lib $::180MCU_MODELS/sm141064.ngspice typical
.lib $::180MCU_MODELS/sm141064.ngspice diode_typical
.include [xschem get current_dirname]/spice/decoder_7to128_ideal.spice
"}
C {devices/code_shown.sym} 400 700 0 0 {name=NGSPICE only_toplevel=true
value="
.param VDEC=5.0 VINV=3.3 VCTRL=2.0
.options method=gear reltol=1e-3
.save v(in) v(out) v(fout) v(vco_en) v(vctrl) v(x1.r0) v(x1.r3) v(x1.r6) v(x1.min) v(x1.mout)
.save v(x1.vbp) v(x1.vbn) v(vdd_inv) i(vddi)
.control
let nfail = 0
foreach vc 1.0 1.5 2.0 2.5 3.3
  alterparam VCTRL=$vc
  reset
  tran 0.1n 8u 0 0.2n
  meas tran out_lo find v(out) at=1.4u
  meas tran out_hi find v(out) at=1.9u
  meas tran tr1 when v(fout)=1.65 rise=1 td=4u
  meas tran tr11 when v(fout)=1.65 rise=11 td=4u
  meas tran iavg avg i(vddi) from=4u to=8u
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
  set fn = tb_vco_top_vctrl\{$vc\}.raw
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
"}
C {devices/launcher.sym} -600 -600 0 0 {name=h1
descr="Ctrl+click: load waveforms (VCTRL=2.0)"
tclcommand="xschem raw_read $netlist_dir/tb_vco_top_vctrl2.0.raw tran"}
