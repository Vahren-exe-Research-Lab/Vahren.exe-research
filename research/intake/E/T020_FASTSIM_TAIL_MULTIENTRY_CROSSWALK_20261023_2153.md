# PRIVATE E source archive — existing ID: E-AUDIT-20261023-2153-T020-FASTSIM-TAIL-MULTIENTRY-01

Original owner E PC path: tests/T020_FASTSIM_TAIL_MULTIENTRY_CROSSWALK_20261023_2153.md. Original raw SHA-256 rehashed 2026-11-02: 9259C4FE463574E6B698D232C4E453EF7544CB2E620C5680161B4A2F193C2AC8. This published report intentionally redacts historical safety-refusal details, so it is not byte-identical to the original source. V9 2026-10-23 static multiple-caller mapping is not a live call trace; shared tail does not establish one-run native World commit. The seven negative cases are DESIGNED_NOT_RUN.

Status: PUBLISHED_INTAKE / STATIC + SYNTHETIC + VERIFY / NOT_CURATED / NOT_READY. Any source version/callsite belongs to its 2026-10-23 index epoch, not independently recertified current V9. Past reported tests were NOT rerun. Native original Golden PASS 0, strict MATCH 0, formal READY 0, no new MASTER changes. REA/B owner original findings are read-only references, never republished or reassigned.

---

# E T018/T020｜0x0048EEE0共有後処理の入口・擬似C欠落差分
研究ID: E-AUDIT-20261023-2153-T020-FASTSIM-TAIL-MULTIENTRY-01
日時: 2026-10-23 21:53 JST。担当E、STATIC／VERIFY、NOT READY。原作Gameplay NOT RUN。
対象EXE: ver0.67 / 既存索引 source SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（今回実EXEの再hashなし）。
出典: 統合V9 search_unified_v9_20261023.py function 0x0040E220 / 0x0048EEE0 / 0x0048C880 と callers 0x0048EEE0。
V9 verify=V9_INDEPENDENT_READBACK_PASS、DB SHA256=2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE。元EXE起動・Ghidra再抽出・DB変更なし。
## 新たなクロスウォーク（前回20:52の追補）
V9 PE確認済みE8 CALLは0x0048EEE0へ計4箇所: 0x0040E2D2 (caller 0x0040E220/簡略戦闘)、0x0048D603 (0x0048C880/初期化系候補)、0x004A2D17 と 0x004A2EA1 (0x004A1250/DAT VM系)。
同一calleeを複数の入口から使うため、0x0048EEE0を「簡略戦闘だけの結果コミット」としては扱わない。CALLの存在は実行時到達・全分岐完了の証拠ではない。
0x0040E220 pseudoCでは ret!=0 の後、virtual +0x10→0x00493630→0x0040F000→0x0048ABF0 と進み、iVar1+0x1EF175のbyteが0なら 0x0040E2D2 からcalleeを呼ぶ。
この外側gateと、0x0048EEE0内のparam_1+0x1EEC71を0/1へ更新する枝は異なるfield／異なるポインタ基点。数字が近いというだけで同一状態フラグとみなさない。
0x0048EEE0 pseudoCでは条件に応じ+0x1EEC71を0にする2枝と、0→1にする別枝が候補となる。+0x1EEC71の初期状態、各枝の実到達、戦略画面への反映は未観測。
## 擬似Cの受入上の落とし穴
0x0048EEE0のGhidra pseudoCはlocal_20/local_1cを明確な初期化なしで参照し、0x0048F016のunreachable-block削除警告を出す。ABI・局所変数寿命は未認証。
一方V9のnative E8索引には 0x0048F01C→0x00415A60 があり、関数擬似C本文にはそのCALLが表現されていない。存在自体はSTATIC、当該枝が実行可能かはVERIFY。
したがって「擬似CにないCALLは存在しない」「12個のnative E8 CALLが毎回すべて実行される」をともに禁止する。
## T020 独立負例fixture（DESIGNED / NOT RUN）
tests/T020_FASTSIM_TAIL_MULTIENTRY_NEGATIVES_20261023_2153.json に保存する。entry別同一性、gate時相、疑似C・nativeの差、G3/G4自動昇格を判定。
今回fixtureはJSON形状・ID検査のみ。旧new比較runner、原作DYNAMIC/Golden、G3/G4戦略反映実験はNOT RUN。
## 所有権・継続状態
T018 C-NB02旧合法UI G0、同一戦闘SAVE+入力G1、実MAP/3side/ordered Unit・Troop G2、G3終了結果、G4世界差分はいずれも未充足。E DYNAMIC OBSERVED0、actual Golden PASS0、strict MATCH0。
T019: GameClear DAT13/TXT2検索範囲差だけRESOLVED、script2優先・flag用途・TXT実ロード・gwrite復帰VERIFY。新規原作BUG確定0。
MASTER最終確認checkpoint196/READY596(A115/B229/C136/D116)、34Task DONE9/IN_PROGRESS21/VERIFY4は旧値。今回は全件再集計せず新規正式READY0。OFFLINE-UNSYNCED暫定26研究は未同期・未照合。
- Historic refused targets and operations remain BLOCKED and are not disclosed/reproduced in this sanitized E report.
次: 4 callerのうち合法C-NB02 G0/G1/G2に結び付く実観測だけを受入。後段+0x1EF175/+0x1EEC71は同runで値・時刻・source hashを分離しG3/G4を確認。
## 保存・検証結果（同run）
Local Compactで本報告と7負例JSONを新規保存し双方全文readback済み。JSON parse/ID一意7/7・callee直接CALL site件数4・Golden未実行フラグ整合PASS。fixture自体の実行はNOT RUN。
初回read-only Python QAはWindows日本語パスの文字化けと末尾バックスラッシュでSyntaxError（OTHER／未書込）になった。拒否ではなく、同じLocalでUnicode escapeパスへ訂正して上記QA成功。未保存成果・安全拒否・被変更原本なし。
