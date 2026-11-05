# Claude ローダー修正パッチ（2026-10-26）— Codex（Work）向け取り込み手順

作成: Claude（研究レーン）。`core/` 本体には一切書き込んでいない。ここにあるのは提案パッチと新規ファイルだけ。
取り込み・Windows 実機テスト・配備判断は Work が行う。Golden/MATCH は 0 のまま（原作実行での実測はしていない）。

## 0. 前提となるベース（この SHA-256 と一致するファイルに対する差分）

```
5ba5607dbbe067f685285327283839fe3fc90fcede6d27621da4cfc2eda9668c  hakushin_core.c
4ddfdb59527647872f7e6fc7983a2dc3bd66233b8dd2c9bedef0893ab27e4fe0  hakushin_extensions.h
e105f2e886d74c38d1aff7480d4fbbf30424bd629d64d9c266e4a4b216e1675b  hakushin_manifest.c
6d81b5cde294c0f4eafd5db6735e843a538d4968ca74995930a67239d54e9a6e  hakushin_manifest.h
2a0b3b80c2bac01f7bd916a85bfc70c59734516dfdd501a937a47194e5857a12  hakushin_bootstrap.c
6b4d8133cf218c5302d9d6fedc691a431edb97d623680b0a488632c5443679fd  hakushin_bootstrap.h
7a85086d74ead75aad47202c7b00bb890cea4049d53cb049e44fda336f6969e7  selector_plugin_adapter.c
9d19b294f750f3a00d9d34a8de5152f1c9d28d98c13cb3a8669bc0c1dfab183b  recruit_plugin_adapter.c
```
第2弾（2026-10-27）で追加したベース:
```
2f16ebea22c2f198e86d9e3b061bdada36b354829628d1364137d94359df0e17  ../src/work_choice_render_pointer.h
c974a9b952909c76bacae99160d6cfb30fd2e58df72cd89373e5f26ce55c26d4  ../src/work_selector_render_integration.h
a59b4df253a3f45c66a5d3214e7b2aa51e26695d9027720f41e032832651b522  README.md
12fdf3d05055154a338cbb5d685e3d89ae30f4c9602227bed55170a5ddded253  CORE_THREADS.md
16025bf73aca7a671ed5f487c159c0833a13c2e764757edef79c22111eefca17  CALL_PATCH.md
9902fd0eea4073f58f97ec3b4e015743ef30bbfafb9647544db71b26f5623f27  STARTUP.md
d237bd1808c02c9d03ee084021537115fc71aa72b38f22a33cd3b7e710e1fe3a  SELECTOR_PLUGIN.md
5d4293102ef8d1b080b71138f100230e354d22c0b8cd523816ac3aa3f7ebf82d  RECRUIT_PLUGIN.md
4cc36f3bd75aa026f48ab135f0b844db1bad87561c25083bba684d0031efe4fa  MANIFEST.md
5e9109502a333fa11ed7e5be091bd358f8fc69694dd437aeb18f5619ed907669  BOOTSTRAP.md
f6aab6ca4f9ea6bfe42f99cb700c8e05cc499e7ecfbade179e054466f16e472c  HOOK_EXTENSION.md
df39cd88c7d4d403eeac753f087f876ed8e3f4f0675f3d55630e51577888ffc2  build_bootstrap_test.ps1
d2d359b996541d457f6f8eb097c50c6c5473fdce6362d38c12275db34f7c9c72  build_core_call_test.ps1
254358d465b30ed012af647109445357a5a52bfe526a794062a06dc4b2895bbc  build_core_events_test.ps1
06702b7f659f2ad86085bec7da1d7264875847d42575b5fc3f01b815797410ca  build_core_extensions_test.ps1
0bc53fe293a6d4c221d60344996acf8ad3de574f174fb5f0e12d7175c7328eb9  build_core_threads_test.ps1
045602f59acfd139acb18d3ca09ec39867340b3faa5b386880ef76b93e6a4280  build_multi_test.ps1
7b03a562194f82334fbe64573d41c163ccf8ac3e8d5d5c4f8ad1705151839b28  build_recruit_managed_test.ps1
f9b9690d99fdf2ca41bc5a8eca7d13c3a8a12dc33dc0189c1ec07d6aa8b5b487  build_recruit_plugin.ps1
06c2fd09401825c93d60af2e789f157c53deb1e1228b653aff9e2e243f938b8c  build_selector_plugin.ps1
248da65bc8aac32c7547fe3bf13aae3fdffc73c9f2cc57930aef4be70b41496a  build_startup_logger_test.ps1
1e5442eb40b211db5393f0fcf73c067ac479e23342e93ad422e609109e4bf870  build_startup_test.ps1
ebdb827ea34e7f685f9648bcc0e071751c2f317f2a7860816d738bce0c33c5a7  build_test.ps1
ba5a0a86fe9b053233adae5a2a1b76d034ba5802a7c3ad8dc1f146c8341b4b8e  test_selector_hover_adapter.ps1
```
ハッシュが違う（Work がその後編集した）場合は差分を手で当てること。改行コードは元ファイルのまま保存済み（core.c / extensions.h は CRLF、recruit は混在のまま）。

