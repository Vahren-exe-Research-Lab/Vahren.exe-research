# 迫真戦記 ver0.67 — T014ロード後ID参照と新エンジン用場面初期化（2026-10-11）

## 立場・所有権・安全

- 本資料はdev_lab制作専用の増分。研究正本MASTER_LEDGER checkpoint83（公式190 ID、研究DONE9/34）と5レーン規約を最初にread-only照合。A/T014・E/T018の研究正本、REA、他AI成果、元ゲームEXE・元セーブは変更しない。Local Compactのみ利用。Remote/Git/公開/自動化の変更なし。
- 保存済Ghidra 10,257関数ZIPと元writer命令、3件の原作実セーブを照合。旧EXEの新実行・Ghidra/REA新逆解析は0。過去の安全拒否操作を迂回しない。
- 本文の「参照復元」は原セーブ中に記録された文字列IDが原セーブ内の実オブジェクトIDと一致することを確認する意味。C++ native pointer、ロード後のメモリ値、可視UI、ゲーム挙動の再現ではない。原作ゲームplayback Golden0、新エンジンstrict gameplay MATCH0維持。

## 保存データから直接確認した参照

| 保存フィールド | save1 | save2/auto | 検証 |
|---|---:|---:|---|
| Unit全数 | 7355 | 8763 | ID一意 |
| SpotのUnit名格納欄 | 7347 | 8756 | すべて既存Unitと一致、同じUnit重複なし |
| Spotに登録されないUnit | 8 | 7 | 保存から削除しない |
| Unit+0x84の別Spot名 | 8 | 5 | すべて既存Spot名と一致 |
| Spotに登録されずUnit+0x84も空 | 0 | 2 | cmd500_matsuei+tmp／cmd_a006+tmp |
| Unit第1ベクタ内のUnit名 | 6069 | 7285 | すべて既存Unitと一致、参照先重複なし |
| Power+0x68欄のSpot名 | 40 | 40 | すべて既存Spot、Power間で重複なし |
| Power+0x24欄のUnit名 | 29 | 29 | すべて既存Unit |

- Unit+0x1Cにはテンプレート名などUnit IDと一致しない文字列が大量にある。Unit+0x38/0x54、ベクタ1（save1側49473参照）はリソース/技能名の可能性があり、無理にUnit pointerとして解決しない。friend文字列もUnit IDと一般名が混在するため一律の強制照合はしない。
- 意味ラベルはVERIFY：SpotのUnit名参照は拠点構成を示す有力候補だが、現実にユニットが画面でそのSpotにいるか、Power+0x68が排他的領地か、Power+0x24が指揮官かは旧engine nativeと可視Goldenを要する。実験コードではneutralなoffset/serial field名のまま保持。

## Ghidraから分かったロードの静的順序と重要な分岐

- normal-save reader入口 0x45E1E0（Ghidra自動名 Save_GlobalEnvelope は通常 .sav reader実体を表すには不正確）。
- 保存C疑似コードは 0x582AA0 Unit storage準備→0x5971A0 Power準備→0x590560 Spot準備→0x470550 preamble→numeric→Unit 0x58E870→Spot 0x598980→Power 0x5964C0→Diplomacy 0x471AF0(1)→World 0x435550(1)の呼出順。各calleeのconstructor/lookup副作用やバージョン分岐は要native追跡。
- 0x435550には2経路あり、param_2==0側にはSpotElm operator_new(0x36c)、SpotPath/Escape operator_new(0x240) とmap挿入が存在する。一方、通常セーブロードの呼出は param_2=1。mode1側はdefault/既存サブタイプとvf23を介する。したがって通常ロード時に0x36C/0x240のheap-new処理を必ず再現すると仮定してはならない。
- 全体Ghidra疑似Cはnativeと関数ABI/型/制御分岐が異なる場合がある。上記は保存静的出力と元セーブの相互整合であり、実機のpointer値を証明したものではない。

## 開発ラボに追加したコードと証拠

