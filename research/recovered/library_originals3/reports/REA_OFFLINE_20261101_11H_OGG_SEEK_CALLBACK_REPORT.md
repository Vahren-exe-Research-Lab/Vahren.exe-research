# 迫真戦記 ver0.67｜REA/T015｜2026-11-01 11時台 P0 オフライン静的調査

**研究ID**: `REA-OFFLINE-20261101-11H-P0-OGG-SEEK-CALLBACK-ERROR-GATE-CROSSCHECK-STATIC-01`  
**最終状態**: `OFFLINE-UNSYNCED / STATIC-INDEX-AND-PRIOR-ASM / INFERRED / VERIFY / NOT READY`  
**重要**: この回で確認したのは保存済みGhidra検索DBの擬似C・CALL索引と先行の実機械語検証記録の整合。オフラインZIPには原作PEがない。新規PE命令バイト取得、REA/Ghidra実行、原作ゲームの動的確認は行っていない。

## 1. 接続・先行成果・非重複

Desktop Commander Local CompactでPC側MASTER/PROTOCOL/REA README/QUEUE/PROGRESS/検索基盤/knowledgeをまとめて読もうとしたが、`UNAVAILABLE: MCP SSE probe returned 429 from openai.org`。接続経路の一時制限であり、PCの電源状態・owner/active.lock・現在の台帳・未同期有無は**不明**。安全拒否と混同しない。接続障害ID `REA-RC-20261101-11H-LOCAL-SSE429-01`。PC正本へ書き込まない。

ChatGPT Libraryに存在した `HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip` を読み取り専用で復元し、ZIP SHA256 `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`、全34メンバーのCRC、旧Ghidra検索SQLiteのSHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`・`PRAGMA integrity_check=ok`を確認。ZIP manifestの原作PE識別子は `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。**原作PEの現在の実SHAを測定したのではない**。この旧検索DBは10,268内部関数・188外部関数のスナップショットであり、後発の統合V9実DBではない。

先行資料 `REA-OFFLINE-20261028-17H-P0-OGG-INDEX-ALLOCATION-RETURNGATE-STATIC-01`、`REA-OFFLINE-20261101-10H-P0-OGG-COUNT-PUBLISHED-BEFORE-ALLOC-SUCCESS-CROSSAUDIT-STATIC-01`の証拠JSONをそれぞれSHA256 `0CDC20B8A92CF7A37B2966121A68C0F5B454009FA0D36B133954B5A3E277070D` / `ECE50225ACC8A09E0E61E5A2CBD7CD320DB2396581B671AC80FC2B3AA4B51FDD` で再読した。以前のalloc/索引リスクを新規発見・新規VERIFIEDとして重複計上しない。

