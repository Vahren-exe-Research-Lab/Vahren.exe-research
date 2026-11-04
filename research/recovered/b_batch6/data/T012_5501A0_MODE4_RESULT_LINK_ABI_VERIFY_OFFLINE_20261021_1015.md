# 迫真戦記 新B｜T012 0x5501A0 mode=4 の生成結果・リンク更新境界（2026-10-21 10:15 JST）

- 研究候補ID：`B-OFFLINE-20261021-1015-01`。復旧ID：`B-RC-20261021-1015-LOCAL-SESSION-01`。担当：B/T012（T011召喚・経験値に参照）。
- 状態：`STATIC-SAVED-GHIDRA-PSEUDOC / INFERRED-BRANCH / VERIFY / OFFLINE-UNSYNCED / NOT READY`。新規B正式READY 0、E MASTER統合0、原作Gameplay Golden PASS0、新旧strict MATCH0。
- 参照元：ユーザー添付 `HAKUSHIN067_AI_OFFLINE_PACK_20261021(1).zip`（34 entries、CRC全件正常）；`headless_analysis/search_index/BUILD_MANIFEST.json` PASS、`search.sqlite`（53,927,936B、SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`）。対象元EXE v0.67 SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` は検索基盤マニフェスト記載であり、この実行では元EXE実体を再hashしていない。
- CLI照合：`search.py function 0x5501A0 --max-chars 19000 --limit 40`、`function 0x54E7B0`、`function 0x580280`、`function 0x4C22B0`。archive元資料を変更せず一時scratchのsearch.sqliteを読取専用で使用。0x5501A0 擬似C 3,734文字、サイズ621B。

## 新しい局所差分（前回09時台の上位dispatcher発見とは別）

1. `0x5501A0` は生成ループ各回先頭で `iVar3=0` に初期化する。定義オブジェクト `*(int*)(def+0x40)==4` の枝は **site `0x550219` で `0x54E7B0` を呼ぶが、保存済み擬似Cでは戻り値を `iVar3` に代入しない**。一方、それ以外の枝では **site `0x55037F` の `0x580280` 戻り値を `iVar3` に格納**する。これは「生成結果ポインタをこのローカル変数へ捕捉するか」の枝差であって、mode=4で生成が失敗するという証明ではない（STATIC-PSEUDOC）。
2. 定義 `def+0x1D0 != 0` の場合、`iVar3!=0 && manager+0x1F8!=0` のときだけ `new+0x194=oldHead` と `oldHead+0x198=new` を実行し、**その後の `manager+0x1F8=iVar3` 自体は毎回実行**する。従って擬似Cを字義通り解釈すると、mode=4では `iVar3=0` のまま head が0へ変わる候補経路がある。既存 head の対象オブジェクト解放や実際の表示消去は本体からは証明できない（INFERRED/VERIFY）。
3. 種類を問わず、上記枝の後で `manager+0x1F0` を +1 して `def+0x74` と比較する。すなわちローカル制御フロー上の **試行回数カウントは `iVar3` がNULLでも進む**。`def+0x78 != 0` なら上限未達時にreturn、`def+0x78 == 0` なら同じ呼出内のwhile反復へ進む。初回のカウントがすでに上限以上なら最初の1回後に終了経路へ行く。これは生成された個体数と同数という確証ではない（STATIC-PSEUDOC）。
4. 解除 site `0x5503F9 → 0x4C22B0(managerItem,0)` は **既存正式B-20261013-1239-01** が `Manager EAX` の active/pending vectors を解除し、deferred appendしない (`arg2=0`) と保存済みASMで確認済み。今回はこの下位関数を新規発見として再計上しない。解除後 `managerItem+0x1D0` のbyteを0へ変更するのは `0x5501A0` 本文による。登録解除とゲーム上の削除、死亡、経験値移転は異なる事象（VERIFY）。

## ABI・到達性に関する未解決境界

