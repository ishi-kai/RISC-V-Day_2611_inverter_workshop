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
N 70 150 100 150 {lab=IN}
N 220 150 250 150 {lab=DUT_IN}
N 130 70 130 100 {lab=SELB}
N 190 70 190 100 {lab=VDD_DEC}
N 130 200 130 230 {lab=SEL}
N 190 200 190 230 {lab=VSS}
N 380 340 380 370 {lab=DUT_IN}
N 300 400 340 400 {lab=SELB}
N 380 430 380 460 {lab=VSS}
N 380 400 420 400 {lab=VSS}
N 10 340 10 370 {lab=VSS}
N 10 430 10 460 {lab=SEL}
N -180 -200 -140 -200 {lab=IN}
N -140 -150 -100 -150 {lab=SEL}
N 620 130 660 130 {lab=VDD_DEC}
N 620 180 660 180 {lab=VSS}
N 620 70 660 70 {lab=DUT_IN}
C {inv_ctrl_5v0.sym} 160 -100 0 0 {name=XSELB}
C {devices/lab_pin.sym} 70 -100 0 0 {name=l1 sig_type=std_logic lab=SEL}
C {devices/lab_pin.sym} 250 -100 0 1 {name=l2 sig_type=std_logic lab=SELB}
C {devices/lab_pin.sym} 160 -180 0 0 {name=l3 sig_type=std_logic lab=VDD_DEC}
C {devices/lab_pin.sym} 160 -20 0 0 {name=l4 sig_type=std_logic lab=VSS}
C {tgate_5v0.sym} 160 150 0 0 {name=XTGIN}
C {devices/lab_pin.sym} 70 150 0 0 {name=l5 sig_type=std_logic lab=IN}
C {devices/lab_pin.sym} 250 150 0 1 {name=l6 sig_type=std_logic lab=DUT_IN}
C {devices/lab_pin.sym} 130 70 0 0 {name=l7 sig_type=std_logic lab=SELB}
C {devices/lab_pin.sym} 190 70 0 1 {name=l8 sig_type=std_logic lab=VDD_DEC}
C {devices/lab_pin.sym} 130 230 0 0 {name=l9 sig_type=std_logic lab=SEL}
C {devices/lab_pin.sym} 190 230 0 1 {name=l10 sig_type=std_logic lab=VSS}
C {symbols/nfet_05v0.sym} 360 400 0 0 {name=MPD
L=0.60u
W=0.42u
nf=1
m=1
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=nfet_05v0
spiceprefix=X
}
C {devices/lab_pin.sym} 380 340 0 0 {name=l17 sig_type=std_logic lab=DUT_IN}
C {devices/lab_pin.sym} 300 400 0 0 {name=l18 sig_type=std_logic lab=SELB}
C {devices/lab_pin.sym} 380 460 0 0 {name=l19 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} 420 400 0 1 {name=l20 sig_type=std_logic lab=VSS}
C {symbols/diode_nw2ps_06v0.sym} 10 400 0 0 {name=DANT
model=diode_nw2ps_06v0
r_w=1.4u
r_l=1.2u
m=1}
C {devices/lab_pin.sym} 10 340 0 0 {name=l21 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} 10 460 0 0 {name=l22 sig_type=std_logic lab=SEL}
C {devices/iopin.sym} -140 -200 0 0 {name=p1 lab=IN}
C {devices/ipin.sym} -140 -150 0 0 {name=p2 lab=SEL}
C {devices/iopin.sym} 660 130 0 0 {name=p6 lab=VDD_DEC}
C {devices/iopin.sym} 660 180 0 0 {name=p7 lab=VSS}
C {devices/iopin.sym} 660 70 0 0 {name=p4 lab=DUT_IN}
