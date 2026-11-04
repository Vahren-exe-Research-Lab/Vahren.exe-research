# REA-20261021-2135-T014-SHORTREAD-STATE-GAP-STATIC-01
- 日時: 2026-10-21 21時台 JST。owner=REA、T014/P0。状態=STATIC / VERIFY / NOT READY。旧EXE Golden=0、新旧strict MATCH=0、ゲーム再実装率=未測定。
- 接続: Desktop Commander Local Compact成功。MASTER/ANALYSIS_LANES_PROTOCOL/REA README・QUEUE・PROGRESS、REA既存T014資料・20:35記録、検索README/BUILD_MANIFESTを先読。既存runs/evidenceは旧同期証拠参照として保持、変更なし。
- source EXE SHA（BUILD_MANIFEST記録）: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。EXE現物再ハッシュなし。
- 検索DB manifest SHA: 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF。今回現物再ハッシュは未実施、DB integrity_check未実施。既存Ghidra12.1.4検索CLI関数抽出のみ、新Ghidra/REAは実行0。
## 新しい独立STATIC差分: 短いブロック読込後の状態ビット更新が疑似C上は未接続
- `0x470700` (code SHA 873CD6F6F7A5DF2EDE7A631557223DEDB71B3AEA7262FADE79ACA0A9AD86D6C8): site `0x470713`→`0x42E700`、要求size=4、直後にstream state `&7` が非ゼロならLoadException、ゼロならDAT_00B060F0を出力。
- `0x42E700` (code SHA E50363BD394C5A7820AADE195D5B53B5B02CF000DA9C4AE12D6EB29C168C8A76): gcount下位+8/上位+12を0初期化、site `0x42E753`→sentry `0x42EC60`、site `0x42E77F`→`0x42ECF0`、返却候補64bitをgcountへ加算し、site `0x42E7A2`→cleanup `0x42E7D4`。親疑似Cには明示的な`gcount < requested`比較がない。
- `0x42ECF0` (code SHA 509ABCB0231F72EE6B7D32D3F197B65F895CDFE2812F22188DBE481B45285E21): site `0x42ED07` はvtable+0x20への間接CALL。Ghidraは戻り型`void`、親は`uint64`として消費するABI矛盾を維持。
- 既存vtable監査上のbasic_stringbuf候補`+0x20` = `0x4297D0`（実行時vptr未検証、REA正式vtable VERIFIEDではない）。今回保存検索CLIでその疑似Cとcaller/indirect一覧を独立抽出。
- `0x4297D0` (217 bytes, code SHA 851F477F38B06755F148F603E3D5387DE54DDCF5FB726345BD836EC30D9CAD2D): 読込可能分があればmemcpy＋ポインタ/残量更新、残量なしはvtable+0x1C (`0x42985F`のcomputed CALL)で1byteを取得。-1なら累計lVar1（部分読込数）を返す。
- `0x4297D0`自身の保存疑似Cにstream stateの明示書込や`0x426E00`直接CALLは見えない。**これは下層の静的観察であり、上位がEOF/failbitを立てないと証明するものではない**。
- `0x42E7D4` (code SHA 5810D08FCC35B9C755402E352BCCD84543832127EF573EFB4A9CB259700D3C1C) は親frameの`EBP-0x14 !=0`で `0x42E7F2`→`0x426E00`を実行する。親疑似Cにそのslotの完全な値伝達が復元されておらず、このcleanupが短読込状態を更新する可能性はVERIFY。
- `0x426E00` (code SHA 7BEBA43A38A9E3880B88EFBA64A11D7CE7087E53C03C0BCF4B846B3C828B1A43) はGhidra疑似Cでstream state `&0x17` と例外マスクを扱う。レジスタ引数`in_EAX`は未解決。`0x42E7D4`からの実際の値を断定しない。
- `0x42EC60` (code SHA BA687A12FA8459739AA47BE9E79DC502205A11B3CBF3DB07972208DA265C7D8F) は入口とsentry後のstate==0条件を確認、失敗時 `0x42ECD1`→`0x426E00`。すでに発生した短読込の事後判定とは別段階。
## 新しく明確にした不確定境界
- 4bytes要求で3bytes/0bytesしか返らない場合、`gcount`は部分数を反映する静的候補だが、`LoadException`発生は**上位ロード前のstate**に依存。`0x42E7D4`の未復元レジスタ/親frame状態を解消するまで「短読込でLoadExceptionになる/ならない」は共に断定禁止。
- 直前20:35の新規成果は`(state & 7) !=0`と4caller。本報告の追加差分は「下層basic_stringbufのpartial-return→gcount更新→cleanupのstate生産が未解決」という経路の接続であり、既知state式やvtable対応を二重計上しない。
- 旧記録で未解決の`0x42E7A2`の命令種や0x42ECF0 EDX:EAXはVERIFY継続。拒否済みCALL_INDEX_V2命令照合は再試行していない。
## 安全・障害記録
- `REA-RC-20261021-2135-429620-CLI-SAFETY-01`: `search.py function 0x429620 --limit 12 --max-chars 16000 --format json` の呼び出しが `Script error: ... blocked by OpenAI's safety checks` で拒否。対象関数の新しい本文/ASMは未取得。接続障害ではなくSAFETY_REFUSAL。
- 上記拒否以後、0x429620についてツール・shell・path・ZIPを変えた再試行なし。取得済み0x4297D0以前の既存合法データのみ使用し、独立な関数間比較を継続。許容される次手は安全境界を維持した状態で対象外の証拠を照合すること。
- 新規info/pseudo/assembly/callers/calleesのREA正式5種完全セット=0、REA新Evidence ID=0、REA新VERIFIED=0、TODO/VERIFY/BLOCKED正式差分=0/0/0。過去報告値Wave1..5=64/64、Wave6候補TODO12/SAFETY_BLOCKED4/VERIFY0、PCの旧QUEUE/PROGRESSはEPERMでstale（変更しない）。
- Golden設計 NOT RUN: 入力4bytes/3bytes/0bytesとEOF直前状態0/1/2/4、stream例外マスク0/2/4を分離。`gcount`、state、出力先の更新、上位LoadException/ios failure、partial byte 0xFFを独立観察。旧EXE実測PASS0、strict MATCH0。
- 次のP0: `0x42E7D4`のEBP-0x14起源と`0x426E00`へ渡るEAX、`0x42ECF0`のEDX:EAX中継を許可済み証拠で照合。拒否済み操作や対象を迂回して再収集しない。
- 実行時間: Ghidra/REA=0秒、全作業所要時間は未計測。PC CPU/RAM実測不明。PC正本のMASTER/QUEUE/PROGRESS/runs/evidence/A-E/T018/dev_lab/原本/Git/設定/スケジュールは変更しない。
- 保存区分: REA担当の新規独立STATICメモに限る。MASTER正式統合・新規VERIFIED・Golden実測は一切行わない。保存/readback/ハッシュは独立チェック後に確定する。
