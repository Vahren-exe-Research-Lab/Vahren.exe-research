# 迫真戦記 ver0.67 REA｜DirectMusic COM生成・所有者テーブル 静的監査（2026-10-26 11時台）
研究ID: `REA-LOCAL-20261026-11H-P0-DMUSIC-COM-CONSTRUCTOR-INIT-GUID-STATIC-01`
状態: **PC-SAVED / STATIC / VERIFY / NOT READY**。本記録は正式REAの新規VERIFIEDではない。
対象研究用PE SHA256: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`
既存Ghidra DB SHA256: `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`

## 差分（既存10時台の重複計上を避ける）
- 10時台既報: `0x004BF685`=Performance8 vtable`+0xCC`→AudioPath取得、`0x004BF697`=AudioPath vtable`+0x14`→SetVolume、HRESULT未検査、音量用スタックスロットを出力領域として流用。
- 今回新規: そのPerformance8ポインタの**元のCoCreateInstance/テーブル確保・初期化**、原作GUID4件の実バイト、終了時のテーブル要素Release経路。既存10時台ファイルは改変しない。

## 原作機械語で確定した生成経路
- `0x004BD2A0`から`0x004BD3E4`で`0x004BE480`（373 bytes）へ直接CALL。既存SQLiteと原作機械語が一致。
- `0x004BE4BF`で全体数`DAT_0065BED8`を読む。研究用PEの静的初期値は**1**（`01 00 00 00`）。実行時変更の不存在までは未証明。
- `0x004BE4E0`はサイズ=`count*4`のテーブル領域確保、`0x004BE4EB`で`stream+0x70`へ保存、`0x004BE4F7/FA`で各スロットをゼロ初期化。
- `0x004BE582`: `CoCreateInstance(CLSID_DirectMusicLoader, NULL, 3, IID_IDirectMusicLoader8, &stream+0x6C)`、HRESULTは`0x004BE588/8A`で検査。
- `0x004BE5BA`: ループ内で`CoCreateInstance(CLSID_DirectMusicPerformance, NULL, 3, IID_IDirectMusicPerformance8, &table[i])`、HRESULTは`0x004BE5C0/C2`で検査。
- `0x004BE5DD`: Performance8 vtable`+0xB0`の仮想CALL。DirectMusic8定義では**InitAudio**と整合。機械語で`0,0,0,8,0x40,0x3F,0`に対応する引数を積んでいる。
- **新規P0 VERIFY**: `0x004BE5DD`の直後`0x004BE5DF`は`INC EDI`。InitAudio相当の返値EAXを検査せず次の要素またはエピローグへ進む。
- `0x004BE820`の`0x004BEF20/27/2F`は`stream+0x70`から要素を選び、`stream+0x78`へコピーする。10時台のGetDefaultAudioPath呼出オブジェクトに到達する。

## 原作EXE内のCOM GUID（UUID little-endian復元）
| VA | GUID | 静的API同定 |
|---|---|---|
| `0x006096EC` | `d2ac2892-b39b-11d1-8704-00600893b1bd` | CLSID_DirectMusicLoader |
| `0x006096CC` | `19e7c08c-0a44-4e6a-a116-595a7cd5de8c` | IID_IDirectMusicLoader8 |
| `0x0060970C` | `d2ac2881-b39b-11d1-8704-00600893b1bd` | CLSID_DirectMusicPerformance |
| `0x006096BC` | `679c4137-c62e-4147-b2b4-9d569acb254c` | IID_IDirectMusicPerformance8 |

## 終了側の所有権境界と保留
- `0x004BE6B0`（353 bytes）が`0x00555CD0`の`0x00555E60`から呼ばれる。`0x004BE79D`でLoader8（+0x6C）を参照してRelease、`0x004BE7C0`でPerformance8配列+0x70を走査。
- 配列の非NULL要素について`0x004BE7D7`でvtable`+0x98`、`0x004BE7E5`でIUnknown::Release相当のvtable`+0x08`をCALLし、`0x004BE7EA`で要素をNULLに戻す。
- **VERIFY**: 初期化失敗後の既取得要素の寿命、vtable`+0x98`の厳密なAPI名、GetDefaultAudioPathで返されるAudioPathのRelease所有者、配列そのものの解放先は未確定。
- `InitAudio`が失敗してもPerformance8のポインタが非NULLのままの場合、10時台GetDefaultAudioPathの未検査経路が発生する条件と接続し得る。ただし実際のCOM失敗・クラッシュ・メモリリークは未実測。

## 監査・完了判定
- 新規`REA_20261026_11H_P0_DMUSIC_INIT_AUDIT.py`で原作PEバイト・Capstone・GUID・Ghidra SQLite（read-only）・関数境界とCALL siteを独立照合。
- 初回テストは`56/57 FAIL`（`0x004BE566`と`0x004BE567`の命令位置を1件取り違え）。監査条件を修正し、**58/58 PASS**でJSON排他保存・読み戻し成功。テスト条件58個であり、58関数VERIFIEDではない。
- `info=INDEX_ONLY / pseudo=INDEX_ONLY / assembly=TARGETED_NATIVE / callers=INDEX_ONLY / callees=INDEX_ONLY`。新規REA正式5種完備0、新規VERIFIED0。正式TODO/VERIFY/BLOCKEDファイル書込差分0/0/0。
- Wave1–5の**過去**64/64は`logs/progress_sync_20261011T153958076Z.json`に基づく旧実績。QUEUE/PROGRESSのEPERM-staleは現状維持。
- 原作ゲームGolden実測PASS=0、strict MATCH未測定、完全複製率未測定。
- PC online（SAITO）、`active.lock`なし。11時台開始時空きRAM約17.42GiB、CPU負荷不明。監査本体0.3577秒、研究全体所要時間は未計測。新REA/Ghidra/ゲーム実行0、Work不使用。
- 過去の13/14時台OFFLINE-UNSYNCEDは未同期。禁止VA/Wave6/FLS/REA export非接触。原本・MASTER/QUEUE/PROGRESS・既存run・他レーン・Git・スケジュールは編集していない。

## 次回優先
- P0: `0x004BE6B0`の`+0x98`の厳密同定と、`stream+0x70`配列領域を最終的に解放する経路を限定xrefs・ASMで追跡。
- 続けて`0x004BE5DD`（InitAudio）失敗後、`0x004BF685`（GetDefaultAudioPath）へ到達する必須条件とAudioPath所有権を詰める。動的Goldenは未実測のまま。
