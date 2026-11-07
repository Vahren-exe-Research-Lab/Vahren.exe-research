# E-AUDIT-20261026-01H-T018-T020-V7-TROOP-MEMBER-EPOCH-CLOSURE-01
Owner E / T018,T020 | 2026-10-26 01H JST | PC Local Compact | ARCHIVED ORIGINAL RAW REPLAY + VERIFY / NOT READY.
## 出典と今回の独立したE受入成果
旧EXE識別SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（RAW申告；本回旧EXE再ハッシュ・起動なし）。
read-only source: rea_lab/headless_analysis/search_index/BATTLE_STAGE11_CROSSRUN_ANALYSIS_20261022.json（今run現物SHA256=DC65D29948A1E5057ACF2BC40CB54539F9C3AEC42B8B05413838DE425E039ADB）。
decoder source: battle_native_war_tree_decoder_v5_20261021.py（SHA256=0DD7C9EBD0BF97E4BA421FEC02909A44A9B6ABDA4A3538239B479530D909EB6A）。REA既存デコーダをread-only import、原作メモリ/REA文書を書かない。
E所有の新規 t020_v7_troop_member_epoch_guard_20261026_01H.py が2別PID（28432/32468）のRAW 4+4件について、各SOURCE SHA8/8を照合し、保管RAW実バイトからdecode_fullを再実行。旧Stage11とUnit/Troop人数・Troop-member/side-roster照合結果が8/8一致。
## 具体的な証拠差分
第1原作戦闘: side Unit refs [192,192,0]→[377,192,0]、Troop個数は全4記録[24,24,0]。
第2原作戦闘: side Unit refs [192,192,0]→[377,200,0]、Troop個数は全4記録[24,24,0]。
第2戦闘の最終RAW_05（元SHA=72FF106B32D2AF20384685A0F45D8DB587EE5EFC9F3F93C75F43E31EB77A3108）のみ、decoder集計で「Troop membersに存在するが対応side rosterには無いポインタ」が[0,3,0]。他7 RAWは[0,0,0]。
**E受入上の増分**: Troopの個数が変わらないこと、初回だけmember closureが0であること、また後続RAWに構造が存在することを、戦闘入口の「確定ordered出撃Unit/Troop」と同一視してはならない。
全8 RAWでtask counterが取得前後に変化し stable_guard=false、selected_map_sha256=null、original_gameplay_verified=false。3件の食い違いの原因が途中召喚/死亡/並行更新/デコーダ誤解釈のいずれかは未確定、原作BUGとはしない。
原作実機の新規戦闘実行は0。REA Stage11の既知データをEが同一decoderで再検証した成果であり、独立実装によるデコーダ正当性証明や新規原作観測ではない。
## T020実行結果・保全
E新規Python unittest 6/6 PASS・FAIL0、保存RAW 8/8 SHA一致・8/8既存Stage11デコード照合・約0.535秒。検証器は既存REAの読み取り専用再利用のみで、Golden comparatorや原作/デコーダを変更しない。
Code SHA256=E63C6D43FAC0A7D2E8E5F82745A3721405C7DFAD6B2E7CDDE13C650A43EAA841。今回新規READY正式統合IDなし。検証器保存/再実行成功。本報告書も保存後readbackとSHAを確認する。

## Golden/T019/MASTER/安全境界
E G0=C-NB02旧合法sci1/po2/sp2→sp16旧UIとnative Spot ID、G1=同戦闘直前SAVE実バイト+入力、G2=実MAP/攻防支援三陣営/ordered deployed Unit/Troop、G3=戦闘結果、G4=戦略World差分。全てNOT QUALIFIED。
既存REA LIVE ORIGINAL RAW部分観測は維持するが、**今回の新規E DYNAMIC OBSERVED=0 / actual Golden PASS=0 / strict MATCH=0**。REAL original captureを合成PASSやE Golden受入と混同しない。
T019新確定Wiki/DAT/EXE矛盾0。GameClear DAT13/TXT2 lexical scopeは既RESOLVED。script2重複優先/phase flag/TXT runtime load/GameClear後gwrite復帰はVERIFY、今回原本再実証なし。
PCのMASTER TASK QUEUEを今回直接再集計: 34 unique / DONE9 / IN_PROGRESS21 / VERIFY4。最終正式checkpoint196 / READY596=A115/B229/C136/D116はMASTERの既存値（READY ID全件再集計は行っていない）。B-20261026-0115-T024の所有者HANDOFFはSTATIC/VERIFY/NOT READY、新規代理統合0。A/C/Dの旧READYを重複計上しない。
旧安全拒否T018表境界、E session join/DAT/旧Stage15、C T026/T032、D T030 TSV、禁止0x5710C0等はBLOCKED維持。今回拒否済操作の再試行/別tool/path/shell/Remote/ZIP迂回0。13H/14H OFFLINE-UNSYNCED未正式統合。
今回のPC書込はE所有Python検証器と本報告書のみ。MASTER/A-D/REA/dev_lab、原本EXE/ZIP/DAT/SAVE、Git/push、Work、他スケジュール/設定は変更0。原作GAMEPLAY新試験NOT RUN。新安全拒否・PC接続障害0。
NEXT: E新fixture受入器では、変動するUnit refsと固定Troop個数を別証拠型にし、入口時刻のordered member一覧・side role・MAP SHA・合法UI操作/SAVE入力の真正性を原作同一戦闘で取得する。原因不明のmember差を自動修復/欠落0埋めせずVERIFY。新たなREADYが来た場合だけowner/readback/hash/ID競合照合のうえ一度正式統合。

## RECOVERY E-RC-20261026-01H-T020-LOCAL-PREFLIGHT-OTHER-01
種別OTHER/RECOVERED。初期raw schema探査でnative_sides.unit_ptrsをlistと仮定しTypeError（実型はcount int）、次の限定読取で構造を確定。MASTER Task集計の初回正規表現はshell escape誤りで不可能な15789件を出力したため未採用、行分解方式で34 unique/DONE9/IN_PROGRESS21/VERIFY4を再計算。SHA集計初回のraw Windows末尾backslash引用はSyntaxError、末尾区切りを除き再実行成功。全3件ともローカルread-only補助コマンドの初回失敗で、安全拒否・接続障害ではない。書込未発生の診断にとどまり、最終検証6/6 PASSと2資料保存/readback/SHA成功を確認。既拒否操作の代替・再試行には該当しない。
