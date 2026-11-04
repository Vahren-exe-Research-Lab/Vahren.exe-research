# 迫真戦記 v0.67 — 戦闘・キャラクター・ストーリーDAT無改変再利用のためのロード順ネイティブ調査

日時：2026-10-11。**所有：DEV新エンジン接続境界のみ**、担当外の研究正本には書込なし。WBSの `BF-19` を参照。原本・Ghidra保存ZIP・A～E各レーン・Claude Code所有ファイルはread-only。

## 方針・厳密な完了基準

- ユーザー要求：旧EXEの内部C++/DirectX/音声再生方式を複製する必要なし。**原作の見える画面、操作結果、戦闘スキル、CPU判断とゲームルールは高精度に合わせる。**
- 原作 `a_default/script/**/*.dat`（戦闘/キャラクター/ストーリー/内政）は**原文のまま保持**し、書き換えずに新エンジンへ読み込む。旧scriptの構文・命令APIを互換層で解釈し、未知命令の消費・実行順を指定された意味で扱う。
- レンダラー/UI、古い音声API、原EXE ABIは互換scriptの外側のサービスに差し替える。イベント内 `msg/dialog/cutin` 等はscriptを編集せず、画面効果要求としてpresentation adapterへ渡す。
- 新しい拡張を使うときも既存本文の一括改変やスクリプトの意味が勝手に変わるグローバル改変は行わず、拡張名前空間/モードを分離する。

## 今回の**新規**保存済みネイティブ逆解析（通常DATのファイル列挙順、構文解析は再調査しない）

対象：同梱 `Vahren.exe` の既存確認済みSHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、保存Ghidra ZIP `dev_lab/recovered_source/peer_script01_ghidra_named_decomp_20261011.zip` 内 `decomp_0050xxxx.c` と `decomp_0051xxxx.c`。**新しいEXE実行/Ghidra/REA/逆アセンブルprocess起動なし。保存済み疑似Cの新しい局所検討のみ。**

1. **`0x50BF60`（scriptフォルダDAT候補収集）：** `FUN_00406CF0("*.dat")` → Win32 `FindFirstFileA` → `dwFileAttributes & 0x10` のディレクトリを除外し、`cFileName` を要素0x1C幅のvectorへ登録、`FindNextFileA` で継続、`FindClose`。この部分のファイル名前要素を既存 `0x429A00` で追加している。
2. **明示ソートあり：** 同関数の後段で `FUN_005116B0(begin, end, (end-begin)/0x1c, &LAB_0050BF00)` を呼び、続けて `FUN_00479B50` に渡す。保存 `FUN_005116B0` 疑似Cには0x21件未満時の局所sort helper、分割後の再帰処理、残深度0時の別helperなどがあり、**ソート処理と整合**。少なくともWin32の列挙順をそのまま最終DAT順とみなすのは不適切。
3. **通常ロードの上位 `0x50C9A0`：** `script/` と `script2/` を含む2系統の分岐があり、`0x50BF60` のファイルlistを構築して `0x50B220` を呼ぶ。**`0x50B220` 一ファイルの構文・命令解釈はClaude Codeが詳細に解析済みなので再実装/再解析しない。** `script2` の優先・merge条件はこの限られた確認から確定しない。
4. **誤った入口を除外：** 別関数 `0x557240` は `debug_paper.txt` と `encode` を扱う `0x558000` から条件付きで呼ばれ、`CreateFileA` read→magic `0x04030201` 判定→未暗号化時変換→`WriteFile`。従来 `VAHREN701_DAT_FORMAT.md` にあるdebug encode処理の範囲。これをゲーム本体の通常script-loaderと混同しない。**この既知部分の再解析を中止。**
5. **現存の原作データ:** 調査用原文スナップショット `data/source_snapshot/hakushin067_core/a_default` には `script/` があり、トップ直下の `script2/` は無い。静的な元データの現在形であり、原作が `script2` をどう扱うかの一般規則とは異なる。

## 既存成果への差分と検証を増やさない理由

- 既存 `dev_lab/src/hakushin_compat/script_source.py` は **CP932原文→元バイト完全roundtrip** 可能。旧 `script_source_audit.py` は `sorted(SCRIPTS.rglob("*.dat"))` で既存590ファイルの字句監査を行う。ただしこれは**新エンジンの実効native-load-orderが一致した証拠ではない**。
- Claudeの `PEER_SCRIPT01_FINDINGS_20261011.md` §15 は `0x50B220` のLexer/構文/keyword/control-flow を再構成済み。A担当はT005/T006/T014の構文・変数・イベントVM、B担当は戦闘CPU/技能/ダメージ、D担当は描画・入力・RTS。**その作業をこのチャットが再実行したり上書きしない**。
- 本日の新規差分は **DAT候補のネイティブ列挙→ソート→個別パーサへの接続**。疑似Cでの関数・呼出順を確認した静的成果であり、元ゲームUIの動的trace/旧新のstrict matchは **0**。
- `LAB_0050BF00` の比較述語（ASCII/大文字小文字/locale/パス序列）、recursive/下層folder順、2分岐 `script/script2` の正確な優先・混合規則、native実機での全sourceロード順は**未確定**。根拠なしに `Path.rglob` やWin32列挙順、名前の辞書順を正解と固定しない。

