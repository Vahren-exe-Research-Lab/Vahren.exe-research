# Bounded v2 implementation — 2026-10-27
Owner: bounded_count_adapter. Status: candidate built and private-memory tests PASS; independent review/native acceptance pending. No deployment, game input, Git, original EXE/DAT/save or protected source edits.

## Contract
- Exact routine(hk_ui_select_v1) stays fixed3. Exact routine(hk_ui_select_v2) opts into count2 or4, inferred from validated candidate vector and required matching reference vector. Other routine names do not opt in.
- Storage max4, one signed column. Supported ordered candidate profiles: akys/kmr and akys/kmr/tnok/rma; v1 akys/kmr/tnok remains exact.
- Snapshot owns version/count/candidate/reference/value copies. Result success is 0..N-1, including index3 for four; native Cancel label is at N. Overlay cancel retains native fallback without stores.
- Native labels are checked against the supported ID profile plus Cancel, max5 labels (last allowed bytes base+4BBC2F). No arbitrary labels/IDs accepted.
- V1 snapshot wrapper and its exact-three validations remain. V2 uses separate map lookups of five output keys and <=4 requested value keys. The existing map cap8 is unchanged. Global record-cell address uniqueness checks span both lookups.
- Existing consume-before-write, no retry after partial writes, serial/opening/lifetime, wrapper ownership and owner-before-popup cleanup remain.
- Build script has optional -OutputDirectory; default unchanged. This candidate and tests are in bounded_v2, outside production DLL output.

## Evidence
1. RED: compiled actual adapter fixture with Zig x86 C11 -O0 -UNDEBUG -Wall -Wextra -Werror and Win32 libraries; executable native-red.exe returned1: 'FAIL: v2 count2 observer did not accept bounded request'. PID13232 captured RED.log. Existing v1 adapter checks passed first. No implementation code had been changed for this first RED.
2. GREEN command (project-relative): core/build_dat_ui_selector.ps1 -Test -OutputDirectory <this-folder>/bounded_v2. PID28756 exit0. Guard plus actual adapter -O0/-O2, then isolated DLL build. Output GREEN.log.
3. Actual adapter tests use private VirtualAlloc relocated x86 memory and transparent nonactivating fixture controls; original close is fixture stub. Both N2/N4 exercise actual literal observer, numeric capture, binding, panel sort, source mapping, stores and once-only close. Negative/tied values -7/55/-7/12; stable ascending order 0,2,3,1 for N4; RMA returns ordinal3/backend1.
4. Seventeen malformed cases per count: counts0/1/3/5, reference count mismatch, duplicate refs/IDs, missing numeric key, value/output alias, value/value alias, output/output alias, unknown ID, wrong Cancel/count/label, fourth-reference/output alias, duplicate requested numeric-map key. Rejection produces no store/close. Also v1 rejects N2/N4; unknown routine preserves pending request; ordinal N rejected; overlay cancel and stale lifetime produce no native commit.
5. Existing suites request/session/snapshot/choice/literal/context/panel/composed built/run at O0 and O2 (16 successes), PID9932 exit0. Command: zig cc -target x86-windows-gnu -std=c11 <opt> -msse2 -UNDEBUG -Wall -Wextra -Werror tests/test_work_dat_ui_<name>.c -ladvapi32 -lcomctl32 -lgdi32 -luser32 -o <bounded_v2>/<name><opt>.exe; execute each, require exit0. REGRESSION_FINAL.log records passes.
6. Standalone existing dispatch suite is NOT verified: dispatch-O0.exe launch returned Windows NativeCommandFailed ('operation canceled by user') after127s, PID8644 exit1; no fixture result. A corrected -msse2 retry was already pending before that result surfaced; stopped owned loop PID18928 (exit4294967295). No further dispatch launches/renaming/bypass. REGRESSION.log retains first launch failure. Actual adapter uses dispatch source but is not a substitute for this standalone ABI regression.

## Intermediate failures and scope notes
- First edit helper failed quoting, second failed stdin Unicode path decoding; neither wrote files. Corrected UTF-8 stdin.
- One implementation helper stopped at runtime UTF-8 decoding, before build-script edits. Following build therefore used old default output and rebuilt guard/native test executables; native v2 failure stopped before DLL build. Default production fixture DLL remains byte-identical SHA CDC4554CF9AB4F542C0360A52B92B4D975A415418EB5BBB3D286322AB0A67438.
- After implementation first N2 test correctly hit old session epoch because fixture reset native epoch while retaining session. Fixed test setup to advance monotonically (no session reset). O0/O2 then passed.
- Standalone v1 choice fixture initially failed because handcrafted snapshot lacked new internal version/count fields. Added explicit version1/count3; all original assertions remain and pass.
- Only authored production/test files listed below changed, plus generated test artifacts described above and this report/logs. No production DLL/manifest/DAT deployment.
- This is bounded feasibility only, not arbitrary candidate API, actual-game resumption, fullscreen/lifecycle coverage, education integration or production migration. Parent owns independent review/deployment/live acceptance.

## SHA256
- src/work_dat_ui_request.h: 6f234e03784340dcf25bf57305bbae27f425f7806c4ca4a3b149ec05c88c5318
- src/work_dat_ui_session.h: a3bfe9715ee5e4ee0fb4ac740a5994173212cee2b3d4e67fc3c244ce5a613d3e
- src/work_dat_ui_snapshot.h: 80b939a457b7e493484657162a38c11c4c3c3b86d68f33b4dd8c6e95955d4b6a
- src/work_dat_ui_choice.h: 3884236b0966671add3e317c719e2821057359c264ccd9209c8eddc3b55f5285
- src/work_dat_ui_literal.h: fc932d45c673014d3c87b3ea52608f1c79557b3e2d8d2bb94a791ab649dd89c7
- core/dat_ui_selector_runtime.h: e5b6b7cff20eb3368e76e01fee9c8e17e12f123e71ead356cb05417198cc058b
- core/test_dat_ui_selector_native.c: 1677d537d5484c73f07674a5022ba4a3d59af1a9515424a839130fb4c8859224
- core/build_dat_ui_selector.ps1: 7211e73e2250dffb0494086f5221d6a0b2a1365e88d77f16ddcf4552b821b90d
- tests/test_work_dat_ui_choice.c: 096d931f2fa641178f09e8fd1f2eb7ba50308d9e0ab3210fb0c7b30f8cee2b21
- bounded_v2/HakushinDatUiSelector.dll: 3a17cd64a07a8e1b2c19ed107776702aaf21762c353a211d1c32e09a3dd57ead