非公開GitHub `ButaMonky/Hakushin067-Research-Knowledge` の `develop`で `KNOWLEDGE_CURATION_PROTOCOL.md`（blob `4d6da0d1fa10fa8bf47956fe2fd9023801ec750a`）、`GHIDRA_V9_COVERAGE_REPORT.md`（blob `786f7fc5647a54a08609d28db2f673c7dbfd6b36`）、`REF_AUDIO_VORBIS.md`（blob `ded46f3597bd9ea5841fb167be5846ce8b0f2223`）、`symbols.tsv`（blob `3fcf2d436c21f3fc91791a91e75c9a800167ca4d`）、`structs.tsv`、`README.md`、`SYNC_STATUS.md`をread-only参照。今回の3間接CALL siteは検索したREF_AUDIO_VORBIS/symbolsに**明示的な同一VA登録を確認できなかった**が、PC owner資料に先行記録がないと断言しない。統合V9 SHA報告値 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`は現物未検証。

## 2. 新たな横断知見：初期シークと索引内シークで戻り値の扱いが異なる

**対象関数** `0x005D1310`（Ogg索引初期化）、`0x005CF4D0`（索引作成）、CRT `0x005C30BE`（_realloc）。既存検索CLIの対象限定 `function`、`callers`、`callees`、`related --depth 2` を使い、追加の全関数解析は行っていない。

旧SQLite内 `FUN_005d1310` 擬似C（保存済みコードSHA256 `8670DBDABE05FCD869D39B297DAF16E3C07409D2384F478219A4F4B57F606462`）の**擬似C行26、33～34**で、owner DWORD配列の `+0x2C4`（index `0xB1`）がseek callback、`+0x2CC`（index `0xB3`）がtell callbackに使用される。ポインタがどちらかNULLなら長さを-1 sentinelに設定する。両方あれば、seekを `(*owner, 0,0,2)` 相当で呼び、**擬似C上ではその戻り値を変数へ受け取らず**、次にtellを呼んでその結果で長さを決める。先行17Hの実x86検証記録には `0x005D136A: FF D0` と `0x005D1375: FF D0` の二つの間接CALL、および後続 `0x005D1377: 99` がある。

一方 `FUN_005cf4d0`擬似C（SHA256 `B0586B68BDF8D49943E9DB10D1F337F693E964F95DAC75EDEC19EE27B61FDA63`）の**行132～136**では、同じ `+0x2C4` callbackを `(*owner, seek_offset, 0)` 相当で呼び、戻り値を `iVar6` に受けて `iVar6 != -1` を検査する。失敗とみなす側は `-0x80`。Ghidra間接CALL索引はこの地点を **`0x005CF884: CALL EAX`** として登録している。**このsiteの実x86ウィンドウは今回未取得**なので、擬似C・索引の観測と原本ASM直接検証を混同しない。

`0x005D1310`ではサイズ検査失敗（callback欠落またはtellの-1 sentinel）から `0xFFFFFF7D`（-131）へ、`0x005CF4D0` の負数結果から `0xFFFFFF80`（-128）へ分岐する（擬似C行45～46, 71）。旧Ghidraの直接CALL索引では `0x005D140D -> 0x005CF4D0`、再帰 `0x005CF628 -> 0x005CF4D0`を確認し、先行実ASMのE8飛先とも整合した。

**新規推論 `KB_CANDIDATE`**：初期シークが失敗を示しても、その後tellが有効値を返すという合成条件では、`0x005D1310`の最初のサイズ分岐は「seek戻り値それ自体」を理由に拒否しない可能性がある。一方、`0x005CF4D0`の後続seekは戻り値`-1`を検査する。この**初期seekと索引内seekのエラー判定非対称性**を、過去17Hの確保失敗や10Hの件数公開問題と別の検証契約として記録する。コールバックABI、`0x005D136A..0x005D1375`の完全な命令列、`0x005CF884`の原本命令、元の入出力状態、他のエラーガード、実ゲームでの到達性は未確認。脆弱性・実クラッシュ・厳密なVorbis仕様の違反とは断定しない。

## 3. 監査・状態差分

監査Pythonを使い、オフラインZIPと旧SQLite実体のSHA/CRC/整合、指定3関数のGhidraコードSHAと本文再SHA、3つの間接CALL site（`0x005D136A`、`0x005D1375`、`0x005CF884`）、2つの直接CALL site、先行x86断片、2種の戻り値ゲートを照合。**44/44 PASS、0 FAIL、監査プログラム実行0.665301秒**。PASSは「保存DBの対象範囲と過去記録の整合」だけであり、44件の原本新規証拠・Golden実測・完全互換の実績ではない。

REA正式5種は `info=旧indexの関数メタデータのみ / pseudo=旧Ghidra擬似C / assembly=先行2サイトの断片のみ、0x005CF884未取得 / callers=旧index / callees=旧index`。**今回新規5種完備0、新規正式VERIFIED0、正式TODO/VERIFY/BLOCKED台帳変更0/0/0、原作Golden実測PASS0、strict MATCH0、READY0、完全複製率未測定**。従来のVERIFIED64は前回までの履歴値を保留し、現行PC台帳とは未照合、二重加算なし。

CPU・RAM・active.lock/owner、ゲーム負荷、作業全体の所要時間は不明。研究PCへの書き込みはゼロ。今回は独立成果・監査器・readbackをオフライン側で保全するのみで、REA/Ghidra/EXE・共有knowledge・MASTER/QUEUE/PROGRESS・Git・既存時刻/スケジュールを変更しない。

## 4. KB_CANDIDATE・再開位置

`KB_CANDIDATE`: owner `REA/T015`、ID上記、VA `0x005D1310 / 0x005CF4D0`、CALL site `0x005D136A/0x005D1375/0x005CF884`、保存フィールド `owner+0x2C4/+0x2CC`、直接CALL `0x005D140D/0x005CF628`。証拠: 旧SQLiteの関数code SHA/間接CALL索引、先行17Hの2箇所のASM、非公開KBの上記blob SHA。`STATIC`は観測された保存資料、`INFERRED/VERIFY`はcallback失敗時の意味・到達性、Golden=0、READY=0。共有辞書へは自動反映せず統合専任へ委ねる。

**次回P0**: PC復旧時にMASTER/QUEUE/PROGRESS・owner/lock・先行IDを確認したうえ、許容される原本ASMから `0x005D136A..0x005D1377` と `0x005CF884` 前後のCALL結果レジスタ生存/分岐を**独立して**検証し、`0x005D1310`のseek/tell ABIとエラー戻り値を特定。PCが不通なら、許可済みオフライン検索DBからcallbackの初期化関数と利用元の読取専用比較を進める。禁止VA・既拒否エクスポートの迂回なし。PC正本同期は現行ownerと重複を照合してから自担当許可範囲に限り1回。
