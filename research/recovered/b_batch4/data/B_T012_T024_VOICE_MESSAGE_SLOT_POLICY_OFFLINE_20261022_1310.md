# 迫真戦記 ver0.67｜新B T012/T024：voice表示候補から24枠の表示・ヒットテスト管理へ

- 研究ID: `B-OFFLINE-20261022-1310-T012-T024-MESSAGE-SLOT-01`
- 接続復旧ID: `B-RC-20261022-1310-LOCAL-SESSION-TERMINATED-01`
- 日時: 2026-10-22 13時台 JST / owner: B (T012, T024)。旧T028/T011/T013の成果を再計上しない。
- 状態: `OFFLINE-UNSYNCED / STATIC / INFERRED / VERIFY / NOT READY`。原作Gameplay Golden PASS=0、strict MATCH=0、B READY=0、MASTER統合=0、Task DONE=0。
- 最初に Desktop Commander Local Compact で PC の `MASTER_LEDGER.md` を読取試行したが `INVALID_ARGUMENT: Error code: INVALID_ARGUMENT; Error: McpServerError: Session terminated`。これは接続障害であり安全拒否ではない。今回PC正本への書込・同期は0。
- 先行 `B-OFFLINE-20261022-1010-T024-TIMER-ACTION-01` / `B-OFFLINE-20261022-1112-T024-T012-ACTION-TIMER-01` / `B-OFFLINE-20261022-1210-T012-T024-VOICE-EXPIRY-01` の研究本文を再確認。既存のUnitタイマーの発見や `voice` スクリプト参照は再計上しない。
- ZIP: ChatGPT Library `/HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip` のオフライン写し SHA256 `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`、34 entries / CRC PASS。`search.sqlite` SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`、SQLite `PRAGMA quick_check=ok`。旧基盤で現行V3の直接E8照合は未実施。
- 原作ver0.67 EXE SHA256は収録Manifest記録 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。原本EXEはZIP非収録、今回直接計算なし。

## 新規静的証拠A：voiceを表示用オブジェクトへ配送する枠管理

- Ghidra擬似C: `0x0057B380` には `0x0057B4CE → 0x0049EB50` と `0x0057B6FC → 0x0049EB50` の2直接CALL登録がある。前者は `Unit+0x1E524 == 0`、後者は同値非0で候補・状態比較等を満たす枝。どちらも `0x00469A20` の `voice` 候補探索の後の処理である。以前の「voiceだから音声再生」は未証明のため維持しない。
- `0x0049EB50` は owner/画面側候補 `param_1` の `+0x1ED1CC` を起点に、stride `0xB4`、最大 `0x18=24` 件の **固定枠** を扱う。`0x0049EC05 → 0x00403290` が直接CALL登録。
- `0x00403290` のGhidra擬似Cは `SetDCBrushColor`・`FillRect`・`SelectObject`・矩形座標更新などのGDI描画を含む。したがって `0x49EB50` は音声専用キューの証拠ではなく、少なくとも **画面上の文字列・表示枠を配置する処理** へつながる。実可視表示と音声再生の有無はVERIFY。
- `0x00578110` の `retreat` 表示分岐から `0x00578281 → 0x0049EB50`、`0x0057BE30` の `skill` 分岐から `0x0057C0FC → 0x0049EB50` もある。voice専用24枠ではなく、retreat/skill/voiceの複数イベントが同じ表示枠管理へ到達する静的根拠。

## 新規静的証拠B：`0x49EB50` の24枠選択・置換優先順位

旧Ghidra擬似Cに基づく局所分岐。`slot_i = pool + 0x1ED1CC + i*0xB4`、i=0..23。

1. 最初の走査で `slot_i+0x78 == param_2` かつ `byte(slot_i+0x80)==0` なら、その枠を再使用する。複数一致時は先頭を採用。
2. 見つからなければ次の走査で `dword(slot_i+0x78)==0` となる最初の未使用枠を選択する。
3. 24枠全部が埋まっていれば、各枠の間接CALL `(**(code **)(*slot + 0x38))()` による評価値が **現在の最小値より小さい** かつ `byte(slot_i+0x80)==0` の枠を候補更新する。等値は先着を保持。呼出しは旧索引で `0x0049EBB7` と `0x0049EBCF` の computed CALL（後者は候補更新時の再評価）。戻り値の意味/副作用は未確定。
4. 全枠が埋まり候補にできる `byte+0x80==0` 枠がない場合、擬似C上は初期index0を維持する。これは境界ケースの候補であり、実機でslot0を置換すると断定しない。
5. 選択後 `0x0049EC05 → 0x00403290` に配送し、返却値は更新された `slot+0x78` の非ゼロ判定に依存してslotポインタ/0を返す。`param_4/param_5` のUI意味はVERIFY。

**注意**: ABI復元未完であるため `param_1/param_2` のゲーム内正式型名やvirtual slot+0x38の意味を `時間値` と命名しない。直接CALLも現行V3/原作ASMの独立E8確認前はGhidra STATIC。

## 新規静的証拠C：24枠は画面ヒットテストでも参照される

- `0x005263E0` のGhidra擬似Cは `in_EAX+0x194` が指す対象の `+0x1ED1CC`、stride `0xB4`、24件（offset loop `<0x10E0`）を参照する。
- 各枠の `slot+0x78` が非0の場合、カーソル相当の `in_EAX+0x32C/+0x330` から、枠の `slot+0x40/+0x44` を引いて `POINT` を作り、`PtInRect((RECT *)(slot+0x94), pt)` を実行する。TRUEなら `0x005264BE → 0x00403D70` がCALL登録。
- `PtInRect` であることは画面矩形との衝突判定の強い証拠。ただし実マウス操作で何が起きるか、`0x00403D70` の副作用はVERIFY。
- `0x00521CDF → 0x005263E0` の旧CALL登録は存在するが、`0x57B380` の `Unit+0x1E0` と `0x5263E0` の `in_EAX+0x194` が実行時に同一表示管理オブジェクトを指すことは **未証明**。共有オフセット・strideであることはSTATIC、同一インスタンス同定はVERIFY。

## 新規静的証拠D：管理レコード寿命の10000境界と設定値供給元

- 前回は `0x57B380` の `Unit+0x1E520` の木ノード `node+0x28` を毎回1減算し、`<1` なら `0x0057B800 → 0x00510030`（erase）と報告済み。
- 今回、同関数の **候補選択成功を伴う非0 `+0x1E524` 分岐内** に `node+0x28 > 9999` なら `DAT_0065BDA8` を代入するループがあり、その後の通常TTL減算へ進むことを別途追跡。大きい値は常に1減るだけではなく、特定条件下で設定値へ戻される。候補なし・非選択枝では同代入が無いので、毎tick必ず初期化とは言えない。
- SQLite data_refs: global `0x0065BDA8` は `0x00459610` の `0x0045B107` でWRITE、`0x0057B380` の `0x0057B711` でREAD（旧索引内2件）。`0x00459610` 擬似Cは `DAT_0065BDA8 = FUN_0046F4C0(unaff_EBX,0x14)`、これを呼ぶ先は `0x00555B70 → 0x00459610`。`0x14 = 20` は **デフォルト値として渡す候補** であり、実ランタイム値が常に20という証明ではない。
- `FUN_0046F4C0` のGhidra宣言は`void`で、呼び元は戻り値を使っておりABI不整合がある。`context`構造から設定値を取る可能性は高いが、原作ASM・DAT設定キー・実際の格納値はVERIFY。
- 新しい話題は上記「特定分岐でのTTL再正規化」と「設定値producer→consumer」の連結であり、前回の単純TTL--／map eraseは再計上しない。

## 合成検証（原作実行ではない）

PythonでGhidra分岐を再表現した24slotモデルを4例実行し、4/4一致：同owner優先index6、同owner枠flag1＋空枠index9なら空枠、満杯・最小評価値が同点なら先のindex5、満杯・全flag1なら暫定index0。これは **MODEL_ONLY / NOT DYNAMIC / NOT GOLDEN**。virtual callの副作用や実引数・ABIを検証するものではない。

## 重複・安全・保存境界

- 10/21収録のMASTER snapshotにはA担当 `A-20261011-0156-01` としてpool+`0x1ED1CC` / 24件/stride`0xB4` の初期化が既存成果にある。**24件・stride自体は新発見として二重計上しない**。今回のB増分は「表示候補の選択・置換ポリシー」「GDI描画と矩形ヒットテスト」「TTL>9999分岐の設定値producer」の3点。
- 前回Bのvoice ScriptBlock/文字列/Unitカウントダウンは既存引用。最新PC MASTERが確認できないので、他レーンとの最終的な非重複性は仮判定。
- 旧安全拒否で指定された範囲 `0x5710C0..0x571500`、既拒否された本文/コマンド/証拠へのアクセス・迂回・再試行なし。今回の関数群はその禁止範囲と無関係。原本ZIP/EXE/DAT/SAVE、他lane/REA/dev_lab/Git/Work/設定/スケジュールの変更0。
- LibraryのB所有 `data` 内の**独立オフライン成果のみ**で保全する。PCのB HANDOFF/MASTERは今回書込・同期不可。接続復帰後に同一ID/owner/READY/競合を照合し、必要な差分だけ一度同期する。EのみMASTER統合。

## P0/Goldenの次の絞り込み

- `0x00403290` の `slot+0x78/+0x80` writer、表示終了時のslot解放関数、`0x00403D70` の実際のクリック反応を調べ、Ghidraのreturn/abi誤認と直接CALLのE8を現行V3で検証する。
- `0x0049EBB7/0x0049EBCF` 間接CALL slot+0x38 の具体targetをvtable/RTTI・原作ASMで特定（推測埋め禁止）。枠が24件満杯のとき本当にindex0へ進むか、再評価CALL副作用やRNG消費有無を確認する。
- `0x0046F4C0` / `0x0045B107` で `DAT_0065BDA8` に設定される実値、`node+0x28` の初期値/20000 sentinel/更新周期を確認する。`+0x1E524` は `0x56F880` に0初期化あり、非0 writerの完全特定は未解明（文字列一致検索は完全なwriter網羅証明ではない）。
- 原作Golden（DESIGNED_NOT_RUN）は無改変EXE/DAT/SAVE/MAP・同一RNGで、Unit voice/skill/retreat、同owner/空き/満枠/flag1、TTL9999/10000/20000、表示文字列/矩形/カーソル応答・sound有無・フレーム寿命を計測。原作実測がないためGameplay PASS0、strict MATCH0。

## 低負荷の再開検索

```text
python search.py function 0x49EB50 --max-chars 12000 --limit 12
python search.py callers 0x49EB50 --limit 20
python search.py function 0x5263E0 --max-chars 12000 --limit 12
python search.py function 0x403290 --max-chars 12000 --limit 12
python search.py function 0x57B380 --max-chars 12000 --limit 12
python search.py function 0x459610 --max-chars 12000 --limit 12
python search.py function 0x46F4C0 --max-chars 12000 --limit 12
```
