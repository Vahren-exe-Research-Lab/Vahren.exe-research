# 迫真戦記 ver0.67｜REA 2026-10-27 22時台 P0・debug_paper の C++例外処理境界
研究ID：`REA-LOCAL-20261027-22H-P0-DEBUGPAPER-EH-UNWIND-MAP-STATIC-01`。
状態：**PC-SAVED / STATIC / VERIFY / NOT READY**。対象 `0x00557A20`、新規重点 `0x005EE240`、そのFuncInfo `0x0064873C`、unwind map `0x0064870C`。
対象EXE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
既存索引SHA `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`／統合V9 SHA `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`。

## 事前確認・重複境界
MASTER_LEDGER／規約／REA README・QUEUE・PROGRESS・旧RUN `20261011T153309850Z`／最終同期 `progress_sync_20261011T153958076Z.json`／検索DB README・BUILD_MANIFEST・21H証拠を先読。
旧PROGRESSの15/16はSTALE_RENAME_DENIED。最終保存同期がWave1～5の**64/64 VERIFIED**で正式根拠。21HのCRT malloc二層new-handler証拠54/54を維持・二重計上せず。
Ghidra旧索引は `0x005EE240` をNOT_FOUND、統合V9では `EH_FH3_WRAPPER_005EE240`、body 46 bytes、FuncInfo VA 0x0064873C と認識。今回は未読だったFuncInfo本体とunwind tableを**原作同SHAのPE専用コピーから独立で復元**。GhidraやREAを再起動していない。

## 新規の機械語・FuncInfo根拠
- `0x00557A20 PUSH -1`、`0x00557A22 PUSH 0x005EE240`、`0x00557A55 MOV FS:[0],EAX` が例外登録。正常出口 `0x00557FDB MOV FS:[0],ECX` で元に戻す。
- EHラッパー `0x005EE264 MOV EAX,0x0064873C` に続き、`0x005EE269 JMP 0x005B8B1E` でC++ EHフレーム処理へ**末尾JMP**。通常の関数戻りABIや通常のE8 CALLとは区別する。
- `0x0064873C` の9 DWORD：`19930522, 00000006, 0064870C, 00000000, 00000000, 00000000, 00000000, 00000000, 00000001`。
- MSVC EH3 FuncInfoの`maxState=6`、`pUnwindMap=0x0064870C`、**`nTryBlocks=0`、`pTryBlockMap=NULL`**。unwind table 6×8=48 bytesは、`0x0064870C`からFuncInfo先頭`0x0064873C`まで丁度連続する。
## 6件のunwind（例外時ローカル後始末）状態
| state | 遷移先 | handler VA | 処理候補 |
|---:|---|---|---|
| 0 | -1 | `0x005EE1D0` | 文字列`-0x588`、`JMP 0x004026B0` |
| 1 | 0 | `0x005EE1DB` | 文字列`-0x56C`、`JMP 0x004026B0` |
| 2 | 1 | `0x005EE1E6` | istringstream`-0x660`、`JMP 0x00428680` |
| 3 | 2 | `0x005EE1F1` | 文字列`-0x5A4`、`JMP 0x004026B0` |
| 4 | 3 | `0x005EE1FC` | `-0x668 & 1`で文字列`-0x5C0`の片付け |
| 5 | 3 | `0x005EE21E` | `-0x668 & 2`で同領域`-0x5C0`の片付け |

`0x004026B0` は短文字列容量を0xFへ戻し必要時freeする関数、`0x00428680` はistringstream関連破棄関数と既存擬似Cが整合。全6つのactionを原作PEから逆アセンブル、V9にあるcompiler unwind fragmentとも関係確認。4/5は同じバッファを**別フラグ**で条件付き片付け、直接両方実行するとは限らない。

## 解釈と限界
**この関数のC++ EHメタデータにはローカルtry/catchが0件**。LF-only debug_paper の不正な文字列長が実際にbad_alloc等を送出した場合、`0x00557A20`内のC++ catchで回復する経路はこのメタデータからは見つからない。一方、6状態のunwindにより生存オブジェクトを後始末する設計は確認できた。
**上位関数で捕捉される可能性は未調査**。クラッシュ、例外発生確率、負荷、ソフトの最終挙動は一切実測していない。原作エラー/異常系を不必要に再現する実装指示ではなく、互換境界調査のSTATIC資料。
後続の優先対象：呼出元`0x005554F0`からCRT入口までの例外伝搬・catch境界、`DAT_0068E8C0`の書込元（直接/間接xref）。ゲームGoldenはCRLF/LF-only/最終行改行なし/1024byteをDESIGNED / NOT RUNで保持。
## 監査結果と安全
対象限定監査 **47/47 PASS**（検査条件数≠関数数）、失敗0。2回目の`--save`でも47/47 PASS。初回2.300秒、保存時1.311秒。SQLite両DB quick_check=ok、原作・DB両版ハッシュ一致。
REA正式Wave1～5 VERIFIED=既存64/64維持、**新規正式VERIFIED=0**、新規5種完全充足=0。info/pseudo/callers/calleesはINDEX_ONLY、assemblyはTARGETED_PE_NATIVE。正式TODO/VERIFY/BLOCKED差分=0/0/0、ゲームGolden PASS=0、strict MATCH=NOT RUN、完全複製率未測定。
Windows研究PC接続あり。active.lockなし、空き物理RAM約13.48GiB、CPU負荷不明、研究全体時間不明。新規REA/Ghidra/原作ゲーム実行なし、Workなし。
出典：既存`search.py function/callers/callees/related`、V9 `function 0x005EE240/0x005EE1FC`、原作同SHAのPEバイト、同所有内の独立 `REA_20261027_22H_P0_DEBUGPAPER_EH_PROBE.py`・`...EH_AUDIT.py`・`...EH_EVIDENCE.json`。
保存は`rea_lab/decomp_task`所有範囲の**新規5ファイル（probe／audit／evidence／report／readback）**に限定。原本ZIP/EXE/SAVE、MASTER、他レーン、既存RUN、QUEUE/PROGRESS、Git、公開先、スケジュールを変更しない。安全拒否なし。
