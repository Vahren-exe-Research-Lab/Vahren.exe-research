# 迫真戦記 ver0.67｜新B T012/T024：Unitカウンタ満了先は `voice` ScriptBlock を参照する

- 研究ID：`B-OFFLINE-20261022-1210-T012-T024-VOICE-EXPIRY-01`
- 復旧/接続ID：`B-RC-20261022-1208-LOCAL-SESSION-TERMINATED-01`
- 実施：2026-10-22 12時台 JST。Owner：B（T012とT024）。T013既存集計は今回は変更しない。
- 判定：`OFFLINE-UNSYNCED / STATIC / INFERRED / VERIFY / NOT READY`。B/Master READY追加0、DONE追加0、Gameplay Golden PASS0、strict MATCH0。
- PC接続：Desktop Commander Local Compactによる `evidence/LANE_B_HANDOFF.md` 読取を最初に試行。実エラー `INVALID_ARGUMENT: Error code: INVALID_ARGUMENT; Error: McpServerError: Session terminated`。接続障害であり、安全拒否ではない。PC最新正本・予約・最新READY・回収索引の照合不能、PCへの書込/同期なし。
- 保全済みの過去オフライン成果：`B-OFFLINE-20261022-1010-T024-TIMER-ACTION-01`、`B-OFFLINE-20261022-1112-T024-T012-ACTION-TIMER-01` を読み、再計上しない。09時台以前の未保存安全拒否は解決扱いにしない。
- 証拠：Library `/HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip` のread-only写し。ZIP SHA256 `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`、34 entries、CRC PASS。内部 `search.sqlite` SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`、immutable read-onlyで `PRAGMA quick_check=ok`。元EXEのSHA256はmanifest記録 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`（今回原本バイト再計算なし）。10/22現行V3/E8照合なし。

## 新規静的証拠と実装上の訂正点

1. **満了入口**：既存T012の `FUN_0057AA00` は `Unit+0x1E4F8` が正の場合だけ1減算し、1→0の際に `0x0057AB22 → FUN_0057B380` をCALLする（既存 `B-20261010-2117-03` の引用、新発見として再計上しない）。
2. **重要な新しい接続**：`FUN_0057B380`（VA `0x0057B380`, Ghidra size 1248）は `Unit+0x1DC` を参照し、`0x0057B453 → FUN_00469A20` を呼ぶ。`FUN_00469A20`（VA `0x00469A20`, size 2458）は `0x00469ABF` 付近で文字列 **`voice`** を構築・検索し、内部で **`voice_type` / `class` / `delskill` / `female` / `power`** などの属性を参照し、`ScriptBlock::vftable` のオブジェクトを生成する。よって `+0x1E4F8` 満了時のcallbackには **声・音声または発声スクリプトの選択・配送に関係する静的経路** がある。実際に音を再生する末端までは未証明。
3. `FUN_0057B380` の外側の入場条件は単純な無条件実行ではない。少なくとも `Unit+0x1867E == 0`、32-bit符号付き `Unit+0xC0 >=0`、`Unit+0xD0 >=0` が必要で、さらに `+0x8C!=0`、`+0x1F8==0`、`+0x1F9!=0`、`+0x18684==2`、`+0x1D0==0`、または `*(Unit+0x1D0+0x1E)==0 && +0x1867D==0` のいずれかを満たす複合ORゲートがある。`+0x1D0` の間接参照は直前のゼロ判定で短絡される。これはGhidra擬似Cに基づくSTATIC、ASM独立照合はVERIFY。
4. スクリプト由来の候補vectorを準備する `0x0057B467 → FUN_0046D180` について、callee擬似Cは `begin/end` から4バイト要素を複製する。`local_bc != local_b8` を満たす場合のみ候補処理へ進む。候補ゼロ時は行動開始を仮定しない。
5. 分岐キー `Unit+0x1E524` が **0** の経路は、`0x0057B4CE → FUN_0049EB50`、`0x0057B559 → FUN_00463280` などを使用し、`Unit+0x1E51C` 周辺に追加処理がある。キーが **非0** の別経路では `Unit+0x1E520` を参照し、比較・候補選択・レコード更新を実行する。両分岐は無条件に同じ動作とはいえない。`0x0049EB50` 擬似Cは `0x1ED1CC` 起点・stride `0xB4`・最大 `0x18` 件の内部slotを探索するが、これを原作ゲーム内の『音声キュー24個』と命名するのはまだINFERRED。
6. 非0の経路では `Unit+0x1E520` が示す連結レコードの `node+0x28` を減算し、結果 `<1` なら `0x0057B800 → FUN_00510030` を呼ぶ。`FUN_00510030` はmap/set系ノードのeraseと更新済みiterator返却に相当するポインタ付け替え・free・要素数減算を含む。これは **Unitタイマー満了後にも別レコードの寿命管理が進む** 静的証拠。`0x57B380` のイベント単位・レコード意味・音声出力保証はVERIFY。
7. `0x0057B838 → FUN_004BA280` はvectorの保持メモリ解放・3ポインタの0化を行う。候補なし・満了条件不成立・map erase時のリソース状態を勝手に「無害なreturn」と置換しない。
8. `0x0057B6FC → FUN_0049EB50`、`0x0057B779` と `0x0057B7D8 → FUN_00463280` も同callbackの別条件枝。`FUN_0040ED80` を経由する候補選択があるが RNG消費回数は未確定。全枝のGolden/RNG順は未検証。

