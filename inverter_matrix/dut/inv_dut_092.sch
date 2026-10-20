v {xschem version=3.4.5 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {DUT #92 (from dut_params.csv)
nfet_03v3 W=0.90u L=0.60u / pfet_03v3 W=2.70u L=0.60u} -200 -300 0 0 0.4 0.4 {}
C {symbols/pfet_03v3.sym} 0 -80 0 0 {name=MP
L=0.60u
W=2.70u
nf=1
m=1
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=pfet_03v3
spiceprefix=X
}
N 20 -110 20 -140 {lab=VDD}
C {devices/lab_pin.sym} 20 -140 0 0 {name=l1 sig_type=std_logic lab=VDD}
N -20 -80 -60 -80 {lab=A}
C {devices/lab_pin.sym} -60 -80 0 0 {name=l2 sig_type=std_logic lab=A}
N 20 -50 20 -20 {lab=Y}
C {devices/lab_pin.sym} 20 -20 0 0 {name=l3 sig_type=std_logic lab=Y}
N 20 -80 60 -80 {lab=VDD}
C {devices/lab_pin.sym} 60 -80 0 1 {name=l4 sig_type=std_logic lab=VDD}
C {symbols/nfet_03v3.sym} 0 80 0 0 {name=MN
L=0.60u
W=0.90u
nf=1
m=1
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=nfet_03v3
spiceprefix=X
}
N 20 50 20 20 {lab=Y}
C {devices/lab_pin.sym} 20 20 0 0 {name=l5 sig_type=std_logic lab=Y}
N -20 80 -60 80 {lab=A}
C {devices/lab_pin.sym} -60 80 0 0 {name=l6 sig_type=std_logic lab=A}
N 20 110 20 140 {lab=VSS}
C {devices/lab_pin.sym} 20 140 0 0 {name=l7 sig_type=std_logic lab=VSS}
N 20 80 60 80 {lab=VSS}
C {devices/lab_pin.sym} 60 80 0 1 {name=l8 sig_type=std_logic lab=VSS}
C {devices/ipin.sym} -300 -150 0 0 {name=p1 lab=A}
N -300 -150 -260 -150 {lab=A}
C {devices/opin.sym} 300 -150 0 0 {name=p2 lab=Y}
N 300 -150 260 -150 {lab=Y}
C {devices/iopin.sym} 300 -100 0 0 {name=p3 lab=VDD}
N 300 -100 260 -100 {lab=VDD}
C {devices/iopin.sym} 300 -50 0 0 {name=p4 lab=VSS}
N 300 -50 260 -50 {lab=VSS}
