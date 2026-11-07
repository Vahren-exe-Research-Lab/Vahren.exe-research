# REA 2026-11-01 21H P0｜__local_unwind4 を呼ぶ4経路と NLG/trampoline
- 研究ID: `REA-LOCAL-20261101-21H-P0-UNWIND-FOUR-CALLERS-NLG-STATIC-01`
- owner/task: REA/P0-T015 (CRT SEH4), 優先度P0。
- 状態: PC-SAVED / NATIVE-STATIC-E8 / V9-PSEUDO-INFERRED / VERIFY / NOT READY。
- 原本出典: `rea_lab/targets/hakushin067_Vahren.exe`、前回20H記録SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`（今回フルハッシュ未再計算）。
- 現行検索: `rea_lab/headless_analysis/search_index/HAKUSHIN067_UNIFIED_V9_20261023.sqlite`、先行20H記録SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`。
- 先行研究 `REA-LOCAL-20261101-19H-P0-FTELL-SEH4-SCOPE-STATIC-01` / `REA-LOCAL-20261101-20H-P0-EH4-DISPATCH-PHASE-STATIC-01` の cleanup 存在・2フェーズは二重計上しない。
## 今回の差分（新規の到達経路クロスウォーク）
- V9 callers の `0x005C3500 __local_unwind4` は4 E8 site：`0x005C35BD`（`0x005C3590` PE EH fragment）、`0x005C35E6`（`0x005C35D6`）、`0x005C3646`（`0x005C363B`）、`0x005D1D33`（`0x005D1CB1 __fsopen`）。
- 原本PEの当該4 E8 + `0x005C356E -> 0x005CC2B5 __NLG_Notify` + `0x005C357B -> 0x005CC2D4` を独立バイト照合した。全6 siteとも opcode/相対先が一致。3byte trampoline `0x005CC2D4: FF D0 C3` も一致。計7/7 PASS。
- `0x005D1CB1 __fsopen` では、Ghidra擬似C上、空文字ファイル名の局所エラー経路に `__local_unwind4(...,-2)` が現れる。**例外のOS配送だけを想定して検証を完了してはいけない**。この具体的条件のASM/CFA・FILE*所有権とcalleeの実引数は未検証。
- `0x005C3590` はV9でPE code fragment、native ABI=UNVERIFIED。`0x005C35D6` もABI未検証。これらを呼出可能な公開DLL関数とは扱わない。
- V9の `__local_unwind4` 擬似Cは scope cursor `[param_2+0xC]` を親indexで先に更新し、filter=0のとき NLG notify(0x101)→間接 cleanup を実行すると示す。cursor更新・notify理由は機械出力であり、今回の7/7バイト監査だけで独立ASM確認したことにはしない。
## 証拠充足・対象外
- 新規独立静的照合: 7/7（6×E8+3-byte trampoline）；全文ソース再抽出・新REA起動・ゲーム起動なし。
- 5種証拠: info=V9、pseudo=V9、assembly=限定6 sites+trampoline、callers=V9索引+限定原本4 E8、callees=V9+限定原本2 E8。正式関数全体の5種証拠完備は0、新規正式VERIFIED0。
- TODO/VERIFY/BLOCKED正式変更0/0/0、原作Golden実測PASS0、strict MATCH0、READY0、完全複製率未測定。研究PC負荷・全作業時間不明。
## KB_CANDIDATE と再開
- 候補: 4 callerサイトと所属関数・7件原本確認の根拠。前回20Hでは `0x005C3646` 経路を詳述済みなので重複計上せず、追加差分は `0x005D1CB1 __fsopen` を含む他3入口の横断対応。
- 出典: `rea_lab/decomp_task/REA_20261101_21H_P0_UNWIND_CALLERS_AUDIT.py` と同ID `*_EVIDENCE.json`。未同期時はGitHub private候補Issueを優先し、共有knowledgeの変更は専任統合担当に委任する。
- 次P0: `0x005D1D33` のエラー経路を元ASM・scope-parentの数値・FILE*状態まで限定追跡、`0x005C3500` のscope cursor更新命令と `__NLG_Notify` side effect。
- 11/1 18Hの部分JSONは未完成・安全拒否のまま維持。禁止VAや別経路取得をしない。

## GitHub REA候補受付（今回ユーザー要望で変更）
- PRIVATE GitHub回収Issue: `https://github.com/ButaMonky/Hakushin067-Research-Knowledge/issues/6`。REA/T015 の17–21H候補と未回収差分を、軽量なVA・CALL site・研究ID・根拠・未検証制限として登録した。これは共有knowledge正式統合やGit commitではない。統合担当が未収録差分をレビューする。
