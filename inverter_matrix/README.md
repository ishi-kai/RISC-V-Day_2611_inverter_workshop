# インバータマトリクス（128ch DUT インバータ ＋ 7→128 デコーダ ＋ TG MUX）

128 個の DUT インバータを 1 組の IN / OUT パッドで切り替えて測定する回路。
D[6:0] をデコーダ（LibreLane で作成した 7→128 one-hot デコーダ）で SEL[127:0] に変換し、
各チャネルの TG（トランスミッションゲート）MUX で 1 つの DUT だけを IN / OUT につなぐ。
PDK: GF180MCU (gf180mcuD)。MUX・デコーダは 5V 品（`nfet_05v0` / `pfet_05v0`）、DUT は 3.3V 品 / 5V 品の混在が可能。

`../vco` の VCO はこの `inv_matrix_top` の選択 DUT をリングの 7 段目として使う。

## ブロック図

```
              D[6:0]
                │
        ┌───────▼────────┐  SEL[127:0] (one-hot, 0 / VDD_DEC)
        │ decoder_7to128 ├──────────────┬──────────────┬─── ...
        └────────────────┘              │              │
                                  ┌─────▼─────┐  ┌─────▼─────┐
  IN ──────────────┬──────────────┤ mux_ch #0 ├──┤ mux_ch #1 ├── ... (128ch)
                   │              │ TG_in     │  │           │
                   │              │   │       │  │           │
                   │              │ DUT_IN ─► inv_dut_000 ─► DUT_OUT
                   │              │ TG_out    │  │           │
  OUT ─────────────┴──────────────┤           ├──┤           ├── ...
                                  └───────────┘  └───────────┘
```

mux_ch_5v0（1 チャネル分）:

| SEL | TG_in / TG_out | DUT_IN | 動作 |
|---|---|---|---|
| 1 | ON | IN | 選択チャネル: IN → DUT → OUT |
| 0 | OFF | MPD で VSS に固定 | 非選択チャネル: DUT 入力を固定して貫通電流を防ぐ |

SELB は各チャネル内の inv_ctrl_5v0 で生成する（長い SELB 配線を持たない）。

## 回路（ファイル）

| ファイル | 内容 |
|---|---|
| `dut/inv_dut_000..127.sch/.sym` | DUT インバータ（ピン A, Y, VDD, VSS）。`apply_dut_csv.py` で差し替え |
| `inv_ctrl_5v0.sch/.sym` | SEL → SELB 反転（5V 品） |
| `tgate_5v0.sch/.sym` | トランスミッションゲート（5V 品、PMOS N-well = VDD_DEC） |
| `mux_ch_5v0.sch/.sym` | 1 チャネルの MUX: TG_in, TG_out, SELB 生成, MPD, SEL のアンテナダイオード DANT |
| `inv_array_128.sch/.sym` | 128 × (mux_ch_5v0 + inv_dut_NNN)、IN / OUT 共通 |
| `decoder_7to128.sym` | LibreLane で作ったデコーダ（`~/librelane-tg-logic`）のシンボル |
| `inv_matrix_top.sch/.sym` | decoder_7to128 + inv_array_128 + D[6:0] のアンテナダイオード DANT0〜6 |
| `tb_inv_matrix.sch` | テストベンチ（全 128ch を順に選択して IN→OUT 反転と SEL の one-hot を確認） |
| `spice/decoder_7to128_xs.spice` | デコーダの抽出ネットリスト ＋ xschem のピン順ラッパ |
| `layout/inv_dut_NNN.gds/.cdl` | DUT のレイアウトと LVS 用リファレンスネットリスト |
| `xsch_lib.py` | 共通ヘルパ（回路図書き出し、`MODEL_MIN`、`ANT_D`） |
| `gen_schematics.py` | 上記の回路図・シンボルの生成 |
| `apply_dut_csv.py` | CSV から DUT 回路図を差し替え |
| `gen_tb.py` | テストベンチ生成 |
| `gen_layout.py`, `check_layout.py` | DUT レイアウト生成と DRC / LVS |
| `sim_layout/` | レイアウト抽出ネットリスト（`../layout/workshop_inverter.gds`）での全 128ch インバータ動作確認（下記） |

## 電源

| 電源 | 対象 |
|---|---|
| VDD_DEC (5V) | デコーダ、SELB インバータ、TG のゲート振幅と PMOS N-well |
| VDD_INV | DUT インバータのみ（128ch 共通）。VDD_INV ≦ VDD_DEC |
| VSS | 共通 |

3.3V 品の DUT が 1 つでもある場合は、VDD_INV と IN を 3.3V 以下にする。

## サイズ

