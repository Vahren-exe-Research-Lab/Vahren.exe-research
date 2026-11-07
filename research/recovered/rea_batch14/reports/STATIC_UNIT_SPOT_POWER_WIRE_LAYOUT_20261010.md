# Unit / Spot / Power 保存ストリームの構造別検証（2026-10-10）

範囲：保存済みGhidra静的疑似コード・アセンブリと既存native dumpのread-only照合。**新EXE・新Ghidra/REA解析実行0、原作ゲームgolden0**。対象EXE SHAは既存RUN_RESULT記録 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
正本MASTER/5レーン規約read-only確認。本研究メモはrea_lab所有範囲。開発の別成果はdev_labにのみ保存。

## S-UNIT-01 Unit固定prefixと4つの28-byte vector間の補助field

一次保存証拠：`runs/20261009T224617297Z/58EFD0_procedure_{pseudo_code,assembly}.json` (writer)、`runs/20261009T223622536Z/58E870_procedure_{pseudo_code,assembly}.json` (reader)、既存native `exe/T014_GROUP_PROBE.txt`。
- writerは string +0,+0x1C → raw dword +0x70 → string +0x38,+0x54 → 7 raw byte +0x74..+0x7A → dword +0x80 → string +0x84 → raw dword +0xC8,+0xCC,+0x174,+0xBC,+0xC0,+0xC4,+0xD0 の順。reader 0x58E8AF..0x58E9F0のhelper呼出/field offsetは同順。数値のゲーム上のsignednessはraw DWORDとして未同定。
- 4つのstring-vectorメモリ(begin,end)は (+0xD4,+0xD8)、(+0xEC,+0xF0)、(+0xFC,+0x100)、(+0x10C,+0x110)。各要素は28byte stride、書込は各要素のstringをNUL終端で出力し、各vector末尾にempty stringを1つ出力。readerにもempty stringで停止する4ループがある。
- **重要**：第1vector終端と第2vector開始の間に、+0xE4 raw dwordと+0xE8 raw byteが入る（writer 0x58F1C0..0x58F1E6、reader最初のvector後）。4vectorを物理的に連続していると仮定すると後続streamを誤読する。
- 第4vector後にUnit+0x130のRB-treeが続く。writerは各entryのkey文字列＋node+0x28のraw dwordをin-order出力し、0x58F405でglobal string object 0x68B9D0を出力。reader 0x58ED55..0x58ED75は同markerと比較し、marker一致時0x58EE5Fで0x58E480を呼ぶ。**0x58E480のGhidra5点検証は未取得**。marker具体bytesも本検証では未同定。
- writer後半にはliteral arbeit、arbeit_user、item_skill、friend、+0x11C/+0x120追加vector、+0x15C追加tree、+0x13C string、+0x168..+0x1A0 dword群がある。`arbeit`後の+0x7C dword、`arbeit_user`後の+0xA0 string、`item_skill`後のvector、`friend`後の別treeを区別する。全Unit解析は未完。
- `dev_lab/unit_runtime_prefix.py`で固定prefix＋4 vector＋E4/E8の合成byte codec、独立テスト5件PASS。原作の実Unit saveファイルを扱えたという意味ではない。

## S-WRITER-02 文字列writer 0x470830：2 pass検査／全体空文字化

- Ghidra保存一次証拠 `runs/20261009T220712454Z/470830_procedure_assembly.json` VA0x47084F..0x470894を照合。
- 0x47084F `CMP byte,0x20; JL 0x47088C`、0x470860 `CMP byte,0x7F; JG 0x47088C`。0x470866..869の全byte検査完了後だけ0x470871..88Aで内容を書き込み、0x47088C..88Fは常にNULを1つ出力。
- よって途中に `<0x20` または `>0x7F` が1byteでもあれば**文字列全体を捨ててNULだけ**を出す。途中まで出して切る処理ではない。0x7Fは境界内で許可（DELであってもこのnative比較では通る）。
- 同writerは保存形式の名前・境界文字列にも適用されるため、想定外control byteや空vector要素はdelimiterと衝突し得る。ただし**原作ゲームで合法に作れるか／実害があるかは未観測**。作者のバグと確定しない。
- `dev_lab/native_stream_strings.py`でwriterのbyte処理を純粋合成実装し、`dev_lab/save_envelope.py`の0x7F過剰拒否を修正。専用テスト4件PASS。

## S-SPOT-03 Spotは可変tree後の固定label境界を使う

