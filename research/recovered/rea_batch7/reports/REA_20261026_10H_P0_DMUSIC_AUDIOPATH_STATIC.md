# 迫真戦記 ver0.67 — REA P0 DirectMusic AudioPath音量ルート（2026-10-26 10時台）
研究ID: REA-LOCAL-20261026-10H-P0-DMUSIC-PERFORMANCE-AUDIOPATH-ABI-STATIC-01
状態: PC-SAVED（監査JSON排他保存）/ STATIC / VERIFY / NOT READY。正式REA新規VERIFIED=0、原作Golden実測=0。
対象コピーSHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
既存検索DB SHA256: 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF

## 新旧の境界
- 09時台既報: 4BF630はMP3 +9C / OGG +A0 / DirectMusic +78の三分岐、先の2 backend音量スロット、およびfade定数0.2/±15。レーンD T015にも音声フェード/適用は既報。これらを新規として二重計上しない。
- 今回新規: +78の実producer（4BEF20/27/2F）、一段目・二段目の両間接CALLのABI、および先行09時台「3間接CALL」という過少計数の訂正。

## DirectMusicの二段階COM呼出し：原作機械語
- 4BEE82: LEA EBX,[EBP+78h]、4BEE85: MOV [EBX],0。4BEF20で管理テーブル+70を読取り、4BEF27で index*4 の実体を取得、4BEF2Fでstream+78に格納。4BEFC5は非NULL検査。ランダム化関係の周辺分岐は本回の断定対象外。
- 4BF630: EAX=stream、ECX=要求音量。PUSH ECX/PUSH ESI。4BF638がstream+0Cへ音量保存。stream+08=0かつ+09=0の分岐で、4BF670からstream+78のポインタを取得し非NULLを検査。
- 4BF679で LEA EDX,[ESP+4]。これはPROLOGUEの PUSH ECX で積んだローカルDWORDを出力領域として指す。4BF67D/7Eで outポインタ/performance-this を積み、4BF67Fで vtable+0xCC を取得、4BF685で間接CALL。
- vtable +0xCC(第51スロット) + 引数(out IDirectMusicAudioPath**)は DirectX SDK の IDirectMusicPerformance8::GetDefaultAudioPath に一致する（推定API同定。runtime vptr未採取）。
- 4BF687で EAX=[ESP+4] を読み、GetDefaultAudioPathのHRESULTを上書き。4BF68Bで volume=[stream+0C]、4BF68Eで EAX をthisとしてVTableを無条件逆参照。4BF690/692/693で duration=0, volume, path-this を積み、4BF694で vtable+0x14、4BF697で間接CALL。
- vtable +0x14(第5スロット)と2引数は IDirectMusicAudioPath8::SetVolume(LONG, DWORD) に一致。duration=0 msの即時適用を指定し、ユーザー側fadeは別途+0x20による逐次更新で制御する。
- SDKのSetVolumeに渡すLONGは-9600..0（1/100 dB）、duration=0はbackend自身に継続フェードを指示しない。
- 本回では原作PE・Capstoneおよび保存済みSQLiteの4BF630間接CALL索引が0x4BF64A/0x4BF66B/0x4BF685/0x4BF697の **4サイト** で一致。09時台の本文「3つ」は誤り、既存09時台ファイルは改変せず本記録で訂正。監査数値・過去成果は二重計上しない。

## 新しいP0 VERIFY / ABIと失敗経路
- 4BF673はperformance-thisを非NULL検査するが、4BF685後、HRESULT検査がない。4BF687がEAXを上書きし、4BF68Eは出力ポインタのNULL/有効性を検査しない。GetDefaultAudioPathが失敗し有効なinterfaceを返さない場合、不正ポインタを逆参照する可能性がある。
- とくにout DWORDは初期値NULLではなく呼出時ECXの音量値。失敗後にoutが未更新なら、音量整数をCOMオブジェクトと誤認して読もうとする経路が成立する。ただしCOM実装による失敗時出力初期化や到達条件は未実測。
- 4BF697後、本関数内に取得したAudioPathのRelease呼出しは見当たらない。GetDefaultAudioPathが参照を加算して返す場合のownership・繰返しvolume呼出しによる参照残存はVERIFY。ここでは確定リーク/クラッシュとは判定しない。
- 実行時Interface GUID/vptrとGetDefaultAudioPath成功/失敗実態、4BF697のHRESULTを上位が利用するか、他箇所でのAudioPathのrelease、音声0/極小音量フェードの再現性は未検証。

## ソース・限定検証・保存境界
- 原作複製PE read-only (研究ラボtargets)をCapstone PE32 x86解析、検索CLI function/callers/callees/related、検索DB read-only/quick_check/間接CALL siteを使用。API同定の外部裏付け: DirectX SDK GetDefaultAudioPath https://documentation.help/DirectMusic/idirectmusicperformance8getdefaultaudiopath.htm 、Microsoft Learn SetVolume https://learn.microsoft.com/en-us/previous-versions/ms808952(v=msdn.10) 、AudioPath実装のvtable例 https://doxygen.reactos.org/d3/d3f/audiopath_8c.html 。
- 10時台監査44/44 PASS。source/DB SHA、PE ImageBase、4BF630と4BE820の関数全命令長、対象x86 site、4 indirect索引、+78 writer provenance、既知caller接続を個別検査。数値は静的テスト条件数であり44関数取得の意味ではない。
- INFO=INDEX_ONLY / PSEUDO=INDEX_ONLY / ASSEMBLY=TARGETED_SOURCE / CALLERS=INDEX_ONLY / CALLEES=INDEX_ONLY。5種類のREA独立完備0、正式VERIFIED追加0。正式TODO/VERIFY/BLOCKEDファイル書込差分0/0/0。Golden旧実機PASS0、strict MATCH未測定、完全複製率未測定。
- 同期ログ20261011T153958076Z.jsonにあるWave1～5=64/64は旧実績。QUEUE/PROGRESS EPERM staleであり更新禁止。既存 runs/evidence・MASTER・他レーン所有ファイルにも非書込。
- PCオンライン10:38～10:50 JST、active.lockなし、空き物理RAM約17.83～17.87GiB、CPU単発観測5%（10:50）、Python既存プロセスあり、研究全体時間未測定。監査単体約0.351秒。新規REA/Ghidra/原作ゲーム実行0、Work使用0。
- 最初の一時stdin probeはPS→Python Unicode path文字化けでWinError123（元資料変更なし）。cwd相対pathへ直して成功。監査初回43/44はRET命令の表示末尾空白による期待文字列ミス、1行修正後44/44。いずれも安全拒否ではなく、隠さず記録。
- 13/14時台OFFLINE-UNSYNCEDは未同期。禁止済FLS/VA/Wave6・拒否エクスポートには非接触。原本ZIP/EXE/SAVE、MASTER/T018/dev_lab/A～E/Git/公開先/既存スケジュール非編集。
- 次P0: stream+0x70テーブル生成とDirectMusicPerformance8の実IID/実生成経路、GetDefaultAudioPathが返すAudioPathのRelease所有者、HRESULT失敗の伝搬。続いて極小volumeでのfade+0x20負値境界。新Ghidra全関数再解析は不要。
