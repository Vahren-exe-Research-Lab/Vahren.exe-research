# 迫真戦記 ver0.67｜REA P0 DirectMusic CloseDown と所有権境界（2026-10-26 12時台）
研究ID: `REA-LOCAL-20261026-12H-P0-DMUSIC-CLOSEDOWN-ARRAY-OWNERSHIP-STATIC-01`
状態: **PC-SAVED / STATIC / VERIFY / NOT READY**。Goldenは未実測。
研究対象PE SHA256: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`
Ghidra search.sqlite SHA256: `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`

## 新旧成果境界
11時台の既報: 0x4BE480でPerformance8生成とInitAudio(+0xB0)、0x4BE6B0で+0x98→Release(+0x08)、管理表+0x70の解放先は未解決。
**今回新規**: +0x98のSDK vtable順序による**CloseDown**同定、呼出元0x555CD0→0x4BE6B0→0x4BE600→親オブジェクトfreeの実命令順、+0x70の配列領域がこの破棄経路で直接freeされないこと、AudioPath成功時の参照数VERIFYを分離。

## 対象アドレスと機械語
- 0x004BE4E0: `CALL 0x005B5C0B` 管理配列確保、0x004BE4EB: `MOV [ESI+0x70],EAX`。
- 0x004BE7C0: 管理配列読み取り、0x004BE7D0: `MOV EDX,[ECX+0x98]`、0x004BE7D7: `CALL EDX`（thisは直前PUSH EAX）。
- 0x004BE7E1: `MOV EDX,[ECX+8]`、0x004BE7E5: `CALL EDX`（IUnknown::Release）、0x004BE7EA: 管理配列の当該スロットをNULL化。
- 0x00555E60: `CALL 0x004BE6B0`（COM/音声shutdown）。
- 0x00555E71: `CALL 0x004BE600`（親オブジェクトの他所有フィールド破棄）。
- 0x00555E77: `CALL 0x005B6BBB`（親オブジェクト本体free）。
- 0x004BE600: 0x4BE651/667/686のfreeは+0x80配下、+0x44、+0x28系であり、+0x70を直接解放する命令なし。
- 0x004BE6B0: 0x4BE7B3以後の管理配列走査・NULL化〜ret経路に配列領域そのものをfreeするCALLなし。

## COM API同定の根拠
- Wineの公開 `dmusici.h` ではIDirectMusicPerformance8のメソッド番号38（0始まり）が`CloseDown`、x86スロット`38*4=0x98`。原作の引数はthisのみで一致する。
- `CloseDown`を`Release`前に実行することはMicrosoft DirectMusic SDKの契約にも一致する。
- GUID `IID_IDirectMusicPerformance8`とPerformance8生成元の同定自体は11時台既報。実行時vptr採取はないため、API名称は静的同定。
- 参照: https://sources.debian.org/src/wine/10.0~repack-6/include/dmusici.h
- 参照: https://learn.microsoft.com/ja-jp/previous-versions/ms809533(v=msdn.10)
## 新規VERIFY：所有権を区別する
**V1 / 管理配列+0x70:** shutdownの各Performance8要素はCloseDown→Release→NULL化されるが、配列本体の動的確保に対応するfreeは確認した破棄経路（0x4BE6B0、0x4BE600、0x555CD0の該当直列部分）にはない。OSによるプロセス終了時回収を考慮するとゲーム中の増加リークとは未判定。別所の解放・初期化回数をさらに検査する。
**V2 / AudioPath参照:** 0x004BF685でGetDefaultAudioPathと整合するCALL後、0x004BF697でSetVolumeを実行して0x004BF69Bでreturn。返されたローカルAudioPathのReleaseは同一関数中にない。Wineの実装ではGetDefaultAudioPathの成功返却時にAddRefするため、互換実装で同じ契約なら音量更新ごとに参照が残る懸念がある。Windowsの実COM実装でのAddRefや回数は未確認、確定バグ・量的リーク値とはしない。
**V3 / InitAudio異常:** 11時台のHRESULT未検査とGetDefaultAudioPathのHRESULT未検査を接続して、初期化に失敗したPerformanceが音量APIまで進む場合の異常経路をGolden候補にする。実機到達性不明。
- 参照: https://fossies.org/dox/wine-11.17/performance_8c_source.html （GetDefaultAudioPath実装のAddRef）
- 注意: 元EXEの実クラッシュ/リークを検証したものではなく、静的・別実装情報を区別して保存。

## 検査と正式REAの境界
- `REA_20261026_12H_P0_DMUSIC_CLOSE_ARRAY_AUDIT.py`: 機械語・関数境界・直接CALL・間接CALL・検索DB quick_check・ソース/DB SHAの計42条件を独立検査し **42/42 PASS**。
- 機械語はPE32の研究用コピーをCapstoneで独立逆アセンブル。関連Ghidra `function/callees/related`、SQLite read-onlyと対照。既存疑似Cの機械出力を正式VERIFIEDに自動昇格しない。
- 5方法: info=INDEX_ONLY、pseudo=INDEX_ONLY、assembly=TARGETED_NATIVE、callers=INDEX_ONLY、callees=INDEX_ONLY。今回正式VERIFIED追加0、正式TODO/VERIFY/BLOCKED書込差分0/0/0。
- 旧Wave1–5=64/64は`logs/progress_sync_20261011T153958076Z.json`の**過去**同期記録（新規計上なし）。古いQUEUE/PROGRESSはEPERM-staleで編集しない。
- 原作実機Golden PASS=0、strict MATCH未測定、完全複製率未測定。
## 再現性・安全と次の調査
- 12:36 JSTのPC SAITO online、active.lockなし、DBとPEハッシュ一致、空きRAM約13.44GiB。CPU単発値約9.7%。監査単体初回約0.356秒、保存時約0.379秒、全体所要時間不明。
- 新REA/Ghidra/原作ゲーム実行0、Work未使用。拒否済VA 0x5710C0..0x571500、Wave6、FLS再実行/REAエクスポートは行わない。
- 13時台・14時台のOFFLINE-UNSYNCEDは未同期。原本、MASTER、QUEUE/PROGRESS、既存RUN/証拠、他レーン、Git、公開先、スケジュールには触れない。
- P0次候補: `0x004BD2A0`と`0x00555CD0`の全owner lifecycleを追い、+0x70配列が別関数でfreeされる可能性/初期化が複数回走る可能性を限定xrefsで検査。
- 次点: `0x004BF630`AudioPathポインタの寿命とDirectMusicGetDefaultAudioPathの参照契約を実機トレース設計へ。GetDefaultAudioPath/SetVolume失敗時も別のゴールデン条件に分離。
- 重要: 静的監査のPASS件数は関数VERIFIED数ではない。保存後の独立読み戻しは別資料に記録する。
