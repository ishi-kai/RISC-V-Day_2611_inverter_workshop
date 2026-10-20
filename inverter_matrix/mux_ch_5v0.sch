v {xschem version=3.4.5 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {MUX for one channel:  IN --[TG_in]-- DUT_IN    DUT_OUT --[TG_out]-- OUT
SEL=1 : channel selected.  SELB is generated locally.
SEL=0 : MPD pulls DUT_IN to VSS (no shoot-through in unselected DUTs).
All devices 5V (05v0).  VDD_DEC : SELB inverter + TG N-well (VDD_DEC >= VDD_INV).
DANT : antenna diode on the long SEL line (reverse biased, place next to the SEL gates).} -300 -480 0 0 0.4 0.4 {}
C {inv_ctrl_5v0.sym} -300 -200 0 0 {name=XSELB}
N -360 -200 -390 -200 {lab=SEL}
C {devices/lab_pin.sym} -390 -200 0 0 {name=l1 sig_type=std_logic lab=SEL}
N -240 -200 -210 -200 {lab=SELB}
C {devices/lab_pin.sym} -210 -200 0 1 {name=l2 sig_type=std_logic lab=SELB}
N -300 -250 -300 -280 {lab=VDD_DEC}
C {devices/lab_pin.sym} -300 -280 0 0 {name=l3 sig_type=std_logic lab=VDD_DEC}
N -300 -150 -300 -120 {lab=VSS}
C {devices/lab_pin.sym} -300 -120 0 0 {name=l4 sig_type=std_logic lab=VSS}
C {tgate_5v0.sym} -300 50 0 0 {name=XTGIN}
N -360 50 -390 50 {lab=IN}
C {devices/lab_pin.sym} -390 50 0 0 {name=l5 sig_type=std_logic lab=IN}
N -240 50 -210 50 {lab=DUT_IN}
C {devices/lab_pin.sym} -210 50 0 1 {name=l6 sig_type=std_logic lab=DUT_IN}
N -330 0 -330 -30 {lab=SELB}
C {devices/lab_pin.sym} -330 -30 0 0 {name=l7 sig_type=std_logic lab=SELB}
N -270 0 -270 -30 {lab=VDD_DEC}
C {devices/lab_pin.sym} -270 -30 0 1 {name=l8 sig_type=std_logic lab=VDD_DEC}
N -330 100 -330 130 {lab=SEL}
C {devices/lab_pin.sym} -330 130 0 0 {name=l9 sig_type=std_logic lab=SEL}
N -270 100 -270 130 {lab=VSS}
C {devices/lab_pin.sym} -270 130 0 1 {name=l10 sig_type=std_logic lab=VSS}
C {tgate_5v0.sym} 300 50 0 0 {name=XTGOUT}
N 240 50 210 50 {lab=DUT_OUT}
C {devices/lab_pin.sym} 210 50 0 0 {name=l11 sig_type=std_logic lab=DUT_OUT}
N 360 50 390 50 {lab=OUT}
C {devices/lab_pin.sym} 390 50 0 1 {name=l12 sig_type=std_logic lab=OUT}
N 270 0 270 -30 {lab=SELB}
C {devices/lab_pin.sym} 270 -30 0 0 {name=l13 sig_type=std_logic lab=SELB}
N 330 0 330 -30 {lab=VDD_DEC}
C {devices/lab_pin.sym} 330 -30 0 1 {name=l14 sig_type=std_logic lab=VDD_DEC}
N 270 100 270 130 {lab=SEL}
C {devices/lab_pin.sym} 270 130 0 0 {name=l15 sig_type=std_logic lab=SEL}
N 330 100 330 130 {lab=VSS}
C {devices/lab_pin.sym} 330 130 0 1 {name=l16 sig_type=std_logic lab=VSS}
C {symbols/nfet_05v0.sym} -100 300 0 0 {name=MPD
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
N -80 270 -80 240 {lab=DUT_IN}
C {devices/lab_pin.sym} -80 240 0 0 {name=l17 sig_type=std_logic lab=DUT_IN}
N -120 300 -160 300 {lab=SELB}
C {devices/lab_pin.sym} -160 300 0 0 {name=l18 sig_type=std_logic lab=SELB}
N -80 330 -80 360 {lab=VSS}
C {devices/lab_pin.sym} -80 360 0 0 {name=l19 sig_type=std_logic lab=VSS}
N -80 300 -40 300 {lab=VSS}
C {devices/lab_pin.sym} -40 300 0 1 {name=l20 sig_type=std_logic lab=VSS}
C {symbols/diode_nw2ps_06v0.sym} -450 300 0 0 {name=DANT
model=diode_nw2ps_06v0
r_w=1.4u
r_l=1.2u
m=1}
N -450 270 -450 240 {lab=VSS}
C {devices/lab_pin.sym} -450 240 0 0 {name=l21 sig_type=std_logic lab=VSS}
N -450 330 -450 360 {lab=SEL}
C {devices/lab_pin.sym} -450 360 0 0 {name=l22 sig_type=std_logic lab=SEL}
C {devices/iopin.sym} -600 -300 0 0 {name=p1 lab=IN}
N -600 -300 -640 -300 {lab=IN}
C {devices/ipin.sym} -600 -250 0 0 {name=p2 lab=SEL}
N -600 -250 -560 -250 {lab=SEL}
C {devices/iopin.sym} 600 -300 0 0 {name=p3 lab=OUT}
N 600 -300 560 -300 {lab=OUT}
C {devices/iopin.sym} 600 -250 0 0 {name=p4 lab=DUT_IN}
N 600 -250 560 -250 {lab=DUT_IN}
C {devices/iopin.sym} 600 -200 0 0 {name=p5 lab=DUT_OUT}
N 600 -200 560 -200 {lab=DUT_OUT}
C {devices/iopin.sym} 600 -150 0 0 {name=p6 lab=VDD_DEC}
N 600 -150 560 -150 {lab=VDD_DEC}
C {devices/iopin.sym} 600 -100 0 0 {name=p7 lab=VSS}
N 600 -100 560 -100 {lab=VSS}
