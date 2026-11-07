# 新B T028｜効果登録0x5AA6E0のAL入力8直接CALL・3ラッパcaller（2026-10-29 08H）
ID: B-20261029-08H-T028-EFFECT-ALFLAG-CALLSITE-SENTINEL-MATRIX-01
Status: STATIC ORIGINAL-PE ASM / INFERRED / VERIFY / NOT READY。owner B T028。公式READY0、Task DONE0、E統合0、原作Gameplay Golden PASS0、strict MATCH0。
## 出典・プリチェック
- Desktop Commander Local Compact PC ONLINE。MASTER最終公式cp196/READY596（旧値、全再集計なし）。ANALYSIS_LANES_PROTOCOL、LANE_B_HANDOFF、B所有5資料、B未同期・安全保留索引、search_index README/BUILD_MANIFEST/search.sqlite存在を事前確認。
- 検索: 既存V9 search_unified_v9_20261023.py function 0x431BE0/0x434EB0/0x4A6CE0/0x49E490/0x5AA6E0 および callers。V9は現行PCデフォルトV3を置換せず使用。Ghidra・Java・ゲーム起動/再解析0。
- 機械語: rea_lab/targets/hakushin067_Vahren.exe（読取専用）、Capstone x86 32bit と pefile PE image mapping。今回現物EXE SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187／2910720 bytes。
- V9で0x5AA6E0へのE8 direct callerは計8件。原作現物PEの相対disp32を全8箇所独立再計算し、8/8が0x5AA6E0に一致。間接vtable呼びの意味/実体は未確定。
## 直接CALL 8件のAL引数
| CALL site | AL直前の機械語 | 条件・意味の限定 |
|---|---|---|
| 0x431BF7 | 0x431BED MOV AL,[ESP+4] | 0x431BE7 vtable+0x64戻り真の場合、ラッパ引数byteを渡す。動的値 |
| 0x435246 | 0x435244 MOV AL,1 | 0x435234 vtable+0x64 真後の1 |
| 0x48CFD7 | 0x48CFD5 MOV AL,1 | 旧05Hの第1queue、既知・再計数0 |
| 0x48D089 | 0x48D087 XOR AL,AL | 旧05Hの第2queue、既知・再計数0 |
| 0x494A41 | 0x494A3F XOR AL,AL | 0x494A1B [EBP+0x1EEC3C]==1、0x494A33 vslot真の0 |
| 0x495B7D | 0x495B7B MOV AL,1 | 0x495B57 [EBP+0x1EEC3C]==1、0x495B6F vslot真の1 |
| 0x4977E4 | 0x4977E2 MOV AL,1 | 0x4977C6 [EDI+0x1EEC3C]==1、0x4977D6 vslot真の1 |
| 0x4A6DC9 | 0x4A6DC7 XOR AL,AL | 0x4A6DBB vslot真の0 |
- 直CALL内訳: literal1=4、literal0=3、stack引数=1。旧05HのAL1/0二queueだけを汎用の唯一の呼出と誤認しない。
## 0x431BE0ラッパのcaller3件からAL値をさらに限定
- 0x431BE0..0x431BFC は [ESI] vtable+0x64 を0x431BE7 CALL、0x431BE9 TEST ALし、falseで0x431BFC RET4。trueのみ0x431BEDで[ESP+4]のbyteをALへ再設定し、0x431BF1 ECX=ESI+0x260、0x431BF7 CALL0x5AA6E0。仮想関数のtrueがそのままAL引数になるわけではない。
- V9 callers(0x431BE0) は0x4A3AEB、0x4A3BA7、0x4A8ED2のE8 3件。各callerでのスタック引数とE8相対先をPE native確認。
- 0x4A3ADF CMP EBX,-1 / 0x4A3AE2 SETE CL / 0x4A3AE5 MOVZX EDX,CL / 0x4A3AE8 PUSH EDX / 0x4A3AEB CALL wrapper。直前の0x4A3AD0 TEST EBX / 0x4A3AD2 JS により負値枝で、-1ならAL1、その他負値ならAL0となる候補。ただし到達/対象型はVERIFY。
- 0x4A3B97 CMP [EBP-0xF04],-1 / 0x4A3BA0 SETE DL / 0x4A3BA3 MOVZX ECX,DL / 0x4A3BA6 PUSH ECX / 0x4A3BA7 CALL wrapper。局所値==-1ならAL1、そうでなければAL0。
- 0x4A8ECE PUSH 0 / 0x4A8ED2 CALL wrapper は常にAL0。以上の3siteとも0x431BE7 vslot+0x64で真を返す条件が必要。
## 既知calleeとの接続と解釈境界
- 既知0x5AA6E9 は[N+0x8C]=AL保存。AL0は0x5AA6F1 JE→0x5AA70E。AL1時は0x5AA6F3 L=[N+0x6C] の vtable+0x64判定真の時だけ0x5AA709 E8→0x5A9CC0 を通り、L+0x160の内包座標縮退後に共通登録へ。旧06H/07Hのcallee効果詳細は再計数0。
- 本回の増分は「直接8siteとwrapper間接3siteのAL provenance」「-1 sentinelからAL bool化」「manager+0x1EEC3C==1を要求する別3経路」。flag本来の意味、manager同一インスタンス性、vtable+0x64実体、N/L型、効果・士気・敗走への影響はVERIFY。
- 0x48C8BEでmanager+0x1EEC3C=1を書く既23H結果処理との時相接続は候補だが、この3callerのEBP/EDIと当該managerの同一性・順序は未確認。原作実バイト比較だけでruntimeの再入や多重登録を断定しない。
## 重複・復旧・Golden
- B owner T011/T012/T013/T024/T028 のT0*.mdとLANE_B_HANDOFF計353 Markdownを局所文字列検索。新site 0x494A41/0x495B7D/0x4977E4/0x431BED/0x4A6DC9 は先行字句一致0。完全意味dedup、2026-10-25未発見資料、他lane全体はVERIFY。
- 旧B Library資料はSAFE134バイト照合済み・HOLD21安全保留。旧B147については93同サイズ/54差1Bという別時点監査あり、全体完全同期の根拠にはしない。禁止VA0x5710C0..0x571500等の既安全拒否を検索・再提出・迂回せず、保留21の実行もしない。
- 原作未改変EXEとX20改変前DATの同一SAVE/MAP/input/RNGで直8経路とwrapper3経路の到達、-1/他負値/0、各vslot真偽、AL+0x8C、I/L/N矩形、Task登録・解除、次tick/士気・敗走を原作一次receiptとして採取必要。設計のみDESIGNED_NOT_RUN、Game Golden PASS0、strict MATCH0、NOT READY。
- 次の合法検索先: 0x4A3AEB/0x4A3BA7のEBX・stack source、0x5AA6F8 L vslot+0x64の型、N+0x6C writer、0x48C8BE manager連結、T013最終target/T024 AI/T028士気・敗走本体。
- 今回はPC側にB詳細・T028 owner・B HANDOFFだけを更新する。原本/MASTER/他lane/REA/dev_lab/Git/Work/設定/scheduleは不変更。新安全拒否0、研究全体READY0。
