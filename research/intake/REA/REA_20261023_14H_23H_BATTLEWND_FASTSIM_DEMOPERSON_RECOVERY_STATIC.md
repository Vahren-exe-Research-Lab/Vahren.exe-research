# 2026-10-23 REA historical battle clock / fast simulation / DemoPerson source-recovery

Owner independent REA; PRIVATE owner intake, STATIC/INFERRED/VERIFY and NOT CURATED. Ten distinct **historical** source research IDs. This source owner created the reports on 2026-10-23, not in this GitHub recovery. Source report byte SHA256 and, where present in the owner directory, JSON evidence byte SHA256 were recomputed read-only on the authorized PC on 2026-11-02 JST; there is no new PE/Ghidra V9 re-run, original game run, dynamic reachability proof or newly formal five-method bundle. PE reported historic target SHA256: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`. Older 14–15H reports reference V3; their native claims require V9/PE recheck before formal curation. The first three source reports do **not** have same-basename adjacent EVIDENCE JSON in the inspected owner folder; do not invent evidence SHA.

### REA-LOCAL-20261023-1435-P0-BTL-AUTO-GATE-STATIC-01

- Original source: `rea_lab/decomp_task/REA_20261023_1435_P0_BTL_AUTO_TRANSITION_GATE_STATIC.md` / SHA256 `885DB1244F93A86E0A8D581A64684C031B1772C296D6856445E448C86A45CD0A` (rehash 2026-11-02 JST). Adjacent same-basename EVIDENCE JSON not found; report and its embedded native traces remain STATIC-source only.
- VA/CALL/offset search anchors: 0x5656A0, 0x5656F3, 0x526140, 0x5261CD.
- Source-backed, limited interpretation: 0x5656A0 routes a normal timer btl_auto equality to 0x526140 with ESI loaded from [0x67B86C] just before the CALL. Conditional 0x5261CD writes 5 to object+0x20. Special clock value 0x80000008 does not take this gate. Original warning text indicates an auto-control mode, but the real input/AI transition was not observed.
- Correction / unresolved / next validation: V3-era index; 0x67B86C aliases, two btl_auto-setting owner pointers, and +0x20=5 downstream consumers need V9 and live evidence.
- Owner=T010/T015 and battle take-over related REA; STATIC/INFERRED, VERIFY; game Golden PASS=0, strict MATCH=0, READY=0. Historical related earlier/later IDs constitute a correction chain, not extra observed functions.

### REA-LOCAL-20261023-1537-P0-BTL-TIMER-MODE-SPLIT-STATIC-01

- Original source: `rea_lab/decomp_task/REA_20261023_1537_P0_BTL_TIMER_MODE_SPLIT_STATIC.md` / SHA256 `BAABC5C4438746BC1B5BE813373522D3BF2A6618AAF15659D3D91B49359DF2D0` (rehash 2026-11-02 JST). Adjacent same-basename EVIDENCE JSON not found; report and its embedded native traces remain STATIC-source only.
- VA/CALL/offset search anchors: 0x492D80, 0x492E95, 0x492EC3, 0x492FA9, 0x49B346.
- Source-backed, limited interpretation: 0x492D80 uses implicit EAX and a one-byte flag at first stack slot, normal RET 4. Nonzero mode can tick through 0x565700 without btl_auto, whereas zero mode branches via 0x49B280 or calls 0x5656A0. Original rel32 audit 7/7 was historical.
- Correction / unresolved / next validation: A clock tick in these branches does not prove a game-state or input auto-switch; timing and full ABI still VERIFY.
- Owner=T010/T015 and battle take-over related REA; STATIC/INFERRED, VERIFY; game Golden PASS=0, strict MATCH=0, READY=0. Historical related earlier/later IDs constitute a correction chain, not extra observed functions.

### REA-LOCAL-20261023-1638-P0-FASTSIM-500TICK-RESULT-STATIC-01

- Original source: `rea_lab/decomp_task/REA_20261023_1638_P0_FAST_SIM_500TICK_OUTCOME_CONTRACT_STATIC.md` / SHA256 `E9D7C28700D261A702D6ACCE065E32D892AC195000C9D54192D6CC03BB0193C2` (rehash 2026-11-02 JST). Adjacent same-basename EVIDENCE JSON not found; report and its embedded native traces remain STATIC-source only.
- VA/CALL/offset search anchors: 0x40E220, 0x40E2F0, 0x40E3B0, 0x514C80, 0x40E617.
- Source-backed, limited interpretation: 0x40E2F0 is an EAX-fed fast-simulation loop of at most 500 iterations; evaluates separate groups [EDI+0x1CC] and +0x1C8 via EAX-input 0x514C80 around each 50-iteration boundary. Returns 2 or 1 for respective candidate outcomes, else 0 including 500-cap exhaustion.
- Correction / unresolved / next validation: 500 is not elapsed milliseconds; return meanings in native settlement and original-game observed outcomes remain unverified.
- Owner=T010/T015 and battle take-over related REA; STATIC/INFERRED, VERIFY; game Golden PASS=0, strict MATCH=0, READY=0. Historical related earlier/later IDs constitute a correction chain, not extra observed functions.

### REA-LOCAL-20261023-17H-P0-BATTLEWND-SECONDARY-VPTR-STATIC-01

- Original source: `rea_lab/decomp_task/REA_20261023_17H_P0_BATTLEWND_SECONDARY_VTABLE_FASTSIM_STATIC.md` / SHA256 `11DE5B516A3A28B3B8FAB2AAF400FB5A6FE117D727CDAF224C28EA2B8A929E7F` (rehash 2026-11-02 JST). Original owner `rea_lab/decomp_task/REA_20261023_17H_P0_BATTLEWND_SECONDARY_VTABLE_FASTSIM_EVIDENCE.json` SHA256 `E25B833D35CA16EC1FE76766F0C520185A0DABBED699CB2EF505748C22A41493`; JSON not uploaded.
- VA/CALL/offset search anchors: 0x6380CC, 0x6380D0, 0x40E220, 0x40E27F.
- Source-backed, limited interpretation: BattleWnd has primary vptr 0x638074 and secondary +0x28 vptr 0x6380CC with slot+4=0x40E220. This virtual method consumes ECX as the secondary subobject pointer and passes EAX=ECX-0x28 into 0x40E2F0; E8 caller count of 0 is consistent with indirect dispatch.
- Correction / unresolved / next validation: Actual virtual invocation and class-substitution reachability are not proved.
- Owner=T010/T015 and battle take-over related REA; STATIC/INFERRED, VERIFY; game Golden PASS=0, strict MATCH=0, READY=0. Historical related earlier/later IDs constitute a correction chain, not extra observed functions.

### REA-LOCAL-20261023-1833-P0-DEMOPERSON-VSLOT18-STATE4-STATIC-01

- Original source: `rea_lab/decomp_task/REA_20261023_1833_P0_DEMOPERSON_VSLOT18_STATE4_STATIC.md` / SHA256 `E9BFEEC1D1046DD9DEE7F228250450D6BEB00B560A53BBB87E4D10C62EBE32A0` (rehash 2026-11-02 JST). Original owner `rea_lab/decomp_task/REA_20261023_1833_P0_DEMOPERSON_VSLOT18_STATE4_EVIDENCE.json` SHA256 `DDAA6A46383DB4C385C43C290779F79D06B48754557B1C2F8309D26EA58052F1`; JSON not uploaded.
- VA/CALL/offset search anchors: 0x40CCF0, 0x8B8E58, 0x8B8E5C, 0x5146E0.
- Source-backed, limited interpretation: Two BattleWnd fields at +0x1C8/+0x1CC conditionally allocate 0x188-byte DemoPerson objects. DemoPerson main vtable slot+0x18 points to 0x5146E0, a four-byte MOV EAX,[ECX+0x20];RET getter shared by multiple Person-style vtables.
- Correction / unresolved / next validation: State code 4 means a native +0x20 value, not automatically a definitive victory/death outcome.
- Owner=T010/T015 and battle take-over related REA; STATIC/INFERRED, VERIFY; game Golden PASS=0, strict MATCH=0, READY=0. Historical related earlier/later IDs constitute a correction chain, not extra observed functions.

### REA-LOCAL-20261023-1942-P0-PERSON-STATE4-WRITER-STATIC-01

- Original source: `rea_lab/decomp_task/REA_20261023_1942_P0_PERSON_STATE4_WRITER_STATIC.md` / SHA256 `CBF0FCF42CFFAADBB9F931C4DE5AAB8F29E6E25FEB4E7EFAB68D348B76E03DE9` (rehash 2026-11-02 JST). Original owner `rea_lab/decomp_task/REA_20261023_1942_P0_PERSON_STATE4_WRITER_EVIDENCE.json` SHA256 `71E39036CCE46D9C08DC68D1BB11742775138536E39EA2B85320F432AF30EC0F`; JSON not uploaded.
- VA/CALL/offset search anchors: 0x44CF80, 0x44CF8E, 0x44B7B0, 0x44B5EA.
- Source-backed, limited interpretation: 0x44CF80 has a +0xA5==0 gate; at 0x44CF8E it sets owner+0x20=4 regardless of +0x18, while +0x18 controls an additional 0x49D1B0 CALL. Other direct writers to +0x20 assign 1,2,3; 0x44CF8E is inside 0x44CF80, not a function entry.
- Correction / unresolved / next validation: A specific DemoPerson runtime instance reaching this writer and any higher-level game semantics still need original-game corroboration.
- Owner=T010/T015 and battle take-over related REA; STATIC/INFERRED, VERIFY; game Golden PASS=0, strict MATCH=0, READY=0. Historical related earlier/later IDs constitute a correction chain, not extra observed functions.

### REA-LOCAL-20261023-2033-P0-DEMOPERSON-STATE4-VIRTUAL-REACH-STATIC-01

- Original source: `rea_lab/decomp_task/REA_20261023_2033_P0_DEMOPERSON_STATE4_VIRTUAL_REACH_STATIC.md` / SHA256 `7BFFE9EE08276EA93C9804DC8186058CF18B6950532D684C80A70FEA906D9EDB` (rehash 2026-11-02 JST). Original owner `rea_lab/decomp_task/REA_20261023_2033_P0_DEMOPERSON_STATE4_VIRTUAL_REACH_EVIDENCE.json` SHA256 `9533CEDCF5004372E9DC5CAB5E2B78CE0AB0D3CD86A3E499AC1AC61420BA0FC1`; JSON not uploaded.
- VA/CALL/offset search anchors: 0x638054, 0x449730, 0x44AE70, 0x44CF80, 0x44987E.
- Source-backed, limited interpretation: DemoPerson secondary vptr+0x90 slot+4=0x449730; ECX (subobject) is rebased -0x90 to the primary owner before calls to 0x44AE70/0x44CD70 and state writer 0x44CF80. Its state4 branch skips one update route but still shares later 0x44A260 cleanup.
- Correction / unresolved / next validation: Indirect caller reachability and all side effects at state4 remain VERIFY; do not claim all updates stop.
- Owner=T010/T015 and battle take-over related REA; STATIC/INFERRED, VERIFY; game Golden PASS=0, strict MATCH=0, READY=0. Historical related earlier/later IDs constitute a correction chain, not extra observed functions.

### REA-LOCAL-20261023-21H-P0-DEMOPERSON-A5-RTTI-GATE-STATIC-01

- Original source: `rea_lab/decomp_task/REA_20261023_21H_P0_DEMOPERSON_A5_RTTI_GATE_STATIC.md` / SHA256 `D237DE3D4F011861923DD25AA93345FBCBE2A0A88A1107156F5A22CC12FED40D` (rehash 2026-11-02 JST). Original owner `rea_lab/decomp_task/REA_20261023_21H_P0_DEMOPERSON_A5_RTTI_GATE_EVIDENCE.json` SHA256 `8ED09873DB8C30988861B0F28BCC032C51DDAF6CE123D922C540EC898775C10F`; JSON not uploaded.
- VA/CALL/offset search anchors: 0x447810, 0x4479C5, 0x4479CC, 0x4479F5, 0x44CF88.
- Source-backed, limited interpretation: 0x447810 conditionally initializes object+0xA5=0, then RTTI dynamic-cast path and flag checks may set it to 1; +0x14 NULL takes an early path. The +0xA5 gate blocks 0x44CF80's state4 write when set; +0x18 only governs a subsequent auxiliary CALL.
- Correction / unresolved / next validation: RTTI flag's gameplay meaning, field lifetime, and definite initialization on every instance remain unknown.
- Owner=T010/T015 and battle take-over related REA; STATIC/INFERRED, VERIFY; game Golden PASS=0, strict MATCH=0, READY=0. Historical related earlier/later IDs constitute a correction chain, not extra observed functions.

### REA-LOCAL-20261023-2236-P0-FASTSIM-DUAL-DEMO-VCALL-STATIC-01

- Original source: `rea_lab/decomp_task/REA_20261023_22H_P0_DEMO_DUAL_VCALL_STATIC.md` / SHA256 `D2FF458F121B0FB9B1A646EC93BF2C6C74E59BA234D4E4CB04439A756226313E` (rehash 2026-11-02 JST). Original owner `rea_lab/decomp_task/REA_20261023_22H_P0_DEMO_DUAL_VCALL_EVIDENCE.json` SHA256 `E240FC47890087A20FA9CFC610FE5116640A616F30A335412D9AFA40A09A409E`; JSON not uploaded.
- VA/CALL/offset search anchors: 0x40E42E, 0x40E445, 0x638058, 0x638B88, 0x51E6F0.
- Source-backed, limited interpretation: Inside eligible fast-sim iterations, the two FF D0 indirect calls use separate group fields, passing object+0x90 to secondary vptr+4 in order +0x1C8 then +0x1CC. DemoPerson slot resolves 0x449730, Enemy to 0x4498E0. Player vptr connects its slot+4 through 0x51E6F0 -> 0x40CCF0 and slot+0x0C through 0x51EF80 -> 0x447810 in conditional paths.
- Correction / unresolved / next validation: Vtable membership and native instruction order do not establish runtime object identity or universal initialization order.
- Owner=T010/T015 and battle take-over related REA; STATIC/INFERRED, VERIFY; game Golden PASS=0, strict MATCH=0, READY=0. Historical related earlier/later IDs constitute a correction chain, not extra observed functions.

### REA-LOCAL-20261023-23H-P0-BATTLEWND-DEMO-FIELD-IDENTITY-STATIC-01

- Original source: `rea_lab/decomp_task/REA_20261023_23H_P0_BATTLEWND_DEMO_GLOBAL_IDENTITY_STATIC.md` / SHA256 `64D1ACE873FA41C0B94D4A36442601827DD0ABE7BF2A93733C503C73D1B4C663` (rehash 2026-11-02 JST). Original owner `rea_lab/decomp_task/REA_20261023_23H_P0_BATTLEWND_DEMO_GLOBAL_IDENTITY_EVIDENCE.json` SHA256 `216031E676D8D6389D3FC9A2F0AB970994AD9707DC1160B4AD48CBDA514577B7`; JSON not uploaded.
- VA/CALL/offset search anchors: 0x8B8C90, 0x8B8E58, 0x8B8E5C, 0x40CB90, 0x40F320.
- Source-backed, limited interpretation: The two global fields coincide arithmetically with BattleWnd+0x1C8/+0x1CC, are zeroed by 0x40CB90 and allocated conditionally in 0x40CCF0. 0x40F320 calls DemoPerson primary virtual +0x04/+0x0C and +0x08; +0x0C connects to 0x447810 if the native class remains DemoPerson.
- Correction / unresolved / next validation: Do not assume that EDI always equals the static BattleWnd base or that all these separate functions execute in one unbroken run.
- Owner=T010/T015 and battle take-over related REA; STATIC/INFERRED, VERIFY; game Golden PASS=0, strict MATCH=0, READY=0. Historical related earlier/later IDs constitute a correction chain, not extra observed functions.

## Owner handoff to dedicated curator

- Read source report SHA, original instruction windows and current V9 E8 before accepting a semantic claim. Avoid duplicate reuse of the same vtable pointer, 500-tick loop and +0x20 getter/writer across adjacent source IDs. Compare with current `REF_BATTLE_TAKEOVER.md` and `REF_SCRIPT_VM_CONTEXT.md`; preserve owner chronology and limitations.
- Nothing here is a verified substitute battle result or a safe handoff ABI. Formal 5-method additions 0; VERIFIED delta 0; historical Wave1–5 64/64 is not newly counted; actual original Golden PASS 0 / READY 0. Source reports/evidence stay on PC, not copied to GitHub. Prohibited Wave6/11-01 18H/VA operations not retried. Next REA recovery: 2026-10-24 20H onward (00–09H is already a separate recovered batch).
