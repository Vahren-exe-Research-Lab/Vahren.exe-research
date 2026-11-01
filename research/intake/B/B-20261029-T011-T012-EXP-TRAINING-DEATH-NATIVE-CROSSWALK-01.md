# T011/T012 死亡EXP補正・訓練閾値MOV・召喚EXP境界（旧B原本研究の保全）

- research_id: `B-20261029-T011-T012-EXP-TRAINING-DEATH-NATIVE-CROSSWALK-01`
- owner: `B` / tasks: `T011` primary; `T012` crossref。T028死亡／P0 G4戦後処理は参照候補のみ。
- observed_at: `2026-10-29 JST`。source report/PEファイルSHA実測: `2026-11-02 03H JST`（この回は原報告とPEのファイルhash検査のみ、ASM/E8/原DAT行を新たに全実測したわけではない）。
- source_relative_paths: `_REDEV_RESEARCH/data/T011_T012_EXP_TRAINING_DEATH_CROSSWALK_NATIVE_20261029.md`（B所有59行）；DAT参照は元owner記録の`data/normalized/hakushin067_core/a_default/script/context.dat`等であり、この回DAT hashを再検証していない。
- source_sha256: `314B33BB633B6C113F78B8B67FB3D72B9688FFAB9A8672F63D5463575E7EB8F0`（今回PCで実測）。
- original_PE: `_REDEV_RESEARCH/rea_lab/targets/hakushin067_Vahren.exe`, SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`（今回PCで実測、起動なし）。
- V9_source: 原ownerは統合V9の特定CALLを照合。V9索引のDB digest・raw ASMウィンドウを**本runで再hash/再走査していない**。
- evidence_kind: `STATIC`（原報告保存のnative ASM/DAT行）、`INFERRED`（条件付き数式、呼出意味）、`VERIFY`（原作到達・セーブ・召喚EXP移管）。`DYNAMIC=0`、original game `Golden PASS=0`、`strict MATCH=0`、B newly `READY=0`。stage: `PUBLISHED_INTAKE / NOT_CURATED`（正確なGithub readbackを条件）。

## 元報告の限定根拠と意味

- 原文L9–16: ver0.67 `context.dat` L110 `dead_penalty = 95` は**旧source snapshotの直接指定**（実効runtime値ではない）。原作VA `0x588D77` は `dead_penalty` lookup、`0x588D7C -> 0x46F4C0`、`0x588D85..0x588DB3` FPUはUnitData累積EXP `+0x16C` と設定係数を乗算。 `0x588DE0` が結果を書戻す。通常非負の適法入力では概ね `floor(oldEXP * dead_penalty / 100 + 0.5)`；例1000→950。全死亡に常時適用されると断定しない。旧native 121B segment SHA256 `998FB5293D12BCAF2BA07A407580821F9379943C26E2CC377EEAE914F45EC724` は歴史的測定値。
- 原文L20–24: 訓練 `0x4723D8` は UnitData `+0x170` 次レベル閾値を `+0x16C` EXPに `MOV` し、`0x4723DE -> 0x58A650` レベル更新へ。通常戦闘 `0x551FB2` のEXP `ADD` と異なる。訓練ループ回数の元入力・レベル上限挙動・実際のレベル上昇はVERIFY。
- 原文L27–35: 共通EXP計算 `0x551E50` の既知直接E8 caller `0x547A8C`（簡易召喚関連）、`0x551167`（攻撃）、`0x551C6A`（回復）、`0x57F4E9`（通常召喚関連）は**先行EXP研究の再掲で新発見ではない**。UnitData `+0x168` Lv/`+0x16C` EXP/`+0x170` next。召喚 `+0x1E4B4` cache・child `+0x1C8`への共有参照と、戦後の恒久EXP移管の有無は別問題、後者はVERIFY。
- 原文L49–53: `exp_mul` の491個の原DAT文字列指定という旧レポート上の静的ソース集計は定義の複数宣言・継承を含み、491人の実効成長倍率ではない。今回の再集計件数と主張しない。

## 先行・訂正・戦闘乗っ取りへ残る境界

- prior_ids: 過去EXP CP01–25、REA側P0_SUMMON_EXP_OWNER、既存`REF_UNIT_EXP_SUMMON.md` §§1–4（多くの仕組みは**既にcurated**）。同じ既知CALL/機能を新発見/新curated項目として二重に数えない。supersedes: null; 本件は同一owner一次報告の追跡可能な元根拠・条件・注意点の保全。
- G4_takeover: native battle finish `0x493630`等の戦後副作用について、death EXP補正、`+0x16C`への反映、親子・召喚cache/Unit同一性、Save→Load consistencyが確認されなければ外部結果をCOMMITTEDと扱わない。P0 takeover owner所有資料を変更せず、`REF_BATTLE_TAKEOVER.md`は参照に留める。
- VERIFY: `dead_penalty` 実効値/死亡branch、x87例外・丸め境界、訓練回数の正しい呼出元、召喚Rの精算、同一UnitData record alias、戦後save snapshotと原ゲーム終端到達。
- next_validation: 未改変原作EXE・元DAT・同SAVE/MAP/入力/RNGで死亡前後 EXP/Lv/閾値と召喚キャッシュ/親子を追跡し、訓練0/1/2と死亡復帰を交差比較。元owner MD L9–44のVA/E8/fieldを既存V9で限定照合、実機Goldenまでは未判定のまま維持。
- safety: 私的データ、EXE/DAT/MAP/SAVE/ZIP、巨大索引、元ログ、過去拒否操作・証拠はGitHubへ送らず、本文は限定サニタイズ要約のみ。E MASTER/共有REF/辞書・developへ書き込まない。
