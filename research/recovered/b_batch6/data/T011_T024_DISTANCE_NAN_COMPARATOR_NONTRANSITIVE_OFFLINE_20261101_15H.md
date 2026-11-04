# 迫真戦記 ver0.67｜新B T011/T024：距離比較のNaNと順序契約（2026-11-01 15H JST）

研究ID：`B-OFFLINE-20261101-15H-T011-T024-NAN-COMPARATOR-TRANSITIVITY-01`。owner B／担当T011・T024。T013の最終対象選択との接続は **VERIFYのみ**。`OFFLINE-UNSYNCED / PRIOR_CAPTURED_STATIC / INFERRED / SYNTHETIC_ONLY / VERIFY / NOT READY`。DYNAMIC=0、原作実機Golden PASS=0、strict MATCH=0、新規正式READY=0。

## 1. 証拠源と未同期回収の優先照合

最初に許可済みDesktop Commander Local Compactの `read_multiple_files` でPCの `MASTER_LEDGER.md`、`evidence/ANALYSIS_LANES_PROTOCOL.md`、`evidence/LANE_B_HANDOFF.md`、`knowledge/{README.md,SYNC_STATUS.md}`、旧Ghidra検索基盤 `README.md`／`BUILD_MANIFEST.json` を読み取ろうとした。しかし `INVALID_ARGUMENT: Error code: INVALID_ARGUMENT; Error: McpServerError: Session terminated`。これは**PC接続障害であって安全拒否ではない**。03HのPC保存失敗・最新MASTER・PC側READY/既存ID・未保存索引の実体確認は未了。05〜14H成果のPC統合は未確認である。

