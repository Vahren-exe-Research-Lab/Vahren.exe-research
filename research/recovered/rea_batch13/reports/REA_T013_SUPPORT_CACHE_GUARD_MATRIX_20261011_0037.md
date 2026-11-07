# REA独立静的監査：support候補cacheの更新ガード行列（2026-10-11 00時台 JST）
判定: CONFIRMED-SAVED-ASSEMBLY（0x57B870関数内の制御フロー限定）。他関数によるcache無効化、実ゲームへの効果はVERIFY。
対象: ver0.67承認済みコピー、保存run `20261009T225741694Z`、T013、関数 `0x57B870`（812 byte）。本回のEXE hash再測定・新規REA/Ghidra実行なし。
source SHA（保存済み一次証拠）: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
根拠: `runs/20261009T225741694Z/57B870_procedure_assembly.json` (`ev_89e3a86b53663da35b8cadf02226f2163996275f1d24f93e37e8009fc50f048c`)。
独立照合: `57B870_procedure_pseudo_code.json` (`ev_4767a901e9f4b9ad1fc38d59a2f36a6a4a1ef4cc22287abb8e74c97f094aa2dc`)、callee (`ev_5f69dc42c9b24ee6e1c0cf83c2fb4da210af2dda6c4e48b70cbf9ef185ea6203`)。
## 分岐とローカル書込
- `0x57B87F`で`Unit+0x1E534 < unit_search_bdr`なら`0x57B88F/0x57B8D4..DB`の早期return。support builder/mergeは到達せず、この関数内でsupport vector `Unit+0x1E584/588/58C`を直接更新しない。
- 閾値到達時はtarget選択またはcached target距離再計算の後、`0x57B9F4 CMP byte [Unit+0x137],0`→`0x57BA01 JZ 0x57BA9C`。capabilityが0ならbuilderとmergeを回避し、この関数内ではsupport vectorを明示clearしない。
- capability非0・混乱判定成功では`0x57BA41 CALL 0x514F10`→`0x57BA53 CALL 0x57CFA0`→`0x57BA58 JMP 0x57BA9C`（`0x5158A0`と`0x57CFD0`は経由しない）。
- capability非0・通常側では`0x57BA62 CALL 0x514F10`→`0x57BA7E` begin/end照合。非空の場合のみ`0x57BA84 CALL 0x5158A0`の結果を`0x57BA89`でendへ書込。続いて`0x57BA97 CALL 0x57CFD0`。
- どの分岐でも`0x57BA9C`以降の距離条件ラッチ・負値statusによるHP変化・特殊action gateはsupport vector更新とは独立に後続評価される（ただしcounter未達枝はreturn済み）。
## 実装上の境界と未確定点
- `support capability=0`と`support vector length=0`を同義にしない。0は本関数におけるmergeの非実行条件であり、vector消去の証拠ではない。
- 過去フレームの候補が現実に残るか、後続evaluatorがそれを使用できるかは外部writer/consumerとlifecycle未追跡のためVERIFY。`0x5158A0/0x57CFA0/0x57CFD0`の内部副作用も未確定。
- テスト候補（DESIGNED/NOT RUN）: counter未達/到達 × `+0x137` 0/1 × vector空/非空 × confusion成否、各分岐で3 helper呼数と`+0x1E584/588/58C`前後値・可視support行動を別々にtrace。
- Wave進捗変更なし: W1 16/16、W2 10/10、W3 10/10、W4 3/12、合計39/48、今回新VERIFIED 0。旧EXE golden PASS0。ゲーム再実装率未計測。
- 本メモはREA専用領域内のみ。MASTER/A-E/T018/QUEUE/PROGRESS/原本/Git/設定/自動化を変更しない。過去拒否済みREAbatch/抽出/状態hashは反復しない。