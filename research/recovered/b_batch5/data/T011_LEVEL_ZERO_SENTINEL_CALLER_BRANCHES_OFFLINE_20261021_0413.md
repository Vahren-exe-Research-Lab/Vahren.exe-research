# 迫真戦記 新B / T011：「level=0」からclass基準Lv入力へ切り替える2系統caller（2026-10-21 04:13 JST）

- 研究候補ID：`B-OFFLINE-20261021-0413-01`。正式証拠IDではない。Task=T011、T012経験値経路を参照。
- 状態：`STATIC / INFERRED-SEMANTICS / VERIFY / OFFLINE-UNSYNCED / NOT READY`。新規B限定READY=0、E MASTER統合=0。
- 接続障害復旧ID：`B-RC-20261021-0413-LOCAL-SESSION-01`（CONNECTION）。Local CompactによるPC `MASTER_LEDGER.md` readを最初に実行したが、実エラー `INVALID_ARGUMENT: Error code: INVALID_ARGUMENT; Error: McpServerError: Session terminated`。安全拒否ではない。Remote等には切り替えていない。
- 使用資料：ユーザー添付 `HAKUSHIN067_AI_OFFLINE_PACK_20261021(1).zip`。ZIP SHA-256=`911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`、収録34 entryすべてCRCチェックPASS。`search.sqlite` SHA-256=`0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`（manifest一致、SQLite `mode=ro&immutable=1`）。収録対象EXEの記録SHA-256=`E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`（このrunに原本から再測定したものではない）。
- 保存擬似C SHA-256：`0x00582D90`=`0C97A9F541E871B941734CAC55644C0E68E80566BE16D84D9D8B641F690FED8E`、`0x004667B0`=`73CFEC184C9C691BC84E01DA71D0796149CB4D85044571488E7CC6DBCF62B33B`、`0x0058B7F0`=`1A25189DEA9DD51CECAD5D5F3671EC3F03927AA2894D924228C8295C6ADEEE44`。いずれもGhidra保存擬似Cであり原作ソースではない。

## 新しいSTATIC結合その1：`0x582D90` の設定キー `level` とゼロ→class番兵

1. DBのSTRING_INDEX/データ参照では、`0x0058328F`からアドレス`0x00626BD0`の文字列**`level`**への参照を確認。保存擬似Cでは `0x005832A3`付近で`0x00585AD0`を呼び、その戻り値の`+0x20`から整数`iVar5`を読む。
2. 擬似Cの同一制御経路では、`if (iVar5 == 0) iVar5 = -0x7FFFFFF8;`、次に`0x005832CF → FUN_0058B7F0`の直接CALL。`-0x7FFFFFF8`の32bitビット表現は`0x80000008`。ここでの「0」は`0x585AD0`から読んだ整数値であり、元DATのキー欠落と明示的`level=0`を区別できるとは限らない。
3. callee `0x0058B7F0`の保存擬似Cは第3引数が`-0x7FFFFFF8`の場合、Unit候補`+0x1A4`の辞書からキー`class`の値を取り直して`+0x168`へ書き込む。それ以外では渡された数値を使用する。その後、別の`param_1`種別による`scenario`値または`param_1+0xDC`の加算と下限1補正があり、`0x0058C022 → 0x0058A540`、`0x0058C029 → 0x0058A400`の順で経験値風累積値と閾値を再計算する。
4. **新しい限界付き結論**：`0x582D90`は `level` 設定結果0をそのまま「レベル0」として渡さず、`class`再参照の番兵値へ変換するcallerである（STATIC）。class基準値から最終表示Lvになるまでの補正、構造体実体、呼出到達はVERIFY。`level`が非0なら直接値を渡すが、calleeで下限1および別mode補正が残るため、単純な `final Lv = level` とは限らない。

## 新しいSTATIC結合その2：`0x4667B0` は番兵・明示class/参照元補正の別分岐

