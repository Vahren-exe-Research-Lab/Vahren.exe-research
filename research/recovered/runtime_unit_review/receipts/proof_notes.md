# Proof notes (inclusive source lines)

All Sxx references use source_index.json, which pins full source path and SHA256.

| Claim | Evidence | Limit |
|---|---|---|
| Live pointer and mode | S03:L69-L70; S06:L4 | EAX/ESI local pointer; no global Unit alias |
| HP +0x90 / max +0xDC reads | S06:L5; S03:L71 | FILD/FIDIV, operand width omitted |
| +0x738 write | S06:L5; S07:L7 | signed clamp is operation, not storage type proof |
| +0x185F4 read/write | S06:L4-L6; S03:L72 | mode/guards and helper normal return conditional |
| constructor +0x185F4=0 | S07:L3-L4 | report provenance only; no proposed owner edge |
| countdown A | S07:L5 | >0 decrement, at zero guard +1867C/+8C before unlink; owner edge withheld |
| countdown B | S07:L6 | +1867C nonzero skips decrement itself; caller/cadence unknown |
| no frame/visibility claim | S07:L2, L6-L7, L9-L12; S03:L74 | original/new Golden remain zero |
| descriptive name basis | S02:L234, L240; S09:L4; S10:L7-L11 | constructor vptr support, not every callee's concrete class |
| UnitDef distinction | S01:L7, L11, L13; S05:L12-L14 | same offset numbers are unrelated evidence |
| R/P/L correction | S03:L35-L39, L60; S06:L4; S07:L7 | common helper is not shared object type |
| deferred MP/Skill | S08:L3-L4, L10-L14; S02:L137 | local debit stage; canonical Skill owner and outer registered owner not bound |

The only extra reviewed report bodies beyond the mandatory list are S09 and S10. Filename inventory was constrained to constructor/summon/destructor patterns in research/recovered; no other extra report body was opened. Native paths mentioned inside the reports were treated as provenance strings and never followed.
