# B/T012｜0x00464290 Ghidra関数ボディ5Bギャップの実証・18H疑義訂正
研究ID: B-20261024-1917-T012-PRESENCE-GHIDRA-SPARSE-BODY-GAP-01
日時: 2026-10-24 19:17 JST。owner B/T012。判定 STATIC-ORIGINAL-PE-ASM / STATIC-GHIDRA-BODY / VERIFY / NOT READY。
## 先行確認と安全境界
Desktop Commander Local Compact接続成功。MASTER最終既確認 checkpoint196・正式READY596 (A115/B229/C136/D116) は旧集計、今回E再集計無し。
規約、B HANDOFF、B T012資料、未同期回収索引、既拒否0x5710C0..0x571500／0x514C50／0x5769B0 XREFを先読。拒否対象の再試行・迂回0。
10/21 PC回収済22ファイルと後発OFFLINE10研究のID単位照合は未完。10/24 10H～18HのLibrary/会話資料をPCに全件取り込んだとは扱わない。18Hの原文はPC未同期。
search_index README/BUILD_MANIFEST、既存search.py (0x00464290のみ) と抽出済 ALL_FUNCTION_BODY_RANGES_ORIGINAL_20261021.jsonl をread-only照合。再Ghidra/REA/原作起動なし。
現物 EXE SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187 一致。旧検索DB SHA256 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF 一致。
## Ghidra original function bodyの実範囲 (初めて直接確認した増分)
entry=0x00464290, body_size_bytes=802, span=807, gap_bytes=5, range_count=2, max_address=0x004645B6, naive_end_va=0x004645B1。
range1=0x00464290..0x0046444A (443 bytes), range2=0x00464450..0x004645B6 (359 bytes)。443+359=802、入口～末端807の差5Bは **0x0046444B..0x0046444F**。
出典: search_index/ALL_FUNCTION_BODY_RANGES_ORIGINAL_20261021.jsonl の entry_va=0x00464290 行。Ghidra pseudocはvoid、code_sha256=68EBE29629531DA6FB5AA44E315BBF120DD5AACB8F7400AC5619845748E5BB56。
## 原作PEの当該5バイトと周囲（PE section RVAで読み、Capstone x86 32bit）
0x0046443B MOV AL,1 ; 0x0046443D JMP 0x0046457C ; 0x00464442 MOV ESI,[EAX+0x28]
0x00464445 MOV [ESP+0x14],EBX ; 0x00464449 JMP 0x00464454 (EB 09)
0x0046444B JMP 0x00464450 (EB 03) ; 0x0046444D LEA ECX,[ECX] (8D 49 00、意味上NOP)
0x00464450 MOV EDI,[ESP+0x1C] ; 0x00464454 MOV EAX,EDI
Ghidraが除外する5Bは短いJMP2B+NOP相当3Bであり、関数後尾ではない。0x004645B3 MOV AL,1 / 0x004645B5 JMP 0x0046457Cを含む末尾はGhidra body範囲2内にある。
## 18H成果の限定訂正と互換性
B-OFFLINE-20261024-18H-T012-PRESENCE-TAIL-CFG-01の『802 vs 807』は **関数終端欠落の証拠ではない**。802は非連続body内アドレス総数、807は最大連続スパン。先行18HがVERIFY留保した疑義を今回「差分の原因＝内部5B gap」として解決。先行研究ID・原文は消去/上書きしない。
従って逆コンパイルDBで size_bytes だけから entry+size-1=0x4645B1 を関数末尾と仮定すると誤る。body_ranges を優先する。今回の確認で『Ghidraのvoid戻り値宣言がAL真偽を表現しない』という17Hの別問題は解決しない。
gap内部への未知の外部/間接流入、正確なC++型、属性優先順位、DAT実到達はVERIFY。これらを実行時に確認していない。
## 非重複・Golden・再開点
既B-17HのAL戻り値/50回上限、既18Hの0x004644C3→0x004645A0→0x004645B3成功経路は再計上0。今回の新規増分はGhidra元body range2組とgap実ASMのクロス検証・誤判定の訂正。
無改変同一EXE・X20変更前DAT・同SAVE/MAP/input/RNGでstr_ratio省略/明示0/親継承/50階層境界とダメージ・HP・次tickを比較。DESIGNED NOT RUN。
原作Gameplay Golden PASS0、strict MATCH0、新B正式READY0、E MASTER統合0、Task DONE0。
次回: 0x004644BCの検索result-vs-header分岐と0x0046444B gapへのcross-reference有無を、既安全拒否を除外したB担当STATICのみに限定して検証。PC旧Library資料のID・SHA・owner突合を行い一度だけ取り込む。