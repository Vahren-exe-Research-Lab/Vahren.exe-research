# 迫真戦記 B・T012｜生成試行番号からTroop選択への跨関数分岐（2026-10-21 13時台）

- 研究候補 ID: `B-OFFLINE-20261021-1310-01`（新規B LIMITED CANDIDATE、NOT READY）
- 復旧 ID: `B-RC-20261021-1310-LOCAL-DISCONNECT-01`（CONNECTION、OFFLINE-UNSYNCED）
- Task / owner: T012主・T011参照。E所有MASTER統合、他レーン・REA領域編集なし。
- 対象: 迫真戦記 ver0.67同梱EXE、SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
- 証拠分類: caller引数=STATIC X86（既保存PEのCapstone ASM）、callee条件=STATIC GHIDRA_PSEUDOC、跨関数作用=INFERRED/VERIFY、原作DYNAMIC=NOT RUN。

## PC正本・安全・重複の先行照合
- このrun前半のDesktop Commander Local Compact読取成功：`MASTER_LEDGER.md`末尾（E audit 12:47、最終正式checkpoint195、E記載累計595、今回総数独立再集計なし）、`evidence/ANALYSIS_LANES_PROTOCOL.md`、`evidence/LANE_B_HANDOFF.md`、検索基盤`README.md`/`BUILD_MANIFEST.json`。正本の旧不完全JSONと既存拒否の区別を継承。
- 検索manifest status PASS、DB `search.sqlite` 53,927,936B、SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`（manifest記載、今回全DBハッシュ再計算なし）。内部10,268・直接CALL47,550・間接候補5,109、対象EXE SHA一致。
- search indexに`active.lock`未見、Local active sessionsなし。CPU瞬時実使用率は取得できず低負荷保証なし。
- PC復旧索引：26候補`X14/P4/I0/D1/C4/L2/O1`（履歴）、10/21の02～08時台7研究資料は09時台PC不存在、09時台T012本文はPC保存と前回報告。今runで過去本文の回収/重複投入0。
- 以前の08時台本文PCコピー・HANDOFF追記のSAFETY_REFUSALおよび10/20不完全JSON168行は従来のBLOCKED/INVALID維持。拒否本文・禁止VA 0x5710C0..0x571500・他に拒否記録のある0x58021E..0x580340の新逆解析/別経路リトライなし。
- 後半Local接続は `UNAVAILABLE: ... Connection timed out`→`INVALID_ARGUMENT: ... Session terminated` と失敗。これはCONNECTIONであってSAFETY_REFUSALではない。正本書込み・HANDOFF追記を未試行／未保存、元拒否操作の迂回なし。Library単独保全のみ。

## 具体的な静的差分
- `0x5501A0` のkind4分岐 `0x5501D6 cmp [EDI+0x40],4`→`0x550219 call 0x54E7B0`。
- 独立に既保存された`rea_lab/headless_analysis/search_index/P0_SUMMON_CALLSITE_ASM_20261021.json`で、CALL直前`0x550209 MOV EAX,[ESI+0x1F0]`→`0x55020F PUSH EAX`、`0x550216 PUSH EBX`、`0x550217 MOV EDX,EDI`、`0x550210 LEA ECX,[ESI+0x1E8]`を確認した。スタック引数第2項（callee第4引数）は生成試行カウンタ+0x1F0である。先行独立研究`P0_SUMMON_EXP_OWNER_REPORT_20261021.md`のABI表と一致。
- `0x54E7B0` の検索DB擬似C（`search.py function 0x54E7B0 --max-chars 12000 --limit 6`）では`local_24c=param_4`。選択モード `local_284 >= 2` かつ`sourceUnit+0x1D0 != NULL`の場合に、`local_24c==0`なら`0x567EE0`経由の新Troop確保候補、非0ならsourceUnit+0x178..+0x17Cの末尾memberから`+0x1D0`を取得（無ければNULL）する。モード名、成立条件、確保成功、所有者はVERIFY。
- `0x5501A0`の擬似Cでは、kind4のcallee帰還後に、返値の生成成功チェックとは独立してmanager+0x1F0を1加算（初期レジスタ/実ASMの加算命令位置はこのrun未抽出）。定義+0x74で上限判定し、周期+0x78が0なら条件付きで同一呼出し内再試行する。
- **増分INFERRED**：kind4・mode2/3・有効source Troop・次の試行が存在という条件では、試行前カウンタ0と非0が`0x54E7B0`内部のTroop取得分岐を変える。前の試行で候補が空（Skill+0x14C=0かつ+0x158==+0x15Cの早期cleanup）でも試行数は進み得るため、次回のTroop選択分岐は「実際に生成できたUnit数」ではなく**試行番号**に依存し得る。初期+0x1F0=0・モード2/3実成立・同一owner・空候補から後の成功候補への移行は未実証。
- これは既B `B-20261013-1134-01` の子関数body、`B-20261021-0910-01` の上位周期、`B-OFFLINE-20261021-1110-01` の空候補quota、および独立P0 reportのABI/モード表を再計上しない**新しい跨関数条件結合**である。PC最新版の全内容との意味重複監査未完成のためB限定READYには昇格しない。

## Golden設計／次回再開
- DESIGNED_NOT_RUN: 同一合法EXE/DAT/SAVE/入力/技能・同一召喚主で、(a) +1F0開始0/非0の合法到達、(b) Skill troop mode0/1/2/3、(c) sourceUnit+1D0 NULL/非NULL、(d) 空候補・非空候補、(e) 周期0/正値、(f) 直近Troop member有/無を分ける。原作の可視部隊/個体数、同一owner、生成時刻、EXPリンク、戦闘後SAVEを旧新同SHAで比較する。内部値が合法UIから不可観測ならUNKNOWN/INELIGIBLE。
- 旧原作Gameplay Golden PASS=0／strict MATCH=0／Task DONE追加0／E公式READY追加0。
- 次の許可済み調査先：B所有の`exe/T012_SUMMON_CORE_54E7B0_NATIVE_20261013.txt`の既保存`0x54EF94..0x54F096`部分にあるmode2/3と第4引数のx86分岐（元の拒否領域外）をread-only照合し、+0x1F0の初期setter/再初期化者を**既存検索索引と許可済み保存証拠のみ**で特定する。`0x550219`に対応するASМ callerは独立報告の既存証拠を再利用し再抽出しない。
- PC復帰後：MASTER checkpoint / B owner/HANDOFF / Recovery Index / READY と本IDの重複・owner・競合を再照合、B所有資料に単独の未同期差分を一度だけ取り込み、保存後独立readback。EのMASTER統合はEのみ。
- 本文はChatGPT Library B/dataへのオフライン研究候補として保存予定。PC B data、LANE_B_HANDOFF、MASTER、原作、Git、REA、Work、他レーン、既存automationは変更なし。
