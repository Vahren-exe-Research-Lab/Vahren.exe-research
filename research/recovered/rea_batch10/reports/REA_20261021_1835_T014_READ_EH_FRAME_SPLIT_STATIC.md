# REA-20261021-1835-T014-READ-EH-FRAME-SPLIT-STATIC-01

- 所属: 独立REA / T014(P0) / STATIC・VERIFY・NOT READY / 新REA VERIFIED=0 / 旧EXE Golden PASS=0。
- 実行: 2026-10-21 18:35台 JST。Desktop Commander Local Compact接続成功。原本・MASTER・A〜E・既存QUEUE/PROGRESS・Git・スケジュール未変更。
- 出自: Ghidra12.1.4既存検索DBの保存疑似C/関数境界/直接・間接CALL索引。EXE記録SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（EXE現物再hashなし）。
- DB search.sqlite現物SHA256=0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF、BUILD_MANIFESTと照合PASS。SQLite integrity_checkは今回未実施。
- 既往先読: MASTER、ANALYSIS_LANES_PROTOCOL、REA README/QUEUE/PROGRESS/WAVES、旧run 20261011T153309850Z、最新sync 20261011T153958076Z、直前のREA_20261021_1735_T014_SENTRY_EOFBIT_V34_CONTRAST_STATIC.md。
- 凍結進捗: 最新保存syncによりW1..5=16+10+10+12+16=64/64 STATIC VERIFIED。QUEUE/PROGRESSはEPERM古値のため上書き禁止。Wave6は正式0/16、候補TODO12・安全拒否BLOCKED4・結果VERIFY0（前回記録値、新たな変更なし）。

## P0未解決ABIとEH境界の新規差分
- 関数 `0x42E700`（code SHA E50363BD394C5A7820AADE195D5B53B5B02CF000DA9C4AE12D6EB29C168C8A76）は始めにstreamの64bit gcount下位+8/上位+12をゼロ初期化。`0x42E753→0x42EC60` read sentry、成功時 `0x42E77F→0x42ECF0`、その後 `0x42E7A2→0x42E7D4` とつながる。これらのCALL siteは検索DBの直接CALL索引に存在。
- `0x42ECF0`（31 bytes、code SHA 509ABCB0231F72EE6B7D32D3F197B65F895CDFE2812F22188DBE481B45285E21）は `0x42ED07` の未解決間接CALL `CALL EAX`（vtable+0x20）を行う。疑似Cは`void`だがcaller `0x42E700`は`uVar5`(64bit)としてその結果をgcount下位/上位に加算。**呼出元期待値と呼出先デコンパイルの戻り値型が一致しない。** 具体的なEDX:EAXは未実証。
- `0x42E7D4`（84 bytes、code SHA 5810D08FCC35B9C755402E352BCCD84543832127EF573EFB4A9CB259700D3C1C）は`unaff_EBP`/`unaff_EDI`を参照し、EBP-0x14非ゼロで `0x42E7F2→0x426E00`、EBP-4を-1へ設定、tied stream候補のvtable+8を `0x42E810` で間接CALLし、`ExceptionList`をEBP-0xCから復元する。したがって親のframe/SEH状態に依存する可能性が高い。
- 親 `0x42E700` の成功分岐では、Ghidraが`piVar4=(int *)FUN_0042E7D4(); return piVar4;`を生成する一方、子 `0x42E7D4` は`void`として復元される。この**型矛盾は正常戻り値を子の独立returnとして確定できない根拠**。sentry不成立分岐の疑似Cでは `return param_1`。成功分岐も同じ戻り値とはASM未照合につき断定しない。
- `0x42E7A4` はGhidra命名 `Catch_All@0042e7a4`、45bytes、code SHA 3E535771EFAAAF577B0A3C7EDDE9E62202A6949F8951F25C26BE1C98154A89D0。`0x42E7BF→0x426E00`をCALL、EBP-4=1を設定し、`0x42E7D1`を復帰位置として返す疑似C。直接CALL索引のcaller=0でも**EHハンドラであれば到達し得る**ためdead codeと解釈しない。
- `0x42E700` にSEHハンドラ候補 `LAB_005EB8D0`のデータ参照(site 0x42E705)があり、同疑似Cは`0x42E7E4/EE/F1`のunreachable block除去警告を出す。0x42E7A4がそのハンドラとどう結び付くかはEHメタデータ/ASM未照合。推測をVERIFIEDにしない。
- `0x426E00` は状態/例外マスクを使って条件付きthrow可能なhelper。`0x42E7A4`のCALLを『常に例外を投げる』とは解釈しない。`0x42E7D4`のEBP-0x14が何由来かも、親frameのASM検証なしに状態フラグと断定しない。

## 独立比較・安全境界
- 直前17:35記録はread sentryのstate==0対write (state&6)==0が中心。本記録は新たにcatch側0x42E7A4／cleanup側0x42E7D4／戻り値型の矛盾を対応づけた差分で、既知のread/write predicateや既往vtable mappingを再計上しない。
- 新Ghidra/REA実行0。拒否済み0x5710C0..0x571500・Wave6拒否4件・REAエクスポート・旧EPERM置換は一切再試行/迂回せず。新規info/pseudo/assembly/callers/callees 5種セット取得0、REA正式Evidence ID0、VERIFIED増分0。
- 再照合CLI: `search.py function`で0x42E700/0x42EC60/0x42ECF0/0x42E7D4/0x42E7A4/0x426E00、`callers 0x42E7D4`、`callees 0x42E7A4`、`related 0x42E7D4 --depth 2 --limit 30`を既存DBに限定して実行。直接CALL、indirect CALL、関数別code SHAと矛盾なし。
- 保存済みASM(対象EH範囲)について、REA担当Markdown内の`0x42E7A4`と`exe`のtxt内の`42ECF0`を文字列検索したが該当0。見つからなかったことはASM非存在の証明ではない。現時点のassembly充足は0。
- 黄金検証設計（DESIGNED_NOT_RUN）: sentry失敗/成功、取得数0/1/部分読込、EOF状態1・failbit2・badbit4、例外マスク0/2/4、tied streamあり/なし、仮想+8の戻り/throw、catch経由の後始末、返却streamポインタとgcountを別々に測る。原作実機PASS=0、新旧strict MATCH=0、再実装率未測定。
- 最新同期照合必要: REA結果64/64とmaster DONE9/34は既往保存値。今回QUEUE/PROGRESSとMASTERの更新をしていない。担当A/T014が仕様に統合するまでは本メモはREA独立STATIC・非READY。
- PC状態: Local Compact接続成功、decomp_task内にactive.lockなし、開始時Local sessions 0件。プロセス一覧取得したがCPU使用率はn/a、空きRAM未測定。全作業時間未計測、Ghidra/REA実行0秒。SQLite現物hash確認、既存DB再構築なし。
- NEXT P0: 既存許可済みASMまたは次回PCのread-only調査で`0x42E77F`前後のEAX/EDX・ESP、`0x42E7A2`から子cleanupの正常return、0x42E7A4 EH table、EBP-0x14初期化と`0x42E7D4`例外経路を照合。原本・拒否対象を別経路で再抽出しない。
- 記録状態: このREA担当フォルダの新規Markdownのみ書込対象。readback成功/ハッシュ確認後に確定とする。MCP/OS設定、owner他資料、既存予定を変更しない。