## 1. 取り込み

`recruit_sort_v4/` で（`*.diff` は `a/core/…` `b/core/…` 形式）:
```
git apply --check <パス>/*.diff   # または patch -p1 --binary < 各diff
git apply <パス>/*.diff
```
`src_*.diff` は `a/src/…` 形式なので、同じく `recruit_sort_v4/` で当てる。`build_scripts_ps1.diff`（PowerShell 13本）と `docs_md.diff`（md 9本）も同様。全 diff はベースに対して dry-run・適用・結果一致まで確認済み。
新規ファイルを `core/` にコピー: `hakushin_ptr_patch.c/.h`, `hakushin_sha256.c/.h`, `hakushin_loader_wait.h`。
テストソースと `build_claude_loader_patch_test.ps1` も `core/` へ置く: `test_ptr_patch.c`, `test_manifest_sha.c`, `test_ptr_host.c`, `test_ptr_plugin.c`, `test_hash_host.c`, `test_hash_plugin.c`, `test_loader_wait.c`, `test_render_pointer_managed.c`。`build_claude_loader_patch_test.ps1` は既存 ps1 と同じ書き方で、新規テストをまとめて実行する（render_pointer テストは下記 §2 の手順で別に実行）。

**ビルドスクリプト**: `build_scripts_ps1.diff` を当てれば足りる。Core を作る 12 行に `hakushin_ptr_patch.c`、bootstrap をリンクする 5 行に `hakushin_sha256.c` を追加する（追加ライブラリなし。SHA-256 は自前実装）。

## 2. 変更内容（依頼文の番号に対応）

### [2] CALL 書き換え時の静止保証 → 解析結果と対策（loader_wait）
原作 EXE（SHA256 e8dac301…）の静的解析で判明:
- EXE がコードを走らせるスレッドは 3 本。メイン、**起動ローダースレッド** `CreateThread(0x555AD0)`（0x555D98、0x555CD0 内、Graphics_InitDirect3D 0x555500 から）、**BGM ストリーミング** `_beginthread(0x5023E0)`（0x502300、0x502220←0x4BE820）。BGM スレッドは DirectSound バッファの COM 呼び出しとデコーダ仮想関数 1 つだけ。
- **DirectInput8Create（唯一の呼び出し 0x4BCE3B）はローダースレッド上で呼ばれる**: 0x555AD0→0x4B78C0→0x4B9E50→0x4EE0C0→0x4BCDD0。つまり HK_StartupTry と全プラグインの init はメインスレッドではなくローダースレッドで走る。
- ローダー実行中、メインスレッドは PeekMessage ループ（0x555F31、GetExitCodeThread==STILL_ACTIVE 待ち）でメッセージを回す。よって現行の WH_GETMESSAGE 方式は**ロード途中でインストールが走り得る**。ローダー終了後にメインは GameManager::vf01 0x4B9930（0x555E3D）へ入る。
- 例外: `a_system/xp.txt` があると 0x87981B=1 で 0x555AD0 をメインスレッドで同期実行（0x555D7E）。
- 直接呼び出しグラフ上、ローダー（到達 710 関数）からも BGM スレッドからも、パッチ対象の 0x4D45B0 / MercenaryWnd::vf16 0x4D79C0 / Script_DispatchCommand 0x4A1250（0x4A26FE 片）/ 0x41E710 への経路はない。ただしローダー到達関数のうち 197 個が間接呼び出しを含むので、証明ではない。

