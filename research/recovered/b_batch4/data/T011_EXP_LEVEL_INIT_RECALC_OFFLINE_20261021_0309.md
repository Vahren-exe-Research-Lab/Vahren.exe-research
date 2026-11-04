# 迫真戦記 新B｜T011 Lv・EXP風カウンタの生成時初期化／再計算経路（2026-10-21 03時台 JST）

- 研究候補ID: `B-OFFLINE-20261021-0309-01`。Bの正式証拠IDではない。所有Task=T011、T012参照。状態=`OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY`。
- 復旧ID: `B-RC-20261021-0309-LOCAL-SESSION-01`（CONNECTION、SAFETY_REFUSALではない）。
- 証拠源: ユーザー添付 `HAKUSHIN067_AI_OFFLINE_PACK_20261021(1).zip`、ZIP SHA256 `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`、34 entry CRC 全PASS。
- 抽出した `headless_analysis/search_index/search.sqlite` SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`、BUILD_MANIFEST一致。SQLiteを`mode=ro&immutable=1`で軽量検索。参照する対象EXEの記録SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。この回に原本EXEからSHAを測り直したわけではない。
- 保存済み擬似C code_sha256: `0x58B7F0`=1A25189DEA9DD51CECAD5D5F3671EC3F03927AA2894D924228C8295C6ADEEE44、`0x58A540`=8B8F6EC30A565A9760B27883817B2A0C8D27FC6E30FD596BED767F97BD0E03D7、`0x58A400`=A3BD244F223D1765BB0F122D25D424BC7C524660DA763F5BB75AA687DD5BCEC8、`0x58A650`=6B530AC4D4372949EB50315A602773E539D3BAC1BB7308923AD87342CDF8F634。

## 一次スナップショットにおける局所STATIC

1. `0x58B7F0`擬似C: 引数`param_3==-0x7FFFFFF8`のとき、`param_2+0x1A4`に関係する辞書の`class`値をレベル候補へ取得。それ以外は渡された`param_3`を用いる。`param_1==0x00AB42F8`では辞書`scenario`の値を加算、別の`param_1!=0`では`param_1+0xDC`を加算。最終値は最低1へ丸められ、`param_2+0x168`に置かれる（この意味づけはレベル候補、実ゲームLv表示はVERIFY）。
2. 同じ関数の後半からの連続した直接CALL: `0x58C022→0x58A540`、`0x58C029→0x58A400`。両siteは検索DBのCALLグラフと保存擬似Cの呼出順で一致。
3. `0x58A540`: `param_1+0x16C=0`を書いた後、`+0x168 > 1`ならレベルに応じたループで`+0x16C`を再算出。`exp_max`と`exp_mul`という設定キーを参照し、成長の途中で`0x5D1B80`も呼ぶ。`+0x16C`は初期化経路で残存値を無条件に温存する領域ではない。`0x5D1B80`の実作用・スタック引数・丸めは未確定。
4. `0x58A400`: 旧`+0x170`を保持して、設定キー`exp_max`・`exp_mul`と、名前未解決の`DAT_00627620`の値に基づいて成長閾値候補を計算し、`+0x170`へ書く。`new(+0x170)<=old(+0x170)`かつ演算中の`uVar7 < +0x16C`の場合のみ`+0x16C=uVar7`へ調整する。無条件で「獲得EXPを消費して0へ戻す」処理とは読まない。
5. `0x551E50`の直接CALL `0x551FD3→0x58A650`は既存B研究のhit-side経路。今回読んだ`0x58A650`は`+0x16C >= +0x170`（unsigned）でループへ入り、`level_max`設定値が0なら`0x46F4C0(...+0x1A4,100)`を代わりに使用、許容範囲で`+0x168`を1加算。後段はステータス等の更新および`0x58AE65→0x58AFA0`、`0x58AE6C→0x58A400`を実行して、再度閾値条件を判定する。Lv上限実値・各関数の副作用・実レベル上昇UIはVERIFY。
6. `0x58B7F0`生成時 (`58A540→58A400`) と、`0x58A650`閾値到達時 (`58AFA0→58A400`) では**同じ閾値再計算関数を異なる前処理と組み合わせる**。ゲーム内の生成・復活・変身・召喚がそれぞれどの経路へ実際に到達するかは、この資料だけで確定しない。

## 新規性・設計上の注意

- 既存B保存の`0x551E50→0x58A650`、linked Unit+`0x16C/+0x170`、writer`0x58F659/0x58F672/0x58F68B`は**既知証拠**として参照のみで再計上しない。保存スナップショットB HANDOFF/T011/T012には、`0x58C022/0x58C029`、`0x58A540`、`0x58AE65/0x58AE6C`、`exp_mul/level_max`の同じ連結条件の記録がないことを検索した（スナップショット時点に限る）。
- この回の増分は**生成時のレベル元3経路→+168確定→+16Cの再構築→+170閾値計算**と、既知hit-side Lv処理での**+168増加→再計算**を静的に連結した点に限定。実ゲームで「任意ユニットのEXPを別ユニットへ自動転送できる」証拠ではない。
- 再開発案（未実装）: 表示上のUnit/変身・召喚Unitと、進行度の参照元Unitを独立IDで保持し、レベルのみ複写・+16Cのみ複写・レベルと閾値再計算・同一source共有の挙動を別々の規則として扱う。原作仕様として断定禁止。
- 未確認: `param_3==-0x7FFFFFF8`の合法実呼出、`param_1` mode、整数overflow、`0x5D1B80`の丸め/RNG意味、`DAT_00627620`キー名、`0x58AFA0`副作用、`0x58A400`のFPU経路、クラスチェンジ・召喚/死亡時のidentity、セーブ/ロードからの取り込み、表示EXP/レベル差、実性能。

## Golden受入設計（DESIGNED / NOT RUN）

- 同一EXE/DAT/SAVE/map/input/capture SHAと再現可能なseed/乱数状態（不明ならUNKNOWN）を揃える。初期Lv1/2以上、Lv上限付近、exp_max=0/非0、exp_mul差、経験値閾値の直前/一致/直後、連続レベルアップを分ける。
- 同じUnitを維持、戦闘終了→SAVE/LOAD、合法召喚・死亡後再生成・変身が可能な場合を別fixtureとし、可視Lv/EXP/技能/能力値/経験値獲得先を前後比較。+168/+16C/+170と参照元identityは合法的に取得できる別証拠がある場合にのみ補助観測、内部値のみではGameplay PASSにしない。
- 他ユニットの経験値を参照させる再実装の受入は原作再現と**ユーザー希望の拡張仕様**を別テスト系列で管理する。原作に未搭載と断定もしない。

## 接続・保存/復旧

- 2026-10-21 03時台 JST: Desktop Commander Local CompactでPC MASTER末尾の読取を最初に試行し、実エラー`INVALID_ARGUMENT: Error code: INVALID_ARGUMENT; Error: McpServerError: Session terminated`。分類`CONNECTION`/`BLOCKED-PC-READ`。Remote/Desktop別経路による再試行なし、安全拒否ではない。
- 前回の`B-OFFLINE-20261021-0200-01` PC部分保存の存在/完全性は依然UNKNOWN。`B-OFFLINE-20261021-0216-01`はLibrary保存済、PC未同期。今回それらのPCへの再送信なし。10/20までの26候補分類や旧安全拒否12件・不完全JSONは旧復旧台帳のまま変更なし。
- 本メモのPC保存、PC B HANDOFF追記は**未実施・PC未保存**。クラウド保存はアップロード後の独立readbackで確定する。E MASTER/原本/他レーン/rea_lab/dev_lab/Git/push/Work/設定/automationに書込なし。
- 次回PC接続時: 最新MASTER TASK QUEUE/checkpoint/予約・B HANDOFF・5 owner資料・旧復旧索引を優先し、`B-OFFLINE-20261021-0200-01`のPC部分書込の現状→この研究候補の重複/競合をread-only照合。B所有場所へ差分のみ保存・独立読み戻し、READYは原本ASM/最新所有資料/根拠の照合後に別判断。
- 次の軽量検索: `0x58B7F0` callerにおける`param_3`種類、`0x58AFA0`の実際のクラス/skill更新、EXP-like LinkedUnitインスタンスの`+16C` writerおよび保存/復元reader。原本Gameplay Golden PASS=0、新旧strict MATCH=0、新規正式READY=0、Task DONE追加=0。PC CPU/RAM負荷は未取得、不明。
