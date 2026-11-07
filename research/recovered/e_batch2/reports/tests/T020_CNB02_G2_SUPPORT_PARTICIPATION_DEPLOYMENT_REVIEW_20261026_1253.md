# E-AUDIT-20261026-1253-T018-T020-SUPPORT-PRESENCE-DEPL-REVIEW-01
Owner E: T018/T020; T019 read-only. 2026-10-26 12:53 JST. STATIC RESEARCH / SYNTHETIC TEST EXECUTED / VERIFY / NOT READY.

## Source and distinguishing result
- Desktop Commander Local Compact connected. Read MASTER, ANALYSIS_LANES_PROTOCOL, A-D HANDOFF, REA saved PROGRESS, dev IMPLEMENTATION_PLAN, T018/T019, earlier E G2 validators, search index README. No native EXE startup or Ghidra rebuild.
- New E-only overlay: t020_cnb02_g2_support_presence_deployment_review_20261026_1253.py. Actual file SHA256 0320A180906CBFF14EC943011FB24BDA1835D2C53669EF7C99724513A01F1F4A (PowerShell Get-FileHash).
- Previous E 11:58 cross-role review SHA256 9EBB19F73F284D119FA536308AF9DA9694DB8181A0E5E0DA2189C0FA2B2F6AC8. Old logic distinguished presence of attack/defense roster but had no review of support-participant presence vs support-deployment receipt.
- New conditional flags: SUPPORT_DECLARED_WITHOUT_DEPLOYED_RECEIPT_REVIEW; SUPPORT_DEPLOYED_RECEIPT_WITHOUT_DECLARED_PARTICIPANT_REVIEW. Both mean REVIEW, NEVER original game bug or fatal mismatch. Support Power may be recorded even if third Side Troop=0, or the participation lists may not enumerate deployed Units.
- Empty support participants and no support roster remains a valid syntactic possibility, NOT proof of absent native support. Nontext support participants are diagnosed by upstream, not silently treated as genuinely absent.
- This is a review of declared-role/visible-roster shape only. Power ID cannot be assumed equal to Unit/Troop ID; cross-role visible aliases cannot establish native pointer alias; clocks and game epochs are not bound here.

## Execution and acceptance
- New tests 12/12 PASS; combined seven E generations (2026-10-25 11H plus 2026-10-26 08H/09H/10H/11H unhashable/11:58 cross-role/12:53 new) 89/89 PASS, all synthetic, no source game observation. Python -B on PC, results 'Ran 89 tests ... OK'.
- Tests cover support=[] baseline, support participant+roster, one-sided absence both directions, invalid participant, invalid support roster, old defense receipt check, prior cross-role alias, malformed object/schema, fake SHA, multiple support participant labels not equal to missing troop count, and input immutability.
- G0 legal native UI attack receipt NOT QUALIFIED; G1 same-run immediate prebattle SAVE bytes/hash+input NOT QUALIFIED; G2 real loaded MAP, three Side/Power roles, ordered deployed Unit/Troop identity and atomic epoch NOT QUALIFIED. G3 result and G4 World/Record state diff NOT QUALIFIED.
- This code cannot return original actual Golden PASS or strict MATCH; E new DYNAMIC OBSERVED 0, actual Golden PASS 0, strict MATCH 0. Historical partial Watch and non-atomic RAW8 retained, not joined or reclassified.
## E ledger/contradictions/regression and safety
- MASTER latest formal checkpoint196, READY596=A115/B229/C136/D116 (prior formal values, not full READY reenumeration this run). TASK QUEUE directly re-counted today from actual MASTER: 34 Tasks, DONE9/IN_PROGRESS21/VERIFY4; newly integrated READY IDs none. This E note and test are independent NOT READY, MASTER unmodified.
- T019 new confirmed DAT/Wiki/EXE contradictions 0. GameClear exact DAT13 + TXT2 broad lexical scope remains RESOLVED; script2 winner/phase, runtime TXT load, and gwrite after GameClear remain VERIFY.
- New unsafe-operation refusal 0 and connection failures 0 in this run; old blocked E T018 table/session joins, C T026/T032, D incomplete T030 TSV, VA0x5710C0 and earlier refused write operations remain separately BLOCKED, never retried via alternate shell/path/tool/Remote/ZIP.
- Old E 13H/14H OFFLINE-UNSYNCED not reconciled; other owners' new NOT READY notes not adopted. 原本 EXE/ZIP/DAT/SAVE, A-D, REA, dev_lab, Git/push, Work, settings and schedules unchanged.
- Next: one legitimately launched original C-NB02 battle, G0 UI action+exact window; G1 same-battle SAVE byte hash+input receipt; G2 actual loaded MAP SHA, both Power identities, support role and ordered Unit/Troop identities; explicitly distinguish support-present-but-zero-deployment from unobserved support; verify epoch and old/new input equivalence before formal receipt acceptance.