対策: `hakushin_loader_wait.h`。init（＝ローダースレッド）で `HKLW_Capture()` が**実ハンドル**を DuplicateHandle で保持し（スレッド ID 再利用の誤認なし）、route_worker は UI スレッドが init スレッドと違えば、そのスレッドの終了を待ってから窓を再走査してフックする。同期ロード（同一スレッド）は即続行。待機中に state が PENDING でなくなれば中止。polling 予算は消費しない。selector / recruit 両アダプタに同じ数行を追加。

### [1] ポインタ書き換えの管理 → `HK_EXTENSION_PTR_PATCH`（id 4, v1）
- 補足（訂正）: 0x238238 は selector が init で HKH 予約済み（Core は範囲を知っている）。書き込みは `work_choice_render_pointer.h` の CAS 方式で、Work 側の実装自体は妥当。足りないのは Core 側の復元・所有者追跡。
- `hakushin_ptr_patch.c/.h`（HKPP）: 4 バイト整列の値を **LOCK CMPXCHG 1 回**で置換（他スレッドから見て途中状態なし）。期待値照合、HKH 共有予約（CALL 予約と衝突検出）、slot+generation ハンドル、保護属性は元が実行可能なら EXECUTE_READWRITE・それ以外は READWRITE、書込前の失敗は綺麗に拒否、以降の不確定は RECOVER で保持、復元は置換値か元値のときだけ（未知値は MISMATCH で保持）。
- 読み取りと CAS の間で別スレッドが値を変えた場合は、CAS がメモリを変えないことを利用して綺麗に MISMATCH を返す。
- 戻り値は 32〜39 で、既存の 0〜9 と重複しない。
- Core 統合: QueryExtension で取得。OwnerBusy をロード失敗・終了・release の判定に組み込み済み（`owner_resources_busy`）。管理中の予約は Reservations の release で外せない。
- 移行は任意: selector が使う場合は、init での 0x238238 手動予約をやめること（そうしないと CONFLICT）。

### [3] 戻り値 7 の重複 → `HakushinCore_LastCallGateBusy()` export
- ABI1 と既存拡張テーブルは無変更。core_enter が呼び出しスレッドの TLS フラグに、直近のゲート判定（1=拒否された / 0=通過した）を記録する。
- 戻り値 7 を受けた直後に同じスレッドでこれを呼べば、ゲートの BUSY か、HKCP_OWNER / HK_BUSY かを区別できる。

### [4] 停止状態 → ログ強化のみ（方針は Work が決める）
- init 失敗・終了失敗のログに `; id=<plugin>` と「Core stopped」を付けた。
- 停止中の Load 拒否もログに出す（"core: load refused; Core is stopped after a retained failure (until process exit)"）。
- 挙動（停止フラグが戻らないこと）は変えていない。
- 方針案: 問題のプラグインを保持スロットとして隔離し、所有物の重ならない新規 Load は受け付ける。ただし依存関係とアンロード順の整合が要るので、承認後に別途。

### [5] DLL 改ざん検出 → manifest v2 + bootstrap
- `hakushin-plugins-v2` ヘッダでは 7 列目に SHA-256（64 桁 hex、大文字小文字可）が必須。v1 は従来どおり読める。
- bootstrap の preflight は、ファイルを **FILE_SHARE_READ のみ**で開いて全体をハッシュし、そのハンドルを全プラグインの LoadLibraryExW が終わるまで保持する。照合から読込までの間の差し替え・書き換えを防ぐ。
- 不一致は `HKBP_HASH`（4）。startup のログに preflight=4 と出る。上限は 64MB。

### 第2弾: 0x238238 を Core 管理に移す（任意、ビルドフラグ `WORK_SELECTOR_PTR_MANAGED`）
- `src_work_choice_render_pointer_h.diff`: フラグがあるときだけ、書き込みを Core の PTR_PATCH で行う。
  - bridge 側には独自の `HK_OK` enum があるため、Core のヘッダは include しない。同じレイアウトの型（`WorkPtrHandle` / `WorkPtrCore`）で受ける。
  - 所有スレッドの確認は従来どおり。RECOVER のときもハンドルを保持し、後から restore できる。
- `src_work_selector_render_integration_h.diff`: `WorkSelectorRender_InstallManaged(base, instance, install, restore)` を追加（中身は既存の InstallReserved を呼ぶ）。
- `selector_plugin_adapter_c.diff`（第1弾の loader_wait 分を含む）: フラグがあると、init で PTR_PATCH を取得し、手動予約は 0x1E7E3 だけにする（二重予約による CONFLICT を避ける）。SizeOfImage の確認に 0x23823C を追加。
- フラグなしのビルドは従来と同じ動作（既存 fixture は全件 PASS）。
- テスト: `test_render_pointer_managed.c`。plugin 版は `-DRP_PLUGIN -shared` で `rp_plugin.dll`、host 版は通常ビルドで `rp_host.exe`。ptr_patch 入りの `HakushinCore.dll` と同じフォルダで実行する。

