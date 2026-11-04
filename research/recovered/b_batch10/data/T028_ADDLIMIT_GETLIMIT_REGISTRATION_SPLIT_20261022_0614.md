# B-20261022-0614-T028-LIMIT-REGISTRY-01｜addLimit/getLimitを別の登録経路として静的追跡
[DATE/OWNER] 2026-10-22 06時台 JST / B T028主・T024参照。STATIC/INFERRED/VERIFY/NOT READY。
[BASELINE] Local Compact接続成功、MASTER cp196/READY596(A115/B229/C136/D116)、規約、B HANDOFF、T028/T024、旧22回収・SAFETY_REFUSAL、search_index README/BUILD_MANIFEST PASS確認。原作ver0.67 manifest SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（今回原本ハッシュ再計算なし）。
[SEARCH] read-only: search.py strings addLimit/getLimit, function 0x4B4230/0x44E3F0/0x4B78C0/0x48A5B0/0x463280。Ghidra起動/REA/原本EXE実行・変更なし。
[NEW STATIC-1] Ghidra STRING_INDEXで addLimit=VA0x6303DC、参照site0x4B42CA in 0x4B4230。0x4B4230内0x4B42EF→0x463280（関数リスト登録候補）；0x4B4230は引数ベース+0x1EEF80へ作った文字列/値のpairを0x463280へ反復登録。0x4B4230直接callerは0x48A9D0 in 0x48A5B0。
[NEW STATIC-2] getLimit=VA0x63541C、参照site0x44F0E9 in 0x44E3F0。0x44E3F0はDAT_0087A368を登録先に用いる0x463280反復呼出群を持つ。0x44E3F0直接callerは0x4B795D in 0x4B78C0。
[NEW STATIC-3] 同じ起動初期化元0x4B78C0では、0x4B795D→0x44E3F0と0x4B79D6→0x48A5B0→0x48A9D0→0x4B4230の2段の直接CALLが確認できる。0x48A5B0は複数の初期化関数とオブジェクト確保を含み、原作実行時間のaddLimit利用経路を意味しない。
[INTERPRETATION] addLimitとgetLimitは少なくとも同一の単一登録テーブルへ入ることが直接コード上では示されず、別の登録経路がある。命令系と式評価系を分離保持する互換設計候補。ただしテーブルの正式な型、opcode、runtime handler、両者が同じbattle limit変数を操作するか、同一単位・反映タイミングはVERIFY。
[DEDUPE] B-20261020-1015-02はboss_tisa/webによるaddLimit(514)とAI getLimit()<500/>=500のDAT字句crossjoinが既知。本IDの増分はネイティブの登録起点2系列とCALL siteのみ。旧boss死亡時rank分岐/加算やAIしきい値をREADYとして再計上しない。
[PROVENANCE] Ghidra cached pseudocode codeSHA 0x4B4230=0A3DAAD25F6405CF68CF8016C29B046EF579133E23D691F45D824AFFFC3D3874、0x44E3F0=B30B8DBD71FAE49D0B187D13946619CF4DCAE4BEF02E964005CA5E7CFBF24289、0x48A5B0=0CEAA388E7C045A2F55590C378ADB4767DAE9B633AE7079B1D8AB31B27996874。
[REIMPLEMENT] btl event action addLimitとAI expression getLimitを別入力APIとして扱い、同一clockへの接続を証拠なしに確定しない。ネイティブが両者を同一stateに束ねることが検証できるまでVERIFYのまま。
[GOLDEN] boss_tisa/web合法死亡前後のgetLimit表示/AI tick、R=499/500、rank0/4、dialog0/2、full/kanni、cpu_red0/1を元EXE/DAT/SAVE/MAP/入力RNGと可視receiptで比較。原作x20改変DATではstrict不可。DESIGNED_NOT_RUN。original Gameplay Golden PASS0、新旧strict MATCH0。
[NEXT] 許可済み静的証拠で0x4B4230/0x44E3F0登録された実際のhandlerの初期化・呼出型を特定し、native timer stateとaddLimit/getLimit両routeの合流点を検証。拒否済み0x5710C0..0x571500、0x599BD0、旧T024書込み等は再試行・迂回しない。
[STATE] B詳細ファイルPC保存・直接readback成功。B READY0、E MASTER正式統合0、Task DONE0。