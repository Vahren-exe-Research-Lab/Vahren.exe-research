# 迫真戦記 ver0.67｜REA 18時台 P0：debug_paperのCRLF・EOFゲート
研究ID：`REA-LOCAL-20261027-18H-P0-DEBUGPAPER-CRLF-EOF-STATIC-01`。状態：PC-SAVED / STATIC / VERIFY / NOT READY。
## ソースと既存成果
原作コピーSHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、10/21検索DB `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`、統合V9 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`。3ファイルのSHA一致、2 SQLite read-only/immutable quick_check=ok。保存済み旧同期 Wave1-5 VERIFIED 64/64、旧PROGRESS 15/16は古い。17時台64/64監査を別計数として確認。新規正式VERIFIED 0。
新Ghidra起動なし。検索CLI `function/callers/callees/related 0x00558CF0`、`function 0x00558E68`、`_strpbrk 0x005B83B0`を使用。原作PE機械語で `0x00557A20`、`0x00558CF0`、`0x00558E68`、`0x005B83B0`の対象命令を独立照合。
## 新規確定A：改行のない最終行はパースに入らない
`0x00557BFF PUSH 0x0A`→`0x00557C1C CALL 0x00558CF0`（改行で区切るストリーム読込）。`0x00558D93 CMP EAX,-1`→EOFで`0x00558D98 OR [EBP-0x14],1`→`0x00558DA3`から終了ヘルパ`0x00558E68`へ。ヘルパ`0x00558E6B`はNUL終端し、エラー状態を更新する。
呼出元`0x00557C2C TEST AL,1`→`0x00557C2E JNE 0x00557F73`により、EOFに遭遇した読込結果は`_strpbrk`の前に処理を抜ける。後続の2回目の読込`0x00557F02`にも同じbit1ゲート`0x00557F12/14`がある。最終未終端行のテキストはバッファに残り得るが、行として適用されない（static）。
## 新規確定B：配布fixtureはCRLF×5、末尾switch改行なし
スナップショット64byte / SHA256 `867E889A74C302F17C1398C2A8311E0C1F305896BC8CBFE43010C8127295B988`。5行は
、末尾`switch`には改行なし。先行する`width1320`と`height990`はCRLF終端のため読込・解釈対象になり得るが、最後の`switch`はEOFゲートで読み飛ばされる。実ゲームの最終表示結果は未測定。
## 新規VERIFY：LF-onlyのパーサー到達条件
読込関数は区切り`0x0A`を消費し、バッファへ格納しない。`0x00557C68`でCR/LF集合 `\n\r`を`_strpbrk(0x005B83B0)`へ渡す。`0x005B83DC`は不一致終端でNULLを返す経路。LF-onlyの非空長>2の行では、区切りLFは既に除去されCRもなく、NULL候補に到達する。呼出元`0x00557C7D SUB EAX,ECX`はNULL検査なしで長さを計算し、`0x00557CA4`のstring構築へ渡す。この経路の実際の例外・クラッシュ・設定適用可否は **VERIFY / NOT RUN**。
## 監査と再開
独立静的監査 **45/45 PASS**。既存VERIFIED 64維持、新規5種完全証拠0、正式TODO/VERIFY/BLOCKED差分0/0/0。5種：info/pseudo/callers/callees=INDEX_ONLY、assembly=TARGETED_PE_NATIVE。原作Golden PASS0、strict MATCH NOT RUN、完全複製率NOT MEASURED。ゲーム・REA・Ghidraの新規起動0、Work未使用。
CPU負荷不明、作業全体の所要時間未測定、監査本体約2.092秒。開始時active.lockなし/空きRAM約12.1GiB。所有範囲のみ新規ファイルを保存し、MASTER/QUEUE/PROGRESS/旧RUN/他owner/原本/Git/スケジュールは変更しない。
**次優先：** `0x00557C4A`の長さ判定、`0x00402800`のNULL由来サイズに対する境界処理、`0x005555DF`のDisplayMode寸法上書き。LF-onlyとCRLF・最終未終端行のGolden設計はDESIGNED / NOT RUN。
