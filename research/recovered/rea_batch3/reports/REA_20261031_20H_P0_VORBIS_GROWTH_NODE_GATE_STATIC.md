# REA 2026-10-31 20H｜Vorbis確保容量のgrowと退避ノードのNULL境界（P0）
研究ID: `REA-LOCAL-20261031-20H-P0-VORBIS-GROWTH-NODE-GATE-STATIC-01`
Owner: REA / T015 / **PC-SAVED / STATIC + INFERRED / VERIFY / NOT READY**。前回19H reallocの旧ポインタ喪失は既知として重複計上しない。

## 出典・重複・索引
- 研究専用PE `rea_lab/targets/hakushin067_Vahren.exe`：SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。同一原作bytesをCapstoneで独立照合。
- 既存 `REA_20261031_19H_P0_VORBIS_REALLOC_OWNER_LOSS_STATIC.md`、そのEVIDENCE、18H teardown、知識ベース `kb.py addr/docs/research 0x5D4980`、非公開GitHub `develop` の `REF_AUDIO_VORBIS.md`を参照。今回の `0x5D4980`ノード確保条件は未収録。
- 旧 `search_index/README.md` と `BUILD_MANIFEST.json` はENOENTのため、既存 `00_START_HERE_UNIFIED_V9_20261023.md` と `HAKUSHIN067_UNIFIED_V9_20261023.sqlite` をread-only。V9関数範囲 `0x5D4980..0x5D49E5`、calleesは2件のCRT malloc、callers索引21件。今回の原PE独立E8確認は4件（malloc2、caller2）、前回cleanup E8確認を含め計5件。V9疑似CをREA正式5方法の証拠として新規計上しない。
- 関数窓 `0x5D4980..0x5D49E6` SHA256 `EC4BBFD1046A9D3228F53F5FD3D10DF6071B02835C2BDE91D8D23350589BC566`。前回cleanup窓SHAは別証拠として非重複照合した。

## 新規STATIC（原PE x86命令）
- `0x5D4988` は `outer+0x48` の旧使用バイト数をEBXへ取得。`0x5D498F/92` は要求を `(size+7)&~7` で8byte整列。`0x5D4995/98/9B` は旧使用量と整列サイズの加算値を `outer+0x4C` 容量と**signed JLE**比較し、収まれば再確保しない。
- 容量不足かつ `outer+0x44 != NULL` なら `0x5D49A5` で `malloc(8)`。**この戻りEAXをNULL検査せず** `0x5D49B3 mov [eax+4],ecx`、`0x5D49B9 mov [eax],edx`へ進む。`0x5D49B0` で `outer+0x50 += EBX`（旧使用バイト数）、`0x5D49BB` で退避リスト先頭 `outer+0x54`を更新。
- さらに `0x5D49C2` で整列サイズの新バッファをmallocし、`0x5D49CA` で戻り値を `outer+0x44`へ未検査保存、`0x5D49CD`で使用量 `+0x48=0` に戻す。戻りアドレスは `outer+0x44 + (再初期化後の+0x48)`であり、grow前EBXの旧使用オフセットを足して返すわけではない（元監査JSONの旧使用という語の精密化）。
- `0x5D471B` と `0x5D4739` の呼出元 `0x5D45E0` は、V9疑似C上では返ったポインタを配列格納先へ使用するが、全呼出元の制御フロー・入力大小関係・実際のmalloc失敗到達性は未検証。
- 19H `0x5D49F0` の `outer+0x50 != 0` realloc条件のproducerは本関数で明確化：**+0x50へ加算するのは旧使用バイト数であり、確保容量とは別**。後続のrealloc上書きリーク候補自体は再発見扱いにしない。

## VERIFY・統合候補・保存
- 未証明：最終mallocがNULLを返す環境、CRT new-handler/例外挙動、実ゲームOOM・クラッシュ・リーク、容量計算のsigned overflow、他の19 caller入力条件、ABI、別所有者alias、原作Golden。
- `KB_CANDIDATE`: `0x005D4980` / `0x005D49A5` / `0x005D49B3` / `0x005D49C2` / `outer+0x44/+0x48/+0x4C/+0x50/+0x54` の対応。source原PE SHA、関数窓SHAとE8一覧は `REA_20261031_20H_P0_BUFFER_GROWTH_EVIDENCE.json`。**STATIC**＝命令・分岐・未検査store、**INFERRED/VERIFY**＝確保失敗の影響。自動で辞書の確度を上げない。knowledge書込・push・mergeしない。
- 監査 `REA_20261031_20H_P0_BUFFER_GROWTH_AUDIT.py`：元PEに対し **49/49 PASS**。独立読戻しは別 `REA_20261031_20H_P0_BUFFER_GROWTH_READBACK_VERIFY.py` の結果を参照。正式5種完備の増分0、正式VERIFIED増分0、QUEUE/PROGRESSのTODO/VERIFY/BLOCKED変更0/0/0、原作Golden PASS0/strict MATCH0、READY0、完全複製率未測定。
- PC接続正常、開始時active.lockなし、Java/Ghidra観測0、空きRAM約15.77GiB。CPU負荷・全所要時間・監査単体実測時間は不明。原作実行、Ghidra新規再解析、共有KB/A-E/MASTER/Git/スケジュール変更なし。
- **RECOVERY-ID `REA-RECOVERY-20261031-20H-QUOTE-SYNTAX-OTHER-01`**：最初の一行読取用PythonコマンドはPowerShellの引用符処理でSyntaxError、成果未生成。安全拒否・接続障害ではない。以後REA片側の新規read-only probeスクリプトで正しい元機械語を取得、監査49件保存。旧失敗操作の再実行なし。未保存の知見なし。
- **次**：`0x005D4980` の残余callers（特に`0x005DEDF0`、`0x005E06C0`）、`0x005D45E0` のerror戻り・サイズ上限、`0x005D49F0` のrealloc要求長の条件を非重複で静的比較。原作動的Goldenは別工程。
