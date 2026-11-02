# PRIVATE E/T018–T020 historical 2026-10-23 16:51 G3/G4 FastSim provenance gate

Existing E ID `E-AUDIT-20261023-1651-T018-T020-FASTSIM-EXIT-PROOF-SPLIT-01`. Raw original PC report: `tests/T020_FASTSIM_RETURN0_1_2_G3G4_PROOF_GATE_20261023_1651.md` SHA-256 `607F9EE4C00C6EC3B5DBAAC2D4CBC8A311D08E3FAC5FC3FFBB75FEDF19346E1E` (verified 2026-11-02). This sanitized copy omits refused scope metadata, so it is NOT byte-identical to raw PC report. Upstream REA-owned fast-sim analysis remains read-only cited, not reproduced or reattributed. Source V9 DB/callsite numbers are **2026-10-23 historical epoch** and were not re-extracted this run. Original Gameplay `NOT RUN`; synthetic 15/15 is historical and was **not rerun**. `PUBLISHED_INTAKE / NOT_CURATED / STATIC+SYNTHETIC+VERIFY / NOT READY`; no G3/G4 strict parity, original Golden PASS 0, strict MATCH 0, new MASTER/READY 0.

[Original byte-matched E-only Python](repro/t020_fastsim_exit_provenance_gate_20261023_1651.py) and [15-case JSON](repro/t020_fastsim_exit_provenance_gate_20261023_1651.json) can reproduce *only synthetic* routing/receipt expectations.

---

# 迫真戦記 E T018/T020｜簡略戦闘return0/1/2とG3/G4受入境界（2026-10-23 16:51 JST）
ID: E-AUDIT-20261023-1651-T018-T020-FASTSIM-EXIT-PROOF-SPLIT-01
状態: PC-SAVED / STATIC V9 CROSS-SOURCE / SYNTHETIC 15/15 / VERIFY / NOT READY / ORIGINAL GAMEPLAY NOT RUN。
根拠: REA所有 rea_lab/decomp_task/REA_20261023_1638_P0_FAST_SIM_500TICK_OUTCOME_CONTRACT_STATIC.md、E既存 tests/T020_BATTLE_RETURN_COMMIT_GATE_20261021_2147.md と E T020 2026-10-23 15H、統合V9 CLIで本回read-only取得した0x40E220/0x40E2F0とcallers 0x493630。
原作EXE出典SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。V9 SQLite SHA256: 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE。
V9独立verify本回: V9_INDEPENDENT_READBACK_PASS、functions11950 / refs243678 / native sites51214 / unowned E8=0 / unowned JMP=1。PC標準search_current.py/CURRENT pointerはV3のままでありV9への昇格は未実施。
## 今回のE新規横断差分（REAの計算式を再READYにしない）
V9直接E8 callers 0x00493630 は5 site: fast-sim 0x0040E2B9、通常時計0x0049303A/0x00493082/0x004930A1、DAT VM 0x004A1764。5 siteを一つの簡略戦闘経路へ統合しない。
0x0040E220 は条件[+0x78/+0x7C]==0x80000008 かつ [+0x19C]!=0 の経路で 0x0040E27F→0x0040E2F0 を呼ぶ候補。関数0x40E220の直接E8 callerは0と報告されており、実ゲーム到達と所有者登録はVERIFY。
0x0040E2F0 のreturn=0なら0x0040E28E→0x0040D220へ進み、この枝の0x00493630直接呼出は無い。return=1/2なら0x0040E2B9→0x00493630で渡すboolは(return==1)。flag bool0/1を勝利/敗北/攻撃側に即翻訳しない。
REAの機械語における最大500反復・0,50,...,450の定期判定はSTATIC。500はtick反復上限で実時間ではない。+0x1C8/+0x1CC側の0x514C80は別EAX入力、疑似Cに引数が無くても同一判定の二重実行ではない。vptr+0x18とcounterの意味はVERIFY。
## Golden G3/G4のE独立受入条件
G0合法旧UI起源、G1同battle-windowの直前SAVE bytes/SHAと入力、G2実MAP/side/ordered Unit/Troopが未充足なら、fast-sim戻り値をG3可視戦果・G4戦略復帰commitの代用にしない。
return0の0x40D220経路にも戦略側の最終結果/時間経過の観測が必要。return1/2のnative finish呼出事実だけでもHP/MP/死亡/EXP/所有権/勝敗一回反映を保証しない。0x40F000以後も別receiptが必要。
境界は {source G0-G4一意battleID, native execution route, returned code, finish bool, native finish count, external apply count, side identity, source old/new hashes, world diff} をnullableで保存。未観測はnull、固定アドレスの跨PID/跨watch接合は禁止。
T020合成fixture15件は tests/t020_fastsim_exit_provenance_gate_20261023_1651.json、軽量validatorは同名.py。今回 Local Python独立実行15/15 PASS / fail0、これは旧原作Gameplay PASSではない。元資料や製品コードは変更していない。
## DAT復元の独立確認（今回、原本起動なし）
data/KARATE_X20_20261022/manifest.json はRESTORED、restore_result.jsonは2026-10-22T04:46:19+09:00に復元成功を報告。PCでmanifest全591 DATのbefore SHAと現行ゲームディスク実bytesをread-only再計算し **591/591一致**、警告フラグTEST_MOD_KARATE_X20_ACTIVE.mdは不在。
このbeforeは2026-10-22 02:49時点の改変直前ローカルsnapshotであり、原本ZIPバイト全体との一致証明ではない。さらに復元前起動プロセス内のDAT反映/セーブへの残存は未検証。原作Goldenはexe hashだけで承認せずDAT digest・起動世代・実原作操作を別観測する。
## T019/MASTER/安全境界
T019 新規確定Wiki/DAT/EXE矛盾0。GameClearのDAT13/TXT2字句検索scope差のみRESOLVED、script2同名winner/phase flag用途/TXT loader/gwrite復帰はVERIFY。
今回E原作DYNAMIC OBSERVED0、actual Golden PASS0、strict MATCH0、正式READY統合0。MASTER最新全件再集計はしていない：旧checkpoint196 / 累計596=A115,B229,C136,D116 / 34Task DONE9,IN_PROGRESS21,VERIFY4。OFFLINE-UNSYNCED暫定26は依然要突合、旧成果を自動採録しない。
拒否保護: 既存の安全拒否ID・対象はBLOCKED。拒否済み元操作・内容・保護範囲は本入庫に再掲せず、別経路で再提出しない。
本回は新規E-owned testsのみ保存。原本EXE/ZIP/SAVE/DAT、他レーン・REA・dev_lab・Ghidra・V9/標準索引・MASTER・Git・Work・スケジュール変更0。
NEXT: 合法旧UIのG0/G1/G2と同一戦闘のG3/G4、戦闘終了の0→D220と1/2→493630のnative routeを区別する一次receiptを収集。新実測がない間はSTATIC/VERIFY。PC版MASTER最終照合・source/owner/READY/重複競合確認後にのみ正式統合。
