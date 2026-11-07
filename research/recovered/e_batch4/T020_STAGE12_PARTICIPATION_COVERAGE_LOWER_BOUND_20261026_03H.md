# E-AUDIT-20261026-03H-T018-T020-STAGE12-ROSTER-COVERAGE-LOWER-BOUND-01
Owner E | 2026-10-26 03H JST | T018/T020 | ARCHIVED STATIC REPLAY / VERIFY / NOT READY.
## 出典
PC Local Compactで、rea_lab/headless_analysis/search_index/BATTLE_STAGE12_WAR_SIDE_CROSSWALK_20261022.json（SHA256 9BC09C7EC861C5E21068ADD274534BD88685BAA1AB1EF780C8B1E3BD4B06EB8E）を読み取り専用再利用。保存原作RAW8ファイルの実バイトSHA8/8一致を検証。2セッション別。原作EXE SHA E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187は当時の記録値（本回現物再ハッシュ・実行なし）。
既E 02HのAttackMap/HelpMap非排他的証拠を再加算せず、出撃名簿の**網羅性の数値下界**のみ独立評価。
## 今回のE新規受入差分
各RAWのruntime Troop leader数は[24,24,0]、participation-treeの3entryからside別に確認されたleader record matchは[8+16,8,0]=[24,8,0]。
一つの一致recordが必ず別々のleaderを指すとの保証はないため、match数合計は固有leaderの被覆数の**上界**に過ぎない。従って未被覆leader数の下界は max(0, leader_count - match_count_sum)。
全8 RAWでside0: 24/24→未被覆下界0（網羅性は未証明）、side1: 8/24→**少なくとも16リーダーはこの3entryのmatchだけでは被覆不能**、side2: 0/0（出撃援軍存在を証明しない）。
これは「元の出撃名簿から16が欠落した」という意味ではなく、**この参加treeを原作G2全出撃Troop名簿の代用にすると必ず情報不足**という受入上の証拠。treeはそもそも全Troop列挙のための構造でない可能性がある。原作ゲームのBUGではない。
HelpMap同Spot/side_byte=1の情報から第三runtime sideのTroopを捏造せず、runtime Player/Enemy表示やside indexから攻防援軍の意味役割を自動確定しない。
## 新規E実行結果
E専用 tests/t020_stage12_participation_coverage_lower_bound_20261026_03H.py（SHA256 779AFC0F0F4A8AFAB93DBDE8A28E1975463E356AAB9149473ECD9DCB0C220B01）を新規保存。Windows上のPython unittest 5/5 PASS / failure0 / exit0。
試験はSOURCE SHA・RAW8/8 byte SHA・2独立session、8/8のside1未被覆下界16、仮に照合件数がleader総数と等しい場合も重複可能性によりG2不昇格、HelpMap/third-side非同一、non-atomic/territory names未確認を検査。
同一REA Stage12の数値解釈を監査したもので、独立なnative解読、原作の新規戦闘観測、正しい固有ポインタ結合の証明ではない。8 RAWとも非原子的。新Golden実機試験 NOT RUN。
## E Golden / T019 / 正本
C-NB02合法旧原作 G0(戦闘開始UI/Spot)、G1(同run直前SAVE実bytes/SHA+入力)、G2(実MAP+攻防支援3side+ordered deployed Unit/Troop)は全未充足。G3/G4も未充足。新E DYNAMIC OBSERVED 0 / actual Golden PASS 0 / old-new strict MATCH 0。
T019新確定矛盾0。GameClear DAT13/TXT2字句検索scope RESOLVED、script2同名勝者/phase flag、TXT実load、GameClear後gwriteはVERIFY据置。T020新規5/5はSTATIC replayのみ。
PC MASTER TASK QUEUEを本回直接再計数して34 unique：DONE9 / IN_PROGRESS21 / VERIFY4。最終正式checkpoint196、READY596=A115/B229/C136/D116（既MASTER記載の旧正式値・全READY ID再集計なし）。新規READY正式統合0。B 03H T024はSTATIC/VERIFY/NOT READY、代理採用なし。
旧T018表境界・E session-join/DAT note、C T026/T032、D T030 TSV、禁止0x5710C0、その他安全拒否は別BLOCKED据置、別shell/path/tool/ZIP/Remote迂回0。13H/14H OFFLINE-UNSYNCEDは未正式統合。
本回書込は新規E所有Pythonと本E所有報告書のみ。MASTER/A-D/REA/dev_lab/原本EXE/ZIP/DAT/SAVE/Git/Work/他スケジュール/設定には書込なし。
NEXT: participation-treeのpointer-level固有被覆を証明できても、実入口時点の同一epoch・MAP・role・順序・SAVE/入力/旧合法UIが必要。C-NB02同一原作戦闘一次receiptを最優先し、partial rawの全名簿昇格を禁止する。
