# B-20261028-10H-T028-ROSTER-VECTOR-DUAL-SET-PRODUCER-01｜T028 pointer-vector producer → 二つの赤黒木集合
Owner: B / T028。2026-10-28 10時台。STATIC-ORIGINAL-PE-ASM / STATIC-V3-GHIDRA / INFERRED / VERIFY / NOT READY。新規正式READY 0、E MASTER統合 0、Task DONE 0。
## PRECHECK / SOURCE
- Desktop Commander Local CompactでMASTER_LEDGER最終E公式checkpoint196/READY596、ANALYSIS_LANES_PROTOCOL、B owner5タスク、LANE_B_HANDOFF、復旧ハブ・旧拒否と未同期索引を読取。2026-10-25 14HのOFFLINE-UNSYNCED研究全文と他lane意味的完全重複照合は未完/VERIFY。
- 原作ver0.67 read-only EXE: rea_lab/targets/hakushin067_Vahren.exe。実サイズ2910720B、SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。実行・変更なし。
- 現行V3正本: rea_lab/headless_analysis/search_index/HAKUSHIN067_CURRENT_CANONICAL_V3_20261022.sqlite、135110656B、実SHA256 0B057C43D30EAEC74588C84CF7E09AA7A488BD0FF170925591953EF578AFCB25、immutable read-only PRAGMA quick_check=ok。旧search.sqliteは新規解析に使わずmanifest/READMEのみ確認。Ghidra全面実行なし。active.lock確認2箇所ともなし。
## NEW NATIVE PRODUCER/CONSUMER CROSSJOIN
- 0x493A59 CALL 0x44D730、0x493A7B CALL 0x47BB50後、0x493A8Bで一次ポインタ配列のbeginを読み、0x493A92 MOV EDI,[EAX+EBX*4]で当該元オブジェクト参照を取得（各calleeの厳密なゲーム上の役割はVERIFY）。
- 0x493A95 LEA ECX,[ESP+0xFC] / 0x493A9C PUSH ECX / 0x493A9D PUSH EDI / 0x493A9E CALL 0x5882F0。既07H原作ASMで解明済みの0x5882F0は元オブジェクト自身を先頭seedし、source+0xD4..D8の0x1C幅名レコードを0x467DE0で解決、成功した参照だけ追加する4Bポインタ配列を生成する。
- 0x493AB6 CMP [ESP+0x20],1 / 0x493ABB JL 0x493AD6。1以上のとき0x493ABD [ESP+0x100]（end）・0x493AC4 [ESP+0xFC]（begin）をPUSHし、0x493AD1 CALL 0x498EE0で第1赤黒木集合に登録する。
- 0x493AD6 CMP [ESP+0x20],2 / 0x493ADB JNE 0x493AF9。2なら0x493ADD [ESP+0x100]（同一end）・0x493AE4 [ESP+0xFC]（同一begin）をPUSHし、0x493AF4 CALL 0x498EE0で第2の別集合に登録する。N=0は両方skip、N=1は第1のみ、N=2は両方（N決定自体は既03H）。
- 0x498EE0原作ASMは引数のbegin..endを4Bごとに走査し、0x565780/0x40EBE0/0x5AF0F0を介して32bitキーを赤黒木集合にinsert（重複処理を含む・既04H）。今回の新規差分は**このキー配列のproducerが0x5882F0の自己seed＋名前解決結果のポインタ列であり、両集合が同一範囲を条件付きで共有する**という接続。純数値Unit IDへの変換はこの経路に無い。
- 0x493AF9から解放・後始末へ進み、0x493B01 [ESP+0xFC]を確認して0x493B0F CALL 0x5B6BBBで一時vector bufferを解放。0x493B18/1F/26でbegin/end/capを0に戻し、0x493B2Dで次要素へループする。集合ノードと一時vectorの寿命は別。解放済vectorバッファではなく32bitキー値を集合側に保存することがnative register-flowから分かる。
## VALIDATION / DEDUP
- 原作x86-32限定ASM 0x493A8B..0x493B35 (170B) SHA256 78F78277FBD099AF150818ABAEAC102094C48E76C4982A4531BD9EBEA2085918。0x498EE0から176BのSHA256 EC24F6328C60D1D66BFEC46EC9247188BB738CEBCCA64AF8CA5DCEB70C7EA1D5。V3検索の0x493630擬似C・callers 0x5882F0 (13 direct sites)はSTATIC補助。
- 原本E8+rel32検算: 0x493A59→0x44D730、0x493A7B→0x47BB50、0x493A9E→0x5882F0、0x493AD1/0x493AF4→0x498EE0、5/5一致。過去03H/04H既知2つのCALLと挿入関数自体を新発見として再計数しない。
- B所有T011/T012/T013/T024/T028のMarkdown＋LANE_B_HANDOFF 計324ファイルで新sites 0x493A9E/0x493A92/0x493AC4/0x493AE4/0x493B18/0x493B1F/0x493A95/0x493AB1の旧literal先行一致0。他lane/10月25日未同期全文の完全意味的非重複はVERIFY。
## INTERPRETATION LIMIT
- 05/06Hの第1集合consumerは0x467DE0の解決ポインタで0x44D070を検索する。今回の第1集合producerもポインタ値を登録する一経路と静的に接続したが、全てのproducer・全ての戦闘状況への適用は未確定。他の書込／消費者、第2集合のconsumer、元オブジェクトの正式型と実際の士気/敗走効果はVERIFY。
- 0x5916E0共有fallbackの利用有無はこの0x5882F0名解決経路からは証明されない（名解決calleeは0x467DE0）。名前解決missをfallback成功と同一視しない。連続ヒット/ミスで同一ポインタの安定性もDYNAMIC未実証。
## GOLDEN / NEXT
- 原作EXE無改変・20倍強化前DAT・同一SAVE/MAP/input/RNGを用い、木flag N=0/1/2、関連名参照0/1/複数、解決hit/miss/同一参照重複、両集合のキー前後と第1集合の後続skipを同一runで照合する設計のみ。原作Gameplay Golden PASS0/strict MATCH0、DYNAMIC実測NOT RUN。新B正式READY0/E MASTER統合0/DONE0、NOT READY。
- 次は0x493A59の入力key producerと0x47BB50の実体、二番目の集合のconsumer、実オブジェクト型+0xC0/+0xC4、T028本来の士気/敗走、T013最終target、T024 AI判断、T011召喚親子・T012状態/RNG。
- 既拒否VA 0x5710C0..0x571500/0x58021E..0x580340と既拒否操作の別tool/shell/path/Remote/ZIP迂回は0。原本/MASTER/他lane/REA/dev_lab/Git/Work/設定/scheduleに書込なし。今回の新規安全拒否0。保存後readback証明は別追記。
