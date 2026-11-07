# B-20261015-1011-01｜T012/T013 通常kind2 child要素→resolver→技能処理選択の限定静的接続
[OWNER/STATE] 2026-10-15 10時台JST。T012 primary、T013 crossref。OWNER STATIC CANDIDATE（3 owner地点＋HANDOFFの保存/再読までREADY不可）。Task DONE+0／旧原作Gameplay PASS0／new-old strict MATCH0。
[IDENTITY] 原作同梱Vahren.exe SHA256 e8dac301050c8e630d7e0ce93aeefd95e641207d9c0576017f62ba46a8767187。新EXE解析・原本実行なし。
[LOCAL SOURCE] B保存 exe/T013_SKILL_HANDLERS_BOUNDED_NATIVE_20261013.txt の0x57EFA9..0x57F077（mode0 kind2 0x57EB40）、B data/T013_AI.md 既存57FA系support resolver証拠。保存ファイルをread-only照合。
[NEW VA FACT] 0x57EFA9/AFでSkill+0x100/+0x104のbegin/endを読む。0x57EFDEでbegin＋子offsetを選び、0x57EFE2..57F001では0x1Cバイトstack一時領域を作って選択要素のアドレスを0x402710へ渡す。
[NEW VA FACT] 0x57F006 MOV ECX,[EBP+0x1DC]→0x57F00C CALL 0x4678A0。その戻りEAXの[+0x74]を0x57F011で検査し、zeroなら0x57F02E/0x57F045から0x580280、nonzeroなら0x57F06Fから0x54F720に進む。
[ADDITIONAL SOURCE] 0x57F0C4..0x57F0EC のSkill+0xF4 optional末尾もSkill+0xE4の参照を0x402710へ渡し、0x57F0E1で[EBP+0x1DC]、0x57F0E7で0x4678A0、0x57F0ECで戻り対象[+0x74]を検査する。末尾成功/攻撃成立は未認定。
[INDEPENDENCE] 既B-20261015-0611-01はMP debit/root/child/optional/ALの全段、B-0709-01はvector再ロード、B-0821-01はzero子のguard。本増分は **kind2 child/optionalが一時領域→0x4678A0 lookup結果→+0x74 dispatchという解決境界を経る**点。既T013 support 57FB02..57FB75の同helper経路を新証拠として二重採録しない。
[FACT/VERIFY] 上記実命令・順序はSTATIC。0x402710の高水準意味、[EBP+1DC]の論理owner、0x4678A0の名前解決/失敗契約、Skill+100/104を作るDAT setter、runtime継承、callee実作用、実射出/HP/MP/乱数はVERIFY。未解決helperが正常returnすることを捏造しない。
[WORK IMPACT] 28byte child recordを最初からlive Skill pointerと同一視せず、要素ordinal→一時コピー→resolver受付→返値[+74]種別分岐→factory receiptに分解。parent/raw next3との対応は未確定。root/child/optional・対象・MP・戻りALを分離。
[GOLDEN] 未改変原作で合法kind2 mode0の子0/1/2とoptional +F4有無を可視観測できるときだけ、同SAVE SHA/seed/入力で発動時刻、弾/子効果、MP/HP、次行動をold/new比較。DESIGNED_NOT_RUN、原作Gameplay PASS0、strict MATCH0。内部pointer/VAだけならINELIGIBLE。
[NEXT] [EBP+1DC]/0x4678A0の既保存callee契約を探し、Skill+100/+104のsetterを既保存B資料のみで追う。失敗返値・vector mutation・実合法技能はVERIFY。T012 A18/A1C/latch/4E7ED0/MP fallbackとT013優先も未解決。
[SAFETY] 原本ZIP/EXE/SAV・MASTER/T018・他owner/REA/dev_lab/Work/WRQ・Git/push/設定/automation変更0。拒否済0x5710C0..571500ほかの新規逆解析/別shell/path/tool/Remote迂回なし。重いGhidra/REA/test起動0、CPU実率n/a。
[READY GATE] detail/T012 owner/T013 xref/B HANDOFFの4点readback後だけ B-20261015-1011-01 に限定STATIC READYを認定し、Eのみ正式MASTER統合。