代替として、以前に本会話のChatGPT作業環境へ保存された13H/14Hの証拠JSONと10H/13H/14Hの日本語研究報告を読取専用で照合した。本実行で実際の原作EXE・Ghidra擬似C ZIP・古い `search.sqlite` は**新たに取得・ハッシュ検証していない**。元EXE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` は先行の原本検証記録からの引継ぎ値である。ChatGPT Libraryの `HAKUSHIN_B_LANE_SAFE_RECOVERY_20261029_V3.zip` は一時作業環境にmaterializeし、136件全件のZIP CRCが正常であることを確認したが、このZIPには今回の原作EXE/全擬似Cが含まれないため原作確認の代用にしていない。

旧保存証拠から今回再読取した SHA256：

- `data/B_OFFLINE_20261101_13H_DISTANCE_SORT_EVIDENCE.json`：`1C2030F7A1D8EB12A5E97F51509C70FA1BA25ADD600C271A5DA23516939A0205`
- `data/B_OFFLINE_20261101_14H_DISTANCE_BOUNDARY_EVIDENCE.json`：`9941DE16CB1EB58D894EDCDCA4846E058976EE4093C6D4C2A604512124EBB392`
- 先行取得擬似C相対パス `headless_analysis/full_pseudoc_20261020/HAKUSHIN067_FULL_PSEUDOC.zip!/functions/0052/00526030.c` SHA256 `7FEE7676046DFF1E081ED82702FBB17AEEEA2CCA92CCE64E1BB57B2F0D5745CF`、`functions/0052/0052AD00.c` SHA256 `F733FD10A1DB29D30C54096EC23DFC45152BBF06805554C099F755A467ED80C8`。**擬似C実体・ソース行の15H再取得なし**。

非公開GitHub `ButaMonky/Hakushin067-Research-Knowledge` `develop` を読取専用で照合：`GHIDRA_V9_B_REVIEW_TOP150.tsv` blob `270f60f0...`、`GHIDRA_V9_COVERAGE_REPORT.md` blob `786f7fc5...`、`KNOWLEDGE_CURATION_PROTOCOL.md` blob `4d6da0d1...`、`symbols.tsv` blob `3fcf2d43...`、`structs.tsv` blob `d79f03b1...`、`REF_BATTLE_AI_MORALE.md` blob `83fb9b91...`。パスはKBリポジトリの**ルート直下**。辞書・横断索引にこの順序契約の正式解決があったとは認めず、最新PC研究IDとの完全な非重複はVERIFY。V9順位は元挙動の証明ではない。

05〜14Hのコンテナ内既存readback台帳10個に登録されている**40個の既存成果ファイル**について、実ファイルを再読取してSHA-256が**40/40一致**した。これは**ChatGPT作業環境のローカル読み戻し**であり、PCへの同期成功を意味しない。04Hの未同期成果と03H保存失敗の回収は別件のまま。SAFE134件の今回再検査は行わず、既存安全HOLD21件を変更していない。

## 2. 旧Native証拠の限定再検査（STATICは先行取得）

13Hの保存済機械語記録で、`0x526030` 内部の `0x52608E: imul eax,eax`、`0x526091: imul ecx,ecx`、`0x526094: add eax,ecx`、`0x526117: fcomp qword [esp+0x10]`、`0x52611D: test ah,0x41`、`0x526120: jnz`、`0x526122: mov eax,1`、`0x526134: xor eax,eax` をバイト文字列で再照合。先行E8記録では `0x52609E -> 0x5E3B70`、`0x526112 -> 0x5E3B70`（平方根処理）、`0x52AD35 -> 0x526030`（比較）が存在する。マージ側の `0x52AD3A: test al,al`／`0x52AD3C: je` も再照合した。今回、新しいEXEバイトを読んだわけではない。

先行14Hのx87状態語モデルでは、通常の条件で `AH` は `greater:0x00`、`less:0x01`、`equal:0x40`、`unordered:0x45`。`test ah,0x41` 後に `jnz` で失敗側へ行くため、**比較の該当オペランドがordered greaterのときだけAL=1**、同距離やunorderedではAL=0、という局所ABIが得られる。ただし比較2オペランドの実Unitへの割当順序や制御語は15Hに原作実体で再検証していない。

## 3. 15H追加の独立検査：NaNによる「同値関係」の推移律破綻

14Hの32bit平方和例 `(dx,dy)=(46341,0)` は理想値 `2147488281` だが、x86符号付き32bitでは **`-2147479015`** になる。これは先行14Hの結果を新しい成果とは数えない。**条件付き推論**：その負値が負数平方根経路を通り、x87例外がマスクされて最終距離がNaNとなる場合、`fcomp` はunorderedを返し、`test ah,0x41` により比較結果AL=0になる。

15Hはこの2つの先行事実を結合して、**比較器のstrict weak ordering前提**を新しくテストした。抽象距離 `a=1`, `b=NaN`, `c=2` の場合：

| 比較 | `0x526030`相当のx87モデル結果 |
|---|---|
| a vs b / b vs a | 両方0（双方unordered） |
| b vs c / c vs b | 両方0（双方unordered） |
| a vs c / c vs a | 一方0、他方1（有限数は順序あり） |

比較器が両方向とも0を返した組を「同値」と扱うと、`a~b` と `b~c` は真なのに `a~c` は偽になる。**同値の推移律が破れ、順序付けの前提が成立しない**。先行13Hで `0x529DC0` が26個の一時リストと `0x52AD00` のマージを用いることは分かっているため、**NaNに到達する特殊値を含めてC++等の標準的な厳密弱順序比較器として無条件に再実装するのは危険**、という新しい設計上の警告になる。

これは**合成モデルでの反例**であって、原作のゲームプレイでNaNが実際に生成・到達すること、マージ順序が実害を生むこと、CPUが例外停止しないこと、ソートが不安定であることを示してはいない。有限正常値の比較器自体に非推移性があるという主張でもない。

## 4. 重複防止・検証・次回再開

先行研究ID：13H `B-OFFLINE-20261101-13H-T011-T024-DISTANCE-SORT-MODE-GATE-01`（距離ソートと元ASM）、14H `B-OFFLINE-20261101-14H-T011-T024-DISTANCE-COMPARE-BOUNDARY-01`（32bit overflow、x87分岐、2フィルタ）。**15Hの新規差分は「NaNを含む比較器の同値関係が非推移的になる合成反例」と、それを回帰条件にする設計注意**のみ。構造の再発見、原作実機PASS、新規READYとして二重計上しない。

検査スクリプト：`data/B_20261101_15H_NAN_COMPARATOR_ORDER_READONLY_VERIFY.py`。13H/14Hの証拠JSONから機械語10サイト、直接CALL3件、SHA2件、x87比較4ケース、NaN反例、過去10台帳40件を**合計72チェックPASS**として記録した。成果JSON：`data/B_OFFLINE_20261101_15H_NAN_COMPARATOR_ORDER_EVIDENCE.json`。スクリプトは入力読取専用、出力は標準出力のみ。原作EXE・ZIP・DB・Git・MASTER・他レーンは変更していない。作業環境に独立レポートとB HANDOFF差分を新規保存する。

**KB_CANDIDATE（正式登録禁止）**：owner B／T011,T024、15H研究ID、親13H・14H、VA `0x526030`、`0x529DC0`、`0x52AD00`、E8 site `0x52AD35 -> 0x526030`、`0x52609E/0x526112 -> 0x5E3B70`、ASM `0x52608E/91/94/117/11D/120/122/134`、擬似Cパス・SHA上記、STATIC=先行バイトのみ、INFERRED=NaN/ordering条件付きリスク、VERIFY=負平方根からNaNへの実経路・x87制御語・比較対象割当・実ゲーム到達性・原作ソート順、DYNAMIC=0、Golden0、READY0。

**Golden必要条件**：認可された原作ver0.67の同一EXE/DAT/MAP/SAVE/入力と一致するUnit座標/グループ/モード・tick/RNG、該当32bit平方和とx87ステータス、`0x526030` の返値と `0x52AD00` のノード順、実行停止/例外の有無を同一runで記録し、再実装と照合すること。許可されない原本実行はしない。境界値の実ゲーム到達性を証明できなければ例外系はVERIFY継続。

**再開位置**：PC復旧時はまずMASTER→PROTOCOL→B HANDOFF→復旧索引・03H実ファイル→安全拒否/HOLD/READY・04～15H ID/所有/競合を再照合し、B所有資料に一度だけ取り込んでreadback。PCオフライン時は安全拒否範囲を避け、`0x52AD00` の同値時マージ全手順（必要な原作証拠が得られた場合のみ）と `0x529691/0x529851` の2基準座標を追跡。未解明P0はT011召喚/EXP、T012ダメージ・回復・状態、T013最終対象選択、T024戦闘AI、T028士気・敗走。既存安全拒否例 `0x5710C0..0x571500`、拒否済み `0x5769B0` XREF操作は別手段で迂回しない。
