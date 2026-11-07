# B-20261013-1831-02｜T012/T013/T011 属性19種の双系統index一致（保存済証拠限定）
[OWNER/STATUS] 2026-10-13 18:31 JST、T012 primary/T013 T011 reference。READY-STATIC-CROSSWALK（owner HANDOFF readback後のみ）。old Gameplay PASS0 / new strict MATCH0 / Task DONE+0。
[SOURCES] B所有 exe/T013_A18_A1C_CALLBACK_MAP_20261012.txt（登録 VA0x59FA40..0x59FAE3, key table0x65BC60）、exe/T012_ATTR_TABLES.txt（heal key table0x68D420, up labels0x68D470, down labels0x68D4C0）、exe/T012_HEAL_ATTR_PROBE.txt（VA0x5516D0..0x551753）。全て既保存ファイルをDesktop Commander Local read-onlyで照合。新EXE disassembly・原本実行0。
[FACT-1] key table0x65BC60（Skill+0x110 raw attr stringから+A18/+A1Cを0x59FACE/0x59FADCで設定）とheal key table0x68D420（候補local nameを0x55170Bで比較、0x551738でattr index store）は、ordinal 0..18の19件が**全件同じraw name・同じ順序**。比較スクリプト上 count=19/19, mismatch=0, contiguous index=19/19。
[EXACT ORDER] 00 hp,01 mp,02 attack,03 defense,04 magic,05 magdef,06 speed,07 dext,08 move,09 hprec,10 mprec,11 poi,12 para,13 sil,14 conf,15 ill,16 stone,17 fear,18 all。
[FACT-2] heal側に別の同順ordinalテーブル0x68D470（t_*Up表示候補文字列）と0x68D4C0（t_*Down表示候補文字列）も存在する。ただしlabelの見た目は実際の能力変化・Task実作用の証明ではない。
[FACT-3] callback表ではindex11..18の+A18 function pointerはすべて0x599310で共有するが、+A1C filter pointerはindex11..18それぞれ異なる(0x5994A0..0x599580)。+A18 pointer単体からpoi/para/sil/conf/ill/stone/fear/allを逆推定禁止。
[LIMIT] 一致するのはraw key文字列とordinalのみ。0x65BC60と0x68D420は別ポインタテーブルであり、Skill parser入力・heal scratch candidate・比較関数の到達順/SSO、parent inheritance、callbackの実効果、index別対象Unit stateはそれぞれ独立。native key comparisonが全ケース同じ意味・effect callbackが成功することを証明していない。
[DELTA] B-20261012-0108-01はcallback登録表、B-20261013-1814-01はheal側name scanを独立READYにしたが両者のordinal一致は未確定としていた。本IDの増分は既保存2表の19/19 exact correspondence、および+A18のstatus8同一pointerを避ける実装型契約。既知branch/recordは二重計上しない。
[REIMPLEMENT] attr raw key→ordinal lookupを両経路で共通データ定義として再利用可能。ただしSkill+A18/A1C登録とheal候補name解決・HP/stat/status writer、up/down表示、RNG/MP消費、callback returnは別stage/receipt。unknown keyは+ A18/+A1C nullの既知局所分岐とheal no-match→0x551D40分岐を区別し、勝手にeffective attrへfallbackさせない。
[GOLDEN] 原作合法skillで属性hp/mp/attack/dext/poi/all、既知・未知attr、候補0/1/複数、先行chance/MP、同seed可視HP/stat/status/次技能と表示effectを別々に old/new capture：DESIGNED/NOT RUN。表比較の静的整合を原作Gameplay PASS/MATCHへ加算禁止。
[NEXT] T012 551C6A→551E50 once flag/EXP→551C7F flash/callbackとWork既接続551924の後段を参照join。T013 +A1C実条件・対象順位、T011跨種parent遷移、合法Unit付与は別VERIFY。禁止新逆解析0x5710C0..0x571500、4E13F0、4C28D0、4C5CC0、579A20等を別tool/path/shell/Remoteで再試行せず。
[SCOPE] B所有 data/ と HANDOFF 以外は不変更。MASTER/T018/他レーン/REA/dev_lab/Work/Git/原本/設定/schedule編集0。Eのみ正式統合。初回保存後readbackしてHANDOFFへ一意登録する。
[STATUS] READY-CANDIDATE (STATIC CROSSWALK CONFIRMED) / HANDOFF PENDING (CONFLICT) / MASTER NOT INTEGRATED / old Gameplay PASS0 / new strict MATCH0

## B-RC-20261013-1833-HANDOFF-IDCOLLISION-01｜owner HANDOFF競合・未登録の引継ぎ（非READY）
[CAUSE/OBJECT] CONFLICT。2026-10-13 18:33 JSTに別Bの同時実行がevidence/LANE_B_HANDOFF.mdへB-20261013-1831-01（4C3250 rect callee）を登録、同時にHANDOFFサイズ460426→461784 bytes/2243→2248 linesへ変化。自runの初期ローカル文書で同IDを付けたため衝突、B自分所有新文書のみ1831-02へ訂正。別B資料/HANDOFFは編集せず。
[LAST SUCCESS] 本文書はB-20261013-1831-02として保存し、静的19/19対応を既存B exe2資料から検証。旧EXE実行なし。owner HANDOFFへのB-1831-02追記0、MASTER統合0、正式READY0。
[NEXT/RESUME] 同時B HANDOFF writerが終了/排他であることと最新MASTER・HANDOFF末尾のIDを再確認し、同IDの重複がない場合のみB HANDOFFへ本docの限定STATIC成果を追記→読み戻し→Eへ正式統合待ち。競合中はread-only。元拒否済逆解析には再介入しない。
[STATUS] BLOCKED HANDOFF REGISTRATION / NOT READY FOR E / DOCUMENT READBACK REQUIRED / original Gameplay PASS0 / new strict MATCH0

[RECOVERED-20261013-1844 / READBACK] B-RC-20261013-1833-HANDOFF-IDCOLLISION-01: resolved registration only. B HANDOFF readback `## B-20261013-1831-02` & `READY-STATIC-CROSSWALK` confirmed; latest precheck MASTER cp121/430, no E integration. `B-20261013-1831-01` (rect) and `B-20261013-1833-01` (phase) remain other B's separate IDs. Current proof is static19/19, not original Gameplay PASS.
[STATUS] OWNER-HANDOFF READY READBACK PASS / E INTEGRATION PENDING / TASK OPEN / old Gameplay PASS0 / new strict MATCH0
