# 迫真戦記 REA｜2026-10-29 05H Ogg read負値ABI・fill巻戻り・state遷移
研究ID: `REA-LOCAL-20261029-05H-P0-OGG-NEGATIVE-READ-STATE-STATIC-01`。
状態: **PC-SAVED / STATIC / VERIFY / NOT READY**。正式REA新規VERIFIED=0、原作Golden実測PASS=0。

## 開始時照合・重複回避
- Desktop Commander Local接続成功。MASTER_LEDGER、ANALYSIS_LANES_PROTOCOL、REA README/QUEUE/PROGRESS/保存run、2026-10-21検索基盤README/BUILD_MANIFEST、旧syncと直近04H証拠をread-onlyで照合。
- 既存 `logs/progress_sync_20261011T153958076Z.json` はWave1～5合計 **64/64 STATIC VERIFIED**。QUEUE/PROGRESS表示はWindows rename EPERMにより古いため更新も再計上もしない。
- 2026-10-26 03HはOggDecoder fill本体・memset/loop/戻値無視、10/26 04Hは読込ゼロのloop再試行、10/29 04Hはseek復帰失敗コードを破棄する分岐を既報告。今回は **負のread結果を符号なし累積数として扱う経路** と **void誤推定の別関数ABI** を補強する。既知loop問題を別不具合と二重計上しない。
- 隔離研究EXE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、検索DB SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`、SQLite quick_check=ok。開始時active.lockなし、Java/Ghidra先行プロセスなし。

## P0-A｜0x005D12E0 は Ghidra void 宣言と異なりEAXを返すwrapper
- 2026-10-21 `search.py function 0x005D12E0` の機械擬似Cは `void FUN_005d12e0(...7 args)` と宣言し、`FUN_005d0fb0(...7 args,0,0)` の結果を捨てたように見える。
- 原作隔離PEの命令は `0x005D12EC/EE PUSH 0/0`、`0x005D12F0..1302` の7引数積み込み、`0x005D1303 CALL 0x005D0FB0`、`0x005D1308 ADD ESP,0x24`、`0x005D130B POP EBP`、`0x005D130C RET`。**CALL後にEAXを書き換えずreturn**する。9個の32bit stack引数を処理するcdecl相当。
- `0x005D0FB0` の `0x005D0FBA/FC0` は内部state<2で**-131**、`0x005D0FFA CALL 0x005CFA10`が-2なら `0x005D1002/1005`→`0x005D12CF XOR EAX,EAX` で **0（EOF）**、その他の非正値は `0x005D100B/100D/100F..1015` からそのままreturn。通常成功時は `0x005D12B7/BA` でchannel×bytes-per-sample×frame数をEAXへ返す。
- `0x005D0FB0` 内の `0x005D1076 CALL EAX` は検索DB上では**未解決間接CALL**であり、非NULL user callbackの呼出し先を固定しない。この関数の擬似Cは機械生成で、フルパスの正しさは原作Golden未測定。

## P0-B｜0x00501F10 はread負値を0扱いせず、unsigned加算後に成功帰還し得る
- 初期guard: `0x00501F19 CMP [ECX+5],0`で初期化フラグを確認し、`0x00501F26..2D`でoutputBuffer非NULLを確認する。正常入口ではoutputBufferの要求範囲を先にmemset(0)、EDI=0で開始。
- `0x00501F91 CALL 0x005D12E0` → `0x00501F96 MOV ESI,EAX` → `0x00501F9B TEST ESI,ESI` / `0x00501F9D JNE 0x00501FBF`。**0のみ**EOF/loop分岐へ行く。負値（-131/-137/-128など）も非0としてread処理継続。
- `0x00501FC2 ADD EDI,ESI` は32bit加算。初回readが-131なら EDI=0xFFFFFF7D（符号なし解釈で4,294,967,165）。`0x00501FC4 CMP EDI,requestSize` / `0x00501FC6 JAE` は**unsigned比較**のため、要求サイズ1～8192などでは完了扱いへ進む。
- `0x00501FE6 MOV [EAX],EDI` はoptionalActualBytesポインタが非NULLなら巻き戻った巨大全バイト数を返し得る。 `0x00501FEA MOV AL,1`で成功フラグを返す。通常のOgg再生入口 `0x005023A0` ではoptionalActualBytesがNULL（10/26 03H既報）で、実際に巨大数が外へ出たという証拠ではない。エラーパスの再生出力はゼロ埋めされたbufferになり得る。
- 上記は **負のread EAXが本fillに到達する場合の条件付き静的推論**。現場での負値発生頻度、アプリのフリーズ、異常メモリアクセス、原作の聴感異常を実測したものではない。unsigned算術独立モデル9条件を確認したが、原作プログラム実行ではない。

## P0-C｜0x005CF970 はESI依存のdecoder状態3→4ゲート
- Ghidraは `undefined4 FUN_005cf970(void)` と表示するが、ネイティブは **ESIを暗黙のdecoderポインタ**として `[ESI+0x58]` を参照する。通常C形式の引数0個だけで単独再実装すると呼出規約を失う。
- `state>3`なら `0x005CF978 XOR EAX,EAX`で0、`state<3`なら `0x005CF97D MOV EAX,0xFFFFFF7F`で**-129**を返す。**state==3**のみ `0x005CF9A1 CALL 0x005D5BD0` へ進み、非0なら `0x005CF9AD`で**-137**。成功時は `0x005CF9BC CALL 0x005D4900`、2つのdouble累積値を0、`0x005CF9CC`でstate=4、`0x005CF9D3`で0を返す。
- `0x005D5BD0` は `0x005D5BDE CALL 0x005D57C0`が非0なら処理片付け・return 1、成功ならreturn 0。この下位failureの詳細条件は次回VERIFY。
- 呼出元 `0x005D0B60` の **2箇所** `0x005D0B8A/0x005D0D67 CALL 0x005CF970` に続く `TEST EAX,EAX; JNE` は、state不正または初期化失敗時の負returnを上位へ保持。前回04Hのseek失敗でのerror保持と区別する。

## 索引・監査と証拠等級
- CLI: `search.py function` 0x005D12E0/0x005D0FB0/0x005CF970/0x005D5BD0/0x005D4900/0x005CFA10 と関連caller/callee、旧DB direct/indirect CALL、隔離PE32のCapstone disassemblyで命令とCALL siteを独立照合。
- 新監査 `REA_20261029_05H_P0_OGG_READ_NEGATIVE_AUDIT.py` は **80/80 PASS、0.508秒**。内訳はハッシュ/lock/旧64件/既存04H/DB健康、8対象関数、48対象命令、8CALL site、9静的unsignedモデル。失敗0。
- 5種証拠: info=SEARCH INDEX、pseudo=SEARCH INDEX+PE誤型対照、assembly=TARGETED PE、callers=SEARCH INDEX+native site、callees=SEARCH INDEX+native site。**正式REA 5種フル証拠新規0、正式VERIFIED追加0、既存64/64維持。正式TODO/VERIFY/BLOCKED差分0/0/0。**
- 独立検証課題は今回発見群として①read負値がfillへ達する入力と結果、②state3初期化失敗の条件と上位保持。正式キューやREADYを更新しない。

## 原作Golden試験条件（DESIGN/NOT RUN）
- 初期化済みOggDecoderで正常read>0、EOF相当-2→0、state<2で-131、その他デコード失敗負値をそれぞれ分離し、fillのAL、actualBytes、bufferゼロ埋め、上位消費を比較する。requestSize=1/4096/8192、optionalActualBytes NULL/非NULLを別々に扱う。
- state3→4成功、state2→-129、state3で0x005D5BD0失敗→-137、state4 no-op 0 を比較。PCコピーで実行許可・安全条件を確認するまで試験しない。
- 原作Golden PASS **0**、strict MATCH **NOT RUN**、完全複製率 **未計測**。新規REA/Ghidra・原作ゲーム・Workは実行していない。

## 記録・次のP0
- 研究対象PCはオンライン。開始時RAM空き約16.44GiB、CPU負荷は未測定。独立静的audit0.508秒、研究全体所要時間は未測定。
- 保存対象はREA owner内新規AUDIT.py/EVIDENCE.json/STATIC.md/READBACK.mdのみ。原本ZIP/EXE/SAVE、他レーン、MASTER、既存RUN、QUEUE/PROGRESS、検索DB、Git、スケジュールは一切書き換えない。10/28 17～22H Library未同期成果は未統合のまま保留。
- **再開位置:** `0x005D57C0` 非0returnの具体的条件と `0x005D0FB0` の間接CALL site `0x005D1076` の安全な対象同定、負エラーの発生経路を優先。既存二重計上禁止。原作GoldenはNOT RUNのまま。
