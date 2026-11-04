# 迫真戦記ver0.67 REA 08H｜OggDecoderのファイルオープン経路と__chsize_nolockの到達条件
研究ID: `REA-LOCAL-20261028-08H-P0-OGG-FOPEN-CHSIZE-UNREACHABLE-GATE-STATIC-01`
状態: **PC-SAVED / STATIC / VERIFY / NOT READY**。Game Golden実測0、strict MATCH NOT RUN、正式REA新規VERIFIED 0。
source SHA256: EXE `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、10/21検索DB `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`、統合V9 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`。

## 先行照合・新規差分
MASTER、所有権規約、REA README/QUEUE/PROGRESS、10/11最終sync(64/64)、10/21検索README/BUILD_MANIFEST、07H静的監査証拠を読取。07H証拠の52/52 PASSを確認。active.lockなし、Windows PC接続成功。08Hは07Hで未解決の `0x005D2742` CALL siteの上位到達性を対象とし、07Hの4096-byte zero-fill解析を二重計上しない。
検索CLIを `function/callers/related` に限定使用し、原作PE専用コピーの必要範囲だけCapstoneで静的再照合。未承認のREA/Ghidra再実行は行わない。

## 新規STATIC-A：__chsize_nolockの呼出元はCRTオープン関数
`0x005D2742 CALL 0x005D2F0C` は、Ghidraで `FUN_005d2370` と記録されたCRT `__sopen_nolock` 相当関数の内部。そこへ到達する直接CALLを、次のように上位まで辿った。
`0x005D16C0`（ファイル読取用wrapper）→ `0x005D16CF CALL 0x005D1D6D`（`_fopen`）→ `0x005D1D7A CALL 0x005D1CB1`（`__fsopen`）→ `0x005D1D43 CALL 0x005D1ECE`（`__openfile`）→ `0x005D212E CALL 0x005D2B68`（`__sopen_s`）→ `0x005D2B7E CALL 0x005D2AA4`（`__sopen_helper`/VS2010 FID候補）→ `0x005D2B0E CALL 0x005D2370`。
`0x005D2AA4`はGhidra FIDで狭文字/ワイド文字の競合警告あり。呼出元の`_fopen`がchar*で、下流PEにはCreateFileAが存在するため、**今回の特定経路**は狭文字経路と整合するが、一般CRTライブラリの全入口を形式同定した主張ではない。

## 新規STATIC-B：ゲームのOggDecoderからはrbで開く
ゲーム側の音声ルート `0x004BEAD9 CALL 0x00501E20` → `0x00501E93 CALL 0x00502020`（OggDecoder::vftableを持つオブジェクト）→ `0x00502038 CALL 0x005D16C0` を保存済検索索引と原作機械語で照合。
`0x005D16C9 PUSH 0x0065B5B4` は`_fopen`のmode引数。原作PEの`0x0065B5B4`にある実バイトを確認したところ **`72 62 00` = `"rb"`**。
`__openfile`の `0x005D2046 OR EBX,0x8000` はb指定でバイナリフラグを設定する経路。r指定は読み取りモードで、`_O_RDWR=2`を付与しない。したがって本Ogg読取経路はread-only/binaryであり、後述の条件を満たさない。

## 新規STATIC-C：__chsize_nolockはテキストRW + 末尾Ctrl-Z時の限定処理
原作機械語 `0x005D26E2 TEST CL,0x80` → `0x005D26E5 JE 0x005D2992` がテキスト/バイナリ系ガード、`0x005D26EB TEST byte ptr [EBP+0x10],2` → `0x005D26EF JE 0x005D2760` がread/writeフラグのガード。
通過後に `0x005D2729 CALL 0x005BDCD1`（`__read_nolock`、1byte）を実行し、`0x005D2731 TEST EAX,EAX` → `0x005D2733 JNE 0x005D274E` と `0x005D2735 CMP byte ptr [EBP-4],0x1A` → `0x005D2739 JNE 0x005D274E` の両ガードを満たすと `0x005D2742 CALL 0x005D2F0C`へ到達する。
読み取り戻り値0かつバッファ中の0x1Aが成立する場合、EOF相当の末尾Ctrl-Zを切詰めるCRT互換コードと整合。返値-1なら `0x005D274C JE 0x005D2711` からclose/error処理へ分岐する。
**特定したOggDecoder `rb` 呼出経路では、上記テキスト・read/write条件の双方を満たさず、この__chsize_nolock呼び出しには到達しない。** これはあくまで特定の直接CALL経路に関する静的判定。間接CALLを含む全ゲーム実行経路の未到達証明でも、実機のトレースでもない。

## 索引・品質ゲート・到達範囲
新規独立監査は **32/32 PASS**（保存時約1.179秒）。対象の直接CALL site10箇所は、10/21 `calls` と統合V9 `native_callsite` の双方で各1件、今回範囲の索引欠落0。両DB `PRAGMA quick_check=ok`。偽の新規欠落や新規VERIFIEDを作らない。
関数別5種の充足は info=INDEX_ONLY、pseudo=INDEX_ONLY+原作ASM対照、assembly=TARGETED_PE_NATIVE、callers=INDEX_ONLY、callees=INDEX_ONLY+TARGETED_PE_NATIVE。正式REAの5種類完全パックの新規取得0、新規VERIFIED=0。既存Wave1～5最終保存同期64/64のまま。正式TODO/VERIFY/BLOCKED差分0/0/0。原作Golden PASS0、完全複製率未測定。
既存の07H証拠にはゼロ拡張の分岐が記録済みだが、今回の限定到達性判定はその別件であり、新規証拠として区別する。

## Golden設計・再開位置
使い捨てOGG素材について、末尾に`0x1A`を加えた場合と加えない場合、別途同じファイルを開く前後のサイズ・SHAを測定し、`rb`読み込みでは原本を変更しないという条件をデザインする。実際のデコード成功可否は別判定。ゲームEXE原本やユーザーの現存ファイルを変更しない。
CRT一般の`_O_RDWR|_O_TEXT`末尾Ctrl-Z条件でのファイル切詰めを実証するGoldenは、本作に安全な専用試験入口が特定されていないので**DESIGNED/NOT RUN**。
次の対象は `0x005CA1D1..0x005CA4EB`（`__write_nolock` Unicode/console戻り値補正）、またはOggDecoder `0x00502020` の仮想CALL `0x0050202A`のvptr解決。いずれも既存証拠と重複しないか先読する。
所有制限: 本ファイル・専用監査/証拠だけをrea_lab/decomp_taskに新規保存。MASTER/QUEUE/PROGRESS/既存RUN・他レーン・検索DB・原本ZIP/EXE/SAVE・Git・公開先・自動化設定は変更しない。Work不使用、新規REA/Ghidra/ゲーム実行0。

