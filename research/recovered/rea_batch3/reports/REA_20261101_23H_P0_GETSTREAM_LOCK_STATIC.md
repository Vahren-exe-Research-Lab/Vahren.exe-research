# 迫真戦記 REA 2026-11-01 23H P0｜__getstream 二層ロックとFILE*所有権（原本x86）
**研究ID** `REA-LOCAL-20261101-23H-P0-GETSTREAM-LOCK-OWNERSHIP-STATIC-01` / REA/T015。
**状態** PC-SAVED / NATIVE-STATIC / VERIFY / NOT READY / GITHUB-INTAKE-PENDING。原作ゲームは実行していない。

## 先行・基盤と非重複
- 22H `REA-LOCAL-20261101-22H-P0-FSOPEN-EMPTY-NAME-UNWIND-STATIC-01` は `0x005D1CFD -> 0x005D2165` 呼出と後続 __fsopen cleanup `0x005D1D63` を確定済み。本報告は **callee内部のグローバルlockとFILE*単位lockの保持/返却条件**のみ新規照合。E8 CALLサイトは再計上しない。
- 認可済み読取専用PEコピー `rea_lab/targets/hakushin067_Vahren.exe` SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` を今回再計算一致。
- 読取専用V9 `rea_lab/headless_analysis/search_index/HAKUSHIN067_UNIFIED_V9_20261023.sqlite` SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`、SQLite quick_check=ok。旧 `search_index/README.md` / `BUILD_MANIFEST.json` は存在せず、V9正規入口を使用。

## 原本x86による新規の限定静的関係
1. `0x005D2165..0x005D228B` 全295BをCapstoneで隙間なくdecode。入口 `0x005D2178 push 1` → `0x005D217A call 0x005C1041` でグローバルCRT stream tableロック候補を取得。`0x005D227F call 0x005D228F` は全ての明示return直前にあり、9B helper `0x005D228F push 1` → `0x005D2291 call 0x005C0F68` → RETで対応するglobal unlockを行う（ロック関数名はV9シンボル解釈）。
2. 既存stream候補は `0x005D219C` でポインタ有無を判定、`0x005D21A5/0x005D21A9` でflags `0x83/0x8000` を除外。必要なら `0x005D21BC -> 0x005C0F7F` のlock初期化条件を経て、`0x005D21D3 -> 0x005BDB12 __lock_file2` を呼び、`0x005D21E2` で再びflags `0x83` を検査。使用中なら `0x005D21EA -> 0x005BDB80 __unlock_file2` の後に次slotへ進む。未使用のままならEDIにFILE*を保持し、**FILE*ロックを明示解除せず**グローバルunlock後に返す。
3. 空slotでは `0x005D21FB` の38hバイトmalloc（`0x005D21FD -> 0x005BAFAE`）の戻り値をグローバルtableに設定し、NULLなら戻り値NULL。非NULLの場合、`0x005D2221 call [0x006090C8]` のcritical-section初期化候補を確認。戻り値0なら `0x005D2233` free、`0x005D223E` slot pointerをNULLに戻してreturn NULL。成功なら `0x005D224A call [0x00609098]` のEnterCriticalSection候補が先行し、`0x005D225B` でFILE flag=0を設定。これらのAPI名はV9疑似Cのラベルであり**IAT個別の独立名称確証ではない**。
4. 非NULL returnの準備は `0x005D2262` flag mask `0x8000`、`0x005D2269/6C/6F/71` のFILEメタdata初期化、`0x005D2274` `_file=-1`、`0x005D2278` scope=-2、global unlock、`0x005D2284 mov eax,edi` → SEH epilog/RET。**通常戻り成功時には個別FILE lockが維持される形**で、caller `__fsopen` の `0x005D1D55 -> 0x005D1D63` cleanup（`__unlock_file`）と整合する。
5. `__getstream` 単体では **失敗時に全slot走査を続けるとは限らない**：`0x005D21C4` lock準備失敗・`0x005D220E` malloc NULL・`0x005D2241` critical-section初期化失敗が直接共通return block `0x005D225E` へ分岐する。特に予約済みstream slotが他に空いていても、この失敗後は局所再探索しない。実機での失敗発生や他スレッド下の競合は未観測。

## 独立証拠・正式判定
- `REA_20261101_23H_P0_GETSTREAM_LOCK_AUDIT.py` がPE/V9全SHA2、SQLite quick_check・PE32・全命令境界3、native opcode35、E8解決9の**49/49 PASS、FAIL0**。証拠 `REA_20261101_23H_P0_GETSTREAM_LOCK_EVIDENCE.json`、`0x5D2165`窓SHA256 `973BE2F2ADBB309B94ECB05282358E56E05445532EF36EFBDCD2EDF9632F2B46`、`0x5D228F`窓SHA `07DC33ADD7C561A7C3CF4B869E86CC7FC74442EF106CEE681CD4BA8A1D4141AC`。監査実行約0.83秒。
- info=V9、pseudo=V9、assembly=原本限定295+9B、callers=V9(`__fsopen`から1直接E8)、callees=原本E89件。**正式5種証拠の新規完備0・新規VERIFIED0**、既存64は旧sync履歴であり加算しない。正式TODO/VERIFY/BLOCKED差分0/0/0、原作Golden実測PASS0、strict MATCH0、READY0、完全複製率未測定。CPU負荷・作業全体時間は不明。

## KB_CANDIDATE・次回
- 研究ID上記、`0x005D2165` body `[0x005D2165,0x005D228B]`、helper `0x005D228F`、FILEロック `0x005D21D3/0x005D21EA`、global lock/unlock `0x005D217A/0x005D2291`、追加CALL site `0x005D2221/0x005D224A`（IAT indirect, API名称VERIFY）。key fields `stream_table 0x00B13A00` / `count 0x00B14A20` / `FILE+0x0C,+0x10,+0x1C,+0x20`。登録先 private KB intake/REA → curator REF CRT/IO等。
- 出典相対path 本MD・同名EVIDENCE.json/AUDIT.py、PE/V9 SHA上記。STATIC_NATIVE、IAT名称/通常のreturn資源所有は条件付きINFERRED、異常ケース/OS例外ロック状態/DLL ABIはVERIFY、DYNAMIC未実測。先行22Hと20H/21H、17H/19HのCRT調査を横断リンクし、23Hは新規**個別FILE lock取得の経路**のみ独立差分。
- 次回 P0：`0x005BDB12 __lock_file2` と `0x005BDB80 __unlock_file2` のlock番号分岐を原本x86で確認し、`0x005D1D63`の親EBPと `__getstream` 戻り保持を接続。過去未収録01H/02H residue3研究IDもprivate GitHubに非重複で回収。
- 18Hの安全拒否済み部分JSON・禁止VA/旧Wave6は変更・再試行しない。MASTER/QUEUE/PROGRESS、原本、他owner、共有KB/develop、スケジュールは変更しない。
