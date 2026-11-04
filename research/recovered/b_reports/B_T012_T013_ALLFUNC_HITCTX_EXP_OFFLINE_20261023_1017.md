# 迫真戦記 ver0.67｜新B 2026-10-23 10時台：allfunc対象ごとのhit context再初期化とEXP候補のone-shot適用範囲

- **研究ID**：`B-OFFLINE-20261023-1017-T012-T013-ALLFUNC-HITCTX-EXP-REARM-01`
- **復旧ID**：`B-RC-20261023-1017-LOCAL429-01`
- **owner**：B/T012（効果・経験値候補）・T013（対象の反復配送）。T011構造体へ参照のみ。T024/T028新規成果なし。
- **状態**：`OFFLINE-UNSYNCED / STATIC-EXE-ASM / STATIC-SQLITE / STATIC-DERIVED / SYNTHETIC / VERIFY / NOT READY`。原作Gameplay Golden PASS=0、strict MATCH=0、新規READY=0、E統合=0、DONE増加=0。
- **対象EXEの実測SHA256**：`E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。Library提供の原作 `Vahren.exe` を読み取り専用で使用し実行・改変・配布なし。
- **オフラインZIP実測SHA256**：`911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`。CRC34/34成功。
- **検索DB実測SHA256**：`0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`。SQLite `mode=ro&immutable=1`、整合性`ok`。元の検索ZIPとEXEは未変更。

## 1. 今回の進捗と新規性

前回09時台 `B-OFFLINE-20261023-0909-T012-T013-DUAL-POOL-RANGE-FANOUT-01` が `0x00547DB0` の「複数候補へ個別に `0x00550E70` を呼び、候補走査後に Unit+0x94 を一回減算」という経路を整理した。2026-10-21スナップショットの `data/T012_BATTLE_CALC.md` §34 は **候補ごとに context+0x0C=0、+0x0D=1、+0x0E=0 を書く事実**を、同§59 は **`0x00551E50`がcontext+0x0Cをone-shot flagとして検査・セットする事実**を既に保存している。これらの単体発見は再計上しない。

**今回の独立増分**は、上記二つを原作実バイトの命令順・直接CALL・Ghidra擬似Cの三者で結び、**one-shotは「技能一回」ではなく「配送候補ごとに再初期化されるhit context」単位になり得る**と確定した静的制御フローの横断関係である。さらに、同経路は context+0x0E=0 によって `0x00551E50` 内の通知callback枝を抑止するが、加算と閾値処理まで一律抑止するわけではない。

**重要な限定**：本ファイルは実際のHP変化・EXP獲得・通知成否を測定したものではない。EXPというゲーム上の正式名称と任意の技能で必ず獲得するという主張は行わない。最近のLibrary成果とのテキスト照合はしたがPC正本最新の意味重複は未確認。

## 2. 一次証拠：1候補ごとのcontext再初期化

`0x00547DB0`（allfunc側の候補vector走査）の内部で、次のネイティブ命令をEXEから直接照合した。

| VA | 機械語 / 機能 |
| --- | --- |
| `0x547F3F` | `lea eax,[ebp+0x7c]`：Unit内の共通hit contextを得る |
| `0x547F4E` | `mov word ptr [eax+0x0c],0x0100`：C=0、D=1 |
| `0x547F55` | `mov word ptr [eax+0x0d],0x0101`：D=1、E=1 |
| `0x547F5C` | `mov byte ptr [eax+0x0e],0`：E=0 |
| `0x547F60` | `E8 rel32 → 0x550E70`：候補1件に効果コアを同期呼出し |
| `0x547F65` | 個別配送を試みた後、局所成功フラグを1にする |
| `0x547F7F` | 候補loopの先頭`0x547EB4`へ戻る条件付きjump |
| `0x547F85` | 成功フラグ検査（候補なし・全件skipなら消費しない） |
| `0x547F96` | `sub [ebp+0x94],eax`：候補全件を走査した後の一回のコスト減算 |

x86がlittle-endianであるため、最終的なcontext 3 byteは `[+0x0C,+0x0D,+0x0E] = [0,1,0]`。3個の書き込みは**候補ループの中**で毎回繰り返される。候補が2件なら両者とも独立に`+0x0C=0`から効果コアへ入る。構造体アドレス自体は同じ `Unit+0x7C` の再利用であり、異なるメモリ個体を毎回確保するという意味ではない。

## 3. 一次証拠：damage virtual後のEXP候補ヘルパー、および免疫枝

`0x00550E70` 内部では：

- `0x5510E5: cmp edx,10`。等しい場合 `0x5510EA: xor edi,edi`、`0x5510EC: jmp 0x551156`。この経路は通常のtarget `vtable+0x70`（`0x551154: call edx`）をskipする。
- しかし **`0x551156`に両枝が合流**する。`0x551156`でUnit `+0x1C8`のlinked候補、`0x55115C`でlinked `+0x178`の分母候補を取り、`0x551162..0x551165`で引数・contextを準備し、`0x551167: call 0x551E50`へ到達する。
- 従って「damage virtualを呼んでいない ⇒ EXP候補ヘルパーにも入らない」と単純化するのは不正確。特別なresistance index10経路では入力第2引数 `EDI=0` でもヘルパーへのCALLは存在する。**ただしEXP実加算の有無は、次項の別gate依存であり未実測。**

`0x00551E50` の静的gateと副作用：

1. `0x551E55..0x551E6C`：Skill+`0x2A8`と特別定数の比較（sentinel一致なら早期exit）。
2. `0x551E74`：Unit+`0x1D0`が0ならexit。`0x551E81`：Unit+`0x18614`が非0ならexit。
3. `0x551E8E`：context+`0x0C`非0ならexit。通過すると**`0x551E9F`で同フラグを1にセット**。
4. `0x551EA3`：Unit+`0x1C8`のlinked候補を取得。`0x551FB2`：linked+`0x16C`に計算整数値を加算。
5. `0x551FC9`：linked+`0x170`との閾値比較。そのほかUnit+`0x8C`条件を通る場合 `0x551FD3 → 0x58A650` を呼び得る。
6. **`0x551FD8`はcontext+`0x0E`を検査し、ゼロなら`0x552012`へジャンプ**。その場合は、この関数に限り、後続の `0x571A40`、`t_levelup` に係る`0x4E13F0`、virtual `levelup` 呼出経路には進まない。`0x58A650`はこの検査より前にあるため、一律skipとは言えない。

以上により、候補Aでヘルパーが`context+C=1`を設定しても、候補Bの配送準備 `0x547F4E`で同じ場所を0へ**再初期化**する。条件を満たす複数候補に対してlinked+`0x16C`加算を複数回実行できる**静的経路**がある。一方`actor+0x94`の減算は配送全体で一回のみで、かつ`0x547F65`のsuccessフラグはHP減少やEXP発生の確認値ではない。

## 4. 再実装のための区別と未確定要因

- `AbilityCostDebited`（行動単位）・`DamageDispatchOccurred`（候補単位）・`ExpHelperEntered`（候補単位）・`ExpIncrementOccurred`（gate通過単位）・`LevelThresholdHandlerCalled`・`LevelupNotificationCalled`を別イベントにする。
- 一度の行動で複数候補へ配送されたとき、1行動1回のEXP加算と決めつけない。また、全対象にEXPが必ず加算されるとも決めつけない。
- 特別index10ではHP virtualの不実行とEXP helperのCALLを切り分ける。Skill+0x2A8がゼロで他gateが揃った場合、`0x551FA8..0x551FB2`の下限10付き加算経路も存在する。ただしそこへ実技能が到達するか、ゲーム画面上の経験値として反映するかはVERIFY。
- context+E=0は **`0x551E50`内部のlevelup通知枝**を抑制する証拠であり、ゲーム全体で通知が絶対に発生しないという根拠ではない。
- `0x550E70`後段のstatus/RNGおよび`0x551E50`の丸め・overflow・他caller・linked instance寿命は今回非網羅。実験無しでDYNAMIC/PASSとしない。

## 5. 独立検証と非重複

読み取り専用検証 `B_T012_T013_ALLFUNC_HITCTX_EXP_VERIFY_20261023_1017.py` は、入力EXEとSQLiteの厳密SHA・SQLite `integrity_check`を検査したのち、原作EXEの**27箇所**の命令byte、原作E8 rel32とDB参照の**4 CALL site**（`0x547F60→0x550E70`、`0x551167→0x551E50`、`0x551FD3→0x58A650`、`0x551FF5→0x4E13F0`）、DB内擬似C原文SHA**3関数**を照合。さらに0/1/2/3候補についてコンテキスト重複書込みの純粋な合成4ケースを検査し、PASSした。原作実機Goldenではない。

既存§34（per-target context）、§59（once-per-context EXP）、§77（index10→helper）と2026-10-23 09:09（fanout/cost）は**既存成果として継承するのみ**。今回新規計数は、それらの「同じUnit scratchの候補ごとの再arm」「cost1回対EXP加算可能性N回」「context+E=0の内部通知制限」のcrossjoin。一部の細部は既存静的断片と意味重複するため、最新版B正本を取得した後、完全重複が判明すれば本IDを`DUPLICATE/REFERENCE`へ落とし新規READYに加算しない。

## 6. Golden設計と次回再開点

同一原作EXE SHA / 同一DAT / SAVE / MAP / 入力 / RNG seed と状態で、合法な `allfunc` ミサイル技能を採り、候補vectorが0/1/2/3件の場合と、2件中1件不適格・index10/非10・Skill+0x2A8 sentinel/zero・Unit+0x1D0 null/non-null・Unit+0x18614 0/1・Unit+0x8C 0/1・+0x170境界を分ける。各候補直前/直後のcontext+C/D/E、`0x550E70`、target virtual+0x70、`0x551E50`、linked+0x16C/+0x170、MP候補+0x94、level/通知callback、HP/状態・RNG順を**tick別**に記録。受動観測だけで内部flag観測不可ならINELIGIBLEとし、Golden PASSとしない。

次のP0は `0x00550E70` の **target vtable+0x70 の実派生先**と対象HP/状態書換えの接続、`0x00547DB0` の候補vector writer・途中増減（loopでbegin/end再取得）、EXP flagが二次呼出で変更される副作用、T024のAIが選ぶ行動との合流。T028士気・敗走は今回未調査で未解明維持。禁止済 `0x5710C0..0x571500`・拒否ペイロードは再探索・再提出なし。

## 7. 保存と復旧

Desktop Commander Local Compact最初の `read_multiple_files` によるPC MASTER/Protocol/B HANDOFFの取得は `UNAVAILABLE: Error code: UNAVAILABLE; Error: McpServerError: MCP SSE probe returned 429 from openai.org` で失敗した（CONNECTION/TRANSIENT、**安全拒否ではない**）。PC最新checkpoint・Task Queue・owner・未保存ID・READYは未確認。古い10/21研究スナップショットと`2026-10-20`復旧索引のみ読取可能。正本反映は禁じ、Library B所有`/迫真戦記再開発プロジェクト/data/`への独立保存に限定。過去の`B-RC-20261023-0213-LIBRARY-OVERWRITE-CONTAINER-01`（訂正版未反映）と後続復旧記録は未解決維持、同一上書き再試行なし。

**実際の新規Library保存・読み戻し状態は同IDの復旧記録／最終報告に記す。** 実測なしでPC同期やLibrary SHA一致を主張しない。
