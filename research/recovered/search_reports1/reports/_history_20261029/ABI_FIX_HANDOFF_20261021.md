# 迫真戦記ver0.67 ABI修正実施・引継ぎ
- Task: `REDEV-ABI-FIX-20261021` / 状態 `GHIDRA_CLONE_FIXED_AND_REOPENED / RAW_X86_VERIFIED / GAME_NOT_RUN`。
- 原作EXE SHA256: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
- 元の `search.sqlite` SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`、変更なし。
- Ghidra原プロジェクト `Hakushin067_Index.gpr` は変更せず、複製した `Hakushin067_ABI_Fixed_20261021.gpr` の**3関数にのみ型・引数格納位置を適用**した。
- 修正後にGhidraを終了→複製プロジェクトを再度read-onlyで開き直し、3件を新規に逆コンパイルして確認。2件は `dword` 戻り値と `return dVar...` が表示され、EXPは不明な `in_EAX` ではなく `ctx_eax` を明示的に受け取る。

## 修正済みAPI
| VA | Ghidraの修正済み表記 | 生EXEの重要条件 |
| --- | --- | --- |
| `0x00595170` | `dword __stdcall FUN_00595170(dword arg_stack_0)` | 引数Stack+4、結果EAX、`ret 4` |
| `0x00595320` | `dword __stdcall FUN_00595320(dword arg_stack_0)` | 引数Stack+4、結果EAX、`ret 4` |
| `0x00551E50` | `void __stdcall FUN_00551e50(pointer32 ctx_eax, dword arg_stack_0, dword arg_stack_1, dword arg_stack_2)` | **カスタム格納位置: ctxはEAX**, 他3引数Stack+4/8/C、`ret 12` |

**注意:** 0x00551E50のGhidra表記を一般的なCの4引数stdCall関数ポインタとして呼ぶのは危険。4引数をスタックに積むと壊れる。実際のstack引数は3個で、ctxはEAXから渡す。未検証のレジスタブリッジを勝手に実装・実行しない。
- 0x551E50のvoid戻り値自体は今回反証されていない（直接callerは結果EAXを使用しない）。2訓練関数は呼出元が結果EAXを使用するので元void宣言はABIとして不適切。

## 成果の利用場所
- 修正された複製Ghidra: `.../rea_lab/headless_analysis/Hakushin067_ABI_Fixed_20261021.gpr`。
- 独立SQLite: `search_index/ABI_VERIFIED_OVERLAY_20261021.sqlite`、3関数のネイティブABI・スタック・EAX使用・caller9箇所を収録。旧DBは元のまま。
- 自動検証: `ABI_GHIDRA_CLONE_PATCH_RESULT_20261021.json`, `ABI_GHIDRA_CLONE_READBACK_DECOMP_20261021.json`, `ABI_VERIFIED_OVERLAY_20261021.json`。
- 修正後擬似C: `ABI_CORRECTED_GHIDRA_00595170_20261021.c`, `ABI_CORRECTED_GHIDRA_00595320_20261021.c`, `ABI_CORRECTED_GHIDRA_00551E50_20261021.c`。元の10,268件擬似C ZIPは改変せず。
- DLL用ヘッダー: `hakushin_abi_verified_20261021.h`。訓練関数はEAX 32bit戻り値型。EXPの標準関数ポインタは**意図的に提供しない**。
- 自動ゲート: `abi_hook_preflight_20261021.py`。未検証関数はBLOCKED、EXP EAX橋渡し無しもBLOCKED、訓練EAX戻り値の引継ぎ無しもBLOCKED。
- テスト: 正しい指定3/3 PASS、EXPのbridge無し・訓練EAX無視・未検証アドレスの各ケースはBLOCKEDを確認。ゲーム実機へフック実行した試験ではない。

## 雇用V2と残余
- 既存の雇用画面V2はこの3関数をフックしていない。描画 `0x004D4A50` は `ret 4`、提示 `0x00453C20` は `ret 12`。V2の対応する型と一致（ただしその他の安全性を保証しない）。
- 別問題として `reloadMenu` 経由の2箇所 `0x004A5B28/0x004A5B54` が既存V2の6箇所フックに含まれておらず、実機確認・修正が必要。
- 今回はゲーム・DLL・EXE・MOD・セーブ・MASTER・Work所有キューを変更していない。原作実機テストなし。
- 利用者が今すぐ行うべきABI修復操作は不要。既存V2の確認は**バックアップ済みゲームコピーとテスト用セーブ**だけで行う。
- 今後、他レーン/Work/REAが0x595170/0x595320/0x551E50を使用するなら元Ghidra推測宣言ではなく本ABI資料を参照。
- 全10,268関数のABI修正ではない。フック対象となる関数を同じ手順で個別に認証する。

