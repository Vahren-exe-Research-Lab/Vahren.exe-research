# 迫真戦記 新B｜T013 24B支援候補vectorの確保容量算出（保存REA限定・2026-10-20 16時台）

- **研究候補ID** `B-OFFLINE-20261020-1609-01`（正式証拠IDではない）／**復旧ID** `B-RC-OFFLINE-20261020-1609-LOCAL-SESSION-01`。
- **状態** `SAVED-REA-STATIC / SYNTHETIC-TEST / OVERLAP-VERIFY / OFFLINE-UNSYNCED / NOT READY`。新規正式B READY=0・MASTER統合=0。
- 担当 Lane B / **T013**。既存T013支援候補レコードの`SUPPORT-RECORD`系と、PC保存済みと報告の`B-20261020-1015-01`（自己参照append保護）に**関連**。意味重複は最新PC正本照合まで未確定。
- 2026-10-20 16時台のLocal最初のMASTER読み取りは `INVALID_ARGUMENT: McpServerError: Session terminated`。**CONNECTION**であり安全拒否ではない。Remote/Work未使用。最新MASTER/規約/B HANDOFF/担当正本を読めず、PC書込みなし。
- 参照クラウド: Library `/decomp_task.zip`（更新2026-10-18T17:01:26Z、今回取得したZIP SHA-256 `e1ecf0b9c9a315df3eae39bc88399b54150ed0622baee813d945d31f7d2442cb`）。保存REAの対象EXE digest `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` は**保存メタデータ値**であり、原本再ハッシュではない。
- Source: `runs/20261011T153309850Z/5155C0_procedure_{assembly,pseudo_code,callees}.json`、`runs/20261011T144115307Z/5154F0_procedure_{assembly,pseudo_code}.json`。各`checked.ok=true`。原本EXE/ZIP/SAVE実行・変更なし。今回の新規逆コンパイルなし。

## 1. 小区画A｜`0x5155C0` の共有vector容量要求（保存ASMの局所事実）

- 共有配列のbegin=`[0xAC09EC]`、end=`[0xAC09F0]`、capacity-end=`[0xAC09F4]`。`0x5155C0..0x515601`の保存ASMは(end-begin)および(capacity-end-begin)を**24バイトstride**で個数に変換。`0x2AAAAAAB`で整数除算を実現。
- `0x5155E0 CMP ECX, 0xAAAAAA9`のガードにより現在要素数が `0xAAAAAA9`（178,956,969）を超えると`0x5155ED CALL 0x5B5B6D`の異常系へ。pseudo-codeには `vector<T> too long` の引数と`does not return`注記がある。**例外形式・実際の処理継続はVERIFY**。
- `0x515609 INC ECX`で必要要素数を `size+1` とし、`0x51560C CMP ECX,EAX`の分岐により既存容量以上なら容量変更要求なし。足りない場合は `0x515612..0x515629`で `capacity + floor(capacity/2)` を候補とし、最大値に近い場合はオーバーフロー回避枝で候補0、最後に`max(candidate,size+1)` を選ぶ。
- `0x51562C CALL 0x515640`へ**算出した希望容量を渡す**。`0x515640`本体ASMは今回の保存ZIPで見つからず、**確保成功、戻り、再配置、OOM時の実作用はVERIFY**。ここで確定するのはcall前の算出分岐に限定。
- `0xAAAAAAA`（178,956,970）個を想定上限とするガードであり、現実のゲームがこの個数の候補を扱う証拠はない。最大値のfixtureは純粋な合成数値モデル。

## 2. 小区画B｜`0x5154F0` からの呼出し分離

- 配列**内部**からの追加経路では、満杯時 `0x515523 CALL 0x5155C0`、その後 `0x515528/+0x51552E`でend/beginを再取得して24B単位の旧indexを復元する。これは既存`B-20261020-1015-01`関連の事実であり**今回の新規READYとして再計上しない**。
- 配列**外部**からの追加経路でも満杯時 `0x51557A CALL 0x5155C0`、その後 `0x51557F`で更新endを再取得する。両経路が共通の容量算出処理を使用することを既存ASMで直接確認した。
- `0x5154F0`の両経路は6 DWORD（24B）をコピーする。レコード内`+0x04/+0x14`を意味フィールドとして**解釈する証拠はない**。以前の`B-OFFLINE-20261020-0908-01`・`1313-01`・`1408-01`の未確定8B問題とは混同しない。

## 3. 合成検証・実装影響・Golden条件

- 同フォルダ `test_T013_SUPPORT_VECTOR_CAPACITY_20261020.py`は保存ZIPのSHA、`0x5155C0/0x5154F0`保存REAのEXE SHAと`checked.ok`、主要ASMアンカーをread-only照合し、容量入力9条件＋上限ガード1条件の算術モデルを実行。**17/17 PASS**（静的アンカー7、合成数値10）。原作実機テストや新旧strict比較ではない。
- 再実装時、**要素数**と**確保容量**を分離する。容量拡大は共有候補配列の内部実装であって、対象選択の評価順、最終target、命中、HP/MP、士気への直接効果は未確認。互換対象がゲーム可視結果なら配列容量のバイト一致をGolden条件にしない。
- Golden案: 同一EXE/DAT/map/行動入力と記録条件で候補大量生成に伴う**ゲーム可視**動作が比較できる場合に限定。内部capacityしか観測できない場合は`INELIGIBLE`。原作Gameplay Golden PASS=0、strict MATCH=0。
- 2026-10-20 15:15クラウド復旧索引の**25件**を継承。これは新しい正式証拠に加算しない。安全拒否8件は`BLOCKED-METADATA-ONLY`のまま。

## 4. 必要な次手と保存判定

1. PCに繋がったら**最初に**現行MASTER TASK QUEUE/checkpoint/P0、規約、B HANDOFF、T011/T012/T013/T024/T028担当資料を取得。特に`B-20261020-1015-01`で既に容量増加比・上限を扱っているか意味重複を確かめる。
2. `0x515640`の効果は**既存の許可済みB資料がある場合のみ**参照し、ない場合はVERIFY。新規のREA/Ghidra逆解析、拒否済みVAへの迂回、他レーンへの書込みはしない。
3. 今回の局所増分が先行資料に無い場合のみ、B所有T013の`data/`とHANDOFFに許可された範囲で反映し、独立読み戻し・証拠ID重複検査を実施。重複なら`DUPLICATE`を記録し新規採番しない。
4. 現段階は **PC未保存／クラウド独立保全対象／OFFLINE-UNSYNCED／NOT READY**。Libraryへの保存結果と独立読み戻しは**アップロード後に別途検証**。直近PC正本checkpoint194は会話中の報告に過ぎず今回未検証、旧Library MASTER checkpoint187との差分不明。
5. P0継続: T012の`0x580280`実作用・MP fallback・攻撃結果、T013のtarget優先・consumer・cache寿命、T011クロス種継承、T024 AI状態、T028士気効果寿命。PC CPU/RAM負荷不明。既存automationの有効状態・実行時刻・頻度を変更しない。
