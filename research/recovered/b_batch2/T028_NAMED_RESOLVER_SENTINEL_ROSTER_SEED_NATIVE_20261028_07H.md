# B-20261028-07H-T028-NAMED-RESOLVER-SENTINEL-ROSTER-SEED-01｜戦闘後候補列の自己要素・名前解決失敗時の共有fallback（STATIC/VERIFY/NOT READY）
Owner: B/T028、2026-10-28 07時台。新規正式READY 0 / E MASTER統合0 / Task DONE 0。
## 接続・未同期・出典
- Desktop Commander Local Compact PC ONLINE。MASTERのE正式最終既知cp196/READY596（全件再集計なし）、ANALYSIS_LANES_PROTOCOL、B5 owner、LANE_B_HANDOFF、RECOVERY_HUB、共通運用規則、既拒否・未同期索引を読み取り。2026-10-25 14H旧offline研究全文と他レーン全意味重複は未回収・未照合VERIFY。
- 原作ver0.67 Vahren.exe現物 2910720B / SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。原本をread-onlyで取得。旧search.sqlite README/BUILD_MANIFESTは履歴参照のみ。LATEST指示のV3 search_current.pyの限定function 0x5882F0・0x5916E0を参照。V3 validator PASS_ACTIVE_V3_STATIC、14入力SHA一致、E8直接44889、E9/EB 6324、errors[]、gameplay NOT_RUN。Ghidra再解析なし。
## 今回の新規原作ASMと擬似C照合
- 0x5882F0 はB06H既知0x494931/0x4958C1の候補列ビルダ。Native 0x588317 ESI=output vector、0x58831B EBP=source object、0x588325/327/32Aはoutput begin/end/capacityを0初期化。0x58833B CALL0x4C12F0 capacity準備後、0x588340..349で[output end]=source owner EBPを格納し、endを+4。**名前解決する前にsource自身を先頭候補としてseedする**。
- 元オブジェクト+0xD4/+0xD8の範囲差を0x1C-strideで要素数へ換算（0x58834D..36E / 0x588416..43F）。範囲空は0x58836Eで反復をskipするが上記先頭seedは済んでいる。0x588384..3B4で各0x1Cレコードを文字列として0x402710へ渡し、owner+0x1A4をECXとして0x467DE0で参照解決。EAX!=0なら追加、0なら0x5883C1→0x588416でskip。重複除去の保証なし。
- よって通常成功戻りのoutput候補は少なくともowner参照を含む。全件について重複なし・0以外か、EXE異常時/NULL owner/例外処理は未確認。Ghidra擬似Cには偽装hook ABI警告 verified_abi=0 があり、戻値型や呼出規約の最終固定はVERIFY。
- 0x5916E0 はB06Hの0x494881 caller。native 0x591704/708で入力文字列の+0x24/+0x38をSSO分岐で解決、0x59173B CALL0x402800で文字列準備、0x591746 CALL0x467DE0。0x59174B CMP EAX,EBX（0x591718 EBX=0）→0x59174D JNE0x591799なので命中時はresolved pointerを返す。
- miss（EAX=0）では0x59175C/762の一回限りのlazy init flag [0xB05BFC] を通り0x59176B CALL0x582AA0、0x591775 atexit登録。0x59177D [0xB05BCC]=[input+0xE0]を書き、0x591788/78Eで2バイト状態を0へ戻し、0x591794 EAX=0xB05A28を返す。**通常の名前解決失敗はNULLを上位へ返さず共有fallback実体を返す**ことをnativeで確認。shared fallbackの型/有効期間/属性初期化内容はVERIFY。
- 上位0x494881 CALL0x5916E0の直後0x494886 CMP EAX,EDI / 0x494888 JE0x494899、非一致時0x49488A..95で100-[EAX+0xC4]を減算量へ加算する。06Hには『非NULLなら補正』と暫定記述があるが、実際のASM比較対象はEDI。EDI値と経路での意味を独立確定するまでは『非NULL判定』とは断定しない。名前解決missだけで補正をskipするわけではない可能性が新規重要差分。
## 原作byte独立検証
- 0x5916E0の207B SHA256 064BBAB46A0BEB43BB48033F7E0DF6C73552E7DEFD2838844729FCA6DD5271EB、0x5882F0の375B SHA256 DC4E714FC738312F97ED515A4CF890825683F60C179D67FC7C726CBCF71B42C2。
- PEのE8 REL32を独立再計算：0x494881→0x5916E0、0x59173B→0x402800、0x591746→0x467DE0、0x59176B→0x582AA0、0x5883B4→0x467DE0、0x5883A9→0x402710 = 6/6一致。
## 重複・状態・次回
- B Task指定prefix 5種のdata owner Markdown計320件を文字列検索。新規site 0x588349, 0x5883B4, 0x591794, 0x591783, 0x591746は先行literal0。関数entry 0x5882F0は06H2資料、0x5916E0は06H詳細1資料に既知。06Hのcallee存在／loyal_down・集合5分岐は再採番0、新規差分はSELF-SEEDとMISS-SENTINEL・callsite実CMP EDI。ただし他lane/旧未同期全文の意味dedup未完。
- 追加のOTHER/RECOVERED：初回data/T024_BATTLE_AI.mdを参照しENOENT、正名data/T024_HAKUSHIN_BATTLE_AI.mdを読戻した（RECOVERY-ID B-RC-20261028-07H-T024-PATH-OTHER-01）。Capstone初回0x588368は命令途中の開始位置で誤表示、0x588360からの命令境界で再取得し解消（RECOVERY-ID B-RC-20261028-07H-DISASM-ALIGN-OTHER-01）。どちらも読取段階のみ、新安全拒否0、原本変更0。
- Golden必要条件：無改変ver0.67 EXE、20倍前DAT、同一SAVE/MAP/入力/RNGでsourceの空／単数／複数名前参照、hit/miss、重複、0x5916E0のfallback/EAX、0x494886比較EDI・+0xC4、候補先頭/末尾、loyal_down変化と可視結果を原作実測。DESIGNED_NOT_RUN、原作Gameplay PASS0 / strict MATCH0、STATIC/INFERRED/VERIFY/NOT READY。
- 次回P0：0x494886時点のEDI導出、0x5916E0 fallback初期化0x582AA0後の+0xC4の型と値、0x5882F0のcallerがsourceとoutputをどう処理するか、2番目の一時集合、T028本来の士気敗走/T013 final targeting/T024戦闘AI/T011召喚親/T012 damage。
- 既拒否対象0x5710C0..0x571500、0x58021E..0x580340および拒否済操作の再試行や別path/shell/Remote/ZIP迂回なし。B ownerのみ記録し、MASTER/他owner/REA/dev_lab/原本EXE/DAT/SAVE/ZIP/Git/Work/設定/スケジュール不変更。
