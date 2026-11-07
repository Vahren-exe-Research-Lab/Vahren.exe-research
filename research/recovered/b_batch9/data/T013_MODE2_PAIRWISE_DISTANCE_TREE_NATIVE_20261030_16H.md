# B-20261030-1615-T013-MODE2-PAIRWISE-DISTANCE-TREE-01 — B/T013・mode2非空候補木の二重走査と距離キー（16H JST）
Owner: B/T013。STATIC (原作PE ASM) / INFERRED / VERIFY / NOT READY。原作Gameplay Golden PASS=0、strict MATCH=0、新規正式READY=0。
## 出典・継続境界
Local CompactでMASTER cp196旧値、規約、B owner5件、LANE_B_HANDOFF、15H研究・復旧索引を読取。11HのB-RC-20261030-1115-T028-T013-APPEND-SAFETY-01の拒否済み3要約はBLOCKED、再提出せず。SAFE134/HOLD21、Library54件差、10/25欠落本文はOPEN。
原作解析コピー EXE 2910720 bytes SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。統合V9 DB 141033472 bytes SHA256 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE、immutable mode=ro quick_check=ok。旧search.sqlite/READMEは欠落、V9入口00_START_HERE_UNIFIED_V9_20261023.mdを参照。active.lockなし・Java/Ghidra稼働報告なし。
## 新規Native ASM（前15Hのflag/phase選択は再計数しない）
1. 0x44C068 CMP [ESP+0x4C],0 / 0x44C06C JNE 0x44C0FE。0側は既知mode3 gate→一時木掃除。非零なら0x44C0FEで[ESP+0x48]側の候補木のbeginを取得し、0x44C114〜0x44C150で[ESP+0x38]側の別候補木と二重走査を開始する（木の正確な役割/producerはVERIFY）。
2. 0x44C114 [node+0x0C]→0x44C118 [+0xB8]のUnit候補、0x44C11F/0x44C125でその+0x220/+0x224を取得。0x44C150 node+0x0C→0x44C157 [+0xB8]の対候補、0x44C15D/+0x224で対応座標を取得。
3. 0x44C169 SUB x、0x44C16F/76 SUB y、0x44C173/78 IMUL 32bit、0x44C17B ADD、0x44C181 FILD signed32、0x44C185 CALL0x5E3B70 → 0x44C18A/92 QWORD保存。**座標の二乗距離相当（dx*dx+dy*dy）をfloat経由でdoubleキーへ渡す**。0x5E3B70は内部でx87 store/finite確認・制御を行い、このCALL単体でsqrt済みとは言えない。32bit overflowとNaN等はVERIFY。
4. 0x44C1AD CALL0x44D630で0x28-byte nodeを確保（0x44D633 PUSH0x28）。0x44D65F/61でdoubleキーをnode+0x10へ格納し、0x44D663/66で関連pointerを+0x18へ格納。0x44C1BC CALL0x44D1C0はdouble比較(0x44D1E1/0x44D24A)を用いた木への挿入。既存キーに当たる枝では0x44D27Cで生成nodeを解放するため、同一キーの組合せが個別に残るとは断定できない。
5. 0x44C1C8 manager+0xA7!=0、0x44C1D5 第一候補Unit+0x1A4==0、0x44C1EA 対候補Unit+0x1A4==2 の3条件成立時だけ、0x44C212 CALL0x44D630 / 0x44C221 CALL0x44D1C0の**第2挿入**を行う。0x44C1F7でEBP+0xBCを準備し元と異なるpayload方向を渡す。+0x1A4の戦術意味はVERIFY。
6. 0x44C226〜0x44C2CDで木iteratorを進めて各候補組を検討し、0x44C2D3で管理objectへ戻り後続処理へ進む。これを実最終ターゲット決定と同一視しない。
## Native window SHA / 非重複
PE VA0x44C150+0x160B SHA256=4056259477D0E29557B07EEA9F26EB18314BEF38DBED75DF879675BD1BACFB9B。0x44D630+0x65B SHA=471591165F535F5AFAA5E5156A433A372ED6BCAC1ED85DD4510D5C011A4885E6。0x44D1C0+0xD8B SHA=8B4F419755FD493567875EA6E9BFF2108DFD56396403A5A35772266A39874921。
B-owned T011/T012/T013/T024/T028 data/exe Markdown＋B HANDOFF計386件で0x44C150/0x44C1AD/0x44C1F3/0x44D1C0/0x44C2D3/0x44C169の先行literalはいずれも0。既15Hの0x44C0FE分岐先自体は既知・新規再計数0。未回収10/25および他owner全文の意味重複はVERIFY。
## 実装／Golden／再開点
距離計算の32bit符号・overflow、同距離時のキー衝突・木順序、manager+0xA7の由来、両一時木の候補識別、実Unit+0x1A4の意味と先頭選択/最終AI結果への影響を独立照合。Node/key lifetime、0x44D3F0側副作用もVERIFY。
原作無改変EXE＋20倍改変前DAT、同SAVE/MAP/input/RNGで非空候補木・同距離/異距離・特別属性条件・挿入結果・最終選択・翌tickを採取するまでGolden DESIGNED_NOT_RUN、Gameplay PASS0/strict MATCH0。
次：0x44C2DA〜0x44C414の二重木後処理および0x44D1C0同値整理、T011召喚/EXP・T012 damage・T024通常AI・T028士気を引続きP0。Ghidra全体解析、原作ゲーム実行、他owner/MASTER/REA/dev_lab/Git/設定/automationへの書込なし。