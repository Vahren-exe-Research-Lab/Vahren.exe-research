# 迫真戦記 ver0.67 REA｜23時台 P0 DirectMusic乱数選択・FTOL共有tail
研究ID: REA-LOCAL-20261026-23H-P0-DMUSIC-FTOL-SHAREDTAIL-STATIC-01
状態: PC-SAVED / STATIC / VERIFY / NOT READY（2026-10-26 JST）
対象PE SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
旧検索DB SHA256: 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF
統合V9 SHA256: 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE

## 新規静的成果（過去22H・2026-10-11の断片との非重複）
旧研究は0x4BEEE3で名前探索結果を判定、0x4BEEFAで個数読み、0x4BEF1BでFTOL、0x4BEF27で配列要素取得と報告。2026-10-11のSOURCE_RECOVERY_MODE6_FTOLには0x5D1BB6以降の**前半**（～0x5D1BDD）まで、下流0x5D1BDF..0x5D1C15は未取得と明記。本回の新しい静的証拠はその下流から最終RETまでの原作ネイティブ命令。
- 0x004BEEBE CALL 0x004C1200（検索ヘルパー）。0x004BEEE3で戻ったノードと[EBP+0x80]の番兵を比較、0x004BEEE9 JE 0x004BEEFAでランダムfallbackへ。非番兵では0x004BEEEBで[ECX+0x28]を採用し、乱数抽選をskip。
- 0x004BEF04 CALL 0x005B6EAB、0x004BEF0D/11/17でrand×(1/32768)×count、0x004BEF1B CALL 0x005D1B80、0x004BEF27 MOV EAX,[EDX+EAX*4]。名前解決fallbackに入った後の配列参照で、count=0時の論理範囲外候補は22Hから引継ぎVERIFY。
- 0x005D1B80はGhidra SQLiteのsize_bytes=28だが、0x005D1B87 **JE 0x005D1BB6**で登録関数範囲外の共有tailへ分岐する。SSE側は0x005D1B95 CVTTSD2SI→0x005D1B9B RET。非SSE側の0x005D1BB6..0x005D1C2Aも呼出しの実処理であり、28バイトのGhidra疑似Cだけを完全な制御フローとして扱えない。
- x87側は0x005D1BC5 FISTP QWORD、0x005D1BC9 FILD QWORD、0x005D1BD9 FSUBP ST(1)。0x005D1BDF..0x005D1BFBは負数の残差に応じADCで丸め済値を+1、0x005D1BFD..0x005D1C13は非負数の残差に応じSBBで-1。0x005D1C15..0x005D1C29には低DWORDゼロの特別処理・共通復帰、**RETは0x005D1C2A**。
- これはFISTPのx87制御語に従う一旦丸めた値を、元の実数からの差分符号で切り捨てへ補正する構造。少なくとも正常な小範囲・有限値に関し、通常の4丸めモード（最近接偶数・floor・ceil・toward-zero）いずれも整数部の0方向切捨てと整合する。
- DAT_00B14A40の旧Ghidra索引参照はREAD6件・WRITE0件。0x005D1B9Cの読出しは登録された0x5D1B80の28バイト範囲外にある。SSE gateの実ゲーム時の値や未索引のwriterは不明であり「非SSE確定」とはしない。

## 限定静的監査／合成検証
原作研究用EXE・旧DB・V9をSHA照合、SQLite双方quick_check。Capstoneで候補26命令・分岐と復帰、旧DBからFTOLの28バイト記録/索引CALL・SSEフラグデータ参照、旧64件同期記録を確認し**39/39 PASS**。
合成契約: k=0..32767、個数n=-10,-1,0,1..10、4種丸めを組み合わせ **1,703,936 synthetic cases / FAIL0**。実ゲームの乱数・x87環境・BGM音源を動作させた証拠ではなくGoldenに含めない。負数設定は確保段階で例外になり得るため、負数indexの実行到達を保証しない。

## 正式進捗／安全・未解決
既存Wave1～5 VERIFIED **64/64は2026-10-11同期記録**から継承、今回新規正式VERIFIED0。5種の証拠はinfo/pseudo/callers/callees=INDEX_ONLY、assembly=TARGETED_PE_NATIVE。正式TODO/VERIFY/BLOCKED更新差分0/0/0、原作Golden実測PASS0、strict MATCH・完全複製率未測定。
PC接続成功、23:44時点空きRAM約13.01GiB、23:50時点active.lock無し。CPU負荷不明、今回監査単独4.9～5.2秒、全作業時間未測定。新REA/Ghidra/ゲームの起動なし。Workなし。初回read-only Python stdin経由の日本語パスが文字化けしたためPath.cwd()方式で正常復旧（OTHER、SAFETY_REFUSALではない）。
原本ZIP/EXE/SAVE、MASTER/QUEUE/PROGRESS/既存runs、A～E/T018/dev_lab、Git・公開先・スケジュール未変更。未同期の過去オフライン証拠は今回も未統合。

## 次P0
0x004BE820の呼出元0x004BDE40:0x004BE178と0x004C1200の検索キー構築・番兵条件をさらに絞る。入力が名前不一致となるBGM指定経路とcount=0の到達性、+0x70の別名free候補を優先。次にDAT_00B14A40の初期化条件・未索引の書込みを独立確認。実機Goldenは隔離試験が準備されるまではNOT RUN。