- src/hakushin_compat/native_saved_reference_graph.py：Spot→Unit、Unit→Spot、Power→Spot、Power→Unit+0x24、Unit第1ベクタ→Unit、Unit+0x84→Spotの保存ID crosswalkをimmutable mappingで作成。未知参照/Spot二重登録はfail closed。
- src/hakushin_compat/native_saved_reference_audit.py → reports/ACTUAL_SAVE_REFERENCE_GRAPH_20261011.json：上表の全件検証、save1/auto/save2のSHA gate、未登録Unitおよびoffsetの訂正証拠を記録（実原sav bytesは同梱しない）。
- src/hakushin_compat/native_saved_loader_bootstrap.py：原readerに対応する静的11段階の読込計画、各保存オブジェクトのIDベース世界状態、個別Unit/Spot/Power/numeric検索API。original native constructor/pointer/renderer/VMの実行は全てfalse。
- src/hakushin_compat/native_saved_scene_transition.py：save1→save2のSpot名登録変更をsource IDで差分化。reports/NATIVE_SAVED_SCENE_RELATION_DELTA_20261011.json を別auditで書込。
- src/hakushin_compat/native_saved_scene_inspector.py：新エンジン用読取専用CLIを追加。セーブファイルからsummary/unit/spot/power/route/compareの保存ID情報をJSONで表示。元savは書き換えず、既存保存コピーでCLI smoke PASS。

## ターン1からターン2への保存登録変化

- 共有UnitのうちSpot記録の変化170、同Spot記録の共通Unit7173、新しいSpot記録名1413、旧Spot記録から消失4、Spotレコード変更40。
- Power+0x68のSpot ID40、およびPower+0x24のUnit ID29は両保存で一件も変更なし。
- 共通Unitの第1ベクタ記録が変更されたIDは3。graph171 pathの保存データは両保存で同一。
- a002+0〜a002+6の7 Unitは保存上sp49→sp50に変わったが、移動コマンド/シナリオイベント/再配備の原因は不明であり「旧ゲームでの移動が観測された」とは扱わない。
- これらはsrc/hakushin_compat/native_saved_scene_transition_audit.pyがreports/NATIVE_SAVED_SCENE_RELATION_DELTA_20261011.jsonへ専用出力した。未証明のゲーム因果を記載しない。

## 実装と限定テスト（全件正常終了確認）

| 追加コード/試験ファイル | 実行結果 |
|---|---:|
| test_native_saved_reference_graph.py | 12/12 PASS |
| test_native_saved_loader_bootstrap.py | 8/8 PASS |
| test_native_saved_scene_transition.py | 7/7 PASS |
| test_native_saved_scene_inspector.py | 10/10 PASS |
| 新CLIのcapture save1 summary起動 | EXIT 0 |
| 2つの新JSONレポート作成 | EXIT 0、source SHAチェック通過 |

- 追加専用合計37/37 PASS。上記の個別実行を確認。テスト内でも私用captured .savをSHA256 gateし、変化時に失敗する。
- 旧のtest_native_save*/test_normal_save*/test_real_save*群の再実行は今回省略。プロジェクト全体run_checks.ps1のPASSは**今回確認していない**。他AIのPEER script surveyに時間がかかる問題と本実装の結果を混同しない。
- reports/ACTUAL_SAVE_REFERENCE_GRAPH_20261011.json と reports/NATIVE_SAVED_SCENE_RELATION_DELTA_20261011.json はjson meta/ゲームIDのみで元sav本体を含まない。後者には170件の登録先変化一覧、40拠点の増減概要を保存。

## CLIのPC上の安全な使い方

開発ラボのルートから実行する。環境変数の設定は現在のPowerShellセッションだけに影響する。

    $env:PYTHONPATH = ".\src"
    $env:PYTHONDONTWRITEBYTECODE = "1"
    python -m hakushin_compat.native_saved_scene_inspector --save ".\_work\target_actual_20261011_save1.sav" --kind summary
    python -m hakushin_compat.native_saved_scene_inspector --save ".\_work\target_actual_20261011_save1.sav" --kind spot --name sp1 --limit 10
    python -m hakushin_compat.native_saved_scene_inspector --save ".\_work\target_actual_20261011_save1.sav" --kind compare --other-save ".\_work\target_actual_20261011_save2.sav" --limit 10

- kind は summary/unit/spot/power/route/compare。名称照合は保存IDに限る。表示されたraw bytes値やdirectionの意味を勝手に解釈しない。存在しないIDや壊れた原savはfail closed。
- CLIはsourceをread_bytesするだけで、ゲームフォルダには書き込まない。原本.exeを起動せず、GUI操作を発生させない。

