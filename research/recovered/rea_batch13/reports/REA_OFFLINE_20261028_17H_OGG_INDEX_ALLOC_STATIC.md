# 迫真戦記 ver0.67 REA｜2026-10-28 17時台 Ogg索引確保・返値ゲート

- **独立研究ID**: `REA-OFFLINE-20261028-17H-P0-OGG-INDEX-ALLOCATION-RETURNGATE-STATIC-01`
- **状態**: `OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY`
- **対象**: `0x005CF4D0`（Ogg索引構築）、`0x005D1310`（上位初期化）、`0x005CF320`（ページスキャン/値集計）、CRT `_malloc` `0x005B9BC8`・`_realloc` `0x005C30BE`。
- **接続障害**: Desktop Commander Local Compactで2026-10-28 17時台に読取を2回試みたが、両方 `MCP SSE probe returned 429 from openai.org`。これは**接続/制限の一時エラー**であり**安全拒否ではない**。PCの実オンライン状態、owner、active.lock、最新QUEUE/PROGRESS/MASTERは**不明**。Remote/別経路による安全拒否迂回は行っていない。

## 入力の出典・正本境界

Libraryの既存 `/HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip` と `/Vahren.exe` を読み取り専用でコピー。ZIP 34件のCRC PASS。内部の `search.sqlite` は10月21日時点の旧検索DBであり、PC最新統合V9ではない。独立再ハッシュで以下を確認：

| 入力 | SHA256 |
|---|---|
| Vahren.exe | `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` |
| オフラインZIP | `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2` |
| ZIP内search.sqlite | `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF` |

ZIP内 `PROGRESS.md` は2026-10-09時点で15/16 VERIFIED。過去会話で報告されたWave1〜5の64件は**今回は最新版正本から独立再検証不能**。15/16と64は別時点の異なる記録なので加算しない。MASTER snapshotも最新正本として扱わない。

## 増分1：`0x005CF4D0` の索引配列は6本まとめて確保し、各戻り値を検査しない

`0x005CF708`で索引の構築枝へ入り、`0x005CF77A..0x005CF7D7`で次の6件を実行する。VAは原作PE32機械語の**CALL site**。既存Ghidra DBの直接CALL索引とも1件ずつ整合した。

| site | API | 対象フィールド | 確保サイズ（count=`[EBX+0x34]`） |
|---|---|---|---|
| `0x005CF77A` | `_malloc` | `+0x38` | `8×count+8` |
| `0x005CF78A` | `_realloc` | `+0x48` | `32×count` |
| `0x005CF79D` | `_realloc` | `+0x4C` | `16×count` |
| `0x005CF7B0` | `_malloc` | `+0x40` | `4×count` |
| `0x005CF7C0` | `_malloc` | `+0x3C` | `8×count` |
| `0x005CF7CC` | `_malloc` | `+0x44` | `16×count` |

各CALL直後の `EAX` はフィールドへ保存されるが、NULLを検査する `TEST EAX,EAX / JZ` 等は入っていない。`0x005CF7DA MOV EAX,[EBX+38h]`、`0x005CF7DD MOV [EAX+EDI*8+8],EDX` で、最初の `_malloc` の結果を直接使う。CRT `_malloc`（`0x005B9BC8`）は失敗時にNULLを返す経路があるので、**確保失敗時の不正ポインタ使用候補**である。ゲームでの再現はしていない。

さらに`0x005CF79A`/`0x005CF7A5`は `_realloc` の結果で所有フィールドを直接上書きする。CRT `_realloc`（`0x005C30BE`）は失敗時NULLを返す一方、`HeapReAlloc` が失敗した元メモリを同関数では解放しない。このため、他の所有参照がない場合、**元ポインタ喪失・メモリリーク候補**となる。別参照の不存在までは証明していない。

