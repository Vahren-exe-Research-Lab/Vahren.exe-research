# 迫真戦記 ver0.67 REA独立静的研究｜GameManager仮想CALLのライフサイクル制約・ガード監査

- **独立研究ID**: `REA-OFFLINE-20261023-0331-T014-VPTR-LIFECYCLE-FLAGGATE-STATIC-01`
- **研究枠**: 2026-10-23 03:31 JST／REA／P0・T014
- **状態**: `OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY`
- **対象**: `0x00543428`（`0x005433D0`内）、GameManager vtable `0x00638DF0` +`0x1C`、基底vtable `0x00638E1C` +`0x1C`、状態バイト `GameManager+0x1EF148`
- **操作境界**: 原本EXE・ZIP・SAVE、PC正本MASTER/QUEUE/PROGRESS、研究A〜E/T018/dev_lab/Git/スケジュールを変更していない。REA/Ghidraの新規プロセスを起動していない。Work未使用。

## 研究環境・重複排除

- Desktop Commander Local Compactの先行read_multiple_files試行は `UNAVAILABLE / McpServerError: Connection timed out`。**接続タイムアウト**であり安全拒否ではない。PCの電源/負荷、active.lock、最新owner・QUEUE/PROGRESSは確認不能。
- 代替は本人が事前共有したChatGPT Libraryの`Vahren.exe`、`HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip`、`decomp_task.zip`。EXE・DB等はすべて**読取専用**。既知の問題の別経路再実行や安全拒否対象 `0x5710C0..0x571500`へのアクセスは行っていない。
- 原作EXE SHA256: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` （2,910,720 bytes）
- オフラインZIP SHA256: `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`、ZIP CRC **34/34 PASS**。
- `search.sqlite` SHA256: `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`、manifest一致、`PRAGMA integrity_check=ok`。
- `decomp_task.zip` SHA256: `E1ECF0B9C9A315DF3EAE39BC88399B54150ED0622BAEE813D945D31F7D2442CB`、ZIP CRC PASS。過去runアーカイブには関数ごとの5種証拠が**62関数分**確認できた。他2件の既往証拠は別パスから参照されるため、これだけで全64件を再認定しない。オフラインQUEUEではWave1=16 VERIFIEDだがWave2〜5の48件はTODOと表示。一方Wave2〜4はそれぞれ凍結値10/10、10/10、12/12であり、**EPERMの影響でQUEUE表示が古い**可能性に注意。既報のWave1〜5 64/64は過去報告値のまま、加算しない。
- 比較対象: 02:33の既存 `REA-OFFLINE-20261023-0233-T014-CONTEXT-SELFRECEIVER-WRITER-STATIC-01`。今回の新情報は **(A) デストラクタ側のvptr逆遷移、(B) 基底スロットの実装が即RET、(C) `+0x1EF148`を参照する全リテラル命令の読取限定性およびPEローダの初期ゼロ**。前回のGameManager自己参照や新規仮想ディスパッチ件数は二重計上しない。

## 増分A：構築時と破棄時にvptrが逆向きに切り替わる

原作PE32の機械語および既存SQLiteの関数境界・CALL索引を照合した。

| フェーズ | 命令VA | 機械語 | 機能 |
|---|---|---|---|
| 基底コンストラクタ `0x553B20` | `0x553B4F` | `C7 05 F0 E2 8B 00 1C 8E 63 00` | `[0x008BE2F0]=0x00638E1C` |
| 派生コンストラクタ `0x553A90` | `0x553ACB` | `C7 05 F0 E2 8B 00 F0 8D 63 00` | `[0x008BE2F0]=0x00638DF0` |
| 派生デストラクタ本体相当 `0x4B8650` | `0x4B8675` | `C7 06 F0 8D 63 00` | `[ESI]=0x00638DF0` |
| 基底デストラクタ本体相当 `0x4BBAE0` | `0x4BBB09` | `C7 07 1C 8E 63 00` | `[EDI]=0x00638E1C` |

後半の2箇所は**絶対アドレスへのWRITEではなく、オブジェクトポインタ経由のWRITE**である。Ghidraの`data_refs`で `0x008BE2F0` のWRITEとしてコンストラクタ2件だけを見ても、デストラクタのvptr書換えを見落とす。これは前回の「動的vptr維持未確認」の重要な補強となる。

確認済みCALL辺: `0x004B86F4 → 0x004B8650`（デストラクタラッパーから派生本体）、`0x004B86CC → 0x004BBAE0`（派生本体から基底本体）。いずれもE8相対オフセットを再計算し、SQLiteの`calls`レコードと一致。

`.rdata`を直接読んだvtable +`0x1C`の値は、**最終GameManager `0x00638E0C → 0x004B9D70`**、**基底GameMngBase `0x00638E38 → 0x004BBBD0`**。基底ターゲット `0x004BBBD0`の先頭実命令は `C3`（RET）で、**スタック引数を回収しない即復帰no-op**である。派生ターゲットは状態フラグを判定してから内部状態をクリアする。異なるvptrへの切替を無視し、両方を常に`0x004B9D70`としてフックする実装は不正確になり得る。

**範囲制約**: デストラクタでvptrが切り替わる静的構造は確認したが、`0x00543428`がデストラクタ実行中に再入・到達することは**未確認**。安全な結論は「全実行状態で同じvptrが維持されるという仮定は証明できない」であり、「破棄時に必ず基底スロットがCALLされる」ではない。

## 増分B：状態バイト `+0x1EF148` の静的利用と初期状態を限定

原作EXEの`.text`に存在するdisp32バイト列 `48 F1 1E 00` をPEセクション境界内で**全一致検索**すると**16命令位置**。コード逆アセンブルで16/16が `CMP BYTE PTR [reg+0x1EF148],...`、または`MOV CL,BYTE PTR [reg+0x1EF148]`に該当し、直接ストア命令は**0**。SQLite疑似Cで当該オフセットを含むのは**15関数**（`0x4B9DC0`等、関数内に複数の参照があり得る）。

代表的な実バイト:

- `0x004B9D78`: `38 91 48 F1 1E 00` → `CMP [ECX+0x1EF148],DL`。
- `0x004B9D7E`: `74 38` → フラグがゼロなら `0x004B9DB8`へ分岐し、副作用をスキップ。
- `0x004FCC15`: `8A 89 48 F1 1E 00` → `MOV CL,[ECX+0x1EF148]`（読み出し）。
- `0x004DE868`: `38 98 48 F1 1E 00` → `CMP [EAX+0x1EF148],BL`。

派生ターゲット `0x004B9D70` は、非ゼロ時にオブジェクト `+0x80=25`、`+0x84=40` を設定し、`[ECX+0x98]`配下の複数バイトをゼロ化することが先行研究で確認済み。今回の新情報はフラグの**直接書込先がリテラルdisp32参照には見つからない**こと。

計算上、初期グローバルGameManager `0x008BE2F0 + 0x1EF148 = 0x00AAD438`。PEの`.data`セクションは**VMA 0x0065A000、VirtualSize 0x004BAA4C、RawSize 0x00033C00**。`0x00AAD438`は仮想サイズ内、RawSize外の**ゼロフィル領域**に存在する。通常のPEローダはその領域を**初期状態ゼロ**として割り当てる。ただし、実際に関数を呼ぶまでに別名参照、別の基点+小オフセット、領域一括コピー、外部モジュール経由等で値を書き込む経路を**否定していない**。

**重要**: 「ローダの初期値=0」「直のdisp32参照はすべて読み込み」の2点から、「原作ゲームで永久に0」「ガードが機能しない」と結論付けてはならない。実際の書込経路と遷移時刻はP0/VERIFYに残す。

## 再実装・Golden試験条件（設計のみ）

1. map新規空（登録前要素数0）かつ**最終GameManager vptr**・フラグ0: `0x00543428 → 0x004B9D70`と解決されても、当該関数は副作用なしで戻るはず（実機未測定）。
2. 同条件・フラグ非ゼロ: `0x004B9D70`が上記内部フィールドを設定。`[ECX+0x98]`が有効な構造体を指すことも観測する必要がある。
3. 登録前map要素数が正: `0x0054341E`で仮想CALLごと飛ばす。関数本体のガードと**別のゲート**として検証する。
4. 基底クラスvptr `0x00638E1C` の状態で同スロットを解決した場合: `0x004BBBD0`（即RET）。ただしGameManagerの正常な登録・破棄で到達可能かは未検証。
5. PEローダ直後のフラグゼロから、ゲームが初回画面登録に到達するまでに、どのイベントで変化したかを読み書き監視で確認する。動的トレーサー実装・Golden採取は今回**行わない**。

## 独立検証、5種証拠、保存状態

- `verify_rea_t014_vptr_lifecycle_flaggate_20261023.py`を原本・検索DB・manifest・旧REA archiveに**read-only**で実行: `PASS`。マシンコード**28個のユニーク指定命令箇所**、`+0x1EF148`のリテラルdisp32**16/16**、間接CALL索引**1**、直接CALL索引**2/2**、`.rdata`vtable**2/2**、関数擬似Cのdistinct SHA **22関数**で一致。ZIP CRCとSQLite整合性もPASS。
- **REAの正式5種証拠**: 今回の対象`0x4B9D70`・デストラクタ系列について、Ghidra検索DBの`pseudo`や局所ASM/SQLite caller・calleeを確認したが、REA正式`info/pseudo/assembly/callers/callees`一揃いの新RUNは無い。**新規VERIFIED 0**、新規5点完備**0**。過去の64/64は別時点の報告値で、今回の62件アーカイブ現物検証を加算しない。
- 正式TODO/VERIFY/BLOCKEDの**台帳変更0/0/0**。オフライン研究内で**P0/VERIFY継続2件**（別名書込・実行中vptr遷移）。新たな安全拒否0。
- 原作ゲーム実行0、**Golden PASS 0**、strict MATCH 0、完全複製率未測定。
- 単体検証器実行時間は成果JSON `session_validation_seconds`参照。調査全体の実行時間・研究PC負荷は不明。

## 引継ぎ・同期上の残課題

- **次回優先**: `0x1EF148`への**別名・間接・バルク書込**を追う。候補となる構造体初期化/ロード/イベント更新のcallerを検索DBで絞り、少数のASMだけ読取検証する。関係のないGhidra全関数再解析はしない。
- 次点: `0x4B8650→0x4BBAE0`が実際にどのタイミングで呼ばれ、画面mapの寿命と交差するかを調べ、reentrancyを厳密に区別する。
- **接続障害ID**: `REA-RC-20261023-0331-LOCAL-TIMEOUT-01`。試行は正本複数ファイルの先読、失敗理由`McpServerError: Connection timed out`、正本最新の未読/未同期、影響は正式台帳差分とowner/lock確認不可。復帰後の安全な次手は最新MASTER/QUEUE/PROGRESS/runs/owner/hashesを先読し、今回の研究IDと既存IDの重複・競合を照合した上でREA所有範囲だけ単回同期。
- 本研究は **OFFLINE-UNSYNCED**。PC正本に保存したと偽らない。前回までの研究記録・正式VERIFIEDを消したり二重計上したりしない。
