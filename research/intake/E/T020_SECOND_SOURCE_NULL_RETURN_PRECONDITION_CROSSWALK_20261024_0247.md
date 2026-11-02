> Archived E-owned historical study. Original source: `tests/T020_SECOND_SOURCE_NULL_RETURN_PRECONDITION_CROSSWALK_20261024_0247.md`; PC SHA-256 `5025646D8BB67F4A4592674791CA2F08DCEB3F36BAA65FABAE020782532290D3` rechecked 2026-11-02. Safety-refusal specifics redacted. Historical STATIC/SYNTHETIC/VERIFY; NOT_CURATED, original-game Golden not run, NOT READY; archived test metrics not rerun in this intake.

# 研究E｜簡略戦闘・第2source filtered lookupのNULL前提条件とG2非昇格
ID: E-AUDIT-20261024-0247-T020-SECOND-SOURCE-NULL-PRECONDITION-01 / 2026-10-24 02:47 JST / owner E / STATIC CROSSWALK + SYNTHETIC / NOT READY。
## PRECHECK / 証拠
- Desktop Commander Local Compact接続成功。MASTER_LEDGER.md、evidence/ANALYSIS_LANES_PROTOCOL.md、A～D HANDOFF末尾、REA PROGRESS/最新02H成果、dev_lab/docs/IMPLEMENTATION_PLAN.md、E T018/T019/T020、旧search_index README/BUILD_MANIFESTと統合V9入口をread-only参照。
- MASTER最終正式checkpoint196、READY596=A115/B229/C136/D116。34 Task DONE9/IN_PROGRESS21/VERIFY4は以前の正式確認値を継承（今回全件再集計なし）。B 02:17 T013とREA 02H研究はいずれもNOT READYで、E公式統合0。
- 原作識別EXE SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（REA 02H実バイト照合済み。今回EはEXE自体を再ハッシュしない）。統合V9 SQLite SHA256 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE（既verify値、今回E再hash無し）。PC標準CLIはV3のまま。
- REA 02H owner source: REA_20261024_02H_P0_F720_FILTERED_LOOKUP_ABI_STATIC.md SHA256 E8D60E3A7EABB1E6D8844BFED22E4E2D1C94070F6559CA2101B1EF7699014907、同EVIDENCE.json SHA256 ED65CEA2D2707213633C41B83B7B37A4C7A72D629A9C36FED178EBBDD6538162。今回E checkerで両ファイル実バイトSHA 2/2一致。
- Eは統合V9の function 0x0048F720 / function 0x00583C70 を専用CLIで直接取得。0x48F720の未補正疑似Cは候補ループとreturn0を示すがnative ABI未認証。0x583C70の0x583CE6→0x597B00は E9_TAIL_JMP（通常E8ではない）。
## T018：限定した新しい受入結論
- REAの原作PE/rel32証拠で、0x40F393 E8 CALL0x48F720の戻りEAXを0x40F398 E8 CALL0x583C70に引き渡し、次の0x583C76で[EDI+0x94]参照する（EDI=EAX）。このcallee入口には独立NULLガードが示されていない。
- 0x48F720は[EBP+0x1EED34]の比較先木を参照し、列のうち『比較先木にないキー、かつnode+0x18非zero』の最初の候補を選択する静的パターン。候補不在はEAX=0 / RET4。ノード+0x21はiteratorの走査、候補属性ではない。成功返値はnode+0x14から更に2段の間接参照を経由して得る。
- **新たなE受入境界**：『lookupに0戻り経路がある』『callerが次のcalleeへEAXを渡す』『calleeが+0x94を読む』だけで、旧ゲームでNULLが本当に渡った・Access Violationが起きた・通常戦闘にバグがある、とは判定しない。0に至る合法入力可達性・候補集合・同一call時相・実行時EAX/EDI・他の前提条件をVERIFYで保持する。
- 逆に『第2sourceが非NULL』『第1sourceと第2sourceの選定が成功』『DemoPerson初期化が走った』のいずれもG2のMAP・三陣営・ordered deployed Unit/Troopを証明しない。既存の0x597B00ソース選択、第2selector、0x583C70処理、後段+0x0C vcallを別stageとする。
- C-NB02合法旧UIのG0戦闘起動、G1同一run直前SAVE bytes/SHA+入力、G2実MAP+攻撃/防御/支援+出撃名簿、G3終了・G4戦略復帰World差分は全受入未充足。実機内部のNULL/候補木を合法に観測できない場合は対象をINELIGIBLEとしGoldenの穴埋めをしない。
## T020：独立合成負例
- 新規E-owned tests/t020_second_source_null_flow_gate_20261024_0247.py と tests/T020_SECOND_SOURCE_NULL_FLOW_CASES_20261024_0247.json を作成。source SHA/出典JSONの5静的条件、same-run/at-call snapshot、候補完全性、lookup戻り値、後続CALLの到達、クラッシュ断定、G2誤昇格を分離。
- Python軽量実行実測: REA source SHA verified2、static claims5、synthetic18/18 PASS、fail0。実行は合成判定器のみ。原作ゲームとT018比較runner NOT RUN / 新規E DYNAMIC OBSERVED0 / actual Golden PASS0 / strict MATCH0。
- synthetic complete candidate snapshotは実ゲームから採取済みの事実ではなく、検証器の仮定。NULL+後続CALLでも結果はSTATIC_NULL_FLOW_RISK_NOT_CRASH_PROOF。実際のクラッシュ認定やデータ破損を示さない。
## T019・統合・安全と再開
- T019新確定矛盾0。GameClear DAT13/TXT2の字句検索範囲差RESOLVEDを維持し、script2同名優先、phase flag、TXT runtime、gwrite復帰はVERIFY。原作バグ追加0。
- [SAFETY_HOLD] 既存の拒否済操作・対象は移管範囲外。拒否メタデータのみ保持し、再取得・迂回は行わない。
- 今回のPC書込はE所有tests新規3点のみ（報告・fixture・checker）。A-D/REA/dev_lab/原本EXE・DAT・ZIP・SAVE/Git/push/Work/設定/他スケジュール不変更。新規安全拒否0。
- NEXT: 合法C-NB02同runのG0/G1/G2 receipts有無と、選定前コンテナ・木・nodeフラグのsnapshot同時性を分けて確認。原作入口/出口受入が無ければG3/G4やstrict MATCHへ昇格しない。Eの新資料は保存後に直接readback+SHAを取る。
- [保存後SHA/readback] fixture SHA256=2B94FEE3323BA30D7F3A8B22A44743126E547FD043F9C0E968546E321BE9ED42、checker SHA256=098B3D14A17E531429860F9AD7CCE6FE03FF4542F0B407F7F21AEDC9A823934C。本文・両成果物はLocal read_multiple_filesで直接読み戻し済み。