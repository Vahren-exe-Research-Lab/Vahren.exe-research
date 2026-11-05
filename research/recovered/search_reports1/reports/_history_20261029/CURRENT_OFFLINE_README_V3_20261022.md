# 迫真戦記ver0.67 — 最新の静的解析検索パック（2026-10-22 / 第3版）

**必ずこのREADMEと `CURRENT_ACTIVE_RESEARCH_STATE_V3_20261022.json` を最初に参照してください。**

`HAKUSHIN067_CURRENT_CANONICAL_V3_20261022.sqlite` は、原本EXEの機械語と修復済みGhidraを照合した最新の静的検索DBです。

主な修復点：
- 関数全10,462件（内部10,274）、Ghidraの参照243,670件、PE再配置57,921件、ABI確認済み3件は第2版から全行保持。
- Ghidraが `UNCONDITIONAL_CALL` と記録した51,213件を、**実際のE8直接CALL（44,889件）とE9/EB JMP（6,324件）に分離**。生の原作EXEの命令バイト・相対分岐先を全51,213件検査して不一致0件。
- `search_current.py callers` はE8だけ返します。`jump-callers`はJMPだけ、`flow-callers`は両方を機械語種別付きで返します。JMPが必ず末尾呼出しであるとは限りません。
- `search_current.py search` は**大文字小文字を無視した文字列の部分一致**。以前の全文検索では漏れた `ctx_ea` などが検索できます。`search-token` は単語／フレーズ単位の高速検索。
- 修復済みの擬似Cは10件。その他は元のGhidra推定。3件のABI以外のフック引数・戻り値は独立認証が必要です。

## ZIP展開後の使い方

Windows PowerShell:

```powershell
python -B .\verify_offline_current_v3_20261022.py
python -B .\search_current.py stats
python -B .\search_current.py function 0x004A1250
python -B .\search_current.py callers 0x004D4A50
python -B .\search_current.py jump-callers 0x005B6635
python -B .\search_current.py search ctx_ea
python -B .\search_current.py search-token load
python -B .\search_current.py abi 0x00551E50
```

このZIPには、旧検索DB、旧CLI、原作EXE、Ghidraの元/修復プロジェクト .rep、ゲームの製品コードは**含まれていません**。PC上の静的解析に必要な正本は、`Hakushin067_FunctionRepair_20261021.gpr`です。オフラインの他AIにはこのZIPを渡してください。

**原作ゲームや雇用画面DLLの実機動作は未検証。ユーザーからは雇用画面V2の失敗報告あり。** ゲーム改造の動作成功を主張するものではありません。
