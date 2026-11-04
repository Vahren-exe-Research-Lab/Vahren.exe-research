# 迫真戦記 REA｜2026-10-29 23H OggDecoder仮想Readの到達・復号負値とEOFゲート
研究ID：`REA-LOCAL-20261029-23H-P0-OGG-VTABLE-ERROR-GATE-STATIC-01`
分類：**PC-SAVED / STATIC / VERIFY / NOT READY**。ゲームGolden実測0、正式REA新規VERIFIED0。
## 出典・既存研究の差分
MASTER、5レーン規約、REA README/QUEUE/PROGRESS、既存RUN/22H evidence・readback、2026-10-26 04H worker・05H EOF研究を先読した。既存正式進捗は `logs/progress_sync_20261011T153958076Z.json` で64/64。古いQUEUE/PROGRESSの15/16表示はEPERM後のstale。
隔離EXE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、現行V9検索DB SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE` を再計算一致。SQLite quick_check=ok。旧search.sqlite不存在は10/29整理済であり障害ではない。
22Hの `0x00501F10` 負値転送量、10/26のworker `0x0050249E/0x0050252E` 仮想+4、およびEOFラッチの読み手は**既知**。これらを新規発見として二重計上しない。
## P0追加静的証拠：仮想関数テーブルの原作実体
`0x006395CC` から連続5 DWORD：`+0x00=0x00501DF0`、`+0x04=0x00501F10`、`+0x08=0x00502000`、`+0x0C=0x00502020`、`+0x10=0x00501EB0`。直前 `0x006395C8=0x0063E678` はRTTI情報ポインタ候補。V9 refs-to `0x00501F10` のDATA参照 `0x006395D0` と、PE再配置参照 `pe-to` が一致。
`0x00501E7E MOV [ESI],0x006395CC` はコンストラクタ `0x00501E20` に存在し、上位 `0x004BEAD9 CALL 0x00501E20` と接続。`0x00502284 MOV [ESI],EDI` はworker保持先のdecoderオブジェクトを更新する。
worker `0x00502483/85/87`: `[ESI]→[decoder]→[vptr+4]`、`0x0050249E CALL EDX`。後半 `0x00502513/15/17→0x0050252E CALL EAX` も同スロット。`0x00502395→0x005023A0` の初期fillも+4。**OggDecoder型vptrが維持された条件では、workerの仮想Readは0x00501F10に解決**する。静的参照が実機のvptr値を証明したわけではない。
## P0追加：-3戻り値時の内部出力とworker側分岐
22Hの条件（下位復号が-3を返す）を取ると、`0x00501F54` でEOF out=0、`0x00501F5D` で要求PCM領域をゼロ初期化済み、`0x00501F9D JNE 0x00501FBF` → `0x00501FC2 ADD EDI,ESI` → `0x00501FC6 JAE 0x00501FDF`。初回EDI=0、ESI=-3なら `EDI=0xFFFFFFFD`、`0x00501FE6` でout countへ書き、`0x00501FEA` でAL=1。ただしEOF out=0を維持する経路。
workerはReadのEAX/AL成否を直接判定せずUnlockへ進む（`0x005024BD` または `0x0050254D`）。その後 `0x005024C4/0x005024C8` または `0x00502551/0x00502555` が**EOF=0なら`0x00502565`へ飛ばす**。従って、この条件では異常countがスタックout変数に発生しても、`stream+0x54`への保存 `0x0050255E/0x00502562` は通らない。
これは22Hの「巨大countが上位で利用され得る」という疑義の**worker経路に限った絞り込み**であり、他の仮想呼出元・EOF破損時の振舞いは未確認。ゼロ初期化済みのPCM領域をUnlockするので、負値が直接buffer sizeを書換/越境アクセスしたとは断定できない。短い無音や回復の実測も未実施。

## 監査・正式判定と負荷
REA独立監査 `REA_20261029_23H_P0_OGG_VCALL_ERROR_GATE_AUDIT.py`：**52/52 PASS / 1.099秒**、 `REA_20261029_23H_P0_OGG_VCALL_ERROR_GATE_EVIDENCE.json` をexclusive作成。孤立した検索CLIの `related` は現行V9で未対応（引数エラー）。直ちに許可された `refs-to/pe-to/flow-callers/function` で調査し直した。安全拒否ではない。疑似Cの型推定は原作ABIの確定に用いない。
今回の5種確認水準：info=V9 INDEX / pseudo=V9 INDEX / assembly=隔離同SHA PE局所Capstone / callers=V9 INDEX（E8直接0・VTABLE DATA 1）/ callees=V9 INDEX。REAの独立した正式5種証拠新規完備 **0**、新規正式VERIFIED **0**、既存STATIC **64/64維持**。正式TODO/VERIFY/BLOCKED差分 **0/0/0**。独立の新規VERIFYはworkerのOggDecoder型到達、異常out countの他のconsumer、破損パケット入力時の実機PCM結果。
原作実機Golden PASS **0**。完全複製率 **未測定**。当該調査はSTATIC_ONLYでありクラッシュ・音声欠落・メモリ破壊の確定報告ではない。
PCオンライン、開始時空きRAM **約12.26GiB**、`active.lock` 不在、Java/Ghidra先行プロセス検出なし。CPU負荷と総研究時間は未測定。新REA/Ghidra/ゲーム起動は0。安全拒否VA、Wave6、REAエクスポートは未試行。
保存はREA所有`rea_lab/decomp_task`のみ。原本ZIP/EXE/SAVE、MASTER、QUEUE、PROGRESS、既存RUN、他レーン、Git、公開先、スケジュールは無変更。別研究のOFFLINE-UNSYNCED成果は未統合のまま。
## 次のP0再開位置
1. `0x00501F10` の仮想callを持つ`0x00502330` 初期fill（`0x005023A0`）とworker二相（`0x0050249E/0x0050252E`）で、-3→count/EOF→Unlock引数の作用を別々に照合。初期fillはEOF outがNULLのためworkerとは別の境界。
2. `0x005023E0` 内のUnlock引数、`0x00502580` のEOF消費、`0x004BF780` と最終転送の呼出条件を限定調査し、巨大countがその他の領域へ流出しないことは未証明として保持。
3. 原作Golden候補：正常OGG、途中欠損packet、非loop EOF、loop EOF、Lockが複数領域を返す条件の順。観測結果0のまま実ゲーム実行を装わない。
出典確認は`search_unified_v9_20261023.py` の `function 0x00501F10/0x00501E20/0x005023E0`、`refs-to 0x00501F10/0x006395CC`、`pe-to 0x00501F10`、`callers 0x00501F10`、および同SHA PE静的ASM。保存後の独立読戻しを別処理で記録する。
