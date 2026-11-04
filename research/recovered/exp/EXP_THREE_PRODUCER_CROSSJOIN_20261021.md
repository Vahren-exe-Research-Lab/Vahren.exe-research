# EXP-COLLAB-20261021-2112-01 / CP02｜UnitData風cache Rの3系統producer

- 状態: STATIC_GHIDRA_DIRECT_CALL / INFERRED / VERIFY / NOT READY。原作実機NOT RUN。
- 取得元: 原作ver0.67 Ghidra `search_index/search.sqlite`、直接CALL索引。Ghidra擬似Cのパラメータ型と呼出規約は別途検証。
- 旧知見: B/REA `P0_SUMMON_EXP_OWNER_REPORT_20261021.md`は `0x577260` の4直接callerと召喚Rを既報。今回の差分は**そのうち3 producer本体を同一4関数のCALL site順で一括検証**した点。別ownerの正式READYを新規計上しない。

| caller | 検索 577260 | UnitData生成 58B7F0 | 複写 466BA0 | 登録 577310 |
|---|---|---|---|---|
| 0x547490 | 0x5477F4 | 0x547897 | 0x5478B3 | 0x5478BA |
| 0x553390 | 0x55352D | 0x5535E4 | 0x553600 | 0x55360C |
| 0x54E7B0 | 0x54EE82 | 0x54EF3E | 0x54EF5A | 0x54EF69 |

- [STATIC] 上の各行は `calls` の `caller_va/callee_va/site_va` に実在する、順序付き4直接CALL。合計12 siteを照合（ゲーム内到達頻度や条件成立回数ではない）。
- [STATIC_PSEUDOC] 3callerとも `0x577260` の戻値がNULLの分岐内でUnitData生成→複写→登録を行う候補。hitでは既存Rを利用するように読める。
- [STATIC] `0x466BA0` はUnitDataの `+0x168/+0x16C/+0x170` をソースからコピーする。したがってmiss時に新しく生成されたUnitDataレベル・EXP・閾値がノード内Rへ複写される構造と整合。
- [BOUNDARY] 一時RへのEXP加算 `0x551E50`、node+0x28、BattleUnit+0x1C8の連結はP0既知。新しいEXP親転送の証明ではない。
- [VERIFY] 0x547490と0x553390の可視スキル種別・入力元オブジェクト・検索キー、3producerが同一BattleUnitを受け取るか、生成分岐への実到達、hit後のEXP/Lv再初期化を別の場所で行うか、元ユニットが死亡した場合の処理を未特定。
- [NEXT] `0x547490` のskill context、`0x553390` のcaller、`0x577310` に渡すキーの生成元を独立調査。BattleUnit所属キーが同一と確認できるまでは「3経路間でXP共有」を原作仕様として断定しない。
- [IMPACT] 外部戦闘EXE設計では `producer_path, source_actor_id, summon_key, record_generation, owner_unit_id, gain_event_id` を分けて記録。actorごと1個のEXPノードと決め打ちしない（設計候補）。
