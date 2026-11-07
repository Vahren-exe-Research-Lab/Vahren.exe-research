# REA-20261022-0843-T014-BYTE-WIRE4-PAIR-STATIC-01
- JST 2026-10-22 08時台 / owner=REA独立 / P0=T014 / STATIC・VERIFY・NOT READY。既存REA_20261021_2035、20261022_0737、WAVE5監査と差分照合済み。新規は対称な1byte field⇄4byte転送の親子横断実ASM照合。
- source EXE SHA（既存manifest/RUN_RESULT、現物EXE再計算なし）: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
- Desktop Commander Local接続成功。MASTER、ANALYSIS_LANES_PROTOCOL、REA README/QUEUE/PROGRESS/WAVES、既存runs/RUN_RESULT・最新sync_20261011T153958076Z、旧REA記録を先読。QUEUE/PROGRESSは既往EPERMのstaleのため変更しない。
- 検索現物: search.sqlite SHA 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF、search.py SHA DF2E4C9220E6EA564C3955D5BF60628D0F2B04F850CDC0FBFD8F413B412A44B0。BUILD_MANIFESTと一致。SQLite read-only immutable integrity_check=ok。
## 今回の新規STATIC：ローダーとライターの1byte/4byte非対称な保存幅
- 既存実ASM `exe/T014_RECORD_CODEC_PROBE.txt` SHA256 B8919E34D260739BC00488D0DCBF3B10D3F98F84BD4FD10C34D18C57C0221CCE。
- `0x4707D0`: 0x4707D3 PUSH 0、0x4707D5 PUSH 4、0x4707D7 PUSH 0x00B060E8、0x4707DC PUSH ESI、0x4707DD CALL 0x42E700。固定長4byteを一時領域へ読み込む。成功状態の場合のみ0x47081E MOV DL,BYTE [0x00B060E8]、0x470824 MOV EAX,[ESP+0x14]、0x470828 MOV BYTE [EAX],DL。出力先への1byte storeは実ASM確認。
- 同0x4707D0の状態判定は0x4707EB..0x4707FC。下位state &7異常なら0x470802/0x470819 LoadException経路へ進み、0x47081Eコピー処理を経由しない（それ以前の内部例外可能性は別）。
- `0x4708A0`: 0x4708B1 MOVZX EAX,AL（元byteを0..255へゼロ拡張）、0x4708B6 MOV DWORD [ESP+0x14],EAX、その格納位置を0x4708AD LEA ECX,[ESP+0xC]で事前取得。0x4708A9 PUSH 0、0x4708AB PUSH 4、0x4708B4 PUSH ECX、0x4708B5 PUSH EDX、0x4708BA CALL 0x4628F0。byte値をzero-extended DWORDの一時4byte領域として出力関数へ渡す。実ファイル書込副作用は未実機。
- 旧WAVE5は0x4708A0と0x4707D0の個別CALL存在を既知としたが、同一型の4byte wire→1byte fieldの入出力対称性をこの回に新規横断照合。古い結果を新規関数として加算しない。
## 上位構造体での同じ2フィールドを照合
- 実ASM `exe/T014_GROUP_PROBE.txt` SHA256 0D2323A789F6ED9A3472879169AEC5547B5801F54565D46586A195A1237BA611。
- 書込親0x596AA0: 0x596ADE MOV AL,BYTE [EBP+0x1C] →0x596AE3 CALL 0x4708A0、0x596AE8 MOV AL,BYTE [EBP+0x1D] →0x596AED CALL 0x4708A0。よって隣接1byteメンバーを2度呼出し、正常時4byte transferを2回指示する（合計8byteの対象部分）。次に0x596AF2 DWORD [EBP+0x5C]を取得。
- 読込親0x5964C0: 既存Ghidra擬似Cでは0x59650D CALL 0x4707D0に `param_1+0x1C`、0x59651D CALL 0x4707D0に `param_1+0x1D` を渡し、次の0x596529 CALL 0x470700には `param_1+0x5C` を渡す。後者のABI・ESI等の引数モデルはGhidra機械復元なので完全確定ではないが、親の対称関数順序は直接CALL索引と一致。
- Ghidra codeSHA: 0x4707D0=A6F57840EB564D48C00D8757E6CE0CDEB98DE66016C5C5C327BC6E429DF3A45B、0x4708A0=4A51D26D7141B63406F7EDEF0FE7A04E5B34AE4DC8BD7905C3A2FDDDE08ADD43。
- Ghidra codeSHA: 0x5964C0=A3A43FB167F7CEDE8A2E9AB94D364F8B62CC2F13A62294BDB3BA1868C7C5F41A、0x596AA0=AC59C5508CEA1686A98F84FF9D72F58F7C476D70CB6479E5DCD5A189B3858D11。
- Ghidra検索の直接CALL: reader 0x59650D/0x59651D→0x4707D0、0x596529→0x470700、writer 0x596AE3/0x596AED→0x4708A0、0x4708BA→0x4628F0、reader 0x4707DD→0x42E700。
## 合成比較（原作Goldenではない）
- x86 little-endian DWORDのzero-extended byteを模型化。0..255の256候補は writer4byte→reader低1byte の値一致256/256。ただしこれはPython structによる静的条件モデルでありEXE/save実観測ではない。
- 非正規4byte例 `00 01 00 00`→byte0、`FF 00 00 01`→byte255、`78 56 34 12`→byte120という低byte投影候補（上位3byte非ゼロをreaderが検査する直接命令は今回の0x4707D0本体では見当たらない）。読込前段や後段の検証有無はVERIFY。
- Golden設計 NOT RUN: 2つの隣接byteフィールドを0/1, 0x7F/0x80, 0xFF/0x00に設定し、保存片の期待8byte領域・次フィールド位置+0x5C・state/LoadExceptionを観測。さらに上位3byte非ゼロ入力で受理/拒否を分離。保存全体のglobal layoutを本段階で確定しない。
## 判定・未解決・次回
- 重点P0は0x4707D0/0x4708A0で実ASM局所処理を確認。0x4628F0の実バッファへのwrite到達性、0x42E700の実取得数とEOF/exception、親0x5964C0の正確な引数ABI、actual wire file bytesはVERIFY。インターフェイスを推測で厳密フック型にしない。
- 0x42ECF0の0x42ED07 indirect CALL +0x20、EDX:EAXの64bit戻り値は依然未解決。0x470AE3 +0x08の実calleeと副作用も旧VERIFY。今回ここを解決済みとはしない。
- 検索済み機械pseudoはREA info/pseudo/assembly/callers/callees各method evidenceを自動付与しない。今回新規5種完全充足0、REA Evidence ID0、新VERIFIED0。既存Wave1–5 64/64維持、Wave6正式0/16・旧候補TODO12/VERIFY0/安全BLOCKED4、正式差分0/0/0。
- 実機旧EXE Golden PASS=0、新旧strict MATCH=0、完成複製率=未測定。新Ghidra/REA実行=0、CPU瞬時LoadPercentage=0（サンプル値で持続率ではない）、freeRAM=13.26GiB、全調査時間未計測。
- active.lock無し。新たな安全拒否無し。既拒否Wave6/0x5710C0..0x571500/REA exporter/旧0x42E7A2命令bytes確認を迂回せず、原本・A～E/MASTER/T018/dev_lab/既存RUN/QUEUE/PROGRESS/Git/スケジュールは変更なし。
- 次P0: 0x5964C0の2つのbyte格納先callsiteの既存ASM照合で引数ABIを確定、writer 0x596AA0のentry objectとreader 0x5964C0同型接続、4byteワイヤ値上位3byteの検証有無を親/下層から検査。必要なら0x4708A0→0x4628F0のwrite pathを既存DBのみ追う。
- 同期: 本Markdown新規単独追加。PC所有成果はまだE/MASTER正本へ正式統合していない。保存後にreadback+SHA256を独立確認し、未保存なら未保存明記。
