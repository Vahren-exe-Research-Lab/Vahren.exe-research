# 研究E｜T020 T028退却予約減算と通知gateの独立受入（2026-10-30 04H JST）
研究ID: `E-AUDIT-20261030-04H-T020-T028-NOTIFY-GATE-DECOUPLING-01`
状態: STATIC SOURCE-PINNED / SYNTHETIC EXECUTED / VERIFY / NOT READY。旧原作EXE・新エンジン未実行。
## 出典・同一性
- B owner: `B-20261030-0417-T028-RETREAT-NOTIFY-INDEPENDENT-GATE-01`、`data/T028_RETREAT_NOTIFICATION_POSTRELEASE_FLAG_GATE_NATIVE_20261030_04H.md`。E独立読取済み実バイトSHA256 `7A56916D8FA5540426BB178F5272295DAE5F353F826C8AD2ADA8F45410190774`、B状態 VERIFY/NOT READY。
- Bが報告した原作PE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、PE局所窓SHA `78061E1E994CE7EB210B5640E27611EF06B577FD945401D7FED0ED014696820B`。これらのPEバイトはE本回では独立再ハッシュなし。
- Ghidra現行状態は2026-10-29更新 `rea_lab/headless_analysis/00_START_HERE_ACTIVE_RESEARCH.md` と `CURRENT_ACTIVE_RESEARCH_STATE_LATEST.json` で V9選択を確認。DBのE独立再ハッシュは未実施。旧V3選択という古い案内へ巻戻さない。
## T020の新規受入契約（B静的記録のモデル化）
- `0x495578` でSpot参照一致時のみ `0x495580` のSpot+0xB8減算呼出経路。一致・不一致はその後の通知判定と独立。実メモリ値・下限保証はVERIFY。
- `0x495586` と `0x49558C` はESI+0x77またはESI+0x75の非0を要求、`0x495596` はstack+0x6F非0を要求。どちらか不成立なら `0x49516F` の次要素経路へ。
- 条件を満たす場合、`0x4955A8` のmanager mode==1側は `0x4956AA CALL 0x52CF50`、その他側は `0x49579E CALL 0x434B10` (ECX=10)。これはCALL分岐であり、表示・通知配信成功ではない。
- CP932 string `decide11` と `$$$は###へ退却しました` はB原PEの候補文字列。どの経路で実際に表示されるか、APIの意味、producerと有効な入力状態はVERIFY。
- 静的gate入力が取得不能の場合はUNKNOWN/INELIGIBLEとし、通常UIの撮影から内部flagや正確なSpot+0xB8値を捏造しない。原作GAMEPLAY証明には使わない。
## T020 合成回帰
- `tests/t020_e_t028_postrelease_notify_gate_20261030_04H.py` と `tests/T020_E_T028_POSTRELEASE_NOTIFY_CASES_20261030_04H.json` を新規作成。source SHA fail-closed、必要VA marker照合、fixture再現性・ID一意性・truth-table分布検証。
- 32件のSpot一致/不一致×flag77×flag75×stack×modeの全組合せと14件の数値境界・欠落・型エラー・Golden誤認負例の合計46件を実行し46/46 PASS。
- 旧7検証器（21H,22H,23H,00H,01H,02H,03H）をread-only再実行し8+18+21+18+22+28+30=145/145 PASS。新旧合計191/191合成回帰、8/8 runner exit0。出典source pin/マーカー検証は別でありGameplay PASSへ加算しない。
- 数字の訂正: 02H報告の旧107件は21Hの8件を含まない部分集計で、旧7本を全て数えると115件、03Hで145件、今回191件。回帰を重複追加したわけではない。
## T018・T019・MASTER
- C-NB02 G0には通常UIの旧原作戦闘開始の限定的既存観測記録がある。しかし同一run G1直前無改変SAVEのSHA＋入力、G2 ACTIVEの実MAP/三陣営/ordered Unit/Troop、G3結果、G4 World差分は不足。正式認定 DYNAMIC OBSERVED=0 / actual Golden PASS=0 / strict MATCH=0。
- T019の新規確定矛盾0。GameClear DAT13/TXT2は「検索範囲差」だけRESOLVED、script2優先/phase flag/TXT実load/gwrite/decide11用途はVERIFY。
- MASTER最終正式checkpoint196、READY596(A115/B229/C136/D116)を読取、今回新規READY統合IDなし(0件)。34 Taskは今回TASK QUEUEの34行を再集計しDONE9/IN_PROGRESS21/VERIFY4。
## 安全・同期・次回
- B04H ownerはVERIFY/NOT READYでMASTER正式統合しない。旧E T018表境界/session-join/T019 XREF、C T026/T032、D T030 TSV、禁止0x5710C0等はBLOCKED据置。元拒否操作の迂回なし。
- 旧OFFLINE-UNSYNCED全件のowner/ID/意味重複・READY照合はOPEN。原本ZIP/EXE/DAT/SAVE、A-D/REA/dev_lab、Git、Work、設定/他automationには変更なし。
- 次の優先はBのESI+0x75/+0x77とESP+0x6F producer・2 sinkと `0x49516F` loopの一次証拠、同一戦闘G0/G1/G2の合法原作receipt。今回追加fixtureはstatic/syntheticのみで実機未実施。