## 既存の解釈に対する修正

11時台の『AIが `Unit+0x1E4F8` を設定 → 0到達時 `0x57B380` へ』はSTATICとして維持する。一方、それだけで **AIの攻撃・移動・待機の実行イベント** だと判断してはならない。今回、callback内に `voice` ScriptBlockを読み出す具体経路が見つかったため、少なくとも発声イベント/スクリプト配送が混在する。`Unit+0x1E4F8` は「AIアクション実行タイマー」ではなく **Unitの文字列付き通知/発声に関連するカウントダウン候補** と暫定ラベル変更するのが妥当。発声以外の副作用が全くないとする断定も禁止。

## 非重複・次回のP0調査

- 10/21オフラインB HANDOFF/T012/T024/MASTER snapshotに `0x469A20`, `voice_type`, `+0x1E524`, `+0x1E520`, `0x49EB50` の同定記録を発見できず。最新10/22正本未接続のため、非重複判定は暫定。
- PC接続復帰時：MASTER最新cp/Task Queue/READYと復旧索引を最初に読み、今回IDと既存ID/owner/競合/READYを照合してBが所有する資料へ **一度だけ** 取り込む。EのMASTERは変更しない。現行V3でE8 `0x57AB22`, `0x57B453`, `0x57B467`, `0x57B4CE`, `0x57B6FC`, `0x57B800`, `0x57B838` をJMP/RefTypeと独立に照合。
- 次は `0x469A20` が具体的に何の `voice` 定義を選ぶか、`0x49EB50` が script/event queueへ何を送るか、`Unit+0x1E51C/+0x1E520/+0x1E524` の構造体境界と所有者、`0x57B380` の音声以外の副作用を絞る。原作DATの voice/voice_type 実宣言と比較する。旧安全拒否範囲には触れない。
- Golden（**計画のみ・NOT RUN**）：無改変EXE/DAT/SAVE/MAP、同一入力・RNG・Unit/Skill/AIモードで `+0x1E4F8=0/1/2`, `+0x1E518=0/75`, voice候補空/あり, `+0x1E524=0/非0`, `+0x1E520` node TTL `0/1/2/10000`, 外側ガード各偽/真、発声イベント有無・AI実行行動・MP/RNG順を区別して観測。実測なしならGolden PASS=0、strict MATCH=0。

## 今回の保存先・復旧

- この報告は今回独立成果。PC正本へ未保存・未同期。Libraryの `/迫真戦記再開発プロジェクト/data/` に独立コピーを保存しreadback確認することを試みる。安全拒否が発生した場合、迂回せず拒否・未保存の事実だけ別途復旧IDとして記録し、できなければチャット本文を再開資料とする。
- 原作EXE/ZIP/DAT/SAVE/Git、他lane、REA、dev_lab、MASTER、ローカル設定・自動化スケジュールは変更しない。

### 再検索手順（既存のread-only検索基盤）

```text
python search.py function 0x57B380 --max-chars 12000 --limit 12
python search.py callers 0x57B380 --limit 20
python search.py callees 0x57B380 --limit 50
python search.py function 0x469A20 --max-chars 12000 --limit 12
python search.py function 0x49EB50 --max-chars 12000 --limit 12
python search.py function 0x510030 --max-chars 12000 --limit 12
```
