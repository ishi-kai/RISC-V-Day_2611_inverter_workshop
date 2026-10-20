v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N -400 -530 -360 -530 {lab=VCTRL}
N -400 -490 -360 -490 {lab=VCO_EN}
N -400 -450 -360 -450 {lab=D[6:0]}
N -400 -410 -360 -410 {lab=IN}
N -120 -490 -80 -490 {lab=OUT}
N -120 -450 -80 -450 {lab=FOUT}
C {devices/ipin.sym} -400 -530 0 0 {name=p1 lab=VCTRL}
C {devices/ipin.sym} -400 -490 0 0 {name=p2 lab=VCO_EN}
C {devices/ipin.sym} -400 -450 0 0 {name=p3 lab=D[6:0]}
C {devices/iopin.sym} -400 -410 0 1 {name=p4 lab=IN}
C {devices/iopin.sym} -80 -490 0 0 {name=p5 lab=OUT}
C {devices/opin.sym} -80 -450 0 0 {name=p6 lab=FOUT}
C {devices/iopin.sym} -260 -570 0 1 {name=p7 lab=VDD_INV}
C {devices/iopin.sym} -220 -570 0 0 {name=p8 lab=VDD_DEC}
C {devices/iopin.sym} -240 -370 0 0 {name=p9 lab=VSS}
C {vco/vco_top.sym} -240 -470 0 0 {name=x1}
