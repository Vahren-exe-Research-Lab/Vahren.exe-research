# B-20261029-T011-T012-EXP-TRAINING-DEATH-NATIVE-CROSSWALK-01｜経験値・死亡補正・訓練閾値の原作横断照合
[OWNER/STATUS] T011 primary / T012 crossref。2026-10-29 JST。STATIC ORIGINAL PE / INFERRED / VERIFY / GAMEPLAY_NOT_RUN / NOT READY。
[PRIMARY] 原作解析コピー rea_lab/targets/hakushin067_Vahren.exe。今回実SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187、実行・改変0。
[INDEX] 統合V9 HAKUSHIN067_UNIFIED_V9_20261023.sqlite を明示的にread-only検索。現行V3 default・search.sqlite・MASTER・REA・他laneは無変更。
[PRECHECK] Desktop Commander Local Compact 接続成功。MASTER checkpoint196/READY596（最後の確認値）、規約・B HANDOFF・B owner資料・復旧索引を先読。
[RECOVERY] B147件は同名PC存在、93件サイズ一致/54件末尾1B差（完全byte同一性VERIFY）。既安全拒否8件と10/25未発見資料を保留。禁止済本文・コマンドを再投入せず。

## NEW-01｜死亡後累積経験値に直接掛ける設定は dead_penalty
[SOURCE DAT] data/normalized/hakushin067_core/a_default/script/context.dat L110: dead_penalty = 95。これは原文直接指定で、正規runtime読込/上書き順は未実機。
[SOURCE ASM] 0x588D6E MOV EDX,[EBX+0x1A4]、0x588D74 PUSH 0x32（設定欠如時fallback 50）、0x588D76 PUSH EDX、0x588D77 MOV ECX,0x62723C。
[STRING READ] 元PE内0x62723CのASCII C文字列=dead_penalty。0x588D7C E8 CALL 0x46F4C0で設定値取得。元PEの当該native直接CALLとV9 refs-from 0x588D7C→0x46F4C0のGhidra参照一致。
[NATIVE FPU] 0x588D85 FILD 設定値、0x588D8F FMUL double[0x63B070] (0.01)、0x588D95 FILD [EBX+0x16C]（累積EXP）、0x588DB3 FMULP。
[ROUND/WRITE] 0x588DC5 FADD double[0x63B050] (+0.5)、x87 CWへ0xC00 OR、0x588DD2 FISTP qword→0x588DE0 MOV [EBX+0x16C],ECX。
[NUMERIC] 非負/通常表現可能範囲では新EXP=floor(旧EXP×dead_penalty/100+0.5)。95の設定下で例:1000→950。死亡により経験値が一律0になる処理ではない。
[ENTRY-GATE] FUN_00588470 Ghidra擬似CではUnitData+0x77または+0x75が真の経路内で先にEXP閾値判定を行い、この係数処理へ続く。全Unit/全死亡で必ず到達は未証明。
[SEGMENT HASH] 原本VA 0x588D6Eから121byteのSHA256=998FB5293D12BCAF2BA07A407580821F9379943C26E2CC377EEAE914F45EC724。原作ゲーム内EXP観測0。
[NOTE] 通常Wikiの別作品/版の死亡ペナルティ割合を、このver0.67のdead_penalty=95経路と混同しない。

## NEW-02｜訓練の閾値強制は通常獲得ADDではなくMOV
[SOURCE ASM] FUN_00471E80内0x4723C1 MOV EAX,[ESP+0x20]→0x4723C5 TEST→0x4723C7 JLE 0x4723E6。正の回数のみloop。
[DIRECT] 0x4723D0 MOV EDX,[EBP+0x170]（次閾値）→0x4723D8 MOV [EBP+0x16C],EDX（累積EXPを閾値にセット）。
[CALL] 0x4723DE E8 CALL 0x58A650でレベル更新、0x4723E3 DEC ESI→0x4723E4 JNE 0x4723D0。V9 callersでも0x4723DE→0x58A650独立verified。
[CONTRACT] この箇所は通常戦闘の0x551FB2 ADD [R+0x16C],gainとは異なる。設定回数だけ試行する候補だがレベル上限などで必ず回数分上がるとは言えない。
[SOURCE DAT] scenario1.dat L30とtuto_scenario.dat L81に training_up = 2 の直接指定。0x4723C1の回数がこの値由来かは未追跡、接続はVERIFYに留める。

## VERIFIED REUSE｜既存の共通経験値系4caller・直接レベル更新3caller（新発見として再加算しない）
[EXPHIT] V9 `callers 0x551E50`: 0x547A8C（簡易召喚者発動）, 0x551167（攻撃）, 0x551C6A（回復）, 0x57F4E9（通常召喚発動者）。直接E8は4site、未知の間接呼出を除外しない。
[LEVEL] V9 `callers 0x58A650`: 0x4723DE（訓練）, 0x4AB49B（命令/イベント候補）, 0x551FD3（命中EXP）。直接E8は3site。
[GATES] 0x551E50のSkill+0x2A8=off sentinel、actor+0x1D0 NULL、actor+0x18614!=0、context+0xC!=0によるearly returnを再読。context+0xCは獲得計算前に1へ。
[RATIO] 対象+0x185FCが基礎報酬、攻撃の分母は対象UnitData+0x178。ceil(base×ratio)→数値exp_per二次丸め。heal kind3=2%、summon kind4=1%の固定枝は旧EXP研究の証拠を参照。
[INPUT SPLIT] 0x550E70のHP変更ECXとEXP入力EDIは独立。0x551490の回復上限超過はEXP入力EBXと別。旧EXP CP22/23の再計上なし。
[OVERFLOW] 0x551FB2のEXP加算はこの命令ではuint32飽和なし。0x58A400の閾値はoverflow飽和あり。旧CP17/18の再計上なし。
[LEVEL] UnitData+0x168 level / +0x16C EXP / +0x170 next threshold。0x58A650即時SimpleUnit、0x575110通常Unitの遅延処理。11field再計算及び0x58AFA0 skill/property刷新は未完全動的確認。
[SUMMON] 0x54EE82→0x577260 parent+0x1E4B4 cache、miss 0x54EF3E→0x58B7F0および0x54EF69→0x577310、0x54F07A→0x56F880 child+0x1C8=cache R。子RへのEXPと発動者EXPは別。
[LIMIT SUMMON] 同一owner/同一add/add2キーでR共有し得る。破棄0x570C90→0x543E00→0x5450C0→0x5454D0→0x4591F0。ただし戦闘終了前にR→親恒久EXPへの精算がある/ないは未解明。
[GOLDEN] 原作そのもののゲーム起動・新規採取・可視EXP画面比較0。Golden PASS0 / strict MATCH0。モデル例およびnative readbackはGameplay PASSでない。

