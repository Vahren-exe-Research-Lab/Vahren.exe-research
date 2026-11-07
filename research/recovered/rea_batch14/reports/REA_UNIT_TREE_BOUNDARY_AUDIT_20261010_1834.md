# REA独立監査：Unit tree readerの3分岐と入力状態（2026-10-10 18時台 JST）

- 対象: 迫真戦記0.67保存済みREA 6.1.0/Ghidra 12.1.4のread-only静的証拠。新規Ghidra/旧EXE実行0。
- source SHAは保存済みrunの開始/終了値 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。本回の再ハッシュではない。
- T014 / Unit reader `0x58E870`、writer `0x58EFD0`、共通文字列writer `0x470830` を比較。これらの5種証拠は既存VERIFIEDで、新規昇格なし。
- reader run `20261009T223622536Z`: assembly `ev_dd3a4fa049e9751b44ab874ad4dce5fdfbe23f8fc364274bf923e7a9cbebb839`、pseudo `ev_992508cdab86c44fc73e0f72aa80b7ab30679a2b84144a444f5afe7a7d80760d`。
- writer assembly `ev_fc8c23eb060d4cca74ce05f46674a7ceb09d69e81637d412eed595d6c6e0cedb`、string writer assembly `ev_1ffa032ec901cde47d6811b2e2941ff163adbcd1a68d9573bed5f6efe6b58d02`。

## 今回の追加分：+0x130 treeの入力は「空文字・固有marker・通常key」の3分岐
- `0x58ED10..1E`: 文字列read直後に長さを検査。長さ0では`0x58EE36`を経て`0x58EE8B`の次fieldへ進む。marker終端処理`0x58E480`はこの経路では**呼ばれない**。
- 長さ非0なら`0x58ED24..75`でグローバル文字列 `0x68B9D0` と比較。完全一致時だけ`0x58EE58..5F`で`0x58E480`を呼び、次fieldへ進む。
- 非空かつmarker不一致では`0x58ED7B..85`でDWORD系のstream reader `0x42E700`を呼び、`0x58ED93..A4`でstream state bitsを判定。
- stream stateが問題を示す枝は`0x58EFA2`へ分岐し、`0x58EFAB..BD`の異常処理（疑似コード上はLoadException throw）へ進む。成功枝は`0x58EDAA..E8`でkey/valueの挿入処理を行いtree読込loopを継続。
- writer `0x58F343..38C`はtree node由来key文字列＋DWORD、`0x58F405..40A`は固有marker `0x68B9D0` を保存する。vectorの空文字終端(`0x68B3A8`)とこのtree markerを単一種類として扱わない。
- **新しく明確になった点**: Unit treeの空文字経路は専用marker一致経路と副作用が違う。また非markerレコードではDWORDを読み、stream error状態を調べてから挿入する。

## 確度と再実装上の課題
- STATIC CONFIRMED: 上記CALL/branchの順序。`0x58E480`の作用、`0x42E700`のexact I/O、throwの上位回復、実ゲームで空key/不正byteが到達可能かはVERIFY。
- 共通writerは不適格byte混入時にその文字列全体を空として書く。tree keyが空へ変換された場合のreader分岐差は静的に成立するが、原作ファイル破損や正規ゲームバグは**未観測・断定禁止**。
- 比較fixture案: tree marker/empty key/通常key＋DWORD/途中stream failureを分離。すべてDESIGNED・旧EXE実機NOT RUN。
- 次回優先: 既存証拠から`0x58E480`の呼出契約とtree後続の読み込みを精密化。未取得Wave4 `0x4930C0`/`0x514D60`/`0x428010`等の新Ghidra取得は既往安全拒否が解消するまでBLOCKED。
- 進捗: Wave1 16/16、Wave2 10/10、Wave3 10/10、Wave4 3/12、累計39/48・今回新規VERIFIED0・P0 20/21・P1 19/27・TODO8・VERIFY1。
- MASTER checkpoint70: 研究DONE9/34。旧EXE実機golden PASS0、ゲーム再実装率は測定していない。
- 今回はQUEUE/PROGRESSを修正せず、既存EPERMによるSTALE維持。A-E/MASTER/T018/原本/対象EXE/Git/MCP設定/スケジュール変更なし。過去の拒否操作の再試行・迂回なし。
