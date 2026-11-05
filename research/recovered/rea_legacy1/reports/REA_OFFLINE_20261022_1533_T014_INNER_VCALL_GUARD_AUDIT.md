# 迫真戦記 ver0.67｜REA/T014 `0x543428` 間接CALLの条件・受信オブジェクトの独立検証

- **研究ID**：`REA-OFFLINE-20261022-1533-T014-INNER-VCALL-GUARD-STATIC-01`
- **日時**：2026-10-22 15時台 JST
- **状態**：`OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY`
- **owner**：REA/T014。研究PC正本・MASTER・QUEUE・PROGRESS・原本・他レーン・製品コード・Git・スケジュールは一切変更しない。

## 1. 着手時の状態・出典

`Desktop Commander Local Compact`でPC上のMASTER、規約、REA README/QUEUE/PROGRESS、および検索基盤マニフェストの先読を一括試行したが、**`INVALID_ARGUMENT: McpServerError: Session terminated`**で失敗。これは今回確認できた限り**CONNECTION**事象であり、安全拒否とは区別する。PC電源・現在のowner/lock・新Wave状態・現行V3/V4検索DB・CPU/RAMは**不明**。復旧ID `REA-RC-20261022-1533-LOCAL-SESSION-TERMINATED-01`。未保存のPC書込は発生していない。PC正本への同期は未実施。

代替として、ChatGPT Libraryルートの実在を確認した `HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip` と `Vahren(2).exe` を正規のFiles取得経路でコンテナへ複製して**read-only**検証した。ZIP CRC異常なし、内包DB SHAと同梱BUILD_MANIFEST一致、SQLite `integrity_check=ok`。

| 現物 | SHA256 |
|---|---|
| 原作PE32 EXE | `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` |
| オフラインZIP | `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2` |
| ZIP内検索SQLite | `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF` |
| 14:33先行REA JSON（参照・非再計上） | `19A21025B2BBDB24E0AA800D9EF32B8E022395C21E089B27B47F927F5419AF90` |

旧スナップショットの `PROGRESS.md` は2026-10-09最終照合の初期キュー **15/16** を記載する。直近チャットのWave1〜5 **64/64 VERIFIED**は過去報告値であり、両数値を同じ分母として足したり、旧ZIPから現行進捗を証明したりしない。REA正本 `RUN_RESULT`の今回は現物再確認不可。Ghidra旧DBの擬似Cは正式REA五種証拠に自動昇格しない。

重複回避：先行 `REA-OFFLINE-20261022-1433-T014-UPSTREAM-CATCH-VCALL-STATIC-01` は `0x43400E → FadeOutSheet vtable+0x18 → 0x543AE0` を**条件付き**で特定済み。E/T020 `E-OFFLINE-20261022-1453-T020-FADE-VTABLE-PROVENANCE-01` は戦闘経路／読込エラー経路の同一vtableを既に横断検証済み。**今回の増分は、その一段内側 `0x543428` に関する「別オブジェクト・別vptr・事前読込ガード」の独立した実命令検証**であり、先行知見を新規発見に再計上しない。

## 2. 新たな静的結果：`0x543428` は FadeOutSheet のvtableではない

原作PEの `.text` 実バイト、`objdump -M intel`逆アセンブリ、旧SQLiteの `function 0x5433D0` / `callers` / `callees` / `related --depth 2` / 間接CALL索引を照合した。

```asm
0x5433D5  mov esi, ecx           ; Fade系オブジェクト
0x5433F3  mov esi, [esi+0x04]    ; constructorが保存した context
0x5433F6  mov ebx, [esi+0x20]    ; context+0x20 をここでスナップショット
          ...                    ; 0x416E80/0x416B90などの下位CALL
0x54341C  test ebx, ebx
0x54341E  jne  0x54342A          ; 非ゼロなら間接CALLをスキップ
0x543420  mov ecx, [esi+0x10]    ; context+0x10 の二次オブジェクト
0x543423  mov edx, [ecx]         ; 二次オブジェクトのvptr
0x543425  mov eax, [edx+0x1C]   ; 二次vtable +0x1C
0x543428  call eax
0x543430  ret 4
```

**確定する局所条件**：`context = *(Fade+0x04)`、`guard_snapshot = *(context+0x20)`。これが0の場合だけ、`secondary = *(context+0x10)`を`ECX=this`として、**`*( *(secondary) + 0x1C )`**の間接CALLを実施する。直接スタックへ追加引数はPUSHしない。`0x5433D0`自身は`RET 4`で終了する。**二次オブジェクトのクラス、実vptr、スロットの関数VAはまだ未確定**。先行で判明した `FadeOutSheet vtable=0x6388D4` の `+0x18=0x543AE0` を `0x543428`の呼出先として転用してはいけない。

Ghidra疑似Cでも `if (*(context+0x20)==0) (**(code **)(**(int **)(context+0x10)+0x1c))()` に相当するパターンが存在する。しかし**条件は `0x5433F6` 時点のEBXスナップショット**で判定している。途中の `0x416E80` / `0x416B90` 呼出による状態変化は未追跡であり、「CALL瞬間の最新context+0x20を読み直す」とは言えない。

