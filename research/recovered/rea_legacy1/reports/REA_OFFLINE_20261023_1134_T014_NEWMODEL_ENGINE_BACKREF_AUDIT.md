# 迫真戦記 ver0.67｜REA独立静的解析：NewGameModel ↔ エンジン逆参照

- 研究ID: `REA-OFFLINE-20261023-1134-T014-NEWMODEL-ENGINE-BACKREF-STATIC-01`
- 実施日: 2026-10-23 11時台 JST
- 状態: `OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY`
- 所有範囲: REA独立証拠。MASTER、他レーン、原本EXE、Git、正式QUEUE/PROGRESS、既存スケジュールの変更なし。
- 対象EXE SHA256: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`
- 検索DB SHA256: `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`
- オフラインZIP SHA256: `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`

## 0. 先行確認と境界

- Desktop Commander Local Compactの正本読取は `McpServerError: MCP SSE probe returned 429 from openai.org` により失敗。接続制限として記録。安全拒否ではない。PCオンライン/電源・負荷・owner/lockは不明。
- Libraryから実在確認した `Vahren.exe`、`HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip`、旧`decomp_task.zip`、`decomp_task_offline_rule_20261019.zip` をコンテナへ取得。SHA256・ZIP CRC・SQLite integrity_checkを検証。Ghidra、REA、原作ゲームは実行していない。
- 保存済みのMASTER・プロトコル・旧PROGRESSはZIP内スナップショット。PC正本の現行値ではない。
- 前回の`REA-OFFLINE-20261023-1033-T014-SCRIPTBATTLE-PLAYER-VSLOT0C-STATIC-01`が示した `0x00492A70` は**機械語としては既知**。本研究の新規部分は、その受信者と**NewGameModelへの逆参照**を証拠で特定したこと。3件のvcall自体を新規と数えない。

## 1. 結論：0x00492A70はNewGameModel+0x38へエンジンポインタを格納する

### 参照元の構築

`0x0048A5FB`（`FUN_0048A5B0`）:

```asm
MOV DWORD PTR [EDI+0x08], 0x008BE378
```

この関数の通常のエンジン初期化経路では、`[engine+0x08]`が`GameWindow`（静的アドレス`0x008BE378`）を指す。GameWindowの`+0x08`、つまり`0x008BE380`は別のポインタ格納先である。

`0x00553B5E`で`ESI=0`とした後、`0x00553B74`で`[0x008BE380]=ESI`としてゼロ初期化する経路がある。`0x004B9E50`は`0xB8`バイトのオブジェクトを確保し、`0x004B9EB4`で`FUN_004E4830`を呼ぶ。`0x004B9EB9`で戻り値を`EDI`へ取り、`0x004B9F40`で`[0x008BE380]=EDI`を実行する（確保失敗時はゼロの可能性）。

`FUN_004E4830`のGhidra疑似C・原作機械語は、`0x004E4877`でオブジェクトのvptrに`0x00639490`（`NewGameModel::vftable`）を設定し、`0x004E4870`の`XOR EBX,EBX`に続いて`0x004E48C9`で`MOV [EDI+0x38],EBX`（初期値0）を示す。

### ScriptBattleからの代入

`0x004338FC`: `MOV ESI,ECX`（呼出側のスクリプト処理オブジェクトをESIに保持）。`0x00433E58`から`FUN_00492890`をCALLする。`FUN_00492890`は自前でESIを初期化せず、`unaff_ESI`として使用している。間のCALLがESIを保持することは通常のx86 ABIと整合するが、包括的ABI検証は未完了。

```asm
0x00492A6A  MOV ECX, [ESI+0x08]
0x00492A6D  MOV EAX, [ECX+0x08]
0x00492A70  MOV [EAX+0x38], ESI
```

**通常のポインタ状態におけるデータフロー:**

```text
ESI = Engine
  └─ [Engine+0x08] = 0x008BE378  (GameWindow)
       └─ [GameWindow+0x08] = [0x008BE380] = NewGameModel*
            └─ [NewGameModel+0x38] = Engine*
