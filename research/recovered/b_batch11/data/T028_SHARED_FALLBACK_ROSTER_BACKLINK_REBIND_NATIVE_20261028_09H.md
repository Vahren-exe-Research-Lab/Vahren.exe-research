# B-20261028-0913-T028-FALLBACK-ROSTER-BACKLINK-REBIND-01｜T028共有fallbackの空候補範囲とmiss時のowner再束縛
Owner: B / T028。2026-10-28 09時台。STATIC-ORIGINAL-PE-ASM / STATIC-GHIDRA / INFERRED / VERIFY / NOT READY。新B正式READY0、E MASTER統合0、Task DONE0。
## PRECHECK / source
- Desktop Commander Local Compact PC接続。MASTER最新正式既知 checkpoint196・READY596（再集計値ではない）、規約、B5 owner・LANE_B_HANDOFF・安全拒否/未同期/回収索引、旧search README/manifestを読取。旧2026-10-25 14H offline全文・他owner完全意味重複は未照合VERIFY。
- 原本 rea_lab/targets/hakushin067_Vahren.exe はread-only。2,910,720B SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。旧search.sqlite immutable mode=ro quick_check=ok。Ghidra再解析・ゲーム実行なし。
## DELTA / native
- 0x582AA0一般オブジェクト初期化: 0x582ACA `xor ebx,ebx`; 0x582B1C `mov [esi+0xD4],ebx`、0x582B22 `[esi+0xD8]=0`、0x582B28 `[esi+0xDC]=0`。名前関連可変配列らしいbegin/end/capの初期範囲が空。元オブジェクト型と配列意味はVERIFY。
- 同初期化で 0x582CD4 `mov [esi+0x1A4],ebx`、0x582D11 `mov [esi+0x1D0],ebx`。+0x1A4のconstructor既定値は0。既08Hの+0xC0/C4=100初期化と同じ成功経路だが再計上しない。
- 0x5916E0 miss は既07Hの初回fallback確保を使用。0x591762 `push 0xB05A28`→0x59176B E8→0x582AA0。続く共通miss処理0x59177D `[ebp+0xE0]`→0x591783 `[0xB05BCC]=eax`、0x591788 `[0xB05A9C]=bl`、0x59178E `[0xB05A9F]=bl`。0x591718の`xor ebx,ebx`からBL=0を引き継ぐ。
- アドレス算術を原本ASMと照合：0xB05BCC=0xB05A28+0x1A4、0xB05A9C=base+0x74、0xB05A9F=base+0x77。よって fallback+0x1A4はconstructorで0にされた後、**初回・再使用を問わずmissごとに入力+0xE0由来へ上書き**される。+0x74/+0x77はmiss時0に戻る。
- 07H既知の0x5882F0はsource自身を候補へ先頭追加し、source+0xD4/+0xD8を巡回。今回の増分はfallback初期配列が空であることと、missで+0x1A4だけが再束縛されるという初期化→再利用時系列。fallbackが0x5882F0へ入力される実到達は未確認であり、常に候補1件とは断定しない。
## DIRECT REFS / boundary
- 旧Ghidra検索DBのdata_refsで0xB05A28への直接参照は0x591762/0x591794の2site、0xB05AEC(共有fallback+0xC4)直接refは0。これは抽出済み静的直接参照の範囲限定であり、+0xC4への間接/alias writer不存在の証明ではない。
- +0x1A4の正式なゲーム意味（所有/参照先）・input+0xE0の型、再使用中のalias/backlink影響、+0xD4/+0xD8の後続writer、+0xC4の間接writerはVERIFY。
## VALIDATION / dedup
- 原本0x582AA0先頭746B SHA256 C1207A014FBDC753EDA726A9C25AF4988BBAE14F2ACDA6B27FD31BE78E171DA3。原本窓 0x59177D/27B SHA A9FB8639BA6866BCBD8CF432AB511C4B475EB2B5D783B228549BBC62FB4D215A。
- E8 REL32原本再計算 0x59176B→0x582AA0、0x5883B4→0x467DE0 は2/2一致（CALL自体は既知で今回新規計上0）。新たなoff site 0x582B1C/0x582B22/0x582CD4/0x582D11の命令をx86-32 CapstoneとGhidra擬似Cで独立照合。
- B所有T011/T012/T013/T024/T028 MarkdownとHANDOFF計323ファイルの新site 0x582B1C/0x582B22/0x582CD4/0x582D11は各先行literal0。0xB05AECの旧記録3件と既07/08Hのmiss sentinel、C4既定100・backlink writerは再計上しない。10/25 offline全文・他レーン意味的全非重複はVERIFY。
## GOLDEN / scope
- 無改変原作ver0.67 EXE＋20倍強化前DAT、同一SAVE/MAP/入力/RNGで連続miss(A→B)、hit、fallbackの先頭候補生成有無、+0x1A4再束縛と可視効果を合法観測するまで DESIGNED_NOT_RUN。旧Gameplay実測PASS0、strict MATCH0。
- 本runはB owner T028資料とLANE_B_HANDOFFだけ書込。MASTER/他lane/REA/dev_lab/原本/Git/Work/設定/スケジュール不変更。既拒否VA0x5710C0..0x571500、0x58021E..0x580340・旧拒否操作の再試行/迂回0。新安全拒否0。前段SQL Python引用符失敗1件は OTHER / RECOVERED（別途HANDOFFへ）。
## NEXT
- 0x5916E0返値のconsumerで共有aliasの+0x1A4を読み戻す位置と、0x5882F0に実際にfallbackが到達するかを優先。+0xC4 indirect writer、T028本題士気敗走、T013最終target、T024 AI、T011召喚親子、T012状態/RNGはP0/VERIFY。
