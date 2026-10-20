v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {VCO top: 7-stage ring = 6 current-starved stages (CS1..CS5, CS6 = x4) + selected DUT of inv_matrix_top
VCO_EN=1 : R6 -> TG_VI -> MIN -> [DUT] -> MOUT -> TG_VO -> R0   (ring, FOUT = buffered R3)
VCO_EN=0 : IN -> TG_EI -> MIN -> [DUT] -> MOUT -> TG_EO -> OUT  (inverter mode), MPD holds R0 low
VDD_INV : CS stages, bias, FOUT buffer and DUTs (same swing on the whole ring)
VDD_DEC (5V) : VCO_EN logic, TG gates/N-well, decoder.   Inverter mode: VCTRL = 0 -> VCO current 0
DANT1/DANT2 : antenna diodes on VCO_EN / VCTRL (place next to the gates they feed)} -900 -930 0 0 0.5 0.5 {}
N -520 -500 -490 -500 {lab=VCTRL}
N -310 -520 -280 -520 {lab=VBP}
N -310 -480 -280 -480 {lab=VBN}
N -400 -590 -400 -560 {lab=VDD_INV}
N -400 -440 -400 -410 {lab=VSS}
N -850 -200 -820 -200 {lab=R0}
N -680 -200 -650 -200 {lab=R1}
N -770 -280 -770 -250 {lab=VBP}
N -730 -280 -730 -250 {lab=VDD_INV}
N -770 -150 -770 -120 {lab=VBN}
N -730 -150 -730 -120 {lab=VSS}
N -600 -200 -570 -200 {lab=R1}
N -430 -200 -400 -200 {lab=R2}
N -520 -280 -520 -250 {lab=VBP}
N -480 -280 -480 -250 {lab=VDD_INV}
N -520 -150 -520 -120 {lab=VBN}
N -480 -150 -480 -120 {lab=VSS}
N -350 -200 -320 -200 {lab=R2}
N -180 -200 -150 -200 {lab=R3}
N -270 -280 -270 -250 {lab=VBP}
N -230 -280 -230 -250 {lab=VDD_INV}
N -270 -150 -270 -120 {lab=VBN}
N -230 -150 -230 -120 {lab=VSS}
N -100 -200 -70 -200 {lab=R3}
N 70 -200 100 -200 {lab=R4}
N -20 -280 -20 -250 {lab=VBP}
N 20 -280 20 -250 {lab=VDD_INV}
N -20 -150 -20 -120 {lab=VBN}
N 20 -150 20 -120 {lab=VSS}
N 150 -200 180 -200 {lab=R4}
N 320 -200 350 -200 {lab=R5}
N 230 -280 230 -250 {lab=VBP}
N 270 -280 270 -250 {lab=VDD_INV}
N 230 -150 230 -120 {lab=VBN}
N 270 -150 270 -120 {lab=VSS}
N 400 -200 430 -200 {lab=R5}
N 570 -200 600 -200 {lab=R6}
N 480 -280 480 -250 {lab=VBP}
N 520 -280 520 -250 {lab=VDD_INV}
N 480 -150 480 -120 {lab=VBN}
N 520 -150 520 -120 {lab=VSS}
N -930 -110 -930 -80 {lab=R0}
N -1010 -50 -970 -50 {lab=VCO_ENB1}
N -930 -20 -930 10 {lab=VSS}
N -930 -50 -890 -50 {lab=VSS}
N 210 -450 240 -450 {lab=R3}
N 360 -450 390 -450 {lab=FB}
N 300 -530 300 -500 {lab=VDD_INV}
N 300 -400 300 -370 {lab=VSS}
N 460 -450 490 -450 {lab=FB}
N 610 -450 640 -450 {lab=FOUT}
N 550 -530 550 -500 {lab=VDD_INV}
N 550 -400 550 -370 {lab=VSS}
N 560 120 590 120 {lab=R6}
N 710 120 740 120 {lab=INV_IN}
N 620 170 620 200 {lab=VCO_EN}
N 620 40 620 70 {lab=VCO_ENB3}
N 680 40 680 70 {lab=VDD_DEC}
N 680 170 680 200 {lab=VSS}
N 560 380 590 380 {lab=IN}
N 710 380 740 380 {lab=INV_IN}
N 620 430 620 460 {lab=VCO_ENB4}
N 620 300 620 330 {lab=VCO_EN}
N 680 300 680 330 {lab=VDD_DEC}
N 680 430 680 460 {lab=VSS}
N -740 130 -710 130 {lab=INV_OUT}
N -590 130 -560 130 {lab=R0}
N -680 180 -680 210 {lab=VCO_EN}
N -680 50 -680 80 {lab=VCO_ENB1}
N -620 50 -620 80 {lab=VDD_DEC}
N -620 180 -620 210 {lab=VSS}
N -740 370 -710 370 {lab=INV_OUT}
N -590 370 -560 370 {lab=OUT}
N -680 420 -680 450 {lab=VCO_ENB2}
N -680 290 -680 320 {lab=VCO_EN}
N -620 290 -620 320 {lab=VDD_DEC}
N -620 420 -620 450 {lab=VSS}
N -1040 40 -1040 70 {lab=VSS}
N -1040 130 -1040 160 {lab=VCTRL}
N -1300 -650 -1260 -650 {lab=VCTRL}
N -1300 -600 -1260 -600 {lab=VCO_EN}
N 1260 -500 1300 -500 {lab=IN}
N 1260 -450 1300 -450 {lab=OUT}
N 1260 -400 1300 -400 {lab=FOUT}
N 1260 -170 1300 -170 {lab=INV_IN}
N 1260 -300 1300 -300 {lab=VDD_DEC}
N 1260 -250 1300 -250 {lab=VSS}
N 1260 -140 1300 -140 {lab=INV_OUT}
N 230 120 260 120 {lab=VCO_EN}
N 380 120 410 120 {lab=VCO_ENB3}
N 320 40 320 70 {lab=VDD_DEC}
N 320 170 320 200 {lab=VSS}
N 230 380 260 380 {lab=VCO_EN}
N 380 380 410 380 {lab=VCO_ENB4}
N 320 300 320 330 {lab=VDD_DEC}
N 320 430 320 460 {lab=VSS}
N -420 130 -390 130 {lab=VCO_EN}
N -270 130 -240 130 {lab=VCO_ENB1}
N -330 50 -330 80 {lab=VDD_DEC}
N -330 180 -330 210 {lab=VSS}
N -420 370 -390 370 {lab=VCO_EN}
N -270 370 -240 370 {lab=VCO_ENB2}
N -330 290 -330 320 {lab=VDD_DEC}
N -330 420 -330 450 {lab=VSS}
N -80 70 -80 100 {lab=VSS}
N -80 160 -80 190 {lab=VCO_EN}
N 100 70 100 100 {lab=VSS}
N 100 160 100 190 {lab=VCO_EN}
N -90 320 -90 350 {lab=VSS}
N -90 410 -90 440 {lab=VCO_EN}
N 90 320 90 350 {lab=VSS}
N 90 410 90 440 {lab=VCO_EN}
N 1260 -330 1300 -330 {lab=VDD_DEC}
C {vco_bias_5v0.sym} -400 -500 0 0 {name=X2}
C {devices/lab_pin.sym} -520 -500 0 0 {name=l5 sig_type=std_logic lab=VCTRL}
C {devices/lab_pin.sym} -280 -520 0 1 {name=l6 sig_type=std_logic lab=VBP}
C {devices/lab_pin.sym} -280 -480 0 1 {name=l7 sig_type=std_logic lab=VBN}
C {devices/lab_pin.sym} -400 -590 0 0 {name=l8 sig_type=std_logic lab=VDD_INV}
C {devices/lab_pin.sym} -400 -410 0 0 {name=l9 sig_type=std_logic lab=VSS}
C {cs_inv_5v0.sym} -750 -200 0 0 {name=X3}
C {devices/lab_pin.sym} -850 -200 0 0 {name=l10 sig_type=std_logic lab=R0}
C {devices/lab_pin.sym} -650 -200 0 1 {name=l11 sig_type=std_logic lab=R1}
C {devices/lab_pin.sym} -770 -280 0 0 {name=l12 sig_type=std_logic lab=VBP}
C {devices/lab_pin.sym} -730 -280 0 1 {name=l13 sig_type=std_logic lab=VDD_INV}
C {devices/lab_pin.sym} -770 -120 0 0 {name=l14 sig_type=std_logic lab=VBN}
C {devices/lab_pin.sym} -730 -120 0 1 {name=l15 sig_type=std_logic lab=VSS}
C {cs_inv_5v0.sym} -500 -200 0 0 {name=X4}
C {devices/lab_pin.sym} -600 -200 0 0 {name=l16 sig_type=std_logic lab=R1}
C {devices/lab_pin.sym} -400 -200 0 1 {name=l17 sig_type=std_logic lab=R2}
C {devices/lab_pin.sym} -520 -280 0 0 {name=l18 sig_type=std_logic lab=VBP}
C {devices/lab_pin.sym} -480 -280 0 1 {name=l19 sig_type=std_logic lab=VDD_INV}
C {devices/lab_pin.sym} -520 -120 0 0 {name=l20 sig_type=std_logic lab=VBN}
C {devices/lab_pin.sym} -480 -120 0 1 {name=l21 sig_type=std_logic lab=VSS}
C {cs_inv_5v0.sym} -250 -200 0 0 {name=X5}
C {devices/lab_pin.sym} -350 -200 0 0 {name=l22 sig_type=std_logic lab=R2}
C {devices/lab_pin.sym} -150 -200 0 1 {name=l23 sig_type=std_logic lab=R3}
C {devices/lab_pin.sym} -270 -280 0 0 {name=l24 sig_type=std_logic lab=VBP}
C {devices/lab_pin.sym} -230 -280 0 1 {name=l25 sig_type=std_logic lab=VDD_INV}
C {devices/lab_pin.sym} -270 -120 0 0 {name=l26 sig_type=std_logic lab=VBN}
C {devices/lab_pin.sym} -230 -120 0 1 {name=l27 sig_type=std_logic lab=VSS}
C {cs_inv_5v0.sym} 0 -200 0 0 {name=X6}
C {devices/lab_pin.sym} -100 -200 0 0 {name=l28 sig_type=std_logic lab=R3}
C {devices/lab_pin.sym} 100 -200 0 1 {name=l29 sig_type=std_logic lab=R4}
C {devices/lab_pin.sym} -20 -280 0 0 {name=l30 sig_type=std_logic lab=VBP}
C {devices/lab_pin.sym} 20 -280 0 1 {name=l31 sig_type=std_logic lab=VDD_INV}
C {devices/lab_pin.sym} -20 -120 0 0 {name=l32 sig_type=std_logic lab=VBN}
C {devices/lab_pin.sym} 20 -120 0 1 {name=l33 sig_type=std_logic lab=VSS}
C {cs_inv_5v0.sym} 250 -200 0 0 {name=X7}
C {devices/lab_pin.sym} 150 -200 0 0 {name=l34 sig_type=std_logic lab=R4}
C {devices/lab_pin.sym} 350 -200 0 1 {name=l35 sig_type=std_logic lab=R5}
C {devices/lab_pin.sym} 230 -280 0 0 {name=l36 sig_type=std_logic lab=VBP}
C {devices/lab_pin.sym} 270 -280 0 1 {name=l37 sig_type=std_logic lab=VDD_INV}
C {devices/lab_pin.sym} 230 -120 0 0 {name=l38 sig_type=std_logic lab=VBN}
C {devices/lab_pin.sym} 270 -120 0 1 {name=l39 sig_type=std_logic lab=VSS}
C {cs_inv_x4_5v0.sym} 500 -200 0 0 {name=X8}
C {devices/lab_pin.sym} 400 -200 0 0 {name=l40 sig_type=std_logic lab=R5}
C {devices/lab_pin.sym} 600 -200 0 1 {name=l41 sig_type=std_logic lab=R6}
C {devices/lab_pin.sym} 480 -280 0 0 {name=l42 sig_type=std_logic lab=VBP}
C {devices/lab_pin.sym} 520 -280 0 1 {name=l43 sig_type=std_logic lab=VDD_INV}
C {devices/lab_pin.sym} 480 -120 0 0 {name=l44 sig_type=std_logic lab=VBN}
C {devices/lab_pin.sym} 520 -120 0 1 {name=l45 sig_type=std_logic lab=VSS}
C {symbols/nfet_05v0.sym} -950 -50 0 0 {name=MPD
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
C {devices/lab_pin.sym} -930 -110 0 0 {name=l46 sig_type=std_logic lab=R0}
C {devices/lab_pin.sym} -1010 -50 0 0 {name=l47 sig_type=std_logic lab=VCO_ENB1}
C {devices/lab_pin.sym} -930 10 0 0 {name=l48 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} -890 -50 0 1 {name=l49 sig_type=std_logic lab=VSS}
C {vco_buf1_5v0.sym} 300 -450 0 0 {name=X9}
C {devices/lab_pin.sym} 210 -450 0 0 {name=l50 sig_type=std_logic lab=R3}
C {devices/lab_pin.sym} 390 -450 0 1 {name=l51 sig_type=std_logic lab=FB}
C {devices/lab_pin.sym} 300 -530 0 0 {name=l52 sig_type=std_logic lab=VDD_INV}
C {devices/lab_pin.sym} 300 -370 0 0 {name=l53 sig_type=std_logic lab=VSS}
C {vco_buf2_5v0.sym} 550 -450 0 0 {name=X10}
C {devices/lab_pin.sym} 460 -450 0 0 {name=l54 sig_type=std_logic lab=FB}
C {devices/lab_pin.sym} 640 -450 0 1 {name=l55 sig_type=std_logic lab=FOUT}
C {devices/lab_pin.sym} 550 -530 0 0 {name=l56 sig_type=std_logic lab=VDD_INV}
C {devices/lab_pin.sym} 550 -370 0 0 {name=l57 sig_type=std_logic lab=VSS}
C {tgate_5v0.sym} 650 120 0 0 {name=X11}
C {devices/lab_pin.sym} 560 120 0 0 {name=l58 sig_type=std_logic lab=R6}
C {devices/lab_pin.sym} 740 120 0 1 {name=l59 sig_type=std_logic lab=INV_IN}
C {devices/lab_pin.sym} 620 200 0 0 {name=l60 sig_type=std_logic lab=VCO_EN}
C {devices/lab_pin.sym} 620 40 0 0 {name=l61 sig_type=std_logic lab=VCO_ENB3}
C {devices/lab_pin.sym} 680 40 0 1 {name=l62 sig_type=std_logic lab=VDD_DEC}
C {devices/lab_pin.sym} 680 200 0 1 {name=l63 sig_type=std_logic lab=VSS}
C {tgate_5v0.sym} 650 380 0 0 {name=X12}
C {devices/lab_pin.sym} 560 380 0 0 {name=l64 sig_type=std_logic lab=IN}
C {devices/lab_pin.sym} 740 380 0 1 {name=l65 sig_type=std_logic lab=INV_IN}
C {devices/lab_pin.sym} 620 460 0 0 {name=l66 sig_type=std_logic lab=VCO_ENB4}
C {devices/lab_pin.sym} 620 300 0 0 {name=l67 sig_type=std_logic lab=VCO_EN}
C {devices/lab_pin.sym} 680 300 0 1 {name=l68 sig_type=std_logic lab=VDD_DEC}
C {devices/lab_pin.sym} 680 460 0 1 {name=l69 sig_type=std_logic lab=VSS}
C {tgate_5v0.sym} -650 130 0 0 {name=X13}
C {devices/lab_pin.sym} -740 130 0 0 {name=l70 sig_type=std_logic lab=INV_OUT}
C {devices/lab_pin.sym} -560 130 0 1 {name=l71 sig_type=std_logic lab=R0}
C {devices/lab_pin.sym} -680 210 0 0 {name=l72 sig_type=std_logic lab=VCO_EN}
C {devices/lab_pin.sym} -680 50 0 0 {name=l73 sig_type=std_logic lab=VCO_ENB1}
C {devices/lab_pin.sym} -620 50 0 1 {name=l74 sig_type=std_logic lab=VDD_DEC}
C {devices/lab_pin.sym} -620 210 0 1 {name=l75 sig_type=std_logic lab=VSS}
C {tgate_5v0.sym} -650 370 0 0 {name=X14}
C {devices/lab_pin.sym} -740 370 0 0 {name=l76 sig_type=std_logic lab=INV_OUT}
C {devices/lab_pin.sym} -560 370 0 1 {name=l77 sig_type=std_logic lab=OUT}
C {devices/lab_pin.sym} -680 450 0 0 {name=l78 sig_type=std_logic lab=VCO_ENB2}
C {devices/lab_pin.sym} -680 290 0 0 {name=l79 sig_type=std_logic lab=VCO_EN}
C {devices/lab_pin.sym} -620 290 0 1 {name=l80 sig_type=std_logic lab=VDD_DEC}
C {devices/lab_pin.sym} -620 450 0 1 {name=l81 sig_type=std_logic lab=VSS}
C {symbols/diode_nw2ps_06v0.sym} -1040 100 0 0 {name=DANT2
model=diode_nw2ps_06v0
r_w=1.4u
r_l=1.2u
m=1}
C {devices/lab_pin.sym} -1040 40 0 0 {name=l90 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} -1040 160 0 0 {name=l91 sig_type=std_logic lab=VCTRL}
C {devices/ipin.sym} -1300 -650 0 0 {name=p1 lab=VCTRL}
C {devices/ipin.sym} -1300 -600 0 0 {name=p2 lab=VCO_EN}
C {devices/iopin.sym} 1300 -500 0 0 {name=p4 lab=IN}
C {devices/iopin.sym} 1300 -450 0 0 {name=p5 lab=OUT}
C {devices/opin.sym} 1300 -400 0 0 {name=p6 lab=FOUT}
C {devices/iopin.sym} 1300 -170 0 0 {name=p7 lab=INV_IN}
C {devices/iopin.sym} 1300 -300 0 0 {name=p8 lab=VDD_DEC}
C {devices/iopin.sym} 1300 -250 0 0 {name=p9 lab=VSS}
C {devices/iopin.sym} 1300 -140 0 0 {name=p3 lab=INV_OUT}
C {inv_ctrl_5v0.sym} 320 120 0 0 {name=X15}
C {devices/lab_pin.sym} 230 120 0 0 {name=l82 sig_type=std_logic lab=VCO_EN}
C {devices/lab_pin.sym} 410 120 0 1 {name=l83 sig_type=std_logic lab=VCO_ENB3}
C {devices/lab_pin.sym} 320 40 0 0 {name=l84 sig_type=std_logic lab=VDD_DEC}
C {devices/lab_pin.sym} 320 200 0 0 {name=l85 sig_type=std_logic lab=VSS}
C {inv_ctrl_5v0.sym} 320 380 0 0 {name=X16}
C {devices/lab_pin.sym} 230 380 0 0 {name=l86 sig_type=std_logic lab=VCO_EN}
C {devices/lab_pin.sym} 410 380 0 1 {name=l87 sig_type=std_logic lab=VCO_ENB4}
C {devices/lab_pin.sym} 320 300 0 0 {name=l92 sig_type=std_logic lab=VDD_DEC}
C {devices/lab_pin.sym} 320 460 0 0 {name=l93 sig_type=std_logic lab=VSS}
C {inv_ctrl_5v0.sym} -330 130 0 0 {name=X17}
C {devices/lab_pin.sym} -420 130 0 0 {name=l94 sig_type=std_logic lab=VCO_EN}
C {devices/lab_pin.sym} -240 130 0 1 {name=l95 sig_type=std_logic lab=VCO_ENB1}
C {devices/lab_pin.sym} -330 50 0 0 {name=l96 sig_type=std_logic lab=VDD_DEC}
C {devices/lab_pin.sym} -330 210 0 0 {name=l97 sig_type=std_logic lab=VSS}
C {inv_ctrl_5v0.sym} -330 370 0 0 {name=X18}
C {devices/lab_pin.sym} -420 370 0 0 {name=l98 sig_type=std_logic lab=VCO_EN}
C {devices/lab_pin.sym} -240 370 0 1 {name=l99 sig_type=std_logic lab=VCO_ENB2}
C {devices/lab_pin.sym} -330 290 0 0 {name=l100 sig_type=std_logic lab=VDD_DEC}
C {devices/lab_pin.sym} -330 450 0 0 {name=l101 sig_type=std_logic lab=VSS}
C {symbols/diode_nw2ps_06v0.sym} -80 130 0 0 {name=DANT3
model=diode_nw2ps_06v0
r_w=1.4u
r_l=1.2u
m=1}
C {devices/lab_pin.sym} -80 70 0 0 {name=l1 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} -80 190 0 0 {name=l2 sig_type=std_logic lab=VCO_EN}
C {symbols/diode_nw2ps_06v0.sym} 100 130 0 0 {name=DANT4
model=diode_nw2ps_06v0
r_w=1.4u
r_l=1.2u
m=1}
C {devices/lab_pin.sym} 100 70 0 0 {name=l3 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} 100 190 0 0 {name=l4 sig_type=std_logic lab=VCO_EN}
C {symbols/diode_nw2ps_06v0.sym} -90 380 0 0 {name=DANT5
model=diode_nw2ps_06v0
r_w=1.4u
r_l=1.2u
m=1}
C {devices/lab_pin.sym} -90 320 0 0 {name=l102 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} -90 440 0 0 {name=l103 sig_type=std_logic lab=VCO_EN}
C {symbols/diode_nw2ps_06v0.sym} 90 380 0 0 {name=DANT6
model=diode_nw2ps_06v0
r_w=1.4u
r_l=1.2u
m=1}
C {devices/lab_pin.sym} 90 320 0 0 {name=l104 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} 90 440 0 0 {name=l105 sig_type=std_logic lab=VCO_EN}
C {devices/iopin.sym} 1300 -330 0 0 {name=p10 lab=VDD_INV}
