# symbols.tsv 全分野拡充 作業報告（2026-10-29）

作業ID: KB-SYMBOLS-EXPAND-20261029-01  
対象: `knowledge/symbols.tsv`（迫真戦記 ver0.67、0x400000基準 VA）  
状態: **完了 — 静的根拠の辞書登録、形式検査、事典再生成、Ghidra・x32dbg検索試験成功**  
原作での新規実機プレイ／デバッガ動作試験: **未実施**。静的確認はゲームでの実作用検証を意味しない。

## 1. 結果

| 分野 | 追加 | 静的確認 | 推定 | 実機確認 | テストのみ |
|---|---:|---:|---:|---:|---:|
| 戦闘：ユニット更新・簡易戦闘 | 18 | 17 | 1 | 0 | 0 |
| 戦闘：技能・ダメージ・回復・状態 | 32 | 27 | 5 | 0 | 0 |
| AI：目標探索・支援・操作 | 27 | 17 | 10 | 0 | 0 |
| 経験値・召喚・ユニット記録 | 30 | 28 | 2 | 0 | 0 |
| セーブ・永続変数 | 35 | 29 | 6 | 0 | 0 |
| イベント・式・乱数 | 34 | 29 | 5 | 0 | 0 |
| 戦略・場面・領地 | 16 | 13 | 3 | 0 | 0 |
| 画面・入力・音 | 47 | 34 | 13 | 0 | 0 |
| **合計** | **239** | **194** | **45** | **0** | **0** |

開始時の手書き辞書 **124件** → 現在 **363件**。既存124アドレス・行は全て残し、意味の誤りが明らかだった2件のみ更新した。

優先的に辞書化した要点:
- `0x48D6A0 Battle_ConstructScene`：通常戦闘 scene2 の構築、元ゲームへ正常復帰する `RET=0x48EA5A`
- `0x550E70 Damage_ComputeAttackDefense`：攻撃・防御・乱数・耐性
- `0x545CC0 Skill_DispatchUnitAbility`：技能種別1〜4の分岐
- `0x57B870 Ai_SearchTargetCadence`、`0x514D60 Ai_SelectNearestTarget`：探索タイミング・目標選択
- `0x54E7B0 Summon_SpawnFromSkill`、`0x577260 UnitData_FindSummonRecord`：召喚・記録
- `0x460000 Save_WriteFullState`、`0x427040 Save_EncodeAdditiveEnvelope`：.sav・global.savで共有する保存形式
- `0x5559B0 Window_HandleWin32Messages`、`0x4BE220 Audio_AdvancePlaylistOnEnd`：入力とBGM遷移

## 2. 根拠と確認方式

最初に `00_START_HERE.md` と `knowledge/README.md` を読んだ。既存 `knowledge/CATALOG.md` と `kb.py` を入口として、`data/T009〜T015`、`T024`、`T025`、`T031`、`T032` の各研究報告、`exp_research_20261021/EXP_*.md`、`rea_lab/headless_analysis/search_index/BATTLE_BRIDGE_RESEARCH_INDEX.md` とStage16等の一次保存証拠を参照した。

`knowledge/tools/_symbol_candidates_20261029.py` は、報告内のVAを統合 V9 `function_range` により関数先頭へ正規化し、元の124件を除外、見つかった資料行・出現頻度を分野別に列挙する**読取専用**の候補抽出器。`knowledge/tools/validate_symbol_expansion_20261029.py` は、タブ6列、VA・名前の重複、セクション、関数先頭、code の所属関数、関数の擬似コード存在、原本辞書SHAを事前検査してから、許可時のみ辞書をバックアップして原子的に更新する。新規逆解析禁止帯 `0x5710C0〜0x571500` は候補から除外した。

各新規 `func` は統合V9の関数先頭と一致し、各 `code` はV9内の所属関数に含まれることを検証した。V9の擬似コードは旧版Ghidraの既知の関数境界誤認を含み得るため、**疑似コードの存在だけでゲーム実作用を保証しない**。出典がその関数の途中の命令VAだけを載せている場合は、そのV9関数先頭へ正規化している。

コード/データの境界について1件だけ注意: `0x6385BC` は指定の便宜的な `0x639000` より手前だが、既存研究で確認された**Spot の仮想関数表**のため、実体に合わせて `kind=object` で登録した。禁止範囲や原作ファイルを編集する例外ではない。

## 3. 訂正した既存行

1. `0x879822`：旧 `g_titleEnabled`／「タイトル画面の入力有効」／テストのみ → 新 `g_WindowActiveForInput`／WndProc `WM_ACTIVATE` と GameMouse の非アクティブ抑止／静的確認。根拠 `T015§Win32/D3D window mode`。**旧名前を直接参照する外部ツールには読み替えが必要**。
2. `0x65BEEC`：旧「テストでは1024を入れる幅」／推定 → D3Dバックバッファ幅（高さ `0x65BEF0` と対）／静的確認。名前 `g_screenWidth` とVAは維持。根拠 `T015§Win32/D3D window mode`。