```

**これは単に新しいDLLを差し込めるという結論ではない。** 正常なScriptBattle経路では、バトル開始処理の前段でモデルからエンジンへ戻る参照が作られる、という**静的証拠**である。GameWindowとNewGameModelは別オブジェクト。

## 2. 代入の前後と呼出条件

`0x00492A35`で`engine+0x1EED40`を判定し、非ゼロの場合のみ`0x00492A3E`から`0x0049D6A0`を呼ぶ。静的疑似C上は単位群の座標`>>5`やマップ領域を巡回・登録する処理であり、3つの仮想CALL直前の準備処理として位置付く。ただし全副作用やvptr不変性は未確定。

その後に既知のvcall 3箇所（`0x00492A4E`, `0x00492A5B`, `0x00492A68`）を通り、正常復帰した場合に`0x00492A70`の逆参照代入へ進む。従って**逆参照代入は3 vcallより後**であり、早期例外・異常終了した場合に実行されるとは限らない。

`0x00492A73`で`[ESI+0x1EED18]`を判定し、`0x00492A79`のJEは`0x00492C75`へ分岐する。非ゼロ側では`0x00492AA9`、ゼロ側では`0x00492D4E`から、ともに`FUN_00564160`を直接CALLする。`FUN_00564160`の疑似Cは多数の状態フラグ・グローバル設定を書き換える。2経路は引数構成が異なるので、**戦闘開始ハンドオフの観測候補**として採録するが、引数のゲーム上の意味・両経路の互換性は未確定。

`engine+0x1EED18`と以前解明したGameManagerの`+0x1EF144`は**異なる基点・異なるフィールド**である。混同しない。

## 3. 検証結果

- 原作EXE SHA256／検索DB SHA256／オフラインZIP SHA256: 全一致。
- ZIP CRC 34/34 PASS、SQLite `PRAGMA integrity_check=ok`。
- 原作機械語指定箇所 **33/33 PASS**（`0x004E48C9`, `0x004B9F40`, `0x00492A70`等）。
- 直接CALL命令の相対先およびSQLite索引: **5/5 PASS**（`0x00433E58`, `0x004B9EB4`, `0x00492A3E`, `0x00492AA9`, `0x00492D4E`）。
- 間接CALLサイトの既存索引照合: 3/3 PASS（**再確認・新規0**）。
- 分岐先の独立再計算: 2/2 PASS。
- Ghidra擬似Cの関数別SHA256: 8/8 PASS（新規正式REA証拠ではない）。
- Python検証器の初回実行時間: 結果JSONの`elapsed_seconds`欄（検証実行単体）。調査全体の時間は未計測、PC負荷は不明。

## 4. 旧REA件数の注意点（今回の重複防止）

旧`decomp_task.zip`および`decomp_task_offline_rule_20261019.zip`の`QUEUE.json`にはWave1=16、Wave2=10、Wave3=10、Wave4=12のフリーズ済み静的検証件数があり、**計48件**。Wave5は`IN_PROGRESS`で`verified_at_freeze`値なし。`function_queue`そのものは64件のうち16件がVERIFIED、48件がTODOと記録されており、Waveのフリーズ集計とは整合しない。旧`PROGRESS.md`はさらに古い15/16である。

したがって、過去チャットで述べられた**「Wave1〜5合計64/64 VERIFIED」は現存するこの旧アーカイブからは裏付けられない**。今回のVERIFIEDへの昇格は0。正本の最新値・対応証拠を確認できるまでは64/64と再断定しない。旧アーカイブの48件を取り消す・上書きするという意味でもない。

## 5. 再現可能な検証とGolden契約（未実施）

コマンド:

```bash
python verify_rea_t014_newgamemodel_engine_backref_20261023.py \
  --exe /path/to/Vahren.exe --sqlite /path/to/search.sqlite \
  --pack /path/to/HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip --out check.json
```

Golden取得の設計観測点：`0x00433E58`前のESI・スクリプト引数、`0x00492A4E`/`0x00492A5B`/`0x00492A68`の受信者とvptr、`0x00492A70`直前のNewGameModel+0x38（初期値0）と直後の値、`0x00492A73`の分岐値、`0x00492AA9`/`0x00492D4E`での実引数、正常復帰時の状態。PC再接続後にowner・許可・環境が確認できた場合に別途実機計測する。**本研究では未計測／Golden PASS=0。**

## 6. 未解決・次回

- P0/VERIFY: NewGameModel+0x38を読む関数／解除・破棄時の初期化元をxrefsとレジスタ別名経路から探索。現段階では`0x00492A70`が唯一のwriterとは断定しない。
- P0/VERIFY: `0x00564160`の各呼出引数の値・所有者・ゲーム状態を区別。戦闘モード差し替えの入口で必要な入力フィールドを整理。
- P0/VERIFY: `0x0049D6A0`の各副作用とESI/ECX受渡し、Player/Enemyのvptr変更の可能性。
- 旧rea run `info/pseudo/assembly/callers/callees`の正式5種は新規で取得していない。新規REA VERIFIED **0**、TODO/VERIFY/BLOCKED正式書込差分 **0/0/0**。
- Ghidra/REA実行0、原作Golden PASS0、strict MATCH0、完全複製率未計測。PCのMASTER/QUEUE/PROGRESS/owner/lock/競合は未確認。正式同期禁止。

## 7. 接続・保存記録

- 接続障害ID: `REA-RC-20261023-1134-LOCAL-SSE429-01`
- 試行：Desktop Commander Local CompactでMASTER/プロトコル/REA資料/Ghidra検索資料を読み取る操作。応答429。
- 影響：PC正本最新状態、PC負荷、正式保存不可。安全拒否は発生していない。正規Libraryからオフラインパック・EXEを確認して独立静的解析を実施。
- コンテナに作成した本報告、独立JSON証拠、検証器はLibraryへ保存・読戻しを行い、成功可否を追加で記録する。PC正本の保存成功とは区別する。
