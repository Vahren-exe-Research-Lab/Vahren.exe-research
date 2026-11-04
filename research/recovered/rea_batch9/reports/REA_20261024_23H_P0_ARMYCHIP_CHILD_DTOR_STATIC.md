# 迫真戦記 ver0.67｜REA 23時台 P0：ArmyChip子デストラクタの実装境界と所有者未解明の切り分け
研究ID: `REA-LOCAL-20261024-2334-P0-ARMYCHIP-CHILD-DTOR-OWNERSHIP-STATIC-01`
分類: **PC-SAVED / STATIC / VERIFY / NOT READY**。原作ゲーム実行なし、正式REA VERIFIED昇格なし。
原作SHA256: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`（今回再計算一致）。
統合V9 SHA256: `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`（今回再計算一致）。

## 先行成果と新規差分
MASTER、レーン規約、REA README/QUEUE/PROGRESS、syncログ、旧検索README/MANIFEST、V9入口、前回22時台のvector寿命監査を読み取った。
Wave1～5正式64/64は`progress_sync_20261011T153958076Z.json`由来（今回再実行なし）。旧QUEUE/PROGRESSはEPERMによりstale。既存64を今回の件数へ再加算しない。
**前回22時台の既知:** 親 `0x005B09A0` は子ポインタvector領域をfreeするが子を個別に破棄しない。
**今回の新規:** 子自身の仮想デストラクタ `0x005B1310` のwrapperと本体 `0x005B1330` の処理内容、およびE8直接呼出元不在をPE実バイト・V9索引で独立検証。

## 静的証拠：子デストラクタ2段階
- 子vtable `0x0063AE74` の先頭スロットは `0x005B1310`。スロット+0x04は `0x005B13D0`。
- wrapper `0x005B1310` は、site `0x005B1313` から `0x005B1330` を呼ぶ。
- wrapperにはsite `0x005B1320` → free系 `0x005B6BBB` があり、Ghidra擬似Cでは削除フラグのbit0が立つ場合のみ自オブジェクトのメモリを解放する。フラグの全ABIは未証明。
- 内部本体 `0x005B1330～0x005B13CB` は子オブジェクト中の2つのリンク構造を掃除する。Ghidra出力と命令参照の対応は `child+0x94 / +0x98` と `child+0x88 / +0x8C`。それぞれ先頭（sentinel）と要素数と解釈される。
- 本体の直接CALL 4件は `0x005B1359, 0x005B1372, 0x005B13A3, 0x005B13BC` → 全件 `0x005B6BBB`。本体の間接CALLはこの範囲では0件、基底Actionable vptrへ戻す命令も確認。
- 上記4件は子内部のリンク要素とsentinelの解放に対応するもので、**親の子ポインタvectorそのものを解放する証拠ではない**。
- 親本体 `0x005B09A0～0x005B0A4B` の6件のCALLは全てfree系であり、子デストラクタ呼出はない（22時台結果を独立再照合）。

## 直接CALL索引の否定証拠と限界
統合V9 `native_callsite` のE8_DIRECT_CALLでは `0x005B1310` への直接callerが**0件**。`0x005B1330` への直接callerは `0x005B1313` の**1件**だけ。
ただし子のvtable先頭は `0x005B1310` なので、間接仮想CALLで解放される可能性がある。E8が0件というだけで「未使用」「メモリリーク確定」とは言えない。
また子側の2つのリンク構造をfreeすることは、オブジェクト本体のfree完了とは別段階。再実装時に一律 `delete` や親による全件破棄を固定しない。

## 独立検証・進捗
監査スクリプト `REA_20261024_23H_P0_ARMYCHIP_CHILD_DTOR_AUDIT.py` は原作PE byte/関数範囲のCapstone全命令分解/機械語E8宛先/V9直接参照/SQLite quick_check/擬似C存在とSHAを照合。
**29/29 PASS（初回1.717秒、保存用実行1.69秒）。** この数字は検査項目数であって解析済み関数数ではない。
`info/pseudo/assembly/callers/callees`の新規正式5種セット=0、REA正式VERIFIED +0、TODO/VERIFY/BLOCKEDの正式書込差分=0/0/0。対象5関数のV9 verified_abi=0。
原作ゲームGolden PASS=0、strict MATCH=0、完全複製率=未測定。新規Ghidra/REA/ゲーム実行0。
PCオンライン、read-only検索利用。事前active.lockなし、Java/Ghidraプロセス未検出、空き物理メモリ約14.95GiB。PC総CPU負荷・研究全体の時間は未計測。
今回の一時的な `python -c` 引用符構文エラー（調査表示用、原本や成果物未変更）と、新規ファイル存在確認のENOENTは**安全拒否ではない**。その後専用監査スクリプトで検証成功。
過去安全拒否の `0x004BC9C0` 検索CLI、0x5710C0..0x571500、Wave6、REA export は再試行・迂回なし。

## 次回再開位置 / Golden設計（NOT RUN）
P0: `0x005B1310` への実際の**間接仮想デストラクタ呼出元**を、生成・登録/イベント解除・親消滅の所有権経路で追う。子が独立した所有者へ移管される証拠、vptr変更・再配置、vector削除の正常経路を検証する。
Golden想定: 子0/1/複数件で、親vector確保・子0xA4生成・子内部2リンク構造生成/破棄・子自体の解放・親vector領域の解放を**別々**に観測する。例外/途中終了では二重freeや未解放の疑いを別項目で検査する。
正式統合は最新MASTER/owner/QUEUE/PROGRESS・証拠ハッシュ・競合チェック後のみ。原本・他レーン・Git・Work・既存スケジュールは変更しない。