これは前回16時台に確認した `0x005D3500`（Ogg**読込バッファ**確保）の失敗処理と**別の箇所**である。今回の対象はOgg**索引メタデータ配列6本**であり、前回発見を二重計上していない。

## 増分2：`0x005D1310` は索引構築の負のエラーを `-128` に正規化する

`0x005D140D CALL 0x005CF4D0` → `0x005D1415 TEST EAX,EAX` → `0x005D1417 JNS 0x005D1425`、負であれば `0x005D141B MOV EAX,0xFFFFFF80`（**-128**）で返る。上位 `0x005D1630` は `0x005D1689` でこの関数を呼び、戻り値非ゼロ時に`[ESI]`を0にして`0x005CFE00`の解放を実行する。

別経路では、tellによるファイル終端長が `-1` なら`0x005D13A7`で **-131** を返す。したがって**end/tell異常 -131 と索引構築失敗 -128 は別**である。索引構築失敗に`_malloc`のNULLクラッシュが必ず含まれるという意味ではない。NULL使用はこの返値処理に到達する前に発生し得るため、エラー返却を保証できない。

## 増分3：ページ集計 `0x005CF320` は負の64bit値を0に丸め、呼出元は結果のエラーを調べない

`0x005CF4A2 TEST EDX,EDX` → 負なら `0x005CF4AF XOR EAX,EAX; 0x005CF4B1 XOR EDX,EDX`。関数末尾には**負値を0へクランプ**する経路がある。呼出元 `0x005D1342 CALL 0x005CF320` は `EAX→EDI`・`EDX→EBX` に記録し、すぐ後ではコールバックの**存在**を検査する。`0x005CF320`から受け取った値自体をエラーコードとして検査する分岐ではない。

**条件付き見解**：読み込み障害により計算値が負となる場合、その区別が失われ、0件/0長と同様に処理される可能性。ただし、どの障害がこの負値へ至るかは未実測であり、`0x005CF320`全分岐の意味論も未確定。バグ確定とはしない。

## 独立監査

Python標準ライブラリでPEヘッダ/VA→raw offsetを解決し、原作機械語の局所バイトパターン、E8の相対CALL到達先、SQLite上のCALL登録、間接CALL登録、関数存在、SHA、ZIP CRCと`PRAGMA integrity_check`を監査。**92/92 PASS、失敗0**。対象のみであり、全関数のVERIFIEDや実機Goldenではない。

証拠の5種類: info=`INDEX_ONLY`、pseudo=`INDEX_ONLY + native照合`、assembly=`TARGETED_PE_NATIVE`、callers=`INDEX_ONLY + native E8`、callees=`INDEX_ONLY + native E8`。正式REA完全5種の新規充足0関数。**新規正式VERIFIED 0件、正式TODO/VERIFY/BLOCKED差分 0/0/0**（PC正本の現在数は未確認）。独立オフラインVERIFY論点を1 ID追加。原作ゲームGolden PASS **0**、strict MATCH **NOT RUN**、完全複製率**未測定**。新Ghidra/REA実行0、ゲーム実行0、Work不使用。

## 安全・再開位置

PC正本のowner/lock/既存ID未確認につき、MASTER、QUEUE、PROGRESS、既存RUN、原本、Git、他レーンへの書き込みは**一切なし**。成果は別IDとしてOFFLINE-UNSYNCEDで保全。CPU負荷・PCメモリ・研究全体の実行時間は不明。独立監査実行は約0.9秒。

次回P0：PC復帰時に最新MASTER/QUEUE/PROGRESS、owner/lock/重複ID、先行16時台までの成果を照合してから、正規REA所有領域に必要最小限の同期を検討。技術面では`0x005CF4D0`の確保失敗・`_realloc`失敗・countの32bit算術溢れと、`0x005CF320`のエラー時丸めを追加検証。必要ならゲーム原本を変更しない隔離fixtureで、正常Ogg/CRC破損/OOM時の返値・カーソル・リソース状態をGolden比較する（**未実行**）。
