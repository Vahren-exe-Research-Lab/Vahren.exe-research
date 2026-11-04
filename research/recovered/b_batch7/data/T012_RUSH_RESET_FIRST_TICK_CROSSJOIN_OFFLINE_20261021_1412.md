# 迫真戦記 新B／T012 — Rush系生成レコード再利用・初回周期ゲート跨関数照合（2026-10-21 14時台）

- 研究候補ID：`B-OFFLINE-20261021-1412-01`。owner：B/T012（T011召喚部隊参照、T013 Skill handler参照のみ）。
- 復旧ID：`B-RC-20261021-1412-LOCAL-SESSION-01`。CONNECTION/TRANSIENT。状態：`STATIC-GHIDRA_PSEUDOC / INFERRED-CROSSJOIN / SYNTHETIC-ONLY / VERIFY / OFFLINE-UNSYNCED / NOT READY`。
- 原作ver0.67 EXE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` はオフラインmanifest記載値であり、今回の原本実体を再hashした値ではない。
- PC：Desktop Commander Local Compactによる `[RESEARCH_ROOT]\MASTER_LEDGER.md` 冒頭読取は `INVALID_ARGUMENT: Error code: INVALID_ARGUMENT; Error: McpServerError: Session terminated`。安全拒否ではなく接続障害。PC MASTER/HANDOFF/予約の最新確認と未同期回収は0。checkpoint195／E累計595は過去の報告で、最新値と断定しない。
- オフライン正本候補：Library root `HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip`（19,646,444 bytes）、SHA256 `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`、34 entries／CRC errorなし。`headless_analysis/search_index/search.sqlite` 53,927,936 bytes／実測 SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`；`search.py` SHA256 `DF2E4C9220E6EA564C3955D5BF60628D0F2B04F850CDC0FBFD8F413B412A44B0`。manifest status PASS。DBはscratchでSQLite `mode=ro&immutable=1`、ZIPは変更していない。
- 元研究スナップショット `research_snapshot/evidence/LANE_B_HANDOFF.md` SHA256 `6C8A5359E6214F1504D9A288D17BB8F75725A788337F669366949748DC71ADBE`。過去PC最新版との重複・READY監査は不可能。既拒否対象VAや拒否された本文の再要求なし。

## STATIC：レコード初期化とtick処理（具体アドレス）

1. `0x0054F720` の保存済みGhidra擬似Cと直接CALLグラフ：既存レコード `record+0x1D0 == 0` を見つけた再利用経路は **site `0x0054F7DD → 0x0054F990`**。空きがなければ0x218Bレコードを確保・登録し、**site `0x0054F819 → 0x0054F990`**。2つの経路が同じinitializerを呼ぶ。以前の `B-20261013-1130-01` READY-STATIC-BODYと同じ関数本体であり、再採番しない。
2. `0x0054F990` 擬似Cで `record=param_3` とすると、**`record+0x1D0=1`（active候補）、`record+0x1D4=in_EAX`（定義候補）、`record+0x1F0=0`（試行番号）、`record+0x1F8=0`（リンク先候補）、`record+0x1F4=*(in_EAX+0x78)`（周期カウンタの初期値=定義周期）**が同じ前半ブロックにある。さらに `record+0x1FC=0`。既存 `B-20261013-1154-01` は initializer 全ASMを保存済みなので、今回新規発見として再計上しない。
3. `0x005501A0` 擬似C：引数 `manager+0x1F4` を先に1加算し、`def=*(manager+0x1D4)`・`def+0x78 <= manager+0x1F4` のゲート成立時にカウンタ `+0x1F4=0`、dispatch、`manager+0x1F0` を+1。kind4は **site `0x00550219 → 0x0054E7B0`**、elseは **site `0x0055037F → 0x00580280`**（後者の既拒否VA部分の解析・再取得なし）。上限で **site `0x005503F9 → 0x004C22B0`**、終了時に `manager+0x1D0=0`。
4. **今回の独立増分／INFERRED**：`0x54F990`で初期化した**同一レコード**が`0x5501A0`の`manager`に渡るなら、初回 tick前 `timer=interval`、tick開始で `timer=interval+1` となる。32-bit signed overflowがない通常の非負小整数 `interval>=0` では `interval <= timer` は**初回更新で真**。その後timerは0に戻り、`interval=N>0`なら次の試行は原則N回目の更新に発生する。再利用レコードも+1F0と+1F8が0に戻るため、前回の試行番号・リンク先を持ち越さない候補となる。これは既知の個別BODYを「pool reuse → initializer → update gate」とつないだ新しい条件付き横断知見であり、最初の発動タイミングを実機で確定したわけではない。
5. `0x5501A0`にはDB上の直接callerが0、該当vtable/関数ポインタ実体は未確認。`0x54F990`生成レコードと`0x5501A0`更新オブジェクトの**動的同一性はVERIFY**。`in_EAX`の正確な継続保持、符号比較、特殊値、オーバーフロー、実CALL順序やactive gatingもVERIFY。過去のT011別構造の `+0x1F0`（knock_speed等）とはオブジェクト型が異なるので絶対に混同しない。

