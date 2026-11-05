# 迫真戦記E｜T028 Spot予約カウント・解放境界をT020合成受入へ追加（2026-10-29 23H）
研究ID: E-AUDIT-20261029-23H-T020-T028-RESERVATION-COUNT-RELEASE-01
分類: STATIC / SOURCE PINNED / SYNTHETIC EXECUTED / VERIFY / NOT READY。原作Gameplay NOT RUN。
## 根拠・今回の独立差分
- B-20261029-2315-T028-RETREAT-SPOT-RESERVATION-RELEASE-01はB所有でSTATIC/INFERRED/VERIFY/NOT READY。詳細data/T028_RETREAT_SPOT_RESERVATION_RELEASE_NATIVE_20261029_23H.mdの実SHA256は E2A056108081F370199A0E7990979277D4D8B19269EBD979EAE69D5A51DD205D。
- 既B22H detailの実SHA256 D2E746997C492CE294EFF9BD9B61D7D45C14DBF5FE7030DAC02C624BE5ED26F6、E22H既存コードの実SHA256 9A6E36AD65892FD7F708AE804C452418D0D336CA36D18AA69601638ABFD18DA4と合わせ新検証器が実バイト3/3固定。
- 0x597A50計数は全linked nodeではなく、resolverが非NULLを返し、その対象のbyte+0x78が非零のときだけ局所countを加算する原生ASM条件（countモデルはこの条件だけ）。
- 0x495578のEBXと処理後Unit+0x1B4比較が等しい経路だけ0x495580 DEC [EBX+0xB8]へ到達する。早い時点のUnit参照と処理後比較を混ぜない。
- B21Hの0x56832F INCとB23HのDECは逆向き局所writerだが、真の予約寿命、元の値、解放完了、負値/zero、競合副作用、UI・セーブ挙動はVERIFY。単独DECからSpot退却成功や全体の予約releaseを確定しない。
## E所有T020合成試験
- 新規 tests/T020_E_T028_RESERVATION_COUNT_RELEASE_CASES_20261029_23H.json：count11件、release10件の計21件（合成のみ）。
- 新規 tests/t020_e_t028_reservation_count_release_gate_20261029_23H.py：上記3ソースをSHA256で固定し、unknown resolver/byte範囲/boolean混同、NULL/pointer不一致、比較site到達、0/INT_MIN境界を検査。
- PC python -B 新規SOURCE_PINS 3/3 PASS、SYNTHETIC_COUNT_RELEASE 21/21 PASS。旧22H容量回帰も別runでSOURCE_PINS 3/3 PASS・18/18 PASS。原作・新エンジン未実行。
## Golden、T019、正本、権限
- C-NB02原作G0は限定資料のみ。同一runのG1直前未改変SAVE+入力、G2 ACTIVEの実MAP/三陣営/順序付き出撃Unit/Troop、G3/G4を含む実証連結は未充足。x20テストDATを未改変原作と混同しない。Golden認定DYNAMIC OBSERVED0、actual Golden PASS0、strict MATCH0。
- T019確定新矛盾0：GameClear DAT13/TXT2 scope RESOLVED、script2/phase flag/TXT実読込/gwrite/decide11 VERIFY。
- MASTER正式cp196、READY596（A115/B229/C136/D116）は前回正式値。34Task DONE9/IN_PROGRESS21/VERIFY4も旧値（今回全件再集計なし）。B23H NOT READYにつき新規正式統合IDなし、MASTER未編集。
- 旧T018表境界/E session-join/T019 XREF/C T026/T032/D T030 TSV/禁止0x5710C0等はBLOCKEDのまま。新規安全拒否0、迂回0。旧OFFLINE-UNSYNCED完全照合未了。
- E所有testsだけ新規保存。原本EXE/DAT/SAVE/ZIP、A-D/REA/dev_lab、Git/push/Work/設定/スケジュールの変更なし。
## NEXT
原作合法旧UIで同一戦闘G0/G1/G2一次receiptが得られた場合のみactual Goldenへ進める。B側では0x598450副作用、0x467DE0戻りの+0x78型、0x495580前後の予約寿命・カウンタ有界性が次のVERIFY。