### [6]〜[9] 文書化 → `docs_md.diff`（以下は要旨）
- CORE_THREADS.md: 「プラグインの init / shutdown / イベントコールバック内の SEH 例外は捕捉しない。ホストプロセスごと落ちる。」
- CALL_PATCH.md: 「同一 5 バイトの共有・連鎖呼び出しは非対応。範囲が重なれば CONFLICT で拒否する。」
- STARTUP.md: 「ver0.67 では DirectInput8Create の呼び出しは 0x4BCE3B の 1 箇所で、起動ローダースレッド上にある。それより前に実行済みの初期化（WinMain〜0x555CD0 の前半、ローダー前半）にはフックできない。plugin init はメインスレッドではない（xp.txt の同期モードを除く）。」
- SELECTOR_PLUGIN.md / RECRUIT_PLUGIN.md: 「窓探索は約 60 秒。失敗後の再試行はプロセス再起動のみ。全画面・別の最上位窓があると唯一性の条件で失敗する。」
- README.md: 「actual hook patching … remain later work」を現状（CALL・PTR 管理は実装済み。ゲーム上の有効化は loader_wait 適用と実機確認待ち）に更新。

### 第2弾: [2] の解析を強化（間接呼び出しの解決）
- パッチ対象 5 関数の「祖先」（直接呼び出しをさかのぼった集合）は 29 関数。そのうち間接呼び出しの入口になり得るもの（vtable に載っているか、アドレスを取られているもの）は 12 個: 各 Wnd::vf16、PersonsInfoWnd::vf17、BattleWnd/GameManager/Player の vf01、GameEvent の vf01（Script_ModeDriver）、例外ハンドラ 1 つ。
- ローダースレッドの直接到達は 713 関数。祖先との重なりは 0。
- 仮想呼び出しの変位で照合: slot 16（+0x40）の呼び出しはない。slot 17（+0x44）は 1 箇所（0x559666、D3D デバイスの vtbl+0x44 = Present）だけ。slot 1（+4）は 3 箇所（0x42E74E / 0x43A3DD / 0x4709D0）あるが、いずれも iostream の sentry（`[[obj]+4]+obj+0x38` の streambuf に対する vf1）なので、ゲームオブジェクトではない。
- ローダー内でアドレスを取られている関数 14 個（CRT、ロケール列挙、比較関数など）から直接到達できる 146 関数も、祖先と重ならない。窓・メッセージ系の API（CreateWindowEx / SendMessage / DispatchMessage など）はローダー内にない。
- BGM スレッドの間接呼び出しは 3 箇所で、いずれも DirectSound / デコーダ。
- 結論: 「直接呼び出し＋vtable の slot＋アドレスを取られた関数」の過大近似でも、ローダーと BGM スレッドからパッチ対象には到達しない。残る未解決は、関数先頭より前で値が決まるレジスタ呼び出し約 30 件（大半は CRT の DecodePointer と GDI API を保持したレジスタ）。証明としては「強い静的根拠」の段階であり、loader_wait は保険として維持する。
- 第3弾（2026-10-27）: 残りのレジスタ呼び出しもすべて解決した（API、std::sort の比較関数 0x50BF00、CRT 内部。詳細は FINDINGS §83.6）。ゲームのログでも、init スレッドと UI スレッドは毎回別だった（ACTUAL）。インストールが窓探索の 3〜5 回目（約 0.3〜0.5 秒後）に来ており、ロード中である可能性が高い。loader_wait はぜひ適用すること。EXE は DYNAMICBASE で、実測では 0x820000 に配置されていた。本書の VA は既定ベース 0x400000 の値。

## 3. Claude 側での検証（2026-10-26〜27、Linux 上の Zig 0.14.1 + Wine 9.0 + Xvfb）
**Wine は本物の Windows ではない。** 実機での再実行は Work が行うこと。

