# 迫真戦記 ver0.67｜REA 2026-10-25 00時台 P0：ArmyChipの遅延破棄キュー／仮想デストラクタ呼出経路
研究ID: `REA-LOCAL-20261025-00H-P0-ARMYCHIP-DEFERRED-OWNER-VCALL-GATE-STATIC-02`
状態: **PC-SAVED / STATIC / VERIFY / NOT READY**。原作実機Golden未実行、正式REAのVERIFIED増加0。
対象原作EXE SHA256: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`
参照検索DB: 統合V9 `HAKUSHIN067_UNIFIED_V9_20261023.sqlite` SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`
両SHAは今回専用監査で実ファイル再計算一致。旧2026-10-21 search.sqliteは入口・互換情報だけを参照し、新規研究はV9に統一。

## 先読・非重複照合
MASTER_LEDGER、ANALYSIS_LANES_PROTOCOL、REA README/QUEUE/PROGRESS、既存run/syncログ、前回2026-10-24 23H子デストラクタ証拠、V9研究入口と旧検索manifestを先読。
保存済み`progress_sync_20261011T153958076Z.json`はWave1～5=64/64・21 runs。QUEUE/PROGRESSは既知のrename EPERMでstale。今回の結果をこの64に加算しない。
前回までの既知: 親デストラクタ`0x005B09A0`は子ポインタvectorの保存領域をfreeするが、子オブジェクトを直接破棄しない。子仮想デストラクタ`0x005B1310`は本体`0x005B1330`と条件付き本体メモリfreeを持ち、E8直接callerは0件だった。
**今回の新規:** 子が通る除外・破棄キューと、キューを走査する仮想デストラクタ呼出命令を原作PE実バイトで接続した。

## 新しい静的連鎖：ArmyChipの破棄予約と実行
1. 親 `0x005B0A50` の子処理で `0x005B0B5C` は子vtable`+0x08`を呼ぶ。ArmyChip型では`0x00431910`で1を返すため、`0x005B0B65 PUSH 0 / 0x005B0B67 PUSH ESI / 0x005B0B6B CALL 0x004C22B0`へ進む。この呼出しは管理側の登録vectorから子ポインタを外すが、ここでは子のdestructorを呼ばない。
2. 続く子vtable`+0x44`はArmyChip型では`0x0043B5A0`で0を返すため、`0x005B0BA0 PUSH ESI / 0x005B0BA4 CALL 0x004C2440`へ進む。`0x004C2440`は管理vector`+0x44/+0x48`へポインタを追加する。**解除は即時deleteではなくキュー登録**と区別する。
3. 管理ループ `0x004C24B0` の終盤では管理vector`+0x44/+0x48`を列挙し、NULL以外の要素について`0x004C281F MOV EAX,[ECX]; 0x004C2821 MOV EDX,[EAX]; 0x004C2823 PUSH 1; 0x004C2825 CALL EDX`を発行する。ここで`EDX`は要素vtable**先頭スロット+0x00**である。
4. ArmyChipのvtable `0x0063AE74` の+0x00は `0x005B1310`。よって**その型とvptrが保持された子がこのキューに入って到達した場合**、`0x004C2825`は子仮想デストラクタを削除フラグ1で呼び出す。実ゲームでの全到達条件、同一マネージャへの実際の継続関連、例外による途中中止はVERIFY。

## 別経路：親を遅延キューへ積む分岐
`0x005B0B23 PUSH 1 / 0x005B0B25 PUSH EBX / 0x005B0B29 CALL 0x004C22B0`は親ポインタを管理vector`+0x54/+0x58`へ追加する経路（フラグ1）。
管理ループ`0x004C24B0`では`0x004C27AE`で該当要素vtable`+0x14`の関数ポインタを取得し、`0x004C27B3`で呼び、戻り値AL==0の場合だけ`0x004C27BB MOV EDX,[EAX]; 0x004C27BD PUSH 1; 0x004C27C1 CALL EDX`でvtable+0x00の削除を呼ぶ。親の述語がどの条件で0になるかは今回未解析。
`+0x54`は条件付きの**遅延破棄候補キュー**、`+0x44`はNULLガードのみでデストラクタを呼ぶ**別の破棄キュー**。この差を一律deleteへ畳み込まない。


