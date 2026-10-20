v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {Transmission gate, 5V devices (P = 3 x N: PMOS N-well on VDD_DEC=5V)
nfet_05v0 W=2u L=0.60u // pfet_05v0 W=6u L=0.50u
EN=1 / ENB=0 : A <-> B ON   Ron ~1-1.5k (0..3.3V, tt)} -200 -340 0 0 0.4 0.4 {}
N 70 -100 100 -100 {lab=SEL}
N 220 -100 250 -100 {lab=SELB}
N 160 -180 160 -150 {lab=VDD_DEC}
N 160 -50 160 -20 {lab=VSS}
N 10 340 10 370 {lab=VSS}
N 10 430 10 460 {lab=SEL}
N -180 -200 -140 -200 {lab=IN}
N -140 -150 -100 -150 {lab=SEL}
N 620 130 660 130 {lab=VDD_DEC}
N 620 180 660 180 {lab=VSS}
N 620 70 660 70 {lab=DUT_OUT}
N 90 170 120 170 {lab=DUT_OUT}
N 240 170 270 170 {lab=OUT}
N 150 90 150 120 {lab=SELB}
N 210 90 210 120 {lab=VDD_DEC}
N 150 220 150 250 {lab=SEL}
N 210 220 210 250 {lab=VSS}
C {inv_ctrl_5v0.sym} 160 -100 0 0 {name=XSELB}
C {devices/lab_pin.sym} 70 -100 0 0 {name=l1 sig_type=std_logic lab=SEL}
C {devices/lab_pin.sym} 250 -100 0 1 {name=l2 sig_type=std_logic lab=SELB}
C {devices/lab_pin.sym} 160 -180 0 0 {name=l3 sig_type=std_logic lab=VDD_DEC}
C {devices/lab_pin.sym} 160 -20 0 0 {name=l4 sig_type=std_logic lab=VSS}
C {symbols/diode_nw2ps_06v0.sym} 10 400 0 0 {name=DANT
model=diode_nw2ps_06v0
r_w=1.4u
r_l=1.2u
m=1}
C {devices/lab_pin.sym} 10 340 0 0 {name=l21 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} 10 460 0 0 {name=l22 sig_type=std_logic lab=SEL}
C {devices/iopin.sym} -140 -200 0 0 {name=p1 lab=OUT}
C {devices/ipin.sym} -140 -150 0 0 {name=p2 lab=SEL}
C {devices/iopin.sym} 660 130 0 0 {name=p6 lab=VDD_DEC}
C {devices/iopin.sym} 660 180 0 0 {name=p7 lab=VSS}
C {devices/iopin.sym} 660 70 0 0 {name=p4 lab=DUT_OUT}
C {tgate_5v0.sym} 180 170 0 0 {name=XTGOUT}
C {devices/lab_pin.sym} 90 170 0 0 {name=l11 sig_type=std_logic lab=DUT_OUT}
C {devices/lab_pin.sym} 270 170 0 1 {name=l12 sig_type=std_logic lab=OUT}
C {devices/lab_pin.sym} 150 90 0 0 {name=l13 sig_type=std_logic lab=SELB}
C {devices/lab_pin.sym} 210 90 0 1 {name=l14 sig_type=std_logic lab=VDD_DEC}
C {devices/lab_pin.sym} 150 250 0 0 {name=l15 sig_type=std_logic lab=SEL}
C {devices/lab_pin.sym} 210 250 0 1 {name=l16 sig_type=std_logic lab=VSS}
