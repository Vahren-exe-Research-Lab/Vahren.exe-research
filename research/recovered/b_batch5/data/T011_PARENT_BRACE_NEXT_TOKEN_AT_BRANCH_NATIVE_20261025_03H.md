# B T011｜super後の上位token反復・空文字終了・@判定（03時台）
研究ID: B-20261025-0312-T011-TOKEN-POSTBRACE-AT-DISPATCH-01 / owner B / T011主・T012参考 / STATIC-ORIGINAL-PE-ASM / STATIC-GHIDRA / INFERRED / VERIFY / NOT READY

## 事前確認・証拠源
Desktop Commander Local Compact接続成功。MASTER/ANALYSIS_LANES_PROTOCOL/B HANDOFF/B担当T011/T012/T013/T024/T028・過去の拒否/未同期索引確認。10/21回収22file＋後続10研究＋Library訂正版2・10/24オフライン成果のID完全統合は未完。
原作 ver0.67 既存派生証拠 rea_lab/targets/hakushin067_Vahren.exe SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187 現物一致。search.sqlite SHA256=0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF、BUILD_MANIFEST一致、ro immutable quick_check=ok。2 lock候補なし、Java/Ghidra再解析なし。原本の実行/編集なし（PC上Vahren.exe稼働中でも介入せず）。
## 新規原作ASM：親宣言後のtoken非空判定
0x50B8E6→0x5049E0 のstatusを 0x50BA65 MOV EBP,EAX /0x50BA69 JNE0x50BB40で分岐するのは既02H成果で再計上0。
新：正常EAX=0で 0x50BA6F..0x50BAC4 は一時文字列長容量によるcleanup、0x50BAC7 LEA EDX,[ESP+0x24]、0x50BACB PUSH EBX(=0)、0x50BACC PUSH EDX、0x50BACD LEA ECX,[ESP+0xCC]、0x50BAD4 CALL 0x502DD0、0x50BAD9 ADD ESP,8。出力先として上位パーサのローカル文字列候補を渡す。
0x50BAE9 CMP DWORD PTR [ESP+0xD4],EBX(=0) → 0x50BAF0 JNE0x50B4C0。+0xD4はtoken文字列候補の+0x10 lengthに整合。非空なら0x50B4C0の汎用token判定へ、ゼロなら0x50BAF6..0x50BB34 cleanup、0x50BB39 XOR EAX,EAX→0x50BBBC共通復帰。静的な分岐は確実だが、token長0の全発生理由（EOF/空入力/パーサ状態）はVERIFY。
## 非空側では @ 文字を検査する経路に進む
0x50B4C0で新token処理を開始。0x50B4EC PUSH 1→0x50B4EE PUSH 0x62CF54→0x50B4F3 LEA EAX,[ESP+0xCC]→0x50B4FA PUSH EAX→0x50B4FB CALL 0x426490（Ghidra疑似C側も当該CALL確認）。
原作PE 0x62CF54..55 生バイト=40 00、すなわち '@' とNUL。0x50B508 CMP EAX,-1 /0x50B50B JE0x50B5CA。非-1の場合 0x50B511以降0x4261B0を使う追加処理。検索位置/一致条件と解釈するのはINFERRED、0x426490の正確な契約/全パスはVERIFY（A T005のExplicitNull意味論を本件で再認定しない）。
## 既存との境界・証跡
前01Hは { 字句判定と失敗メッセージ、前02Hは0x5049E0の戻り値と上位伝播。本件の独立増分は0x50BAD4後のtoken長分岐・長さ0→EAX=0の上位終了・非空→@判定の具体的CALL siteとliteral。B T011/T012/HANDOFFおよびA T005で0x50BAE9/0x50B4C0/0x62CF54完全一致記録0（02Hの0x50BAC7言及は既知として差し引く）。意味重複完全照合はVERIFY。
原作PE 0x50BA65..0x50BB3F=219B SHA256 CD6F5ACF7E71E1520638B8BB933323DF158126BEEEA0C45A3EB00ABF700D4DD8。
原作PE 0x50B4C0..0x50B511=82B SHA256 BD3070AABB177B27BC836105A538E7FD9215D79A155A09026C74C14A61C37BC7。
原作PE 0x62CF54..55=2B SHA256 EEC4121F2A07B61ABA16414812AA9AFC39AB0A136360A5ACE2240DC19B0464EB。
## リスク・Golden・次の一手
STATICは具体的命令・分岐・生バイトのみ。上位0x50B220の正確な戻り値型、@の意味、token長0の原因、実際のu_diplo_nt3..6の実効str_ratio/Skill+0x288はVERIFY。0x416920内部/0x5710C0..0x571500等既安全拒否対象に非介入。
無改変旧EXE＋20倍改変前DAT＋同一SAVE/MAP/input/RNGで正常super宣言、次token有無・@を含む合法DAT実例、compiled倍率・可視HP/MP/後続tickを比較DESIGNED_NOT_RUN。旧Gameplay Golden PASS0、strict MATCH0、新B READY0、E MASTER統合0、DONE0。
[RECOVERY OTHER/RESOLVED B-RC-20261025-0312-PY-QUOTING-01] 初回PowerShell python -c引用符解釈でSyntaxError。修正済み別コマンド実行で限定ASM/PE hash取得。初回未検証出力破棄、書込0、安全拒否ではない。
[RECOVERY OTHER/RESOLVED B-RC-20261025-0312-ASM-ALIGN-01] 0x50BA60非命令境界でcapstone初回0命令、原作命令境界0x50BA65へ補正して分岐列取得。未検証出力不採用、原本変更なし。
本IDの成果はPCのB所有詳細とT011/HANDOFFのみ保存し独立読み戻し。Ghidra全面解析/REA重複/他owner・MASTER・Git・設定・スケジュール変更なし。次は0x50B4C0非空字句分岐とSkillロード関数0x599BD0でのsuper継承実効値を既存検索索引から絞って照合。
