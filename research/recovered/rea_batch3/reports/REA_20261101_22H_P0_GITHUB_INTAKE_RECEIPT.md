# REA 2026-11-01 22H｜GitHub PRIVATE intake / 原本x86 P0研究保存・読み戻しreceipt
- 作業ID: `REA-LOCAL-20261101-22H-P0-FSOPEN-EMPTY-NAME-UNWIND-STATIC-01` / 担当 REA/T015。
- 状態: `PC-SAVED / PUBLISHED_INTAKE / NOT_CURATED / NATIVE-STATIC / VERIFY / NOT READY`。
- PRIVATE GitHub: `ButaMonky/Hakushin067-Research-Knowledge`。Owner固有隔離branch: `intake/rea-20261101-22h-fsopen-native-r1`、HEAD `f9384eeb024e25a871438e56cffeef064245cd0b`。`develop` は変更していない（compare: ahead3/behind0、変更は `research/intake/REA/` の3ファイルのみ）。
- 専任curator用DRAFT PR: `https://github.com/ButaMonky/Hakushin067-Research-Knowledge/pull/10`（OPEN/DRAFT、未merge）。所有sourceのprivate入庫であり共有symbols/REFの正式採録とは異なる。

## 原本P0静的確認
- 0x005D1CB1 `__fsopen` で `__getstream` のnonNULL後に filename先頭0を検査し、空文字なら errno=22 → `0x005D1D33 -> 0x005C3500` の明示3引数local unwind。SEH4 table `0x00641798` のcleanupは `0x005D1D63`（親EBP+8を読んで `0x005BDB44 __unlock_file`）。通常経路 `0x005D1D55` も同一helperをCALL。これは現物原本x86に基づく局所分岐、実機ロック解放成功・DLL ABIは未証明。
- 新規 `REA_20261101_22H_P0_FSOPEN_SCOPE_AUDIT.py` 29/29静的PASS、再実行時は既存EVIDENCEの非時間依存部分との一致を検証し上書き無し。監査再実行約0.89068秒。原作ゲーム実行無し。
- 原本一致PE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、V9 SQLite `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE` 現物再計算一致。SQLite quick_check=ok。
- 22H owner日本語報告 `REA_20261101_22H_P0_FSOPEN_EMPTY_NAME_UNWIND_STATIC.md` SHA256 `614554CF6BC019DAC8E1AD955F1BE2D511020D4724E67858BBA93D47122C10DE`、証拠JSON `REA_20261101_22H_P0_FSOPEN_SCOPE_EVIDENCE.json` SHA256 `BE8DFE4A64F895EF5C2BAE3D1AF052D44B8A9182FED65902A35AB7DE55120A27`、監査py SHA256 `7A7D44A2BB3556C9D8807D097BDC969780EDFC5E73071A4A1E4D1DDC588F2862`。別 `REA_20261101_22H_P0_FSOPEN_INTAKE_READBACK.py` でPC全文読戻し/JSON 29/29構文・対象ID一致 PASS。

## GitHubへ入庫した5研究ID（過去成果を重複加算しない）
- ① `REA-LOCAL-20261031-22H-P0-VORBIS-GROWTH-CALLER-PAIR-STATIC-01` （2段grow caller）。
- ② `REA-LOCAL-20261031-23H-P0-VORBIS-GROWTH-TAIL-BOUNDARY-STATIC-01` （正規関数範囲・2除数）。
- ③ `REA-LOCAL-20261101-00H-P0-VORBIS-INDIRECT-CALLBACK-DISPATCH-STATIC-01` （間接CALL 3箇所、root/table）。
- ④ `REA-LOCAL-20261101-21H-P0-UNWIND-FOUR-CALLERS-NLG-STATIC-01` （既存20Hとの差分）。
- ⑤ `REA-LOCAL-20261101-22H-P0-FSOPEN-EMPTY-NAME-UNWIND-STATIC-01` （今回新規、3引数＋scope共有cleanup）。
- OwnerからのGitHub原文保全先: `research/intake/REA/INDEX.md`、`REA_20261031_22H_23H_20261101_00H_GROW_CALLBACKS.md`、`REA_20261101_21H_22H_FSOPEN_UNWIND_STATIC.md`。private branchで3/3独立fetch/readback成功、研究ID/Source SHA/Golden境界と非機密を確認。commit順 `8987d4ee30d2c15df06674a27f8d4f0405fa3955` → `543486872665b34478e8394263b8c7702d434c68` → `f9384eeb024e25a871438e56cffeef064245cd0b`。
- GitHub参照: `https://github.com/ButaMonky/Hakushin067-Research-Knowledge/blob/intake/rea-20261101-22h-fsopen-native-r1/research/intake/REA/INDEX.md`。

## 境界・次の再開点
- **正式CURATED増分は今回0**（Owner入庫のみ）。新規正式5種証拠完備0・REA VERIFIED0・TODO/VERIFY/BLOCKED公式差分0/0/0、原作Golden実測PASS0、strict MATCH0、READY0、完全複製率不明。旧正式VERIFIED64件は先行履歴で二重計上せず。
- 既にKB developに採録の11/1 17H、19H、20Hは今回再採録0。18Hの部分EVIDENCE JSONはSAFETY-HOLD、内容再取得・別経路追記・GitHub出版をしない。
- 次回未収録カーソル: 11/1 01H residue type2 parser、02H FIRST_DIVISOR と同時間帯 SECOND_DIVISOR（**研究ID 2件**）、次に03–16H Library14ID/67files（GitHub Issue #3）。同研究の訂正とsource SHAを比較してOwner intakeに差分追加、既採録は二重処理しない。
- 次のP0関数: `0x005D2165 __getstream` のFILE* lock lifetime・error帰還、`0x005D1D63` の正常/exception経由でのEBP維持。原本/共有Git/他ownerのworktree、MASTER/QUEUE/PROGRESS、スケジュール無変更。
- 本回の読み戻しワンライナーに一度PowerShell引数のSyntaxErrorがあった（書込動作なし）。新規専用readonly readback scriptで正常検証。安全拒否ではない。開始時REA専用 `active.lock` はENOENT。PC CPU/RAM負荷・全作業時間は未測定。
