v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 210 -450 240 -450 {lab=R3}
N 360 -450 390 -450 {lab=FB}
N 300 -530 300 -500 {lab=VDD_INV}
N 300 -400 300 -370 {lab=VSS}
N 460 -450 490 -450 {lab=FB}
N 610 -450 640 -450 {lab=FOUT}
N 550 -530 550 -500 {lab=VDD_INV}
N 550 -400 550 -370 {lab=VSS}
N 1260 -500 1300 -500 {lab=IN}
N 1260 -400 1300 -400 {lab=FOUT}
N 1260 -350 1300 -350 {lab=VDD_INV}
N 1260 -250 1300 -250 {lab=VSS}
C {vco_buf1_5v0.sym} 300 -450 0 0 {name=X1}
C {devices/lab_pin.sym} 210 -450 0 0 {name=l50 sig_type=std_logic lab=IN}
C {devices/lab_pin.sym} 390 -450 0 1 {name=l51 sig_type=std_logic lab=FB}
C {devices/lab_pin.sym} 300 -530 0 0 {name=l52 sig_type=std_logic lab=VDD_INV}
C {devices/lab_pin.sym} 300 -370 0 0 {name=l53 sig_type=std_logic lab=VSS}
C {vco_buf2_5v0.sym} 550 -450 0 0 {name=X2}
C {devices/lab_pin.sym} 460 -450 0 0 {name=l54 sig_type=std_logic lab=FB}
C {devices/lab_pin.sym} 640 -450 0 1 {name=l55 sig_type=std_logic lab=FOUT}
C {devices/lab_pin.sym} 550 -530 0 0 {name=l56 sig_type=std_logic lab=VDD_INV}
C {devices/lab_pin.sym} 550 -370 0 0 {name=l57 sig_type=std_logic lab=VSS}
C {devices/iopin.sym} 1300 -500 0 0 {name=p4 lab=IN}
C {devices/opin.sym} 1300 -400 0 0 {name=p6 lab=FOUT}
C {devices/iopin.sym} 1300 -350 0 0 {name=p7 lab=VDD_INV}
C {devices/iopin.sym} 1300 -250 0 0 {name=p9 lab=VSS}
