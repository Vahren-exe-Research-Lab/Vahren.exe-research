# REA-20261021-2236-T014-STATE-MASK10-EPILOGUE-CROSSWALK-STATIC-01
- 日時: 2026-10-21 22:36 JST / owner REA / T014 P0 / STATIC・VERIFY・NOT READY。既存IDを上書きせず独立新規。
- 範囲: 旧EXEを実行せず既存Ghidra12.1.4 SQLite検索DBで条件式・CALL graphをread-only照合。新Ghidra/REA=0、Golden PASS=0、新旧strict MATCH=0、再実装率未測定。
- 出典EXE SHA256（manifest記録）: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。今回EXE現物再hashは未実施。
- 出典検索DB現物 SHA256: 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF、CLI現物 SHA256: DF2E4C9220E6EA564C3955D5BF60628D0F2B04F850CDC0FBFD8F413B412A44B0。BUILD_MANIFEST一致。今回SQLite integrity_check未実施。
- 先読: MASTER、ANALYSIS_LANES_PROTOCOL、decomp_task README/QUEUE/PROGRESS/WAVES、旧T014資料、既存最終RUN_RESULT 20261011T153309850Z、sync 20261011T153958076Z、21:35独立STATIC報告を確認。最新同期W1..5=64/64、QUEUE/PROGRESSはEPERMによる古値、置換せず。
## 新規静的差分A: 状態更新helperのマスクと上位LoadException条件の非同値
- `0x426E00`（code SHA 7BEBA43A38A9E3880B88EFBA64A11D7CE7087E53C03C0BCF4B846B3C828B1A43）疑似Cは、入力レジスタ値Sを `S & 0x17` にマスクし、ストリーム内のstate候補 `[param_1+0xC]` に代入。例外マスク候補 `[param_1+0x10]` との交差が非0ならthrow経路。**Sの供給元と旧状態のOR有無はABI未解明**。
- `0x470700`（code SHA 873CD6F6F7A5DF2EDE7A631557223DEDB71B3AEA7262FADE79ACA0A9AD86D6C8）、CALL site `0x470713 → 0x42E700` は正常return後に `(observed_state & 7)!=0` で `LoadException`。上位は0x10ビットを条件に含めない。
- すなわちhelper `0x17` と上位 `0x07` の差はビット4（0x10）。数式レベルでは`0x10`単独は上位判定で無視され、helper例外マスクが0x10を許せばthrowの候補。到達可能なstate/exception mask値かは未確定。
- `0x426E00`内のthrow優先度は `(masked & 4)`→badbit、次に`(masked & 2)`→failbit、残りのマスク交差は`eofbit set`文字列。従ってmasked=0x10だけでも最後のメッセージ候補へ落ちる。ただし通常許容マスク範囲と実call register値が不明であり原作実到達・バグの証拠ではない。
- 合成クロスチェックは仮定 `S=helper入力、例外フラグ引数=0、helper正常return後に上位が同じstream stateを読む` の場合に限定。S,M=0..31の1024組を分類: 事前helper throw条件700組、helper return後上位LoadException条件228組、両条件通過96組。**前回16時台の状態式テストと入力空間が重なるため、新規VERIFIEDや新規Golden件数に加算しない**。
- 代表組: S=1,M=0→上位LoadException候補、S=1,M=1→helper throw候補、S=0x10,M=0→両判定通過候補、S=0x10,M=0x10→helperの残余`eofbit set`候補、S=8,M=31→S&0x17=0で両判定通過候補。
## 新規静的差分B: cleanup間のfailbit組み立てを同一視できない
- P0 `0x42E7D4`（code SHA 5810D08FCC35B9C755402E352BCCD84543832127EF573EFB4A9CB259700D3C1C）は親`EBP-0x14 !=0`でsite `0x42E7F2 → 0x426E00`をCALLするが、疑似C内に明示`|2`がない。親frameへの書込起源・渡すEAXは未復元。
- 比較 `0x43A4ED`（code SHA E35CFF4E28E894B80AEF51FF5D0776C7581A6D7E6A1A8509EF29E209663638B0、site `0x43A514`）は親frameのbyte `EBP-0x11==0`で `uVar2 |= 2` とした後、非ゼロ時に同helperをCALL。
- 比較 `0x558E68`（code SHA B605B03D944834CCC9BC96B0E662CE671F554AD4007F1BBAFDDB54E0A40354A2、site `0x558E92`）はgcount候補 `[EDI+8/+0xC]` が両方0なら `uVar2 |= 2`。この`|2`が見えない0x42E7D4へコピーして『短読込は必ずfailbit』と決めつけない。
- 共通helperのcallerはGhidra直接CALLで確認済み。`0x42E7D4`への親site `0x42E7A2`、`0x42ECF0`へのsite `0x42E77F`、仮想CALL `0x42ED07(+0x20)`も保存索引と一致。ただしvirtual実体/ABI/正常returnはVERIFY。
## 証拠充足/進捗/Golden
- 今回の関数別REA正式5種（info/pseudo/assembly/callers/callees）完全セット新規0、Evidence ID新規0、VERIFIED新規0。Ghidra機械疑似CとCALL索引のみ確認、対象4関数の新ASM証拠0。
- W1..W5既存sync値64/64（各16+10+10+12+16）、Wave6以前の記録上TODO12/SAFETY_BLOCKED4/VERIFY0、今回の正式TODO/VERIFY/BLOCKED増減0/0/0。最新W6実行を意味しない。
- Golden条件DESIGNED_NOT_RUN: 入力4byte/3byte/0byte、state 0/1/2/4/0x10、exception mask 0/1/2/4/0x10。上位LoadException/下層ios_base::failure/gcount/出力代入順序を区別。無効マスクの場合は仕様テスト候補に限定。
## 保全と次の再開位置
- PC接続成功、開始時既存Local対話セッション2件（中断・変更なし）、decomp_task/active.lock不在、CPU LoadPercentage 7%、空き物理RAM約15.6GiB。負荷実測は簡易スナップショット、解析実行時間0秒、作業全時間未計測。
- 安全拒否済み `0x429620` CLI、CALL_INDEX_V2命令照合、owner既存ファイル追記、Wave6拒否VA・REAエクスポート等を再試行/別経路で回避せず。新規拒否・接続障害なし。
- 原本ZIP/EXE/SAVE・A～E/MASTER/T018/dev_lab/既存runs/QUEUE/PROGRESS/Git/公開先/スケジュール変更なし。REA所有フォルダに新規メモ1件のみ、後続の同名修正/追記を行わない。
- NEXT T014: 許可済み既存ASMの存在を照合し、0x42E7D4 の EBP-0x14 と直前 EAX、0x42ECF0 return EDX:EAX、上位state検査実体を別々に確定。S=0x10経路の実行可能性は仮説で保留。
- 保存はファイル作成後の独立readback/ハッシュ確認が完了するまで未確認扱い。現時点ではREA正式VERIFIEDでもMASTER同期でもない。