| 素子 | モデル | W / L |
|---|---|---|
| TG（tgate_5v0）N / P | nfet_05v0 / pfet_05v0 | 2u / 0.6u、6u / 0.5u |
| SELB インバータ（inv_ctrl_5v0）N / P | nfet_05v0 / pfet_05v0 | 1u / 0.6u、2u / 0.5u |
| MPD（非選択時の DUT_IN プルダウン） | nfet_05v0 | 0.42u / 0.6u |
| DANT（SEL）、DANT0〜6（D[6:0]）アンテナダイオード | diode_nw2ps_06v0 | W=1.4u × L=1.2u |

TG の ON 抵抗は約 0.93k〜1.5kΩ（tt、0〜3.3V）。PMOS の N-well が VDD_DEC (5V) なので基板効果で弱くなる分、P = 3 × N にしている。

### トランジスタの最小 W / L（`xsch_lib.py` の `MODEL_MIN`）

| モデル | 最小 W | 最小 L |
|---|---|---|
| nfet_03v3 / pfet_03v3 | 0.22u | 0.28u |
| nfet_05v0 | **0.42u** | 0.60u |
| pfet_05v0 | **0.36u** | 0.50u |
| nfet_06v0 / pfet_06v0 | 0.30u（未確認） | 0.70u / 0.55u |

PDK の xschem シンボルの初期値は 5V/6V 品とも W=0.30u だが、5V 品はこれでは最小 W を満たさない。
`gen_schematics.py` は W を指定しないトランジスタにこの最小値を使い、`apply_dut_csv.py` は CSV の値をこの最小値でチェックする。
6V 品の最小 W はまだ確認していない（現在の設計では未使用）。

## 設計上のポイント

1. **非選択チャネルの固定**: SEL=0 のチャネルは TG_in が OFF になり DUT 入力が浮くので、MPD で VSS に固定して
   中間電位による貫通電流を防ぐ。
2. **TG の電源**: TG のゲート振幅と PMOS N-well を VDD_DEC (5V) にして ON 抵抗を下げる。
   DUT 側（IN / OUT / VDD_INV）は 3.3V 以下でも使える。
3. **アンテナ対策**: ゲートにしかつながらない長い配線に Nwell/Psub ダイオード（`diode_nw2ps_06v0`、W=1.4u×L=1.2u、
   アノード=VSS、常に逆バイアス）を入れている。
   - **SEL[i]**（mux_ch_5v0 の DANT）: デコーダからアレイ全体に伸びる 128 本の線。つながるゲートは
     SELB インバータ ＋ TG_N × 2（約 3.6µm²）だけ。
   - **D[6:0]**（inv_matrix_top の DANT0〜6）: デコーダはハードマクロで、LibreLane のアンテナチェックは
     マクロ内部の配線しか見ないため、パッドからデコーダ入力までの配線は別途対策が要る。

   GF180 ANT.16_ii（厚膜ゲート）: メタル周長×0.54 / (ゲート面積 + 15×ダイオード面積) ≦ 400（メタル層ごと）。
   SEL では許容メタル周長が約 2.7mm（ダイオードなし）→ 約 21mm（1.4u×1.2u）になる。
   レイアウトでは **保護するゲートのすぐ近く**（SEL は各チャネルの mux_ch 内、D[6:0] はデコーダ入力ピンの横）に置くこと。
   サイズは `xsch_lib.py` の `ANT_D` で変更できる（`../vco` も同じ値を使う）。
   IN / OUT / DUT_IN / DUT_OUT は TG やトランジスタの拡散につながるので不要。
4. **IN / OUT バスの寄生**: 非選択 127ch の OFF TG の接合容量（約 3fF × 128 ≈ 0.4pF）が IN / OUT に乗る。

## 使い方

```bash
python3 gen_schematics.py              # 回路図・シンボル生成（既存の dut/ は上書きしない）
python3 gen_schematics.py --reset-dut  # dut/ も最小サイズの 5V インバータで作り直す
python3 apply_dut_csv.py dut_params.csv [--dry-run]   # CSV で DUT を差し替え
python3 gen_layout.py dut_params.csv [--only 0,5,17]  # DUT レイアウト生成
python3 check_layout.py [--only 0,5,17] [--jobs N]    # DRC / LVS
python3 gen_tb.py [--ideal-dec] [--slot=<秒>]         # テストベンチ生成
xschem --rcfile xschemrc tb_inv_matrix.sch            # Netlist → Simulate
```

レイアウト抽出ネットリストでの全 128ch 確認（`sim_layout/`、手順は下記の節を参照）:

```bash
cd sim_layout
python3 prep_netlist.py                       # ../../layout/workshop_inverter_extracted.cir → ngspice 用
python3 gen_tb.py                             # tb_ref.spice（DUT 単体）
ngspice -b tb_ref.spice > tb_ref.log
python3 gen_tb.py                             # tb_ch000〜127.spice（tb_ref.log の VM を使う）
./run_all.sh 4                                # 4 並列で実行（1ch 約 3 分）
python3 collect.py                            # results.csv / summary.txt、PASS / FAIL
```

