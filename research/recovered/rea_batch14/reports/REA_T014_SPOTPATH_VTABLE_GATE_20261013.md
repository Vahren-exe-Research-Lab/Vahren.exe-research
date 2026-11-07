# REA T014 — SpotPath / SpotEscapePath のvtable別 Task・Render 分岐条件（2026-10-13）

## 判定と範囲
- Status: SAVED-NATIVE STATIC CLASS-BINDING / VERIFY（実callsiteのdynamic型・manager下位効果）。新規REA/Ghidra取得ではなく既存保存native・RTTI資料からの独立追加確認。
- 対象: ver0.67承認済みコピー SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、研究T014（関連T015/Task登録へは参照のみ）。原本・他ownerは変更しない。
- 前回の `REA-RC-20261013-0644-RUNTIME-NOTE` は新規runtime lifecycle文書の保存拒否であり、その元要求の再提出・代理保存はしていない。本資料は**それ以後に取得したクラス固有vtableとcallee returnの追加照合だけ**を対象とする。

## 一次保存証拠
- `exe/T014_SPOT_PATH_VFUNCS.txt`: SHA256 F95EF8CC0ECDFAE026F2B873C735C9B69F37689265F392CE1720110C6A77E23F、保存VA `0x5B0120..0x5B03DB`。
- `exe/T014_SPOT_PAYLOAD_PROBE.txt`: SHA256 CE130D8432D239AE7E553C9D16F6F203D0130DBD547EFF83A447A5B91CEB9E1F、RTTI `SpotPath` vtable 0x6387F4／`SpotEscapePath` 0x638864。両typeの+0x54=`0x5B0120`、+0x58=`0x5B0250`。
- `exe/T010_BATTLE_FRAME_ORDER.md`: SHA256 567D87BB18B753D8D2B908065B4884FE3BCC0D9D1767F5C43153BB120100A5AC、共有callee `0x43B5A0=raw AL0` の保存Cに基づく照合。これを別クラスに無条件一般化しない。
- この3資料の読み取り専用PowerShell局所検査は **15個の構造assertion一致／不一致0**。これは文字列・static callsiteの整合であり、旧ゲーム実機の15ケースPASSではない。

## 具体クラスが解決された場合のcall経路
| Vtable slot | SpotPath 0x6387F4 | SpotEscapePath 0x638864 | 呼出側の直接効果 |
|---|---|---|---|
| +0x08 | `0x43B5A0` / AL0 | 同左 | 登録5B020D、解除5B02ECのTask条件はfalse |
| +0x34 | `0x4BBBD0` | 同左 | 解除5B02E1で呼出。callee作用は保存疑似C範囲に限定 |
| +0x44 | `0x43B5A0` / AL0 | 同左 | 解除5B037Cで呼出、返ALは検査しない |
| +0x48 | `0x43B5A0` / AL0 | 同左 | 登録5B0226・解除5B0368のRender条件はfalse |
| +0x54 | `0x5B0120` | 同左 | 登録処理の実体 |
| +0x58 | `0x5B0250` | 同左 | 解除処理の実体 |

- `0x5B0120`: `0x5B020D`でvtable+8のAL0→`0x5B020F JE 0x5B021D`、従って条件付き`0x4C2240` Task登録呼出を**実行しない**。`0x5B0226`でvtable+48のAL0→`0x5B0228 JE 0x5B0234`、従って`0x4C3DC0` Render登録も**実行しない**。その後`0x5B0239`の`0x4BC920`空間索引登録は引き続き到達する（下位の成功・重複方針はVERIFY）。
- `0x5B0250`: +34呼出後、`0x5B02EA`の+8がAL0→`0x5B02EE JE 0x5B035F`でTask active tombstone/待機配列stable eraseへの局所経路を丸ごとskip。+48もAL0→`0x5B036A JE 0x5B0375`で`0x4C3E40` Renderリスト解除をskip。ただし+44呼出後、`0x5B039C`の`0x4BC3C0`による空間セル検索と`0x5B03C5..0x5B03D5`の最初一致tail-swap除去は残る（cell不在・対象不在ならreturn）。
- 同じ関数を使用する他の派生型や異なる動的vtableへこの結論を無条件適用しない。原作GUIに「非表示」と解釈せず、spatial・相互adjacency・その他副作用とは区別する。