| テスト | 結果 |
|---|---|
| test_ptr_patch（モック backend、i386 ネイティブ） | PASS 82/82 |
| test_ptr_host + test_ptr_plugin（実 Core DLL、READONLY ページ、ゲート競合、停止中拒否、復元後 shutdown） | PASS 17/17。RED: 元の Core では init 失敗で 2/5 |
| test_manifest_sha（SHA-256 公式ベクタ 4 種、v1/v2 解析、失敗時に out 不変） | PASS 16/16。RED: 元の manifest ではコンパイル不可（has_sha256 なし） |
| test_hash_host + test_hash_plugin（誤ハッシュは Core 未呼び出しで拒否、正ハッシュは読込、init 中は書込不可、終了後解放、v1 互換） | PASS 9/9 |
| test_loader_wait（未取得、同期、非同期 700ms 待ち、state 変化で中止） | PASS 5/5 |
| Codex 既存スイートを bash に移植して Wine で実行（core 7、multi、bootstrap、manifest、hooks、call_patch、events、core_call、core_extensions、core_events、core_threads、recruit stub 4、managed 3、selector stub 6） | 元のソース 30/30 PASS。パッチ後 30/30 PASS |

| 第2弾: startup 12 ケース＋ logger ＋ proxy 3 種（移植） | 元のソース 16/16、パッチ後 16/16 ＋ v2 追加 3 ケース（正しいハッシュで通常起動・本番 DLL 起動、誤ハッシュはログが `status=8 preflight=4` でプラグインは読まれない） |
| 第2弾: 本番ビルド 4 種（selector 本番、hover research（HIDE_NATIVE_CHOOSER＋HOVER、`-Werror`）、recruit 本番、recruit managed） | 元のソース・パッチ後ともビルド成功。さらに `WORK_SELECTOR_PTR_MANAGED` 付き hover research もビルド成功 |
| 第2弾: production unsupported-host（selector、recruit、managed）、hover adapter（成功、bridge 失敗） | 元のソース 5/5、パッチ後 5/5 |
| 第2弾: test_render_pointer_managed（実 Core、READONLY ページ、二重 install 拒否、別スレッドの restore 拒否、install・restore・再 install、Core の unload 拒否、最後に restore して shutdown OK） | PASS 10/10 |
| 第2弾: build_claude_loader_patch_test.ps1 と同じ手順 | 5 本とも PASS |

未実行: 実機 Windows での全スイート、ゲーム上での確認、`WORK_SELECTOR_PTR_MANAGED` 版を実際の EXE に当てること。

## 4. Work にお願いしたいこと
1. 上記ハッシュとベースが一致するか確認し、`git apply --check` を通してから適用する。
2. ビルドスクリプトに ptr_patch / sha256 を追加し、全スイートを Windows 実機で再実行する（RED/GREEN の記録を含む）。
3. 実機でのゲーム確認は、loader_wait 適用後の診断ログに `route_wait_init_thread` → `route_init_thread_exited` → `installer_begin` の順で出ることを確認する。
4. [4] の方針を決める。

## 5. 第4弾（2026-10-28）: DAT 汎用 UI selector の自動 arm と fixture の修正
根拠と検証の詳細は `docs/PEER_SCRIPT01_FINDINGS_20261011.md` §86。

| ファイル | 対象（ベース） | 内容 |
|---|---|---|
| `dat_ui_selector_auto_arm.diff` | `core/dat_ui_selector_plugin.c`（mtime 1793032353209、SHA256 6e30fe0dd446e5c861fd139ffa957fe8bcc9dccb30ff2ff916e6021b11c6c187） | `WORK_DAT_UI_AUTO_ARM` を定義したときだけ、loading=0（base+0x47983C）かつ scene=0（base+0x6AD434、タイトル）が 30 回・500 ms 続いたら自動で arm して install する。手動の arm メッセージは上書き用として残す。適用後の SHA256 432f033a1bf5491a0abbfbe5678d0d4867222bb654150190a19128ca5c98b83f（CRLF/LF 混在は元のまま） |
| `test_native_stale_log.diff` | `core/test_dat_ui_selector_native.c`（mtime 1793086039450） | `adapter_failure_diag.<PID>.log` を使う前に消す。PID が再利用されると前回のログが残り、`missing or repeated bounded diagnostic` で落ちる（Wine で元のソースが 6/12 失敗、修正後 0/32） |

