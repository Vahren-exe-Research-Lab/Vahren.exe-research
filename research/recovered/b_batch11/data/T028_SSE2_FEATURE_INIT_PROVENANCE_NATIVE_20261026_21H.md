# 迫真戦記 B T028/T012｜方向整数化CRT SSE2判定フラグの設定元（2026-10-26 21H）
研究ID: B-20261026-2127-T028-SSE2-FEATURE-INIT-01 / owner B / STATIC-ORIGINAL-PE-ASM / STATIC-ORIGINAL-PE-DATA / INFERRED / VERIFY / NOT READY
## 前提・境界
MASTER checkpoint196/READY596=A115/B229/C136/D116 は E 既存正式値。B5 owner・LANES protocol・HANDOFF・未同期/拒否台帳を読取、10/25 14H全文・他lane/Library意味重複は未完。禁止VA/既拒否コマンドの再試行なし。
対象原本 rea_lab/targets/hakushin067_Vahren.exe 実SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。旧search.sqlite実SHA256 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF、URI mode=ro&immutable=1 quick_check=ok。active.lock 3候補不在、新Ghidra/REA起動0。
## 今回の新規原作機械語・PEインポート
- 0x5BB349 PUSH 0xA → 0x5BB34B CALL DWORD PTR [0x609118] → 0x5BB351 MOV [0xB14A40],EAX → 0x5BB356 XOR EAX,EAX → 0x5BB358 RET。原作PEのIAT 0x609118 は KERNEL32.dll!IsProcessorFeaturePresent と実照合。
- Windows公式の ProcessorFeature=10 は PF_XMMI64_INSTRUCTIONS_AVAILABLE（SSE2利用可）。APIが真のとき、初期化後[0xB14A40]!=0になり得る。API仕様出典 https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-isprocessorfeaturepresent
- .rdata 0x609654 はDWORD 0x005BB349。連続した初期化関数ポインタ表0x60964C..0x609667に含まれる。
- 0x5BB438(__cinit) は0x5BB464 PUSH 0x609668 / 0x5BB469 PUSH 0x60964C / 0x5BB46E CALL 0x5BB414(__initterm_e)。0x5BB414 はポインタを先頭から末尾排他で走査し非NULL関数を間接CALL、非0戻値なら中断。故に正常な初期化経路では0x5BB349を呼び出しSSE2可否を一度設定（STATIC+条件付きINFERRED）。
- 原作0x5BB349 16B窓 SHA256 B22BB4290A9827E78C737711D10DBAD791C07E64BE5CD5EE625A6A9E47DCF5E0。0x5BB414 36B SHA256 1F28B44DC2C37853FCA518C9BE09224B5AE94CB545A6D9B7AC4F9552CCF7D0F8。0x5BB438 151B SHA256 5750E3AE184D9E53A99DEE1C889672FF743EAB73A8683C7F6D83BA67A951DB93。
## 旧20H成果との接続（再計数しない）
- 既知0x5D1B80 CMP [0xB14A40],0 → 非0は0x5D1B95 CVTTSD2SI、0なら0x5D1BB6..0x5D1C2A x87 fallback。今回の増分はCPU/OS機能API→初期化テーブル→flagへの具体的producer接続。0x40EDB0/atan2/Unit+0x18688更新は既知で再計数0。
- 原作.textからDWORD 0x00B14A40 の直接アドレス埋込は計8箇所：0x5B674A/0x5B875A/0x5BB352/0x5BE420/0x5C94FA/0x5CD923/0x5D1B82/0x5D1B9E。旧SQLite data_refs はREAD6/WRITE0、原作で未索引の0x5BB351 STOREと0x5D1B9C READを確認。インデックス0件を『writer不存在』と見なすのは誤り（索引網羅性VERIFY）。
- CRT側0x5BB349はGhidra内部関数一覧で直接の独立エントリがなく、元PEの.rdata初期化関数ポインタで到達する。間接CALL・静的関数ポインタを手掛かりとする必要がある。実機呼出トレースはまだない。
## 残VERIFYと安全・Golden
- SSE2判定APIの実行時返却値、CRT早期中断、OS/CPU差のSSE/x87挙動、x87例外・丸め境界、atan2実際の二軸順、方向8/同位置の実ゲーム到達はVERIFY。製品挙動の確定やバグ認定を行わない。
- Golden設計: 無改変原作ver0.67 EXE、x20強化前DAT、同SAVE/MAP/input/RNGで起動時feature flag、四象限/方向境界/同座標、翌tick方向/位置を取得。旧Gameplay PASS0、strict MATCH0、DESIGNED_NOT_RUN。
- 既拒否対象/コマンド/証拠を別tool/path/shell/Remote/ZIPで迂回しない。MASTER/他lane/REA/dev_lab/原本ZIP/EXE/DAT/SAVE/Git/Work/設定/スケジュール書込0。正式新READY0/E MASTER統合0/Task DONE0。
## 次回
0x5E48F7→0x5E75EC のatan2引数軸・符号分岐を許可された静的範囲で限定照合。必要時は0x5D1B9Cの第二入口利用元と戻値下位32bitを検証。T013索敵direction consumerは既拒否範囲を避け独立根拠で検索。旧10/25 14H OFFLINE全文の完全重複照合は未完。
