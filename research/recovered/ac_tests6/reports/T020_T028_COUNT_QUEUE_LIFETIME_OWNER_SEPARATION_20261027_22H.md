# E-AUDIT-20261027-22H-T020-T028-COUNT-QUEUE-LIFETIME-OWNER-01
[OWNER/STATUS] E/T020（T018受入の負例を補助）。2026-10-27 22時台 JST。STATIC / SYNTHETIC EXECUTED / VERIFY / NOT READY。正式READY新規統合なし。
[PC/SOURCE] Desktop Commander Local Compactオンライン。MASTER・運用規約・A～D HANDOFF・REA PROGRESS・dev_lab IMPLEMENTATION_PLAN・E T018/T019/T020・legacy search_index README/BUILD_MANIFESTを読取。B新規 B-20261027-22H-T028-COUNT-QUEUE-TRANSITION-CLEAR-01、詳細 data/T028_DEATHCOUNT_RECORD_CLEAR_TRANSITION_NATIVE_20261027_22H.md を直接照合。B詳細実バイトSHA256=0D93569856C41550EB7F76AE79BD2E5802567AB1E3FBBA45CC9934F0B4D6D8B5 を新T020テスト内で照合成功。
[SOURCE LIMIT] EXE manifest識別SHA=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。今回は原本EXE実バイト再計算・新Ghidra実行・旧原作実機起動なし。B保存済ASMを二次根拠として使用し、E独自の原本機械語照合達成とは扱わない。
[NEW T020] 21時台に区別済みのdead_event=count writer候補0x49CFB8→0x429A00と、22時台B発見の0x4923BA..0x4923E5の配列生存期間境界を、同一owner/戦闘epoch未証明のまま連結しない負例ゲートへ落とし込んだ。
[STATIC BRANCH] B元資料の0x4923C6 CMP(begin,end)・0x4923C8 JEで空ならskip。非空時0x4923D0→0x417160、0x4923E0→0x415A60、0x4923E5 end=begin（begin+0x1EEFA0/end+0x1EEFA4/cap+0x1EEFA8）。局所的には各0x1C要素のstring析構・論理clear候補であり、capacity解放・表示・死亡数増加・士気変化の証明ではない。
[PROVENANCE SPLIT] producerの[Unit+0x1E0]とtransitionのowner param_1が実体同一かはVERIFY。同じ数値ポインタでも戦闘epoch相違・メモリ再利用を跨いで同一性を推定しない。vector端点から算出した件数は合成候補であり、実死者数・生成件数・Color表示数ではない。
[NEW CODE] tests/t020_t028_count_queue_lifetime_owner_gate_20261027_22H.py。未定義/boolean/負値/逆転範囲/容量越え/0x1C非整数倍/NULL beginなどをfail-closedとし、空配列skip、非空配列のend→begin・cap保持候補、別owner・別epoch、合成owner同値でもREVIEW_ONLYの条件を確認。
[EXECUTION] python -B新規合成19/19 PASS、0 failure、exit code 0。原作旧EXE GamePlayおよびdev実装テストはNOT RUN。実ゲームGOLDEN合格とは無関係。
[T018 GOLDEN] G0合法旧UI＋Spot/開戦入力、G1同一戦闘の直前SAVE実バイト＋操作時系列、G2実MAP/攻防支援三陣営/確定出撃Unit・Troop、G3原作戦闘結果、G4戦略World差分は未充足。DYNAMIC OBSERVED=0、actual Golden PASS=0、strict MATCH=0。戦闘中死亡recordはG2初期出撃名簿に転用しない。
[T019] 新規確定矛盾0。GameClearのDAT13箇所/TXT2箇所の検索scope差はRESOLVED、script2同名優先・phase flag・TXT runtime・gwrite復帰はVERIFY。原作BUGの確定追加なし。
[MASTER] 最終既知正式checkpoint196、READY596（A115/B229/C136/D116）。34Taskは前回確認値DONE9/IN_PROGRESS21/VERIFY4、今回は全履歴独立再集計なし。B22時台研究はSTATIC/VERIFY/NOT READYなのでMASTER統合0、追加READY IDなし。
[SAFETY/SYNC] T018表境界・session-join、T019拒否XREF、C T026/T032、D T030 TSV、禁止0x5710C0/0x58021E等の過去拒否を迂回しない。旧OFFLINE-UNSYNCED成果未統合、owner完全意味dedup未完。E新コード・本報告以外書込なし。MASTER・A-D・REA・dev_lab・原本EXE/ZIP/DAT/SAVE・Git/push・Work・設定・スケジュール変更なし。
[NEXT] 同一合法runのG0/G1/G2実バイトreceiptを優先。T028は合法同一戦闘でproducer ownerとtransition ownerの同一性、string配列の可視reader/処理時相、countとnamedの差を原作側資料に沿って別々に観測する。未検証をREADY/MATCHに昇格させない。
[READBACK RECEIPT] Local Compactの独立read_multiple_filesでE新コード88行/報告14行を全文読戻し2/2。PC上のGet-FileHash(SHA256)でコードB5A7FB1CBC115B903533FCE80EFB27E0C7D0125C8D8ABCD107044AB618AF89AF、報告追記前1B73D2B04AB218F15E730CFF4DCFF048BB35AFFD59B8ADD8E6C576DE6A697E4Aを取得。追記により報告最終SHAは変化する。新安全拒否0、プロセス失敗0。READY追加/原作Golden/strict MATCHは全0。
