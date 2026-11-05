# E-AUDIT-20261028-00H-T020-T028-BATTLE-CONFIG-MODE-GATE-01
[OWNER/STATE] 研究E T020、2026-10-28 00時台JST。STATIC / SYNTHETIC EXECUTED / VERIFY / NOT READY。正式READY追加0。
[ACCESS] Desktop Commander Local Compact接続成功。MASTER TASK QUEUE/PROTOCOL、A-D HANDOFF、REA PROGRESS、DEV計画、E T018/T019と2026-10-21索引README/manifestをread-only確認。
[SOURCE B00] B-20261028-0014-T028-BATTLE-MODE-CONFIG-PRODUCER-01、data/T028_BATTLE_MODE_CONFIG_PRODUCER_NATIVE_20261028_00H.mdの実バイトSHA256 D6708901880A1E7C85BE81C542027506546E443EDAF377E5E88577E4BB87AA36（新T020 pin照合PASS）。
[SOURCE B23] 既知 data/T028_COUNT_QUEUE_MODE_BRANCH_NATIVE_20261027_23H.md SHA256 8C7354AB542866963C555805C04BDDB2790F2B1E88D3570EB702F2C36FF7FB17（同pin照合PASS）。22H死亡queue清掃/B23H mode consumerは既知・再READY計数0。
[NATIVE PROVENANCE] 原作EXE SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187、B保存PE 0x490A83..0x490AB0 window SHA A34ED7E0B7F3043F262E4D271E82EB52956DD5E367ECE3BB34B74226D21D5F54、E8 4/4、V3 callers 3/3はBのSTATIC結果継承。E側で原作EXE/DBを再ハッシュ・逆解析していない。
[MODE SELECTOR] 0x565BA4 player_battle既定1、0x565BE2 enemy_battle既定0。明示entry+0x1C非0は1、0は0。0x490A83 AL==0かつmanager+0x1EED55==0なら mode=NOT enemy_battle（0x490A98）、それ以外mode=NOT player_battle（0x490AAA）。
[NEW E TEST] tests/t020_t028_battle_mode_config_producer_gate_20261028_00H.py。実バイトSHA256 FBE10DD49AAF70943A4BD33777FF87A76E9D61508EAEF8A77CEB6C58CEEE3DB6。新規21/21 PASS、既存23H 19/19 PASS、合計40/40 PASS、両Python終了コード0。
[NEGATIVE CASES] 設定未指定と明示0、敵/味方設定の独立性、4通りのon/off、非0負値、raw不正・範囲外・unknown、AL/flag不明、source manager異値、同pointer別run、管理者同一性が合成値だけのケースを分離。
[ORDER / BOUNDARY] 合成mode0はFadeOutSheet候補、非0は後続event候補。前回23Hの局所 mode書込→死亡queue清掃/空skip→mode branch を両modeで保持。ただしwriter(0x490590)実到達、0x491870経由でconsumerに届くinstance/epoch同一性、AL上流意味、manager+0x1EED55論理名はVERIFY。合成したsource/manager同値を実戦同一性に昇格させない。
[IMPLEMENTATION CROSSWALK] strict実装時、{config raw/absence, compiled boolean, AL/manager flag, selected source, mode-write, queue clear, mode branch, battle epoch}を個別nullableなtraceにする。静的なmode0を勝敗/経験値/死亡イベント実作用と同義に扱わない。dev_labへの直接修正・受領確認なし。
[T018 LEGAL] C-NB02 G0=合法原作UI・Spot・入力、G1=同一runの直前SAVE bytes/SHAと操作時刻/入力、G2=実MAP、攻防援軍三side、ordered deployed Unit/Troopを別byte receiptで結ぶ。G3可視終戦・G4戦略World差分も別に採取。settings/config snapshot SHAを補助にし、internal manager識別が合法UIで採れなければINELIGIBLE。x20変更後DATを未改変strict Goldenと混同しない。
[GOLDEN] E原作 gameplay DYNAMIC OBSERVED新規0／actual Golden PASS0／strict MATCH0。BのSTATIC・E合成PASSを実原作の観測に換算しない。
[T019] 新規確定矛盾/原作BUG0。GameClear DAT13/TXT2字句scope差RESOLVED維持。script2同名優先/phase flag/TXT runtime load/gwrite復帰はVERIFY。
[MASTER COUNT] 今回MASTER TASK QUEUE34行を独立再集計：ID unique34、DONE9/IN_PROGRESS21/VERIFY4。最終既知正式checkpoint196・READY596=A115/B229/C136/D116は旧正式値（全READY履歴再集計なし）。B00はNOT READY、E正式統合IDなし、MASTER追記0。
[SAFETY] 旧T018表境界/session-join、T019 XREF、C T026/T032、D T030 TSV、0x5710C0、他の拒否操作はBLOCKED継承。新規拒否0、旧拒否別shell/tool/path/Remote/ZIP再試行なし。旧OFFLINE-UNSYNCEDとB10/25全文dedupはVERIFY・未統合。
[WRITE SCOPE] E所有testsの新規Python/本記録のみ。原本EXE/ZIP/DAT/SAVE、A-D/REA/dev_lab、Git/push、Work、設定・自動化変更なし。
[NEXT] 許可済み合法原作G0/G1/G2同run byte receiptを最優先。次点はBのAL producer/manager flag writerと同一instanceの一次証拠、実装側nullable traceの一対一照合。新T020結果はNOT READYのまま維持。
[READBACK RECEIPT] Local Compact read_multiple_filesで新規Pythonと本報告を2/2独立読戻し成功。PC Get-FileHash実バイト照合: コードFBE10DD49AAF70943A4BD33777FF87A76E9D61508EAEF8A77CEB6C58CEEE3DB6、本追記前の報告60A48452666E8BF0711447C2AD0CBDFBA74BDBFABCB4527539A5472D358C6AB9。追記後報告SHAは変化。新規安全拒否0/未保存差分0。
