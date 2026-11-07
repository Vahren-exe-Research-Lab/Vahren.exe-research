# REA-LOCAL-20261024-08H-P0-NESTED-MAP-NONEMPTY-TRANSFER-STATIC-01
2026-10-24 08時台 JST / owner REA / P0 / PC-SAVED / STATIC / VERIFY / NOT READY

## 前提・非重複照合
- MASTER_LEDGER、ANALYSIS_LANES_PROTOCOL、REA README/QUEUE/PROGRESS/WAVES、既存runs一覧、最新sync、検索README/BUILD_MANIFEST、07H成果とREADBACKを先読。新規Ghidra/REA実行は行わず、旧証拠を上書きしない。
- 前回07Hは「0x47D770→0x47D9B6正常到達では外側入力0xB136A8に最低1ノード」を静的確認。本08Hでは未検証だった**そのノードの +0x18（内側treeの件数）**に焦点を当てた。
- 既存Wave1〜5=64/64は `logs/progress_sync_20261011T153958076Z.json` の既存値。QUEUE/PROGRESSはEPERM stale、新規VERIFIEDへ転用しない。
- 承認済み隔離EXE SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
- search.sqlite SHA256 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF（BUILD_MANIFESTと一致）。

## 新規発見A：0x47D770の一時「内側tree」は空で生成した後に1件挿入
- 0x47D86C XOR ESI,ESI、0x47D8B5の一時tree件数=0、0x47D8C9/D3/DAでhead自己リンク、0x47D8E8でhead+0x11=1。
- 0x47D8FE CALL 0x565780で0x14-byteの候補ノードを生成、0x47D908でEBXに一時treeアドレスを設定、0x47D90C CALL 0x5158E0。
- 初期空treeでは0x5158E8のhead、0x5158EEのsentinel判定から0x515923 CL=1 → 0x51592Aのhead比較 → 0x51593A CALL 0x40EBE0へ到達する分岐。
- 0x40EC03 INC ECX / 0x40EC04 MOV [EDI+8],ECXが内側tree要素数を増加。初期0なら通常挿入後に1。
- この推論は割当成功・例外なし・該当call経路正常終了を前提とする静的制御フローであり、原作ゲームでの動的追跡ではない。

## 新規発見B：内側tree件数は外側ノード+0x18へ伝播する
- 0x47D91E CALL 0x476700は一時treeを出力へ複製。0x476712 CALL 0x47BA10 → 0x47BA7B CALL 0x476B20。0x476B39 MOV ECX,[EBX+8]、0x476B3F MOV [ESI+8],ECXで複製先のcountを元treeから設定。
- 0x47D932 CALL 0x476A50は0x24-byte外側ノードを作り、0x476AC4でsource内側treeのアドレスを取得して0x476AC8 CALL 0x476C50。
- 0x476C50は一時的に新node内側treeのcountを0にするが、0x476CC9 MOV EDX,[ESI+8] → 0x476CCF MOV [EDI+8],EDXでsource countと交換する（0x476CD2でsource countを戻す）。
- new node+0x10がtree基点、node+0x14=head pointer、node+0x18=count。よって本呼出経路で正常にnodeが作られた場合、**外側ノード+0x18=1**。07Hの「外側に1ノード」は今回「内側件数も1」へ強化された。
- 0x47D942 CALL 0x476720で外側tree 0xB136A8に挿入。0x47D98Aの分岐を越えた0x47D9B6 CALL 0x48F9E0へ渡す。
- 0x48F9E0→0x498E60→0x498F90→0x4991C0は外側ノードの複製。0x499239 CALL 0x47BA10（内側tree deep-copy）によって内側件数を維持する構造。Ghidra擬似Cだけでなく、CALL先バイトを独立照合。

## 新規発見C：0x48F720は内側tree非空判定後に先頭キーを返す
- 0x48F786の比較木フィルタ通過条件の後、0x48F78A CMP [ECX+0x18],0 → 0x48F78E JNE 0x48F7ED。
- 通過時は0x48F7ED MOV ECX,[ECX+0x14]（内側head）→ 0x48F7F0 MOV EDX,[ECX]（先頭ノード）→ 0x48F7F2 MOV EAX,[EDX+0x0C]（先頭キー）→ RET 4。
- 不採択・候補終了時は0x48F7E4 XOR EAX,EAX → RET 4。したがって非NULLを保証するには「外側ノードがある」だけでは不足し、「内側treeに要素あり」かつ「比較treeの除外条件を通過」が必要。
- 本件の0x47D770正常経路では内側件数>0も満たす構造を追加確認。残る主な不確定要素は比較treeによる棄却、実行時再入/副作用、および他の4つの0x48F9E0 caller。
- 0x48F720の返値は通常経路では**内側tree最左ノードのkey**に相当。これをゲーム上のunit/陣営等の具体型と断定しない。

## 検査結果・境界
- 読取専用Capstoneによる原作機械語24/24、E8相対CALL先13/13、合計37の指定静的判定PASS。監査: `REA_20261024_08H_P0_NESTED_COUNT_TRANSFER_AUDIT.py`。
- 件数37は静的判定の件数であり、独立関数37件・REA正式証拠37件ではない。07Hとの既知CALLも検証用として含むが新発見数に加算しない。
- 対象VA: 0x47D770/0x5158E0/0x40EBE0/0x476700/0x47BA10/0x476B20/0x476A50/0x476C50/0x476720/0x4991C0/0x48F720。
- REA正式5種（info/pseudo/assembly/callers/callees）の新規完全セット0、新規VERIFIED0。正式TODO/VERIFY/BLOCKED差分0/0/0。旧EXE実ゲームGolden PASS0、strict MATCH0、完全複製率未測定。
- REA/Ghidra新規実行0、ゲーム実行0。安全拒否なし。PowerShell経由Pythonの日本語パス文字化けでOSError22が1回発生し、作業ディレクトリ基準のread-onlyアクセスに変更して正常解消（安全拒否ではない）。
- 新規RUN_RESULT/QUEUE/PROGRESSは変更なし。PC接続成功、作業前active.lockなし、Java/Ghidra 0件、空きRAM14.25GiB、CPU1%瞬間値。全実行時間は未計測。

## 次のP0
- 0x48F720で使用する比較tree（context+0x1EED34）の要素と、0x47D770で構築した外側keyの対応を追い、正常到達で候補が除外されない条件を特定。
- 0x00521D90→0x008BA6F4入力系と残りcallerの内側tree非空・比較tree除外条件を同じ分類で検証。
- 原本/MASTER/A〜E/T018/dev_lab/QUEUE/PROGRESS/既存runs/Git/スケジュール/Workを変更しない。PC正本へ書込成功・readbackは別途読戻しで確認する。
