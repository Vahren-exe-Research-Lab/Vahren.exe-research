# E/T018–T020 source-detail preservation: G2 placeholder identity false positive
Existing research ID: `E-AUDIT-20261026-1350-T018-T020-G2-PLACEHOLDER-IDENTITY-01` (not a new research ID).
Owner: **E** / T018,T020; T019 reference only. Evidence classification: **historical SYNTHETIC diagnostic and STATIC report, original runtime VERIFY**; Golden and official READY not established.

## Authorized PC source and time
- Original PC-relative: `tests/T020_CNB02_G2_PLACEHOLDER_IDENTITY_REVIEW_20261026_13H.md`; 19 lines / 3,755 bytes.
- Original report SHA256 **independently recomputed 2026-11-02 JST**: `23F1C78F6BBA3B705D695522F57771B8B252D2258F4C010818018BD6DC90FFC4`, same as existing E 193-ID index; preserved first as excerpt in E crosswalk batch02.
- Evidence original lines **3–10** identify false-positive and historical synthetic execution; lines **11–16** mark witness/owner boundaries; lines **17–19** identify acceptance and next step. VA/function/CALL/offset: **null** for this E-only gate; B/T028 native interpretation remains B-owned/read-only.
- Earlier E parent context: 2026-10-26 12:53 G2 roster reviewer (source claim), and subsequent 13:50 E placeholder overlay. `supersedes`: none; `errata`: the older reviewer could accept literal placeholder strings as valid **schema fields**, not legitimate original Unit/Troop identities.

## Distinct preserved source meaning
- The prior G2 synthetic roster reviewer checked strings, emptiness, duplicates and cross-role identity, but accepted a literal `unit_visible="unknown"` as a plausible field; an otherwise well-shaped synthetic record could return zero diagnostic issues. This is a **false acceptance in E's diagnostic model**, not an observed original-game bug.
- Owner E's 13H overlay proposed case-insensitive trim/casefold validation of **exact placeholder tokens** for the Unit, Troop and side-participant labels separately, with diagnostics `G2_UNIT_ID_PLACEHOLDER_REVIEW`, `G2_TROOP_ID_PLACEHOLDER_REVIEW`, `G2_SIDE_PARTICIPANT_PLACEHOLDER_REVIEW`. It avoids treating a legitimate-looking longer name such as `Unknown Soldier` as necessarily a placeholder.
- Owner's historical run logged **13/13** new synthetic tests and **89/89** preexisting seven-generation synthetic checks, **102/102** overall. The recorded Python source hash was `3A1B5F0A10A5F29657FB2CA93D5A4F5ECC755BAE5B35A207A1087D30B5DB92B4`. **Those script tests have not been rerun in the 2026-11-02 source-preservation run**; the script content is not published here.
- The reported overlay unconditionally returns **VERIFY_NOT_GOLDEN**, `actual_golden_pass=false`, `strict_match=false`. Placeholder token sets are E diagnostic heuristics, **not rules of the original executable**.
- The older read-only B/REA stage input summary quoted 4,190 aggregate Unit occurrences but lacked native Unit position and side membership evidence; a count of occurrences cannot prove same-time actual MAP deployment. Independently owned B static findings were referenced by the old report but **are not reattributed or republished** by E.

## Eligibility and curator-only review
- Link G2 to authenticated *same original battle* legal G0 UI/Spot and G1 immediate prebattle SAVE/input, actual runtime MAP bytes/SHA, three side identities, **ordered deployed Unit/Troop** at a usable atomic epoch. Generic labels, non-atomic structures or independent PID snapshots do not establish G2.
- Reproduce only via an authorized copy of E source and safe synthetic stand-ins. Curator may adopt **false-positive prevention rules** into an E acceptance reference after source and errata review, but must not turn them into original battle mechanics, READY or original Golden.
- Source report and current hash verified; gameplay DYNAMIC OBSERVED=0, actual Golden PASS=0, strict MATCH=0, new formal READY=0; no direct original EXE, game, SAVE, DAT, generated DB, protected region or denied source was read or changed.
- State after successful readback: `PUBLISHED_INTAKE / NOT_CURATED / VERIFY`. Next: source-targeted curator validation and independent legal same-run G0–G2 evidence; keep B owner proofs read-only.
