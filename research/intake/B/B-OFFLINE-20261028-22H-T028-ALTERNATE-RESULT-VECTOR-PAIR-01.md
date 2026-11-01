# T028：代替結果sink `0x434B10`による管理vectorへの二段追記（2026-10-28 22H、既存成果の回収）

- research_id: `B-OFFLINE-20261028-22H-T028-ALTERNATE-RESULT-VECTOR-PAIR-01`
- owner/tasks: B / T028（T011・戦後所属変更との意味接続はVERIFY）。
- observed_at: 2026-10-28 22H JST。archive / original PE independent recheck: 2026-11-02 JST。
- evidence: **STATIC-ORIGINAL-PE-ASM / STATIC-OLD-GHIDRA / INFERRED / VERIFY**。DYNAMIC=0、original gameplay Golden PASS=0、strict MATCH=0、新規READY=0。
- current state: PRIVATE `research/intake/B/` owner staging / **NOT_CURATED**。PC MASTER/HANDOFF・現行V9は接続不可のため未確認、PCへの反映 **OFFLINE_UNSYNCED**。
- recovered from verified safe archive `HAKUSHIN_B_LANE_SAFE_RECOVERY_20261029_V3.zip`, SHA256 `059B91381C1B58214353769006E0F4049FCDE393A6B7970F4513602878A2B2C9`。同梱manifestは134 source membersを記録、既拒否関連21件は除外されており今回の研究は収録済み。
- owner source `data/B_T028_ALTERNATE_RESULT_VECTOR_PAIR_OFFLINE_20261028_22H.md`, **実測member SHA256** `626E7F979F35DE0824EAB08AD68CCAFF7C98B9DEAB28977C445609472CB3B51E`。
- owner evidence `data/B_T028_ALTERNATE_RESULT_VECTOR_PAIR_EVIDENCE_20261028_22H.json`, **実測member SHA256** `B45D7BC12A3E00150B85D772AACFF3CD38E10BDD9325E024BEA2D536D70BBFFB`。両digestはarchive manifestと一致。
- current available original PE (Library, **PC最新ではない**): `Vahren.exe`, SHA256 **このrunで再測定** `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。未起動・未改変。
- historical search evidence: `HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip` SHA256 `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`、内部 `headless_analysis/search_index/search.sqlite` SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`。これは**2026-10-21旧STATIC索引**で統合V9とは異なる。

## 本質的な差分：別画面の直接描画ではなく追記処理を含む

先行21H `B-OFFLINE-20261028-21H-T028-WANDER-MERCENARY-DUAL-RESULT-SINK-01` は、放浪 `0x498AB3` と傭兵化 `0x498D55` が `0x434B10`へE8することまでを確認していた。そのCALLは**本IDの新規発見に二重計上しない**。今回の原作ASM根拠：

| VA | 限定STATIC意味 |
| --- | --- |
| `0x434B42`, `0x434B48` | スタック引数の管理object候補に `+0x1EEC74` を加え、vector候補のアドレスを構築。 |
| `0x434B5A -> 0x415530` | 同vector候補へ最初の追加処理CALL。 |
| `0x434B5F`～`0x434B7B` | global index `0xAC0868`をincrementし、8以上なら0へ戻し、128-byte幅のscratch `0xAC0460` を選択。既存index 0..7のとき8スロット循環。 |
| `0x434B82 -> 0x5D1779` | 入力整数候補を10進文字列化（`__itoa`の旧索引名）。 |
| `0x434BC0 -> 0x402800` | 一時stringへの転記CALL。 |
| `0x434BD0 -> 0x429A00` | 同vector候補への追加経路。下位 `0x429AAC` はvector endに `0x1C` を加算。 |

**INFERRED**: `manager+0x1EEC74` の幅0x1C要素vectorに、文面と別の値の表現を二段階で加える処理。これは「8件で永続通知が消える」ではない。`0xAC0460`はフォーマット時の一時scratchであり、管理vectorの保持数と独立。入力値の正体、実際のUI表示、consumer/erase/save、Unitの所属変更、同じバトル中の副作用はすべて **VERIFY**。

## 実測証拠・訂正・次の検証

- `0x434B10`先頭から427 bytesの原作SHA256 `9B727120D32D9011E453DCB15B99C7A266A2192899104341693476F952A85A92` を**今回の別Library実PEから再hashして一致**。
- 旧evidence JSONのnative instructions **24/24**、rel32 native E8 sites **7/7** を原作PEに独立再照合、すべて一致。対象CALLには `0x434B5A,0x434B82,0x434BC0,0x434BD0,0x406DF7,0x498AB3,0x498D55` を含む。
- **先行/訂正**: 21Hの「`0x434B10`は不明な別sink」は追記vectorを含むと精緻化。ただし **「永続履歴表示である」「傭兵化を確定する」へ昇格しない**。既存REF_BATTLE_AI_MORALEに当該2ID/明細VAの直接登録は今回閲覧時なし。curatorが現行owner・重複・訂正を審査。
- KB_CANDIDATE: `0x434B10`、manager `+0x1EEC74`、`0x429AAC`要素幅0x1C、scratch `0xAC0868/0xAC0460`。すべて役割の厳密命名・ABI・readerは未確証。Bはdevelop/REF/symbols/structsに書かない。
- G4 takeoverへの関連: 戦後通知/所属状態との接点候補であって、結果commit/永続化の境界契約を立証しない。Golden条件は無改変原作0.67＋改変前DAT＋同一SAVE/MAP/input/RNGで両経路の通知vectorとUnit実体・保存を同一runで照合すること。
- Next cursor: `manager+0x1EEC74`へのread/clear/save writer/consumer、`0x434B10`第2入力の生成元、`0x1EEC3C`条件の全到達定義。次のPC復帰時は原本owner/最新V9/同ID/安全HOLD21を照合。過去の安全拒否や保護VAは別ツール経路でも再解析しない。
