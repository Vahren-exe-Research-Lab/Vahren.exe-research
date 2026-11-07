# 迫真戦記ver0.67 新B｜Missileの描画経路と二種類のソート経路の区別（2026-10-22 19:12 JST）

**研究ID**: `B-OFFLINE-20261022-1912-T012-RENDER-ORDER-ROUTE-01`  
**担当**: B / T012（ミサイル描画と戦闘処理）、T011（Skillフィールド）。T013/T024/T028への事実昇格は行わない。  
**接続復旧ID**: `B-RC-20261022-1912-LOCAL-SESSION-TERMINATED-01`。  
**判定**: `OFFLINE-UNSYNCED / STATIC-ASM / STATIC-SAVED-PSEUDOC / INFERRED / VERIFY / NOT READY`。  
**実行・変更禁止対象**: 原作EXE/ZIP/DAT/SAVE、PC MASTER、他lane、REA、Git。**新規正式READY=0、Gameplay Golden PASS=0、strict MATCH=0、MASTER統合=0、PC同期=未実施**。

## 証拠源、接続状態と既存拒否の回収

Desktop Commander Local Compactで指定PCの `MASTER_LEDGER.md`、レーン規約、B HANDOFFを最初に同時読取り試行したが、`INVALID_ARGUMENT: Error code: INVALID_ARGUMENT; Error: McpServerError: Session terminated` が返った。これは**接続障害**であり、既存安全拒否を再試行・迂回していない。正本の最新checkpoint、Task Queue、READY、active.lock、未保存成果は今回確認できない。

認可済みChatGPT Library直下に存在する `/HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip` と `/Vahren(2).exe` を通常の許可されたLibrary取得機能で**作業用の読み取り専用証拠源**として取得した。ZIP 34エントリのCRC検査PASS、ZIP SHA256 `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`、SQLite SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`（Manifest一致、`quick_check=ok`）。原作EXEを**実行せず**実バイトのみ調査し、SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` と直接一致した。EXE→VA mappingはPE32の各sectionを使用。再逆コンパイル・Ghidra再起動・REA処理なし。

過去18:13の研究ID `B-OFFLINE-20261022-1813-T011-T012-MISSILE-VTABLE-SLOT38-01` を継承し、そのLibrary上書き失敗 `B-RC-20261022-1813-LIBRARY-OVERWRITE-CONTAINER-01` は**未解決**とする。10/21収録 `research_snapshot/evidence/LANE_B_HANDOFF.md`、同日MASTERスナップショット、Libraryの `T011_T012_T013_T024_T028_UNSYNCED_RECOVERY_REGISTER_20261020.md` と18時台のB研究資料を読み、既存IDを再計上しない。最新PC正本・現行V3とは未照合。

## 発見1：Missile系2種類の vslot+0x48 は常に0を返す

原作`.rdata`の vtable `Missile=0x0063A544` / `SimpleMissile=0x0063A5A4` の両方で、slot `+0x48` と `+0x4C` は実アドレス `0x0043B5A0` を指す。原作ASM `0x0043B5A0: xor al,al; ret`（`32 C0 C3`）により、**このvptrを持つオブジェクトのslot+0x48の戻りは0**。この確認は旧DBの直接caller 0でも、実バイトvtable解決によるSTATIC-ASMである。

`0x004C5C80` は `0x004C5C9C: mov edx,[eax+0x48]` → `0x004C5CA1: call edx` → `0x004C5CA3: test al,al` → `0x004C5CA5: je 0x4C5CB1` と分岐し、**戻りが非0のときだけ** `0x004C5CAC: call 0x004C3DC0` に進む。したがって、通常のMissile/SimpleMissileのvptrを保持したまま`0x4C5C80`から登録する経路では、`0x4C3DC0`を通るリストソートは**スキップされる**。両者に代わり、`0x004C5CB6: call 0x004BC920` の空間登録処理へ進む（呼出先は18時以前の既知関数、新規と数えない）。

**重要な解釈修正**: 18:13には `0x4C5910` のvslot+0x38/+0x3Cソート比較が確定していたが、**それをMissile通常登録経路の実ソートと直結させてはいけない**。同ソート関数が他経路からMissileに適用される可能性は残すが、この登録経路の直接到達はSTATIC上不可。vptr変更や別呼出経路はVERIFY。

## 発見2：非0のslot+0x48は別の描画リストへ登録・ソートされる

`0x004C3DC0` の原作ASMでは `0x004C3DD3: mov edx,[eax+0x38]` → `0x004C3DD8: call edx` → `0x004C3DE0: js 0x4C3E0F`。戻り値の符号に応じてオブジェクト管理側`+0x18`または`+0x24`のリンクリストを選択する。その後 `0x004C3E2C: call 0x004C55A0` で各リストをソートする。

`0x004C55A0 → 0x004C5910` の旧CALL索引3箇所 (`0x4C567B`, `0x4C56C2`, `0x4C5725`) は既知だが、`0x004C5910` の原作ASM `0x4C5965` で第一キー（slot+0x38）を比較、一致時slot+0x3Cを比較、`0x4C5991: setl al` で**符号付き小なり**を使うことを再照合した。二本の連結リストのマージで第二側が厳密に小さい場合にだけ前へ移すため、**同値なら第一側の順番を残す（マージ局所の安定性）**。全体のソート安定性は個別Goldenで要確認。

## 発見3：Missileの通常候補には空間バケットから描画へ渡る別経路が存在する

`0x004C3EB0` のGhidra擬似CにはD3Dのrender-state設定・draw命令に相当するvtable `+0x114/+0x144`、`FUN_004c4970`、`FUN_004c4850` の反復呼出しがある。原作ASM `0x004C4142: call 0x004BC4F0` で可視領域候補を抽出し、同関数が返したバケット領域を`0x004C41A0/0x004C422A/0x004C42A8/0x004C4352: call 0x004C4850`などへ渡して頂点処理後にdrawする。

