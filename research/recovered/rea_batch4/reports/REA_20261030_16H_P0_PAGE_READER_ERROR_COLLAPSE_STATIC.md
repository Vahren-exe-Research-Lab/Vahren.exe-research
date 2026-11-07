# 迫真戦記 REA｜2026-10-30 16H｜Ogg読み込みエラーのEOF正規化
研究ID: `REA-LOCAL-20261030-16H-P0-OGG-READER-HARDERROR-EOF-COLLAPSE-STATIC-01`
状態: **PC-SAVED / STATIC / VERIFY / NOT READY**。原作実行・Golden未実測。15Hのページ更新status表を原因別に深掘りしたもので、旧成果を新規計上しない。

## 新規P0静的発見：下位I/Oハードエラーが上位では正常EOFになり得る
基底のOggページ取得ヘルパー`0x005CEB90`は、`ESI`から入力オブジェクトを取得し、callback `ESI+0x2C0`を呼び出す。この関数のGhidra疑似Cは`unaff_ESI`を示し、通常のcdecl引数として直接流用してはいけない。
- `0x005CEC04` callbackポインタ無し、`0x005CEC49` callbackが負数、`0x005CEC53..5B` callback 0かつerrno非0 → `0x005CEC72..7D`で64bit `-128`。
- `0x005CEC0D` sourceポインタ無し、またはcallback 0かつerrno=0 → `0x005CEC5D..68`で64bit `-2`（EOF扱い）。
- `0x005CEC69..71`は上限に達したときの64bit `-1`。`0x005CEC7E..99`は成功時にバイト位置を更新し、64bit位置を返す。

**新規の呼出側非対称:** `0x005CF010`初期ヘッダ読込では`0x005CF035`後の`0x005CF03D..45`で64bit `-128`を個別判定し、そのまま返す。一方`0x005CFA10`ページ更新中の`0x005CFB23`では、`0x005CFB2B/2D`で`EDX<0`の全結果を`0x005CFDC4`へ分岐させ、`-2`を返す。よって下位`-128`も当該ページ読込経路では`-2`に統一され得る。
さらに既存15H確認の`0x005D0FB0`再生側は`0x005D1002/05`で`-2`を`0x005D12CF`の戻り値0へ変換する。すなわち、**callbackハードエラー→ページ更新-2→再生側0(EOF)**という条件付きの静的到達経路が成立する。

## 既存研究との差分と実機未確認点
15Hはページ更新`-2`の存在と再生/シークでの非対称処理を記録済み。16Hで追加したのは、`0x005CEB90`の`-128/-2/-1`発生原因と、初期ヘッダ処理では保存される`-128`がページ更新では`-2`に潰れるという**I/Oエラー区別の欠落**。
正常なOgg音声・通常のファイル読み込みでcallback失敗が実際に発生することは示していない。原作不具合/音切れ/無限ループは断定しない。後続`0x005D0CC1`シーク経路と他11 E8呼出サイトの全エラー処理は未監査。間接呼出も未証明。
再実装の比較Golden案: ヘッダ初回読み込み成功/失敗、ページ更新直前にcallbackが負数、0+errno非0、0+errno=0を返す各条件を分離し、直接return値と上位EOF処理を記録（原作実測PASS 0）。

## 検証方法・前回境界
出典は同一SHA研究専用PE `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、V9 SQLite `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`。
PC接続正常、active.lockなし、Java/Ghidra/REA競合プロセス未検出、空きメモリ約14.99GiB（確認時）。CPU負荷および研究全体の経過時間は不明。V9非破壊verifyとSQLite quick_checkがPASS。初回監査44/47は`0x005D0FFC`から逆アセンブルして命令途中を開始点とした監査窓の誤りであり、`0x005D0FD0`へ修正後**47/47 PASS（0.9716秒）**。
V9のinfo/pseudo/callers/calleesと同一PEの局所ASMを独立照合。REA正式info/pseudo/assembly/callers/calleesファイル5種の取得ではない。既存正式STATIC VERIFIED **64/64**を維持、新規正式VERIFIED **0**、5種完備 **0**、TODO/VERIFY/BLOCKED正本書込差分 **0/0/0**。Golden実測PASS **0**、完全複製率未測定。
本実行でREA/Ghidraの新規解析・ゲーム起動・原本変更なし。MASTER、QUEUE、PROGRESS、既存RUN、他レーン、Git、公開先、スケジュールは不変更。owner配下の16H固有ファイルのみ新規保存し、別プロセス読み戻し・SHAを保存する。

## 次回再開位置
優先`0x005D0B60`のcall site `0x005D0CC1`が受け取る`-128/-2`の分岐先`0x005D0D89`を照合する。次に`0x005CF010`の別読込サイト`0x005CF17D/0x005CF2AA`のerror分類を比較。ページ取得成功と失敗を分離してエラー伝播表へ追加する。