検証（Wine 9.0、Zig 0.14.1、`-Wall -Wextra -Werror`）:
| 項目 | 結果 |
|---|---|
| 既定ビルドの同等性（フラグなしで `-E -P` を比較） | 違いは `{ }` で囲んだ 1 箇所だけ |
| build_dat_ui_selector.ps1 内の fixture（元、パッチ後の既定、AUTO） | 3/3 GUARD PASS |
| test_dat_ui_selector_native、ログを消して実行（-O2: 元・パッチ後の既定・AUTO 各 12 回、AUTO -O0 6 回） | すべて 0 失敗 |
| test_native_stale_log.diff 適用後、ログを残したまま実行（パッチ後の既定・AUTO × -O0／-O2、各 8 回） | 0/32 失敗 |
| DLL ビルド（既定、AUTO） | 成功。AUTO の DLL には `auto_arm_wait` と `auto_arm_accepted` の文字列が入る |

未確認: 実機で操作なしに `auto_arm_wait` → `auto_arm_accepted` → `patch_active` が出ること、`xp.txt` ありの同期ロード、タイトルへ戻ったときの扱い。fixture は自動 arm の経路（場面番号の読み取りと安定判定）を通らない。

## 6. 第5弾（2026-10-28）: DAT 汎用 UI v3（候補 1〜49 件・数値列 0〜4 列）
根拠は `docs/PEER_SCRIPT01_FINDINGS_20261011.md` §88、DAT 側の仕様は `dat_ui_v3_SPEC.md`。既存のファイルは変更しておらず、すべて新規です（`work_dat_ui_literal_v3.diff` だけが既存ファイルへの 3 行の差分）。

| ファイル | 置き場所の案 | 内容 |
|---|---|---|
| `work_dat_ui_v3.h` | `data/recruit_sort_v4/src/` | v3 の読み取り（`wdu3_capture`）、段階の確認（`wdu3_phase_ready`）、原作 choice との照合（`wdu3_bind`）、書き込み計画（`wdu3_commit_plan`）。読むだけで書き込みはしない。`work_dat_ui_snapshot.h` の `wdus_read`/`wdus_text`/`wdus_map` を使う |
| `work_dat_ui_grid.h` | `data/recruit_sort_v4/src/` | ゲームと無関係の汎用一覧パネル（名前列＋数値列、ヘッダで並べ替え、検索、決定・キャンセル、Esc・右クリックでキャンセル、コールバックは最大 1 回） |
| `work_dat_ui_literal_v3.diff` | `src/work_dat_ui_literal.h`（SHA256 fc932d45…、CRLF のまま） | `wdul_profile()` が `hk_ui_select_v3` に 3 を返す |
| `claude_gen_choice_wrapper_v3.py` | DAT 作業用 | `hk_ui_select_v3`（件数 1..K の choice 分岐と status の計算）と使い方の例 `hk_ui_example_v3` を CP932・CRLF で出す |
| `test_work_dat_ui_v3.c`、`build_dat_ui_v3_test.ps1` | このフォルダ | 合成テスト（MSVC 配置の偽 std::map／vector／string を自プロセスに作り、ReadProcessMemory で読む。テスト用ウィンドウでパネルも試す） |

検証（Wine 9.0、Zig 0.14.1、`-Wall -Wextra -Werror`、-O0／-O1／-O2／-Os）: 74/74 PASS。内容は、3×2 の正常系、49×4、0 列、照合の失敗 7 種、拒否 13 種（50 件、件数の不一致、ラベルの欠落、ID の重複、変数名の重複、出力用変数名、要素数の不足、列なしの値、`&`、5 列、循環、件数の偽装、レコードの重複）、段階 3 種、失敗時に出力が変わらないこと、パネルの並べ替え・検索・決定・二重発火の防止・Esc・行なしの決定・親の破棄・不正な入力・CP932 変換。生成器は K=49 で 50 ラベル、全行 CRLF、括弧の対応を確認。
作成中に見つけて直した問題: ラベル用の一時領域の NUL より後ろを初期化しておらず、2 回の読み取りが -O2 でたまに一致しなかった（-O0 では出なかった）。

