# 迫真戦記 ver0.67 REA｜P0 D3DX補助初期化の幾何入力・終了到達性
研究ID: `REA-LOCAL-20261027-08H-P0-D3DX-CAMERA-GEOMETRY-STATIC-01`
日時: 2026-10-27 08時台 JST。状態: PC-SAVED / STATIC / VERIFY / NOT READY。Golden: NOT RUN。
対象SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
旧DB SHA256: 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF
統合V9 SHA256: 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE

## 先行研究との境界
07H報告では 0x00559990 の無上限ループ・FPU両誤差悪化停止と、float32停滞の合成例をSTATIC/VERIFY管理。今回はそれらを再取得・二重加算せず、**ループに渡る固定幾何入力を原作PE機械語から別途復元**した。原作実行、REA/Ghidra再実行なし。
検索CLIで `function/callers/callees/related 0x00559990` を確認。直接親 `0x00559690`、CALL site `0x00559830` は旧DB/V9双方で一致。関数長915バイト、最後のRETは `0x00559D22`。

## NEW STATIC：交差平面は正常な非退化 z=0 平面
`0x00559A2A..0x00559A73` で組立てる3点を、x87のfld/fst/fstp・pushに伴うESP移動を追って復元した。
- 点A = (-100, +100, 0)
- 点B = (-100, -100, 0)
- 点C = (+100, -100, 0)
3点は非共線で、平面方程式は **z=0**。`0x00559A73` のIAT `0x006092CC` は `D3DXPlaneFromPoints`。
関数先頭の `0x005599D5..0x00559A1C` は、視点の上方向(0,1,0)、原点を見る基準点(0,0,0)、スクリーン座標の端点(0,0,0)・(0,0,1)を用意する。
反復内 `0x00559B77..0x00559BA0` は Eye=(0,0,z)、At=(0,0,0)、Up=(0,1,0) の視点行列を作成。初期z=-2.0、各反復で約0.01減少。
`0x00559BCF` と `0x00559BFE` の2回の `D3DXVec3Unproject` は、同一画面位置(0,0)で深度0/1の2点を逆投影。続く `0x00559C1D` は `D3DXPlaneIntersectLine` でz=0平面との交点を計算し、結果のx/yを `0x00559C1F`、`0x00559C42` で読み出す。
この各ベクトルの割当は呼出し規約に沿う静的再構成であり、D3DX DLL実呼出しの観測ではない。

## NEW STATIC：透視投影のパラメータ
PE定数: `0x0063B0E0`=45.0 (f64)、`0x0065C4C0`≈π/180、`0x0063B154`≈0.1 (f32)、`0x0063B0EC`=10.0 (f32)。
`0x00559B25` のFLD1によるaspect=1とともに、`0x00559B43` の `D3DXMatrixPerspectiveFovLH` へ渡す。従ってFOV≈45°、aspect=1、near=0.1、far=10。初期視点は面z=0から距離2で、near/far区間内にある。
IAT `0x006092F4=D3DXMatrixLookAtLH`、`0x006092DC=D3DXVec3Unproject`、`0x006092E4=D3DXPlaneIntersectLine` もPEインポートで独立照合。

## NEW SYNTHETIC：通常有効なviewportでは短時間で停止するモデル
**条件**: D3DX APIが正常終了・行列が非特異・viewport原点(0,0)、幅/高さ>0、有限値、深度範囲0..1。上記の固定幾何から理想的な投影を計算すると、視点距離 d=-z のとき
```
交点 (x,y,z) = (-d*tan(22.5°), +d*tan(22.5°), 0)
e1 = |-1-x|, e2 = |1-y|  → e1=e2=|1-d*tan(22.5°)|
```
理想的な最良距離は `d=1/tan(22.5°)≈2.41421356`。初期2.0から約0.01ずつ増えるので、通常有限値なら両誤差がいったん減り、その後ともに増加する。
保存済みPEの定数を読み、走査値を反復ごとにfloat32丸めする**合成幾何モデル**では、n=41で z≈-2.409999609（誤差≈0.00174545）、n=42で z≈-2.419999599（誤差≈0.00239669）となり、n=42の検査で両方が悪化して終了する。保存候補は前回サンプルの `z≈-2.409999609`。
これは**DirectX本体・実ゲームの浮動小数点丸め、viewport値、環境状態を再現したGoldenではない**。反復42回の断定は行わない。

## 07Hのハング懸念の絞り込み
「無制限反復」は機械語上の特徴として維持。ただし通常の有効な幾何入力を上記通り解釈する限り、無限ループは必然ではなく、合成モデルではむしろ速やかに停止する。
重点VERIFYを **GetViewport失敗/ゼロ寸法/非標準原点、D3DX逆投影失敗・NaN・平行線で交点未更新、射影行列非特異性** に限定して深掘りする。 `0x00559C1D CALL EBX` の戻り値は直後の `0x00559C1F FLD` より前に検査されない。
`0x00879838` は `0x00559D11` で計算値が書かれ、既存索引では `0x004C3C20` などが読取。画面変換の基準値候補として位置付け、実際のデバイス状態・厳密な値・不具合発生はVERIFYとする。

## 監査・進捗・保存
対象限定Capstone ASM、PE IAT・定数、旧/統合V9 SQLite quick_check、直接CALL、07H=58/58証拠、最終progress_syncの既存64/64をread-only照合。新監査 **74/74 PASS**。コードはowner内 `REA_20261027_08H_P0_D3DX_CAMERA_GEOMETRY_AUDIT.py`、機械証拠 `REA_20261027_08H_P0_D3DX_CAMERA_GEOMETRY_EVIDENCE.json`。
5種: info=INDEX_ONLY / pseudo=INDEX_ONLY / assembly=TARGETED_PE_NATIVE / callers=INDEX_ONLY / callees=INDEX_ONLY。新規5種完全取得0、新規正式VERIFIED0。旧64件保持、正式TODO/VERIFY/BLOCKED書込差分各0。原作Golden PASS0、strict MATCH/完全複製率は未測定。
研究PCからのread-only検査時にVahrenプロセスが稼働していたため、ゲーム操作・APIフック・REA・Ghidra・Workは行わず、対象コピーのみ静的に読んだ。CPU負荷は未計測。事前空きRAM約16.69GiB、active.lockなし。安全拒否・接続障害なし。MASTER/他レーン/QUEUE/PROGRESS/既存runs/Git/スケジュールは変更していない。
次回: `0x00559A28` vtable+0xC0のGetViewport戻り値・出力値使用、`0x00559C1D` の交差失敗時pOut規約、`0x004C3C20` 等による `0x00879838` 消費者の追加ASM照合。すべて本owner範囲内で静的調査する。