## 受入試験 / 境界 / 次の検索
[GOLDEN-1] 同一原作EXE/SHA、未改変DAT/SAVE/MAP、操作/乱数で死亡前後のEXP・Lv・次閾値・復活後保存ロードを観測。dead_penalty=95の枝到達確認、親子/通常型を区別。
[GOLDEN-2] 訓練回数0/1/2、Lv上限前/上限時、再計算後EXP/Stats/Skillの各段階の前後を観測。training_up=2との実caller由来はまず静的に確認。
[GOLDEN-3] 通常召喚1回/同キー2回/異キー、子攻撃EXP、親発動EXP、子先死亡・親先死亡、戦闘終了直前/直後/次戦闘の同一性を収録。
[P0 NEXT] 0x4723BCの先行処理→[ESP+0x20]回数のwriter・training_up parser、0x588D7C条件の上位呼出と別補正、0x4AB49BイベントLv更新、R寿命/戦闘出口の精算をREAD ONLYで追跡。
[DEDUP] 旧EXP CP01〜25、REA P0_SUMMON_EXP_OWNER、T011のlevelup既報は既知として引用。新規差分はdead_penalty=95の元DAT×0x588D7C native設定×EXP書戻しおよび訓練0x4723D8 MOV/0x4723DE level callの対照。
[PROVENANCE] Ghidra V9 refs-from 0x588D7Cも一致（direct CALL 0x46F4C0）。機械語x86は原本EXE実バイト読取のみ、ゲーム未実行。
[SAFETY] 他owner/MASTER/REA/dev_lab/Git/設定/automation・原本EXE/DAT/SAVE無変更。過去安全拒否資料の別経路迂回なし、新拒否なし。
[STATE] STATIC/INFERRED/VERIFY/NOT READY。B新正式READY0、E MASTER統合0、Task DONE0。次回再開時まずPC最新正本、重複、未同期、安全保留を再照合。

## CORPUS ADDENDUM｜原作DAT直接指定のEXP曲線パラメータ（10/29、既存level計算の新しい実データ照合）
[KEY BYTES] 原本EXE 0x627620 ASCII='exp'、0x627624='exp_max'、0x62762C='exp_mul'。0x58A400の閾値更新Ghidra擬似Cはこれらの設定を読み、UnitData+0x170へ累積次閾値を構築する。
[MECHANISM] 通常非負・オーバーフローなしのモデルでは、レベルごとの増分を前増分×exp_mul/100で丸め（exp_max>0なら上限）、次累積閾値へ加算する。原本FPUや32bit境界は既存EXP CP17/18のVERIFYを継承。
[DIRECT DAT COUNT] a_default/scriptの590 DAT内、行頭コメントを除く正規表現 ^\\s*exp_mul\\s*= の直接指定491行。内訳は130=234行、125=207行、140=15行、252=8行、150=7行、@=6行、187=3行、120=3行、9999=2行、105=2行、2525=2行、115=1行、3777=1行（計491）。
[BOUNDARY] 同じ名前の複数宣言やDAT継承・上書き前のsource行集計であり、491ユニットの実効値/ランタイムでの頻度ではない。各キャラの確定成長率をこの総計から推測しない。
[NEW/DEDUP] 本addendumの増分はMOD ver0.67原文491行の直接値分布と、原本文字列0x627620/0x62762Cとの照合。0x58A400の閾値式自体は旧EXP CP17/18既報として新規READYに再計上0。

## 操作障害と回復記録｜2026-10-29 JST
[ERR-V9-CLI-01] 統合V9検索に strings dead_penalty --limit 15 を試行→argparse invalid choice: strings。当該CLIはstrings非対応。対応 search dead_penalty は0件（検索できた文字列なし）で、許可済み原本PE読取による0x62723C文字列と0x588D77 ASM照合を行った。安全拒否でない。
[ERR-V9-CLI-02] callers 0x46F4C0 --limit 500 は上限1..200でargument error。--limit 200へ正常化し274件中200件を返却。個別 refs-from 0x588D7C は同site→0x46F4C0を確認。callers上位200件だけでsite不存在とは判定しない。
[ERR-PREFLIGHT-03] 検索索引直下のactive.lock及び新規作成予定の研究資料パスの事前statはENOENT。高負荷/lock不在を全PCへ一般化しない。保存前新規資料不存在は想定内で、その後許可B-owned dataへ通常作成・保存した。
[CLASSIFICATION] 上記は工具/探索条件・存在確認エラーでSAFETY_REFUSALではない。既安全拒否に対する別tool/shell/path迂回0。新規研究本文はPC B担当3ファイルへ保存・独立readback完了。次回はV9対応modeと1..200 limitを遵守。
