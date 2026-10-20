v {xschem version=3.4.5 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {Inverter matrix top:  D[6:0] -> decoder_7to128 -> SEL[127:0] -> 128ch TG MUX (in/out)
VDD_DEC = 5V : decoder + MUX control + TG N-well     VDD_INV : all DUT inverters     VSS common
If any DUT uses 3.3V devices: VDD_INV <= 3.3V and IN <= 3.3V
DANT0..6 : antenna diodes on D[6:0] (place next to the decoder input pins)} -400 -450 0 0 0.5 0.5 {}
C {decoder_7to128.sym} -250 0 0 0 {name=XDEC}
N -250 -50 -250 -80 {lab=VDD_DEC}
C {devices/lab_pin.sym} -250 -80 0 0 {name=l1 sig_type=std_logic lab=VDD_DEC}
N -250 50 -250 80 {lab=VSS}
C {devices/lab_pin.sym} -250 80 0 0 {name=l2 sig_type=std_logic lab=VSS}
N -370 0 -400 0 {lab=D[6:0]}
C {devices/lab_pin.sym} -400 0 0 0 {name=l3 sig_type=std_logic lab=D[6:0]}
N -130 0 -100 0 {lab=SEL[127:0]}
C {devices/lab_pin.sym} -100 0 0 1 {name=l4 sig_type=std_logic lab=SEL[127:0]}
C {inv_array_128.sym} 250 0 0 0 {name=XARR}
N 130 -30 100 -30 {lab=IN}
C {devices/lab_pin.sym} 100 -30 0 0 {name=l5 sig_type=std_logic lab=IN}
N 130 30 100 30 {lab=SEL[127:0]}
C {devices/lab_pin.sym} 100 30 0 0 {name=l6 sig_type=std_logic lab=SEL[127:0]}
N 370 0 400 0 {lab=OUT}
C {devices/lab_pin.sym} 400 0 0 1 {name=l7 sig_type=std_logic lab=OUT}
N 220 -80 220 -110 {lab=VDD_INV}
C {devices/lab_pin.sym} 220 -110 0 0 {name=l8 sig_type=std_logic lab=VDD_INV}
N 280 -80 280 -110 {lab=VDD_DEC}
C {devices/lab_pin.sym} 280 -110 0 1 {name=l9 sig_type=std_logic lab=VDD_DEC}
N 250 80 250 110 {lab=VSS}
C {devices/lab_pin.sym} 250 110 0 0 {name=l10 sig_type=std_logic lab=VSS}
C {symbols/diode_nw2ps_06v0.sym} -1000 300 0 0 {name=DANT0
model=diode_nw2ps_06v0
r_w=1.4u
r_l=1.2u
m=1}
N -1000 270 -1000 240 {lab=VSS}
C {devices/lab_pin.sym} -1000 240 0 0 {name=l11 sig_type=std_logic lab=VSS}
N -1000 330 -1000 360 {lab=D[0]}
C {devices/lab_pin.sym} -1000 360 0 0 {name=l12 sig_type=std_logic lab=D[0]}
C {symbols/diode_nw2ps_06v0.sym} -820 300 0 0 {name=DANT1
model=diode_nw2ps_06v0
r_w=1.4u
r_l=1.2u
m=1}
N -820 270 -820 240 {lab=VSS}
C {devices/lab_pin.sym} -820 240 0 0 {name=l13 sig_type=std_logic lab=VSS}
N -820 330 -820 360 {lab=D[1]}
C {devices/lab_pin.sym} -820 360 0 0 {name=l14 sig_type=std_logic lab=D[1]}
C {symbols/diode_nw2ps_06v0.sym} -640 300 0 0 {name=DANT2
model=diode_nw2ps_06v0
r_w=1.4u
r_l=1.2u
m=1}
N -640 270 -640 240 {lab=VSS}
C {devices/lab_pin.sym} -640 240 0 0 {name=l15 sig_type=std_logic lab=VSS}
N -640 330 -640 360 {lab=D[2]}
C {devices/lab_pin.sym} -640 360 0 0 {name=l16 sig_type=std_logic lab=D[2]}
C {symbols/diode_nw2ps_06v0.sym} -460 300 0 0 {name=DANT3
model=diode_nw2ps_06v0
r_w=1.4u
r_l=1.2u
m=1}
N -460 270 -460 240 {lab=VSS}
C {devices/lab_pin.sym} -460 240 0 0 {name=l17 sig_type=std_logic lab=VSS}
N -460 330 -460 360 {lab=D[3]}
C {devices/lab_pin.sym} -460 360 0 0 {name=l18 sig_type=std_logic lab=D[3]}
C {symbols/diode_nw2ps_06v0.sym} -280 300 0 0 {name=DANT4
model=diode_nw2ps_06v0
r_w=1.4u
r_l=1.2u
m=1}
N -280 270 -280 240 {lab=VSS}
C {devices/lab_pin.sym} -280 240 0 0 {name=l19 sig_type=std_logic lab=VSS}
N -280 330 -280 360 {lab=D[4]}
C {devices/lab_pin.sym} -280 360 0 0 {name=l20 sig_type=std_logic lab=D[4]}
C {symbols/diode_nw2ps_06v0.sym} -100 300 0 0 {name=DANT5
model=diode_nw2ps_06v0
r_w=1.4u
r_l=1.2u
m=1}
N -100 270 -100 240 {lab=VSS}
C {devices/lab_pin.sym} -100 240 0 0 {name=l21 sig_type=std_logic lab=VSS}
N -100 330 -100 360 {lab=D[5]}
C {devices/lab_pin.sym} -100 360 0 0 {name=l22 sig_type=std_logic lab=D[5]}
C {symbols/diode_nw2ps_06v0.sym} 80 300 0 0 {name=DANT6
model=diode_nw2ps_06v0
r_w=1.4u
r_l=1.2u
m=1}
N 80 270 80 240 {lab=VSS}
C {devices/lab_pin.sym} 80 240 0 0 {name=l23 sig_type=std_logic lab=VSS}
N 80 330 80 360 {lab=D[6]}
C {devices/lab_pin.sym} 80 360 0 0 {name=l24 sig_type=std_logic lab=D[6]}
C {devices/iopin.sym} -650 -250 0 0 {name=p1 lab=IN}
N -650 -250 -690 -250 {lab=IN}
C {devices/ipin.sym} -650 -200 0 0 {name=p2 lab=D[6:0]}
N -650 -200 -610 -200 {lab=D[6:0]}
C {devices/iopin.sym} 650 -250 0 0 {name=p3 lab=OUT}
N 650 -250 610 -250 {lab=OUT}
C {devices/iopin.sym} 650 -200 0 0 {name=p4 lab=VDD_INV}
N 650 -200 610 -200 {lab=VDD_INV}
C {devices/iopin.sym} 650 -150 0 0 {name=p5 lab=VDD_DEC}
N 650 -150 610 -150 {lab=VDD_DEC}
C {devices/iopin.sym} 650 -100 0 0 {name=p6 lab=VSS}
N 650 -100 610 -100 {lab=VSS}
