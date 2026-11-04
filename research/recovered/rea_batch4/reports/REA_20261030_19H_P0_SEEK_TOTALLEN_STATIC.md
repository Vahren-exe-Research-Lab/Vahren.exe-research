# 迫真戦記 REA｜2026-10-30 19H｜Oggシークの総長getter(-1)と先行guard
研究ID：`REA-LOCAL-20261030-19H-P0-OGG-AGGREGATE-STATE-GATE-STATIC-01`
判定：**STATIC / VERIFY / NOT READY**。18H、14Hの成果と非重複（既存の負値代入発見を再計上しない）。
原作EXE SHA256：`E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
統合V9 DB SHA256：`2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`。SQLite quick_check=ok。

## 新規P0結論：エラーsentinel到達条件を狭める
- `0x005CFF10`（133 bytes）の `(this,index=-1)` は **通常の「総バイト長」getter**。state `[this+0x58]>=2`、リンクモード `[this+4]!=0`、リンク件数 `[this+0x34]>=0` が安定していれば、リンク `[this+0x44]` の各エントリ `+8/+0xC` から64bit値を取得して合計（0件では0）。負数-131は正常な合計処理の出口ではない。
- Native根拠：`0x005CFF1A/1E` state guard、`0x005CFF30/33` リンクguard、`0x005CFF35/3B/3D` index<件数、`0x005CFF3F/41` index<0分岐、`0x005CFF52` 自己再帰呼出、`0x005CFF5A/5C` ADD/ADC合算、`0x005CFF79/7D` EAX:EDXの64bit長読み取り、`0x005CFF20` / `0x005CFF88` の-131返却。範囲外または無効状態で-131。
- `0x005D04E0` は `0x005D04ED` の-1引数で総長取得を先行実行し、その後 `0x005D04F8` stateと `0x005D050E` リンク有無を再確認。失敗は-131または-138で処理終了。従って正常安定状態でシーク本体まで進む場合、上記sentinelの原因となる2条件は予防される。
- 上位入口 `0x005D0E90` にも `0x005D0EA4/AE` のstate、`0x005D0EBF/C2` のリンクguardが存在。V9で `0x00501FB7` / `0x00502015` → `0x005D0E90` → `0x005D0F5F` → `0x005D0B60` を確認。
- 失敗後処理は従来どおり `0x005D0E43` ページ更新が0以下→`0x005D0E52` で `0x005CFF10(this,-1)` 再呼出→`0x005D0E5A/5D` が戻りのEAX/EDXを直接格納。この**値未検査の構造は存在する**が、14Hの「-131代入」シナリオは、正常安定なリンク状態では現状の根拠からは成立せず、途中のstate/link/count変化や破損などの**追加条件を必要とするVERIFY仮説**に修正。
- 例外的に、リンク総長の64bit算術オーバーフロー、異常な件数、再入・並行状態変更、ポインター無効などは未検証。仮に-131相当の値が整数和として生じても、それは直接sentinelを返した証明にはならない。
- `0x005CFA10` の間接作用・呼出先の所有権/再入、他スレッド変更は追跡未完了。通常のEOF/復帰/無限ループ/音声障害を実機で断定しない。

## 根拠・検証
- V9 `function`（VA `0x005CFF10`, `0x005D04E0`, `0x005D0B60`, `0x005D0E90`, `0x005CFA10`）と `callers`、PE独立局所assembly。CALL sites `0x005CFF52`（再帰）、`0x005D04F0`（前処理）、`0x005D0E43`（page）、`0x005D0E52`（総長）。4個の直接CALLはV9参照と原本同SHAのnative E8を照合。
- `REA_20261030_19H_P0_SEEK_TOTALLEN_PROBE.py` と `..._AUDIT.py` を新規作成。独立静的監査 **87/87 PASS（0.8760秒）**、安定した合成状態 `state=0..4` ×リンク有無×リンク数0..3の40組を監査。これは合成算術でありゲーム実測ではない。
- 旧進捗：最新保存済み `logs/progress_sync_20261011T153958076Z.json` が **64/64 VERIFIED** と報告（Wave1〜5）、ただし既存 `QUEUE.json` はWindows rename EPERMにより **VERIFIED16/TODO48** の古い表示。旧run/ログを根拠に64/64を維持し、新規昇格0。
- このrunの正式REA個別5種（info/pseudo/assembly/callers/callees）新規取得は **0件**。V9 info/pseudo/callers/callees＋局所PE ASMは独立静的証拠だが正式REA5種evidence IDではない。新規正式VERIFIED **0**、正式TODO/VERIFY/BLOCKED差分 **0/0/0**、原作Golden実測PASS **0**、完全複製率未測定。
- 開始前後 `active.lock` 不在。PC接続成功。開始時Java/Ghidra競合プロセスは表示されず。OS空き物理メモリ取得値15,917,176KiB。CPU負荷と総所要時間は不明。新規REA/Ghidra/ゲーム実行なし。
- 旧18H読み戻し24/24、今回のsource/DB SHA一致とV9 quick_checkを確認。安全拒否の迂回、既存ファイルの上書き、MASTER/QUEUE/PROGRESS/RUN/原本/他レーン/Git/公開先/スケジュール変更なし。

## 再開位置・Golden設計
次回は `0x005CFA10` とそこで呼ぶ `0x005CF010` / `0x005CEB90` の状態書込と、`0x005CFF10` 再入直前に `[this+0x58]` / `[this+4]` / `[this+0x34]` が変化し得るかをcaller/callee xrefsで確認。ガード成立からgetter再呼出までの不変条件を検証する。
実機Golden候補：リンク正常・リンク0件・I/O hard-error(-128)・EOF(-2)・シーク不可(-138)・状態無効(-131)を別条件にし、復帰値・64bit再生位置・停止性を比較。**未実測0件**。
保存：19H固有のPROBE/AUDIT/EVIDENCE/STATICのみ。保存後の別プロセス読み戻し結果は `REA_20261030_19H_P0_SEEK_TOTALLEN_READBACK.json` を参照。
