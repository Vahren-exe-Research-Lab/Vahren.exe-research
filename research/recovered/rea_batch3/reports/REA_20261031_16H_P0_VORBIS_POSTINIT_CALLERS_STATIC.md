# REA｜2026-10-31 16H｜Vorbis post-init残り2呼出元と別初期化callocの条件付きNULL経路（P0）
研究ID：`REA-LOCAL-20261031-16H-P0-VORBIS-POSTINIT-OTHER-CALLERS-STATIC-01`。owner=REA、Task=T015、状態 **PC-SAVED / STATIC+INFERRED / VERIFY / NOT READY**。
15H `REA-LOCAL-20261031-15H-P0-VORBIS-POSTINIT-RETURN-LOSS-STATIC-01` の残余caller検証。14Hの二重cleanup、15Hのwrapper戻り値破棄、13Hの配列解放漏れを新規として二重計上しない。

## 読取り前提・非重複
- MASTER/レーン規約、REA README/QUEUE/PROGRESS、既存15H報告とevidence、knowledge README/SYNC_STATUS、private GitHub developのVorbis解説、V9研究入口を読取専用で照合。
- 旧index README/BUILD_MANIFESTは実在せず、既知の現行配置差異。承認済みV9別名CLI/SQLiteを使用。旧V3ポインタ・既拒否操作には触れない。
- 研究用PE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、V9 SQLite SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`、SQLite quick_check=ok。
- PC Local接続成功、`active.lock`なし、Java/Ghidra競合プロセス出力なし。確認時空き物理RAM約18.3GiB。CPU負荷・作業総時間は未計測。原作EXEのゲーム実行・新規Ghidra/REA実行なし。
- `knowledge/kb.py addr` は `0x5D0020/0x5D04E0/0x5D4900` を未命名・本文索引未言及と返す。共有辞書は変更しない。

## 新規STATIC：post-initの残り2直接CALL
- `0x005D0020`（関数body V9: 0x5D0020..0x5D04DD）は、状態 `outer+0x58>=2` と `outer+4!=NULL`、目標位置などの前提検査後、`0x5D00E3 -> 0x5D4D20` を実行する。続く `0x5D00E8` ではpost-init返値EAXを判定せず、`0x5D00EC -> 0x5CEB30` の返値を `0x5D00F4 test eax,eax` で検査。**そのテストはpost-initではなく後続関数の戻り値**。
- `0x005D04E0`（body V9: 0x5D04E0..0x5D0B57）は `0x5D092C cmp edi,[esi+0x60]`／`0x5D092F je 0x5D094B` で選択streamの一致を検査。一致時だけ `0x5D0952 -> 0x5D4D20` を実行し、直後 `add esp,4` の後の `0x5D095A` はstream fieldを読取る（post-initのEAXは未判定）。不一致側は `0x5D0931 -> 0x5CF9E0`、`outer+0x58=3` の更新後、`0x5D0949 jmp 0x5D095A` でpost-initを省略する。
- V9直接CALL関係は `0x5D0A85 -> 0x5D0020`（`0x5D04E0`内部）を含み、上位から同じ後続処理へ入る別経路がある。転送後の全条件/エラー伝播は未検証。上記の2サイトは15Hの `0x5D5BFB` と別の直接CALLであり、既存問題の3重カウントはしない。

## 新規STATIC：状態4側の別初期化関数0x5D4900
- V9は `0x5CF9BC`／`0x5CFA5D` から `0x5D4900` への直接CALLを2件保存。関数入口は別の0x70バイト構造体をゼロ初期化する。`0x5D4922 cmp [eax],esi`／`0x5D4924 je` の空入力側は大きな確保を行わず戻る。
- 非NULL入力側は `0x5D492B -> 0x5D1C71 calloc(1,0x48)`、`0x5D4938`で戻り値を `inner+0x68` に格納し、`0x5D493B fstp [edi+4]` で書込。**この局所区間に確保結果のNULL検査は確認できない**。後続 `0x5D4952 calloc(1,0x14)` は反復領域へ格納され `0x5D4963 -> 0x5E6C70` に渡されるが、下位関数のNULL許容は未確認。
- `0x5D4900` の確保と13Hの `0x5D59BA/0x5D59CD`、12Hの `0x5D57F8`、11Hのlook内部確保は別経路。実際のOOM、破損、発生確率、クラッシュは DYNAMIC 未測定・VERIFY。安全性や脆弱性の断定をしない。

## 証拠・復旧・KB_CANDIDATE
- 16Hの最初のprobeは `0x5D00CA`／`0x5D093E` を命令途中から復号した。**RECOVERY-ID `REA-RECOVERY-20261031-16H-NATIVE-PROBE-ALIGN-01`**。その出力は認定に使わず、関数入口 `0x5D0020`／`0x5D04E0`から復号するV2で命令境界を確認した。V1スクリプトは削除・改変せず保存。
- 正本PE/V9・26個の指定命令bytesとCapstone decode・9件のdirect E8・3関数のV9 owner・3 caller set・前回15H IDを独立照合。静的監査 **82/82 PASS（1.8993秒）**。
- 保存済み証拠：`REA_20261031_16H_P0_POSTINIT_CALLER_EVIDENCE.json` SHA256 `99EE83CE9F41F0757EEA33B90BB792604843815A18EC874F219E61D92E388780`。機械語3rangeのSHA・全site・修正履歴を保持。
- **KB_CANDIDATE**：`0x5D0020`でpostinit EAX破棄／後続戻り値を検査、`0x5D04E0`でstream index分岐によりpostinit実行・省略、`0x5D4900`の条件付きcalloc NULL未検査。source相対path、PE/V9 SHA、callsite、STATIC/INFERRED/VERIFYを統合専任へ渡す。共有knowledgeには未反映・未確定。
- 新規REA正式5種証拠完備 **0**、新規正式VERIFIED **0**、既存正式STATIC VERIFIED **64/64維持**、TODO/VERIFY/BLOCKEDの正式差分 **0/0/0**。原作Golden実測PASS **0**、strict MATCH **0**、完全複製率未測定、READY=NO。
- 再開位置：`0x5D0A85`（`0x5D04E0`から `0x5D0020` への推移）、`0x5D0B60` 上位caller、`0x5E6C70` のNULL入力契約を出典付きで検証。所有者/重複/実行環境を次回再確認する。
- 書込みはREA所有の新規16Hスクリプト・証拠・報告のみ。原本ZIP/EXE/SAVE、MASTER、QUEUE/PROGRESS、他owner、Git、共有KB、DB、既存スケジュールは無変更。

