# Ghidra保存済み静的証拠：RNG・シャッフル・ターゲット選択の独立互換監査（2026-10-10）

**状態：READ-ONLY保存済み証拠の再照合＋dev_labへの実装契約。新規Ghidra/EXE起動なし。**
対象ver0.67同梱Vahren.exeの隔離済み証拠。SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` は既存`RUN_RESULT.json`のstart/end記録で確認済みであり、この回で原本を再hashし直していない。

## SDC-01 | shuffle内の28-byte strideと実swap 24-byte（T031）

- `runs/20261009T213635897Z/479A30_procedure_assembly.json` のGhidra `ev_2e6b35f821850d3520355b4c13d985d1716da9d16125603c4e06490b2c82eb48` を再照合。
- `0x479A68`: ESIを初期+0x1Cし、`0x479B19`でも各iterationで+0x1C、すなわち**要素間隔28byte**。
- `0x479ABD..0x479AC6`:選択jは`EDX`剰余から28byte stride算出。`0x479ACD..0x479B16`の実swap MOVは+0,+4,+8,+0xC,+0x10,+0x14の**6 dword=24byteのみ**。元データの`+0x18..+0x1B`（末尾4byte）はこのswap内にMOVがない。
- `0x479A85`の1回目CRT randを含み、`upper=i+1`が0x7FFFより大きいと`0x479A97`で追加draw、`0x479A9C..0x479AB1`で15bit連結と比較して`0x479AB7 DIV EBP`の剰余をjに採用する。
- draw境界: 上限32767なら当該step1回、32768なら2回、0xFFFFFFFFなら3回（uint32拡張mask）。51要素は50回。`dev_lab/src/hakushin_compat/native_vector_shuffle_subset.py`を別純粋バイト模型として作成し境界試験4件合格。
- **VERIFY**: 末尾4byteのフィールド意味。これを『std::stringの特定メタデータ』と即命名したり、既存のPython object/list swapを無条件置換しない。ゲームのUIで可視な並びがこの内部24byte swapと一致するかは原作実測0件。

## SDC-02 | index(count)の末尾foldとpushRand2の疎な15bit lattice（T031/T006）

- 既存owner `data/T031_RANDOM_EVENT_SCHEDULER.md` §15（`0x4B05EF`からのindex clamp）と§19（`0x4AEE1F..0x4AEE5F` pushRand2）、保存native `exe/T031_RNG_INDEX_PROBE.txt`・`exe/T031_RNG_CORE_PROBE.txt`をcross-check。
- index(list,i): N>0でi<0は0、0<=i<Nはi、i>=NはN-1。よって2つの**異なる**raw index N-1/Nが同一末尾要素になる。pre-draw scriptは`value>count(list)`だけを再抽選するのでraw Nも残り得る。
- `pushRand2`は0..2^31-1範囲のuniform int32でなく、MSVC rand15値kに対し`floor((2^31-1)*k/32768)`。k=0なら0、1..32767なら`65536*k-1`。例えばk=1→65535、k=32767→2147418111。幅2/4/8で剰余をとる場合、k>0の値はN-1側へ偏るが、実mod命令・UI到達はVERIFY。
- `dev_lab/src/hakushin_compat/script_rng_quirks.py` で非空index clamp、単一pre-draw、pushRand2格子を分離し、人工契約テスト5件合格。これを原作実ゲームの最終イベント/人数結果とは呼ばない。

## SDC-03 | primary/fallback selectorはprimary最短距離を保持して比較（T013）

- 保存済みnative `exe/T013_TARGET_SELECTOR_PROBE.txt` の0x514D60..0x514F0B、`data/T013_AI.md`の同距離tie・2-pointer返却節を照合。
- primary SimpleUnit（owner+0x48）内ではstrict `newDistance<bestDistance`の時だけbestを更新、同距離で先勝ち。primary bestがcandidate+0x18C範囲内ならそのままfast return。
- primaryが範囲外でも初期best pointer/distanceをresetせず、fallback SimpleStaticUnit（owner+0x58）は**今のbest距離より短い場合だけ**更新する。fallbackが同距離/遠い場合もnative helper出力bestは元primaryに残り得る。
- native out[0]が最終best、out[+0x10]がprimary最短（primary無し時は最終best）なので両pointerは異なり得る。上位search coreはこれをUnit+0x1E574 / +0x1E580へ別々に保存する。
- **重要な修正**: 以前の`dev_lab/targeting_subset.py`はrange外primaryを忘れてfallbackを無条件採用し、最後の2-pointer情報も失っていた。今回helperの静的契約として修正。'out-of-range primary' helper出力を即「戦闘で攻撃対象採用」とは呼ばない。既存＋新規テスト9件合格。

## SDC-04 | search refresh閾値とselector呼出は別条件（T013）

- 保存Ghidra `0x57B870` run=`20261009T225741694Z` のpseudo `ev_4767a901e9f4b9ad1fc38d59a2f36a6a4a1ef4cc22287abb8e74c97f094aa2dc` とassembly `ev_89e3a86b53663da35b8cadf02226f2163996275f1d24f93e37e8009fc50f048c`を使用。
- `counter>=B`ならjitters用randを1回引くが、primary selector `0x514D60`は`Unit+0x1E570` cached pointer **NULL時だけ**call。cached pointer非NULLなら距離更新経路へ進み、同じrefresh tickでprimary選択し直さない。ただしsupport capability `+0x137`があれば独立support builderに進む可能性はある。
- `dev_lab/synthetic_ai_scene.py`では旧full_searchesという曖昧な語をrefresh_checksへ変更し、selector_invokedを独立にtrace。合成1v1の120tickでrefresh4回・primary selector2回・jitter直接draw4回。チーム割当はsynthetic、実native gameplay match0。

## SDC-05 | confusion時の攻撃/支援は別々のCRT呼出（T013）

- 直接CALL site: `0x57B8FE` jitter、cachedTarget=NULLかつUnit+0xC8<0のみ `0x57B940` primary confusion、Unit+0x137非0かつ+0xC8<0のみ`0x57BA10`support confusion。これらのほかcallee内のrandは本式に含めない。
- threshold到達時の当該関数**直接**draw数は `1 + (confused && cachedTargetNull ? 1 : 0) + (confused && supportCapable ? 1 : 0)`。threshold未満は0。攻撃側は通常opponent、混乱missならown側。支援側は通常own、混乱missならopponent。2つの混乱判定は別乱数であり一致するとは限らない。
- `dev_lab/src/hakushin_compat/confusion_refresh_subset.py` でdirect-draw順序・side決定だけを実装、単体テスト6件成功。未知の内部helper乱数、別経路でのreseed、battle実ダメージは未観測。

## 進捗の正しい扱い／再開条件

- 既存REA重点はWave1=16/16、Wave2=10/10、Wave3=10/10、Wave4=3/12、合計 **39/48 STATIC VERIFIED**。本追加解析で**新規Ghidra機能取得0件**。スクリプト・逆アセンブル保存済み証拠の解釈を精密化したのであり、EXE全体の解析率・原作とのgolden PASSではない。
- `run_decompile.ps1`以前のSAFETY_REFUSAL、手動exporter拒否、0x5710C0..0x571500等の拒否は変更なし。別shell/tool/Remoteへの再ルーティングによる逆解析実行はしない。
- 旧EXE実ゲームTARGET OBSERVED 0、新エンジンREIMPLEMENT MATCH 0。既存QUEUE/PROGRESSはWindows EPERMのSTALE可能性あり、書換・権限変更なし。MASTER/他A-E/Git/MCP/automation/原本の編集なし。
- 次の有効な契約golden候補：28vs24物理shuffle、32767/32768追加draw、index(N-1)/index(N)重複末尾、pushRand2のpow2剰余、primary-rangeを挟むfallback距離の順序、cached-targetありのrefresh、混乱時primary/support独立draw。**すべて合成fixtureはSOURCE側、実機原作実測はNOT RUN**。