両件ともアドレス自体は変更せず、旧全124アドレスの集合を保持した。

## 4. 新旧研究の衝突と安全側の判断

- **戦闘scene構築 `0x48D6A0`**：Worldイベントとは区別する。最新の `BRIDGE Stage16§C` と `BATTLE_SCENE_BUILDER_EXTENDED_EPILOGUE_PE_20261021.json` により、旧Ghidraが認識した終端 `0x48EA38` は誤りで、実際の通常 `RET` は `0x48EA5A`。辞書の説明に訂正を明記。古いWorld-phase分岐 `0x48C880` の説明を scene2 builder に適用しない。
- **AI目標選択**：`0x514D60` の主候補 SimpleUnit と代替候補 SimpleStaticUnit の区別、Unit+0x1C0 の `stealth` を後発 `T013` の証拠に従って反映。候補ベクトル操作をスコアの本体として誤記しない。
- **技能分岐**：`0x547DB0` は missile + allfunc の別経路として後の `T012§21` を採用。
- **フェーズ乱数**：`0x48B4A0` は多用途の乱数reset本体とは断言しない（推定）。`0x48BF60` と `0x48BC70` はそれぞれ phase5/6 の経路であり、共通リセットを*呼ぶ側*として区別。
- **除外した候補 `0x5159F0`**：古い報告では比較処理に言及があるが、統合V9で関数先頭・所属関数が解決せず、今回の辞書に**登録していない**。無理な所属推定・確度引上げを避けた。

## 5. 推定45件の扱い

`推定` の典型例:
- `Ai_AdjustSearchTargetCoordinates`、`Ai_CheckOrientationGate`：座標補正や AL の厳密な意味が未確定。
- `Skill_FilterSupportCandidates`、`Skill_PrepareLargeCandidateSet`：フィルタ条件や4件境界での最終的な行動結果は未検証。
- `Save_ReadDiplomacyState`、`Save_WriteDiplomacyState`：世界側保存object +0x1EF4B4 は確認できても人間向け状態名は仮称。
- `Scene_RunRngResetBranch`、`Event_EvaluatePhasePredicate`：特定のコード経路はあるがシーン全体の実作用は未確定。
- `World_RefreshDerivedSkin`、`Audio_TestTrackTransitionGate`、`Input_ResolveBattleWorldPoint`：後段の詳細が未解明。

この45件は、未確認部分を埋めずに根拠で言える範囲だけ記述している。新規原作実機確認0件、合成テストだけで確定した項目0件。

## 6. 書込保護・SHA・検証結果

| チェック | 結果 |
|---|---|
| 変更前 `symbols.tsv` | UTC 2026-10-29 05:56:45.088097、SHA256 `8075FFA9DD1BAEED7489792ACE1217AD54D6DC201F8D15A7100BF9390434E686` |
| 変更前のバックアップ | `knowledge/tools/symbols_baseline_20261029.tsv`。変更前SHAと完全一致 |
| 更新後 `symbols.tsv` | SHA256 `6DE767D362CDAF354C30832E7CFAF82B17512661890C8F215FAF652CB627851F`、原子的更新後のreadback PASS |
| `python -B knowledge/tools/build_kb.py --check` | **入力 OK：symbols 363行、structs 40行** |
| `python -B knowledge/tools/build_kb.py` | **成功**。事典、Ghidra用TSV、x32dbgラベル・コメント、`kb.sqlite`、目録を再生成 |
| `python -B knowledge/kb.py find 戦闘` | **PASS**：`Battle_ConstructScene` 等の新規ラベルを取得 |
| `python -B knowledge/kb.py find 召喚` | **PASS**：`Summon_SpawnFromSkill` 等の新規ラベルを取得 |
| `python -B knowledge/kb.py find 支援` | **PASS**：支援候補の説明・確度を取得 |
| `python -B knowledge/kb.py addr 0x879822` | **PASS**：既存訂正 `g_WindowActiveForInput` を反映 |
| 出力の所在 | `knowledge/REF_ADDRESSES.md`、`knowledge/generated/ghidra/kb_symbols.tsv`、`knowledge/generated/x32dbg_labels.txt`、`knowledge/generated/x32dbg_comments.txt`、`knowledge/generated/kb.sqlite`、`knowledge/CATALOG.md` |

**禁止された原作EXE・DAT・MAP・ZIP・セーブへの書込なし**。生成ファイルの手編集なし（`build_kb.py` による正規再生成のみ）。既存研究の他レーンやMASTERは無変更。

細かな機械検査記録は `knowledge/tools/symbol_expansion_validation_20261029.json` を参照。新しい辞書の全239行は `knowledge/tools/_symbols_add_20261029.tsv` に、旧原本はバックアップに分けて保存した。次回はV9では不足する `0x5159F0` 等の関数境界の正式な資料が追加されてから再判定すること。
