# 迫真戦記 ver0.67｜REA 2026-10-27 20時台 P0・LF設定行の長さ判定とmalloc復旧ABI
研究ID：`REA-LOCAL-20261027-20H-P0-LF-LENGTH64-NEWH-ABI-STATIC-01`
状態：**PC-SAVED / STATIC / VERIFY / NOT READY**。対象：`0x00557A20`, `0x00402A40`, `0x005B6C2B`, `0x005BBA77`。

## 基盤・非重複
MASTER_LEDGER、レーン規約、REA README/QUEUE/PROGRESS、既存runsと2026-10-11最終同期記録、10月21日検索DB manifest、19H静的証拠を先読。
同一原作SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
検索DB `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`、V9 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`。
両DBは `mode=ro&immutable=1` / `PRAGMA query_only=ON` で quick_check=ok。`0x00402ABA -> 0x005B6C2B` のsite照合済み。
CLI `function 0x00402A40/0x005B6C2B/0x005B864E/0x005BBA77`, `callees/callers 0x005B6C2B`, `related 0x00402A40 --depth 2`を使用。対象のPE機械語はCapstoneによって独立確認。
19Hは異常な長さが確保へ伝搬する候補まで。**今回の差分は、64bit相当の短行ゲート、mallocラッパーのEAX戻り値、new-handler再試行／二重の例外経路の分離**。

## 新規静的結果A：短行ゲートは上位・下位DWORDを順に比較
`0x00557A5B XOR EBP,EBP` により比較用EBP=0。
`0x00557C4A CMP [ESP+0x30],EBP`、`0x00557C4E JL 0x00557EC8`、`0x00557C54 JG 0x00557C61`。
上位DWORDが0の場合のみ `0x00557C56 CMP [ESP+0x2C],2` → `0x00557C5B JBE 0x00557EC8`。
この局所制御フローは符号付き上位DWORDと符号なし下位DWORDを組み合わせた64bit長比較（長さ>2）と整合する。上位=0で下位0/1/2なら解析をスキップし、3以上なら `_strpbrk` 方向へ進む。
ただし、入力からこれら2DWORDへの全代入経路とゲーム上の影響は未検証。`0x00557C6E`の `_strpbrk` NULL分岐候補は18H、`0x00557C7D`からの巨大長伝搬は19Hの既存発見であり再計上しない。

## 新規静的結果B：mallocラッパーはGhidraのvoid疑似CとABIが異なる
既存擬似Cは`void FUN_005b6c2b(size_t)`と表示。しかし原作命令は `0x005B6C45 CALL 0x005B9BC8`（`_malloc`）→ `0x005B6C4B TEST EAX,EAX` → 非NULL側 `0x005B6C4F LEAVE` / `0x005B6C50 RET`。
成功時、EAXを上書きせず戻るので、**成功ポインタはEAXで呼出元へ返る**。呼出元 `0x00402ABA CALL 0x005B6C2B` → `0x00402AC2 TEST EAX,EAX` がこれを確認する。
従って再実装でGhidraのvoidシグネチャをそのまま採用すると、正常な戻り値ABIを失う。REA正式5種証拠の完成・正式VERIFIED昇格を意味しない。

## 新規静的結果C：new-handler復旧とbad_allocは別の経路
`0x005B6C2B`でmallocがNULLなら`0x005B6C38 CALL 0x005BBA77`（`__callnewh`）。非ゼロで `0x005B6C42`へ戻りmalloc再試行、ゼロなら `0x005B6C51`以降で `std::bad_alloc`を組み立て、`0x005B6CA5 CALL 0x005B864E` でthrowへ進む。
`0x005BBA77`内部は `0x005BBA82 CALL [0x006091C0]` (DecodePointer経由)、`0x005BBA8F CALL EAX` (動的new-handler) を含む。callbackの実アドレスと有無は未確定で、間接CALL候補として保留。
さらに文字列拡張側 `0x00402AC2 TEST EAX,EAX` → NULL時の `0x00402AEE CALL 0x005B864E` は独立したthrow経路。通常の `0x005B6C2B` 成功復帰は非NULL、失敗復帰はthrowなので、呼出元のNULLフォールバックは防御的経路と解釈できるが、常時到達不能の証明はしない。
巨大要求時に実際のメモリ不足、new-handler、catchまたはゲーム終了が起きるかは実測しておらず、**クラッシュ確定としない**。

## 数値・安全・再開
限定静的監査 **47/47 PASS**（関数数ではなくassert条件数）。保存済みWave1〜5の**64/64 VERIFIED**を維持、新規正式VERIFIED 0、新規5種完全証拠0。正式TODO/VERIFY/BLOCKED差分0/0/0。
5種：info/pseudo/callers/callees=INDEX_ONLY、assembly=TARGETED_PE_NATIVE。原作Golden PASS 0、strict MATCH NOT RUN、完全複製率 NOT MEASURED。
Windows研究PC接続成功、事前active.lockなし、空き物理RAM約11.58GiB、CPU負荷不明。監査本体約1.17秒、研究全体時間不明。新REA・Ghidra・Vahren実行0、Work使用なし。
原本ZIP/EXE/SAVE、MASTER、他レーン、QUEUE/PROGRESS、既存RUN、Git、公開先、スケジュールには触れず。本回のPowerShellで古いUTF-8 sync JSONをConvertFrom-Jsonした際は端末文字コードによるエラー(OTHER、非安全拒否)。後続のPython UTF-8 readで最終64/64を確認し復旧。
次優先は `0x005B9BC8`（CRT malloc自身のnew-handler内部再試行と割当失敗時errno）と `0x00557A20` のSEH catch/unwindの実際の到達・例外処理。Golden案：CRLF/LF-only長さ2・3・10/末尾改行なし/1024byte境界、全件DESIGNED/NOT RUN。
