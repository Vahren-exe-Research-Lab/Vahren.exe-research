# 迫真戦記ver0.67 REA／2026-10-28 22時台 P0独立静的証拠

- **研究ID:** `REA-OFFLINE-20261028-22H-P0-OGG-CF010-CALLER-OWNERSHIP-CROSSCHECK-STATIC-01`
- **分類:** `OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY`
- **対象:** `0x005CF010` の未整理だった残り2呼出元 `0x005CFA10`（CALL site `0x005CFC2F`）および `0x005D1490`（CALL site `0x005D1572`）。比較対象は前回の `0x005CF4D0`（CALL site `0x005CF5BE`）。
- **前回との差分:** 前回21時台に報告した「親 `0x005CF4D0` のエラー時ローカルシリアル配列未解放候補」を**ほかの呼出元へ一般化してはいけない**と独立確認。今回の2経路は配列の生成・破棄契約が異なる。正式不具合件数・正式REA VERIFIEDを増やさない。

## 1. 調査前提・接続・ハッシュ・旧成果

開始時に Desktop Commander Local Compact の `read_multiple_files` を試みたが、`INVALID_ARGUMENT: McpServerError: Session terminated` で取得不能。これは接続障害であり、安全拒否ではない。PC本体の電源・オンライン状態、最新MASTER/規約/QUEUE/PROGRESS/owner/active.lock、CPU/RAM、既存RUNの最新状態は**未確認**である。PCへは一切書いていない。

そのため、実在をLibraryから確認したユーザー提供 `Vahren.exe`、`HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip` をモデルのコンテナへコピーし、ZIP内の研究スナップショットMASTER・レーン規約・REAの旧PROGRESS、検索README・BUILD_MANIFEST・SQLiteを読み取り専用で確認した。検索DBは**2026-10-21のスナップショット**であり、最新PC正本ではない。

| 証拠 | SHA256（一致確認） |
|---|---|
| 原作EXE | `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` |
| オフラインZIP | `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2` |
| 検索SQLite | `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF` |

ZIP全34項目CRC正常、SQLite `PRAGMA integrity_check=ok`。旧ZIPのREA PROGRESSは**2026-10-09時点15/16**、前回会話で報告された正式VERIFIED64件は**今回PC正本から独立照合できない**ため加算・置換しない。前回21時台の既存研究IDは `REA-OFFLINE-20261028-21H-P0-OGG-SERIAL-EARLY-RETURN-OWNERSHIP-STATIC-01`。その証拠は別件として保持し、上書きしない。

## 2. 新規確認A：再生側 `0x005CFA10` はシリアル配列を要求しない

Ghidra保存DB上の `0x005CF010` への直接CALLは、`0x005CF5BE`、`0x005CFC2F`、`0x005D1572` の3件。各E8相対CALL先を原作PEで独立計算した。

`0x005CFC2F`の直前に、次の実命令が存在する。

```asm
005CFC25  PUSH 0          ; param_5 (count pointer) = NULL
005CFC27  PUSH 0          ; param_4 (serial-list pointer) = NULL
005CFC29  PUSH EDX        ; Vorbis setup state
005CFC2A  PUSH EAX        ; Vorbis info state
005CFC2B  PUSH ESI        ; decoder
005CFC2C  LEA EAX,[EBP-2Ch] ; first page in EAX (custom ABI)
005CFC2F  CALL 005CF010
005CFC34  ADD ESP,14h
005CFC37  TEST EAX,EAX
005CFC39  JNE 005CFDC9
```

`0x005CF010`の擬似Cでも `if (param_4 != (int *)0x0)` の下にシリアル配列の追加・重複検査がある。したがってこの再生中呼出しでは**任意のBOSシリアル一時配列を生成せず**、前回の「呼出元所有配列がエラー時に漏れる」という論点はこのサイトへ適用されない。戻り値が非0なら`0x005CFDC9`の共通エピローグへ分岐して、そのエラー値を返す（分岐ターゲットを機械語で検証）。

## 3. 新規確認B：初期化側 `0x005D1490` は一時配列を両結果で解放

`0x005D14C9`/`0x005D14CC`でローカル配列ポインタ`[EBP-08h]`・件数`[EBP-0Ch]`を0で初期化。`0x005D1562`/`0x005D1569`から**ローカル変数へのアドレス**を引数へ積み、`0x005D1572`で`0x005CF010`を呼び出す。これは再生側のNULL渡しとも、再帰索引側の配列所有とも異なる。

