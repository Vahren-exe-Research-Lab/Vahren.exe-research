# T028 結果出力からdialog索引・別fallbackへ連なる静的経路（旧B研究の回収）

- research_id: `B-20261028-16H-T028-POSTRESULT-DIALOG-DISPATCH-FALLBACK-01`
- owner / tasks: `B` / `T028`。T011戦後変更との関連はVERIFY。
- observed_at: `2026-10-28 16H JST`。source/PE SHA実測検証: `2026-11-02 03H JST`。本runは保存済み研究本文と原作PEのhash再検査のみ、原作ASM検証の再実行はしていない。
- source_relative_paths: `_REDEV_RESEARCH/data/T028_POSTRESULT_DIALOG_DISPATCH_FALLBACK_NATIVE_20261028_16H.md`（23行）。
- source_sha256: `C9EDE1AE7A22BCB44AFCFD53C6DD3525B0F23E93FEA8C378D2B607F4CD66A938`（PC実測）。
- original_PE_source: `_REDEV_RESEARCH/rea_lab/targets/hakushin067_Vahren.exe` / SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`（PC実測）。当時のV3解釈を含むため現行V9完全再照合は未実施。
- evidence_kind: `STATIC`（保存済native E8）/ `INFERRED` / `VERIFY`; 原作 `DYNAMIC=0`, `Golden PASS=0`, `strict MATCH=0`, 新規 `READY=0`。Github本文readback時点で `PUBLISHED_INTAKE / NOT_CURATED`。

## 原文のVA・CALL・offset根拠
- 原文L8–12: 15Hの放浪・傭兵両枝から入る`0x52CF50`内で、`0x52CF80 -> 0x52AD90` と `0x52D047 -> 0x43F470` がE8。`0x43F71F`でASCII 'dialog'定数への参照を積み、`0x43F72F -> 0x416E80`, `0x43F73F -> 0x416B90` を通る。`0x43F744`のゼロ判定後`0x43F752 CALL EDX`のindirect vcallは実callee未確定。
- 原文L14–15: `0x43F5B1`のスタック候補ゼロ分岐で`0x43F5BC`に別定数を積む; 旧V3解釈では'`decide11`' fallback。14H上流selectorの`decide3/decide11`選択とこの**内部fallback**は別の条件。入力来歴はVERIFY。
- 原文L17–18: E8 4/4 (`0x52CF80`, `0x52D047`, `0x43F72F`, `0x43F73F`)は旧original-byte検査結果。本runでASM照合を再実行したと主張しない。original native 0x43F705から80B historical SHA256 `2AB700ADCB72691ECE39F8B274A17F82BF89CE676B5FF71AC17E7EF9027F8137`。

## 先行、境界と次工程
- prior_ids: `B-20261028-1515-T028-WANDER-MERCENARY-TEMPLATE-DISPATCH-01`（15H報告）、14H候補producer。`supersedes: null`; 本IDは共通出力の内部を精緻化し、15Hの二文面CALLを再発見扱いしない。
- VERIFY: indirect vcall target、UIと状態変更の分離、オブジェクトの正式ABI、出力直前/直後にUnit/Spot/Power/士気を書換える経路の有無。通知が存在しても戦闘の永続結果ではない。
- G4 related: native結果通知の候補として`REF_BATTLE_TAKEOVER.md`の未確証settlement境界へリンク可能だが、外部結果COMMITTED・G5 PASSの根拠にはしない。
- next_validation: 旧EXE/DAT/SAVE/MAP/RNG同runで2文面と内部fallbackを比較し、vcallへの到達・戻りとWorld保存を分離観測する。現在はDESIGNED/NOT RUN。既存HOLD/拒否/10/25・03H/07H欠落を保持。
- reproduction: 元report L8–18でE8 site→calleeと定数offsetの範囲を確認し上記実測source SHAで版を固定。B owner intake以外には書かない。