DUT の CSV 形式（`dut_params_example.csv` も参照）:

```
DUT_NUM, P_MODEL, P_W, P_L, N_MODEL, N_W, N_L
000, pfet_05v0, 0.36u, 0.50u, nfet_05v0, 0.42u, 0.60u
```

テストベンチはアンテナダイオードのモデルのため `sm141064.ngspice diode_typical` も読み込む。
`--ideal-dec` を付けるとデコーダを動作モデルに置き換え、スロットを 20µs にする（数時間 → 約 5 分）。

## シミュレーション結果（tt, VDD_INV=IN=3.3V, VDD_DEC=5V, 理想デコーダ `--ideal-dec`, スロット 20µs, MPD W=0.42u, アンテナダイオード W=1.4u×L=1.2u）

D[6:0] を 0〜127 と順に切り替え、各チャネルで IN=0 / IN=3.3V のときの DUT_IN・OUT と SEL の合計を測定した
（`sim/tb_inv_matrix_idealdec.log`、実行時間 約 4 分）。

| 測定 | 期待値 | 結果（128ch の最小〜最大） |
|---|---|---|
| IN=0 のとき DUT_IN | low | 4.65 nV |
| IN=0 のとき OUT | high | 3.300 V |
| IN=3.3V のとき DUT_IN | high | 3.300 V |
| IN=3.3V のとき OUT | low | 1.06〜3.07 µV |
| SEL の合計（one-hot） | VDEC = 5V | 5.000 V |

**RESULT: PASS（128 チャネルすべて OK）**

- アンテナダイオードを 2u×2u → 1.4u×1.2u に縮小した後に再実行。結果は縮小前と 6 桁目まで一致（影響なし）。
- 抽出したスタンダードセルのデコーダを使う本番のテストベンチ（`tb_inv_matrix.sch`、スロット 1ms）は数時間かかるため、今回は実行していない。

## レイアウト抽出ネットリストでの全 128ch 確認（`sim_layout/`）

`../layout/workshop_inverter.gds`（＝ `workshop_inverter_fullDUT.gds`）を KLayout LVS（`run_lvs.py --combine --top_lvl_pins --spice_comments`、
LVS 一致）で抽出したネットリストを使う。デコーダはスタンダードセルの実回路。寄生 RC は含まない。
条件: tt、VDD_DEC=5V、VCO_EN=VCTRL=0（インバータモード）、D[6:0]=k 固定、OUT は無負荷（バス容量のみ）。

### 方法

- **電圧は FET の耐圧に合わせる**: 5V 品（`*_05v0`）は VDD_INV=IN 振幅=5.0V、3.3V 品（`*_03v3`）は 3.3V。
  ch ごとに `dut_params.csv` から決める。
- **IN の波形**: 0 → VINV → 0。VM_ref ± 0.4V の範囲だけゆっくり（0.5V/µs）動かし、それ以外は 100ns で動かす。
  チップ全体の DC スイープは毎点 gmin stepping になり 1ch に数時間かかるので、過渡解析にした。
  OUT バス（約 0.4pF）の遅れで上り / 下りの VM が ±30mV ずれるので、両者の平均を VM とする。
- **参照（`tb_ref.spice`）**: 同じ抽出ネットリストの `inv_dut_NNN` を単体で（デコーダ・MUX なし）DC スイープした VM、
  ゲイン、VIL / VIH（ゲイン = −1）。
- 全ノードに `rshunt=1e12`（5V で 5pA）を入れて、VCTRL=0 で浮くノードの収束を助けている。

### 判定（`collect.py`）

| 項目 | 内容 | 基準 |
|---|---|---|
| inverter | IN=0 で OUT=VOH、IN=VINV で OUT=VOL、選択 DUT の入力 (A) が IN と同じ | VOH ≧ VINV−10mV、VOL ≦ 10mV、\|A−IN\| ≦ 10mV |
| decoder | IN=VINV で 128 個の DUT の A を全部見て、High なのが inv_dut_k だけ | A[k] > 0.99·VINV、他 127 個 < 10mV |
| VM vs ref | マトリクス経由の VM と DUT 単体の VM の差 | ≦ 10mV |
| period-32 | ch k, k+32, k+64, k+96（同じサイズ）の VOH / VOL / VM | 差 ≦ 2mV |
| P/N ratio | 同じモデル・同じ L では VM が Wp/Wn だけで決まり、Wp/Wn とともに上がる | 同じ比で差 ≦ 30mV、単調増加 |

period-32 は、D[5] / D[6] が固着していても同じ値になるため、デコーダの確認としては不十分。
そのため decoder の項目で、選ばれた DUT が k 番だけであることを直接確認している。