## 既存成果と今回の差分

- 既存正式 `B-20261013-1130-01` は `0x54F720` pool既存/新規分岐、`B-20261013-1154-01` は `0x54F990`全body、`B-20261021-0910-01` は`0x5501A0`周期・上限処理。`B-OFFLINE-20261021-1215-01`の合成9条件はtimer初期化接続前、`B-OFFLINE-20261021-1310-01`は試行番号→Troop分岐。今回の新しいcrossjoinは「初期timerが周期そのもの」「pool reuseでtimer/attempt/linkを再初期化」「したがって初回tickでの即時ゲート候補」。旧個別関数・旧READYは再加算0。
- 機械的局所探索：SQLite内「`0x1F0`と`0x1D4`を同じ擬似Cに含む関数」3件に絞り、そのうち `0x54F990` の初期writerを見つけた（`0x5501A0` updateと`0x56F880`別構造も検出）。VAとコード同定：`0x54F720` code SHA256 `383700346A877CECCCACCBBA9A53A147359D2FC1F0490A3AAB7AF9189783CE0C`、`0x54F990` SHA256 `2EBA1181BDCCDA466333601F13D5A5EC4DC7FBBAB7A39FBA9891C04F17A99160`、`0x5501A0` SHA256 `1687A2EB67E5D43881EE8E1BCA397AB1089B23168D02AA5D7E86E13DA932CB31`。

## SYNTHETIC／Golden

- `test_T012_RUSH_INIT_FIRST_DISPATCH_20261021.py`で7条件をローカルPythonモデル照合：interval=0,1,2,3,5；quota=1,2,3。**7/7 SYNTHETIC PASS**。典型：N=3、quota=3なら `[1,0,0,1,0,0,1]` 回/tickの試行（**同レコードを適切に更新する場合だけ**）。モデルは元EXEも再開発ゲームも実行しない。
- 必要な実機Golden：原作0.67同一SHA/同DAT/SAVE/skill/map/入力/seed、合法的に初回発動/連続発動ができるか、既存pool reuseが生じるか、N=0/1/>1のskill定義がゲームにあるか、実tick・試行/個体数・owner/Troop・MP/HP/RNG/死亡/消滅を旧新比較。到達不能条件は`INELIGIBLE`。旧原作Gameplay Golden PASS=0、strict MATCH=0、DYNAMIC=NOT RUN。

## 拒否・復旧と次回

- この実行で新たなSAFETY_REFUSALなし。現存の `B-RC-20261021-0910-T011-08-SAFETY-01` と `B-RC-20261021-0910-HANDOFF-METADATA-SAFETY-02`はBLOCKEDのまま；元拒否コピー/コマンド・0x5710C0..0x571500・別拒否の0x58021E..0x580340を他tool/shell/path/ZIPで迂回していない。前報の02～08時台PC未存在7件は当時の確認履歴であり今回再確認できない。PC側回収・正本更新/統合は0。
- 今回未保存のPC差分：本研究および合成モデルのB PC data反映と`evidence/LANE_B_HANDOFF.md`への最終統合、既拒否文書の保留整理（いずれもPC側未実施）。LibraryのB-owned `/迫真戦記再開発プロジェクト/data/`へ独立報告＋合成テストを保存してreadbackする。正式READY=0、新規Task DONE=0、E MASTER統合=0。
- 次回：まず最新MASTER/規約/HANDOFF/復旧索引/READY owner・重複照合をread-only、既拒否は触れない。技術面は `0x5501A0`の実際のvtable/indirect CALL結合と`0x54F990`レコード同一性、初回tickの順序を許可済み索引・保存ASMで確認。次点で `0x54EF94..0x54F096` mode2/3の既保存B ASMと、第4引数の条件を照合。T011経験値継承、T012最終ダメージ/MP、T013最終対象選択、T024 AI時間制御、T028士気効果寿命は未解決P0維持。PC負荷・active.lockは今回取得できずUNKNOWN。