- 保存擬似C内の`bVar1`が真の場合、`0x00466A2E → 0x0058B7F0`へ`0x80000008`の番兵候補を渡す。一方、偽の場合は`FUN_004647D0(...,"class")`の読取値`iVar4`から出発し、`param_3 != NULL`かつ`param_3 != &DAT_00AB42F8`かつ`iVar4 <= *(int*)(param_3+0xDC)+1`であれば、callerが渡す数値を`*(int*)(param_3+0xDC)+1`へ変更して`0x00466A9E → 0x0058B7F0`を呼ぶ。条件が偽なら元のclass値を渡す。
- 擬似C上では`param_4 != 0`なら`bVar1=true`。`param_4==0`のときは別の`FUN_0040B200`結果にも依存する。`bVar1`のゲーム上の意味、`param_3+0xDC`のフィールド名、他modeの加算との重なりは未検証。
- この2分岐の後で`0x00466ABD → 0x0058AFA0`（Unit再計算関連）を呼ぶ。**番兵経路と明示値経路の区別**は静的に言えるが、これを「召喚」「異種雇用」「EXPの継承」と断定しない。
- CALLGRAPH確認：`0x58B7F0`直接CALLは計11 site・8 caller関数。今回の2 callerから3 site（0x5832CF,0x466A2E,0x466A9E）を具体的に結合。これらのsiteは提供スナップショットB HANDOFF/T011と前回`B-OFFLINE-20261021-0309-01`資料に同じVAでの記述が見当たらず、増分は**caller条件の確定的な静的読取**に限る。最新PCや他レーンとの完全重複チェックは未実施。

## 隣接する構造体更新と注意点

- `0x582D90`の保存擬似Cではレベル初期化CALL後、キー`enable`（0x626BD8, data-ref site0x5832D4）から`param_2+0xCC`へ初期値を書き、キー`enable_max`（0x626BE0, site0x58330A）から上限候補を読んだ後、条件`min<=max`で`0x5D1B80`を呼んで`+0xCC`を更新する。さらにキー`money`（0x626BEC, site0x583378）由来の値を`param_2+0x174`へ設定する。`0x00583585 → 0x0058AFA0`も後段に存在。
- `level`,`enable`,`enable_max`,`money`はDBで文字列を直接照合した。`+0xCC/+0x174`のフィールド名、`0x5D1B80`の乱数/丸め仕様、`0x58AFA0`の変化内容はVERIFY。入力・クラス/オーナー識別・ステータス再計算の順序を再実装の重要な検証対象とする。

## 未同期・安全境界・差分

- 先行候補`B-OFFLINE-20261021-0200-01`のPC書込みがタイムアウトして保存状態UNKNOWN（元Libraryは保管済）、`B-OFFLINE-20261021-0216-01`および`B-OFFLINE-20261021-0309-01`はLibrary既存保管のオフライン資料。今回、それらをPCへ再コピーせず、新規候補IDの二重登録・READY昇格をしていない。
- 2026-10-21 04:13 JSTのPC最新正本/HANDOFF/owner/未保存資料の実読取はCONNECTIONで停止。旧会話にあるcheckpoint195とE記載READY予定595は最新確認値ではない。前回の26候補・安全拒否12件・PC部分JSON168行INVALIDは当時の履歴状態として保留する。
- 禁止済み`0x5710C0..0x571500`、過去に安全拒否された本文/操作を別tool/path/Remote/ZIP経由で再提出していない。使用したのは別の未拒否T011関数のみ。原本EXE/ZIP/SAVEの実行/変更、Ghidra/REA重量再解析、他owner、MASTER、Git/push、設定、Work、スケジュール変更なし。PC CPU/RAM負荷は取得不能で不明。
- 本メモは許可B Taskのクラウド `data/` への保存・独立readbackを行う対象。PC正本/B HANDOFFには**未同期**。失敗操作の再開条件はLocalが正当に復帰したとき、まず最新版MASTER/PROTOCOL/HANDOFF/ownerとPC対象存在・競合・既登録IDをread-onlyで確認し、差分のみ同期すること。

## Golden計画（設計のみ・NOT RUN）と次回検索

- 同一EXE/DAT/SAVE/map/input/seed観測可否とcapture SHAを固定し、合法ゲーム内で`level`キーに由来する初期ユニットが確認可能なケースを`0`/正値/負値、`class`基準1/高値、scenario modifier有無、`param_3+0xDC`参照有無で可能な範囲だけ区別。初期可視Lv、EXP、スキル、ステータス、保存→ロード後同一性を収集する。非合法なDAT/EXE変造を本指示の下で実施しない。
- 動的到達、`level=0`を実際の原作データが使うこと、`bVar1`の語義、class越境時の継承、EXP+0x16Cの保持/リセット、RNG順序はすべてVERIFY。原作Gameplay actual Golden PASS **0件**、old/new strict MATCH **0件**。
- 次回の許可された軽量調査：`0x582D90`の呼出元`0x466090/0x466B00/0x466F60`の引数・Unit identity、`0x4667B0`の合法caller`0x478F50/0x47CE80`、`0x58AFA0`のclass/skill updateと`0x58A400`閾値作用を局所的に対照し、T011 cross-kindへの適用範囲を確認。新規安全拒否0、B正式READY0、E統合0、Task DONE増0。
