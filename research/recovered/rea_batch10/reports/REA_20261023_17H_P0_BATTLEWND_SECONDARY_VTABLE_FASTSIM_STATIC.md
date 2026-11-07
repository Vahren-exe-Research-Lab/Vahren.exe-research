# REA-LOCAL-20261023-17H-P0-BATTLEWND-SECONDARY-VPTR-STATIC-01
日時: 2026-10-23 17時台 JST / owner=REA / T010・T012 P0（T014はSAVE担当、計上しない）。
状態: STATIC / VERIFY / NOT READY。研究PC正本への統合は行わず、REA所有の独立証拠のみ新規保存。
## 先行資料・非重複
- MASTER_LEDGER、evidence/ANALYSIS_LANES_PROTOCOL、decomp_task README/QUEUE/PROGRESS、logs/progress_sync_20261011T153958076Z.json、16時台FASTSIM報告、統合V9入口をread-only参照。
- 16時台既存確定: 0x40E220→0x40E2F0、500 tick上限、50 tick毎の二陣営検査、0/1/2返却、0x40E220の直接E8 caller 0。本件ではこの既知内容を新規件数に加えない。
- 出典: 承認済みコピー rea_lab/targets/hakushin067_Vahren.exe、今回の実測 SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
- 新規関数索引: search_index/HAKUSHIN067_UNIFIED_V9_20261023.sqlite、実測 SHA256=2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE。verify=V9_INDEPENDENT_READBACK_PASS、登録11950関数。PC標準のsearch_current.pyは依然V3。
## 新規発見：0x40E220の入口はBattleWnd第2 vptr のvirtual slot +4
- V9 refs-to 0x0040E220 は DATA ref 0x006380D0 1件、PE HIGHLOW pe-to も同site 1件。E8/E9/EB flow-callers=0、未認識の仮想call siteは未解決。
- rdataメモリ: [0x006380C8]=0x0063C594 (RTTI COL), [0x006380CC]=0x0040ED70 (slot+0), [0x006380D0]=0x0040E220 (slot+4)。
- RTTI 0x0063C594: signature=0、subobject offset=0x28、type descriptor=0x0068BCBC、名前=.?AVBattleWnd@@。
- 別のprimary RTTI 0x0063C5A8: subobject offset=0、同じtype descriptor=0x0068BCBC。primary vtableは0x00638074、secondary vtableは0x006380CC。
- グローバル実体 0x008B8C90: 0x0051D29Dで [0x008B8C90] ← 0x00638074、0x0051D2A7で [0x008B8CB8] ← 0x006380CC（差+0x28）。
- 後処理0x0040CE3B/0x0040CE41でも [EBX] と [EBX+0x28] へ同じ各vptrを設定。V9 refs-to 0x006380CCは0x0040CE41 と0x0051D2A7 の2箇所。
- 関数0x0040E220は0x40E22Aで MOV EDI,ECX、0x40E27Aで LEA ESI,[EDI-0x28]、0x40E27Dで MOV EAX,ESI、0x40E27Fで直接CALL 0x0040E2F0。
## 実装上の意味と依然未解明な箇所
- 0x40E220へのECXはBattleWnd primary先頭ではなく、secondary subobject (+0x28) のthis pointerを受ける経路と整合する。0x40E2F0には EAX=ECX-0x28 が渡る。この受渡しは逆コンパイラの__fastcall疑似Cのみで決めず実ASMで確認した。
- 0x40E220側の [ECX+0x78] / [ECX+0x7C] はprimaryからなら +0xA0/+0xA4、[ECX+0x19C]はprimary+0x1C4。オフセットの基準を混同しない。
- BattleWndのこのvirtual slotがいつ・どこからディスパッチされるか、反復処理がどのゲームモードで起動するかは未確定。データ参照のみで「呼び出し確認済み」と言わない。
- 既知の 0x40E644/0x40E658 の vptr+0x18 は 0x40E2F0に渡されたprimaryから [+0x1C8] と [+0x1CC] の *別オブジェクト* へ発行する間接CALL。今回のBattleWnd secondary vtableの+0x18と同一視しない。
- 0x40E644/0x40E658の実装先、戻り値4の意味、0/1/2の原作実機での陣営対応、戦闘終了の厳密な順序は依然VERIFY。
## 機械語・構造の独立検証
- PE実バイト照合13件、RTTI COLとtype名3件、E8相対宛先1件、原作EXE SHA1件 = 18/18 PASS。上記V9索引は別取得でrefs-to/pe-toを突合。
- 代表hex: 0x51D29D=c705908c8b0074806300、0x51D2A7=c705b88c8b00cc806300、0x40CE41=c74328cc806300、0x40E27A=8d77d8、0x40E27F=e86c000000、0x6380D0=20e24000。
- RTTI: 0x63C594 offset=0x28、0x63C5A8 offset=0、双方type descriptor=0x68BCBC。静的コンパイル時の構造であり実行時vptr変更可能性を排除しない。
- 保管するJSONに個別観測VA・値・検証件数を記録し、本MarkdownとJSONを独立にreadbackする。
## 正式進捗・安全
- 保存済みprogress_sync_20261011T153958076Z.jsonではWave1～5 64/64、queueUpdate=STALE_RENAME_DENIED / humanReadableProgress=SKIPPED_QUEUE_STALE。生QUEUE/PROGRESSの古い表示は更新しない。
- 新規正式REA VERIFIED=0、新規5種info/pseudo/assembly/callers/callees完備=0、正式TODO/VERIFY/BLOCKED差分=0/0/0。
- Golden原作実機PASS=0、strict MATCH=0、完全複製率=未測定。ゲーム/新REA/Ghidra実行=0、PC正本・原本・A～E・MASTER・QUEUE・PROGRESS・Git・スケジュール変更=0。
- 禁止VA 0x5710C0..0x571500、既拒否Wave6、拒否済みREA exporter・別検証Python保存には一切再試行なし。
## 次回のP0
- [VERIFY] 0x006380CC+4の実行時virtual dispatch call siteを、安全な静的登録・基底クラスの呼び出し経路で追う。フックABIを未認定のまま実装しない。
- [VERIFY] 0x40E644と0x40E658のreceiver（primary+0x1C8/+0x1CC）の構築元・vptr+0x18具体実装、return4の判定意味を追う。
- [DESIGNED NOT RUN] secondary this補正、0x80000008 gate、return0/1/2、時間満了/片側壊滅・戦略反映を同一run Goldenで比較する条件を作る。
