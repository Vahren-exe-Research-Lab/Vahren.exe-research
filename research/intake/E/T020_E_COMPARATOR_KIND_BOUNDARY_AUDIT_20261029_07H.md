# E/T018・T020 比較器の証拠種別混同防止（2026-10-29 07H JST）
研究ID: E-AUDIT-20261029-07H-T018-T020-COMPARATOR-KIND-BOUNDARY-01
Owner E/T018・T020（T019参照）。STATIC READ-ONLY CROSSWALK / SYNTHETIC EXECUTED / VERIFY / NOT READY。
## 直接参照と新しい発見
- Desktop Commander Local CompactでMASTER末尾、レーン規約、A-D HANDOFF末尾、REA PROGRESS、dev_lab IMPLEMENTATION_PLAN、T018/T019、E06H元ファイル固定gate、E02H合成G2 gate、検索索引README/旧BUILD_MANIFESTを読取。
- dev_lab/src/hakushin_compat/battle_compare.py は静的MAP描画・画像画素差の比較器。test_battle_compare.pyの完全一致画像でも status=PIXEL_DIFF_ONLY__NO_GAMEPLAY_PARITY、reference_is_original_exe_verified=False、aligned_camera_verified=False。
- DEVLAB-006は計画書上 old-vs-new 比較runnerの開発用ID。既存battle_compare.pyを原作戦闘G0/G1/G2照合runnerへ誤同定しない。別の比較器の不存在まで断言しない。
- E06H source pinの SOURCE_PINNED_STATIC_ONLY_NOT_NATIVE とE02H SYNTHETIC_G2_CROSS_CONTRACT_CONSISTENT_NOT_NATIVE は別の情報型。画素差0・正しいsource SHA・同runの自己申告3点を組み合わせてもnative Goldenへ昇格不可。
- 新Eコード tests/t020_e_comparator_kind_boundary_20261029_07H.py はE06Hの実Library pin byte取得＋dev実コードの静的文言/AST検査、偽成功フラグ、run混合、G0 UI、G1 SAVE/input、G2 MAP/roster欠落を非破壊的に回帰。最良状態も REVIEW_ONLY_NOT_NATIVE。
## 今回の独立検証
- 新規15/15 PASS exit0、既存E06H 8/8 PASS exit0、既存E02H 25/25 PASS exit0、合計今回実行48/48 PASS。旧原作・DEV描画アプリ・過去13H安全拒否14件はNOT RUN。
- 新EコードSHA256=CB94301BFC4DC4588041230707518653AACE1FA8787FDF3EF3AFC11C49B35B10。
- 既存E06H pinコードSHA256=CF0ADB6FF53BF5A10B56EAA1CE947ED6ED382946DA03CE4915C80FBD5B54B277。
- dev_lab battle_compare.py SHA256=CBB6ED0B6D8ABA896A9746B08C09AAB00838BDD3388415ED7AC439148A694221、対応test SHA256=78C030E05BD3A3A33684801AFA0BC8977A3508B6CAC6DB69B729459621352E63。
## T018・T019・MASTER
- C-NB02同一合法旧原作のG0通常UI開戦、G1直前未改変SAVE bytes/SHA＋順序付き入力、G2実MAP bytes/SHA＋三陣営＋順序付きUnit/Troopとactive windowが必須。G3結果/G4World差分も未充足。旧原作DYNAMIC OBSERVED=0、actual Golden PASS=0、strict MATCH=0。過去構造RAW8はGoldenへ加算しない。
- 元EXE識別SHA E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187 は過去manifest値。今回原本EXE再SHA、DAT復元証明、原作実行なし。
- T019新規確定矛盾0。GameClear DAT13/TXT2の字句検索scope差RESOLVED、script2同名winner/phase flag/TXT実読込/gwrite復帰/decide11用途はVERIFYの継承。
- 最終確認正式MASTER checkpoint196、READY596=A115/B229/C136/D116。34Task DONE9/IN_PROGRESS21/VERIFY4は旧確認値（今回全履歴再集計NOT RUN）。今回E正式READY統合なし。
- Bレーン07Hの B-20261029-0716-T028-INNER-POINT-OUTER-CENTER-NATIVE-01 はB所有でSTATIC/VERIFY/NOT READY、代理統合しない。他レーン最新の全意味重複検査はNOT RUN。
## 安全・保存境界・次の優先
- 旧T018表境界・T019拒否XREF・C T026/T032・D T030 TSV・0x5710C0・10/28 13H安全拒否14ケースおよび各旧拒否はBLOCKED継続。同一拒否操作の別shell/tool/path/Remote/ZIP迂回0。今回新安全拒否0、接続障害0。
- Library21Hの正しい別名pinは維持。Library原本23件と10/25-27 PC研究133件は前回の保全成果を継承し、今回全件再監査/正式統合はNOT RUN。破損した同名コピーは現存するため誤用防止を継続。
- 今回書込はE所有testsの新コード、報告、readback記録のみ。MASTER、T018正式表、T019表、A-D、REA、dev_lab、EXE/DAT/SAVE/ZIP、Git/Work/設定/scheduleへの変更なし。
- 次は開発ownerが実original vs reimplementation比較の入力・出力schemaを提供した場合に限りE側の証拠資格チェックを接続する。すべての原作観測条件が揃わない間はREVIEW_ONLYで止め、厳密一致と同一画面の画素差を混同しない。