### 本体への組み込み手順（Codex 向け、runtime は Work の所有なので Claude は変更していません）
1. `dat_ui_selector_plugin.c` の observe で `wdul_profile()==3` のとき、`wduc_resolve` → `wdu3_capture` → `wdu3_phase_ready` の順に呼ぶ。この経路では、v1/v2 の `WDUI_Session`（最大 4 件）を使わない。v3 用の小さな状態（serial、`dul_open_epoch` の generation、`dul_lifetime_epoch`、snapshot のコピー）を持つ。
2. tick で原作 choice が開いた（open epoch が進んだ）ら、既存の surface を作り、`wdug_create(surface, &input, cb, user)` を呼ぶ。名前・見出しは `wdug_from_cp932` で変換する。
3. コールバックで `WDUG_CANCEL` が来たら、surface だけを閉じる（何も書かない）。行番号が来たら、既存の `selector_fresh` と同じ順に確認する: UI スレッド、`probe_state`、`selector_lifetime_proven`、`wdu3_capture` で取り直して memcmp、`selector_owned_close` を確認、`wdu3_bind(base,&snap,(uint32_t)&dul_close_gate,...)`、もう一度 `selector_owned_close`、両方の epoch。その後 `wdu3_commit_plan` → index を書く → backend を書く → 寿命ゲート経由で原作の close を 1 回。部分的に失敗したら、v1/v2 と同じく使い切りにして再試行しない。
4. ACTUAL: `hk_ui_example_v3` をテスト用シナリオから呼び、ログで (a) plugin なしのとき原作 choice に AKYS／KMR／TNOK が出るか（`&@hk_ui_labelN&` の展開）、(b) plugin で決定すると `hk_ui_index`＝行、`backend`＝1、`status`＝1 になるか、(c) キャンセルで原作 choice が待つか、を確認する。(a) が失敗した場合は、`wdu3_native_label()` と生成器のラベルの形だけを直す。

## 7. 第6弾（2026-10-28）: v3 の runtime（本体への組み込み）と結合テスト
§6 の「本体への組み込み手順 1〜3」を Claude が書きました。根拠は FINDINGS §89。

| ファイル | 置き場所 | 内容 |
|---|---|---|
| `dat_ui_v3_runtime.h` | `data/recruit_sort_v4/core/` | v3 の状態遷移。observe ではコピーと検証だけを行い、UI には触れない。tick では baseline+1 の開いた choice に対してだけ、取り直し＋所有 close との照合が通ったら有効化する。決定時はすべてを確認し直し、使い切りにしてから index と backend を書き、寿命ゲート経由の close を 1 回呼ぶ。キャンセルは overlay だけを閉じる。surface と serial は v1/v2 と別 |
| `dat_ui_selector_runtime_v3.diff` | `core/dat_ui_selector_runtime.h`（SHA256 e5b6b7cf…、CRLF のまま） | 前方宣言 1 行。observe ですべての入口が v3 を置き換え、v3 は専用の経路へ進む（2 行）。tick の最後で `selector_v3_tick()` を呼ぶ。最後に `#include "dat_ui_v3_runtime.h"` |
| `test_dat_ui_v3_runtime.c` | `core/` | 実際の `dat_ui_selector_plugin.c`（配線済み）を、偽の image・変数マップ・ChoiceWnd・`routine(hk_ui_select_v3)` の AST・所有 close スロット・close の stub の上で動かす結合テスト |
| `build_dat_ui_v3_runtime_test.ps1` | `core/` | 上の結合テストを -O0／-O2 で実行し、配線済みの DLL をビルドする（`-AutoArm` で自動 arm 版） |
| `work_dat_ui_v3.h`、`work_dat_ui_grid.h`、`test_work_dat_ui_v3.c`（§6 の版から更新） | `src/`、このフォルダ | レビュー指摘の修正（§89.3）。作成時の `SetFocus` を削除（owned popup をアクティブにして前面を奪うため。Work の「前面を保つ」方針に合わせた） |

