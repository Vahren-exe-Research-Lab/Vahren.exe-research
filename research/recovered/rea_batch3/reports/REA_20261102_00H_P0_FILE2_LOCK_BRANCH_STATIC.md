# REA 2026-11-02 00H P0｜CRT FILE lockのindex境界とpointer境界
**研究ID** `REA-LOCAL-20261102-00H-P0-CRT-FILE2-LOCK-INDEX-VS-POINTER-STATIC-01` / owner REA/T015。**状態** PC-SAVED（本ファイル保存確認待ち）/ NATIVE-STATIC / VERIFY / NOT READY / GITHUB-INTAKE-PENDING。
## 出典と重複防止
- 原本一致の読取専用PE `rea_lab/targets/hakushin067_Vahren.exe` SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、現行統合V9 `rea_lab/headless_analysis/search_index/HAKUSHIN067_UNIFIED_V9_20261023.sqlite` SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`。両実体のhash一致、SQLite quick_check=ok。V9はPC標準V3を変更せず独立CLIで利用。
- 23H先行 `REA-LOCAL-20261101-23H-P0-GETSTREAM-LOCK-OWNERSHIP-STATIC-01` が `0x005D21D3 -> 0x005BDB12` と `0x005D21EA -> 0x005BDB80` を確認済み。これら2つのE8もCRT関数名も新関数発見としては再計上しない。新しい独立差分は、両calleeの**内部2分岐**と`__fsopen`側の**ポインタ範囲解除規約**のx86根拠。
## 原本機械語による局所静的証拠
1. `0x005BDB12 __lock_file2` は `[EBP+8]` の `_Index` を `0x14`（20）と符号比較し、`0x005BDB1D JGE` で分岐。index<20は `0x005BDB1F ADD EAX,0x10`、`0x005BDB23 -> 0x005C1041` でindex+16番のCRT共通lockを取得し、`0x005BDB2B` で `FILE+0x0C` のflagに `0x8000` をOR。index>=20は `FILE+0x20` を`0x005BDB3C: CALL [0x609098]`へ渡す。IATを原本インポート表で独立照合し`KERNEL32!EnterCriticalSection`と確認。
2. `0x005BDB80 __unlock_file2` はindex<20なら `0x005BDB90`で`FILE+0x0C & 0xFFFF7FFF`、`0x005BDB9B -> 0x005C0F68` でindex+16番の共通unlock。index>=20なら `FILE+0x20` を `0x005BDBA7: CALL [0x609094]`へ渡す。同IATの実インポート名は`KERNEL32!LeaveCriticalSection`。つまり高index経路でのflag操作はこの関数内にない。
3. `0x005BDB44 __unlock_file` は**index引数を取らずFILE pointer値そのもの**を `0x0065AB28 <= FILE <= 0x0065AD88` で比較（`0x005BDB53 JB`、`0x005BDB5A JA`）。範囲内はflag `0x8000` を落とし、`(FILE - 0x0065AB28) >> 5` + 16を共通unlockへ渡す。範囲外は `FILE+0x20` に`LeaveCriticalSection`。両端差は0x260=19×0x20で、静的FILE 20スロット相当の判定である。
4. `__fsopen`側EH補助 `0x005D1D63` は `PUSH [EBP+8] -> 0x005D1D66 CALL 0x005BDB44 -> RET`。自分でEBPを確立せず**親のframeを共有**するため、DLLから通常cdeclとみなして単独で呼ぶのは危険。正常__getstream成功時のlock引渡し（23H）と、この別方式のunlockは、前提としてindexとFILE pointerが同じCRT表上で対応している場合に整合する。
5. **確認限界:** index<0の不正値、FILE pointer/slotの不一致、改変・再入・スレッド競合、OS例外配送、IAT実行成否は未検証。小index判定は符号付きだが、23Hの__getstream通常探索の非負index以外を安全と宣言しない。原作ゲームを実行していない。これはCRTの既知library関数に関する新しい**上流下流のソース対応付け**であり、ゲーム仕様の独立機能が増えたという意味ではない。
## 証拠ファイル・検証結果
- 同担当 `REA_20261102_00H_P0_FILE2_LOCK_BRANCH_AUDIT.py` は独立PE/V9 hashとSQLite、4機械語窓完全decode、25 opcode site、6個のE8、2 IATインポート名の**41/41 PASS、FAIL0**。`0x005BDB12`窓SHA `A59DC4025DEEDF86BBB976B695F883114E6639E14C8FA1A75AAF965721699598`、`0x005BDB80`窓SHA `6C819ED4C1521648BC0A829D0C01FC8C0909F139C046E0FF8754D1B22D801785`。
- `0x005BDB44`窓SHA `5214D8D8289EE4EA73B34C6DF9137401BD45A94C291CD6CA38A645F3FCACCF3F`、`0x005D1D63`窓SHA `4CBF26892B79CD618B4A79E747EDA1AE4CECF2F4536E432C88546DE9E49395B3`。計測実行1.67097秒（監査のみ）。証拠 `REA_20261102_00H_P0_FILE2_LOCK_BRANCH_EVIDENCE.json` SHA256 `D6A5E7B01C4C7A5590530526FEDC4DD3D832FE25305C98CA21CE997F4F55E8FB`。
- 既存V9 info/pseudo/callers/calleesは検索可能、追加assemblyはこの4つの限定窓のみ。正式REAの新規5種完備0、新規VERIFIED0。正式TODO/VERIFY/BLOCKED書換0/0/0、原作Golden実測0、strict MATCH0、READY0、完全複製率未測定。CPU/RAM負荷と作業全体時間は不明。
## KB_CANDIDATE と後続タスク
- 上記研究ID・owner REA/T015、VA `0x005BDB12 / 0x005BDB80 / 0x005BDB44 / 0x005D1D63 / 0x005D2165`、CALL `0x005BDB23 / 0x005BDB9B / 0x005BDB6C / 0x005D1D66 / 0x005D21D3 / 0x005D21EA`、offset `FILE+0x0C/+0x20`、IAT `0x00609094/0x00609098`、出典相対path/PE/V9 SHAと原本窓SHAは上記。STATIC_native; alias/ABI/exceptionはINFERRED/VERIFY。候補先: CRT/IO REF、関連 `REF_AUDIO_VORBIS.md` とresearch/rea索引。
- 過去OFFLINE 03H/04H/05Hのresidue関連Library報告も読み、04Hの03H整数overflow懸念の**訂正関係**、05HのEOF latchを同じ成果と誤計上しないよう区別。03H/04Hの原本局所バイト `0x005D9F64/0x005DA0B2/0x005DFF80` と05H `0x005DFE5C` を現行PC原本で読み戻した。過去の元監査81/100/170はこの回の新規PASSに加算しない。
- GitHub owner intakeへの公開が成功した場合は **PUBLISHED_INTAKE / NOT CURATED**。developのREF/辞書正式採録はcurator専任。18H安全拒否済み部分JSON、禁止VA/旧Waveは一切再試行しない。
- **次カーソル:** 03～05HのOFFLINE成果を原本現行V9・既存curationと比較してPRIVATE intakeへ軽量な訂正リンク付きで保存し、06H以降を継続。新規技術課題は静的FILE20スロット表と`__getstream` indexの不変性、例外unwind中の実ロック状態・呼出元ABI。
- MASTER/QUEUE/PROGRESS、原本・他owner、共有knowledge/develop、既存スケジュールは変更しない。
