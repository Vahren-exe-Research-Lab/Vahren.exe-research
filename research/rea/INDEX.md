# REA/T015 | 2026-11-01 ftell・SEH4 の出典別統合（3研究ID）
この索引と直下の3報告は **private develop** 用の軽量な原作x86研究記録。元のREA所有資料を読取専用で照合し、報告3本のバイト一致コピーを配置。ゲーム本体・PE・SQLite・証拠JSON・セーブは収録しない。

## 研究ID → 原本報告 → 意味 → 元の根拠
| 研究ID / source report（GitHub閲覧可） | 確認された限定的意味と主要VA | 原本報告 SHA256 |
|---|---|---|
| [REA-LOCAL-20261101-17H-P0-CRT-FTELL-FRAME-CROSSWALK-STATIC-01](REA_20261101_17H_P0_FTELL_FRAME_STATIC.md) | `0x005B797C` 91-byte ftell SEH4 entry、`0x005B79D7` は同じEBPを用いるunlock helper。NULL/invalid-parameter経路は常に正常returnとは限らない | `1B4E5F70C04CB60DF97E762A11B5B48ED6EA98DF42E3DD8AA7A90DF4C1ED13EC` |
| [REA-LOCAL-20261101-19H-P0-FTELL-SEH4-SCOPE-STATIC-01](REA_20261101_19H_P0_FTELL_SEH4_SCOPE_STATIC.md) | `0x00641260` にscope record、`parent=-2` / `filter=0` / cleanup `0x005B79D7`。正常系のCALL `0x005B79C9` との一致 | `294608BA2F0FF4523B4129CBE082FD8B759E3977C9C820CE6B625B79C0C5B2A4` |
| [REA-LOCAL-20261101-20H-P0-EH4-DISPATCH-PHASE-STATIC-01](REA_20261101_20H_P0_EH4_DISPATCH_PHASE_STATIC.md) | `0x005BB6E0` 検索/unwind分岐、`0x005C3500` のscope走査と `0x005CC2D4` trampoline。active scope時に間接cleanupへ至る**条件付き静的経路** | `7A97C502DB0DDB0FC02EF682AF3196A38953F43134DAFDFF3FD4E0517A458D0E` |

## 読取専用PC出典・ハッシュの境界
- 元PE：`rea_lab/targets/hakushin067_Vahren.exe` / SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`（2026-11-01現物再ハッシュ一致）。
- 現行V9：`rea_lab/headless_analysis/search_index/HAKUSHIN067_UNIFIED_V9_20261023.sqlite` / SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`（現物再ハッシュ一致、141,033,472 bytes、GitHub非収録）。
- 元レポートはPC `rea_lab/decomp_task/` の同名Markdown。各GitHubコピーは元PCファイルとSHA256完全一致。元監査・証拠は下記の相対PC専用パスを参照。これらはGitHubには無い。
| ID時刻 | 読取専用のEVIDENCE.json（PCのみ） | 原本SHA256 | 静的監査の元報告 |
|---|---|---|---|
| 17H | `rea_lab/decomp_task/REA_20261101_17H_P0_FTELL_FRAME_EVIDENCE.json` | `5769492A8962B24838BBF57D2715D9245B258674C34B0577DDC79BCDE278F1C7` | 38/38 PASS |
| 19H | `rea_lab/decomp_task/REA_20261101_19H_P0_FTELL_SEH4_SCOPE_EVIDENCE.json` | `A1B7519A5724717246776923816A481C5AA997D978CD81C96E4E51E00F3541F5` | 25/25 PASS（readback） |
| 20H | `rea_lab/decomp_task/REA_20261101_20H_P0_EH4_PHASE_EVIDENCE.json` | `0078643B70D22652D1A1BCBA9840A49FD31E12EFB8D3A371ABA570427FAB3444` | 32/32 PASS |

