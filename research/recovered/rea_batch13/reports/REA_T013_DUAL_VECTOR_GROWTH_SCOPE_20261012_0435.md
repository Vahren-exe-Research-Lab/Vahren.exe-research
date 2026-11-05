# REA T013 — 24B候補vector二系統の成長規則を分離（2026-10-12 04:35 JST）
- 状態: SAVED STATIC CROSS-CHECK。今回は新規Ghidra取得0、VERIFIED増加0、旧EXE実機NOT RUN。対象承認済コピーSHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（Get-FileHash一致）。
- 参照: MASTER checkpoint83（DONE9/34）、ANALYSIS_LANES_PROTOCOL、REA README/QUEUE/PROGRESS、runs/20261011T144115307Z・20261011T153309850Z・20261009T225741694Z、最新sync 20261011T153958076Z、既存T013監査メモ。
## 独立した二系統（同一の24byte要素幅 ≠ 同一vector instance）
1. `0x5154F0` は共有作業用vectorの global `0xAC09EC` (begin), `0xAC09F0` (end), `0xAC09F4` (capacity) を参照し、容量満杯時に `0x5155C0` を呼ぶ（0x5154F0 assembly 0x5154F0..0x515523）。`0x5155C0` の疑似コードは同global vectorの `new_capacity=max(old_capacity+floor(old_capacity/2), size+1)` を示す（巨大数ガード別途）。この **約1.5倍成長規則は現時点ではglobal scratchに限定**。
2. `0x57B870` の通常support側は、Unit `+0x1E584` を別のvector先頭アドレスとして `0x57CFD0` へ引渡す（0x57BA72..0x57BA97）。Unit-localのbegin/end/capacity（+1E584/+1E588/+1E58C）と、global 0xAC09EC/F0/F4を混同しない。
3. `0x57CFD0` のGhidra calleeは `0x515750,0x515790,0x5159B0,0x54B460,0x57D180` などで、`0x5155C0` は含まれない。容量不足枝では `0x515750`→`0x515790` と進むが、子関数の意味・Unit-local vectorの成長係数はWave6まで**VERIFY**。Ghidra pseudoに見える呼出引数はABI誤推定が既知なのでそのまま採用しない。
4. `0x5155C0` のsaved callersは `0x5154F0` の1関数、`0x57CFD0` のsaved callees一覧は7件。これはGhidraが解決した静的呼出関係の範囲内の観測であり、関数ポインタ等まで完全網羅とみなさない。
## 一次証拠ID
- `0x5154F0` assembly `ev_6a53e867e218f8905561e0687a0340e1dafe224e61cc7d465b0047e7b21c3d64` / callers `ev_8ce283bf9f936114ed4749b1907814810be35fb077af15de779d65256288d320`。
- `0x5155C0` pseudo `ev_e0069ba6edcf643c2dc695615ff75d8db9c7f580aa072947eefff66fe9bddd00` / callers `ev_8ce57a11472ca4f7210743bb6347db6942fe6f05f256522503722b53d44ff2ce`。
- `0x57B870` assembly `ev_89e3a86b53663da35b8cadf02226f2163996275f1d24f93e37e8009fc50f048c`。
- `0x57CFD0` pseudo `ev_fa33cc83cda4f064bed5262e5fa063359e2fbb86a07b22329757999821da3725` / callees `ev_2dc9297fab51c57cfc686ea99152528224402c6e4b39256935a1d5594e621958`。
## 再実装への影響・再開位置
- T013: global候補生成とUnit-local支援cacheの容量成長を別々に実装・試験する。Unit-localへ「1.5倍規則」を証拠なしに転用しない。Wave6で `0x515750/0x515790/0x5159B0/0x57D180` の入口・5種証拠/ABIを検証する。
- Wave1〜5は64/64 VERIFIED（Wave5 16/16、P0 29/29・P1 35/35）。Wave6候補16件は未正式登録・0/16（P0 5/P1 11、未着手16/関数VERIFY0）。golden PASS0、ゲーム再実装率は測定していない。
- 最新syncのQUEUE更新は `STALE_RENAME_DENIED`、PROGRESSは `SKIPPED_QUEUE_STALE`。既往EPERM操作の反復・迂回をせず新規REA起動0、Wave6正式登録0。原本/A〜E/MASTER/T018/Git/MCP/automationは無変更。
- 事前Local preflight: CPU3%、空きRAM16.24GB、Java/Ghidraなし、active.lockなし。今回は軽量保存済み証拠比較のみ。解析実行0秒、読取/照合時間は未計測。