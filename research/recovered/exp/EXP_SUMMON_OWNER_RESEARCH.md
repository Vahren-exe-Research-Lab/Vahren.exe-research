# EXP-SUMMON-OWNER-20261021-1739｜召喚攻撃経験値の所有者追跡（独立研究）
研究ID: EXP-SUMMON-OWNER-20261021-1739。Task: T011/T012参考、E統合は未実施。
状態: STATIC / VERIFY / PC-SAVED-CHECKPOINT-0 / GAMEPLAY-NOT-RUN / NOT-READY。
原本EXE・DAT・MASTER・B HANDOFF・他レーン・製品コードは変更しない。
目的: 召喚した際のEXPと、召喚個体が攻撃した際のEXPが召喚親へ届くかを厳密に区別。
データ源: HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip、前回EXP研究CP04とPC B所有T011関連資料。
2026-10-21 17:39 JST 現PCの Desktop Commander Local に接続成功し MASTER、QUEUE、B HANDOFF を読取。
既知STATIC: ヒット経験値 writer 0x551E50 は攻撃BattleUnit+0x1C8を用い、紐づくUnit+0x16Cへ加算。
既知STATIC: 0x56F880 が BattleUnit+0x1C8、+0x1CC、+0x1D0 を異なる参照として設定。
既知STATIC: 0x57F190 召喚スキル使用時には別に 0x551E50 への呼び出しがある。
重要な未解決: 0x54E7B0 が 0x56F880 第3引数へ渡すUnit identityの全分岐。親と同一か、独立の召喚Unitか。
注意: +0x1CCを親参照と見ても+0x1C8と同一と推論不可。「必ず親に経験値還元」は未立証。
既存PC: data/T011_SUMMON_RUNTIME_UNIT_56F880_CONTRACT_20261013.md と data/T011_EXP_LEVEL_INIT_RECALC_OFFLINE_20261021_0309.md を確認。
既存B証拠との重複照合は継続、同一証拠を新規READYとして再計上しない。
次: callsite別Unitポインタ生成、lookup/new Unit、EXP加算分岐、kill/cleanup、DAT召喚定義と突合。
RECOVERY: 中断時は本ファイル末尾・独立ZIP報告・直前チャットを参照。PC同期は本独立ファイルのみ。

## CP01 / 2026-10-21 JST：生成・経験値write・グループ参照の静的証明
[STATIC-ASM] 0x54EE7Fで召喚処理がeffect+0x7Cから召喚者BattleUnitを取得、ECX=thisの0x54EE82→0x577260を呼ぶ。
[STATIC-PSEUDOC] 0x577260はBattleUnit+0x1E4B8をsentinelとする検索結果を返す（命中はmap node+0x28、失敗0）。
[STATIC-PSEUDOC] 新BattleUnit constructor 0x56F880は各インスタンスの+0x1E4B8探索ツリーを初期化する。
[STATIC-ASM] lookup missでは0x54EF37 xor ecx,ecx → 0x54EF3E call0x58B7F0で新Unit値を生成し、0x54EF69 call0x577310で召喚者のtreeに登録する。
[STATIC-ASM] 0x5773E6 call0x577260の返値EAXをESIへ保持し、cleanup 0x577400の後に0x577405 mov eax,esiで返す。
[IMPORTANT-DECOMP] 0x577310のGhidra擬似Cはvoidと表示されるがx86実コードはEAX=lookup結果をreturnする。戻り型の誤推定に注意。
[STATIC-ASM] 0x54F06D〜0x54F07Aでgroup等の6引数をpushし新Unitを第三引数として0x56F880へ渡す。
[STATIC-ASM] 0x56FEAF BattleUnit+0x1C8=第三引数Unit（攻撃時の経験値加算先）。0x56FEBB +0x1D0=第六引数group。
[STATIC-ASM] 0x56FEC1〜0x56FEE3: +0x1CCはgroup nullなら0、groupが空なら第三引数Unit、既存子があれば先頭子の+0x1C8へ設定。
[CORRECTION] 従って+0x1CCは親へのEXP送金先でなく同一groupの代表Unit候補。summoner Unitと等しいとは限らない。
[STATIC-PSEUDOC] 0x551E50はBattleUnit+0x1C8のUnit+0x16CへEXPを加算。+0x1CC経由の加算はこの関数にない。
[STATIC-ASM/PSEUDOC] 同関数は+0x1D0==0、+0x18614!=0、skill exp_per=off、hit context重複フラグ等で付与しない。
[STATIC] 0x54E7B0はgroup mode=0で第六引数group=0にする分岐を持つ。新生召喚Unitでも経験値獲得が保証されない。
[STATIC-CALLER] 0x577260直接callerは0x547490/0x54E7B0/0x553390/0x577310の4つ。生成と検索の同種機構が複数経路に存在。
[LIMIT] 戦闘終了後のEXP親転送/Unit値生存期間/同名召喚キー寿命/特定DATにおけるgroup mode到達は未確定。
[RESEARCH-CONCLUSION] 召喚発動自身のEXPが親へ入る道と、召喚子の攻撃EXPが子Unitに入る道を区別。無条件親還元説は棄却候補（原作Gameplay未実施）。
[VALIDATION] 元EXE実行0・変更0。静的x86と検索SQLite/Ghidra codeの照合のみ。B READY/E統合/DONE/Gameplay PASSいずれも追加0。
[RECOVERY] 追加証拠は独立クラウド派生のCP11 report、Wiki補助資料と相互参照。PC保存のreadback後にcheckpointを昇格する。

