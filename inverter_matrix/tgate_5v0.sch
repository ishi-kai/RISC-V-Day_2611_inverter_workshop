v {xschem version=3.4.5 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {Transmission gate, 5V devices (P = 3 x N: PMOS N-well on VDD_DEC=5V)
nfet_05v0 W=2u L=0.60u // pfet_05v0 W=6u L=0.50u
EN=1 / ENB=0 : A <-> B ON   Ron ~1-1.5k (0..3.3V, tt)} -200 -340 0 0 0.4 0.4 {}
C {symbols/nfet_05v0.sym} 0 100 0 0 {name=MN
L=0.60u
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
N 20 70 20 40 {lab=A}
C {devices/lab_pin.sym} 20 40 0 0 {name=l1 sig_type=std_logic lab=A}
N -20 100 -60 100 {lab=EN}
C {devices/lab_pin.sym} -60 100 0 0 {name=l2 sig_type=std_logic lab=EN}
N 20 130 20 160 {lab=B}
C {devices/lab_pin.sym} 20 160 0 0 {name=l3 sig_type=std_logic lab=B}
N 20 100 60 100 {lab=VSS}
C {devices/lab_pin.sym} 60 100 0 1 {name=l4 sig_type=std_logic lab=VSS}
C {symbols/pfet_05v0.sym} 0 -100 0 0 {name=MP
L=0.50u
W=6u
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
N 20 -130 20 -160 {lab=A}
C {devices/lab_pin.sym} 20 -160 0 0 {name=l5 sig_type=std_logic lab=A}
N -20 -100 -60 -100 {lab=ENB}
C {devices/lab_pin.sym} -60 -100 0 0 {name=l6 sig_type=std_logic lab=ENB}
N 20 -70 20 -40 {lab=B}
C {devices/lab_pin.sym} 20 -40 0 0 {name=l7 sig_type=std_logic lab=B}
N 20 -100 60 -100 {lab=VDD}
C {devices/lab_pin.sym} 60 -100 0 1 {name=l8 sig_type=std_logic lab=VDD}
C {devices/iopin.sym} -300 -200 0 0 {name=p1 lab=A}
N -300 -200 -340 -200 {lab=A}
C {devices/iopin.sym} 300 -200 0 0 {name=p2 lab=B}
N 300 -200 260 -200 {lab=B}
C {devices/ipin.sym} -300 -150 0 0 {name=p3 lab=EN}
N -300 -150 -260 -150 {lab=EN}
C {devices/ipin.sym} -300 -100 0 0 {name=p4 lab=ENB}
N -300 -100 -260 -100 {lab=ENB}
C {devices/iopin.sym} 300 -150 0 0 {name=p5 lab=VDD}
N 300 -150 260 -150 {lab=VDD}
C {devices/iopin.sym} 300 -100 0 0 {name=p6 lab=VSS}
N 300 -100 260 -100 {lab=VSS}
