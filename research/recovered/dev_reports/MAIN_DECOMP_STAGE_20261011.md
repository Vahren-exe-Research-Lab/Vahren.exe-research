# 迫真戦記 ver0.67 — 逆コンパイル精密検証 4段階（2026-10-11）

本作業は Desktop Commander Local Compact 経由で既存資料を照合する、開発ラボ独立成果である。Ghidra/REA/原作EXEの新規プロセス起動は0。過去に安全拒否された対象を別経路で逆解析する行為はしない。

## 原則：3種類の「正しさ」を区別する

1. 保存EXEの命令列・.rdata bytes・静的分岐：高信頼の一次証拠。ただし実ゲーム到達・他関数副作用は別問題。
2. Ghidraの疑似C：変数や型を推測した読み物。自動で「OK」となっても演算、呼出引数、戻り値の欠落や誤命名があり得る。
3. 我々の再実装・テスト：1の局所契約を合成入力で試験。原作旧EXEと同seed・同fixtureで実測比較したものではない限り strict MATCH と呼ばない。

今回参照したEXE隔離コピーの既存SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。Ghidra一式ZIPは dev_lab/recovered_source/peer_script01_ghidra_named_decomp_20261011.zip（既存、SHA256 c167dc8b09e8cae6abaa14e23bac94e675585ae432595a1608fdbc1cc8249b9a）。原本は変更せず。

## 段階1：攻撃能力の元式 0x550D80

- 保存一次命令 exe/T012_DAMAGE_CORE_DUMP.txt 0x550DC8..0x550E63：mode3/4/5は FLD QWORD [0x63B0B0] → FSUB skill+0x288 → FIMUL far stat → FILD near stat → FMUL ratio → FADDP → FMUL scale → FADD 0.5 → JMP 0x5D1B80。
- 保存EXEのRDATA 0x63B0B0 はバイト 00 00 00 00 00 00 00 40、doubleの 2.0。よって式は ((near*R)+(far*(2-R)))*S+0.5。mode3 near=Unit+98/far=+A0、mode4 near=+98/far=+AC、mode5 near=+A0/far=+AC。
- 既存 typed_damage_fragments.py は 1-R という誤った仮定で記述されており、その既存単体試験だけでは誤りを発見できなかった。Ghidra FUN_00550D80.c もFPU演算を落としているため、疑似Cだけからは検知困難。
- dev_lab/src/hakushin_compat/main_decomp_attack_expression.py で2-Rを独立モデル化。旧モデルとの差分を確実に検出するテスト13/13 PASS。既存別担当・共用コードには手を入れていない。
- FLOATの局所演算丸め・runtime x87 PC設定・0x5D1B80変換・旧EXE可視結果はVERIFY。Fractionはbinary64値の数学的な計算式であってx87実機エミュレーターではない。

## 段階2：通常状態異常処理 0x578B70

- 保存REA assembly: rea_lab/decomp_task/runs/20261009T211647219Z/578B70_procedure_assembly.json（893 bytes、66 basic blocks）。Ghidra全体疑似Cも再確認。
- ガード 0x578B7A Unit+0x1867C!=0、0x578B8C Unit+0x8D!=0なら即終了。
- ECXへキー文字列を設定し0x40B200の文字列比較により通常状態7枝を選ぶ。PE静的文字列: 0x627DE4 poi / 0x627DE8 para / 0x627DF0 sil / 0x627DF4 conf / 0x627DFC ill / 0x627E00 stone / 0x627E08 fear。
- 書込先はUnit+BC/C0/C4/C8/CC/D0/D4。処理はsigned32 old − EAX（呼出時EBXへ退避）→ global[0x65BD4C]でsigned下限clamp→書込。
- 通常キーの書込後、Unit+0x8C!=0なら0x578E28で追加描画ルートを飛ばす。ゼロなら全7状態を順次見て負値の場合に0x4DFD80へ要求。呼出indexはキー順に (5,1,3,2,4,0,6)。最初の未解析calleeから先を実行済みとは言えない。
- special key suck/magsuck/drain/death は上記とは別。特にHP/MP/リンク先の+0x16Cや乱数・死亡virtualを扱う。Ghidraは引数とレジスタ意味の復元が不十分なため、通常7状態と共通の数値変更ルーチンにはしない。
- dev_lab/src/hakushin_compat/main_decomp_status_gauge_subset.py に、7通常キーだけのsigned32 writeと最初の未知0x4DFD80境界停止を実装。15/15合成専用テストPASS。native画面エフェクトは未実装。

## 段階3：浮動小数点→整数 0x5D1B80

- 保存REA 0x5D1B80..0x5D1B9Bは global[0xB14A40]判定後、非0の場合 FSTP QWORD → CVTTSD2SI EAX → RET。これはsigned int32の結果。NaN/範囲外は**MXCSRのinvalid-operation例外がmaskされている場合のみ**0x80000000（indefinite）を返し、非maskなら例外の可能性がある。原作runtimeのMXCSR状態はVERIFY。
- 全体Ghidraの _ftol2_sse 疑似Cは ulonglong 型で出力されるが、native SSE側はEAXのみ。疑似Cの64-bitシグネチャをそのまま新エンジンの関数ABIと決めない。
- dev_lab/src/hakushin_compat/main_decomp_ftol_sse_subset.py で「FSTPでbinary64が既に確定した後のSSE経路」のみ実装、12/12試験PASS。x87非SSE分岐0x5D1BB6以降、FSTP時の丸めモード、runtime effective FPU precisionは別VERIFY。
- 既存モデルがNaN/overflowで例外停止するのは安全側の未実装契約であってnativeの例外処理そのものではない。差分は将来の所有境界を守る統合時に判断する。

## 段階4：全疑似Cソースの網羅・危険箇所点検