## 独立静的検証
- 追跡用監査 `REA_20261025_00H_P0_ARMYCHIP_OWNER_CHAIN_AUDIT.py`: **60/60 PASS**。PE全命令境界・親CALL site・仮想関数表・管理関数3本の直接CALL一覧・V9 direct-call index・擬似C存在/ABI未証明・SHA・SQLite quick_checkを照合。
- 厳格な2つの破棄gate監査 `REA_20261025_00H_P0_ARMYCHIP_DTOR_VCALL_GATE_AUDIT.py`: **35/35 PASS**。0x004C27AC～0x004C27C6と0x004C2818～0x004C282Aの命令バイト、子vtable+0の実ポインタ、親/子の登録・解除CALL siteを再計算。
- 両監査は一部の原作ハッシュ・CALL siteを重複確認するため**60+35を新関数数と解釈しない**。対象関数は従来の既存擬似Cを再利用、新REAの正式5種証拠セット0、VERIFIED+0、正式TODO/VERIFY/BLOCKED書込差分0/0/0。
- 0x004C24B0内の`0x004C24E1`と`0x004C2886`も手前8命令にPUSH 1があるため60/60監査の単純候補抽出には入ったが、実際はvtable+0xACへの描画系CALLであり**削除対象から除外**。厳格監査により破棄CALL siteは`0x004C27C1`と`0x004C2825`の2つに限定。
- 先に試行した探索版 `REA_20261025_00H_P0_ARMYCHIP_DEFERRED_QUEUE_AUDIT.py` は「0x004C22B0に直接+0x5Cオペランド命令がある」と誤って要求したため **55/56 FAIL**。探索JSONが先に書かれた点を記録し、**正式成功・新発見として二重計上せずSUPERSEDED**。旧ファイルを削除/上書きしない。
- 他の既存`0x004C20D0`のV9疑似Cも読取。管理+0x2C active vectorの要素に対するRTTI除外付きの仮想破棄候補があり、今回2つのキューとは別経路。Chara継承/具体的到達性は未検証。

## 次回のVERIFY（P0）
1. `0x004C24B0`を呼ぶ所有者と親`ArmyChipBuilder`の保持するmanagerが**同一インスタンス**か、途中で共有/変更されないかをcaller・オブジェクト生成元から照合する。
2. `0x004C2825`でのECX child vptrが`0x0063AE74`のままか、派生型・破壊済みポインタ混入・重複登録がないかを追跡。
3. 親の遅延キュー`+0x54`のvtable`+0x14`判定を個別に解明。キュー0/1/複数件・同一要素重複・途中中断のGolden条件を設計（**ゲーム実測PASS=0**）。
4. 親ポインタvector/管理側active/clear/delayed 3種を混同せず、解放順序・二重解放・owner責任を最終特定する。

## 安全・実行状況
接続: Desktop Commander Local CompactでWindows研究PCに接続成功。REA active.lockなしを確認。管理PCの空き物理メモリ約15.98GiB、Java/Ghidraプロセスの検出なし。PC全体のCPU負荷・研究全体の所要時間は不明。
既存REA/Ghidra/ゲームの新規起動0回。安全拒否済み`0x004BC9C0`検索CLI、`0x5710C0..0x571500`、Wave6/REAエクスポートを別tool/shell/ZIP経路で再試行せず。
原本ZIP/EXE/SAVE、MASTER、QUEUE、PROGRESS、他lane、既存runs、Git、Work、スケジュールは無変更。書込はREA所有`decomp_task`内の新規独立ファイルのみ。Golden/strict MATCH=0、完全複製率未測定。

