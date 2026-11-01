# T028：放浪・傭兵化の同文面と条件付き二系統送信先（2026-10-28 21H、既存成果の回収）

- research_id: `B-OFFLINE-20261028-21H-T028-WANDER-MERCENARY-DUAL-RESULT-SINK-01`
- owner/tasks: B / T028（T011の所属・雇用状態との関連は未確証）
- observed_at: 2026-10-28 21H JST（既存研究）。archive再照合: 2026-11-02 JST。
- evidence_kind: **STATIC-ORIGINAL-PE-ASM / STATIC-OLD-GHIDRA / INFERRED / VERIFY**。DYNAMIC=0、original gameplay Golden PASS=0、strict MATCH=0、新規READY=0。
- publication: PRIVATE owner intake candidate、**NOT_CURATED**。研究PC最新MASTER/HANDOFFは接続障害で未照合。PCへの同期は **OFFLINE_UNSYNCED**。
- archive: `HAKUSHIN_B_LANE_SAFE_RECOVERY_20261029_V3.zip` SHA256 `059B91381C1B58214353769006E0F4049FCDE393A6B7970F4513602878A2B2C9`（134 source files / 21 safety-excluded files、今回の2研究は収録対象）。ZIP CRC PASS。
- owner original report: `data/B_T028_WANDER_MERCENARY_DUAL_RESULT_SINK_OFFLINE_20261028_21H.md`, SHA256 `E26426D09BC68B25F7EF7FBAB76F124F2BFE9B98115E7493F9EBD408AAEBDCB9`; native receipt `data/B_T028_DUAL_RESULT_SINK_EVIDENCE_20261028_21H.json`, SHA256 `837A9EA5732C7B6D757FC430CDC3DA8950A89091E17BC04D0B62D35AE36E1397`。両者は実ZIP memberを再hashし同梱manifestと一致。
- original PE: Library上の `Vahren.exe` 2,910,720 bytes、**今回再測定** SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。原本未起動・未改変。
- old static index: `HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip` SHA256 `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`、`headless_analysis/search_index/search.sqlite` SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`。**旧10/21スナップショットであり統合V9現物ではない**。

## Native STATIC：同じ文字列を異なるCALLへ渡す

| 意味（未確定） | 比較・分岐 | 一致側 | 不一致側 | 同文面の定数 |
| --- | --- | --- | --- | --- |
| 放浪 | `0x49891E CMP [EDI+0x1EEC3C],EBX`; `0x498924 JNE 0x4989F1` | `0x4989E7 E8 -> 0x52CF50` | `0x498AB3 E8 -> 0x434B10` | `0x63298C` / `0x6329A0`「$$$は放浪しました」 |
| 傭兵化 | `0x498BC6 CMP [EDI+0x1EEC3C],EBX`; `0x498BCC JNE 0x498C9F` | `0x498C95 E8 -> 0x52CF50` | `0x498D55 E8 -> 0x434B10` | `0x6329BC` / `0x6329D4`「$$$は傭兵になりました」 |

`0x497CB4` / `0x498B2A` に `MOV EBX,1` があるが、全到達経路でEBX=1という証明はない。従って「状態フィールドが常に1ならdialog」という命名は **INFERRED/VERIFY**。旧報告15–16Hの「共通dialogのみ」という過度な一般化を限定し、`0x434B10`の別送信先を認める。実際の所属変更・通知表示・間接副作用は不明。

## 今回の独立照合・訂正・次の検証

- PE bytes 12/12、native E8 4/4、相対分岐4/4、CP932文字列4/4を**今回、原作PEから独立再検証**。各事象の文面2組はraw bytesで一致。SHA256 `[0x49891E,0x498AB8)`=`DD2A116E2EE4B3727A22755BD12233D06865AE5F44F1308C4FA2327E5993125E`、`[0x498BB9,0x498D5A)`=`B86313123DB94476CC13191842B51DAE3B6996C5F46388EB7A96FD89E37D1558`。
- 先行：同日15–16Hのdialog側研究、旧B HANDOFF。**後続訂正**：`B-OFFLINE-20261028-22H-T028-ALTERNATE-RESULT-VECTOR-PAIR-01`は代替CALL `0x434B10`が管理vectorへ追記する処理を明らかにする。二重の新発見として数えない。
- KB_CANDIDATE: `0x434B10`を代替結果sink、`+0x1EEC3C`を条件フィールドとしてVERIFY付き登録候補。現developのREF/辞書はBが変更しない。
- Golden要件: 原作0.67・改変前DAT・同一SAVE/MAP/操作/RNGで、各分岐の到達、実表示、所属/雇用の永続効果、結果処理の順を独立観測。**G4外部戦闘結果のsettlement契約が確定した意味ではない**。
- Next: `0x434B10`の内部と`0x1EEC74`ベクターのconsumer/clear/save、`0x1EEC3C` writerを既存V9・PC owner報告で照合。既拒否対象/保護VAは再解析しない。PC復帰時だけ同ID・SHA・既存PR・安全HOLD21を照合しowner HANDOFFへ一度だけ反映。
