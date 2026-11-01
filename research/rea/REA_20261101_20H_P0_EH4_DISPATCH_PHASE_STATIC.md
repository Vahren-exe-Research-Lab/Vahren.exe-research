# REA 2026-11-01 20H P0｜ftell SEH4 の検索フェーズと unwind cleanup の区別
- 研究ID: `REA-LOCAL-20261101-20H-P0-EH4-DISPATCH-PHASE-STATIC-01`
- owner/task: REA / P0-T015 (CRT FILE* tell callback); 新規差分=exception search と unwind の分岐・cleanup発火経路。旧19Hのscope table取得は二重計上しない。
- 状態: PC-SAVED / NATIVE-STATIC / INFERRED-RUNTIME / VERIFY / NOT READY。
- 先行: `REA-LOCAL-20261101-17H-P0-CRT-FTELL-FRAME-CROSSWALK-STATIC-01`, `REA-LOCAL-20261101-19H-P0-FTELL-SEH4-SCOPE-STATIC-01`。18H部分JSONは安全拒否・未完成のまま放置せず別件として保持（操作を再試行しない）。
- 原本一致専用コピー `rea_lab/targets/hakushin067_Vahren.exe` SHA256=`E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
- 現行V9索引 `rea_lab/headless_analysis/search_index/HAKUSHIN067_UNIFIED_V9_20261023.sqlite` SHA256=`2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`、read-only SQLite quick_check=ok。
## 差分1：`0x005BB6E0 __except_handler4` の2フェーズ分岐（original x86）
- `0x005BB72C test byte [eax+4],66h`; `0x005BB730 jne 005BB84F`。exception flagsの0x66ビットが無い検索フェーズと、あるunwind側を区別。**Ghidra擬似CはCRTコンパイラ補助コードなので正式ABIとはしない。**
- 検索側 `0x005BB750` でscope recordを参照。`0x005BB763 test ecx,ecx`（record filter ptr）→`0x005BB765 je 005BB77B` はfilter=0のrecordでfilter-callを飛ばす。親レベルが-2になると検索ループ終了。
- 19Hで確定した `0x00641260` scope entryは parent=-2 / filter=0 / cleanup target=`0x005B79D7`。**このscopeは検索フェーズで例外を捕捉するfilterではなく、unwind cleanup候補。**
- 索引の`callers 0x005BB6E0`は直接E8件数0。OS経由の例外ディスパッチは間接登録のため、0件は「実行されない」ことを意味しない。
## 差分2：unwind側の局所cleanup駆動（original x86）
- unwind側 `0x005BB84F` がtarget level=-2を設定。 `0x005BB854` は現在のscope level=-2なら処理を飛ばし、それ以外は `0x005BB865 E8 -> 0x005C363B (_EH4_LocalUnwind)`。
- helper `0x005C363B` は `0x005C3646 E8 -> 0x005C3500 (__local_unwind4)`。後者はscope cursorを辿って parent値を更新する。
- `0x005C3560 cmp [ebx+4],0` でfilterがゼロのレコードをcleanup対象と扱い、`0x005C3578`でhandler pointerをEAXへ読出し、`0x005C357B E8 -> 0x005CC2D4`。native `0x005CC2D4` は `FF D0 C3`（CALL EAX; RET）であり、間接実行先はscope recordの`0x005B79D7`候補。
## 原作ftellとの接続と実機限界
- `0x005B797C` は `0x005B7983 -> __SEH_prolog4` と `0x00641260` を登録。正常系は `0x005B79B2` でscope=0、`0x005B79C2`で-2へ戻した後、`0x005B79C9`から `0x005B79D7` を直接呼んでunlockする（先行19Hと同一根拠）。
- **本回の新しい解釈**: scopeがactive=0の間にOS経由で当該EH4ハンドラのunwind分岐へ到達するなら、同じunlock helperを間接呼出する静的経路が存在する。単に「例外発生＝必ず解放」ではない。実例外配送・フレーム正当性・ロック取得前/解放中の例外・二重解放は未実測。
- 先行17H/19Hで共有EBP依存の `0x005B79D7` は通常の独立API/Hook ABIではないと判定済み。本回も勝手なABI確定なし。
## 根拠・独立監査
- 同owner新規read-only監査 `REA_20261101_20H_P0_EH4_PHASE_AUDIT.py` は専用PE全文SHAとV9 SHA/SQLite quick_check、4 native windowの完全命令復号、scope DWORD、例外flags分岐、6個のE8元命令/行先、間接cleanup trampolineの3 bytesを個別照合。
- 32/32 PASS、監査実行約1.09秒。原本限定窓SHA256: handler(399B)=`29B4D3A8A472239624405BF8E3123CD24395474383E8CC9EA5CBDFAECA6CA6F7`, local_unwind(144B)=`679102829B3D04DE3B11B604119C1B891FDD9CDA88B7C60E452D8F205D2DFA15`。
- 5証拠: info=V9索引、pseudo=V9機械擬似C、assembly=限定PE直接ASM照合、callers=V9直接E8 0件（間接SEH未捕捉）、callees=V9とnative E8 6件の部分照合。**REA公式5種証拠完備0／新規正式VERIFIED0**。
- 正式TODO/VERIFY/BLOCKED更新=0/0/0、原作Golden実測PASS=0、strict MATCH=0、READY=0、完全複製率未測定。PC CPU/RAM負荷と全作業時間は未測定。REA/Ghidra新規起動・ゲーム実行なし。
## KB_CANDIDATE / 再開位置
- VA `0x005BB6E0`, `0x005C363B`, `0x005C3500`, `0x005CC2D4`; scope`0x00641260`; cleanup`0x005B79D7`。owner=REA/T015、source=本report/同ID evidence/audit、STATIC_NATIVE、実機EH=VERIFY/NOT READY。
- 先行19Hに「filter=0はexception searchでfilter呼出されず、unwindでcleanup対象となる条件付き静的経路」として補足する候補。現行V9で関数・スコープ自体が既知なので新発見として重複登録しない。
- 次P0: `0x005C3500`のscope cursorと`0x005CC2D4`の間接CALLがstack/EBPを維持する条件、`0x005BB680`登録フレーム整合。原作Goldenは別に安全承認条件を設計。
- PC正本MASTER/QUEUE/PROGRESS、既存runs、他owner、共有knowledge、Git、生成DB、原本ZIP/EXE/SAVE、スケジュール不変更。GitHubへは統合担当が候補を取り込む。
