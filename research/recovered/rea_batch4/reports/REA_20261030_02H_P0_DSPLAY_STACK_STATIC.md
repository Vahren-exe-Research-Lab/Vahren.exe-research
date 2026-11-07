# 迫真戦記 REA｜2026-10-30 02H：DirectSound Play引数の分岐越しPUSH再利用
研究ID：`REA-LOCAL-20261030-02H-P0-DSBUFFER-LOOPPLAY-DUALPUSH-ABI-STATIC-01`
状態：**PC-SAVED / STATIC / VERIFY / NOT READY**。正式VERIFIED新規0、原作ゲームGolden実測0。
## 旧成果・索引の照合
MASTER、ANALYSIS_LANES_PROTOCOL、REA README/QUEUE/PROGRESS、旧runと最新sync `progress_sync_20261011T153958076Z.json`、10/25 19H–21H、10/30 00H/01Hの報告・保存証拠・readbackを先読した。旧syncはWave1–5 **64/64**、QUEUE/PROGRESSの15/16はEPERM由来の古い表示であり今回改変せず。01H監査47/47、readback12/12を確認。オフライン未同期資料は未統合。
隔離専用EXE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、統合V9 SQLite SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`、SQLite quick_check=ok。旧search.sqlite/READMEの不在は10/29整理済みにつき、V9別名CLI/DBを採用。単一Ghidraプロジェクトに完全統合されたと扱わない。
## P0今回の独立静的発見：分岐の両側で共有する0x004BEAFE PUSH 1
`0x004BEAFA CMP BYTE [ESI+0x44],0` → `0x004BEAFE PUSH 1` → `0x004BEB00 JE 0x004BEB86`。PUSHはEFLAGSを変えないためCMP結果によるJEは保持される。
**失敗側**：JEが成立すると`0x004BEB86 MOV ESI,EBP` → `0x004BEB88 CALL 0x004BF2B0`。このcalleeの`0x004BF331 RET 4`と併せ、直前に積んだ1はcleanupの引数として消費される構造。
**成功側**：JE不成立なら`0x004BEB15 MOV EAX,[ESI+8]`、`0x004BEB18 MOV ECX,[EAX]`、`0x004BEB1A MOV EDX,[ECX+0x30]`、`0x004BEB1D PUSH 0`、`0x004BEB1F PUSH 0`、`0x004BEB21 PUSH EAX`、`0x004BEB22 CALL EDX`。先行PUSH 1を含め、this/0/0/1の4 DWORDを積んでいる。DirectSoundBuffer系COM vtableの+0x30=Play規約と対応する場合、これは **Play(0,0,DSBPLAY_LOOPING=1)** の呼出しとなる。
裏付け：`0x004BF314 MOV EDX,[ECX+0x48]` → `0x004BF317 PUSH EAX` → `0x004BF318 CALL EDX`は同系統インターフェースのStop()（+0x48）と一致。Play/Stopメソッド署名・戻り値はMicrosoft Learn `IDirectSoundBuffer::Play` (2016-06-02更新) および `IDirectSoundBuffer::Stop`を参照。これはvptr型の静的整合であり、実行時vptrやHRESULTの実値を観測したものではない。
**重要な意味**：DSBPLAY_LOOPINGはDirectSoundの**再生用リングバッファを循環再生**させる指定であり、ユーザーが選んだ楽曲自体のリピート設定を証明しない。また`0x004BEB22 CALL EDX`の直後`0x004BEB24 MOV [ESI+0x50],1`なのでPlay失敗HRESULTを検査する前に状態を1にする。worker失敗時のready偽陽性と繋がり得るが、実機音声障害は未証明。
## 監査・運用・次回
`REA_20261030_02H_P0_DSPLAY_STACK_AUDIT.py`は既存DB索引＋同一SHA隔離EXEのCapstone局所ASMをread-only照合し **37/37 PASS・1.8572秒**。出力 `REA_20261030_02H_P0_DSPLAY_STACK_EVIDENCE.json`。REA5方法：info=V9 INDEX、pseudo=V9 INDEX、assembly=隔離PE局所Capstone、callers=V9 INDEX、callees=V9 INDEX。関数別正式5方法の新規完備0、正式VERIFIED+0、TODO/VERIFY/BLOCKEDの正式書込差分0/0/0。原作Golden PASS0、完全複製率未測定。
PCオンライン、active.lock無し、空き物理RAM確認時約10.66GiB、Java/Ghidraなし。CPU負荷・研究全体所要時間は不明。新REA/Ghidra/原作実行なし。安全拒否済VA/Wave6/exportの再試行なし。新規作成はREA専用02H報告/監査/証拠/readbackのみ。他owner・MASTER・QUEUE/PROGRESS・既存runs・原本・Git・スケジュールは変更なし。
Golden条件（DESIGNED/NOT RUN）：正常Play HRESULT=0と失敗HRESULT!=0を分け、+0x50・+0x44・+0x48、worker実在、COM vptr実値、バッファ循環と曲リピート状態を別々に記録。次回は`0x00502220`のDirectSoundバッファ生成・vptr所有、`0x00502330`のLock/Unlock（+0x2C/+0x4C）と`0x004BEB22`Playおよび`0x004BF318`Stopの同一COMオブジェクト到達を検証する。
