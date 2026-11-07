# 迫真戦記 ver0.67｜新B：`offset`文字列集合の重複判定と`offset_on`側のポインタキー範囲削除

- **研究ID:** `B-OFFLINE-20261022-2310-T011-T012-T013-STRINGSET-PTRMAP-01`
- **復旧ID:** `B-RC-20261022-2310-LOCAL429-01`
- **時刻:** 2026-10-22 23時台 JST
- **担当:** B T011/T012/T013（T024/T028はP0継続、今回増分なし）
- **状態:** `OFFLINE-UNSYNCED / STATIC-ASM / STATIC-DERIVED / VERIFY / NOT READY`

## 0. 証拠源・未同期／復旧状況

最初にDesktop Commander Local Compactの`read_multiple_files`でPCのMASTER、Protocol、B HANDOFFを読もうとしたが、`UNAVAILABLE: Error code: UNAVAILABLE; Error: McpServerError: MCP SSE probe returned 429 from openai.org` で失敗。接続障害であり安全拒否ではない。Remoteを使わずPC正本にも書き込んでいない。過去の安全拒否案件（例`0x5710C0..0x571500`）は再試行していない。

ChatGPT Libraryルートで実在を確認した`HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip`、`Vahren.exe`、`T011_T012_T013_T024_T028_UNSYNCED_RECOVERY_REGISTER_20261020.md`、`ANALYSIS_LANES_PROTOCOL.md`を取得。ZIP内のSnapshot MASTER/B HANDOFF/T011/T012/T024を閲覧した。ZIP CRC 34/34件PASS、SQLite `PRAGMA quick_check=ok`。読み取り専用のGhidra検索DBと原作EXEを使用し、EXEを実行・変更せず、GhidraやREAの再解析は行っていない。

| 確認対象 | SHA256（大文字） |
|---|---|
| EXE | `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` |
| 34件ZIP | `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2` |
| search.sqlite | `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF` |

保留中の未同期成果は勝手にREADYへ移さない。現行PC MASTER、B HANDOFF、最新READY・競合・予約IDの照合は**未実施**。オフライン資料内では本件の比較関数・重複消去・ポインタ値equal-rangeを詳述したB記録は検出されなかったが、最新PCでの完全非重複判定はVERIFY。

また、18時台の既存ID `B-OFFLINE-20261022-1813-T011-T012-MISSILE-VTABLE-SLOT38-01` の訂正版Library未反映問題を先行回収した。旧版との差分はMarkdown1箇所／JSON2箇所の説明修正に限る。`container_path`利用では`container_session_unavailable`が再発したが、既存の**訂正済みファイルの正規ID**を使ってB所有Libraryファイル2件を上書きし、独立読み戻しで元ファイルとSHA256一致を確認した。復旧ID `B-RC-20261022-1813-LIBRARY-OVERWRITE-CONTAINER-01` は**Library訂正版反映済み・PC正本未同期**と記録する。旧研究IDを再採番しない。

## 1. 新しいSTATIC-ASM結果：`offset`キーの比較はバイト列辞書順

前回22時台に解明した`0x00599BD0 (offset) → 0x00468440 → 0x00417250 → 0x004165B0`を、今回は**比較関数**まで掘り下げた。

- `0x0041728D/0x004172AC/0x004172E1/0x00417304/0x0041732B/0x00417353 → 0x00405370`が挿入位置を比較する。
- `0x00415A28 → 0x00405370`は既存キーと新キーを比較。`0x00405394 → 0x00402C40`は`min(長さ1, 長さ2)`バイトを比較する。
- `0x00402C68..0x00402CA3`は`movzx`でバイトを符号なしとして読み、異なる箇所の差を判定する。`0x0040539D..0x004053B0`は同一prefixの場合、長さの違いを使う。
- `0x00405370`の`+0x14`と`+0x10`の参照は、短い文字列のinline格納と長い文字列の外部バッファ参照に相当する。

したがって、この経路での比較規則は**バイト列の辞書順**。`A`と`a`は比較関数内では別キーになる。ただし、**DATトークナイザが挿入より前に大小文字を変換する可能性**は未確認であり、ゲーム上で常に大文字小文字を区別するとまでは断定しない。文字コード・文字列パーサもVERIFY。

## 2. 新しいSTATIC-ASM結果：同じキーの二重挿入はcountを増やさない

- `0x00415920`はツリーを探索し、重複候補を`0x00415A28 → 0x00405370`で比較。
- **等価キー経路:** `0x00415A2F: je 0x00415A46`でノード確保を通らず、`0x00415A4F: mov byte ptr [eax+4],0`（新規挿入フラグ0）を返す。
- **新規キー経路:** `0x004159F5 → 0x004165B0`で登録し、`0x00415A07: mov byte ptr [eax+4],1`（新規挿入フラグ1）。`0x004165F7: inc ecx`、`0x004165F8: mov [edi+8],ecx`が要素数増分。
- `0x00417250`は指定位置からの挿入を試し、条件が外れた場合`0x00417393 → 0x00415920`へ委譲する。既存キーと一致すれば再挿入しない。

