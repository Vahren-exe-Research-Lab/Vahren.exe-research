# 迫真戦記 新B T011｜member lookupの逆参照更新と生成登録treeの成否境界（2026-10-21 06:10 JST）

- 研究候補ID: `B-OFFLINE-20261021-0610-01`。owner: B / T011 Unit/Class/Skill。T013の一般tree挿入関数は参照のみ。
- 状態: `STATIC-SAVED-GHIDRA / INFERRED (データ意味) / VERIFY / OFFLINE-UNSYNCED / NOT READY`。正式B READY追加0、E統合追加0、DONE追加0。
- PC接続: Desktop Commander Local Compactで `MASTER_LEDGER.md` の読取を最初に試行したが `INVALID_ARGUMENT: Error code: INVALID_ARGUMENT; Error: McpServerError: Session terminated`。分類CONNECTION/TRANSIENT、安全拒否ではない。PC最新OWNER/MASTER/HANDOFF/予約の確認とPCへの保存は未実施。
- 出典: ユーザー添付 `HAKUSHIN067_AI_OFFLINE_PACK_20261021(1).zip`、外側ZIP SHA256 `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`、全34 entry CRC PASS。
- DB: `headless_analysis/search_index/search.sqlite` 53927936 bytes、SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`、`BUILD_MANIFEST.json`の値と一致。SQLiteは派生一時読取コピーを `mode=ro&immutable=1` で開き、収録ソース・DBは改変しない。
- 対象原本 ver0.67 SHA256（マニフェスト記載。原本実測ではない）: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
- 主参照: SQLite `functions.code`, `calls`。`0x00467DE0` 擬似C SHA256 `BBAABFDEFFD065F862307964D73E46442959DCDCDF2DBFD392BAD1EF56D5CA09`、`0x00463280` 擬似C SHA256 `71422E164E422AF8665F4B7F6C9CD93A96CEA2CE5F5278D4EABA75035939ECAE`。`0x00582D90` `0x00466F60` は前回の保存済擬似Cと照合。

## 観測1：`0x00583506 → 0x00467DE0` lookupにはhit時の書込副作用がある（STATIC）

- `0x00467DE0` では `0x00467E1C → 0x004C1200` により候補nodeを取得する（`0x004C1200`はキー比較を含む）。
- `local_10 != *(int *)(param_1 + 0x300)` のhit分岐で、`*(int *)(*(int *)(local_10 + 0x28) + 0x1A4) = param_1` を実行し、続いて `uVar1 = *(undefined4 *)(local_10 + 0x28)` を返す。missing分岐では0を返す。
- よってこのlookupは**純粋な参照専用処理ではない**。hit時に返却オブジェクトの`+0x1A4`へ`param_1`を書き戻す。`+0x1A4`のゲーム上の厳密な意味（所属先・親文脈・キャッシュ等）はVERIFY。
- `0x00582D90`側は返却された`iVar5`を使い、`iVar5==0`または`iVar5+0x75 == 0 && iVar5+0x77 == 0`なら `0x00583546 → 0x00466F60`。従って**既存hitかつフラグで追加生成を見送る場合にも、hit lookupが先に実行されるため+0x1A4更新が起こり得る**（STATIC control/data path。実機到達はVERIFY）。
- この追加差分は前回`B-OFFLINE-20261021-0510-01`の「lookup/flag gateと生成cycle」の深掘りであり、同じcycleの再発見・二重READYではない。

## 観測2：新規候補のtree挿入には重複判定と挿入成否flagがある（STATIC）

- `0x00466F60`の `0x004671B3 → 0x00463280` は `param_1+0x2FC` を第1引数とする（推定用途：当該コンテキスト内のtree管理。実体型VERIFY）。
- `0x00463280`はnode+`0x1C`と投入候補の`+0x1C`を比較し、`0x004632D1 → 0x00402C40` や `0x0046335A → 0x00405370` を使いながら分岐する。新しいkeyを受け入れる分岐では `0x0046332C` または `0x00463376 → 0x004A6700` に進み、結果構造体`param_2`の先頭にnode pointer、次のbyteに`1`を格納する。
- 既存keyに対応する非挿入経路では、入力の文字列後始末を行った後、`*param_2 = puVar3` と `*(undefined1 *)(param_2+1) = 0` を返す。これは**挿入成功候補/既存衝突候補を区別する出力フラグ**（ただし例外・allocator異常・全callerの契約はVERIFY）。
- `0x004A6700`の擬似Cに `map/set<T> too long` とtree node配置・色/回転らしい処理があるため、標準ライブラリ系のordered tree挿入**候補**として整合する。原本ASMとシンボル型未照合のため `std::map`確定とはしない。
- 同じ`0x00463280`は既存T013研究でもtreeへの挿入helperとして言及済み。**今回のT011固有増分は、member lookupの書込と当該生成callerの`param_1+0x2FC` tree成否の接続**であり、汎用挿入helper自体を新発見として再計上しない。

## 観測3：別スロット管理と作成順（STATIC / INFERRED）

- `0x00466F60`には`0x00467000 → 0x00463CA0`の結果の`+0x1C`を読み、`0x00467126 → 0x004637A0`へ`iVar2+1`を渡した後に、`0x00467130 → 0x005B6C2B(0x1D4)`、`0x00467149 → 0x00582AA0`、`0x0046717E → 0x00582D90`、`0x004671B3 → 0x00463280`へ進む。生成側は索引候補作成→子初期化→tree挿入の順序。
- `0x00463CA0`が`param_2+0x310`を参照し、`param_2+0x30C`を登録側へ渡す別経路がある。`+0x2FC`と`+0x30C/+0x310`はオフセットが違うため、同じ格納領域と短絡せず、それぞれ個別追跡する。`iVar2`の実意味、name解決規則、親/子のunit identityはVERIFY。
- 追加の`0x00583557 → 0x00415530`はGhidra疑似Cでelement stride `0x1C`の追記風の操作がある。ただしunaff_EDI等、レジスタ由来引数が壊れているため登録対象の型・格納先はVERIFY。

## 再実装影響 / Golden受入条件（DESIGNED_NOT_RUN）

- lookup hit時`+0x1A4`の更新を見落として「既存memberなので処理不要」とすると原作と状態がずれる可能性。新規登録についてもtree既存keyの非挿入を区別し、重複member生成や順序の違いを避ける必要がある可能性（いずれもINFERRED）。
- 原作の合法なmember参照が「未登録→生成」「登録済み→フラグ0/非0」「同名候補複数」「別所属へ同じ候補」を作り得るか、DAT/実シナリオでまず確認。原作と再実装で起動EXE/DAT/SAVE/map/input/timing/観測可能seed/実プレイcaptureの同一性を採取。
- 比較観測はユニット/隊員数・順序・クラス・レベル・EXP・重複登録・戦闘行動とセーブ/ロード後の状態。hidden +0x1A4/treeの可視化が適法な実験でできなければUNKNOWNとしてpass判定に使わない。
- 原作Gameplay Golden PASS **0件**、旧新strict MATCH **0件**。新しい原作BUG確定 **0件**。擬似C staticがそのまま実ゲーム挙動を保証するとは扱わない。

## 重複・安全・次回再開

- 参照済み既存ID `B-OFFLINE-20261021-0309-01`（level/EXP）、`B-OFFLINE-20261021-0413-01`（level=0 sentinel）、`B-OFFLINE-20261021-0510-01`（member cycle）。前回0510文書とパック内研究B snapshotで`0x00467DE0` hitの+0x1A4書込を独立詳細として取り上げた記録は見つからなかったが、**現在PC MASTER/HANDOFF/ownerとの非重複検査は未完了**。
- 10/20に管理されていた26候補の過去分類X14/P4/I0/D1/C4/L2/O1、12ファイルPC回収履歴、安全拒否12件と168行INVALID JSONは**過去時点の記録**であり、今回更新・解除・再計上なし。`B-OFFLINE-20261021-0200-01`のPC部分保存状態もUNKNOWNを維持、再試行しない。
- 次の許可済み静的照合: `0x00467DE0`の`+0x1A4` reader/writer xref、`0x004637A0`/`0x00463CA0`のkey管理、`0x00463280`成功flagを使うcaller、`0x00582D90`への第三/末尾引数の原作ASM/ABI照合、既存+0x75/+0x77条件の原作DAT到達。具体的データ取得なしにmember帰属/再帰停止を確定しない。
- 最新PC MASTER・PROTOCOL・LANE_B_HANDOFF・B5ownerを接続復帰後に読み、保存先B owner/dataへの重複なしの小区画同期・独立readback後にのみB限定READY可否を判断。E専有MASTERは編集しない。
- 旧安全拒否操作・禁止VA`0x5710C0..0x571500`への新逆解析・別tool/path/shell/Remote/ZIP迂回なし。原本EXE/ZIP/SAVE実行変更なし、REA/Ghidra重処理なし、Git/push/他owner/dev_lab/Work/設定/automation変更なし。PC CPU/RAM実率不明。
