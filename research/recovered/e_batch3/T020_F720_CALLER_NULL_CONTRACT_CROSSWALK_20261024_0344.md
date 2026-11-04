# 研究E｜F720戻値NULL契約：呼出元ガード非対称とGolden非昇格
ID: E-AUDIT-20261024-0344-T020-F720-CALLER-NULL-CONTRACT-01 / 2026-10-24 03時台 JST / owner E / STATIC+SYNTHETIC / NOT READY。
## 先行証拠・所有権
- Desktop Commander Local CompactでPC正本を確認。MASTER_LEDGER、ANALYSIS_LANES_PROTOCOL、A-D HANDOFF、REA PROGRESS/03H証拠、DEV実装計画、T018/T019/T020、index README/manifest/V9入口をread-only照合。
- 正式MASTER最終checkpoint196、READY596（A115/B229/C136/D116）、34 Task DONE9/IN_PROGRESS21/VERIFY4は過去確認値で全件再集計なし。公式新規READY統合0。
- 対象原作EXE SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（REA03H実バイト検査。E本回EXE再ハッシュなし）。PC標準CLIはV3のまま、独立V9は推奨別名。索引ポインタを変更しない。
- REA03H STATIC.md SHA256 DABA032A4DB9821DEE5DE5BA92E9BB3BE7BAE87EEC888B264FB02A0438153EA3、EVIDENCE.json SHA256 78F8B1FCA145FD33552AD68F09A0FF2D23FE8CA71484ED539BDECC9D35B4911C。E checkerで両SHA2/2再確認。24バイト検査24/24・E8 target9/9はREA既実績で、Eが新たに逆アセンブルした件数ではない。
## T018/T020：新しい受入上の差分
- 0x48F720には戻り値0の静的経路がある。03H REA新規差分はcaller間NULL防御の違いであり、02Hのfilter規則/7 caller抽出自体は重複加算しない。
- 0x4901C1 -> 0x4901EE CMP EAX,EBX（EBX=0）->0x4901F0 JE 0x490223 -> 非NULL時のみ0x4901F2 [EAX+0x94]。局所明示NULLガードSTATIC。
- 0x40F393 ->0x40F398->0x583C76 [EDI+0x94]、0x48FBD9->0x48FBF7->同callee、0x4F66ED->0x4F66F2->同calleeの局所経路には同様のNULLガード未確認。
- 0x4905F2と0x49381Eのmode等先行条件は、F720戻りポインタ自身のNULLチェックとは別。0x434EF3の後続EBP使用は未監査。
- 候補不在で0を返せることと、一部callerの明示NULLガードは、旧ゲームで0が非ガード経路に実際に届くこと、クラッシュ、原作バグ、データ破損を証明しない。上位の候補存在不変条件と同一実行での観測が未取得。
- G2 MAP/攻撃・防御・支援/ordered deployed Unit・Troopを、F720選択・DemoPerson側識別0/1・NULLチェック成功から補完しない。G0合法旧UI起源/G1同一run直前SAVE SHA+入力/G2実MAP+三side名簿/G3結果/G4戦略World差分はE完全受入未充足。
- 過去の同一PID内2 battle windowを同一戦闘として結合しない。時刻・EXE/DAT/SAVE/入力/capture SHAの一致が必要。内部NULLの動的観測が合法にできなければSTATIC証拠と区別。
## T020検証・T019矛盾
- E所有JSON20件＋Python checkerを新設。明示NULLスキップ、非ガード局所経路、mode gate、下流未監査、RET未観測、クラッシュ/G2/実観測への誤昇格を区別。
- E checker実行: REA2出典SHA2/2 PASS、caller site set 7/7一致、合成20/20 PASS。元EXEを起動せずactual Golden runner NOT RUN、E DYNAMIC OBSERVED0、actual Golden PASS0、strict MATCH0。合成RET=0は作為的入力で原作観測ではない。
- T019新規確定矛盾0・原作確定BUG0。GameClear DAT13/TXT2字句検索範囲差のみSOURCE-SCOPE RESOLVED、script2同名優先・phase flag・TXT実読込・gwrite復帰はVERIFY。
## 統合・安全・再開
- REA03H PC-SAVED READBACK VERIFIEDでもowner NOT READY。B03:17もNOT READY。MASTERへのREADY代理統合なし。OFFLINE-UNSYNCED暫定26研究は旧報告値、ID照合未完了。
- 旧拒否T018表境界、E17:55/18:56/22:52/00:52/22日08:49・08:57、C T026/T032、D T030、禁0x5710C0を独立BLOCKED維持。拒否済み元操作の別shell/tool/path/Remote/ZIPによる迂回0。
- 今回書込はE所有新規3点のみ。原本EXE/ZIP/SAVE/DAT、A-D/REA/dev_lab、Git/push、Work、設定、他スケジュールの変更0。
- NEXT: 0x40F320入口候補非NULL保証はREA ownerによる継続確認。Eは合法G0/G1/G2一次receiptの同run結合を最優先。F720静的NULL証拠だけでG3/G4/strictへ昇格しない。
