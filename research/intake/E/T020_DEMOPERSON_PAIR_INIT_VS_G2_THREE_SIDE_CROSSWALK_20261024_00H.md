# PRIVATE E/T018–T020 historical three-side G2 evidence boundary (source-preservation, not native proof)

Existing ID `E-AUDIT-20261024-00H-T018-T020-PAIR-THREESIDE-BOUNDARY-01`. Verified original authorized-PC report `tests/T020_DEMOPERSON_PAIR_INIT_VS_G2_THREE_SIDE_CROSSWALK_20261024_00H.md` raw SHA-256 `637BE663B2F2FE801354C43ECCC145803E3987A8E2774D7B70916D38479076F5` on 2026-11-02. The refusal-metadata line below is redacted, so this copy differs from the original raw bytes. Upstream REA/B source reports remain **read-only owned provenance**; this E-owned static crosswalk does not attribute their findings to E. `PUBLISHED_INTAKE / NOT_CURATED / STATIC/VERIFY / NOT READY`, G0–G2 same-run original receipt incomplete, gameplay Golden PASS 0, strict MATCH 0. Historical synthetic static 12/12 cited below was not rerun here.

E-only [repro source](repro/t020_demoperson_pair_g2_static_gate_20261024_00H.py) and [negative fixture](repro/T020_DEMOPERSON_PAIR_G2_NEGATIVES_20261024_00H.json) are archived without upstream original documents; runner needs private owner sources and is not standalone.

---

