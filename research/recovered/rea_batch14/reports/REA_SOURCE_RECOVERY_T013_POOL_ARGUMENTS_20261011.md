# REA保存静的証拠からの部分ソース復元: T013 0x57B870
- 作成: 2026-10-11 JST。状態: **PARTIAL_SOURCE_RECOVERY**（既存VERIFIED関数の呼び出し引数分岐のみ）。Ghidra新規解析=0、旧EXE実機golden=0、今回VERIFIED増加=0。
- 対象: 迫真戦記ver0.67の承認済みコピー。過去source SHA256=`E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。今回ハッシュ再計算なし。
- 根拠run: `runs/20261009T225741694Z/`。0x57B870 Ghidra body 0x57B870..0x57BB9B（812 bytes/34 basic blocks）。
- info: `ev_c4fcdda0f9486944ccdcfe1354a6d2e37f2b68761dfd2e47b7df9a11cd367612`
- pseudo: `ev_4767a901e9f4b9ad1fc38d59a2f36a6a4a1ef4cc22287abb8e74c97f094aa2dc`
- assembly: `ev_89e3a86b53663da35b8cadf02226f2163996275f1d24f93e37e8009fc50f048c`
- callers: `ev_911883dad3560c441dc40b2e53fe8fb1e83d4b85c4cbf622e80eb7ed59e4a8c4`
- callees: `ev_5f69dc42c9b24ee6e1c0cf83c2fb4da210af2dda6c4e48b70cbf9ef185ea6203`

## 既存pseudoだけでは欠落しやすい呼び出しレジスタ
- `0x57B930`: Unit+0x1E570 の既存主targetが非0なら、選択関数`0x514D60`を呼ばず距離更新。NULLなら主target探索へ。
- `0x57B938..0x57B964`: Unit+0xC8<0のときだけ主target側の独立rand15+native変換を行い、`roll < [0x65BD64]`で分岐。
- 主探索の分岐成立 `0x57B966`: `EAX = *(Unit+0x1D4)`を指定して`0x514D60`に入る。
- 主探索の通常側 `0x57B974..0x57B983`: `EAX = *(*(Unit+0x1D4)+0x1C)`を指定して`0x514D60`に入る。
- 両側ともUnitと28-byte局所recordの引数設定を通るが、特定ABI名・実際の攻撃陣営は未確定。
- 支援能力`Unit+0x137!=0`なら別判定。混乱側成立 `0x57BA36..0x57BA41`: `EAX=Unit`, `ECX=*(*(Unit+0x1D4)+0x1C)`で`0x514F10`。後段は`0x57CFA0`。
- 支援通常側 `0x57BA5A..0x57BA62`: `EAX=Unit`, `ECX=*(Unit+0x1D4)`で`0x514F10`。必要時のみ`0x5158A0`、続いて`0x57CFD0`。
- **新しいソース復元上の要点:** primary/supportで条件分岐のpoolポインタ配置が交差する。両者を一つの「混乱時pool」引数として共通化してはならない。poolの友敵など人間向け名は保留。

## C-like部分復元（外部calleeの効果・丸めは抽象のまま）
```c
// u: Unit runtime pointer; root: *(u+0x1D4); alt: *(root+0x1C)
// native_roll_pct() is rand15(0x5B6EAB), FPU scaling,
// then 0x5D1B80 conversion; exact rounding remains VERIFY.
if (s32(u, 0x1E534) >= global_s32(0x65BCAC)) {
    native_update_search_timer(u);        // 0x57B8DC..0x57B92A, one direct rand
    if (!ptr(u, 0x1E570)) {
        bool flip_main = s32(u, 0xC8) < 0 &&
            native_roll_pct() < global_s32(0x65BD64);
        void *root = ptr(u, 0x1D4);
        primary_candidate = call_0x514D60(
            flip_main ? root : ptr(root, 0x1C), u);
    } else { update_cached_target_distance(u); }
    if (u8(u, 0x137) != 0) {
        bool flip_support = s32(u, 0xC8) < 0 &&
            native_roll_pct() < global_s32(0x65BD64); // independent draw
        void *root = ptr(u, 0x1D4);
        support_candidate = call_0x514F10(
            u, flip_support ? ptr(root, 0x1C) : root);
        if (flip_support) call_0x57CFA0(support_candidate);
        else { maybe_call_0x5158A0(u); call_0x57CFD0(support_candidate); }
    }
    post_refresh_gates(u); // native 0x57BA9C..0x57BB8F, not modeled here
} else { cached_target_distance_only_or_return(u); }
```
- このC-likeはABIと後段処理を省略した**非コンパイル・部分復元**。既存Ghidra文字列を原作Cソースと主張しない。
- 先行研究T013の「攻撃側・支援側で別乱数」に対し、今回の追加価値は**nativeレジスタで渡すroot/altの正確な交差規則**を明示したこと。
- VERIFY: `0x514D60` / `0x514F10`の候補順・除外条件、`0x5D1B80`のdefault x87変換、helperの副作用、32-bit演算wrap、ゲーム内友敵選択と実機seed。
- 次回: 保存nativeからcalleeの既存証拠を照合、使える範囲を拡張。禁止済みREA再抽出・0x5710C0..0x571500・既往拒否コマンドの迂回なし。
