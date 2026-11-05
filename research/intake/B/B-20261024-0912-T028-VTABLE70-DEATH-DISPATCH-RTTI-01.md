# B-20261024-0912-T028-VTABLE70-DEATH-DISPATCH-RTTI-01 — B owner historical source intake (verified provenance)

- research_id: `B-20261024-0912-T028-VTABLE70-DEATH-DISPATCH-RTTI-01`
- owner: B; tasks: T028,T012,T011; source_observed_at: 2026-10-24 09:12 JST
- source_relative_path: `data/T028_VTABLE70_FOURCLASS_DEATH_DISPATCH_RTTI_NATIVE_20261024_0912.md`
- source_sha256_verified_readonly_2026-11-02: `DEE9D0671B79F2F37EBD6B8A8E4243722B1DE941D1FB6B3B78E0DABE9F1FCA5A`; source_bytes: 5329
- original_PE_SHA256_verified_readonly_2026-11-02: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (authorized research copy; not executed)
- evidence_kind: STATIC_PRIOR,INFERRED,VERIFY; original_game_Golden_PASS: 0; strict_MATCH: 0; original_dynamic_observed_new: 0
- owner_ready_scope: historical owner NOT READY; newly promoted READY=0; intake_status: PUBLISHED_INTAKE only after GitHub readback; new formal CURATED in this run: 0
- VA/CALL sample (role scoped by owner source, not auto ABI): 0x63A4BC;0x63A9E4;0x63A85C;0x63A8E4;0x544790;0x578370;0x55ABA0;0x55B060;0x55ABBF;0x55B07D
- offsets (untyped until validated): vtable+0x70;Unit+0x90;Unit+0x1867C;COL+0x0C
- prior_ids/errata: B-20261013-1905-01
- develop curation relationship: NO_EXACT_ID_IN_REVIEWED_DEVELOP_REFS

## Owner research evidence (sanitized source-derived summary)
Source-original PE RTTI maps SimpleUnit table 0x63A4BC to slot+0x70=0x544790; Unit table 0x63A9E4 to 0x578370; StaticUnit 0x63A85C to 0x55ABA0; SimpleStaticUnit 0x63A8E4 to 0x55B060. Bounded native StaticUnit and SimpleStaticUnit paths gate on +0x1867C and subtract damage at +0x90 before HP threshold branches. A direct-CALL search returning none cannot disprove indirect virtual dispatch. The source report [TABLE ...], [NATIVE ...], [RDATA SHA] gives PE pointer and RTTI evidence.

## Correction and supersession boundary
ERRATUM: historical B-20261013-1905-01 mislabeled vtable 0x63A9E4 as SimpleUnit; RTTI identifies it as Unit. SimpleUnit is 0x63A4BC. Preserve vtable raw entries; correct type labels only.

## VERIFY / safety / next
- Limitations: Actual runtime vptr, virtual dispatch reachability, death effects, HP/UI/RNG and postbattle world-state/EXP commit have no legal original-game Golden. Do not elevate RTTI class label to validated game event.
- Next legal verification: Curator verify original PE table/RTTI and register erratum against HP-lifebar report; independently establish indirect virtual callers and battle-exit consequences.
- Original owner report sections and original PE windows are the evidence source. This summary does **not** independently redecompile or establish full C++ types, native ABI, game behavior or a safe G4 battle-result commit contract.
- No raw EXE/DAT/SAVE/ZIP, user identity/absolute host path, credentials, denied source body, or experimental game execution included. Blocked operations remain blocked; no other owner, shared REF, dictionary, MASTER or develop changes were authorized.


## 2026-11-05 正本REFの後日実機報告への限定cross-reference（既存ID・非昇格）

Bの本研究（出典 `data/T028_VTABLE70_FOURCLASS_DEATH_DISPATCH_RTTI_NATIVE_20261024_0912.md`、歴史的source SHA-256 `DEE9D0671B79F2F37EBD6B8A8E4243722B1DE941D1FB6B3B78E0DABE9F1FCA5A`）は、**各クラスのvtable+0x70の静的RTTI対応**と、StaticUnit系の条件付き+0x1867C検査までの旧証拠。ここに後日の別担当の観測を取り込んで元B研究が実機検証済みになったと扱わない。

2026-11-05の現行`develop`固定コミット `035719dbad0330f6993bbec3a653202dba114679` の[REF_UNIT_EXP_SUMMON.md §12](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/blob/035719dbad0330f6993bbec3a653202dba114679/REF_UNIT_EXP_SUMMON.md#L175-L182)（Git blob `e2897d379a8236fa442b9f602a64e0d100ea5b64`）には、別担当Claude PEER_SCRIPT01の**限定的ACTUAL報告**として「攻撃が敵を倒した最初のヒットでは、`0x551167 -> 0x551E50` の呼出時点で被攻撃側の `+0x1867C` が立っていた」「その前にvictimのvtable+0x70経由処理が走る」とある。これは特定の実験とそのフック観測に限る。報告のテスト個体・戦闘条件を、全Unit派生型・すべての死因・死亡後処理・戦後EXPの一般契約に拡張しない。

**結合してはならない境界:** 本B研究が静的に対応づけた4 vtableエントリの**それぞれ**が実機で到達したこと、どの実体型が試験で使われたか、+0x1867Cを誰がいつ書くか、HP/UI/士気/RNG・消滅・戦闘終了・G4外部結果適用の完全性は、この2資料だけでは未証明。古い`B-20261013-1905-01`の**vtable+0x4**（ライフバー・タイマー）と、本件**vtable+0x70**（死亡関連）は別スロットであり混同しない。元source SHAの2026-11-02実測は歴史的レシートで、今回の研究PC再測定・原本ASM再decode・原作Goldenには当たらない。

**状態:** 既存B研究IDへの後日出典cross-referenceのみ、`DUPLICATE_LINKED / STATIC_PRIOR + LIMITED_EXTERNAL_ACTUAL_REPORT / VERIFY`。新規研究ID 0、追加PUBLISHED_INTAKE 0、追加CURATED 0、新READY 0、原作Golden PASS 0、strict MATCH 0。次の独立検証は、担当の権限内で原本RTTI/vtableの同一PE SHAと、後日実験で実際に遭遇したruntime vptr・死亡callerの照合。保護・安全拒否対象や禁止済み索引/入口作成は再試行しない。
