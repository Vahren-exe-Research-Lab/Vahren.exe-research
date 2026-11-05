# REA T014 通常セーブ writer: stream正常/異常時のWriteFile bytecount由来（2026-10-11 11時台 JST）
状態: CONFIRMED-SAVED-ASSEMBLY（0x460000の局所データフロー）。実行時値・上位エラー制御・保存結果はVERIFY。新規Ghidra/REA実行0。
対象: 既存run 20261009T212627835Z / VA 0x460000 / T014 / 保存記録source SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。今回再hashなし。
info: ev_76fca377cfc1ee6b6dd225934568ef4fb94e52cc359d35beff1ccb7ef68d99c3
pseudo: ev_06e5a34750f37c054b3f916ca1d135ab52b3b62b35043ac84ffc8b0a668e05c4
assembly: ev_fec99c35153c8902d10879722c3a8fcb90bcdd434f62a9dedd7878e352529394
callers: ev_91099310a072569d892f9a238b2b7849ecf367b30cd5bbcd0c8fbb0f74bc7724
callees: ev_3ed77f73bd20825ba6b7b67779b97a50404d10e858d64bc85630b7d585c0a0a0
## 増分: 直近のstream fail-state監査からWriteFileへ運ばれるbyte countの構築元を明示
- 0x4605EA..EFの(TEST state & 0x06)が正常なら、0x4605F1..60Aでvtable+0x28を呼び、0x46060CでEAX=[ESP+0xC4]、0x460613でEBX=[ESP+0xBC]を取得する。
- 異常なら0x46061CでECX=[0x6098B4]、0x460622でEBX=[0x6098B0]、0x460628でEAX=0。0x46062AでECXを[ESP+0xC0]へ、0x460631で0を[ESP+0xC8]へ格納する。正常側の仮想関数は通らない。
- 0x460638 ADD EBX,EAXで両分岐は合流。すなわちbytecount候補は正常側が[ESP+0xBC]+[ESP+0xC4]、異常側が[0x6098B0]+0（32-bit加算）となる。
- 0x460645の0x42A340と0x46065Cの0x427040を経て、0x460684 PUSH EBX / 0x460687 CALL [0x609080]。import解決済みWriteFileのnNumberOfBytesToWriteにそのEBXを渡す。書込bufferは0x460661..676のinline/heap選択結果、file handleはCreateFileA戻りEBP。
- pseudoは異常側に0xffffffff sentinelを表示するが、assemblyはglobalメモリからのロードである。実行時のglobal値が常に-1だと断定しない。特に『異常時に4GiB近いbytecountを実際に要求する』との断定はしない。
- WriteFileの直後0x46068D PUSH EBP / 0x46068E CloseHandle。戻り値やbytesWrittenを当該局所経路で比較する命令は見えない。
## 未確定/次回優先
- [VERIFY] globals 0x6098B0/0x6098B4の定義・初期値とruntime書換え元、0x42A340/0x427040の異常状態での例外・副作用。
- [VERIFY] bytecount候補と暗号化後buffer lengthの一致、partial write/stream fail時の上位returnやUI通知（caller 0x45F960/0x53A100）。
- static branchingのみの監査。原作Gameplay実機golden PASS0、原作確定バグ0。
## 進捗と境界
Wave1 16/16、Wave2 10/10、Wave3 10/10、Wave4 3/12、重点累計39/48 STATIC VERIFIED・今回追加0（P0 20/21/P1 19/27、TODO8/VERIFY1）。研究MASTER最新cp83 DONE9/34。ゲーム再実装率は測定していない。
Local Compactのみ。原本・A-E・MASTER・T018・QUEUE・PROGRESS・Git・設定・automation変更なし。安全拒否済み新規解析/抽出は再試行も迂回もしない。
