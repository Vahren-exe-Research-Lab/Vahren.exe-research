# B-20261028-13H-T028-NULL-ECX-CALLSITE-MATRIX-01｜0x497BB0のnull出力vector引数producerを6 CALL siteで分類
Owner: B / T028。2026-10-28 13時台 JST。STATIC-ORIGINAL-PE-ASM / STATIC-V3-GHIDRA / INFERRED / VERIFY / NOT READY。新READY0、E MASTER統合0、Task DONE増0。
## PRECHECKと未同期
Desktop Commander Local CompactでMASTER最終E正式checkpoint196/READY596（旧確認値）、ANALYSIS_LANES_PROTOCOL、LANE_B_HANDOFF最新12H、B5 owner T011/T012/T013/T024/T028、未同期復旧索引/RECOVERY_HUB、legacy README/BUILD_MANIFEST、CURRENT_ACTIVE_RESEARCH_STATE_LATESTを読取。10/25 14HのOFFLINE研究全文・他lane意味的重複は依然VERIFY/未同期で統合しない。既拒否VA 0x5710C0..0x571500、0x58021E..0x580340及び拒否済みコマンドは不実行・非迂回。
原作ver0.67 EXE rea_lab/targets/hakushin067_Vahren.exe: 現物2910720B、SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。現行V3 search_current.py callers 0x497BB0 は6 E8_DIRECT_CALLを列挙。現行V3 SQLite 135110656B 実SHA256 0B057C43D30EAEC74588C84CF7E09AA7A488BD0FF170925591953EF578AFCB25、sqlite immutable read-only quick_check=ok。active.lockの2候補なし、Java/Ghidra無し。原本実行/Ghidra全面再解析0。
## 今回の新しい原作CALL site分類
| CALL site → 0x497BB0 | 直前のECX producer | ECXの静的状態 | 前段/到達制約 |
|---|---|---|---|
| 0x494233 | 0x49422F XOR ECX,ECX | **0** | 0x49421B..2Eで候補・他引数準備 |
| 0x494618 | 0x49460F LEA ECX,[ESP+0x98] | **非NULL** | stack上の一時vector参照、11Hと同一既知経路 |
| 0x495120 | 0x49511C XOR ECX,ECX | **0** | 0x495104 CALL 0x467DE0→0x495109 TEST EAX/EAX、0x49510B JEでmissはCALLを飛ばす |
| 0x49516A | 0x495161 LEA ECX,[ESP+0x98] | **非NULL** | stack上の別vector参照、11H既知経路 |
| 0x497781 | 0x497779 XOR ECX,ECX | **0** | 0x497768 candidate+0x7A==0のみ、0x49777B candidate+0x1B0=0を先に書込 |
| 0x49BCF6 | 0x49BCF2 XOR ECX,ECX | **0** | 0x49BCDF..F1で候補・引数準備。cleanup様の上位関数0x49B5C0内 |
6個の直接CALLに対して **ECX=0が4 site、LEA stack非NULLが2 site**。これは静的にnull引数供給経路が実在することを示すが、条件付きCALLの実Gameplay到達は別問題。ECX=0の4 siteから0x463590が無条件に呼ばれるという断定は禁止。
## callee内の追加gateと解釈限界
0x497BB0 の既12H原作ASM: 0x497C0D CMP BYTE [candidate+0x77],0 と0x497C12 CMP BYTE [candidate+0x75],0 の**両方0**の枝だけ0x497C17でECX==0を検査。ECX==0なら0x497C21 CALL0x463590→owner索引整理・候補破棄の経路へ、ECX!=0なら0x497C31 CALL0x4C1290でvector append。flags非0の場合は別経路であり、破棄確定ではない。
0x495120は名前解決hit後しかCALLしない一方、0x497781は+0x7A=0で+0x1B0=0にした後CALLする。+0x7A条件から+0x75/+0x77が両0とは証明できない。0x49BCF6についても指示通り実行/原作Golden未実施。特に4つのnull producerを単一の死亡・敗走意味論に統合しない。
前11Hの0x494618/0x49516A LEA nonnullと12Hの0x497C21 callee清掃は既知で再計数0。今回の新規差分は、V3索引6 callerの**全列挙と4 XOR / 2 LEA の原作前段producer分類**、および0x495120 hit gate / 0x497781 +0x7A gate・事前 +0x1B0書込の接続。
## 原作native検証
x86-32 capstoneを原作PEの固定VA→RVA→RAW範囲で限定解読、REL32の6 CALLを直接再計算し6/6一致。callee既12H 0x497C0D/+0x77、0x497C12/+0x75、0x497C17 null gateは前回の証拠を引継ぐ。
原作窓: 0x495101長36B SHA256 9C7C78DB4216B58F28735C20128F15F7D2F97A3D41961CBB8841AD27DA48B45B、0x497761長37B SHA256 56FB29EF6E893BFED583726D9BC7F616514A0255C936D93E6B40A49E90208737、0x49BCDF長28B SHA256 E72F431AF5016524527879B8B022CF0C090E9B53F58858EDA1867AD6C4E23D9B。
0x49460A長19B SHA256 80C1C5F25DD7BE21519094EE49873B94F6C1D841A6C8E803B76E24B9DF3EBB9C、0x49515C長19B SHA256 609B7AE86A8AE97BC1CEB19186CD608B6ED9F80DB274071CEF6919A0B9ACE91C。
B所有data/exe T011/T012/T013/T024/T028 Markdown＋HANDOFF 327件の今回主要site 11 literalに先行一致0。10/25 OFFLINE全文/他ownerの完全意味的重複はVERIFY。V3擬似CはABI未検証、原作ASMのレジスタ値を優先。
## GOLDEN／次P0／境界
原作無改変EXE＋X20改変前DAT、同SAVE/MAP/入力/RNGで6siteの合法到達・candidate+75/+77/+7A・+1B0の前後、0x463590のowner木清掃・candidate寿命と可視結果を同run観測するまでDESIGNED_NOT_RUN。原作Gameplay Golden PASS0、strict MATCH0、正式READY0/E MASTER0/DONE0、NOT READY。
次は4 null producer各siteの+75/+77の到達状態・上位呼出条件と0x463590副作用の範囲。第2集合真consumer、T028士気敗走、T013最終target、T024戦闘AI、T011召喚親子もP0。元EXE/DAT/ZIP/SAVE、MASTER、他lane、REA/dev_lab、Git/Work/設定/schedule不変更。