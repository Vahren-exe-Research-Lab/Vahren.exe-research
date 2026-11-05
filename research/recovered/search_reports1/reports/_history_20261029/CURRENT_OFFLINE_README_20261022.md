# 迫真戦記ver0.67 最新オフライン解析パック（2026-10-22）

**このZIPが「静的解析を他のAIに渡す」ための最新版です。** 旧版の`HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip`や`HAKUSHIN067_CURRENT_AI_OFFLINE_PACK_20261021.zip`は歴史資料です。削除せず区別してください。

## 中心となるファイル

- `HAKUSHIN067_CURRENT_CANONICAL_V2_20261022.sqlite`：修復済みGhidraの10,462全関数、243,670参照、関数範囲と検証済みABI、最新分類済みPE再配置57,921件。
- `search_current.py`：標準の読み取り専用CLI（Python 3.10+ 標準ライブラリのみ）。
- `CURRENT_ACTIVE_RESEARCH_STATE_20261022.json`：PC上の現行指定とソースハッシュ。
- `GHIDRA_FURTHER_AUDIT_AND_PE_REPAIR_20261022.md`：旧PE分類の不整合156件と対応経緯。
- `verify_offline_current_v2_20261022.py`：このZIP単体でDB・提供資料のSHA・内容の簡易検査。

```powershell
python -B .\verify_offline_current_v2_20261022.py
python -B .\search_current.py stats
python -B .\search_current.py function 0x004A1250 --max-chars 4000
python -B .\search_current.py callers 0x004D4A50
python -B .\search_current.py abi 0x00551E50
python -B .\search_current.py pe-to 0x004B65D0
```

## 厳格な制限

- **静的解析であり、ゲーム・DLLフックの動作保証ではありません。**
- Ghidraの`.rep`および原作EXEはこのZIPに含めません。**Ghidra本体を修正する作業はPC上の`Hakushin067_FunctionRepair_20261021.gpr`を使用**します。
- 3関数以外の呼び出し規約は未認証。残る未所属直接CALL3,024件や未解決CALL先を勝手に所属・呼び先設定しないでください。
- ZIPには旧DB（20261021）は同梱していません。20261021→20261022への詳細差分は監査レポートを参照。旧版の復元はPC上の保存資産で行えます。
- 雇用画面V2はユーザーの実機確認で失敗済み。ここで直したのは解析データの分類です。
- 新しい解析が追加されたときは、古いZIPを改変せず、新版のマニフェストと統合DBを生成してください。
