# T028 原作 dead_event=count 特殊枝と色名候補のキュー投入（歴史的B成果・重複回収）

- research_id: `B-20261027-2114-T028-COUNT-DEATH-EVENT-COLOR-QUEUE-01`
- owner: `B` / tasks: `T028`（Unit死亡とT011の限定関連、G4戦後状態・通知はVERIFY）。
- observed_at: `2026-10-27 21H JST`。source report / original PE SHA再計測: `2026-11-02 03H JST`（PC上の既存資料とPEのファイル単位hash確認）。
- source_relative_paths: `_REDEV_RESEARCH/data/T028_DEADEVENT_COUNT_COLOR_QUEUE_NATIVE_20261027_21H.md`（B所有17行）。
- source_sha256: `2B927D6938D6D9A319CE3BE17452681401C4D028FD251CB4A2D70924E185CE71`（今回PCでGet-FileHash実測）。
- original_PE: `_REDEV_RESEARCH/rea_lab/targets/hakushin067_Vahren.exe` SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`（今回PCで実測、一切起動/改変せず）。
- evidence_kind: `STATIC`（原owner保存のnative ASM/E8）、`INFERRED`（容器の意味）、`VERIFY`（自然到達・実ゲーム後処理）。`DYNAMIC=0` / original game `Golden PASS=0` / `strict MATCH=0` / new B `READY=0`。状態: `PUBLISHED_INTAKE / NOT_CURATED`（GitHub全文一致読戻しが前提）。

## 原文の根拠VA・CALL・offset

- 原文L7–8: Unit側 `0x5789F2` に死亡callback分岐候補（Unit `+0x1862C` 非空ゲート）、文字列 `count` 判定を経て `0x578A1B -> 0x49CF20` に入る。別のSimpleUnit側 `0x544BEF -> 0x49CF20` が同様の特別枝。通常named event dispatcherへの一括同一視は誤り。
- 原文L9–10: `0x49CF51` は対象 `+0x1D4` ポインタを参照、`0x49CF57` はその `+0x18` バイトを読み、ゼロ／非ゼロからASCII `blue` / `red` を選ぶ候補。 `0x49CFB8 -> 0x429A00` はowner候補 `+0x1EEFA0` の `0x1C` byte幅文字列record追加と関連。文字列が実際に何を表示・記録するかはVERIFY。
- 原文L11: `0x49CFD9` 以降は `0x415530` 複数CALLがあるが、即座に複数の死亡効果が適用された証拠ではない。
- 原文L12–13: named-event別枝 `0x578AF5 -> 0x4321B0` と `count` 特殊枝を分離。過去native 5 E8 sites 5/5・original PE `0x49CF20..0x49D02B` window SHA256 `84404302DB75AD8B3E8B74C7589B44CD94799281BE04290B5DCBD9C6B1F632E6` は**旧研究記録**であり今回E8再走査PASSは計上しない。

## 既知との関係・未解決

- prior_ids: 既存B/T028 dead_event一般ルート、named event / class分岐、`REF_BATTLE_AI_MORALE.md`のcount特殊経路。これらは本IDで再発見数を増やさない。supersedes: null。新規差分は色選択・容器追記・named dispatch分離のbounded STATIC crosswalk。
- crossref boundary: REF記載の別の名称格納field `+0x1861C` と本原文death gate `+0x1862C` は同一であると証明できていない。移送・phase・別Unit型を照合するまで単一offsetに訂正しない。
- VERIFY: `+0x1D4` 参照先型、`+0x1EEFA0` のowner/consumer・セーブ対象か、ゲームDATで `count` が合法到達するか、実死亡とUI・士気/敗走/World/EXP結果との関係。
- next_validation: 原作未改変EXE/DATと同一SAVE/MAP/input/RNGで Unit/SimpleUnit×dead_event空/count/named×flag0/非0の状態変化・キュー・色・次tickを同run比較。まず元owner報告L7–13とV9の安全な直接CALL/fieldをcuratorが照合し、G4 settlement契約には昇格させない。
- safety: 既存HOLD21・拒否済操作/本文・10/25/03H/07H欠損を維持し、禁VA・原作・他owner・develop・辞書・MASTERは不変更。
