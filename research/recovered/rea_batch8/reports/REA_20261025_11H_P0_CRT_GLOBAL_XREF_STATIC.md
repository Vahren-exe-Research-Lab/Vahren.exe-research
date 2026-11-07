# 迫真戦記 ver0.67｜REA 2026-10-25 11時台 P0 CRT new-mode 全参照・handler setter・calloc/realloc 異常系
研究ID：REA-LOCAL-20261025-1137-P0-CRT-GLOBAL-XREF-STATIC-01
状態：PC-SAVED（保存後にreadback別途確認）/ STATIC / VERIFY / NOT READY。新規正式VERIFIED=0、原作Golden実測=0。
原作EXE SHA256：E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
初期検索DB SHA256：0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF
統合V9 DB SHA256：2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE

## 新しい独立照合（08～10時台成果とは二重計上しない）
- `DAT_0068e8c0`（new-mode）への検索DB data_refs は3件すべてREAD：`0x005B9C1C`（_malloc）、`0x005C3089`（__calloc_impl）、`0x005C3109`（_realloc）。独立PEの `.text` 即値出現も正確に3箇所（埋込DWORD開始VA `0x005B9C1E/0x005C308B/0x005C310B`）。直接WRITE=0。
- `DAT_0068dfe8`（encoded handler）のdata_refsはWRITE `0x005BBA70` とREAD `0x005BBA7C` の2件。`.text` 埋込DWORD出現も同じ2件（`0x005BBA71/0x005BBA7E`）。
- 既存pointer_refs 4,358件の索引に上記両グローバルをtargetとする静的データポインタ参照は0件。両グローバルともPE .data raw終端の後・virtual内でロード時ゼロ初期化対象。
- `0x005BBA68`（encoded handler保存）のGhidra直接callerは唯一 `0x005BB3E1`、CALL site=`0x005BB3EC`。直接グローバルWRITEと単一callerを合わせても、アドレスを算出した間接WRITE、間接CALL、外部変更、フック等が不存在とまでは証明できない。
- 新知見：new-modeを読む3関数は失敗時契約が異なる。Ghidra疑似Cと対象機械語の分岐を照合：`__calloc_impl 0x005C303C` は乗算サイズ溢れを `0x005C304F`比較→`0x005C3054`の`__errno`設定→NULL返却へ進み、通常HeapAlloc失敗時はnew-mode=0なら`0x005C3090`分岐でhandlerを呼ばずNULL（任意errno出力ポインタに12）を返す。`_realloc 0x005C30BE` は引数ptr=NULL時 `0x005C30CC`で_mallocへ委譲、size=0時 `0x005C30DF`で_freeを呼びNULL。HeapReAlloc失敗時new-mode=0なら`0x005C3109`比較から0x005C3151側のGetLastError→errno変換へ進む。巨大サイズとhandler有効時は独立分岐。Spotの外側 `0x005B6C2B` は失敗時bad_alloc送出を持ち、CRTのNULL返却と混同不可。
- `_malloc/__calloc_impl/_realloc`のnew-mode参照は初期DBと原作機械語で一致。`0x005C3093/0x005C3112/0x005C3122`の直接CALL先は `0x005BBA77`。特殊サイズ・handler登録時の全動的経路はVERIFY。

## 出典、検証、限界
- 出典：read-only検索CLI `function/callers/related`、初期SQLite `functions/calls/data_refs/pointer_refs`、原作同SHA研究用PEのCapstone機械語、旧rea_lab成果・進捗同期ログ。
- 独立Python stdin監査：**36/36 PASS**（0.666秒）。EXE/DB0/V9 SHA、旧同期64、SQLite quick_check、PE base/.dataゼロ埋め境界、5 site ASM・DB xrefs、埋込即値全走査、pointer_refs、関数疑似C、CALLを照合。初回20/25は比較文字列のゼロ埋め方の誤りで、修正後36/36 PASS。試験件数を関数VERIFIEDへ換算しない。
- 形式5種類：info=既存DB索引、pseudo=既存機械出力、assembly=今回の関連命令のみ、callers=既存索引、callees=既存索引。新規完備関数0、正式VERIFIED増0、正式TODO/VERIFY/BLOCKED書込差分0/0/0。既存Wave1～5 VERIFIED64は過去sync値の維持、旧QUEUE/PROGRESSはEPERMで古い。
- 未解決：間接WRITE・外部モジュールによる書換えとsetterへの間接到達の不存在は未証明。すべての動的実行時値、異常系Golden、完全複製率は未実測。Golden条件はDESIGNED/NOT RUN：malloc/calloc/reallocのnew-mode0、handler有効・NULL・例外・サイズ溢れをそれぞれ分ける。
- 開始preflight：研究PCオンライン、active.lockなし、競合するJava/Ghidra/REA名プロセスなし、空きRAM約13.83GiB。CPU負荷・研究全体の経過時間は不明。新規Ghidra/REA/原作ゲーム実行0。
- 安全：09時台に拒否された `REA_20261025_09H_P0_MALLOC_INNER_OUTER_AUDIT.py` は未完成のまま変更せず。安全拒否操作の別経路迂回なし。原本/MASTER/QUEUE/PROGRESS/既存runs/A～E/Git/Work/スケジュール変更なし。
- 次P0：`0x005C30BE`巨大サイズ分岐の一次機械語とerrno優先順位、`0x005BBA68`の関数アドレス間接参照、CRT handler/戻り値契約を追加検証。