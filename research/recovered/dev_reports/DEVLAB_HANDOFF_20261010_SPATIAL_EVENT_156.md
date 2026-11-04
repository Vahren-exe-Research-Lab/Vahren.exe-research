# 迫真戦記再開発・保存済み逆コンパイルの追加解析ハンドオフ（2026-10-10）

## 基準・所有権・動作

- Desktop Commander Local Compactで最初に `MASTER_LEDGER.md` checkpoint68、`evidence/ANALYSIS_LANES_PROTOCOL.md`、REA statusと前回16時台handoffをread-only確認。統合済みREADY113 ID／Task34(DONE9 IN_PROGRESS21 VERIFY4) は今回編集せず。開始時Local active terminal sessions0。
- 同梱ver0.67 EXEの旧保存済みGhidra `RUN_RESULT`／`pseudo_code`／`assembly`／`callers`／`callees`／`info`をread-onlyで突き合わせた。元EXEハッシュは保存RUN_RESULT内 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` と記録（この回で再hashなし）。
- **新規のGhidra/REA逆解析プロセス起動0**。過去にSAFETY_REFUSALとなった解析バッチを同一・別shell/tool/Remote/実行方法で試していない。REAキュー未完了9件はそのまま。重点STATIC VERIFIEDは39/48で全EXE完成割合とは無関係。
- 書込先は `rea_lab/decomp_task/STATIC_SPATIAL_EVENT_MISSILE_20261010.md` と独立 `dev_lab` の実装・tests・docs・reportsのみ。他A〜E ownerのdata/exe/evidence、MASTER/T018、原本ZIP/EXE、Git、システム設定、automation、Remoteは不変更。

## 新たな静的な枝対応

1. **`0x4E7ED0`**／T012・T013／保存run `20261009T224617297Z`。grid state +0x3C非zeroは方向表から単一セルoccupantを参照、座標signed÷32が0方向丸め。radius mode +0x3C=0ではsource action flags +0xB0/+0xA8とcounter+0x1E530のgate後radius+0x20を加えて周辺検索。両mode候補+0x65/1AE/1D0/1D4の4条件が必要。radiusは候補+0x228のgateつきeffective reachへstrict `distanceInt < radius`。grid branchに距離比較なし。Ghidra pseudoが省略したsource radius gateはassembly0x4E7F99..0x4E7FD3で補完。方向8点テーブル値／x87 trig／distance helper精度はVERIFY。
2. **`0x4321B0`**／T006・T014／保存run `20261009T225741694Z`。battle+invocation flagの両者成立時はspecial pathへ進み、この関数のusual numeric writerと3 evaluator CALL siteをskip。通常pathの初期 `0x40B200@0x4328E7` resultは+0x1EED40/41/42へそれぞれbyte store。参照A/Bの+0x1Dがtrueならそれぞれ後続evaluator callをskip、A成立でB全体skip。flag54=1→(pointer44=slot8630,48=slot8634)、flag55=1→(44=slot8634,48=slot8630)、両0→(44=slot8638,48=slot8634)。参照NULLはstructure+0x58に補完。履歴writeの実save永続化やnested unwindはVERIFY。
3. **`0x546F70`**／T012 saved native `exe/T012_ALLFUNC_FLOW_PROBE.txt` VA0x54714E..0x5471A6。先行skill/scene gate通過後Unit+0x1E560が2ならspatial無しでAL0早期ret、0なら`0x4E7ED0`へ。predicate true時はlatch=2でSkill+0x278 MP debit前にret、false時はlatch=1でMP減算へ進む。latch1（その他2以外の非0）ではspatial再実行なしでMP debit以後へ。missile成功/hitのbooleanだと断定しない。
4. **`0x4693F0` → `0x464290` → `0x4647D0`**／T005 saved Ghidra Wave3。`0x4693F0`のGhidra pseudoは両枝とも0x4647D0に見えるがassemblyで存在ならEDX=qualified key、欠損ならEDX=base keyと確認。0x464290 super探索にも`0x464550..0x46455C`のcounter++/cmp0x32/jlによる50反復上限を独立確認。既知の0x4647D0側50-pass上限と混同せず、全構文継承の最大深度を50と断定しない。generic_properties.pyのqualified-over-baseモデルと整合するが全special parser実装はVERIFY。

## 新たな実装・回帰

- `src/hakushin_compat/spatial_presence_subset.py`＋`tests/test_spatial_presence_subset.py`：6件。2mode区別、Cの負座標÷32、単一セル範囲、4条件、strict range、radius+32、入力制限。
- `src/hakushin_compat/event_view_branch.py`＋`tests/test_event_view_branch.py`：6件。特殊path bypass、3つの0x40B200呼出文脈、参照flagsのlazy判定、3 pointer mappings。
- `src/hakushin_compat/missile_latch_subset.py`＋`tests/test_missile_latch_subset.py`：6件。latch0/1/2、spatial laziness、MP減算前早期ret。upper-gateやdamage未実装。
- 完全回帰 `dev_lab/run_checks.ps1` 実行終了code0、**156/156 unittest PASS**（旧138＋新18）。MAP151/151、atlas513、script590(14,591,845byte)、parent21,214、context204、scenario/event body sample516と旧headless1v1/2v2各試験もPASS。合成内部テストであり、本家旧EXE TARGET OBSERVED actual PASS0、新エンジン strict MATCH0。

## 次に解析すべき内容

- 高優先：`0x57EB40`（spatial helper第2 caller）の前後の合法到達と副作用；`0x4E7ED0`の向き表データとradius x87幾何・0x44D8F0距離単位；イベント2参照+0x1Dの実オブジェクトとmarker更新（target static＋dynamic goldens）。
- `0x4693F0`のvariant presenceにある50反復guardと0x4647D0 getterの50反復guardの相互作用・49/50/51境界は旧EXE実機未検証なので専用golden候補のまま。
- セーブ後半reader0x58E480、Spot0x598980、Power0x5964C0は前回からVERIFY。Wave4未解析9件の新取得は許可された通常経路が可能になるまでBLOCKED。
- ユーザーはPCに触れないと明示しているため、手作業やセーブは依頼せず、既存`docs/USER_MANUAL_TASKS_DEFERRED.md`に保留。現時点でのmanual actionsは0。

## 根拠リンク（ローカルファイル内）

- `rea_lab/decomp_task/STATIC_SPATIAL_EVENT_MISSILE_20261010.md`（今回作成、命令アドレスとevidence ID付き）
- `rea_lab/decomp_task/STATIC_UNIT_SPOT_POWER_WIRE_LAYOUT_20261010.md`（前回保存）
- `dev_lab/README.md`・`docs/IMPLEMENTATION_PLAN.md`（テスト件数・実装範囲更新済み）
