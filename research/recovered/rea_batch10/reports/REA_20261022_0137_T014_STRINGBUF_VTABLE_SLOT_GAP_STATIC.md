# REA-20261022-0137-T014-STRINGBUF-VTABLE-SLOT-GAP-STATIC-01
- Owner: REA独立 / T014 (REA内P0、MASTERではP1) / 2026-10-22 01時台 JST。状態 STATIC / VERIFY / NOT READY。既存成果非上書き。
- 元EXE source SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（BUILD_MANIFESTと旧REA run記録。今回現物は再hashしていない）。
- DB `search.sqlite`現物SHA256=0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF、manifest一致、PRAGMA integrity_check=ok。既存search.py/read-only SQLiteのみ、新規Ghidra/REA0回。
- 先読: MASTER、規約、README/QUEUE/PROGRESS/WAVES、RUN_RESULTと最新progress_sync、T014 255-byte/00:47/23:39ほか既存資料。既知EOF・255・状態分岐は今回新規として数えない。
## 今回の独立静的差分：input stream生成から実vtableスロットアドレスへ
- Ghidra関数0x429C60 (code SHA256 6882798514D6787EC7429991A5CF2DF76F037760F6B1951D3DD053491426AD56) はbasic_istringstreamを組み立て、ストリームのbuffer pointer `[adjusted iVar3+0x38]` に `param_1+4` を格納。CALL 0x429D0B→0x42A7A0(param_1+4,0x21)。
- 0x42A7A0 (code SHA256 EA6C9787B7D13414C659B7D7A0AEBA972766848610030090AD011DDF025924AD) はそのsubobjectの先頭vptrを `std::basic_stringbuf<...>::vftable` = 0x0063848C に設定。Ghidra DATA site 0x42A7D8、型hint `pointer[15]`。
- 同0x42A7A0の内部flag変換を固定引数0x21へ代入すると uVar2=2、param_1[0x10]=2。入力モードflagの物理的意味・後続の変更は未確定。
- 0x470980 (code SHA256 850A2D2AFD2929E4228F1232AACC50394ECCE9C289CFA3D7834824FA96D8A446) はadjusted stream field +0x38からbufferを引き、buffer vptr経由でCALL。上記constructorで作られた同一bufferが変更されていなければ、vptrの静的基準位置は0x0063848C。
| computed CALL site | buffer vtable相対offset | 仮定成立時のslot VA |
|---|---:|---|
| 0x4709D0 | +0x04 | 0x00638490 |
| 0x470A1B | +0x18 | 0x006384A4 |
| 0x470A66 | +0x1C | 0x006384A8 |
| 0x470AE3 (0x470AAC cleanup) | +0x08 | 0x00638494 |
- Ghidra computed CALL indexは0x4709D0/EAX、0x470A1B/EAX、0x470A66/EDX、0x470AE3/EAX。site→slotはconstructorを前提とする条件付き追跡で、site→calleeの絶対関数VA解決ではない。
## 索引カバレッジの未解決点
- SQLite `pointer_refs` read-onlyで0x0063848C..0x006384C4の15個の4-byte slotを個別照合：recordありは先頭0x0063848C→0x0042A460の1件、残り14 slotには該当record無し。問題の+0x04/+0x08/+0x18/+0x1Cは全て索引未収録。
- pointer[15]という型hintは各slotが非0・有効関数ptrであることの証明ではない。欠落は未型付け・零埋め・抽出器のarray展開不足等でも起こり得る。読込時vptr上書き、実際のoffset構成、各calleeのASM/ABIは未検証。欠落行を架空のCALLとして補わない。
- この監査は旧CALL_INDEX_V2の拒否済み命令取得、拒否済みWave6、REA exportの再試行ではない。SQLiteの既存許可済みpointer_refsと機械疑似Cだけを照合。
## 成果区分・優先再開
- `0x4705F0`の既存REA 5種VERIFIED（既存asm ev_119a86f44bb44e174c04ae524788b577d2b4085fbdba2dbac424cf906663f94d）は再利用のみ。0x429C60/0x42A7A0/0x470980/0x470AACの今回新規のREA info/pseudo/assembly/callers/callees完全充足0、Evidence ID新規0、VERIFIED新規0。
- 旧W1..5 64/64（progress_sync_20261011T153958076Zで確認）、Wave6正式追加0/16、候補TODO12・安全BLOCKED4（旧報告）、正式TODO/VERIFY/BLOCKED差分0/0/0。QUEUE/PROGRESSのEPERM staleは無変更。
- Golden: 旧EXE実機PASS0、新旧strict MATCH0、実再現率未測定。次回は保存済みの許可済みvtable/listing証拠が既存runsにあるか照合し、stream constructorから0x4705F0 callerまで同一object identityを確認。+0x18/+0x1C targetはその後も独立証拠が必要。GoldenはNOT RUN。
- 接続Local成功、owner/decomp_task直下active.lock不在、他Localセッション3件には干渉無し。CPU簡易値53%、free physical RAM 13449360KiB、Java/Ghidra実行0。今回の軽量解析経過時間未計測、REA/Ghidra実行0秒。
- 変更範囲: REA owner内のこの独立新規文書だけ。原本ZIP/EXE/SAVE・MASTER/A〜E/T018/dev_lab・旧runs/evidence・QUEUE/PROGRESS・Git/公開先・スケジュール不変更。保存readback前は未確認扱い。
