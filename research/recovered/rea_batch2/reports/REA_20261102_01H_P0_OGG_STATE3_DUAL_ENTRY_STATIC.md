# REA 2026-11-02 01H P0 | Ogg state3初期化の二つの入口とESI ABI
**研究ID:** `REA-LOCAL-20261102-01H-P0-OGG-STATE3-DUAL-ENTRY-ESI-ABI-STATIC-01` / **owner:** REA/T015 / **状態:** PC-SAVED / NATIVE-STATIC / VERIFY / NOT READY。以前の08H成果の再計上ではなく、同一calleeへの未記載の**早期CALL**とregister-context契約を追加監査する。
**原本と検索DB:** 読取専用 `rea_lab/targets/hakushin067_Vahren.exe` SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、`rea_lab/headless_analysis/search_index/HAKUSHIN067_UNIFIED_V9_20261023.sqlite` SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`。両ファイル2026-11-02 01HにPC現物で再計算一致。V9専用read-only CLIを使用。標準旧V3ポインタは変更せず。
## 独立元ASM監査
1. `0x005D0B60`の入口`0x005D0B6D MOV ESI,[EBP+8]`でdecoder/outerポインタをESIに保持。最初の`0x005D0B7A CALL 0x005D04E0`は3引数、`0x005D0B84 JS 0x005D0E7E`で負の返値を除外後、**`0x005D0B8A E8E1EDFFFF CALL 0x005CF970`**へ進む。 `0x005D0B91 JNE 0x005D0E7E`は初期化失敗の戻り経路。
2. V9と一致する同じcalleeへの後段 `0x005D0D67 E804ECFFFF CALL 0x005CF970` は既存08H調査済み。前段で`0x005D0D48`に既知serial indexを`outer+0x60`へ、`0x005D0D4B`にstate=3を`outer+0x58`へ格納後に呼ぶ経路。**新しい関数ではない**が、二つの別時点に入口が存在する。
3. 原本`0x005CF970..0x005CF9D7`の入口は `MOV EAX,[ESI+0x58]`。state>3なら0を直接return、state<3なら`0xFFFFFF7F` return。**state=3だけ**`0x005CF9A1 -> 0x005D5BD0`で選択した既存ヘッダレコードを初期化し、成功時`0x005CF9CC MOV [ESI+0x58],4`、0 return。失敗時は`0xFFFFFF77`。V9 pseudoの`FUN_005cf970(void)`は**暗黙ESI入力を省略**するため、独立DLL呼出ABIや無引数関数として扱わない。
4. `0x005CF970`へのcallersはV9で**2件**(`0x005D0B8A`,`0x005D0D67`)、callee`0x005D5BD0`へのcallersは`0x005CF9A1`と`0x005CFA45`。既知08Hで調べた`0x005D0D67`や`0x005CF9A1`を新規E8として二重計上しない。
5. 元PE窓SHA256: `0x005D0B60..0x005D0B98`(exclusive) `44FE4A5DAFBF23EB3B79E2B19B2634FB45B4ABFDA410FD1FDBA644746B9DF5AF`、`0x005CF970..0x005CF9D7` `E9F9D9A7B9007542C5C127B9A50CDC2CF176034912B5D2F67AABFBC058C200F3`。capstone5.0.7で現物原本をread-onlyデコード、V9のE8 2件・callee照合。静的証拠 `REA_20261102_01H_P0_OGG_STATE3_DUAL_ENTRY_EVIDENCE.json`。
## 正確性・未解明・次カーソル
**意味:** 最初の呼出は上流seek/position処理 `0x005D04E0` の非負結果のあとにstate3初期化を試行し、後段は既知serial一致後のstate3復帰時に同calleeを呼ぶ。前段の実状態値と全到達可能性・呼出時ESI保存、例外・live seek、エラー伝播の動的挙動、キャッシュレコード有効性はVERIFY。静的分岐だけで「常時必ず成功」や「脆弱性」を証明しない。
**重複/訂正:** 既存 `REA-OFFLINE-20261101-08H-P0-VORBIS-CACHED-STREAM-STATE3-REENTRY-STATIC-01` の「状態3復帰入口」へ補足。06H/07H mode callocとsetup cleanupは別研究。11H/12H Library報告に当該`0x005D0B8A`記載なし、現行developのREF_AUDIO_VORBIS/symbolsと最新owner intake INDEXにも記載なし（現行PC全報告の網羅的重複除外は未保証）。
**正式:** info/pseudo/assembly/callers/calleesの本件完全セットなし、公式新規VERIFIED0、TODO/VERIFY/BLOCKED正本差分0/0/0。原作Golden0、strict MATCH0、READY0、完全複製率未測定。監査用新規REAL gameplayは無し。CPU負荷・全工程時間は不明。
**KB_CANDIDATE:** REA/T015; semantic key `0x005D0B8A -> 0x005CF970` and `0x005D0D67 -> 0x005CF970`; offset `outer+0x58/+0x60/+0x48`; source SHA/windows SHAは上記。候補統合先`REF_AUDIO_VORBIS.md`/symbols/research/rea。未確定STATIC。実証保存はPC所有資料に限定し、私有GitHub intakeは正式CURATEDではない。
**次:** 08Hに続く09H producer `0x005D1490` と索引・研究IDの既存参照を確認し、index/countとcached record対応を調査。既拒否18H証拠・保護VA/旧Waveには触れない。原本・他owner・MASTER・QUEUE・PROGRESS・共有knowledge・develop・元ユーザーworktree・既存スケジュール不変更。