- `0x5501A0` のデコンパイル上、呼出 `0x54E7B0` に表示される実引数は4個だが、`0x54E7B0` 側の自動復元signatureは `void __fastcall(...6個...)` になっている。Ghidraの型・隠れレジスタ引数・戻り値推定が不整合となり得るため、**「mode=4の物体をリンクしない」「+0x1F8を必ず消す」を原作命令上確定するには許可された保存ASMで site前後のEAX/stack/write命令を独立確認する必要がある**。最新PC資料未照合のためここではNOT READY。
- この検索DBの`calls`では `0x5501A0` への直接callerは0。付属`DATA_POINTER_REFS.jsonl`で `0x005501A0` の文字列一致0（参照表は4,358件）。間接CALL/vtableからの到達・実戦での動作は否定できない。実機DYNAMIC OBSERVED0。
- `def+0x40=4` のゲーム内名称、「召喚」との厳密対応、旧オブジェクトの `+0x194/+0x198` 残存、HP/MP、EXP、RNG、間接callers、type分岐のASMはVERIFY。拒否済み `0x5710C0..0x571500` や既拒否証拠はこの調査では一切解析しない。

## 既存ID・回収境界

- 09時台のPC限定非READY `B-20261021-0910-01` は上位周期・mode switch・linked fields・解除callを既報告済み。今回の増分は **mode=4とnon4でのローカルresult捕捉差、NULLでも試行回数カウント、mode4 result=0に伴うリンク更新候補、callee自動signature相違** の4点。既存 `B-20261013-1239-01` をREADY再計上しない。
- 02～08時台7研究資料は09時台のPC存在監査で全件ENOENT（当時の報告であり本run再実査なし）。09時台の08文書PC同期・B HANDOFF追記には安全拒否があり、元操作再提出・別tool/path/クラウド迂回は行わない。先行 `B-OFFLINE-20261021-0200-01` のPC状態は09時台ENOENT報告に従い、今回の最新確認ではない。復旧メタデータのみ引継ぎ、元拒否payloadのコピーはしない。
- 今回Local初回PC MASTER read (`[RESEARCH_ROOT]\MASTER_LEDGER.md`) が `INVALID_ARGUMENT: Error code: INVALID_ARGUMENT; Error: McpServerError: Session terminated`。`CONNECTION`（安全拒否ではない）。PC TASK QUEUE・最新checkpoint・B予約・PC未同期の最新状態・PC CPU/RAMは未確認。最後に会話で確認されたcp195/予定595は過去値で、現在値と主張しない。HANDOFF・MASTER・Git・他lane・REA・dev_lab・原本・設定・automation書込なし。

## Golden検証／再開位置

- 検証は合法的に発火させた同一旧原作 ver0.67 EXE SHA / DAT SHA / SAVE SHA / map /入力 /tick /可能ならseedと、新実装build SHAを分離して採る。mode=4/非4、def+0x1D0=0/1、既存 `manager+0x1F8` NULL/nonnull、`0x580280`結果NULL/nonNULL、interval=`def+0x78` 0/1/正値、limit=`def+0x74` 1/複数について、実生成個体数・active/pending registry・link(+194/+198/+1F8)・counter(+1F0/+1F4)・visible action / HP/MP / EXP / RNGを区別して対照。Game Golden未実施、条件到達不可はUNKNOWN。
- 次回優先：PC再接続時はまず未同期回収と拒否メタデータの最新重複・予約照合、**今回のB独立研究メモがPCにないか先に確認してから**一度だけ取り込む。独立技術照合は `0x5501A0` mode4の `0x550219` 前後・`0x55037F` 後の安全な既保存ASMと `0x54E7B0` 呼出規約、0x5501A0間接caller。安全拒否済み操作・VAの再試行不可。
- 保存計画：この1件をChatGPT Library `/迫真戦記再開発プロジェクト/data/` に保存・独立readback。できなければPC未保存・クラウド未保存と明記する。
