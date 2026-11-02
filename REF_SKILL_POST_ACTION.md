# T012/T013 — skill post-action, cooldown and linked-message boundary

State: **CURATED_STATIC (bounded native facts only)**. Original-game Golden PASS=0; strict MATCH=0; newly accepted READY=0. Neither a completed skill effect nor G4 external-result settlement is established.

## Evidence and correction lineage
- Source research ID: `B-20261013-1110-01` (B/T012 primary, T013 cross-reference; historical 2026-10-13 11:10 JST). Canonical source: [B original intake](research/intake/B/B-20261013-1110-01.md), originally [owner PR #18](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/pull/18) at pinned head `48821779f639013a4cc371ddc91e1b3064bc3647`, owner blob `38342bffb319bb339c5414ab686ff959f82d8e21`.
- Authorized-PC report `data/T012_SKILL_POST_57BE30_CONTRACT_20261013.md`, independent SHA256 `718C89E4DBDFF8BEC49D77D05176C4059C6693929E67D5243D5F8B63D745C9CB`; owner saved source and native-list path `exe/T012_SKILL_POST_57BE30_NATIVE_20261013.txt`.
- Original PE SHA256 independently read back: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`. The original `0x57BE30..0x57C173` (end-exclusive) 835-byte window SHA256 independently matched `E4F7859D1F4D7B7AA857CA8777652BF590C1295F15D2858BC04FF1C3EC19D253`. Capstone 32-bit re-decoded **224 instructions, 835/835 bytes**, with **20 direct CALL instructions** and one normal `0x57C170 ret 4`; this is not a whole-program or exception-path audit.

## Admitted native contract (not gameplay semantics)
- At `0x57BE65`, the stack-supplied Unit-like pointer is moved to EBP; `0x57BE6C` copies ECX into ESI (owner's Skill-like argument). One normal `RET 4` cleans the caller's four-byte stack argument. Input types beyond the observed loads remain VERIFY.
- At `0x57BE78/0x57BE80`, `Unit+0x1E54C` is compared and conditionally written from the `Skill+0x208` loaded at `0x57BE6E`; `0x57BE8C` stores an x87 double to `Unit+0x1E550`. Exact tick/priority gameplay meaning and signed boundary remain VERIFY.
- `Skill+0x210` has a zero gate at `0x57BEA3`; the following branch prepares `Unit+0x1E53C` and `Skill+0x214` for `0x57BEC3 call 0x4C1200`. At `0x57BECC` the cursor is compared with `Unit+0x1E540` and at `0x57BEDB` the hit path writes node `+0x28`. The owner records a separate missing-node creation path via `0x510FD0/0x436680/0x463280`; allocation/duplicate failures and internal effects are VERIFY.
- `0x57BFB8` loads a linked object at `Unit+0x1C8`; the owner identifies linked-byte gates `+0x75/+0x77` before message work. `0x57C0FC` calls `0x49EB50`, then the local body conditionally writes `Unit+0x1E4F8` and `Unit+0x1E518` (observed at `0x57C114/0x57C11A`). `0x57C120` tests `Skill+0x26C` before `0x57C131 call 0x4210A0`; neither visible message nor battle result is proven.
- Previous `B-20261011-0408-02` reaches `0x57BE30` from support-skill dispatch, while another caller sets AL=1 **after** return; do not treat this callee's EAX/AL as proof of hit, HP/MP change or target acceptance. Prior B skill-post/cooldown studies are overlaps, not new independent events.

## Search, verification and hold
- Search `kb.py addr 0x57BE30` (new named symbol), `kb.py docs 0x57BE30`, `kb.py find Skill_PostAction`, or source ID `B-20261013-1110-01`; `REF_BATTLE_AI_MORALE.md` covers related AI selection, not this post-action effect.
- Need original-game same-SAVE/seed contrast of Skill `+0x208/+0x20C/+0x210/+0x26C`, linked `+0x75/+0x77`, message present/absent, effect/MP/RNG and failure paths before any DYNAMIC/Golden/READY promotion. The local CALL list does **not** prove absence of lower-callee RNG or side effects.
