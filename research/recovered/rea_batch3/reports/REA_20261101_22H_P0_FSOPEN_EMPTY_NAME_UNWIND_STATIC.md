# 迫真戦記 REA 2026-11-01 22H P0 | __fsopen 空filenameとEH4後始末（原本x86）
**研究ID** `REA-LOCAL-20261101-22H-P0-FSOPEN-EMPTY-NAME-UNWIND-STATIC-01` / Owner `REA/T015`。
**状態** `PC-SAVED / NATIVE-STATIC / VERIFY / NOT READY / GITHUB-INTAKE-PENDING`。元EXE実行なし。

## 先行・出典と重複抑制
- 先行 `REA-LOCAL-20261101-20H-P0-EH4-DISPATCH-PHASE-STATIC-01` は一般のsearch/unwind分岐、`REA-LOCAL-20261101-21H-P0-UNWIND-FOUR-CALLERS-NLG-STATIC-01` は __local_unwind4 の4つのE8 CALL元を調査済み。本件は既知CALL `0x005D1D33` の**実引数・条件と __fsopen 自身のscope cleanup登録**を新規照合し、CALL元自体を新発見として二重計上しない。
- 原本一致コピー（読取専用）`rea_lab/targets/hakushin067_Vahren.exe` SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` を本回再計算して一致。
- 統合V9（読取専用）`rea_lab/headless_analysis/search_index/HAKUSHIN067_UNIFIED_V9_20261023.sqlite` SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`、SQLite quick_check=ok。古い `search_index/README.md` / `BUILD_MANIFEST.json` は既知のENOENTであり新規Ghidraを実行していない。

## 新規の限定STATIC
1. `__fsopen` 関数入口 `0x005D1CB1..0x005D1D62`（178B）は `0x005D1CB3` でSEH4 table `0x00641798` を登録し、`0x005D1CFD` で `0x005D2165 __getstream` を呼ぶ。非NULL戻りの後、`0x005D1D19 cmp byte [edi],0` / `0x005D1D1B jne 0x005D1D3D` が filename先頭が0かを判定する。
2. **空filename経路**：`0x005D1D1D -> __errno`、`0x005D1D22` でerrno=22、`0x005D1D28 push -2`、`0x005D1D2A lea eax,[ebp-0x10]`、`0x005D1D2E push 0x0065A220`、`0x005D1D33 -> 0x005C3500 __local_unwind4`、`0x005D1D38 add esp,0xC`、`0x005D1D3B -> 0x005D1CE0` の局所帰還。正常な関数帰還は `__SEH_epilog4` 経由となるが、unwind handler実行時の外部例外影響は未計測。
3. スコープテーブル `0x00641798..0x006417B3`（28B）の7 DWORDは `[-2,0,-44,0, -2,0,0x005D1D63]`。MSVC EH4解釈では最後のscope entryのfilter=0、cleanup pointer=`0x005D1D63`。同10B helperは原本 `0x005D1D63 push [ebp+8]` / `0x005D1D66 call 0x005BDB44 __unlock_file` / `ret`。親のEBPを利用するため独立ABIではない。
4. **通常openfile経路**では `0x005D1D43 -> 0x005D1ECE` の結果保持後、`0x005D1D4E` でscope=-2、`0x005D1D55` で同じ `0x005D1D63` を直接CALL。空filenameのunwind経路と通常帰還が**同じ後始末helperを参照**することが独立した静的追加関係。
5. `0x005C355D` のscope parent先行更新・`0x005C357B` のtrampoline呼出は先行20Hと整合。ただし __local_unwind4 から対象helperへの**実行時到達性・ロック状態・解放成功**は原作動的観測ではない。`__getstream` 自身のlock取得経路とFILE*所有権は次回VERIFY。

## 静的監査・5種証拠・Golden
- 新規audit `rea_lab/decomp_task/REA_20261101_22H_P0_FSOPEN_SCOPE_AUDIT.py` と機械証拠 `REA_20261101_22H_P0_FSOPEN_SCOPE_EVIDENCE.json`。元PE/V9全SHA、SQLite quick_check、x86連続命令（178B/144B/10B）、scope28B、分岐・引数・CALL先・trampolineを **29/29 PASS**。再実行は既保存JSONと非時間依存のデータ一致を検証。bounded windows SHAはEVIDENCE参照。
- info=V9、pseudo=V9、assembly=今回限定原本native、callers=先行V9+本E8、callees=今回限定E8。**関数別公式5種完備0、新規VERIFIED0、正式TODO/VERIFY/BLOCKED差分0/0/0**。旧正式VERIFIED64件は再計上せず。
- 原作ゲームGolden実測PASS0、strict MATCH0、READY0。完全複製率未測定。監査実行約0.89秒、PC CPU・RAM負荷と全作業時間不明。

## KB_CANDIDATE・未解決・GitHub引継ぎ
- 候補: `__fsopen 0x005D1CB1`、`__getstream 0x005D2165`、empty filename branch `0x005D1D19..0x005D1D3B`、scope `0x00641798`、unwind `0x005C3500`、同EBP unlock helper `0x005D1D63`、call sites `0x005D1D33/0x005D1D55`、offset `[EBP-0x10]`・scope `[EBP-4]`、state STATIC_NATIVE / INFERRED_RUNTIME / VERIFY / NOT READY。
- 候補統合先 `REF_AUDIO_VORBIS.md` または CRT/EH専用REF。GitHub上で既存20H/21Hとの相互参照を持たせ、新規関数発見やランタイムクラッシュ扱いをしない。出典は本MD＋同ID証拠JSONと監査py。`__getstream`本体のロック取得/戻り状態、異常filename時にunwindで解放が実行される全分岐、DLL ABI、原作Goldenは未確認。
- 次回P0: `0x005D2165 __getstream` のFILE*ロック所有権・解放条件を限定原本ASMで検証し、`0x005D1D63` の正常・unwind呼出のframe整合を追加調査。18H安全拒否の不完全JSON、禁止VA/拒否済みREAエクスポートは引続き触れない。元原本/MASTER/QUEUE/PROGRESS/共有knowledge/develop・他ownerの作業ツリーは変更しない。