## 追加した入口ガードの判別
- `0x5B0123`でbyte[this+0x88]を検査。非0かつ第一stack arg low byte=0なら`0x5B0131 JE 0x5B0241`で**全登録処理を早期return**する。
- 非0でも第一stack arg low byte!=0ならこの早期returnを通らない。backlinkの重複検査はある一方、空間登録`0x4BC920`にはcallが到達するため、下位関数のdedup保証なしに「必ず一度のみ」と断定しない。
- `0x5B0250`には同じ+0x88の入口ガードが見えない。再入・二重呼出への正規上位gateはVERIFYで、解除を二重実行しても常に安全と仮定しない。

## 安全・残課題
- `0x5AFB30`の本体命令は保存exe資料の今回検索で未発見（確認callsite: `0x5AFAD5`, `0x5B05B3`, `0x5B05C8`）。この関数と`0x5B0120`/`0x5B0250`の直接caller-callee関係は未確定。既存callee情報は `0x46F4C0`へのxrefsを示すだけである。未知calleeの返値や実効果を注入しない。
- `0x5710C0..0x571500`の安全拒否済み逆解析、既往拒否text exporterや前回拒否文書の代替実行なし。原本ZIP/EXEの実行・編集0、Ghidra新規run0、REA新5-method evidence ID0、その他研究・Git・設定・schedule変更0。
- Wave1=16/16、Wave2=10/10、Wave3=10/10、Wave4=12/12、Wave5=16/16、計64/64 STATIC（P0 29/29・P1 35/35）。Wave6正式0/16、P0候補5/P1候補11、未着手16・関数単位VERIFY0。MASTER checkpoint94、研究DONE9/34、旧EXE実機golden PASS0。ゲーム再実装率は未測定。QUEUE/PROGRESSは既存rename EPERMの古い表示を維持。
- 次の重点は `0x4BC920`の空間登録時重複方針と、`0x5AFB30`の既存の呼出証拠・callee境界。既往拒否で未承認の本文取得は別手段で反復しない。

