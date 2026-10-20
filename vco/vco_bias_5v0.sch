v {xschem version=3.4.5 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {VCO bias (current-starved VCO), 5V devices
MNI: VCTRL -> I  (nfet_05v0 W=2u L=2u, long L: stays saturated)
MPB: PMOS diode -> VBP   MPM/MNM: mirror -> NMOS diode -> VBN
MPB/MPM pfet_05v0 W=16u L=1u   MNM nfet_05v0 W=4u L=1u
VCTRL = 0 -> I = 0 (VCO off)} -300 -500 0 0 0.4 0.4 {}
C {symbols/pfet_05v0.sym} -150 -80 0 0 {name=MPB
L=1u
W=16u
nf=1
m=1
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=pfet_05v0
spiceprefix=X
}
N -130 -110 -130 -140 {lab=VDD}
C {devices/lab_pin.sym} -130 -140 0 0 {name=l1 sig_type=std_logic lab=VDD}
N -170 -80 -210 -80 {lab=VBP}
C {devices/lab_pin.sym} -210 -80 0 0 {name=l2 sig_type=std_logic lab=VBP}
N -130 -50 -130 -20 {lab=VBP}
C {devices/lab_pin.sym} -130 -20 0 0 {name=l3 sig_type=std_logic lab=VBP}
N -130 -80 -90 -80 {lab=VDD}
C {devices/lab_pin.sym} -90 -80 0 1 {name=l4 sig_type=std_logic lab=VDD}
C {symbols/nfet_05v0.sym} -150 80 0 0 {name=MNI
L=2u
W=2u
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
N -130 50 -130 20 {lab=VBP}
C {devices/lab_pin.sym} -130 20 0 0 {name=l5 sig_type=std_logic lab=VBP}
N -170 80 -210 80 {lab=VCTRL}
C {devices/lab_pin.sym} -210 80 0 0 {name=l6 sig_type=std_logic lab=VCTRL}
N -130 110 -130 140 {lab=VSS}
C {devices/lab_pin.sym} -130 140 0 0 {name=l7 sig_type=std_logic lab=VSS}
N -130 80 -90 80 {lab=VSS}
C {devices/lab_pin.sym} -90 80 0 1 {name=l8 sig_type=std_logic lab=VSS}
C {symbols/pfet_05v0.sym} 150 -80 0 0 {name=MPM
L=1u
W=16u
nf=1
m=1
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=pfet_05v0
spiceprefix=X
}
N 170 -110 170 -140 {lab=VDD}
C {devices/lab_pin.sym} 170 -140 0 0 {name=l9 sig_type=std_logic lab=VDD}
N 130 -80 90 -80 {lab=VBP}
C {devices/lab_pin.sym} 90 -80 0 0 {name=l10 sig_type=std_logic lab=VBP}
N 170 -50 170 -20 {lab=VBN}
C {devices/lab_pin.sym} 170 -20 0 0 {name=l11 sig_type=std_logic lab=VBN}
N 170 -80 210 -80 {lab=VDD}
C {devices/lab_pin.sym} 210 -80 0 1 {name=l12 sig_type=std_logic lab=VDD}
C {symbols/nfet_05v0.sym} 150 80 0 0 {name=MNM
L=1u
W=4u
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
N 170 50 170 20 {lab=VBN}
C {devices/lab_pin.sym} 170 20 0 0 {name=l13 sig_type=std_logic lab=VBN}
N 130 80 90 80 {lab=VBN}
C {devices/lab_pin.sym} 90 80 0 0 {name=l14 sig_type=std_logic lab=VBN}
N 170 110 170 140 {lab=VSS}
C {devices/lab_pin.sym} 170 140 0 0 {name=l15 sig_type=std_logic lab=VSS}
N 170 80 210 80 {lab=VSS}
C {devices/lab_pin.sym} 210 80 0 1 {name=l16 sig_type=std_logic lab=VSS}
C {devices/ipin.sym} -450 -300 0 0 {name=p1 lab=VCTRL}
N -450 -300 -410 -300 {lab=VCTRL}
C {devices/opin.sym} 450 -300 0 0 {name=p2 lab=VBP}
N 450 -300 410 -300 {lab=VBP}
C {devices/opin.sym} 450 -250 0 0 {name=p3 lab=VBN}
N 450 -250 410 -250 {lab=VBN}
C {devices/iopin.sym} 450 -200 0 0 {name=p4 lab=VDD}
N 450 -200 410 -200 {lab=VDD}
C {devices/iopin.sym} 450 -150 0 0 {name=p5 lab=VSS}
N 450 -150 410 -150 {lab=VSS}