## 先行研究、訂正、重複排除
- 旧13H/14Hの「`0x005B797C` がGhidra旧索引で関数未登録」は**旧V3に限る**。現行V9では2026-10-23に `PE_CODE_ENTRY_005B797C` として91 byteを既に復元済み。17Hでの**新規関数発見とは数えない**。
- 16Hオフライン研究 `REA-OFFLINE-20261101-16H-P0-SEEK64-ABI-FTELL-GAP-NATIVE-STATIC-01` が示した `0x005B79C9 -> 0x005B79D7` は既知。17Hは関数フレーム・NULL時エラーガード、19Hはscope table、20Hは例外処理2フェーズを**別々の追加根拠**として採録。16H自体はこの3件のGitHub統合件数に含めない。
- 18H `REA_20261101_18H_P0_INVALID_PARAMETER_TAILJUMP_EVIDENCE.json` は**安全拒否を伴う未完成・HOLD**。追記や拒否操作の再実行、別経路取得、成果採用を行わない。
- 正常系のunlockと、例外時の条件付き候補を区別する。例外配送、stack/EBP全分岐、NULL時実挙動、SEH cleanupの実行回数、元ゲームのクラッシュ・互換性はすべて **INFERRED/VERIFY**。

## 統合状態・相互参照
- REA正式の新規5証拠セット完備 **0**、新規正式VERIFIED **0**、公式TODO/VERIFY/BLOCKED更新 **0/0/0**。原作ゲーム Golden実測PASS **0**、strict MATCH **0**、READY **0**、完全複製率未測定。
- **分野別意味:** [REF_AUDIO_VORBIS.md](../../REF_AUDIO_VORBIS.md) の2026-11-01節。**VA検索:** [symbols.tsv](../../symbols.tsv) に今回の独立原本x86で確認された3アドレスを登録（既存V9関数索引と同一エントリは増やさない）。
- 11/1 03H–16Hの14件／Library計67ファイルはこの3件への一括採用を意味しない。PC owner原本との厳密な同一ID/訂正/SHA検証が済むまで **OFFLINE-UNSYNCED / VERIFY / NOT READY** の別キュー。


## 2026-11-02 01H state3 early-caller source — separately curated
- **One additional REA source ID:** `REA-LOCAL-20261102-01H-P0-OGG-STATE3-DUAL-ENTRY-ESI-ABI-STATIC-01`; [owner original-source intake](../intake/REA/REA_20261102_01H_DUAL_ENTRY_ESI_ABI_STATIC.md), [curated explanation](../../REF_AUDIO_VORBIS.md), BLOB on private owner [PR #16](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/pull/16) at head `857d1f95e56db33bb2aa898c8a5b1b8879a315f5`. Not a fourth new report copied to this `research/rea/` directory.
- PC report SHA256 `A6217D547C1DA7EBD899A97E30B1F7BAF1E81595962AEDEBF8825F235F07D78B` and evidence JSON SHA256 `758EA165AC324844A743FFA5550E2DBCDC61B96C850130153312CB1E1CDAA35B`; original PE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`. Native `0x5D0B8A -> 0x5CF970` and previously known `0x5D0D67 -> 0x5CF970` E8 edges were independently matched, as were source windows `[0x5D0B60,0x5D0B98)` (SHA256 `44FE4A5DAFBF23EB3B79E2B19B2634FB45B4ABFDA410FD1FDBA644746B9DF5AF`) and `[0x5CF970,0x5CF9D7)` (SHA256 `E9F9D9A7B9007542C5C127B9A50CDC2CF176034912B5D2F67AABFBC058C200F3`).
- **CURATED_STATIC delta:** the early nonnegative caller route and `[ESI+0x58]`-dependent state3 gate are new; the later cached-reentry edge was already recorded in `REA-OFFLINE-20261101-08H-P0-VORBIS-CACHED-STREAM-STATE3-REENTRY-STATIC-01`. No complete hook ABI, dynamic game reachability, return/exception guarantees or producer ownership proved. Original gameplay Golden PASS=0, strict MATCH=0, DYNAMIC=0, new READY=0.
