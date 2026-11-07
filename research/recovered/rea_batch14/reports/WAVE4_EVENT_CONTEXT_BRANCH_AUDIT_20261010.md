# Wave4 独立監査：event参照フラグの評価順序（2026-10-10）
対象: ver0.67 承認済みコピーの保存済みGhidra証拠だけ。新規逆コンパイル0件、旧EXE実機観測0件。
関数: `0x4321B0` / T006・T014。run=`20261009T225741694Z`、保存source SHA=`E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`（今回の再計算は未実施）。
一次証拠: pseudo=`ev_6443778f30890c0e5cb33fc7bbabf54b8cd665a1424f7b354c6bd439dbac2051`、assembly=`ev_56f9a3557ec9eaa37a3dae138562b66cdde8d20a39e915d61d3e8c37709157db`。info/callers/calleesは同runのRUN_RESULT参照。

## CALL/分岐をassemblyとpseudoで独立照合
- `0x4328E7: CALL 0x40B200` はmain初期化側の結果を `+0x1EED40`へ格納（`0x4328F4`）、`+0x1EED41/+0x1EED42`へコピー（`0x432913/0x43291F`）。下記二つの判定callと同じ値の再利用ではない。
- NULL既定参照補完（`+0x1EED4C/+0x1EED50`）の後に `0x4329E1`で `+0x1EED54/55`を0に初期化する。
- 第1補完済み参照先の `+0x1D != 0` なら `0x432A98`の分岐から `+0x1EED54=1`へ進み、後続二つの `0x40B200` callは経由しない。
- 第1参照の `+0x1D == 0` なら `0x432AA6: CALL 0x40B200`。戻りAL非0は `+0x1EED54=1`、第二判定へは進まない。
- 上記が偽のとき、第2補完済み参照の `+0x1D != 0` は `+0x1EED55=1`。0なら `0x432AC0: CALL 0x40B200` を呼び、AL非0で同じflag55=1、AL=0なら両flag0のまま。
- 従ってフラグ `(+0x1EED54,+0x1EED55)` の到達状態は (1,0)/(0,1)/(0,0) に限られる。保存済み疑似コードと命令順は整合する。
- 終了前に `0x432B49` が `+0x1EEC4D=1` を設定し、`0x432B6F`でevent lookup、その後scene用オブジェクト生成分岐へ進む。実画面効果・後続でのflag復元はこの1関数だけではVERIFY。

## 再実装向け未確定と安全境界
3つの `0x40B200` callsiteは異なるECX/EDI呼出文脈を持ち、同じbooleanを一括キャッシュして置換しない。calleeの正確な意味と副作用・nested event復元は未確定。
テスト案: 第1参照(+0x1D, helper判定)と第2参照(+0x1D, helper判定)を別入力にし、flag54/55、参照+0x1EED44/48、callsite実行有無、event順序を採取。DESIGNED/NOT RUN。原作golden PASS0。
Wave1=16/16、Wave2=10/10、Wave3=10/10、Wave4=3/12、計39/48、今回新規VERIFIED=0。未着手8/VERIFY1、P0 20/21・P1 19/27、MASTER checkpoint67 DONE9/34。
SAFETY: 新規REA batch拒否を再試行せず、拒否済み抽出・0x5710C0..0x571500へアクセスしない。QUEUE/PROGRESSのEPERM不整合を強制更新しない。原本、他レーン、MASTER、T018、Git、MCP設定、自動化設定は変更しない。