## 次の独立タスクとブロッカー

1. DEVLAB-007/T014：0x58E870、0x598980、0x5964C0、0x471AF0、0x435550 mode1内部の名前→pointer変換・constructor・cleanup差分を保存済みnativeとGhidraで監査。原C++のpointer/owner意味は実機までVERIFY。A ownerの研究資料を直接編集しない。
2. DEVLAB-008/T018：世界マップの実描画・入力状態へSpot138＋Path171＋Unit一覧を安全に接続できる新エンジンstate API。描画座標、terrain、fog、通行可否・方向は別のT007/T015/T025根拠が必要。
3. DEVLAB-009/T010/T018：ターン処理・イベントVM・ロード後再開の最初のgoldenを設計。旧EXEゲーム挙動の実測0なので、保存データだけで対戦AI・地形・天候・土砂崩れが実装できたとは言えない。
4. A/T014とE/T018へDEV handoff共有のみ。公式研究台帳のcheckpoint、READY/DONE、原作golden数を制作チャットが勝手に変更しない。


## 2026-10-11 引継ぎ再監査：保存済みnativeで確認した経路名解決候補

- Local Compactで研究MASTER checkpoint83（190 ID、DONE9/34）、レーン所有規約、既存DEV成果をread-only照合。dev_lab Git HEAD `b49c678`。並行作業の `docs/BATTLE_DEFINITION_STAGE_20261011.md` は他担当の未追跡ファイルとして検出したため非接触。Git stage/commit/pushなし。
- `exe/T014_NORMAL_LOAD_PROBE.txt` VA0x45E536..0x45E54C：通常ロードはDiplomacy `0x471AF0` とWorld graph `0x435550` の直前にそれぞれ `push 1` を行う（Worldは追加引数あり）。従前のgraph mode1判定をnative命令で再確認した。
- `exe/T014_SPOT_PATH_VFUNCS.txt` VA0x5B0400..0x5B0447：別のpath系routineは `[ebp+0x10]` byteを検査し、0なら `0x5B04E7` へ、非0なら `0x4705F0/0x4707D0/0x470700` 等を読む別経路へ進む。**このbyteと0x435550のmode1引数の対応は現時点で未証明**。
- 同資料VA0x5B04E7..0x5B0538はレコードから文字列などを読み、0x5B0544..0x5B057Cは保存文字列offset `+0x1E8` と `+0x204` を `0x49E490` に渡して各結果を取得。0x5B057E..0x5B0584は両結果非zeroを検査し、成功候補では0x5B05AF..0x5B05C8から `0x5AFB30` 呼出、失敗候補では0x5B05D2..0x5B05EDのエラー経路へ進む。文字列→内部参照解決の**有力な保存静的証拠**だが、calleeの対象型とゲーム内効力はVERIFY。
- `dev_lab/recovered_source/ghidra_c_pseudocode/FUN_0045E1E0.c` と `FUN_0058E870.c` は既存保存pseudoとしてread-only照合。新規逆コンパイル起動なし。Sourceに出るUnit readerの文字列フィールドと経路のpointer候補を同一意味へ無理にまとめない。
- Windows Localで `python -m unittest discover -s tests -p 'test_native_saved_*.py' -q` を実行（PYTHONPATH=dev_lab/src、PYTHONDONTWRITEBYTECODE=1）。**37/37 PASS、81.088秒、exit 0**。これは元セーブのID投影の試験で、旧EXEロード成功・pointer再束縛・描画・ゲーム進行のPASSではない。全回帰run_checksは今回は未実施。
- 実装境界：`native_saved_loader_bootstrap.py` の `native_memory_pointer_rebinding_done=False` を維持。`0x49E490` のcallee/callerと`0x435550` mode1からpath readerの引数伝搬が証明されるまで、実エンジンにnative pointer解決済みとマークしない。原作playback golden0、新strict MATCH0、DONE9/34、研究190 IDを変更しない。
- 次のDEVLAB-007は0x435550 mode1→subtype dispatch→0x5B0400引数の接続と、0x49E490/0x5AFB30の保存コードを限定追跡。A/T014所有研究資料とE/MASTERへの直接編集は禁止。DEVLAB-008の描画/入力stateは方向・fog・passability未確定のため、保存ID読取専用レイヤーから段階接続する。
