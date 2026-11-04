# 迫真戦記 新B / T011｜member展開から生成helperへ戻る条件付きCALL cycle（2026-10-21 05:10 JST）

- 研究候補ID: `B-OFFLINE-20261021-0510-01`（新規正式READY証拠IDではない）／owner T011、経験値初期化T012の影響はVERIFY。
- 状態: `STATIC (call graph and saved Ghidra pseudoc) / INFERRED (meaning) / VERIFY / OFFLINE-UNSYNCED / NOT READY`。当回B READY+0、E MASTER統合+0。
- 接続RECOVERY-ID: `B-RC-20261021-0510-LOCAL-429-01`。Local CompactのMASTER読取は `UNAVAILABLE: Error code: UNAVAILABLE; Error: McpServerError: MCP SSE probe returned 429 from openai.org`。CONNECTION/RATE-LIMIT系・一時障害であり、安全拒否ではない。PCへ新規書込0。Remote/別shell/path迂回0。
- 証拠源: 添付 `HAKUSHIN067_AI_OFFLINE_PACK_20261021(1).zip`、ZIP SHA256 `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`、CRC全34 entry PASS。`search.sqlite` SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`（BUILD_MANIFEST一致）。SQLite readonly immutable、未実行のGhidra保存擬似C ZIPを照合。
- 対象EXE SHA256（パックのマニフェストの記録、今回原本から再測定していない）: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。収録研究スナップショットは最新PC正本ではない。
- 擬似C: `functions/0058/00582D90.c` SHA256 `0C97A9F541E871B941734CAC55644C0E68E80566BE16D84D9D8B641F690FED8E`、`functions/0046/00466F60.c` SHA256 `32E0C2CA4CC5747F450E40F5250FCB02B430D0240CD3D31D599BA93AD07A98E4`。両関数のSQLite code と収録Cファイルは文字単位一致。

## 観測A: 0x582D90のmember条件付き走査（STATIC）

1. `0x00582D90`は`param_5 != 0`の場合にのみ、設定キー文字列`"member"`を使うレコード/ポインタ範囲を作り、件数`((end - begin) >> 2)`で要素を走査する形が保存擬似Cにある。参照レコードの意味（編成member / 定義member / 他）は未確定。
2. 要素ごとに`0x00583506 → 0x00467DE0`を呼び、返った`iVar5`が0、**または** `*(char*)(iVar5+0x77)==0 && *(char*)(iVar5+0x75)==0`の場合だけ、`0x00583546 → 0x00466F60`を呼ぶ。返値ありで片方以上のbyteが非0なら、この局所分岐では生成helperを呼ばない。
3. 直後に`0x00583557 → 0x00415530`へ進み、member loop終了後に`0x00583585 → 0x0058AFA0`を呼ぶ。`0x00415530`と`0x0058AFA0`のゲーム上の副作用は未特定。上記は条件付きの**制御フロー**であり、生成対象や既存探索の意味はINFERRED/VERIFY。
4. `0x005832CF → 0x0058B7F0`（前回B-OFFLINE-20261021-0413-01のレベル指定初期化）はmember loopより前にある。保存擬似Cの関数内順序は `level init → member candidate loop → 0x58AFA0`。初期化が全経路で同順実行されるかは実行到達に依存する。

## 観測B: 0x466F60内部のallocate→init→register（STATIC）

1. `0x00467130 → 0x005B6C2B`の擬似C引数は`0x1D4`であり、確保成功時 `0x00467149 → 0x00582AA0`で初期化する。`0x1D4`はこの**生成オブジェクトの確保要求バイト数候補**であって、戦闘Unitの全体サイズと同一とは断定しない。
2. `0x0046717E → 0x00582D90`へ戻る直接CALLを確認。続いて `0x0046718D → 0x00436560`、`0x004671A7 → 0x00436680`、`0x004671B3 → 0x00463280`の順が保存擬似Cに存在し、最後の呼出には`param_1 + 0x2FC`が使われる。`+0x2FC`がどの所有コンテナか、登録された候補の実identityはVERIFY。
3. 故にCALLグラフには `0x582D90 --(site 0x583546)--> 0x466F60 --(site 0x46717E)--> 0x582D90`の**2関数cycle**が実在する（STATIC）。これは実際の無限再帰を意味しない。前段の`param_5`、検索結果byte+0x75/+0x77、生成helperの引数、生成済み/再利用条件でruntimeの再入有無が変わる可能性がある。

## 補助xref（STATIC、用途未確定）

- 薄いwrapper `0x00466B00`も`0x00466B6C → 0x00582D90`へ到達。保存CALLGRAPHでは `0x0054E7B0`から`0x0054EECB → 0x00466B00`があり、同一callerの`0x0054EF3E → 0x0058B7F0`を確認。擬似C上でこれらは`0x00577260`の検索結果がNULLの場合にあるため、後段のレベル再設定可能性を検証すべき。ただし`0x54E7B0`を召喚/死亡/EXP所有者と本研究から断定せず、REA/他レーンの所有中解析を代理確定しない。

## 重複境界・再実装への影響

- 既存`B-OFFLINE-20261021-0309-01`は`0x58B7F0`のlevel/EXP閾値、`B-OFFLINE-20261021-0413-01`は`0x582D90`の`level`番兵と`0x4667B0`の指定分岐。今回の増分は**member keyの条件付き走査、flag75/77 gate、`0x582D90`/`0x466F60`のcycleと生成helperの登録順**であり、既存level発見を新規READYに再計上しない。
- アーカイブ内のB owner T011資料とB HANDOFFに`0x466F60`/`0x583546`の解析本文一致は無く、04:13報告は次回検索先としてのみ挙げている。ただし最新PCにはこの観測が先行保存されている可能性があり、**最新正本との非重複未確認**。
- 再実装で単なる逐次レベル代入だけにすると、member参照解決、子候補生成の順序、登録先コンテナ、既存値0/非0による重複生成回避、レベル・EXPの初期化タイミングが食い違う可能性がある。全てINFERRED、原作バグ認定は0。

## 旧原作Golden計画（DESIGNED / NOT RUN）

- 合法原作シナリオでmemberなし/member1件/member複数、対象存在なし/存在あり、参照解決を確認できる各組を収集。`param_5`の実caller値・flag75/77について実行時採取できない場合はUNKNOWNにし、根拠なしの状態注入をしない。
- 同じ原本EXE/DAT/SAVE/map/input/操作タイミング/seed観測可否/capture SHAの下で、画面上のUnit/member数・順序・同名重複・Level・EXP・クラス・技能・セーブ/ロード後の同一性を古/新で別々に比較する。`+0x2FC`とslot、+0x168/+0x16C/+0x170のmemory検証は許可される証拠条件が整ってから実施。
- 必須未確定: 引数復元（特に`0x466F60 → 0x582D90`の末尾フラグ）、lookup実意味、循環memberの停止規則、子の経験値共有/継承、0x00415530と0x00463280の具体的効果、RNGとowner。合成モデルに原作PASSを付けない。
- 原作Gameplay Golden PASS=0／旧新strict MATCH=0／新規B限定READY=0／E統合=0／Task DONE加算=0。

## 復旧・次回再開

- 接続不能でPC MASTER最新版/TASK QUEUE/B HANDOFFと5担当ownerの**現在状態**、既存PC側研究ファイル、先行書込競合、過去安全拒否の最新件数は未確認。旧PC最終観測checkpoint195は当時の履歴であり、このrunに最新とは主張しない。CPU/RAM負荷不明。
- 以前の26研究候補は最新分類`X14/P4/I0/D1/C4/L2/O1`の**2026-10-21 01時台履歴**。以前の12ファイルPC回収記録と、`B-OFFLINE-20261021-0200-01`のPC書込UNKNOWN、10/20旧安全拒否12件・168行不完全JSON INVALIDの記録は未変更。新規PC回収0、旧拒否payload再試行0。
- PC回復後は、最初にMASTER最新版/PROTOCOL/B HANDOFF/T011..T028 owner/復旧索引を読み、同ID・同義内容・競合・既READYの有無を確認し、このLibrary資料の独立未保存差分だけをB許可 `data/` とB HANDOFFへ取込み、再読backする。MASTER/他laneは編集しない。
- 続く静的調査は許可された証拠で `0x00467DE0`のlookup/flag定義、`0x00415530`の結果、`0x00463280`登録契約、`0x466F60`の末尾フラグ設定を限定検索する。`0x54E7B0`のEXP所有者はREA/既存担当との重複照合後だけ着手する。
- 原本EXE/ZIP/SAVEを実行・改変・無断アップロードせず、禁止済み`0x5710C0..0x571500`や過去安全拒否案件の別tool/shell/path/Remote/ZIP迂回は行わない。Ghidra/REA重処理、他owner、Git/push、Work、スケジュール変更なし。
