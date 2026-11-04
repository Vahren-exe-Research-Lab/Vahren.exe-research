# T028 放浪・傭兵の結果文面が同じ出力関数へ合流する経路（旧B研究の回収）

- research_id: `B-20261028-1515-T028-WANDER-MERCENARY-TEMPLATE-DISPATCH-01`
- owner / tasks: `B` / `T028`。T011死亡・戦後所属変更との意味接続はVERIFY。
- observed_at: `2026-10-28 15H JST`。source/PE実測検証時点: `2026-11-02 03H JST`（元報告本文と原作PEのSHA-256を認可PCで再hash、静的E8検査の**再実行ではない**）。
- source_relative_paths: `_REDEV_RESEARCH/data/T028_WANDER_MERCENARY_TEMPLATE_DISPATCH_NATIVE_20261028_15H.md`（owner原文、27行）。
- source_sha256: `4573D1AF5621B501BC1C7A3B03BA73C489BFC9E0294E2069F4CA36A018407188`（本run PC実測）。
- original_PE_source: `_REDEV_RESEARCH/rea_lab/targets/hakushin067_Vahren.exe` / SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`（本run PC実測）。旧V3擬似Cの意味は歴史的参考。現行V9との全照合は本run未実施。
- evidence_kind: `STATIC`（旧報告のoriginal-PE ASM）/ `INFERRED` / `VERIFY`。`DYNAMIC=0`, 原作Gameplay `Golden PASS=0`, `strict MATCH=0`, 新規owner `READY=0`。現在段階 `PUBLISHED_INTAKE`（Github読戻しを条件）/ `NOT_CURATED`。

## 再利用できる原作ASM出典
- 原文L9: `0x49891E`のmanager候補`+0x1EEC3C`比較で条件分岐。該当枝の`0x4989BA -> 0x436BC0`（放浪文の展開候補）、`0x4989E7 -> 0x52CF50`（結果文の共通経路）。
- 原文L10: 別枝は`0x498BB1`の先行AL検査を経て`0x498BC6`で同offsetを比較し、`0x498C67 -> 0x436BC0`、`0x498C95 -> 0x52CF50`。定数文字列は傭兵化を通知する文面。両枝の実時相・所属変更は未証明。
- 原文L13–15: `0x498966 -> 0x4051D0`と`0x498C13 -> 0x4051D0`にスタック由来値が渡されるが、500/10/25がUIに印字された数値という証拠ではない。テンプレート置換の正式ABIはVERIFY。
- 原文L17–19: 旧研究時点でのnative窓SHA `0x4988EF`から253B=`D7E9400C84169ACFF94EDDF632F2CABD8C6CA87438BB983475CBDFCD047623C1`、`0x498BB9`から225B=`FE22A1FF18BA553269EBBCA956720236DFC9040AAB7355EAB48DC5B5097488BD`。相対E8 6/6は**歴史的検証結果**で、今回再実行PASSと数えない。

## 先行・訂正、未検証と再開点
- prior_ids: B/T028の2026-10-28 14H候補選択・文字列producer（原文L8）、および同日16H `B-20261028-16H-T028-POSTRESULT-DIALOG-DISPATCH-FALLBACK-01`。`supersedes: null`、15Hの新差分は二つの文面経路と合流するCALL。後続の21/22/23H別sink/consumer研究を参照し同一CALLを新発見として重複計数しない。
- VERIFY: 所属・士気・忠誠の変更、+0x1EEC3Cのowner identity、`0x52CF50`がUI以外に書くか、原作DAT/SAVE/MAP入力での到達性。結果文の表示文句だけから戦後副作用は断定不可。
- G4 battle takeover candidate only: 戦後通知とUnit/World結果に関係する可能性はあるが、外部戦闘結果のCOMMIT契約を証明しない。元P0 takeover owner資料は非変更。
- next_validation: 正規の未改変原作EXE/DATと同SAVE/MAP/入力/RNGで両枝の画面・Unit/World/保存前後を比較。安全な最小再現は元報告の出典L9–19と上記SHAを照合し、`REF_BATTLE_AI_MORALE.md`/既存PRに同ID/訂正がないか確認すること。原作未起動。
- safety: 既存HOLD21、10/25欠落、旧拒否操作・範囲のBLOCKEDを継続。保護対象データ・実ゲーム・他owner/develop/REF/辞書には触れない。