- dev_lab/src/hakushin_compat/main_decomp_source_inventory.py が保存済ZIP・index.tsv・従来39件manifestを照合。報告 reports/MAIN_DECOMP_BUNDLE_INVENTORY_20261011.json。
- INDEX 10,257件のGhidra statusはすべてOK。C擬似コードの宣言マーカー10,257件、重複0・欠落0・余分0。従来39重点関数も全て含む。専用5/5試験PASS。
- 名前が FUN_XXXXXXXX のままの関数は2,896件。他に7,361件の非FUN_名があるが、CRTやMSVC/Ghidra自動名を含み、作者が命名した証拠や処理意味の検証済み割合ではない。
- 0x45E1E0 はindex上 Save_GlobalEnvelope だが、保存した0x45E1E0 nativeは通常の .sav loader本体である。Claudeが付けた名称は誤解を招くため「normal-save reader」として管理し、global.sav専用と取り違えない。
- 脆弱候補: 0x550D80（FPU計算消失）、0x5D1B80（疑似C戻り値型）、0x578B70（キー比較の暗黙レジスタ/副作用）、0x576F10（counter＋unknown call）、0x45E1E0／0x460000（通常セーブの群読込/書込）、0x4321B0／0x4338D0（イベントVM stack）。
- 「Ghidra OK 10,257」と「正確なsource復元10,257」は同義ではない。原作者C++をビルドし直せる状態ではない。

## テスト・安全・統合方針

- 新規試験合計45/45 PASS: 攻撃式13、状態異常15、SSE変換12、全ソース台帳5。いずれも既存の保存静的証拠に基づく部分契約の合成試験で、原作ゲームUIの実測goldenではない。
- 研究正本の直近checkpoint82は正式185 ID、34 TaskはDONE9/IN_PROGRESS21/VERIFY4。DEV側の本解析ではMASTER・A〜E owner・REA正本を編集していない。実際のゲーム新エンジン strict gameplay MATCHは0。
- 別AI PEER_SCRIPT01のファイルやGhidraの保存ZIPはread-only。新規フォルダ/worktreeを増設せずdev_lab既存src/tests/docs/reportsだけを使用。原本ZIP/EXE/ゲームアセット/セーブ・Git・Remote・automation・設定の改変0。安全拒否を他ツールで迂回0。

## 次回は段階5以降

1. 0x578B70のsuck/magsuck/drain/death特殊枝、0x4DFD80/0x4E13F0の効果範囲を保存済みnativeで別々に精密化する。7通常状態の既存15件を壊さない。
2. 0x576F10のcounter+0x185F8と0x4DFBB0（Ghidra推定）を既存保存assemblerとの矛盾有無でチェックし、callee作用が不明なら停止点を設ける。
3. Unit/Skill/SpotとEngineの型付けを、構造体のオフセット・reader/writer・仮想関数の3系統で照合する。Claudeのnamesだけで固有フィールドを確定しない。
4. 旧 .sav の新実物3件と通常loader0x45E1E0／writer0x460000を相互比較し、numeric group後のUnit/Spot/Power境界を特定する。gameplay実測・外部ptrが無い部分はVERIFY。
5. 旧実機から可視Goldenを合法採取できる場合に限り、SSE/x87条件・PC設定・戦闘HP/状態をnew engineと厳格比較。これが完了するまで完成・完全互換とは呼ばない。


## 段階5〜9（2026-10-11続行）：特殊status・保存形式・初期ロードの進捗

- 保存済みREA 0x578B70特殊効果suck/magsuck/drain/deathの局所処理を新Pythonへ分離、31/31合成テストPASS。0x576F10前段counterを9/9 PASS。unknown native effectsは残している。
- 旧セーブnormal numericの終端は ------ の類推ではなく厳密な11byteの ----------＋NUL。過去の空文字終端とnumeric record1960/2593集計は誤りと実セーブで確認。旧レポートをSUPERSEDED、新たなrecord数1958/2591で全saveを再構築。
- 原作3セーブのnumeric/Unit/Spot/Power/Diplomacy/WorldGraphを保存済Ghidra/native writerと比較、全レコード型を独立実装し、完全再シリアライズ＋元鍵で全暗号化バイト一致。新コードnormal_save_complete_wire.py、詳細日本語報告 docs/DEVLAB_NORMAL_SAVE_WIRE_COMPLETE_20261011.md参照。
- WorldGraph元171経路の全端点が保存Spot138へ解決。新world_graph_reference_index.pyとreports/WORLD_GRAPH_REFERENCE_CROSSWALK_20261011.jsonで研究用仮グラフを整理。方向の実移動意味はVERIFY。
- native reader 0x45E1E0の自動命名Save_GlobalEnvelopeは通常save loaderとしては紛らわしい。保存済Ghidra疑似CにあるUnit/Power/Spot storage準備→numeric/Unit/Spot/Power/Diplomacy/worldの読込順を確認し、normal_save_runtime_registry.pyでID名をキーとした安全なnew-engine側レジストリを作成、8/8専用試験PASS。ポインタ構築と旧game side effectsは未実装。
- save1→save2 native byte record差はUnit追加1412・削除4・変更1362、Spot変更40、Power変更29、numeric(key,aux)追加633・変更67。報告はreports/NATIVE_SAVE_TURN1_TO_TURN2_DIFF_20261011.json。
- 最新DEV側handoffはdocs/PROJECT_HANDOFF_MASTER_20261011.md §17/§18であり本書の旧「次回は段階5以降」を更新する。今回全run_checks.ps1は新規実行しておらず、別AIの遅いsurveyと本修正を混同しない。
- 次は旧normal readerのconstruction・pointer rebinding・scene setupと、合法原作UI Goldenの比較。完全ゲーム互換の完成報告にはまだ達していない。