`0x004C4850`は、対象のslot+0x48が0である場合だけslot+0x1Cを呼び出し、頂点バッファ候補へ出力する。Missile / SimpleMissile vslot+0x1C はどちらも`0x0054D480`（既存Ghidra本文には頂点座標計算が存在）である。つまり **`+0x48=0`は非描画を意味しない。永続ソートリストに入らず、バケット描画側を通過できる条件**である。描画における全分岐・同一オブジェクトの可達性はVERIFY。

## 発見4：バケット3には別の2キー符号付き比較が存在する

`0x004BC4F0`はvslot`+0x40`を呼んだ後、値に3を足して**バケット番号候補**として使う。`+0x40 == 0`（`+3 == 3`）の場合、`+0x38`の戻りをオブジェクト`+0x04`へ、`+0x3C`の戻りを`+0x08`へ格納する（原作ASM `0x4BC67E..0x4BC6A6`）。これをバケット3（`DAT_00B036E8`近傍）の配列へ追加し、`0x004BC8E9: call 0x0047BB50` で整列する。ここで引数として渡す比較関数ラベルは **`0x004BBC60`**。

`0x004BBC60`は旧SQLite `functions`に関数エントリが**存在しない**が、原作ASMから新たに以下を確認した。

- `0x004BBC64/0x004BBC6C`: 左右オブジェクトの`+0x04`を取得し比較。
- 異なる場合、`0x004BBC84: setl al`（符号付き小なり）。
- 等しい場合、`0x004BBC73/0x004BBC78`で`+0x08`を比較し`0x004BBC7C: setl al`。

**したがってバケット3は、`(signed32(+0x04), signed32(+0x08))`の辞書式昇順比較**で整列する。これは**`0x004C5910`の永続リストソートとは別の具体的な経路**である。`+0x40 !=0`の他バケットはこの比較関数を通るとまでは言えない。

両Missile系vslot+0x40は`0x00546A20`であり、`[this+0xB0]+0x28`を戻す（Skill候補への参照）。この値が0なら通常のバケット3ソートに入る静的条件を持つ。値の合法範囲、DATプロパティ名、他のbucket経路の描画順はVERIFY。

## 原作再現の設計上の修正点

`Missile.sortKey`という抽象値だけを一個設け、全描画と戦闘の命中優先順に共通使用するのは不適切である。少なくとも（a）vslot+0x48に基づく描画投入経路の分岐、（b）vslot+0x40に3を加えたバケット分類、（c）バケット3の`(+0x04,+0x08)`符号付き辞書式整列、（d）`+0x48 !=0`時の永続描画リスト整列、を別々に扱う必要がある。`0x54D970`の`+0x9F4/+0x9F5/+0x28`返り値式は17時台既知のため再計上しない。T013の**最終対象選択順**やT012の**命中・HP確定順**は今回も未証明。

## 既存IDとの非重複と未解決

既知: `B-OFFLINE-20261022-1813-T011-T012-MISSILE-VTABLE-SLOT38-01`（vtable、`0x4C5910`の存在）、17時台`...SKILL9F5-WRITER-CONSUMER-01`、16時台`...MISSILE-POSTREGISTER-01`。**今回の新規増分**は、slot+0x48の値を踏まえた**Missile通常経路のソート非到達証明**、renderer `0x4C3EB0 → 0x4BC4F0 → 0x4C4850`の結合、旧索引から独立したASM比較ラベル`0x4BBC60`の二次キー署名と、3番バケットの区別。最新PC B/HANDOFFやV3との重複照合は未実施なので最終非重複昇格はNOT READY。

過去の安全拒否を解除しない。18:13 Libraryの訂正版上書き失敗は別IDのまま未完了。今回のPC接続失敗は別途`B-RC-20261022-1912-LOCAL-SESSION-TERMINATED-01`で記録した。次回正規復帰点は最新MASTER/B HANDOFF/未同期索引/現行V3の順で読取り、既存ID・owner・競合・READY状態を照合し、B所有領域だけへの一度限りの取込みを提案すること。E以外はMASTER統合しない。

## Golden / 次のP0

無改変EXEと一致するDAT、SAVE、MAP、同一入力・seed/RNG系列で、`Skill+0x28`（少なくとも0/非0）、`+0x9F4/+0x9F5`、Missile/SimpleMissile両型、vptr+0x48戻り、採用バケット、`+0x04/+0x08`、最終描画順を時系列記録する必要がある。等しい第一キー・異なる第二キー、負の第一キー、通常/特殊登録双方を区別する。描画順と**命中/HP反映順**を混同せずに独立観測すること。原作Golden PASS=0、strict MATCH=0。

次の検索先は T012 `0x0054D480`の描画用頂点生成ABI/戻り値と`0x004BC4F0`の重複候補収集の副作用、T013最終対象選択（このソートとの無関係性を確認）、T024 AIの選択順、T028 士気敗走の独立分岐。今回の原本範囲外と安全拒否済み領域には触れない。

## 証拠アーティファクト

対応する `B_T012_RENDER_ORDER_ROUTE_EVIDENCE_20261022_1912.json` は、原作ver0.67と旧SQLiteのSHA・CRC・整合性、2種類のvtable各9スロット、20件の原作ASM opcode一致、8件のE8直接CALL + SQLite整合、12件の擬似C SHAを記録する。すべてSTATICチェックであり、モデルGoldenではない。**両ファイルのLibrary保存および読み戻しは、実際に成功した場合だけ下記チャット報告で確定する**。