## RECOVERY EXP-RC-20261021-PC-WIKI-PARTIAL-01 / SAFETY_REFUSAL / BLOCKED
2026-10-21 JST。EXP_WIKI_DRAFT_PC_20261021.mdの作成は第1部分29行、第2部分24行までwrite_file成功。第三部分appendがOpenAI安全性チェックで拒否。
拒否された内容はPCへ未保存。第四部分は未試行。拒否内容を別tool/path/shell/Remote/分割で再書込しない。
既存PCのWiki草稿は部分ファイルであり不完全。公開・統合・Wiki投稿に使用禁止。
独立した完全版草稿は過去オフライン成果HAKUSHIN067_EXP_WIKI_RESEARCH_20261021.zipに含まれる（PC未同期）。
EXP_SUMMON_OWNER_RESEARCH.mdのCP01は別の先行成功で保存/読み戻し済み。失われた証拠として扱わない。
新たな合法的許可・承認が明示されるまでは、このWiki追記をBLOCKEDとする。
他レーン/MASTER/Git/旧EXE/Workは変更なし。今回追加GamePlay Golden PASS=0、B READY=0、E統合=0。

## CP11 成果物・次回再開契約 / 2026-10-21 JST
[PC CONFIRMED] CP01静的証拠の保存と別read_fileによる確認を完了（計36行時点）。本RECOVERY追記も独立readback済み。
[EXE] 同梱Vahren.exeのSHA256 = E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
[SQLITE] 機械解析search.sqlite SHA256 = 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF。
[ARCHIVE] CP11新報告・元x86狙い窓・6擬似C・SQLite呼出表を独立ZIP HAKUSHIN067_EXP_SUMMON_CP11_20261021.zipへ保全。ZIP CRC PASS。
[WIKI] 既存のWiki全文草稿 HAKUSHIN067_EXP_WIKI_RESEARCH_20261021.zip は独立オフライン成果として存在。PCの部分Wikiコピーには拒否記録があるため公開しない。
[NEXT TEST] 親EXP→召喚行為のみ→子の攻撃→親EXP→戦闘終了→再召喚を別々に採取。group null/非null・同名再召喚・異名召喚を比較。
[NEXT RESEARCH] 0x577310の生成キーと保存寿命、戦闘終了時のツリー解放/転送有無、実DAT召喚モードを調べる。禁止済操作の迂回はしない。
[STATE] CP01 PC-SAVED-READBACK。原作Gameplay Golden 0、Wiki未公開、他レーン正本への正式統合0、研究成果の検証継続。
