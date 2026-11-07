# CRITICAL 修正：原作実機RB-Treeの色とnilの取り違え

修正ID：BRIDGE-LIVE-20261021-RB-NIL-01。2026-10-21 JST。
対象 original Vahren.exe SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187、PID23272。
状態：実機postbattle heap読取済・v5 corrected decoderの合成10/10と別actor8/8 PASS・postbattle実データDecode PASS・開戦時G1未完成。
正本はBATTLE_BRIDGE_RESEARCH_INDEX.md。原本・DAT・save・他レーン・MASTER・製品コード変更なし。

## 原因：_Colorを_Isnilと誤認
旧 battle_war_tree_snapshot_decoder_20261021.py / detached v2/v3/v4及びStage7 captureはRB-tree nodeのColor offsetをIsNil判定としていた。原作の黒node color1を誤ってnil判定1とみなし、最初の原作実戦で詳細キャプチャ28回がすべて unexpected nil tree node で失敗。ゲームデータ破損ではなく解析器不一致の可能性が高い。

| RB tree | Color offset | IsNil offset | 実機例 |
| --- | --- | --- | --- |
| AttackMap | +0x20 | +0x21 | root黒1/nil0、head黒1/nil1 |
| HelpMap | +0x18 | +0x19 | root黒1/nil0、head黒1/nil1 |
| 内側Def* set | +0x10 | +0x11 | root黒1/nil0、head黒1/nil1 |

旧fixtureも同じ誤ったflag位置で作られていたため旧テストのPASSは実機互換を保証できていなかった。Colorは0/1を取り得るがIsNilはhead判定であり、両者を混同してはならない。

## 認可済み原作からのread-only実証
- 14:37Z頃のafterbattleメモリ：AttackMap2件、HelpMap1件。Attack root0x4886FAA8/Head0x02DA9DB0、Help root0x4BB4DD98/Head0x02DA9DE0で上記色とnilの値が別だった。
- 14:39Z頃のnested Def sets：二つのAttackノードにそれぞれ16件、8件のDef参照、内側のhead/color nilとrootの区別を確認。
- 14:45Z頃の別read-onlyサンプル：AttackMap1件・Def*12件・Help0件を修正版v5が原作実メモリから取得してDecode PASS。
- これは時刻の異なる戦略状態であり、実戦の開始packetを後から復元した証拠とはしない。

証拠：
BATTLE_LIVE_WAR_TREE_DIAG_23272_20261021T143722872063Z.json
BATTLE_LIVE_NESTED_DEF_NIL_23272_20261021T143939355413Z.json
BATTLE_ORIGINAL_WAR_TREE_CAPTURE_V5_23272_20261021T144551063564Z.json
BATTLE_ORIGINAL_WAR_TREE_DECODE_V5_23272_20261021T144551063564Z.json

## 現行推奨版
- battle_native_war_tree_decoder_v5_20261021.py：outer Attack +0x21、Help +0x19、内側Def+0x11をnilとして読み、Colorも独立検査。test_battle_native_war_tree_v5_20261021.py synthetic 10/10 PASS。
- battle_native_detached_capture_v5_20261021.py：元Stage7 read-only captureのnil誤読を訂正した別版。旧資料と旧版の証拠は保持。test_battle_live_capture_v5_20261021.py synthetic8/8 PASS。旧readerは黒root1を含むnative相当fixtureで拒否することも再現。
- battle_native_bounded_transition_watch_stage8_v2_20261021.py：v5 parser/captureを採用し、攻撃mapが残ったままmode2→mode1復帰した場合もscene exitを認識するよう更新。次回の侵攻前に別途ARMEDにして実測する必要あり。**今回は稼働していない**。
- 旧v1/v2/v3/v4、Stage7/旧Watcherは歴史/比較用であり、原作live memory向け現行readerと誤認しないこと。

## 制限と復旧台帳
G0は本物のGameEvent mode2 start/active1/active0/mode1復帰とユーザーの実戦報告を確認。G1開始同フレームの完全packet、実選択MAP・HP/MP/技能・current RNG・VM cursor、G2安全停止、G3元EXEとの外部無変更往復、G4単一native finish、G5戦略Golden、G6異常終了rollbackは未達。
- REC BRIDGE-RC08-NIL-01 RESOLVED：28件旧reader失敗の原因を実原作メモリから調べ色とnilの混同を訂正、新版作成、合成＋実後戦闘tree読取PASS。過去のG1失敗は残しG1完成としない。
- REC BRIDGE-RC08-NIL-02 RESOLVED：新testの補助fixtureでnil変数の定義抜けにより初回10 ERROR。headならIsNil1、通常node0と明示し合成10 PASS。
- REC BRIDGE-RC08-WATCH-EXIT-01 DESIGN-FIX/NOT-NATIVE-RUN：旧Watcherはmode1へ戻ってもattack_count2が残って15分タイムアウト。v2でmode判定を変更し修正ツールのhelpとimport/testは確認。ただし原作戦闘中のv2運用は未実施。
- REC BRIDGE-RC08-REPORT-SYNTAX RESOLVED：本記録の初回JS作成にMarkdown内のバッククォートが混入し構文エラー。ファイル書込前に失敗、通常文字列で改めて正規資料へ記録。未保存発見なし。

## Stage8 validation回復補足
REC BRIDGE-RC08-VALIDATION-COUNT-01 RESOLVED: Stage8初回統合検証は台帳ID期待値を25件と誤って固定したため22/23 CHECK PASS。実台帳はStage6まで19件、Stage7で+5件、Stage8で+6件の計30件で重複IDなし。チェックの基準値だけ30件に訂正し新しいBATTLE_BRIDGE_STAGE8_VALIDATION_V2_20261021.jsonに23/23 PASS、v5 mock18/18 PASSを記録。初回22/23ファイルは歴史的回復証拠として保持。元ゲームや元資料・MASTERは変更なし。

REC BRIDGE-RC08-INDEX-STALE-01 RESOLVED: 最終索引照合で歴史的なBATTLE_BRIDGE_STAGE7_VALIDATION_20261021.jsonを参照していたが実ファイルは存在しなかったため、保存済みのtest_battle_native_detached_capture_stage7_20261021.py（旧合成試験）へ参照を修正。存在しない検証済みJSONを捏造しない。別の索引全体検索ではBATTLE_BRIDGE_FINDINGS_LEDGER.jsonlの部分一致が.jsonという偽陽性を生み、MASTER_LEDGER.mdはsearch_indexでなく研究rootに現存する。実在のStage8新規検証はBATTLE_BRIDGE_STAGE8_VALIDATION_V2_20261021.json（23/23、v5 mock18/18、G0実機真、G1完全pack0）。