## 3. 文脈と順序の追加照合

- `0x433FE9`で親 `0x433E80` の `param1+0x04` を読み、`0x433FEC`でコンストラクタ `0x543A30` にPUSHする。`0x543A63`がこれを **Fade+0x04** に格納する。従って上位catchからこの特定の呼出路へ入る条件では、今回のcontext経路が繋がる。
- 同じ親 `0x433E80` の入口にも `0x433EB3` / `0x433EB6` で `param1+0x04 → context+0x20`を取得し、`0x433EC0`で非ゼロなら終端`0x4341CD`へ分岐するガードがある。ただし入口から後続CALLまでに値が維持される動的証明はない。
- `0x543AE0`は`0x543AE9`でまず`0x5433D0`を呼び、その**後**`0x543AEE`からFade+0x30へ入力値を設定し、下限10へ補正する。一方 `0x543440`は0を渡して同じ`0x5433D0`を呼び、さらに`context+0x1EF150`へ1を書き込む。**`0x5433D0`は専用の一回限りのcatch関数ではない。**
- `0x5433D0` は4つの直接CALL (`0x4C2240`, `0x4C3D30`, `0x416E80`, `0x416B90`) と、文字列リテラル `sheet` (VA `0x62A34C`) を持つ。`0x416B90`の目的を原作実行なしに「表示更新確定」などと断定しない。

**追加の条件付き注意**：上位catchでは `0x433FE2/0x433FE4` が確保ポインタ0を `0x434001`の `xor ecx,ecx`へ進め、直後 `0x434007` が `[ecx]` を参照する。**確保関数がNULLを返して実際に分岐する場合**のNULL逆参照候補だが、下位アロケータが例外を投げるか等を調べていないため、実機到達可能なクラッシュ／確定バグとは扱わない。

## 4. 独立検証の範囲・正式カウント

標準Pythonの検証器 `verify_rea_t014_inner_vcall_20261022.py` はEXEの実PE section/RVAをパースし、byte/opcode指定**33/33 PASS**、相対E8ターゲットおよび旧SQLite直接CALL参照**7/7 PASS**、旧SQLite登録関数の疑似C本文ハッシュ**6/6 PASS**、SQLite間接CALL登録 `0x543428` **1/1 PASS**、`sheet`文字列照合PASS、旧仮想表 `0x6388EC→0x543AE0` の実32bit値一致を確認した。2値以上の「guard=0/非0」合成fixtureは設計確認であり、ゲームGoldenではない。

| 管理指標 | 今回 |
|---|---|
| PC正本オンライン・新DB・active.lock | **不明（Local接続障害）** |
| 新規正式REA五種一式 `info/pseudo/assembly/callers/callees` | **0**。旧GhidraとEXEを横断してカテゴリに相当する資料は得たが、正式RUN証拠に未昇格 |
| 新規REA VERIFIED | **0** |
| 正式TODO / VERIFY / BLOCKED差分 | **0 / 0 / 0** （未同期のVERIFY事項は本報告に独立記載） |
| 原作ゲーム Golden PASS / strict MATCH | **0 / 0** （実機未計測） |
| 新規Ghidra・REA実行 | **0 / 0** |
| CPU/RAM | **研究PC不通で不明** |
| 検証器単独時間 | 約**1.2秒**（実測値はJSONに記録） |
| 調査全体所要時間 | **未計測** |
| 新たな安全拒否 | **0** |

旧REA `info` は旧DBの関数名・99バイト範囲、`pseudo` は旧DB本文、`assembly` は原作PEの現物、`callers` は `0x543AE0@0x543AE9` と `0x543440@0x543445`、`callees` は4直接・1間接でそれぞれ根拠はあるが、**REA正式証拠5ファイルの取得・読み戻しを証明するものではない**。以前の64件や初期15件を重複計上しない。

## 5. 次に調べる地点／同期条件

**最優先P0**：`0x543428` の `context+0x10` が指す二次オブジェクトの生成・代入箇所を許可済み検索DBと原作静的証拠から限定し、vptr値と`+0x1C`実装候補を**対象コンストラクタ経路ごと**に検証する。今の段階でターゲットVAを捏造しない。副作用が「画面を描く」ことや、エラーが確実に捕捉されることもGolden未実測のためVERIFY。

別の優先VERIFYは `0x45F72C`近傍のヒープ所有権受渡しと `0x4D0D8A`の上位例外伝播（既報の未解決地点）。E/T020のFade出典判別を上書きせず、必要なら新しいREA独立証拠の所在だけ伝達する。

PC復帰時は最新MASTER→規約→REA README/QUEUE/PROGRESS/RUN・evidence→owner/lock→現行V3/V4 SHA・競合→本ID重複照合の順で**read-only**確認し、REA所有領域だけ最小差分を一度同期する。PC保存・最新DB適合・正式Verified・他レーンREADYを偽装しない。安全拒否済みVA `0x5710C0..0x571500`／Wave6／エクスポートへの迂回再試行は実施していない。
