# REA-T015-OGG-REUSE-20261105 — playback v4 / DirectSound音量分離の実機追補

- 区分: owner intake、統合担当による正式採録待ち。2026-11-05 JST。
- 親研究: [初回経路・ABI設計](../REPORT.md)、[bounded decode](../probe_v2/REPORT.md)、[v3可聴出力と共有音量問題](../playback_v3/REPORT.md)。
- 親commit: 6337820cd5dda49fdec79e650d1c3913114c0238。
- 本追補は過去の「v4ゲーム内未検証」を限定更新する。製品完成、DAT統合完了、全入力への安全性認定ではない。

## 結論

既存host open/info/read/clearを用いた全PCMデコードと、DLL所有DirectSound secondary bufferによる2音再生・個別音量・順次停止を、指定SHAの隔離ゲームコピーで観測した。最初のvoiceの音量を変更しても、2番目のbufferの音量は変わらず、ゲームの同一音声sessionの前後値も一致した。ユーザーもv4試験中にBGM音量が変わらなかったと報告した。

ただしゲームは起動時から小さいとの報告がある。v4開始前のmaster値は既に0.0499885567で、終了後も同じ。これはv3の最終指定3276/65535と一致し、Windowsに保存されたsession音量が次の起動へ残ることと整合する。v3以前のbaselineは未取得であり、元の正確な値は復元できない。ユーザーへWindows音量ミキサーのゲーム項目だけを普段の音量へ戻すよう案内した。復元完了は未確認。自動的に100%へ変更していない。

Windowsのsession音量設定には永続性があり、次回の同種sessionへ引き継がれる場合がある。[Microsoft Audio Sessions](https://learn.microsoft.com/en-us/windows/win32/coreaudio/audio-sessions)

## 境界・設計変更

host ABIは既存証拠のまま:
- open VA 0x005D16C0 / RVA 0x001D16C0
- info VA 0x005D0F70 / RVA 0x001D0F70
- read VA 0x005D12E0 / RVA 0x001D12E0、signed16LE指定(0,2,1)
- clear VA 0x005CFE00 / RVA 0x001CFE00
- DLL側outerはalign16、0x2D0 bytes。2回のdecoder lifecycleは同じouterで逐次実行。DLL側decoderの並列実行を証明しない。

経路: dedicated worker → host open/info/read(EOF)/clear → DLL temporary PCM → DLL-owned DirectSound device → software secondary buffer Lock/copy/Unlock → SetVolume/Play → Stop/Release → device/window解放。

v3のwaveOutSetVolumeは使用しない。v4はDSSCL_NORMAL、DLL所有hidden window、CTRLVOLUME/GLOBALFOCUS/LOCSOFTWAREのsecondary buffersを使用。原作device・manager・primary bufferを借用・変更しない。PCMはUnlock後に作業heapを解放し、再生中のcopyはDirectSoundが所有する。所有worker以外からのcontrolを拒否する既存方針を継承。DLL自体はゲーム終了まで残す。

DirectSoundのSetVolume引数は100分の1dBの減衰値である。[Microsoft SetVolume](https://learn.microsoft.com/en-us/previous-versions/windows/desktop/ee418150(v=vs.85))

## 実機観測

[機械集計](RUNTIME_SUMMARY.json)、[再解析parser](analyze_playback_v4.py)。raw logはローカルのみ。
- EXE SHA256: e8dac301050c8e630d7e0ce93aeefd95e641207d9c0576017f62ba46a8767187
- DLL SHA256: 46316a6f0b645a7ff8bcefdcd9c1abc50b56c2c88faea48d1c93c6fa7fb83bad
- log SHA256: b9416567cf3700f8a2fe13959193a4a76fbafc313d815bd96cf93b4f8b27244c
- 56,926 bytes、1,043 events、1 control worker。launcher exit 0。
- 各cycle: 1,007,616 PCM bytes、251,904 stereo frames、44100 Hz、16bit、正read472回＋EOF0、clear0。
- DS device/coop/buffer/Lock/Unlock/Play/volume/Stopは記録範囲ですべて成功。
- live voice数 1→2→2→1。END=0。
- voice1 cursor bytes: 525672→94884→625848、volume: -1046→-1046→-2602。
- voice2 cursor bytes: 525672→49020→401820、volume: -1398で一定。
- statusは各観測5 (PLAYING|LOOPING)。cursor折返しとloop statusを観測したが、継ぎ目の音質を証明する録音はない。
- session before/after raw logのSHA256はいずれも899e7e29603f513473e79b3378284675c49e67c1030208baa9ab9fba620bb47a。
- session相関hash一致、master0.0499885567、mute0、左右channel各1、audit errors0、matching session1。
- session識別hashは相関用の非暗号学的hashであり、セキュリティ上の同一性証明ではない。

v4での追加音可聴性・操作正常を独立した新しい回答で再確認したとは扱わない。v3にはそれらの本人確認があるが、別runの証拠を混ぜない。

## 検証と残件

22個のsource hashと3実行binary hashをruntime receiptと照合。build時5 C suitesとaudit validation(正常＋8拒否)が成功した記録あり。[build receipt](BUILD_RECEIPT.json)のBUILT_NOT_RUN_IN_GAMEはbuild時の履歴を保存したもので、本追補の実機結果より前の状態。

read-only auditは列挙・必須getterの失敗、欠落項目、多session、異常値を失敗扱いにする。wrapperはsession相関とmaster/mute/channel値を前後比較する。前後snapshotは途中の一時的変化を除外しない。

方式Bは、同一SHA・通常OGG1件・短時間という範囲で具体的な実装成立の根拠を得た。v3のWinMM volume方式は採用しない。次の順序:
1. ユーザー側の通常音量を復元し、そのbaselineを記録する。診断の再実行は音量復元確認の代わりにしない。
2. 通常音量で可聴性・BGM/WAV共存を再確認。別OGG、反復、長時間、メモリ/handle収支、device lossを検証。
3. malformed/truncated/chained-format/failed-openとcodec共有状態のgateを継続。
4. 既存routine busの固定通知＋VM文字列snapshot/owned queue設計を実装・検証。任意pathを現在のroutine引数へ直接渡せるとはしない。
5. 製品統合と関数辞書正式採録は別工程。

原作EXE/DAT/音声、raw logs、PID/TID、session識別値、私用path、製品sourceは保存していない。develop・共有辞書は変更しない。