### 結果（`sim_layout/summary.txt`、`results.csv`）

| 測定 | 結果（128ch） |
|---|---|
| VOH（IN=0） | VINV（差 0.000mV） |
| VOL（IN=VINV） | 最大 3.1µV |
| 非選択 127 個の DUT 入力（IN=VINV） | 最大 0.026µV |
| VM − VM_ref | −0.13 〜 +4.37mV |
| k, k+32, k+64, k+96 の差 | VOH / VOL / VM とも 0.00mV（32 組すべて） |

VM（4 回の繰り返しの平均。同じ比のセルは DUT の大きさ順）:

| モデル | L | Wp/Wn=1 | Wp/Wn=2 | Wp/Wn=3 |
|---|---|---|---|---|
| 5V 品（VINV=5.0V） | 0.6µm | 1.807 / 1.818 / 1.822V | 2.179 / 2.190 / 2.193V | 2.410 / 2.419 / 2.422V |
| 5V 品 | 1.2µm | – | 2.118 / 2.123 / 2.124V | 2.320 / 2.324 / 2.326V |
| 5V 品 | 1.8µm | – | – | 2.278V |
| 3.3V 品（VINV=3.3V） | 0.3µm | 1.315 / 1.315 / 1.313V | 1.521 / 1.523 / 1.522V | 1.648 / 1.650 / 1.648V |
| 3.3V 品 | 0.6µm | – | 1.465 / 1.463 / 1.459V | 1.575 / 1.571 / 1.567V |
| 3.3V 品 | 0.9µm | – | – | 1.535V |

**RESULT: PASS（128 チャネルすべて OK）**

- 同じ Wp/Wn なら VM は DUT の大きさにほぼよらず（差 15mV 以内）、Wp/Wn を 1 → 2 → 3 にすると上がる。
  L を長くすると VM は少し下がる（5V 品、Wp/Wn=3: L=0.6µm で 2.42V → L=1.8µm で 2.28V）。
- 021 / 053 / 085 / 117 の N_W は 2.60u → 2.70u に修正した（Wp/Wn 2.08 → 2.00、VM 1.534V → 1.522V）。
  DUT レイアウトを作り直し、トップの GDS ではセルを差し替え（`../layout/replace_dut.py`）、DRC クリーン / LVS 一致を確認した。
  修正していない ch の結果は、修正前のネットリストでの結果と最大 0.01mV の差で一致した。
- バッティングタップ修正後の再実行（2026-10-23）: VCO の `cs_inv_5v0` / `cs_inv_x4_5v0` / `vco_bias_5v0` / `vco_buf_5v0` で、
  基板と別ネット（ドレインなど）の S/D に接していたタップ（PCell の Bulk Tie）を外し、タップを別に置いた。
  修正後の `../layout/workshop_inverter_fullDUT.gds` から抽出し直して（LVS 一致）全 128ch を再実行。
  結果は修正前と全 128ch で一致（VOH / VOL / VM / 非選択 DUT 入力の差 0）。
- **注意**: VDD_INV は 128 個の DUT で共通。5V 品を 5V で測ると、3.3V 品の DUT 64 個にも VDD_INV=5V がかかる
  （入力は MPD で VSS に固定されるが、電源と出力には 5V がかかる）。
  実チップでは 3.3V 品を壊さないよう、VDD_INV ≦ 3.3V で測るか、過電圧を許容するかを決めること。

## 検証状況

- DUT レイアウト: `dut_params.csv`（3.3V 品 64 個 ＋ 5V 品 64 個）の 128 個すべて DRC クリーン / LVS 一致
  （`layout/check_summary.txt`）。
- MPD の W 変更（0.30u → 0.42u）とアンテナダイオード追加の後、`../vco` のテストベンチ
  （inv_matrix_top を含む、ch0）でインバータモード PASS、VCO 周波数の変化は最大 0.03%。
  結果は `../vco/README.md` を参照。
- アンテナダイオードを 1.4u×1.2u に縮小した後も、上記マトリクスと `../vco` の両テストベンチで PASS（変化は実質なし）。
- `tgate_5v0_in`（SELB インバータ ＋ TG_in ＋ MPD ＋ DANT）のレイアウト: KLayout LVS 一致。
  - ネットリストは KLayout マクロ `gf180_lvs_make`（`~/.klayout/tech/macros/gf180_lvs_make.lym`）で作る。
    サブサーキット呼び出しを `X0_<名前>` にするので、LVS オプション `schematic_translate` の
    変換（X の後が数字でないインスタンスの X を外す）で壊れない。
  - diode_nw2ps の A/P は P+ タップ側で抽出される（KLayout API PCell では 0.36µm × L）が、
    LVS はダイオードの A/P を比較しないので一致になる。