- 一次保存native `exe/T014_GROUP_PROBE.txt` Spot writer 0x598CE0、`exe/T014_ENTITY_MARKERS.txt`の文字列literal `0x6264D0..0x6264F8`をread-only照合。
- 固定prefixはstring +0,+0x2C,+0x64 → raw DWORD +0x80,+0x84。続いてRB-tree +0x20の名前をin-orderでwrite。
- tree後には**明示的な空文字delimiterなし**で `capacity` literal（0x598E11）→raw dword +0x88、`castlebattle`→dword +0x8C、`fightvalue`→dword +0x90、`dunname`→string +0x48、最後にempty string marker（0x598FBB）の順。
- `capacity`をtree boundaryにするreader側の詳しい挙動、tree自身の`capacity`キーとの衝突は**Spot reader 0x598980 body未取得につきVERIFY**。`dev_lab/spot_runtime_writer_fragment.py`はwrite order＋synthetic inverseのみ、元EXE読込実装を確認したという意味ではない。独立テスト4件PASS。

## S-POWER-04 Powerには4つのtagged DWORDとhome_spot vector、連続2 empty

- 一次native `exe/T014_GROUP_PROBE.txt` Power writer 0x596AA0、特にVA0x596E0B..0x597091、literal map `exe/T014_ENTITY_MARKERS.txt`でVA0x626ABC..0x626AE8を照合。
- prefixはstring +0、bytes +0x1C/+0x1D、dword +0x5C、strings +0x24/+0x40、dwords +0x20/+0x60、string +0x74。RB-tree +0x68 names/empty終端、28-byte vector +0x90/+0x94 names/empty、RB-tree +0xA4 names/empty、RB-tree +0xB4は**key stringとnode+0x28 raw dword**の対（0x596D74/0x596DAA）として出力。
- 上記treeの後は literal `fixtype` → raw dword +0xD0、`train_max`→ +0xD4、`train_up`→ +0xD8、`base_level`→ +0xDC、`home_spot`→ vector +0xC0/+0xC4 の順。home_spot vectorは28-byte strideで名前を列挙。
- vector終了時に0x597085で空stringを出し、更に0x597091で同writerを再度呼んで**連続する2個のempty string**を出力。これを1つのvector delimiterへ圧縮しない。2番目の終端が具体的にどのスコープを閉じるかはPower reader 0x5964C0本体の更なる解析までVERIFY。
- `dev_lab/power_runtime_writer_tail.py`では後半4 tagged DWORD＋home_spot vector＋empty×2のsynthetic inverseだけを別モデル化し、独立テスト4件PASS。readerそのもののnative5点証拠や実game `.sav`は未取得。

## 合計・残件・安全条件

- Unit保存prefix5テスト、Spot write fragment4テスト、Power write tail4テスト、string writer4テスト、計17件の新規合成テストがPASS（dev_labの以前121件と併せたフル回帰集計は後続実施）。これらは本家TARGET OBSERVED / strict MATCHではない。
- 直接の次回未解決関数：**0x58E480**（Unit marker以降のload）と0x598980（Spot全reader）、0x5964C0（Power全reader）。そのほかUnit中間tagのread、Power2個目delimiter意味、Spot `capacity`の予約名衝突などは**VERIFY**。
- 旧ゲーム実機セーブの提出はユーザーから後回しと指定されたため、提出前提の試験は計画のみ。指示を繰り返さない。手動観測作業は別途まとめて保管する。
- REA重要重点関数のGhidra 5点証拠取得数は **39/48のまま**（Wave4=3/12）。新Ghidra/REAプロセス、実EXE起動、禁止された再解析・別tool迂回なし。QUEUE/PROGRESSのWindows EPERMによる古い状態は変更なし。MASTER/T018、owner A〜E、原本、Remote、Git/push、MCP/automation設定は変更しない。


## 同日・全回帰確認（16時台、静的/合成のみ）

- 研究メモ本体作成後に独立`dev_lab/run_checks.ps1`を通常実行し、Windows process PID24904が終了code0、単体テスト**138/138 PASS**、`DEV_LAB_ALL_CHECKS_PASSED`を確認した。前回121から新規17件で、既存も全件成功。
- Map151・atlas513、context代入204、DAT script590（14,591,845 bytes）、parent graph21,214 refs、event/scenario body sample516、合成1v1/2v2時計・VM・AIの回帰も前回結果と整合。
- 以上の合格は保存済みGhidra静的証拠に基づく**synthetic source-side unit tests**であり、原作旧EXEのTARGET OBSERVED golden PASS0、新engine strict MATCH0を維持。新Ghidraで逆コンパイルした関数増加は0、重点39/48は変わらない。
- 元ZIP/EXE・MASTER・A〜E資料・T018・REA既存queue/runner・Git/push・Remote/OS/MCP・automationは未変更。追加したresearch noteだけを記録した。

