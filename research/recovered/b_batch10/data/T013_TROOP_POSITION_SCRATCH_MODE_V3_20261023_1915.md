# T013｜Troop目標座標候補の生成・共有scratch・mode分岐（V3 STATIC）
ID: B-20261023-1915-T013-TROOP-POSITION-SCRATCH-01 / owner B:T013 / 2026-10-23 19時台 JST / STATIC-GHIDRA + PE-VERIFIED-E8 / VERIFY / NOT READY。
PRECHECK: Local Compact接続成功。MASTER最後のE正式cp196/READY596、規約、B HANDOFF、B5 owner文書、未同期回収台帳と既安全拒否を先読。現行標準V3使用、旧10,268/47,550は歴史値。
BASELINE: 原EXE ver0.67 SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（今runは既manifest/擬似Cヘッダ値であり現物SHA再計算なし）。原EXEは実行/変更なし。
PROVENANCE: search_current.py read-only V3 function 0x5699C0, 0x569730, 0x569880; callers/callees 0x5699C0。cached Ghidra擬似Cは ORIGINAL_20261020_GHIDRA_PSEUDOC_UNCORRECTED、verified_abi=0。
NEW CALL EDGE: 0x5697B1 (in 0x569730) →0x5699C0 / E8 0A 02 00 00、0x569904 (in 0x569880) →0x5699C0 / E8 B7 00 00 00。V3は2/2 independently_verified_target=1。18時台の0x5697B1は既報なので新規計上は sibling 0x569904 の独立照合のみ。
NEW GATE: 0x5699C0はTroop候補+0x0C/+0x10の4-byte構成員vectorを走査、Unit+0x1867C==0と追加フラグ時Unit+0x1F9==0の候補を0x4C52D0を介して一時リンク構造に収める。後段は適格候補なしで生成処理をskip。既18時の同フィルタは再計上0。
NEW MODE: Troop候補+0x30==1、==2、それ以外の3分岐を持つ。mode1ではTroop+0x38を候補数側の上限として読む条件が存在。mode2/その他の分岐には0x5E3B70→0x5B6ED0とFPU丸め候補がある。式・ゲーム上の名称・signed/float幅はVERIFY。
NEW ROTATION: 生成経路でD3DXMatrixRotationZとD3DXVec3TransformCoordが使われる。角度候補param_6はTroop候補+0x28へ保存される。別の引数フラグ候補param_5で回転適用経路と非回転経路を分ける。正確な入力/座標系/ABIはVERIFY。
NEW SCRATCH: DAT_00B040EC/+F0/+F4は8-byte pairの作業配列のbegin/end/capacity候補。関数入口でendをbeginへ戻す論理clear（capacity再利用）を確認。候補ごとにpairを書き、endを8byte進める経路がある。並行実行/再入時の安全性は未確認。
OTHER STATIC CALLS: 0x569AC5→0x4C52D0 (E8 06 B8 F5 FF), 0x569D14→0x571AD0 (E8 B7 7D 00 00), 0x569DF6/0x569E0C/0x569FAA/0x569FFB→0x5D1B80 はV3 PE照合済。0x571AD0の副作用/RNG量は未確定。呼出し存在だけを確定とする。
WRAPPERS: 0x569730と0x569880は両方0x5699C0→0x46D180→0x47BB50(sort, DATA comparator 0x567EC0)へ進む。後段の選択順・配送意味・最終Unit移動はVERIFY。0x5769B0の呼出先・XREFを新規検索せず、既拒否境界を保持。
INFERENCE: 生存Unitを列挙→+0x30モード別に配置候補pairを生成→共有scratchへ積む→wrapper側ソート、という段階分離と整合。ただし現在の擬似Cは型/レジスタが不正確で、実座標個数や正規のポジショニング規則を固定しない。
DEDUP: 旧B-20261023-1519 (+34集計)、1618 (+34利用)、1708 (Troop RTTI/比率)、18H (座標vsUnit入力とwrapper sort) は再計数0。今回の独立増分はproducer 0x5699C0の+30モード/+38 cap・+28角度・8-byte scratch寿命と2番目のcallerのPE確証。
RECOVERY: B 03–12時オフライン研究10件は未同期、02時Library訂正版2件未反映、14:14安全拒否detail未保存。B-RC-20261023-18H-T013-XREF-SCOPE-01など旧拒否を再試行・迂回しない。別owner/MASTER/REA/dev_lab/Git/Work/設定/automation書込なし。
GOLDEN DESIGNED NOT RUN: 同EXE・無改変DAT・SAVE・MAP・seed/入力でmode +30=1/2/other、+38=0/1/3、構成員0/1/3、+1867C/+1F9状態、角度0/非0、対象座標と回転flagを変え、生成pairs/順序/配送先/可視移動・RNG cursorを観測。現時点原作Gameplay PASS0、strict MATCH0。
NEXT: 許可済み領域で0x567EC0 comparatorの型とsort key、0x571AD0の既保存意味、+30 writer・+38 setterをB既証拠と静的接続。ABI/FPU正確化、原作Golden受入はVERIFY。
STATUS: 新B READY0、E MASTER統合0、Task DONE0。保存・readback結果は後続HANDOFFに明記する。
