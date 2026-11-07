# 研究E｜T020/T028 第3 selector caller と opaque EAX 受入（2026-10-30 10H JST）
研究ID: E-AUDIT-20261030-10H-T020-T028-THIRD-SELECTOR-OPAQUE-EAX-01
状態: STATIC / NATIVE PE BYTE VERIFIED / SYNTHETIC EXECUTED / VERIFY / NOT READY。旧原作ゲームと新エンジンの実行0、正式READY追加0。
## 出典と正本
PC Desktop Commander Local Compact接続。MASTER、5レーン規約、A-D HANDOFF、REA PROGRESS、dev_lab実装計画、E T018/T019/T020、V9案内を読取専用で照合。
B元研究: B-20261030-1017-T028-THIRD-SELECTOR-CALLER-RETURN-GATE-01。data/T028_THIRD_SELECTOR_CALLER_RETURN_GATE_NATIVE_20261030_10H.md 実バイトSHA256=B2273C621C9B4E1E5A7AFFF4061C85F3809246EDFBADD9EAD8ABF57960E45268。B状態 VERIFY/NOT READY。
原作解析用PE（rea_lab/targets、**原本ゲームとは別の読み取り専用研究用コピー**）2910720B実SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
V9 DBはB出典既確認SHA=2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE。本EでDB再SHA・Ghidra新解析なし。PC標準LATESTのV9昇格完了を仮定しない。
## 新規E独立native確認
PEのセクションRVA変換後、0x447BF0から134Bと0x597BA0から234Bの局所SHAをB記録と2/2一致。
E8 rel32 CALL site→calleeを6/6実バイト確認: 0x447C23→0x597BA0、0x447C2F→0x5AC1A0、0x5682B5→0x597BA0、0x5682C3→0x5AC1A0、0x597BDF→0x49E490、0x597C6B→0x5A8110。
0x447C2Fで selector第1引数は直前0x597BA0のEAX、第2引数は[EBX+0x14]、第3引数はliteral0。第1引数を元Unit型・同一ポインターと決めつけない。
0x597BA0のEAXは上流nonzero・cache nonzero・新規作成・ゼロの4候補を区別。Ghidra void表記のみで戻りレジスタを無視しない。
selector返り0→local flag 0、非0でも走査対象Unit+0x1ADに非zeroがあればflag0。どちらでもなければ既存flag値は未証明で、flag1確定とは扱わない。
## T020 fixtureと限界
E新規JSON 56件（producerとselectorの組合せ48、誤推論を拒否するnegative policy 8）、Python検証器新規56/56 PASS。局所PE窓2/2、E8直接call6/6。失敗例0、原作ゲームテスト0。
旧E09時台合成372件は先行保存報告値。今回は再実行していないため428/428の実行確認とは称しない。fixtureの適合は実ゲームの士気・敗走・破棄・予約数・可視効果を証明しない。
C-NB02 G0合法旧UI、G1同一run直前未改変SAVE SHAと入力、G2実MAP SHA・三陣営・ordered Unit/Troop、G3終戦、G4 World差分を同一ID/日時/旧DAT・EXEのSHAで結ぶ一次証拠が必要。x20 DAT改変・別run RAW・合成fixtureは不採用。DYNAMIC OBSERVED=0、actual Golden PASS=0、strict MATCH=0。
T019新規確定原作矛盾0。GameClear DAT13/TXT2字句scopeのみRESOLVED、script2同名勝者・phase flag・TXT runtime load・gwrite復帰・decide11用途はVERIFY。
## 正式統合・安全・再開
MASTER最終正式checkpoint196/READY596=A115/B229/C136/D116。今回TASK QUEUE34件を直接再集計DONE9/IN_PROGRESS21/VERIFY4。B10研究NOT READYで正式READY統合0、MASTER変更なし。
E新検証器初回PE headerチェックでエスケープしたb'PE\\0\\0'を使用したためAssertionError。E所有コードの当該1行だけbytes((80,69,0,0))へ修正して再実行PASS。分類OTHER/RECOVERED・新安全拒否0。
旧T018表境界/E session-join/T019 XREF/C T026/T032/D T030 TSV/0x5710C0をBLOCKED維持。拒否payloadの再試行・他shell/tool/path/Remote/ZIP迂回0。旧OFFLINE-UNSYNCED・SAFE/HOLD・異SHAソース差の完全照合は未完了。
書込はE所有testsの新規fixture/検証器/本報告/読み戻し証跡のみ。原本EXE/ZIP/DAT/SAVE、A-D、REA、dev_lab、Git/push、Work、設定、スケジュールに書込0。
次は0x447C69 local flag後続consumer、0x597BA0のcache pointer寿命と0x49E490戻りABIをB ownerの新出典で再照合。合法原作同run G0-G1-G2は依然P0、READY化は全証拠/owner/hash/重複/合意審査後のみ。
