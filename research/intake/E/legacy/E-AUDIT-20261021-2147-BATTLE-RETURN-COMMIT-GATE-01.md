# T018/T020 — 戦闘終了・戦略復帰の受入境界（既存E研究の安全な出典復元）

- **research_id:** `E-AUDIT-20261021-2147-BATTLE-RETURN-COMMIT-GATE-01`（既存ID。新規発見・新規READYではない）
- **owner / tasks:** E / T018・T020。A/B/Cの元資料は**引用のみ・read-only**。他ownerの研究内容をEへ移管しない。
- **source_relative_path:** `tests/T020_BATTLE_RETURN_COMMIT_GATE_20261021_2147.md`
- **verified original PC SHA-256:** `2417E9BDEB47C7BF8B5602A41CDE8BB214724528E34CC5E5B46BE3B0E3CA24F3` / 4,063 bytes。E担当が2026-11-03 JSTに原本をread-onlyで実測。**本GitHub文書は機密・保護対象を省いた要約で、原本とバイト同一ではない。**
- **original EXE SHA-256:** `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`（過去のmanifest値。今回は原作EXE自体を再hash・起動していない）。
- **evidence_kind:** STATIC_CROSS_LANE_READONLY + SYNTHETIC_DESIGN + VERIFY。原作G0–G4実行はNOT RUN。Golden PASS=0 / strict MATCH=0 / 新正式READY=0 / 新MASTER正式変更=0。
- **prior/supersedes/errata:** 同一研究IDの歴史資料であり、新IDは作らない。既存の [E-owned synthetic runner](../repro/t020_battle_return_commit_gate_20261021_2147.py) と対応する。runnerの存在・合成ケース設計を原作受入証拠に昇格しない。旧checkpoint/READY件数はこの資料では更新・継承しない。

## E側の保存すべき受入仕様（元報告の意味を保持）

1. G0合法UI→G1同runの直前SAVE/入力→G2実MAP・順序付き出撃名簿を基礎に、**G3終了直前可視戦況**と**G4戦略復帰後の可視world状態**を別々の原作一次receiptで証明する。B側のstage呼称を同名として置換しない。
2. 原作終了routeは自然終端・BattleWnd・DAT呼出の候補を区別する。既存B側静的資料に現れる `0x493630` の複数入口と `0x492D80` との関係は、**全runで同routeに到達する証拠ではない**。
3. A側の静的参照は、GameEvent Task virtual+4 → `0x4335E0` → `0x492D80` → active再判定 → 同call内 `0x4338D0` VM runnerという候補列。World/VM再入を一律「次tick」と想定しない。
4. B側資料の `0x493630` は通常結果の副作用・scene解除・再公開の静的候補を含み、特定条件で通常経路以前に終端があり得る。raw resultFlag、戻り値やscene表示のみでG4のworld変化を断定しない。
5. 外部戦闘結果の取込み設計は**native finishと別実装の二重commitを禁止**する。commit権限を一経路に限定し、一意battle/run識別子と独立事後receiptを要求する。これは設計ゲートであり、置換実装の動作確証ではない。
6. Spot.member、Power+0x68、Unit+0x84等の保存参照と、実際のworld roster・死亡・退却・経験値反映は別項目として比較する。Unit対応を数字の一致のみで捏造しない。

## 合成負例と未完了

- EXIT-01 観測不足→DESIGNED_NOT_RUN、EXIT-02 G4不足→VERIFY、EXIT-03 異run混合→REJECT_EVIDENCE、EXIT-04 二重commit→REJECT_DOUBLE_COMMIT。
- EXIT-05 route名のみ→VERIFY、EXIT-06 new buildまたは出典SHA不足→NO_STRICT_COMPARISON、EXIT-07 同run書類が揃ってもREADY_FOR_COMPARISONでありMATCHではない。**これらは元報告の設計ケースであり今回テスト実行結果ではない。**
- 最小比較record: session ID、old/new EXE・SAVE・DAT・MAP・入力の実測SHA、G0–G4のsource/time/capture SHA、ordered Unit/Troop、HP/MP/EXP/死亡/退却、Spot/Power/金銭/イベント変数/次world継続動作をnullableで分離。
- **出典:** A `exe/T010_BATTLE_FRAME_ORDER.md` §3–4、B `search_index/BATTLE_BRIDGE_NEW_FINDINGS_20261021_1830.md` §3–5（該当B研究はNOT READY）、C `evidence/T025_WRQ_C_BATTLES_CAPTURE_REFERENCE_GATES_20261013.json`（read-onlyで引用）。このrunでA/B/C原本のSHAやネイティブ命令列は再検証していない。
- **next_validation:** 拒否済み対象を除外し、合法かつ独立に取得された**同一runのG0 UI、G1 SAVE+入力、G2 MAP/三陣営順序付き配置、G3、G4**一次証拠の存在・出典SHA・時相を確認する。欠損時はNOT_QUALIFIEDのまま。既存安全拒否対象は本文・経路とも再試行しない。

**Publication scope:** private owner-E intake only / VERIFY / NOT_CURATED。正式REF・辞書・developへの採録は専任curatorのみ。