```asm
005D1577  MOV EBX,[EBP-08h]  ; CF010から返った一時配列を退避
005D157A  MOV EDI,EAX        ; 元のステータスを保存
005D1582  TEST EDI,EDI
005D1584  JNS 005D1597       ; 成功側へ
005D158D  CALL 005CFE00     ; エラー時のdecoderリソース破棄
005D1595  JMP 005D1610      ; 配列の共通後処理へ合流
  ... 成功時の索引構築 ...
005D1609  MOV DWORD PTR [ESI+58h],1
005D1610  TEST EBX,EBX      ; 成功側もここへ落ちる
005D1612  JE 005D161D
005D1614  PUSH EBX
005D1615  CALL 005B71E8     ; _free
005D161D  MOV EAX,EDI       ; 元のステータスを戻す
```

`0x005D1490`のGhidra保存擬似Cには `Removing unreachable block (ram,0x005d1614)` と表示され、疑似C本文の共通`_free`が実質欠落している。しかし、**PEのJMP、成功側のフォールスルー、TEST/Jcc、_freeのE8 CALLは実在**し、到達可能である。これは擬似Cだけに依存すると誤判定する典型例。少なくとも今回の入口からの正常復帰とエラー復帰では、一時配列ポインタが非NULLなら同じ`_free`へ到達する。`0x005CFE00`の内部解放と、呼出元スタック上にあるシリアル配列の`_free`を混同しない。

**留保:** `_calloc` 失敗やそれ以前の不正メモリアクセスで例外停止したケースは通常returnしない可能性がある。今回の結論は**通常の制御フローで分岐してエピローグへ到達した場合**に限定。_calloc関連は既知の別VERIFYと重複して新規数には数えない。

## 4. 前回のリーク候補との厳密な対照

| 対象呼出し | `CF010`へのシリアル配列引数 | エラー時の局所配列の後処理 | 判定 |
|---|---|---|---|
| `0x005CF4D0` → `0x005CF5BE` | ローカル配列アドレスを渡す | `0x005CF5CB`で共通returnへ直行、成功側`_free`を飛び越える | **前回のVERIFY候補を維持** |
| `0x005CFA10` → `0x005CFC2F` | `NULL, NULL` | この呼出しでは局所シリアル配列を確保しない | **前回リスクを非適用** |
| `0x005D1490` → `0x005D1572` | ローカル配列アドレスを渡す | `0x005D1610`共通出口、非NULLなら`0x005D1615`の`_free` | **通常return時の局所リーク疑義を否定** |

これは「新たな2つのメモリリーク」ではなく、**既知の所有権問題の適用範囲を1つの呼出元へ狭める重要な反証**。最新PC正本で重複ID照合前なので正式統合しない。

## 5. 実施検査・新規VERIFIED・Golden

`verify_rea_offline_20261028_22h_ogg_caller_ownership.py`は**原本を実行せず**、PE32 VA→rawファイルオフセットの自前変換・命令バイト照合・E8 CALL相対変位・Jcc/JMP分岐ターゲット・SQLite CALL索引・擬似Cハッシュの独立監査のみを実行する。**89/89 PASS**（初回）。別Pythonプロセスから再実行し、保存済み証拠の読み戻し比較を実施する。

関数別REAの5証拠区分：`info=INDEX_ONLY`、`pseudo=INDEX_ONLY+PE比較`、`assembly=TARGETED_NATIVE_PE`、`callers=INDEX_ONLY+E8`、`callees=INDEX_ONLY+E8`。**REA正式5種完成0関数、新規正式VERIFIED0件**、正式TODO/VERIFY/BLOCKED変更0/0/0。原作ゲームGolden実測0件、strict MATCH=`NOT RUN`、完全複製率未測定。先行正式VERIFIED64件は過去報告値であって最新版照合結果ではない。

## 6. 安全・未同期・再開位置

新規Ghidra/REA起動0、原作ゲーム実行0、Work使用0。CPU負荷、RAM、PC lockとPC正本の更新状況は未確認。今回の独立監査所要時間は証拠JSON参照（研究全体の時間は未計測）。原本、MASTER、QUEUE、PROGRESS、既存run、他レーン、Git、公開先、スケジュールは変更しない。

**次のP0:** `0x005D1490`の初期化時`_calloc`結果の異常経路と`0x005CFE00`の終了契約、`0x005CF4D0`の局所配列所有の例外・早期return、`0x005CF320`のEOF/読込エラー伝搬を限定調査。PCが復帰したら、最新MASTER・レーン規約・REA queue/progress/runs/evidence、owner・lock・研究ID・SHA・衝突を先に確認し、非重複REA所有資料だけ一度同期する。これらは`OFFLINE-UNSYNCED`のまま保持する。
