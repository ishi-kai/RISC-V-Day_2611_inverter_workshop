v {xschem version=3.4.5 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {Current-starved inverter x4 (last VCO stage, drives MIN bus), 5V devices
MPC pfet_05v0 W=64u L=1u (gate VBP)   MP pfet_05v0 W=12u L=0.50u
MN nfet_05v0 W=6u L=0.60u   MNC nfet_05v0 W=16u L=1u (gate VBN)
Stage current = 64u/16u x bias current from vco_bias_5v0} -300 -500 0 0 0.4 0.4 {}
C {symbols/pfet_05v0.sym} 0 -230 0 0 {name=MPC
L=1u
W=64u
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
N 20 -260 20 -290 {lab=VDD}
C {devices/lab_pin.sym} 20 -290 0 0 {name=l1 sig_type=std_logic lab=VDD}
N -20 -230 -60 -230 {lab=VBP}
C {devices/lab_pin.sym} -60 -230 0 0 {name=l2 sig_type=std_logic lab=VBP}
N 20 -200 20 -170 {lab=NP}
C {devices/lab_pin.sym} 20 -170 0 0 {name=l3 sig_type=std_logic lab=NP}
N 20 -230 60 -230 {lab=VDD}
C {devices/lab_pin.sym} 60 -230 0 1 {name=l4 sig_type=std_logic lab=VDD}
C {symbols/pfet_05v0.sym} 0 -80 0 0 {name=MP
L=0.50u
W=12u
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
N 20 -110 20 -140 {lab=NP}
C {devices/lab_pin.sym} 20 -140 0 0 {name=l5 sig_type=std_logic lab=NP}
N -20 -80 -60 -80 {lab=A}
C {devices/lab_pin.sym} -60 -80 0 0 {name=l6 sig_type=std_logic lab=A}
N 20 -50 20 -20 {lab=Y}
C {devices/lab_pin.sym} 20 -20 0 0 {name=l7 sig_type=std_logic lab=Y}
N 20 -80 60 -80 {lab=VDD}
C {devices/lab_pin.sym} 60 -80 0 1 {name=l8 sig_type=std_logic lab=VDD}
C {symbols/nfet_05v0.sym} 0 80 0 0 {name=MN
L=0.60u
W=6u
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
N 20 50 20 20 {lab=Y}
C {devices/lab_pin.sym} 20 20 0 0 {name=l9 sig_type=std_logic lab=Y}
N -20 80 -60 80 {lab=A}
C {devices/lab_pin.sym} -60 80 0 0 {name=l10 sig_type=std_logic lab=A}
N 20 110 20 140 {lab=NN}
C {devices/lab_pin.sym} 20 140 0 0 {name=l11 sig_type=std_logic lab=NN}
N 20 80 60 80 {lab=VSS}
C {devices/lab_pin.sym} 60 80 0 1 {name=l12 sig_type=std_logic lab=VSS}
C {symbols/nfet_05v0.sym} 0 230 0 0 {name=MNC
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
model=nfet_05v0
spiceprefix=X
}
N 20 200 20 170 {lab=NN}
C {devices/lab_pin.sym} 20 170 0 0 {name=l13 sig_type=std_logic lab=NN}
N -20 230 -60 230 {lab=VBN}
C {devices/lab_pin.sym} -60 230 0 0 {name=l14 sig_type=std_logic lab=VBN}
N 20 260 20 290 {lab=VSS}
C {devices/lab_pin.sym} 20 290 0 0 {name=l15 sig_type=std_logic lab=VSS}
N 20 230 60 230 {lab=VSS}
C {devices/lab_pin.sym} 60 230 0 1 {name=l16 sig_type=std_logic lab=VSS}
C {devices/ipin.sym} -400 -300 0 0 {name=p1 lab=A}
N -400 -300 -360 -300 {lab=A}
C {devices/opin.sym} 400 -300 0 0 {name=p2 lab=Y}
N 400 -300 360 -300 {lab=Y}
C {devices/ipin.sym} -400 -250 0 0 {name=p3 lab=VBP}
N -400 -250 -360 -250 {lab=VBP}
C {devices/iopin.sym} 400 -250 0 0 {name=p4 lab=VDD}
N 400 -250 360 -250 {lab=VDD}
C {devices/ipin.sym} -400 -200 0 0 {name=p5 lab=VBN}
N -400 -200 -360 -200 {lab=VBN}
C {devices/iopin.sym} 400 -200 0 0 {name=p6 lab=VSS}
N 400 -200 360 -200 {lab=VSS}
