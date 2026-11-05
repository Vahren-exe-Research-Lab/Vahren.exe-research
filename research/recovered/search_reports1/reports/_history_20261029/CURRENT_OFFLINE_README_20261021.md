# 迫真戦記 ver0.67｜現行解析オフライン・検索パック

このZIPは**修復後の静的解析情報を検索するためのもの**です。旧版の`HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip`とは異なります。

- **標準DB**：`HAKUSHIN067_CURRENT_CANONICAL_20261021.sqlite`（内部関数10,274、全関数10,462）
- **標準検索**：`search_current.py`（Python 3.10+、標準ライブラリのみ）
- **現行Ghidra名**：`Hakushin067_FunctionRepair_20261021`（このZIPにはGhidra本体`.rep`は収録していません）
- **参照**：修復済みGhidra243,670件、各関数の実区間10,274件、PE再配置57,921件。
- **更新済みC**：10件。その他は従来のGhidra推定コードのまま。
- **フック用ABI**：検証済みは3件だけ。その他のABIを安全と仮定しない。
- **雇用画面V2**：ユーザーによる実機確認で失敗。修正を別チャットで調査中。静的解析の修復はV2の修復を意味しません。

PowerShell:

```powershell
python -B .\verify_offline_current_bundle_20261021.py
python -B .\search_current.py stats
python -B .\search_current.py function 0x004A1250 --max-chars 4000
python -B .\search_current.py callers 0x004D4A50
python -B .\search_current.py abi 0x00551E50
python -B .\search_current.py owner 0x004A5B28
```

新たな逆解析をPC上で行う場合には`Hakushin067_FunctionRepair_20261021.gpr`を使い、古い`Hakushin067_Index.gpr`を正本にしないでください。Ghidra原本は歴史的比較用として残します。

ZIPの各ファイルSHA256は`PACKAGE_MANIFEST.json`に記録しています。旧`search.sqlite`と`search.py`は現在の復元情報を反映していないため、このパックに含めません。既存のGhidraプロジェクト／EXE／DAT／セーブ／MASTERや他のレーンには一切書き込んでいません。

**静的証拠のみです。ゲーム本体を実行した評価・戦闘挙動のGolden比較・新規フック動作保証は行っていません。**