# 研究E｜T018/T020 DemoPerson 2側初期化とC-NB02 G2三陣営の証拠境界
ID: E-AUDIT-20261024-00H-T018-T020-PAIR-THREESIDE-BOUNDARY-01 / owner E / STATIC CROSSWALK・VERIFY・NOT READY。
## 原本・一次静的資料の固定
- 原作ver0.67 EXE識別SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。今回原作実戦NOT RUN。
- REA新規 2026-10-24 00:43: rea_lab/decomp_task/REA_20261024_0043_P0_DEMOPERSON_PAIR_INIT_ABI_STATIC.md（E側実SHA256 EC0E1D91966008B19C977DF2459B6702AB210DED412C8609FDA0D011370EB493）。
- REA同ID EVIDENCE.json（E側実SHA256 58402D4D09069111BAA4156883DC896C1EE9A00AD82A04CBFEAFDB2E991CD505）。原REAはPC-SAVED-PENDING-READBACK/STATIC/NOT READY。Eが読めてもREA READYへの昇格は不可。
- B-20261024-0015-T013-TROOP-MODE-EXPR-DEDUP-01: data/T013_TROOP_MODE_EXPR_RTTI_DEDUP_NATIVE_20261024_0015.md（E側実SHA256 623ADFC2F53703DC931DD7B8F68FE3E50FE143D0C2F7312F83D785FCFB2549C4、B NOT READY）。
- 既存E: tests/T020_VTABLE_NAMESPACE_DUAL_DEMO_GATE_20261023_2347.md、tests/T020_CNB02_RECEIPT_PROVENANCE_GATE_20261021_2345.md、tests/T018_CNB02_G0G1G2_CHRONOLOGY_20261021_0050.md。過去の既発見を再採番しない。
## 静的根拠を受入条件へ一対一照合
- DemoPerson primary vtable 0x638030 の+0x08(cell 0x638038)=0x514A80。局所ABI ECX=this、stack arg1/source→this+0x14、arg2下位8bit→+0x18、arg3/peer→+0x1C、+0x20=100、RET 12。実クラス・実call完了・+0x20のゲーム上の意味はVERIFY。
- 間接CALL site 0x40F3D6（第1global 0x8B8E58、source 0x8B8E60、side byte 0、peer 0x8B8E5C）と0x40F3F3（第2global 0x8B8E5C、source 0x8B8E64、side byte 1、peer 0x8B8E58）。順序は0x40F320内命令順であって全原作ゲームの動的時系列ではない。
- 0x40D0C6 E8→0x40F320は既存REA資料に存在するが、0x514A80直接E8 caller 0件はvirtual未使用の証明ではない。上位の動的到達、runtime vptr、ALLOC失敗、継続時再利用は未実測。
- B側T013ではTroop+0x30のmode writer 0x569530とcase8 Num/String・同Troop dedupが別の型と経路で確認された。DemoPerson+0x18のside byte=0/1とTroop+0x30 modeを同じ意味・領域として統合しない。
## Eで今回新規確定した『証拠の非同値性』
- 2 DemoPersonとside値0/1の内部初期化は、G2の攻撃/防御/支援の**三陣営**そのものではない。0/1を攻防と断定せず、支援が存在しないとも断定しない。2→3の写像・source pointerの型・実出撃Unit/Troopへの写像はVERIFY。
- +0x1Cの相手DemoPerson参照はordered deployed Troop/Unitの名簿ではなく、+0x14のsource pointerも名簿と断定不可。+0x20初期100をHP、士気、勝率、勝敗のいずれとも確定しない。
- 固定global 0x8B8E58/5Cと同EXE SHAは異PID・異戦闘の同一性を証明しない。E G0/G1/G2の同一run ID・SAVE実バイトSHA・UI操作・MAP・三side・ordered出撃名簿を各別の合法原作receiptで検証。
- G2支援側が合法旧UI観測でいない場合も記録は空配列[]と観測理由を残す。存在/不在を内部のDemoPerson個数から推論しない。
## T020・正式統合・拒否の扱い
- 負例fixture: tests/T020_DEMOPERSON_PAIR_G2_NEGATIVES_20261024_00H.json。機械的出典整合検査のみ可能、実比較runner・原作GameplayはNOT RUN。NOT READYのREA/BをMASTER READYにしない。
- 2026-10-23 23時台までの正式値: checkpoint196／READY596=A115/B229/C136/D116、34 Task DONE9/IN_PROGRESS21/VERIFY4は前回の旧確認値で今回全履歴再集計なし。新正式READY0、旧原作DYNAMIC OBSERVED0、actual Golden PASS0、strict MATCH0。
- T019: GameClear DAT13/TXT2字句範囲差はRESOLVED、script2同名優先・phase flag・TXT実読込・gwrite復帰はVERIFY。新確定矛盾0。
- Historical safety holds remain BLOCKED. Previously refused targets, content and operations are not reproduced here.
- 原本EXE/ZIP/SAVE、A-D/REA/dev_lab、Git/Work/設定/automationを変更しない。次は合法C-NB02同一run G0 UI、G1直前SAVE+入力、G2 MAP・三陣営・実Unit/Troopの一次証拠を優先。
## 今回のE独立実行結果・復旧
- E検証器: tests/t020_demoperson_pair_g2_static_gate_20261024_00H.py をPCで python -B -X utf8 実行。REA/B一次資料実バイトSHA pin 3/3 PASS、REA JSON中のpair ABI・vtable・site/返値など静的12/12 PASS、T020負例ID/期待分類のJSON構造12/12 PASS。
- 12件は判定条件の機械的構造検査のみで、負例を実原作に実行したわけではない。T020 Golden比較runner NOT RUN。真正な旧原作G0/G1/G2 capture無し、G2 actual PASS0、strict MATCH0。
- 本ノート・fixture・検証器はE所有testsへの新規保存に成功し、別操作で全文読み戻し3/3成功。MASTER追記・正式READY採録なし。
- E-OTHER-20261024-00H-T013-MISPATH-01: Bの22H T013資料と推定した名前のread_fileがENOENT。安全拒否ではなくパス推定誤り、PC変更0。Bの2026-10-24 00:15実在文書とHANDOFFに切替えてread-only確認済、未保存差分0。
- 新規SAFETY_REFUSAL=0。旧個別BLOCKED案件・OFFLINE-UNSYNCED暫定26研究は未照合/未同期を維持。
- 受入fixture保存SHA256: 50225630DC6088C2FA14FE0493995DF983074BAE101737F3D7B8CC57BE6C565C。
- E静的検証器保存SHA256: 1DAD0475F624E39573B850EACDBF5D954CA39F80ACBC2B09DEE9D5F2ABDCFCF7。
