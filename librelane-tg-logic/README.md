# 事前準備

## nixのインストール）
> [!Warning]
> nixがすでに入っている場合は不要です。

サイト([https://librelane.readthedocs.io/en/stable/installation/nix_installation/installation_linux.html](https://librelane.readthedocs.io/en/stable/installation/nix_installation/installation_linux.html))にしたがって進めてください。

## このリポジトリ+サブモジュールをクローン
```terminal
git clone --recursive <このリポジトリのリンク>
```

# ① 起動時：nixシェルに入る
```terminal
cd submodules/librelane
nix-shell shell.nix
```

# ② not回路（練習）
[ここ](test/not_logic/README.md)を参照（`test/not_logic/README.md`）

# ③ SAR_LOGICでGDSを作ろう
```terminal
../ishikai-sar-logic-verilog/
├── config     # SAR_LOGIC向けのconfig
├── README.md
├── src        # SAR_LOGICのHDLファイル
├── submodules
├── tb         # RTLシミュレーションファイル
└── test
```
