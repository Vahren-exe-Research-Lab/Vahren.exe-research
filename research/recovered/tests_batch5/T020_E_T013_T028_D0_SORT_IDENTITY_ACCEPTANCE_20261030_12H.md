# 研究E 12H｜T013/T028 +0xD0管理値と+0xE4 sortキーの分離受入
研究ID: E-AUDIT-20261030-12H-T020-T013-T028-D0-SORT-IDENTITY-01
判定: STATIC / NATIVE BYTE WINDOWS VERIFIED / SYNTHETIC EXECUTED / VERIFY / NOT READY
## 出典・照合
B owner: data/T013_T028_BATTLE_D0_PRODUCER_SORT_COMPARATOR_NATIVE_20261030_12H.md
B実バイトSHA256: 552F1ED1E478C0CBFC803DA5FA4A7F6EF2856F30E03FD7A7D6D6AA3D2B2674FD
B状態: B-20261030-12H-T013-T028-D0-CALLER-SORT-CLAMP-01 / VERIFY / NOT READY。新READYなし。
元PE研究コピーSHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
原PE局所窓0x51EF80+64、0x5146F0+67、0x447D52+319のSHA3/3一致。
直接E8 CALL 0x51EF8F -> 0x447810、0x51EFA9 -> 0x47BB50の相対先2/2一致。
B保存ASMによれば caller ECXをcalleeがESI/stack保存し、後続EBX+0xD0 writerへ使う。これは当該caller内のmanager同一性に限定。
直後の配列sort callbackはUnit+0x1C8先の+0xE4 signed less-than。+0xD0を比較キーとはみなさない。
+0xD0は低得点の有限・ordered値に2.0下限、条件不成立では1000000.0 sentinel。NaN/x87例外は未確定。
## T020独立検証
Python: tests/t020_e_t013_t028_d0_sort_identity_gate_20261030_12H.py
Fixture: tests/T020_E_T013_T028_D0_SORT_IDENTITY_CASES_20261030_12H.json
fixture SHA256: 121124FFB00294044E64CD984FA065120460447D3A8E88F21B1F1B1EC90F8611
32合成分岐+8 signed-int32端点+8過剰推論防止=48/48 PASS (Python -B --init exit0)。
このPASSは小さな合成受入モデルの成立のみ。callbackのNULL耐性、tie安定性、全consumerの同一性、実ゲームでの数値・sort順はNOT RUN。
## T018 / T019 / MASTER
G0合法な旧UI開戦/操作、G1同一戦闘の未改変直前SAVE SHA・入力、G2真MAP・攻守援軍と順序付出撃Unit/Troop、G3終端、G4World差分を同じ戦闘runで要求。
2026-10-22のKARATE_X20 test DATがGoldenへ混入しないこと。旧原作Gameplay DYNAMIC OBSERVED0 / actual Golden PASS0 / strict MATCH0。
T019新確定矛盾0。GameClear DAT13/TXT2は字句範囲差RESOLVED、script2/phase/TXT runtime/gwrite/decide11はVERIFY。
MASTER最新正式checkpoint196/READY596(A115/B229/C136/D116)、TASK QUEUE現物34件(DONE9/IN_PROGRESS21/VERIFY4)。B12H NOT READYなので正式統合0、MASTER編集0。
B11H拒否 B-RC-20261030-1115-T028-T013-APPEND-SAFETY-01 はB owner要約3件未保存でBLOCKED維持、代理追記なし。
旧T018表境界/E session join/T019 XREF/C T026/T032/D T030 TSV/0x5710C0は拒否迂回禁止を継続。旧OFFLINE-UNSYNCEDの完全重複照合は未完。
次: T013の4箇所+0xD0 consumerが同一manager・同一frameか、+0xE4 producerと合法G0/G1/G2の同run一次証拠を別途確認。
原本、A-D/REA/dev_lab/Git/Work/設定/既存automationを変更しない。
