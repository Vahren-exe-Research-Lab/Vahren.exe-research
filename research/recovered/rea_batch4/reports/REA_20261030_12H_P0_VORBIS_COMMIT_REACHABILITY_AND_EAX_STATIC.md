# 迫真戦記 REA｜2026-10-30 12H P0 Vorbisフレーム消費の到達性・戻り値ABI
研究ID1：`REA-LOCAL-20261030-12H-P0-VORBIS-COMMIT-STABLE-INVARIANT-STATIC-01`
研究ID2：`REA-LOCAL-20261030-12H-P0-OGG-WRAPPER-EAX-FORWARD-ABI-STATIC-02`
状態：**PC-SAVED / STATIC / VERIFY / NOT READY**。ゲーム実測PASS=0、完全複製率未測定。
## 前回との差分・新規結論
11Hの`0x005D5790`未検査return・`0x005D128D`呼出は既知で二重計上しない。今回の新規点は、**通常の正数復号経路では、フレーム消費ガードの-131が安定状態の下で到達不能になる不変条件を、実命令・呼出関係で結んだこと**。
`0x005D5730`の`0x005D573C/3F`と`0x005D5741/44`は0≦cursor<endを確認。 `0x005D5776/79`はremaining=end-cursorを返す。`0x005D0FB0`は`0x005D0FE1`で同helperを呼び、`0x005D1046`で要求バイト数をframeBytesで符号付き除算、`0x005D104C..53`で min(remaining, requestedFrames)をEBXに保持、`0x005D1055/57`で正値のみ復号へ進む。
`0x005D128B/8D`は同じEBXで`0x005D5790`へcommitし、その内部の`0x005D57A0/2/5`は cursor+count<=endなら成功。`0x005D12EC/EE`でラッパー`0x005D12E0`がcallbackとその引数を両方0としているため、**通常呼出経路に限り、任意callbackによる中途状態変更はない**。
不変式：安定した0≦cursor<end≦INT_MAX、正のframeBytesと正の要求数なら、0<count=min(end-cursor,requestFrames)≦end-cursor、よってcursor+count≦end。合成境界10021組がこの関係を満たした。11Hの「消費失敗も戻り値未検査」は一般的な機械語構造として残るが、**通常安定経路で必ず起きる問題とは扱えない**。
## 追加ABI照合
V9擬似Cは`0x005D12E0`をvoidとしている。しかし実機械語では`0x005D1303 CALL 0x005D0FB0`後、`0x005D1308 ADD ESP,0x24`、`0x005D130B POP EBP`、`0x005D130C RET`でEAXを書き換えない。呼出元`0x00501F91 CALL 0x005D12E0`の直後`0x00501F96 MOV ESI,EAX`が戻り値を受け取る。このため**Ghidra void表記は実際のEAX戻り値伝播を表現しない**。負の復号戻り値も上位へ伝わりうる。
## 論証の限界と次回
他スレッドによるカーソル変更・破損メモリ・未検証の間接呼出先・異常frameBytesはこの証明の前提外。特に`0x005D0B60`はもう1つの`0x005D5790`呼出元（`0x005D0E17`）なので、次回はここでのcountとsigned比較をP0にする。`0x005CFA10`によるポインタ/状態更新も照合する。原作11,025Hz音声のGolden、DirectSound実測・EOFも未実行。
## 取得・監査・保全
出典：同一SHA研究コピーPE `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、統合V9 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`、既存11H報告/証拠、既存sync `logs/progress_sync_20261011T153958076Z.json`。V9 quick_check=ok、旧正式STATIC VERIFIED=64/64（Ghidra5種の既存証拠）。
新規独立PE/V9監査 **52/52 PASS（0.9722秒）**、EAX伝播ABI監査 **13/13 PASS**。監査52件のチェックキー`stable_state_commit_nonfail_10036`は**命名のみ誤り**で、JSONの`model_sample_count`の正しい値は**10021**。証拠JSONは訂正のため上書きせず、本注記で訂正する。
新規正式REA5種完備=0、正式VERIFIED追加=0、正式TODO/VERIFY/BLOCKED書込差分=0/0/0、原作Golden=0。5種類についてinfo/pseudo/callers/calleesはV9既存、assemblyは今回局所PE照合。ABIは正式登録されていない。
PC接続正常、調査前active.lockなし、Java/Ghidra/REA競合なし、確認時空きRAM約15.76GiB。CPU負荷と全作業時間は不明。新Ghidra・REA・ゲーム起動なし。原本・MASTER・QUEUE・PROGRESS・既存run・他レーン・Git・スケジュール無変更。
保存先はREA所有`rea_lab/decomp_task/`のみ。旧11Hの到達性懸念は条件付きに狭め、正式VERIFIEDへ昇格しない。読戻しは別プロセスの証跡を参照する。