## 重複作業防止・後続担当への具体的引継ぎ

- **DEV担当（この成果）:** 将来の `BF-19`「ScriptFileProvider/LoadOrder」契約に `relative_path, raw_sha256, selected_root, native_rank, source_bytes` を用意する。未知のnative rankはnullで持ち、確証が取れるまでは原本文編集をしない。実技術選定やコード全実装をこの時点で開始しない。
- **A/Claude:** 同じparser全590件を再解析しない。必要時のみ `LAB_0050BF00` comparator、`0x50C9A0` のbranchとfolder優先、`0x50BF60` 下位ディレクトリ順を**限定照会**。担当主力タスクを止めて全関数再解析する必要なし。成果は重複IDを避け担当handoffへ残す。
- **B/D:** script loaderを再解析せず、既存のskill/native・視覚効果の担当を維持。戦闘スクリプトの命令効果が足りなければ`BF-19`→VM担当の不足として依頼する。
- **E/統合:** `MASTER_LEDGER.md` を他AIが直接追記しない。必要時に本書の保存済みVA事実をREADYで検討し、既存T005/T006と重複を検査。
- **トークン節約:** 普段は既存証拠を信用して続行。重複再検証は新しい矛盾・再現失敗・モジュール完成の重要ゲートに限定。全体のテスト再実行はせず局所試験/台帳整合だけでよい。作業中の別AIのファイルには書かない。
## 2026-10-11 増分: BF-19-A「無改変 DAT SourceFileProvider」完了

### 保存済み逆コンパイル結果の再解釈
- 根拠ZIPは既存 recovered_source/peer_script01_ghidra_named_decomp_20261011.zip の decomp_0050xxxx.c。今回も旧EXE、新規Ghidra/REA起動、再抽出は実施していない。
- 0x50C9A0の最初のFindFirstFileAは、戻りがINVALIDまたは最初の項目が非ディレクトリの場合、FUN_00416970(...,"script/") → FUN_0050BF60 → FUN_0050B220 のみを走る。
- もう一方の分岐はFUN_00416970(...,"script2/") → FUN_0050BF60 → FUN_0050B220 の処理後、DAT_008797d1=1 → FUN_00416970(...,"script/") → FUN_0050BF60 → FUN_0050B220 を走る。よって二root分岐ではscript2が先、scriptが後。ただし2回のparse間で同名宣言がどう上書き/無視されるかは不明。
- 最初のFUN_00416970の引数はGhidra疑似Cが脱落しており、初回FindFirstFileAの検査対象PATHをscript2/と断定しない。上記二経路のトリガーを「script2フォルダ存在」と決めつけない。
- 0x50BF60は現在のフォルダの*.dat候補を0x1cレコードへ集め、FUN_005116B0(begin,end,count,&LAB_0050BF00)ソート後FUN_00479B50に渡す。ディレクトリ候補は別のqueueで処理される。LAB_0050BF00比較内容、queue全体の探索順、Windows列挙による順序は未解明であり、英字辞書順をnative順と決めない。

### 独立実装と自動検証（この小タスクのみDONE）
- 新規 src/hakushin_compat/native_script_file_provider.py は source_branch=script_only と script2_then_script を明示指定し、原本上のscript/とscript2/のDATだけをread-onlyで取り込む。基準は実際のディレクトリではなく呼出側が選んだ分岐で、原EXE側条件の予言はしない。
- CandidateScriptFileはrelative_path / selected_root / source_bytes / raw_sha256 / native_rank(None)を保持。候補表示用の安定ソートをnative順位と混同しない。ネイティブ順位取得要求はNativeLoadOrderUnverifiedを発生させる。
- 参照パス脱出/シンボリックリンク/空のroot/過大入力/同名大小衝突等は保守的に拒否。既存script_source.py・Claudeのparser・battle GUIには接続せず、他AI作業領域を保護。
- 実豪華版a_default/scriptは590 DAT、14,591,845 bytes、直下19件。実a_default/script2は存在せず、二root分岐を実データで成立したかのようには扱わない。ファイル内容・mtimeに変更なし。
- 新規 tests/test_native_script_file_provider.py は10/10 PASS (exit0)：実原作総量/ファイル数、入出力bytes/sha、分岐順、rank不明の厳格拒否、欠落root/サイズ上限/immutable/原本不変更を検査。ゲーム動的golden PASS0／strict MATCH0は変化しない。

### 残件とタスク判定
- BF-19-A（独立FileProvider/読込元二分岐/原文hash保護）＝DONE。本文BF-19はまだPARTIAL：比較述語LAB_0050BF00、dir探索順、同名登録セマンティクスをnativeと実入力で検証し、初めて適切な読込ordinalを与える必要がある。
- A/T005・E/T018公式研究タスクやWBSのBF-19全体は自動DONEにしない。原作素材/owner/native ZIP/MASTER、Git stage/commit/push、Remote/自動化は今回変更なし。