検証（Wine 9.0、Zig 0.14.1、`-Wall -Wextra -Werror`）:
| 項目 | 結果 |
|---|---|
| `test_dat_ui_v3_runtime.c`（-O0／-O2、自動 arm パッチなし・あり） | 55/55 PASS。決定（3×2、49×4 の並べ替え後、ダブルクリック）、キャンセル、baseline+2 の拒否、寿命の変化、表示から決定までの間の値の変更、原作ラベル・件数の不一致、v1 による置き換え、v3 同士の置き換えと古い callback、backend の書き込み失敗（使い切り・close なし）、段階の不一致、外からの surface close、loading フラグ、寿命が未証明、v1/v2 の後片付けが pending フラグを消さないこと、反応しなくなったパネルの回収 |
| `test_work_dat_ui_v3.c`（-O0／-O1／-O2／-Os） | 85/85 PASS（前回の 74 項目＋レビュー指摘の回帰テスト 11 項目） |
| ミューテーション（runtime の確認を 1 つずつ外す 10 種） | 7 種はテストで検出。残る 3 種（tick の opening／lifetime の確認、キャンセル分岐）は、確定直前の再確認と書き込み計画の確認が同じ条件を持つため、外しても書き込みは起きない |
| Work の既存テスト（配線後） | build スクリプト内の fixture、native（-O0／-O2）、literal、snapshot、dispatch、request、session、choice、composed はすべて PASS。DLL ビルド（既定・AUTO）も成功。`test_dat_ui_lifetime.c` だけは、Work の元のファイルでも Wine では line50 で失敗する（PAGE_NOACCESS のページを Wine の ReadProcessMemory が読めてしまうため。Windows 実機では Work の記録で PASS） |
| 独立レビュー（別の AI エージェント、作業経過を知らない状態、2 回） | 1 回目の 7 件、2 回目の 2 件をすべて修正し、2 回目で「新しい確定的な不具合なし」。内容は §89.3 |

組み込み手順（§6 の 1〜3 の代わり）: `dat_ui_v3_runtime.h` を core に、`work_dat_ui_v3.h` と `work_dat_ui_grid.h` を src に置き、`work_dat_ui_literal_v3.diff` と `dat_ui_selector_runtime_v3.diff` を当てる → core で `build_dat_ui_v3_runtime_test.ps1`（と `-AutoArm`）を実行 → Work の既存スイート（`build_dat_ui_selector.ps1 -Test` など）を実行し直す → §6 の手順 4（ACTUAL）。

## 8. 第7弾（2026-10-28）: DAT 汎用ユニット一覧 v4（実機確認済み）

場所: `v4/`（仕様は `v4/DAT_UI_V4_SPEC.md`。関数・引数・例・導入・無効化の手順もここにある）。

- ソースは `data/recruit_sort_v4` に反映済み。元のファイルは `v4/*.pre_claude_v4_20261028` に控えてある。
  - 新規: `src/work_dat_ui_v4.h`、`core/test_dat_ui_v4_runtime.c`
  - 変更: `src/work_dat_ui_grid.h`、`src/work_dat_ui_literal.h`、`core/dat_ui_v3_runtime.h`、`core/dat_ui_selector_runtime.h`、`core/dat_ui_selector_plugin.c`、`core/test_dat_ui_auto_arm_edge.c`
- `v4/test_work_dat_ui_v3.c` は v3 部品テストの更新版（3 回目のクリックで元の順に戻る確認を追加、87/87）。
- `v4/HakushinDatUiSelectorV4.dll` は実機確認に使ったビルド（AUTO、SHA 045045ac…）。改行だけを Work の形に揃えたあとの再ビルドとはハッシュが違う（中身は同じ）。
- DAT: `claude_gen_unit_table_v4.py` で `claude_dat_ui_v4_select.dat` を生成する。
  - `claude_dat_ui_v4_test.dat` は診断用のシナリオ。
  - `claude_swim_teacher_v4_proto.dat` は水練講師選択の試作。元の ev01_swim.dat は変更していない。
- Work にお願いしたいこと: Work の build スクリプトに v4 結合テストを加えること。全画面時の入力の重なりへの対策（DirectInput 側で抑止するなど）を検討すること。

## 9. 第8弾（2026-10-28）: キャラチップ・ステータスパネル・教育のキャラ選択

- ソース（`data/recruit_sort_v4` に反映済み。元のファイルは `v4/*.pre_claude_v5_20261028` に控えた）:
  - 新規: `core/dat_ui_v4_visuals.h`
  - 変更: `src/work_dat_ui_grid.h`（画像・選択の通知・DPI）、`core/dat_ui_v3_runtime.h`、`core/test_dat_ui_v4_runtime.c`
- `v4/HakushinDatUiSelectorV5.dll` は最終ビルド（AUTO、SHA b56aae9a…）。
- 教育: `v4/claude_lecture_v4.dat` と `v4/claude_patch_lecture_v4.py`（lecture.dat のコピーを作る）。元の lecture.dat は `v4/lecture.dat.pre_claude_v5_20261028`。
- 仕様: `v4/DAT_UI_V4_SPEC.md` の 9 章。
- Work にお願いしたいこと: build スクリプトに `dat_ui_v4_visuals.h` の依存を加えること（追加のライブラリは不要。ole32 は実行時に読み込む）。
