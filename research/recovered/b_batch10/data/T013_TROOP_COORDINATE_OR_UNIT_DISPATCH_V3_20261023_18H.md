# T013｜Troop座標指定／Unit参照指定と構成員配送（V3静的差分）
ID: B-20261023-18H-T013-TROOP-DISPATCH-ROUTE-01 / owner B:T013 / 2026-10-23 18時台 JST / STATIC-GHIDRA + PE-VERIFIED-E8 / VERIFY / NOT READY。
PRECHECK: Local Compact接続成功。MASTER checkpoint196/旧READY596、ANALYSIS_LANES_PROTOCOL、LANE_B_HANDOFF、T011/T012/T013/T024/T028と既存未同期台帳を先に確認。
INDEX: CURRENT_ACTIVE_RESEARCH_STATE_LATEST.jsonはV3を現行標準に指定。verify_active_research_state_v3_20261022.py=PASS_ACTIVE_V3_STATIC; hashes14; E8=44889; JMP=6324; errors=[]。原作実機NOT RUN。
原作対象EXEのSHA256（既存manifest値）: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。今回は原EXEの直接ハッシュ／新ASM逆アセンブルなし。
既知との差分: B-20261023-1519/1618/1708の0x569280→0x569360→Troop vtable+4の経路は再計上0。今回の新対象は0x569050/0x569730/0x569880という座標・構成員配送層。
STATIC V3 Ghidra 0x00569050: param_1==0の枝はTroop候補+0x48=0、+0x4C/+0x50へ2座標候補を設定する。2座標の一方がsentinel -0x7FFFFFF8 (0x80000008)なら0x569730呼出へ進まない制御フロー。
STATIC V3 Ghidra 0x00569050: param_1!=0の枝はTroop候補+0x48に対象Unit参照候補を設定し、+0x4C/+0x50を0にする。対象Unit候補+0x220/+0x224を読んで0x569730へ渡す。
PE V3 E8: 0x00569080→0x00569730 bytes E8 AB 06 00 00、0x005690B6→0x00569730 bytes E8 75 06 00 00。それぞれ別分岐。0x004B5211→0x00569050もE8 3A 3E 0B 00。
STATIC V3 Ghidra 0x00569730: Troop候補+0x0C/+0x10の4byte構成員ポインタvectorに生存候補(Unit+0x1867C==0)が無ければ早期return、条件成立時に0x5699C0で候補を作る経路。
PE V3 E8: 0x005697B1→0x005699C0 (E8 0A 02 00 00)、0x005697E5→0x0047BB50 (E8 66 23 F1 FF)。一時配列をソートしてから処理する経路を確認。comparator LAB_00567EC0はGhidraのDATA参照であり、独立関数としての同定は未完了。
STATIC V3 Ghidra 0x00569730: 後段のUnit候補には+0x1867C==0が必要。引数フラグ候補param_6 !=0のときはUnit+0x1F9==0も必要。param_6==0ならこの局所+0x1F9条件を免れる。
STATIC V3 Ghidra 0x00569880: sibling構成員配送も+0x1867Cのチェック→0x5699C0→0x47BB50のsortを持つが、wrapper局所には+0x1F9分岐が見えない。別経路・callee自身の追加filterはVERIFY。
VERIFY: 0x00569050/0x00569730/0x00569880のABI・レジスタ入力、0x5699C0による生成リスト意味・順序、sorting comparator・RNG消費、0x1F9 flag意味、下流Unit動作は未確定。擬似Cをソース／フックABIとみなさない。
DEDUP: B-owned T013_AI.md、T013_WORK_NORMAL_AI_CONTRACTと最近のHANDOFFを照合。既存0x5769B0単体gateと過去禁止されたXREF探索は既知のまま。今回の差分は0x569050の二つのtarget指定モードと0x569730/0x569880フィルタ違い。
RECOVERY/PROCEDURAL: このrunで既存B資料の禁止一覧を完全確認する前に、誤って0x5769B0 callersのread-only queryを1回発行。後からB-RC-20261012-1920-XREFがBLOCKEDと確認したため、その出力は新規証拠として採用せず隔離、追加検索も再試行も行わない。B-RC-20261023-18H-T013-XREF-SCOPE-01。
UNSYNCED: オフライン研究10件、02時Library訂正版2件、14:14安全拒否研究本文は引き続き未統合/未保存。拒否済コード・コマンドの再提出無し。新規READY0、MASTER統合0、DONE0。
GOLDEN DESIGNED/NOT RUN: 無改変同一原作EXE・DAT・SAVE・MAP・seedと入力。Troop対象を座標指定/Unit参照指定で切替、座標sentinel有無、構成員数0/1/3、+1867C/+1F9の組合せを観測。候補順・配送対象・可視移動とRNG順・state変化を同一runで記録。原作Gameplay PASS0、strict MATCH0。
NEXT: 拒否済XREFに非介入のまま、0x5699C0の合法な計算出力形式と0x569730/0x569880のABI差を独立read-onlyで確認。T024/T028への実副作用は依然VERIFY。
BOUNDARY: B-owned data/とLANE_B_HANDOFF以外への書込0。MASTER/原本/REA/dev_lab/他lane/Git/Work/schedule/設定変更0。