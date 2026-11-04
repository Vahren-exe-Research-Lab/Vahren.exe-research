# REA 2026-10-31 17H｜Vorbis bitbuffer初期化・二段階の確保失敗条件（P0）
研究ID: `REA-LOCAL-20261031-17H-P0-VORBIS-BITBUFFER-TWOLAYER-ALLOC-STATIC-01`。Owner=REA / Task=T015。状態: **PC-SAVED / STATIC+INFERRED / VERIFY / NOT READY**。
既存16H `REA-LOCAL-20261031-16H-P0-VORBIS-POSTINIT-OTHER-CALLERS-STATIC-01` の `0x5D4963` を引継ぎ、16Hの親0x48確保・15Hの戻り値破棄・09H CRT malloc挙動を再発見として二重計上しない。

## 源泉・非重複・環境
- 正本: `rea_lab/targets/hakushin067_Vahren.exe` SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。統合V9 `rea_lab/headless_analysis/search_index/HAKUSHIN067_UNIFIED_V9_20261023.sqlite` SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`、SQLite quick_check=ok。
- PC Localで先行MASTER/担当規約/QUEUE/PROGRESS/16H証拠、knowledge README/SYNC_STATUS、private GitHub developのREF_AUDIO_VORBISと専用V9入口を参照。旧索引README/BUILD_MANIFESTは現行配置に存在せず、既知OTHER/配置差異。拒否済みV3標準化を再試行せず別名V9読取CLIを使用。
- `knowledge/kb.py addr/docs 0x5E6C70` は辞書未命名・全文索引の直接言及なし。V9で `0x5E6C70` 入口、body `0x5E6C70..0x5E6C9D`、呼出元 `0x5D4963` 1件、CALLEE `0x5E6C83 -> 0x5B9BC8` を確認。native ABIは未確定。

## 新しいSTATIC差分
- 元x86 `0x5D4900` は非ゼロ入力時に親0x48バイトをcallocし、`ESI=0..14` の計15スロットを構築する。 `0x5D4941 cmp esi,7`、`0x5D4944 jne` により**index 7だけ**親の埋込 `parent+0x04` を `parent+0x28` へ渡し、他14件は `0x5D4952 calloc(1,0x14)` で独立構造体を確保する。
- いずれのスロットも `0x5D495E` でポインタを取り出し `0x5D4963 E8 -> 0x5E6C70` を呼ぶ。`0x5E6C74` はstack argumentをESIへ、`0x5E6C79 mov [esi],eax` はESIのNULL検査前に0を書込む。**14件のcallocが最終的にNULLを返したと仮定すると、この書込へ到達する条件付き無効書込候補**。
- `0x5E6C7B push 0x100` / `0x5E6C83 E8 -> CRT malloc 0x5B9BC8` の後、`0x5E6C88/8B` で戻り値をESI+0x08/+0x0Cへ保持し、`0x5E6C91 mov byte ptr [eax],0` で**戻りポインタのNULL検査なし**に書込む。malloc(256)が最終失敗したと仮定すると、埋込index 7を含む全スロットの初期化で無効書込候補。実際のOOM発生、CRT new-handler再試行、上位エラー回復、ゲームクラッシュは未実測。
- 別の親関数 `0x5D0B60` は `0x5D0B7A -> 0x5D04E0` の直後 `0x5D0B82 test eax,eax / 0x5D0B84 js` で負の戻り値を遮断し、`0x5D0B8A -> 0x5CF970` の直後 `0x5D0B8F test / 0x5D0B91 jne` で非ゼロを遮断。後段の `0x5D0D67 -> 0x5CF970` も `0x5D0D6C test / 0x5D0D6E jne` で分岐する。**これは15H/16Hのpost-init EAX破棄を是正する保証ではない**。

## 独立検証・KB_CANDIDATE
- `REA_20261031_17H_P0_BITBUFFER_NATIVE_PROBE.py` に元PEからの関数入口全体disasmを保存。`REA_20261031_17H_P0_BITBUFFER_INIT_AUDIT.py` は元PEの命令境界35件とE8 7件、V9関数所有権3件、CALL graph、前回研究ID/DB整合性を独立検証。結果 **98/98 PASS**、監査 **2.4727秒**。
- 構造化証拠 `REA_20261031_17H_P0_BITBUFFER_INIT_EVIDENCE.json` SHA256 `7D46EF2F5C79EA4C80E0B9F0ADEE5966D6EF8740C5381A03DC6B627312003511` に命令bytes、E8、元PEウィンドウSHA、出典、statusを保存。静的命令=STATIC、確保失敗帰結=INFERRED、実ゲーム到達性=VERIFY。
- **KB_CANDIDATE**: Vorbis bitbuffer init `0x5E6C70` と `0x5D4900`、親guard `0x5D0B60`。未登録/未統合として統合担当へ委託。名称・ABI・不具合の実証・Golden/READYを自動確定しない。formal新規REA 5種証拠完備0、新規VERIFIED0、既存64/64維持、TODO/VERIFY/BLOCKED差分0/0/0。原作Golden PASS0、strict MATCH0、完全複製率未測定。
- 起動時の最初のオーケストレーション構文が `SyntaxError: Invalid regular expression` で失敗（RECOVERY-ID `REA-RECOVERY-20261031-17H-ORCHESTRATOR-SYNTAX-01`、分類OTHER）。実ファイル操作前に停止し、正規のread_multiple_filesで復旧、未保存研究はない。16Hの補助的PowerShell hash/list/lock安全拒否は一切再試行していない。
- 原作ゲーム・新Ghidra/REAを実行せず、原本ZIP/EXE/SAVE、他担当、MASTER、QUEUE/PROGRESS、共有knowledge、Git、スケジュールは変更なし。CPU/RAM負荷と総作業時間は未測定（不明）。対象コードへの静的アクセスのみ。
- 次優先: `0x5D4A60` の埋込index7と14個のheap構造体の解放選別、`0x5CF970` の上位エラー伝播、部分確保後のcleanup到達性を既存V9から調査する。
