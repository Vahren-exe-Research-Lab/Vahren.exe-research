# REA/T015 | 2026-11-01 01H–02H — Vorbis residue type2 input gate / two divisor provenance

**Stage:** PRIVATE owner intake only / source PC SHA readback / original x86 STATIC and conditional INFERRED / VERIFY / NOT READY. This is a **recovery of three older research IDs**, not three newly verified functions.
**Original PE SHA256:** `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`.
**V9 SQLite SHA256:** `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`. These baseline full SHA checks were repeated in the separate 23H static audit; older 01H/02H original owner reports have independent bounded original-x86 byte checks.

## 01H — parser accepts residue type2 and rejects selector >=3

**ID** `REA-LOCAL-20261101-01H-P0-VORBIS-RESIDUE-TYPE2-PARSER-GATE-STATIC-01`.
- At parser `0x005D4160`, `0x005D4298 -> 0x005E6E10` obtains a 16-bit selector, `0x005D42A0` saves it in setup `+0x520` slot and `0x005D42A8/0x005D42B1` rejects negative or >=3. The accepted integer types are 0/1/2; type2 is a supported **static parser path**, not proof that any real game OGG uses it.
- `0x005D42B7` reads callback group `0x00612E60 + selector*4`, then `0x005D42C6` indirect-calls parser in group+4; `0x005D42CD/CF` rejects NULL result. For type2, table group `0x00612E68 -> 0x0061AEA0`, parser `0x0061AEA4 -> 0x005DFE10`.
- The `0x00612E6C` adjacent pointer belongs to a **different mapping selector** (`0x005D4324` rejects type>=1), and must not be misreported as a fourth valid residue kind. 00H prior callback work is a predecessor, not another discovery.
- Source: `rea_lab/decomp_task/REA_20261101_01H_P0_VORBIS_RESIDUE_TYPE2_PARSER_GATE_STATIC.md`, SHA256 `C53F251C1125984A2B3CC1A6417ECC5687BB0C00F4181FE8279CE1B93045C271`. Evidence `REA_20261101_01H_P0_RESIDUE_TYPE2_EVIDENCE.json`, SHA256 `D2E1D821D121A1FC3976F791DE5642B8F332F742062DA112016B15EF27850C16`. Owner earlier reported **42 independent static audit checks PASS**, not repeated for this recovery batch.

## 02H A — first divisor: normal-return parser EOF latch

**ID** `REA-LOCAL-20261101-02H-P0-VORBIS-RESIDUE-FIRST-DIVISOR-PARSER-ERROR-LATCH-STATIC-01`.
- Parser `0x005DFE10` reads 24 bits at `0x005DFE50`, increments at `0x005DFE55`, writes `residue+8` at `0x005DFE59`: a successful read 0..0xFFFFFF maps to 1..0x1000000. Reader failure -1 maps to zero, **but** subsequent 8-bit read from the same EOF-latched reader fails and `0x005DFE75 -> 0x005DFF98` takes NULL-result error return.
- Decoder `0x005E0DC0` first stride divisor uses `[residue+8]` at `0x005E0DCD`, then `0x005E0DFE idiv`. Under **successful parser return + no later mutation** the stride is nonzero; uninitialized/modified state, alternate routes, and actual runtime zero-divide are not excluded.
- Source: `rea_lab/decomp_task/REA_20261101_02H_P0_VORBIS_RESIDUE_FIRST_DIVISOR_EOF_LATCH_STATIC.md`, SHA256 `DE075C58955045FE4A9C4AC1D22730D98382773B1486697E54EA621AF60C37F8`. Evidence `REA_20261101_02H_P0_RESIDUE_DIVISOR_EVIDENCE.json`, SHA256 `C7566A72FEC7A944431E54CA3538838626F981F1ED5AA830D370145A7F280AC5`. Owner earlier reported **32/32 native static checks PASS**.

## 02H B — second divisor: selected book dimension producer chain

**ID** `REA-LOCAL-20261101-02H-P0-VORBIS-RESIDUE-COMPILED-BOOK-DIVISOR-STATIC-02`.
- `0x005DFE10` parser selects book via `residue+0x14` and setup `+0x720` array; at `0x005DFF70/0x005DFF72` rejects book dimension <1. Initialization `0x005D57C0` type2 callback table `0x0061AEA8 -> 0x005DFFC0` loads compiled books from setup `+0xB20`, indexed by book number*0x38, and stores pointer into runtime residue `+0x10`.
- Constructors `0x005DA070` and `0x005D9F40` each copy book dimension to the compiled record's first DWORD. Decoder `0x005E0DC0` reads `[residue+0x10]` then the compiled record's dimension; `0x005E0E0C idiv ecx` uses it. **Only under same-book, normally successful init with no later modification** can the second divisor be treated >=1. This is NOT a global no-zero-division proof.
- Source: `rea_lab/decomp_task/REA_20261101_02H_P0_VORBIS_RESIDUE_SECOND_DIVISOR_COMPILED_BOOK_STATIC.md`, SHA256 `AC900C5CE98F24F3934A75173F927EB22329A3169CF3BCC7C9556723F410C158`. Evidence `REA_20261101_02H_RESIDUE_BOOK_CHAIN_EVIDENCE.json`, SHA256 `D14C5C68037191B75D765CD1FBD4990EE5C5D95117CEC826639EA24B17F1E48A`. Owner earlier reported **37/37 static checks PASS**.

## Curation / errata / limits
- Cross-check earlier 00H callback table & 10/31 23H decoder sites; do not recast those as new. 2026-11-01 03H/04H offline candidate reports subsequently qualify some **residue power bound assumptions**; issue #3 governs corrections before any shared KB promotion.
- No original-game Golden PASS, strict MATCH, formal new REA 5-method completion, new VERIFIED or READY resulted from this recovery; **all remain 0**. Full replication rate unmeasured. These 3 source IDs are neither 3 measured gameplay findings nor 3 newly acquired dynamic functions.
- **KB_CANDIDATE:** `0x005D4160`, `0x005DFE10`, `0x005E6E10`, `0x005D57C0`, `0x005DFFC0`, `0x005DA070`, `0x005D9F40`, `0x005E0DC0`, `0x005E0DFE`, `0x005E0E0C`; offsets `+0x520/+0x720/+0xB20/+0x14/+0x10/+8`; owner REA/T015. Curator should attach corrected assertions to REF_AUDIO_VORBIS or a focused residue index, not overwrite source history.
- **Next VERIFY:** original game OGG type2 incidence without unauthorized execution, alternate book writers/mutation, allocator-failure entry into decoder, exception-safe reimplementation tests. Old source files remain on authorized PC; only these sanitized findings and hash pointers appear in GitHub.
