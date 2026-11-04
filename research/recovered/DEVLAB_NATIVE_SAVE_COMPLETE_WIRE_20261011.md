# 迫真戦記 ver0.67 — 全セーブ保存構文のBYTE復元・逆コンパイル継続（2026-10-11）

## 目的と到達点
元作者のC++ソースは未復元。保存済みGhidra疑似C、既存機械語、実際に作られたsave1.sav/auto.sav/save2.savから、保存時の各レコード構造を独立に復元。数値変数・Unit・Spot・Power・Diplomacy・WorldGraphの全データを型付きパーサで読み、各レコードを順に書き直し、保存済み28byte鍵で暗号化し直した元の.savとのBYTE完全一致を3ファイルで確認した。
これはファイル形式の完全なバイト再構築の証拠であって、ゲーム内ロード、C++オブジェクトの生成、AI/戦闘/描画/イベントの挙動一致の証拠ではない。原作ゲーム実機とのstrict gameplay MATCHは0。

## 機械語・疑似Cの主要根拠
- EXE一致SHA256: e8dac301050c8e630d7e0ce93aeefd95e641207d9c0576017f62ba46a8767187。
- 0x460000通常保存writer/0x45E1E0通常save reader、0x427040/0x4270F0の32byte additive envelope。
- 0x4601A8..0x4602A8 数値mapのkey/aux/int32と11byte区切り `----------\x00`。従来の空文字区切り誤認を訂正。
- 0x4708A0はRAMの1byteをゼロ拡張したu32LEで書き込む（PUSH size=4→0x4628F0）。Unit+0x74～0x7A, +0xE8／Power+0x1C, +0x1D／Diplomacy 2flags／WorldGraph Path+0x88を含む。古いunit_runtime_prefix.pyのbyte直書きは誤り。
- Unit writer 0x58EFD0..0x58F7B2：5string、10DWORD、7flags+E8、4vector、+0x130 tree、@@@@、arbeit/arbeit_user/item_skill/friend、+0x13C string、末尾14 rawDWORD。旧reader0x58E870との意味論は別確認。
- Spot writer0x598CE0：name3、dword2、key tree、capacity/castlebattle/fightvalue/dunname。
- Power writer0x596AA0：byte-as-u32 2、名前/数値、複数tree/vector、B4 map key/rawDWORD、fixtype/train_max/train_up/base_level/home_spot、末尾empty×2。
- Diplomacy writer0x471D20：byte-as-u32×2、rawDWORD×2、Power名vector。load後のPower再解決はまだ未実装。
- WorldGraph writer0x435C10、Spot::vf24 0x5A93F0、SpotPath/EscapePath::vf24 0x5B0600とRTTI 0x6385BC/0x6387F4/0x638864。記録時の4つの文字列マーカーは `00000000` / `11111111` / `22222222` / `33333333`。静的初期状態の文字列は空だったのでランタイム変更時点・全scenarioへの一般化はVERIFY。

## 実セーブ構造照合
| 分類 | save1 | auto/save2 |
|---|---:|---:|
| 数値変数レコード | 1,958 | 2,591 |
| 一意な数値変数名 | 1,958 | 2,587 |
| Unit全レコード | 7,355 | 8,763 |
| Spot全レコード | 138 | 138 |
| Power全レコード | 29 | 29 |
| Diplomacy中のPower名参照 | 29 | 29 |
| WorldGraph Spot系 | 121 | 121 |
| WorldGraph 通常Path | 160 | 160 |
| WorldGraph EscapePath | 11 | 11 |
グラフ長は各9,656bytes、Diplomacyは153bytes。save1とsave2でグラフは全bytes一致。Diplomacy保存rawDWORD+0x14は0→1（変数の意味はVERIFY）。autoとsave2は暗号鍵こそ異なるが復号後の全byteが一致。
全レコードを保存と同じ順で再serializeし元の復号byte・元の暗号byteと完全一致。旧ファイルを上書きせず、新規 `reports/ACTUAL_SAVE_COMPLETE_WIRE_20261011.json` を生成。前回の `ACTUAL_SAVE_BYTE_GOLDEN_20261011.json` は区切り誤認によるSTALE記録として残し、 `ACTUAL_SAVE_SECTIONS_CORRECTED_20261011.json` が正しい数値。

## 新規コード
- `src/hakushin_compat/unit_native_wire_prefix.py`・`unit_native_full_wire.py`
- `src/hakushin_compat/spot_native_full_wire.py`・`power_native_full_wire.py`
- `src/hakushin_compat/diplomacy_native_wire.py`・`world_graph_native_wire.py`
- `src/hakushin_compat/normal_save_native_sections.py`・`normal_save_all_wire.py`・`normal_save_complete_wire_audit.py`
- `src/hakushin_compat/real_save_frontmatter.py`・`real_save_audit.py` は既存DEV専用ファイルとして証拠に基づく訂正。その他所有ファイル、ClaudeのPEER_SCRIPT01、5レーンA〜E正本は変更0。
- 戦闘副作用の増分： `main_decomp_status_special_subset.py`（suck/magsuck/drain/death）と `main_decomp_prestatus_counter.py`。0x578B70/0x576F10保存命令に限定した部分計算。未知death仮想+0x70、0x4DFD80/0x4DFBB0は停止境界。

## 未完了タスク（遊べる新エンジンのために）
1. P0：ロードしたraw値からUnit/Spot/Power実オブジェクトを構築、名前/所属/経路endpoint/経験値/能力値をリンクし直す。今回のBYTES一致を実ゲーム挙動へつなぐ。
2. P0：Claude CodeのスクリプトVM・宣言parserを統合し、yet/event/routine、ターン終了・内政を再現する。PEER専用ファイルは勝手に編集しない。
3. P0：戦闘の誤った1−R仮式を実native定数2.0に基づく2−Rへ修正する際、責任owner Bと共有して回帰。x87/MXCSR・乱数・状態異常の完全副作用はVERIFY。
4. P1：world graphのPath160/EscapePath11の参照文字列から実移動・シーン遷移・入力・表示を実装。Spot138≠graph Spot系121という集合の差を理由なく同一視しない。
5. P1：ゲームUIからの合法なセーブ→ロード→ターン進行・戦闘比較を実施し、初めてTARGET OBSERVEDやstrict MATCHを数える。
6. 管理：MASTER最新cp82・正式185研究ID・DONE9/34はレーンE所有につき変更しない。原本ZIP/EXE/.sav、Remote、Git、Windows設定、automation、過去安全拒否は触らない。

## 検査
個別元セーブSHA-256照合、厳密型、group終端・実データ全件/全構文復元、リグレッションテストで結果を固定。これは数千レコードのBYTE一致であり、元ゲームランタイムgolden PASSの増加ではない。
