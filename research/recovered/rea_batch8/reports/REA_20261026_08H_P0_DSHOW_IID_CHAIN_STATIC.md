# 迫真戦記 ver0.67｜REA P0 DirectShow IID・COM所有権の静的追跡（2026-10-26 08時台）
研究ID: REA-LOCAL-20261026-08H-P0-DSHOW-IID-CHAIN-STATIC-01
状態: PC-SAVED / STATIC / VERIFY / NOT READY。原作ゲームGolden PASS=0、新規正式REA VERIFIED=0。
Source EXE SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
Ghidra search.sqlite SHA256: 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF

## 今回の新規証拠：QueryInterface IIDを6 GUIDの原作実バイトから確定
- 0x004BE820 (2695 bytes) のMP3/DirectShow初期化枝。0x004BED21 = ole32.dll!CoCreateInstance（PE import 0x00609310で確認）。
- 0x0060CD6C = e436ebb3-524f-11ce-9f53-0020af0ba770 = CLSID_FilterGraph。
- 0x0060CDBC = 56a868a9-0ad4-11ce-b03a-0020af0ba770 = IID_IGraphBuilder。
- CoCreateInstanceの結果はstream+0x8Cに置かれる。次の4件のQueryInterfaceは同一IGraphBuilderのIUnknown vtable先頭スロット+0を使用。

| CALL site | IID位置 | 原作GUIDに対応する型 | 出力フィールド |
|---|---|---|---|
| 0x004BEDC6 | 0x0060CD7C | IMediaControl | stream+0x90 |
| 0x004BEE17 | 0x0060CD8C | IMediaEvent | stream+0x98 |
| 0x004BEE30 | 0x0060CDAC | IMediaSeeking | stream+0x94 |
| 0x004BEE49 | 0x0060CD9C | IBasicAudio | stream+0x9C |

- GUIDは原作PEバイトをlittle-endian UUIDとして直接読み出した。型名はWindows DirectShowの標準IIDと一致し、実機のvptrは未採取。
- 各QueryInterface直後でHRESULTの負値をチェックし、失敗時は共通cleanup側0x004BEDCCへ移る（初回はJNSで成功先0x004BEE04、他3件はJS/JLで失敗先）。
- 成功時は0x004BEE61のIGraphBuilder vtable+0x34（RenderFile相当）、続いて0x004BEE6BのIMediaControl vtable+0x1C（Run相当）へ進む。

## 新たなVERIFY：RenderFile失敗後もRunへ進む可能性
0x004BEE61 CALL EDX直後は0x004BEE63 MOV EAX,[EDI]で戻りHRESULTを上書きする。RenderFile失敗を調べる条件分岐はその間にないため、0x004BEE6BのRunが呼び出され得る。再生成功・失敗をどう上位へ伝えるかはVERIFY。実ゲーム不具合は未実測。
0x004BF2B0の既存Ghidra疑似Cには+0x9C、+0x94、+0x98、+0x90のRelease/NULLクリアと+0x90のStopがある。これは部分初期化失敗時のcleanupと整合するが、各分岐の全ASM・実機所有権確認は未完了。

## 既存検索DBの参照被覆と訂正
0x004BE820を原作PEからCapstoneで全2695バイト限定逆アセンブルし、実CALL命令88件とGhidra SQLiteの直接/間接CALL site和集合88件が集合として完全一致した。今回の4つのQueryInterfaceも索引収録済み。
search.py function --limit 2の表示に間接CALLが2件だけ現れ、当初欠落と誤推定したが、全SQLite行確認で誤認と判明。最初の不適切な監査期待値46/50はファイル保存前に修正し、正式な結果に加算しない。検索DBのCALL漏れは今回認められなかった。
初回修正後51/51 PASS、排他新規JSON保存時51/51 PASS。51は個別静的条件数であり51関数の逆コンパイル完了ではない。ソースSHA、DB SHA、PE ImageBase、GUID6種、厳密ASM31箇所、SQLite quick_check、関数サイズ、4 QI site、88 site完全一致を検査。証拠: REA_20261026_08H_P0_DSHOW_IID_AUDIT.py / REA_20261026_08H_P0_DSHOW_IID_EVIDENCE.json。

## 正式REA・Golden・次回
- 2026-10-11T15:39:58.076Z の logs/progress_sync_20261011T153958076Z.jsonはWave1-5=64/64、queueUpdate=STALE_RENAME_DENIED、humanReadableProgress=SKIPPED_QUEUE_STALE。過去64件は再計上しない。
- 0x004BE820正式5種: info=INDEX_ONLY、pseudo=INDEX_ONLY、assembly=TARGETED_SOURCE、callers=INDEX_ONLY、callees=INDEX_ONLY。5種完全充足新規0、正式VERIFIED差分0、TODO/VERIFY/BLOCKED書込差分0/0/0。新たな独立VERIFY候補はRenderFile HRESULT経路。
- Golden実測PASS=0、strict MATCH=未測定、完全複製率=未測定。次の候補VA 0x004BF410（音量/フェード状態更新）と0x004BF780（GetEvent失敗時の条件）。
- 追加Golden条件（NOT RUN）: MP3初期化の4 IID個別失敗、RenderFile失敗、Run失敗、正常停止後の部分COM参照解放、ループ中のGetEventタイムアウトを検査。
- 今回のread-only解析はLocal Compactで実施、active.lockなし、Ghidra/REA/ゲームの新規起動なし、Work使用なし。禁止FLS/Wave6/VA 0x5710C0..0x571500の拒否操作へ再試行なし。
- 原本・MASTER・QUEUE・PROGRESS・既存runs・他レーン・Git・スケジュールは無変更。13/14時台オフライン成果の正式同期は未実施。論理所有権はREA専用decomp_taskのみ。
- 参考 Microsoft公式: https://learn.microsoft.com/en-us/windows/win32/directshow/overview-of-graph-building ; https://learn.microsoft.com/en-us/windows/win32/directshow/filter-graph-manager
