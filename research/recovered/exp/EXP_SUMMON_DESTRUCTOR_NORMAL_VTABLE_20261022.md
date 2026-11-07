# EXP-LIFETIME-20261022-01｜通常型BattleUnitの仮想破棄関数から召喚経験値R解放への接続

- 対象: 原本ver0.67 SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。原本EXEコピーと既存SQLiteをread-only照合。
- 状態: STATIC_NATIVE / STATIC_CALL_GRAPH / VERIFY / GAMEPLAY_NOT_RUN、B正式READY0、E統合0。
- 新しい差分: 過去CP12で見つかった Rの解放関数連鎖を、**実際の通常型Unit constructorで書かれるvtable[0]**へ結合した。過去の解放関数単体の発見を再計上しない。
- 証拠: `EXP_SUMMON_DESTRUCTOR_VTABLE_20261022.json` PE native 7/7、直接CALL4/4、vtable slot0値一致。
- 追加チェック: `EXP_UNIT_VTABLE_WRITER_SCAN_20261022.json`。0x56F880..0x570AE7のCapstone 1,121命令のうち、直接`[EBP]` base vptr writeは0x56F8DDの1件のみ（ヘルパー内の間接書込は対象外）。

## 静的に裏付けられたチェーン
1. `0x56F8DD MOV [EBP],0x0063A9E4`：0x56F880が構築する通常型Unitのvptrを設定。
2. PEの `[0x0063A9E4 + 0]` = `0x00570C90`：slot0はdeleting-destructor形関数。
3. `0x570C94 CALL 0x543E00`：本体の片付けを実行。flag bit0で別のthis自体のfree分岐（0x570CA1）あり。したがってfreeは全呼出で一律ではない。
4. `0x543F04 LEA ESI,[EBP+0x1E4B4]`：当該BattleUnit内の召喚UnitData cache treeが片付け対象。
5. `0x543F21 CALL 0x5450C0`→`0x5450DA CALL 0x5454D0`：treeのノード解放経路。
6. `0x545525 CALL 0x4591F0`：node+0x28の埋込UnitData payloadを破棄。その後ノード解放へ進む（旧CP12と一致）。

## 誤認回避
- 旧資料の `0x55B010 → 0x55A000 → 0x543E00` は**別のdeleting-destructor風入口**。今確認した通常型のvtable[0]は `0x570C90`。両方を同一アドレスと混同しない。
- [確定] **もし通常型Unitがslot0で破棄されるなら、そのUnitが持つR cache treeも解放対象になる**。
- [未確定] 原作戦闘終了0x493630→特定Unitのslot0へいつdispatchするか、すべての召喚元が同じvtableか、決着前にRのEXPを永久Unitへ移すか。
- この経路だけで「召喚獣の獲得EXPは必ず失われる」「元へ転送されない」と断定しない。
- 新しい外部戦闘EXE案では native Rポインタがdestructor後に無効になる前提のライフタイム受け渡し設計が必要。ただしstable ownerの正式native契約は未作成。
- 次の調査: side unit vector +0x48/+0x58との実unlink/解放の順、native battle exitでのvirtual slot0到達、Rと戦略UnitDataの別参照。

