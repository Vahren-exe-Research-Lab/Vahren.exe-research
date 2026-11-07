# REA 2026-11-02 01H｜P0原本静的根拠・旧研究3件回収・GitHub readback
**新研究ID:** `REA-LOCAL-20261102-01H-P0-OGG-STATE3-DUAL-ENTRY-ESI-ABI-STATIC-01` / owner REA/T015。
**状態:** PC-SAVED / PUBLISHED_INTAKE / NATIVE-STATIC / VERIFY / NOT CURATED / NOT READY。対象ゲームの実行・REA再問い合わせ・Ghidra全関数再解析は行っていない。
## 検証済み新規意味差分
- 原本x86の `0x005D0B8A E8E1EDFFFF → 0x005CF970` は upstream `0x005D04E0` 非負成功後の初期化用**早期**CALL。以前08Hの `0x005D0D67 E804ECFFFF` は既知の後段cached serial再開CALLであり二重計上しない。
- `0x005D0B6D MOV ESI,[EBP+8]` と `0x005CF970 MOV EAX,[ESI+0x58]` によりcalleeのESI外部依存を元ASMで限定確認。状態3時のみ `0x005CF9A1 → 0x005D5BD0`、正常時 `0x005CF9CC` で状態4に遷移。完全ABI・実ゲーム到達性・異常経路はVERIFY。
- PE window SHA `0x005D0B60..0x005D0B98`：`44FE4A5DAFBF23EB3B79E2B19B2634FB45B4ABFDA410FD1FDBA644746B9DF5AF`。 `0x005CF970..0x005CF9D7`：`E9F9D9A7B9007542C5C127B9A50CDC2CF176034912B5D2F67AABFBC058C200F3`。Capstone5.0.7、統合V9 direct E8 callers を独立照合。
- 原本PE SHA `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、V9 SQLite SHA `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`（ともに本時刻PC現物Get-FileHash再計算一致）。
- PC新報告 `REA_20261102_01H_P0_OGG_STATE3_DUAL_ENTRY_STATIC.md` SHA `A6217D547C1DA7EBD899A97E30B1F7BAF1E81595962AEDEBF8825F235F07D78B`、PC新EVIDENCE JSON `REA_20261102_01H_P0_OGG_STATE3_DUAL_ENTRY_EVIDENCE.json` SHA `758EA165AC324844A743FFA5550E2DBCDC61B96C850130153312CB1E1CDAA35B`。独立readback/JSON parse PASS。
## 旧研究成果の回収・private GitHub入庫
- Library 11/1 06H mode calloc OOM、07H inner-zeroing/cleanup、08H cached stream state3 の**3旧研究ID**を回収。各原Library REPORT/EVIDENCE計6実体を取得・SHA再計算。旧STATIC監査186/117/125 PASSは今回再実行/新規計上していない。Library本文をPC正本へ同期済みとは扱わない。
- PRIVATE GitHub `ButaMonky/Hakushin067-Research-Knowledge`、固有owner branch `intake/rea-20261102-00h-file-lock-residue-r1`、同一既存Draft PR https://github.com/ButaMonky/Hakushin067-Research-Knowledge/pull/16（open/未merge）。
- 新規GitHub入庫 **4研究ID（新解析1、旧回収3）**。`research/intake/REA/REA_20261101_06H_08H_MODE_CACHE_RECOVERY_STATIC.md` commit `79dbd5982447b51186362a4dc96677b983be92cf`、`REA_20261102_01H_DUAL_ENTRY_ESI_ABI_STATIC.md` commit `219ff5e7e6754e8d58c4d08d3ad3c58a4ded7378`、INDEX更新後最終commit `9ae53c82eac731b04b1c6594af3b58b038d6a7ed`。
- GitHub API readback：新2本文SHA `7d3c2bfc354e92226df2ba7ef53e04b604df6449` / `9d2670c530120ffc567454037456de1c09e6f522`、INDEX SHA `8d46df5da5a071b9ea1001d5a540fae52e371249`、研究索引17ID（以前13+今回4）、新4研究IDの記載全確認。PR本文も現行4件/残8IDへ更新成功。共有develop/REF/symbols/structsは不変更。
- 11/1 03–16Hの元オフライン14IDのうち03–08H **6ID入庫済み**、09–16H **8ID未入庫**。他年代・全REA総数はこの部分カウントの分母に含まれない。11/1 18H安全拒否済み部分EVIDENCEはSAFETY-HOLDのまま不処理。
## 再開条件と状態
- 本時刻の新正式REA info/pseudo/assembly/callers/callees完備 **0**、新VERIFIED **0**、公式TODO/VERIFY/BLOCKED差分 **0/0/0**。過去正式静的64件は履歴であり加算しない。
- 原作Golden実測PASS **0**、strict MATCH **0**、READY **0**、完全複製率未測定。PC負荷/全工程時間不明。新Ghidra/REA実行なし。
- 次カーソル **09H** `REA-OFFLINE-20261101-09H-P0-OGG-CACHED-HEADER-SERIAL-INDEX-PRODUCER-BRIDGE-STATIC-01`、`0x005D1490` producer／`outer+0x40/+0x48` serial record、index/count生存条件の追加照合。禁止VA・既拒否Wave6/18H追記回避を厳守。
- 原本 EXE/DAT/MAP/SAVE/ZIP、他owner/MASTER/QUEUE/PROGRESS、元ユーザーGit作業ツリー、共有develop、既存スケジュールは不変更。
