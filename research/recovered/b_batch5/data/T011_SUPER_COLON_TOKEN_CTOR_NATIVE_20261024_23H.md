# B/T011・T012｜DAT 親指定「:」と super ScriptData の原作PE接続（2026-10-24 23H）
研究ID: B-20261024-2318-T011-T012-SUPER-COLON-CTOR-01
Owner: B/T011（T012参照）。STATUS: PC-CONNECTED / STATIC-ORIGINAL-PE-ASM / STATIC-GHIDRA / STATIC-DAT / INFERRED / VERIFY / NOT READY。
## 前提・復旧
Local CompactでMASTER checkpoint196/READY596（E旧正式値、今run再集計せず）、規約、B HANDOFF、B owner、回収/拒否記録、検索README/manifestを先読。旧22-file回収と後発10研究・Library訂正版2・10–18H研究の研究ID単位統合は依然未完。新安全拒否0、既拒否 VA/操作の再試行0。active.lockなし・重いGhidra/Java稼働なし。
EXE: rea_lab/targets/hakushin067_Vahren.exe を読取専用で現物SHA256再計算、E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187 一致。search.sqlite SHA256=0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF、manifest一致。再逆コンパイル・原作実行/改変なし。
## 新しい原作ASM証拠（22Hの0x65DC08未解決を解決）
0x006021D0 PUSH 1; 0x006021D2 PUSH 0x0062C450; 0x006021D7 MOV ECX,0x0065DC08; 0x006021DC CALL 0x00402800; 0x006021E1 PUSH 0x00606420; 0x006021E6 CALL 0x005B6BA4 (_atexit); 0x006021EC RET。
0x0062C450の原作raw bytes = 3A 00（ASCII「:」NUL）。0x00402800のGhidra擬似Cは thiscall string assign：param2入力からparam3 bytesをコピーし、格納長+0x10と終端NULを更新する。従って上記 initializer が走れば 0x0065DC08 のstringオブジェクトは長さ1の「:」となる。
PE on-disk 0x0065DC08の24B初期値は長さ+0x10=0、容量+0x14=0xF、inline buffer0。静的ファイルの空状態から「:」への設定は0x006021D0のruntimeコピー経路が必要。
さらに原作.rdata VA0x0060941C（file offset 0x20881C）には DWORD 0x006021D0。前後0x00609418=0x006021B0、0x00609420=0x006021F0の連続関数ポインタ列。静的初期化リストの有力候補だがCRTの全呼出連鎖・実際の実行はVERIFY。
0x00504FE4 MOV EAX,0x0065DC08; 0x00504FE9 LEA EDX,[ESP+0x78]; 0x00504FED CALL 0x0041DED0; 0x00504FF2 TEST AL,AL; 0x00504FF4 JE 0x00505064。0x0041DED0擬似Cは文字列不一致をboolで返し、一致時AL=0。よって先のinitializer後はここが「:」一致gateとなりsuper生成候補0x00505064へ移る、というSTATIC結線を新たに得た。
既22H: 0x00505099 CALL 0x00502DD0でparent字句読込候補、0x005050D4 literal「super」VA0x0062C918、0x005050E2 pair、0x005050EE CALL 0x00463280で辞書登録候補、0x005050FF次字句取得。これらは既知で新規計上0。0x00502DD0 pseudocはinput token取得にglobal lexer state/param3を利用するが正確な親名の格納契約/例外はVERIFY。
## 証拠整合性・索引の限界
現物PE RVA→RAWで4byte即値 0x0065DC08 の出現は計4箇所：file offsets 0x1043E5(parser)、0x2015D8(initializer)、0x20582A/0x205849(cleanup)。旧Ghidra DATA_REFS.jsonlのtarget 0x0065DC08はsite 0x00504FE4のみ、CLI function 0x006021D0 は NOT_FOUND。原作ASMとの相違は索引の未収録であり、原作EXE側の初期化処理不存在を意味しない。
限定SHA256: PE 0x006021D0..0x006021EC 29B=E6FF0AA56F94D979E2AD433984A64E955A07B2284D60174634422447D944C187; PE 0x00609400 48B=F52EBA04705845D9CECA02105660AED81E6E116F6CE1FC21EEC5D05E2B793D88; 0x0062C450 2B=7648EB81C4E9FEF7B51879C6FCD6FB4B8863EEA0CB2A978C508711DC52C80041; 0x00504FE4 18B=B705BFC267BDB3D4667247EA5DD51068A7187A10C560C96AF57A005390149974。
重複: B T011*.md/T012*.md/B HANDOFFの 6021D0/62C450/60941C exact照合0。22Hのsuper writer/21Hのsuper停止・親DATと16H〜20Hのgetter/反復境界は今回再計数0。E・他lane・Library最新の完全意味重複照合は未了。
## 適用と判定
原DAT「32_ボススキル/B_14_ヌエバ・デスパセーニャ.dat」には u_diplo_nt3..nt6 : u_diplo_nt2 の親宣言がある。構文「:」→token string initializer→比較一致→super ScriptData生成はSTATICとINFERREDで接続。ただし各Skill実通過/compiled +0x288=0/登録成功/重複扱い/エラーパスはVERIFY。
Goldenは無改変原作EXE・X20前DAT・同SAVE/MAP/input/RNGでcolon有無、空親名、合法親名、親のみstr_ratio=0、重複super、実Skill+0x288/HP/MP/次tickを比較（DESIGNED_NOT_RUN）。旧原作Gameplay PASS0、strict MATCH0、新B READY0、E MASTER統合0、Task DONE0。
[RECOVERY OTHER / B-RC-20261024-23H-REPL-MULTILINE-01] 初回read-only Python REPL内def複数行を空行無しで送ってSyntaxError。初回取得データ不採用・PC書込0、同一安全許可の1行lambdaへ訂正してPE/ASM/各SHAを取得・復旧。新安全拒否0。拒否済み範囲・操作の別path/tool迂回0。
NEXT: 0x0060941Cの静的初期化テーブルがCRTでいつ走るか（既存索引/原作ASMで軽量確認）、0x00505099 parent ScriptDataの実出力、super重複時のfirst-wins/例外（A/T005所有の汎用辞書全体はBで変更しない）を検証。PC正本のB HANDOFFだけへ共有し、EのMASTERは触らない。