## 2026-10-13 08時台 — 空間索引登録 0x4BC920 / セル取得 0x4BC3C0（REA-T014-SPATIAL-20261013-0834）
- [SCOPE] T014（関連T015/T010は参照のみ）。本節は従来のSpotPath/EscapePath vtable調査後に、新しく許可された**承認済みEXEコピーの限定read-only x86逆アセンブル**から得た局所契約。前回拒否された別名runtime lifecycle新規文書の代替作成ではない。対象copy SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187は開始時・局所disasm開始時一致。原本ZIP/EXEには触れていない。
- [PRIMARY] コピー `rea_lab/targets/hakushin067_Vahren.exe`、PE32 image baseからVA→file offsetを解決しCapstone 5.0.7で `0x4BC920..0x4BC9AF`（file offset0xBBD20）と `0x4BC3C0..0x4BC4E6` のみ閲覧。新しいREA/Ghidraのinfo/pseudo/assembly/callers/calleesの5点取得ではなく、本関数の新VERIFIED昇格0。保存済みcallerは `exe/T014_SPOT_PATH_VFUNCS.txt` 0x5B0234..0x5B023E、および `exe/T015_SPOT_DISPLAY_VTABLE.txt` 0x5A895D..0x5A8967。両者ともpush object→push(world+8由来manager)→CALL 4BC920。旧A/他owner資料は読み取り専用。
- [ABI] `0x4BC920` はstack arg1=spatial manager(Ebp)、arg2=object(EDI)、RET8。obj+40/+48からcenterX、+44/+4CからcenterYをsigned差分SAR1で算出する。signed32 wrap・負奇数のSAR丸めを勝手にfloat平均へ置き換えない。
- [CELL] `0x4BC943 PUSH 1; 0x4BC947 PUSH EBP; 0x4BC948 CALL 4BC3C0`。calleeはECX=centerX、EAX=centerY、stack(manager,createFlag=1)を受ける。通常gridでは負座標判定とmanager+2C shift、+10上限、+C tile tableから16byte幅のcellを返す。grid外は座標正規化とtree lookupを経て、未登録時createFlag=0は `0x4BC47B XOR EAX,EAX; RET8`、flag非0は `0x4BC487 PUSH 0x10; CALL 5B6C2B` から新規16byte cell確保/挿入枝へ。tree internalsとallocator例外はVERIFY。4BC920の正常登録callではcreateFlag=1を明示する。
- [VECTOR] 4BC920のcell戻りをESIに保持。cell+[0,4,8]をbegin/end/capとして扱い、end==capなら `0x4BC972 CALL 4C12F0` で容量経路へ進む。stack上の引数pointerがvector backing内を指すaliasケースと通常の外部pointerケースを区別するが、**既存vector要素の値がEDIと等しいかを走査する比較は本関数内に無い**。
- [APPEND] 通常非alias枝では `0x4BC99A MOV [EAX],EDI` を実行し、共通 `0x4BC99C ADD DWORD [ESI+4],4` に合流。容量helperの戻り、null/例外時の成立条件は別VERIFY。この局所処理はオブジェクトの同一ポインタ再追加を**自身ではdedupしない**。したがって上位guardやcell層の別制限がなければ重複が起こり得るが、実ゲームで重複が発生したとは主張しない。
- [COUNT] `0x4BC9A0 MOV EAX,[EBP+8]; 0x4BC9A3 INC EAX; 0x4BC9A4 MOV [EBP+8],EAX; 0x4BC9A7 MOV [EDI+0x54],EAX`。manager単位の32bit登録カウンタを1増やし、同値をobject+54へ格納する。これをゲーム内時間・優先順位・グローバルIDと呼ばない（実consumer VERIFY）。連続登録時はoverwriteされる。
- [REIMPLEMENT] 5B0120登録入口のobj+88/flag早期return、既存backlinkの重複検査、4BC920セルvector appendは**別段階**。backlink内の重複排除だけから空間セルの一意性を推論しない。登録と解除(4BC9C0等)のcell選択・first-match・counter/obj+54を別traceとし、同一object再登録、位置変更、同一cell重複、外部cell新規作成のケースを比較する。合成テストはDESIGNED/NOT RUN。
- [SAFETY FAILURE RECEIPT REA-RC-20261013-0837-4BC920-HASHCHECK] 上記許可済み単独disasm後、4BC920/4BC3C0の関数byte SHAと15個のdisasm markerをまとめて検査する新規Local start_process要求は**実行前にplatform safety拒否**。拒否メッセージ「This tool call was blocked by OpenAI's safety checks」。当該追加SHA/15 assertionは取得0・PASS0、再提出・別shell/tool/pathで代替計算しない。最後の成功状態はコピーの全体SHA一致、2関数の許可済みread-only disasmと上の局所命令照合。次に必要なのは独立した正式承認の有無確認であり、この節の保存をもって拒否済み追加検査を成功に変えない。
- [STATUS] PARTIAL-STATIC-CONTRACT/SAVED-IF-READBACK、登録側dedupの局所否定のみ確定。新規5-method VERIFED+0、旧EXE Golden actual PASS0、strict match0。Wave1～5=64/64 STATIC（P0=29/P1=35）、Wave6候補0/16(P0 5/P1 11)。MASTER最新読取checkpoint94、研究DONE9/34。QUEUE/PROGRESSのrename EPERMは既知未解消で実行・syncなし。ゲーム再実装率未測定。原本/他lane/MASTER/T018/dev_lab/Work/Git/設定・automation変更なし。
- [NEXT] 許可済み証拠で 4BC3C0 tree cell新規登録と4C12F0 vector grow／0x4BC9C0解除の重複1件だけの意味差を整合。上位5B0120のflag=1再登録で実際に二重到達するcaller条件、空間grid外の実到達・heap成功はVERIFY。新Ghidra一式を未取得なら本関数をVERIFIEDへ昇格しない。
