# B-20261029-0515-T028-ALFLAG-ONE-SHOT-DRAIN-01｜T028 二系統結果vectorのALフラグ分岐と消費後クリア
日時: 2026-10-29 05:15 JST。Owner B/T028（T012/T013は参照のみ）。STATIC/NATIVE + INFERRED/VERIFY/NOT READY。
## 保全・ソース境界
- Desktop Commander Local Compact ONLINE。MASTERはE正式checkpoint196/READY596（旧値、今回E統合なし）。B5 owner・ANALYSIS_LANES_PROTOCOL・LANE_B_HANDOFF・復旧記録を確認。
- B Library147件はPC同名147、サイズ一致93/末尾1B差54・未SHA全照合、旧拒否関連8件BLOCKED、10/25 14H全文未発見。旧10/28 17H/22H安全拒否・別作業更新の出自VERIFYは変更せず、拒否元操作を再試行していない。
- search_indexの旧README/BUILD_MANIFEST/search.sqliteは履歴。現行V3 canonical SHA256 0B057C43D30EAEC74588C84CF7E09AA7A488BD0FF170925591953EF578AFCB25、guard PASS_ACTIVE_V3_STATIC/inputs14/errors0/gameplay NOT_RUN。active.lockなし、Java/Ghidra観測なし。
- 原作read-only解析copy rea_lab/targets/hakushin067_Vahren.exe の実バイトSHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。Capstone x86 PE raw disasm、原本実行なし。
## 新規証拠1：同じcalleeへ異なるALを渡す
- 既04Hで接続済の第1vector manager+0x1EEC94..98: 0x48CFB3 MOV ECX,ESI→0x48CFB7 E8 CALL0x49E490→0x48CFBE TEST ESI,ESI、非NULLなら0x48CFC4 vtable+0x64→0x48CFC9 indirect CALL→AL gate。新規差分: 0x48CFCF LEA ECX,[ESI+0x260]、0x48CFD5 MOV AL,1、0x48CFD7 CALL0x5AA6E0。
- 第2vector manager+0x1EECA4..A8: 0x48D065 MOV ECX,ESI→0x48D069 E8 CALL0x49E490→0x48D070 TEST ESI,ESI、非NULLなら0x48D076 vtable+0x64→0x48D07B indirect CALL→AL gate。新規差分: 0x48D081 LEA ECX,[ESI+0x260]、0x48D087 XOR AL,AL (=0)、0x48D089 CALL0x5AA6E0。
- 0x5AA6E0 native: 0x5AA6E6 MOV ESI,ECX、0x5AA6E9 MOV BYTE [ESI+0x8C],AL、0x5AA6EF TEST AL,AL→0x5AA6F1 JE0x5AA70E。AL=1の場合のみ、[ESI+0x6C]側virtual+0x64 (0x5AA6FD indirect CALL)が非zeroなら0x5AA709 CALL0x5A9CC0。AL=0はこの前段をskipsし0x5AA70Eへ。
- 04Hの二系統→0x5AA6E0 CALL先とspot_fire経路は既知で重複加算しない。新規は呼出時のAL=1/0差分、receiver+0x260、native保存位置+0x8C、AL依存追加処理。どちらが「火」か、+0x5A9CC0の実効果、対象object/vtable実体はVERIFY。
## 新規証拠2：通常後続で3つの結果vectorを空にする
- 0x48C880後半は、旧既知5tuple manager+0x1EEC74..78で 0x48D2C2 CALL0x417160→0x48D30C MOV [EBP+0x1EEC78],EAX、別第1vectorで0x48D328 CALL0x417160→0x48D36C MOV [EBP+0x1EEC98],EAX、別第2vectorで0x48D388 CALL0x417160→0x48D3CC MOV [EBP+0x1EECA8],EAX。各pairはbegin!=end時のみ。
- 3 CALLともnative E8（raw: 0x48D2C2=e8999ef8ff / 0x48D328=e8339ef8ff / 0x48D388=e8d39df8ff）、V3 PE確認済。同helper 0x417160 nativeはEAX=destination(begin), ECX=source(end), first stack arg=endで equal fast-path、EAX=beginをreturn。callerはold endまで28B strideでheap-string必要時free/SSO初期化し、end=beginを書戻す。正常経路の一回消費後クリアをSTATICで支持する。
- クリアはresult処理後。既03Hの不完全5tuple std::out_of_range throwから正常クリアまで到達するか、上位catch/recoveryがあるかはVERIFY。「例外時も必ずクリア」とは断定しない。
## 再現性・独立性・次の一手
- 原作PE region SHA256: [48CFA9,48CFDC)=C79B7F98D1A87C31E841A3E937D7D6F1D9EAA3F75C5CD033697629F60F21A886、[48D05B,48D08E)=6CFA8E07DDA9AEA9F31A8A179DCDB67996208E7407AF3AB76C840BC94C99FAF6、[48D2AC,48D3D2)=F19B50963BE83FD415D2C0D79337CC8AEDFA5D74DBBAE8579A709B181274F2B2。
- B5 owner+HANDOFF既存新VA literal 0x48CFD5/0x48D087/0x48CFCF/0x48D081/0x48D328/0x48D388/0x48D36C/0x48D3CC 全8種0件。旧二vector・CALL先・5tupleフラッシュは重複0、10/25旧原文と他owner意味照合はVERIFY。
- 0x49E490はGhidra擬似Cでvoidとして表示されるがnative callerはEAXを受けてNULL判定する。ABI未検証なので返値/文字列解決型を確定扱いしない。0x417160もGhidra表示のvoidとは異なりnative callerがEAXを実際に使用している。
- Golden: 改変前DAT＋同一未改変EXE/SAVE/MAP/input/RNGで、両queueに個別に合法データを入れ、virtual gate ON/OFF、AL flag変化、0x5A9CC0/registration/readback、次tick再消費なし、異常tupleのcatch/残留を可視・同run観測する。DESIGNED_NOT_RUN、原作Gameplay PASS0/strict MATCH0。
- 次は0x5A9CC0 の副作用、queue生成元と1/0種別、T013最終対象/T024戦闘AI/T011 summon/T012ダメージ・士気T028本体。B READY新規0 / E MASTER統合0 / Task DONE0、NOT READY。原本/他lane/REA/dev_lab/Git/Work/設定/scheduleは変更なし。