この`offset`集合では、**正規化後に同じバイト列のキーは1要素として扱われる**。前回の`offset=on`単独時に`Skill+0x134`を0へ戻す処理と組み合わせると、仮にパーサが同じ`on`を2回供給しても（他キーを供給しなければ）集合は1要素なので単独`on`の消去条件に到達するという*STATIC-DERIVEDな予測*が成り立つ。原作のDATが重複トークンを本当に供給するかはVERIFY。

合成例として、キー`fire, fire`は一意数1、`FIRE, fire`は比較関数単体なら2、`a, aa`はprefix差で2、`on, on`は比較関数単体なら1→既知の単独`on`正常化条件を満たす。これは原作実行結果でない。

## 3. 新しいSTATIC-ASM結果：`offset_on`側は文字列treeではなく**別の数値tree**を消去

前回の`Skill+0x1FD != 0` → `0x00515420` の後続を調べた。

**引数と所有者:** `0x005525D2: mov ecx,[ebp+0x78]`、`0x005525D5: mov edx,[ecx+0x1D4]`、`0x005525DB: push ebp`、`0x005525DC → 0x00515420`。この呼出サイトでは`ebp`が対象オブジェクト候補であり、`edx`は参照元+`0x1D4`に保持された管理オブジェクト候補である。`0x00515438: lea edi,[edx+0x68]`により対象treeはその管理オブジェクトの`+0x68`にある（型名はVERIFY）。

**キーの出自:** `0x00515420`は呼出引数を`[esp+4]`から読んで`[arg+0x80]`のSkill候補フラグ`+0x1FD`を確認。さらに`0x00515441: lea eax,[esp+0x1C]`はスタック調整後**元の`[entry ESP+4]`（同じ引数ワード）のアドレス**を指す。`0x00515445 → 0x00579AA0`は`[eax]`を整数キーとして取り出し、`0x00579AB8: mov esi,[ecx+0x0C]`のtreeノードキーと`cmp`/`jae`で**符号なし32bit数値比較**する。つまり、今回確認した呼出サイトでは**接触物体候補の32bitポインタ値**がtreeの照合キーに渡る（実行時のポインタ同一性と全呼出元はVERIFY）。

**消去範囲:** `0x00579AA0`は2個のiteratorを返し、`0x0051545A → 0x00510850`へ渡す。`0x0051087A: cmp ecx,edx; 0x0051087C: je 0x005108EE`で同一iteratorなら反復削除なし。異なる場合`0x005108DF → 0x00510C20`でノードを順次除去する。したがって単一ノード消去とは限らず、**値が一致する範囲のtree要素を削除する経路**がある。削除対象を「攻撃ターゲット」や「HP」と断定する証拠はなく、オブジェクト関連索引の清掃として仮分類する。

ここで扱う数値treeは、`Skill+0x12C/+0x134`の`offset`文字列treeとは**別物**。`offset_on`を「offsetキー集合が非空か」という一条件に置き換えたり、数値キーを`attr`文字列と混同する実装は避ける必要がある。

## 4. 既存成果との位置づけ

22時台の `B-OFFLINE-20261022-2245-T011-T012-T013-OFFSET-ATTR-GATE-01` は`offset` writerと独立`offset_on` flag/ゲートを確認済み。今回は**文字列treeの比較規則、重複登録の有無、別treeの数値キー出自とrange erase**のみを増分とした。既存の21時台のAABB、属性除外、中順走査は再計上しない。既存B復旧IDの安全拒否記録・PC READYは変更しない。

## 5. 検証結果・未解明P0・Golden条件

- 原作ASM `E8` CALL命令・検索DB照合 **12/12 PASS**、局所opcode **28/28 PASS**、関連するGhidra擬似C **11関数確認**。SQLite quick_check **ok**。合成バイト列キーケース **6件**。これは原作ゲームのGoldenではない。
- **T011 P0:** `offset`のトークン分割・重複・大小文字正規化・Shift-JIS等の実際の文字コード・DAT定義例、Skill構造体の正式な型。
- **T012/T013 P0:** `0x00515420`で受け取ったobject引数の全経路／管理オブジェクト+`0x68`の保存・所有・消去効果、`0x004E6D10`候補treeのソートキー、最終命中→HP/状態反映・RNG順序。
- **T024/T028 P0:** 戦闘AIの最終行動と士気・敗走の未解明条件は継続。ただし今回は新規証拠を取得していない。
- **Golden:** 無改変原作 EXE・DAT・SAVE・MAP、同一入力とRNGを揃え、単独/重複`offset`キー、大文字小文字、`offset_on=on`、同時複数候補、object pointer、tree消去前後、HP・状態・RNGを個別観測。**実機PASS 0、strict MATCH 0**。

**判定:** STATIC-ASM増分あり、STATIC-DERIVED・INFERREDは要検証。**新規READY 0、Task DONE増加0、MASTER統合0、PC同期なし、NOT READY**。

## 6. 保存・readback／次回再開点

独立成果は本Markdown、証拠JSON、読取専用検査Python。Library B担当`/迫真戦記再開発プロジェクト/data/`への保存と独立読み戻しは別途実結果で報告する。ローカル`/mnt/data`への書込みとPC正本への同期を混同しない。次回は`0x00515420`の全6直接callsite（Missile4/SimpleMissile2）における渡し方と、`manager+0x68`ツリーの挿入元を調査する。安全拒否域には触れない。
