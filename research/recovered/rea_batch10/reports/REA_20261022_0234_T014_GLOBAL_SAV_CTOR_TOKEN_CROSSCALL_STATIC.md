# REA-20261022-0234-T014-GLOBAL-SAV-CTOR-TOKEN-CROSSCALL-STATIC-01
- 記録日: 2026-10-22 02時台 JST。owner=REA独立/T014（REA内部P0、MASTER上P1）。状態=STATIC / VERIFY / NOT READY。旧報告0137の重複記載を除く独立追跡。
- source SHA256（BUILD_MANIFEST由来）: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。原作EXE現物再ハッシュはNOT RUN。
- DB SHA256（現物照合）: 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF。BUILD_MANIFEST一致、SQLite read-only integrity_check=ok、functions 10456（内部10268＋外部188）、検査0.896秒。
- 先読: MASTER、ANALYSIS_LANES_PROTOCOL、REA README/QUEUE/PROGRESS/WAVES、進捗sync 20261011T153958076Z、前回0137報告。古いQUEUE/PROGRESSはEPERM stale扱い。既存run64/64を再加算しない。
## 今回の新規静的差分: global.sav の2つのcaller内にあるコンストラクタ→token reader鎖
| 親関数 | basic_istringstream ctor CALL site | token reader 0x4705F0 CALL site | Ghidra疑似Cで見える入力streamローカル |
|---|---|---|---|
| 0x428010 | 0x4282F4 → 0x429C60 | 0x4283A7、0x428444 | aiStack_24c |
| 0x428710 | 0x428A1F → 0x429C60 | 0x428ADF、0x428B7F | aiStack_26c |
- 両親関数の疑似Cに文字列 `global.sav`、FindFirstFileA/CreateFileA/ReadFile、上記ストリーム生成、複数token読込、終了時のstreambuf/ios破棄が並ぶ。呼出しの前後順序と同じ親関数内の出現はCALL索引＋疑似Cの双方で静的に裏付けられる。
- 親0x428010 code SHA256=FBB4B43CEB8B979ED8A41554C5CC40505AA47D8066296A09E802C0328FC3E369。親0x428710 code SHA256=6513A1B7C947F4A0F76FDAFC21F9F59A90B24CA3163B0226E0FF1E049ABEF878。
- 0x429C60 code SHA256=6882798514D6787EC7429991A5CF2DF76F037760F6B1951D3DD053491426AD56。CALL 0x429D0B→0x42A7A0（0x21）。0x42A7A0 code SHA256=EA6C9787B7D13414C659B7D7A0AEBA972766848610030090AD011DDF025924AD。
- 0x429C60疑似Cには stream内のadjusted iVar3+0x38 に param_1+4（buffer subobject）を格納する箇所がある。0x42A7A0ではbasic_stringbuf vptr候補=0x0063848Cを設定（旧0137根拠の再利用）。
- 0x4705F0 CALL site 0x470611→0x470980（token読込→1byte読込）。0x470980疑似Cはstreamのadjusted field+0x38経由でbuffer pointerを取得し、vptr経由の+0x04/+0x18/+0x1Cを使う。cleanup 0x470AACでは+0x08（旧0137根拠の再利用）。
- 本回の追加意義: 先回の抽象的なconstructor→vtable候補について、**global.savの2つの上位処理から実際のtoken reader呼出しまでの直接CALL経路**を特定。全token reader呼出しが当該vtableを使う、とは主張しない。
## ABIとオブジェクト同一性の限界
- Ghidraでは0x429C60の定義が1引数に見える一方、0x428010/0x428710の疑似Cではそれぞれ2引数相当の呼び出しを復元する。constructorの隠れたthis/引数対応はASM未確認。
- 0x4705F0は疑似Cでunaff_EDIによりstream state参照。一方親0x428010等は token readerを出力文字列バッファらしき引数付きで表現しており、**親ローカルstreamオブジェクトと0x4705F0のEDIが等しいというレジスタ/ABIの実証は未了**。
- 従って、global.sav2つの親関数内にctorとtoken readerが共存し順序付くことはSTATIC、一つの同一オブジェクトを間接CALLまで伝播するとの断定はVERIFY。runtime vptr変更の不在も未証明。
- 前回のpointer_refs 15スロット中先頭1件・残り14件未収録は今回再検査しておらず、実関数VAへの対応はなお未解決。拒否済みCALL_INDEX_V2等の命令取得操作を別経路で行わない。
## 証拠/状態/実行と次回
- 関数別REA正規5証拠 info/pseudo/assembly/callers/callees: 今回4種の新規完全セット0、5種揃い0、Evidence ID新規0、VERIFIED新規0。保存済みGhidra検索出力はREAの正式証拠へ自動昇格させない。
- Wave1～5: 保存済みprogress_sync_20261011T153958076Zで64/64 VERIFIED（旧成果）、Wave6正式登録0件、候補TODO12・安全BLOCKED4・VERIFY0は旧報告値。正式状態差分TODO/VERIFY/BLOCKED=0/0/0。
- Golden: 原作実機PASS0、新旧strict MATCH0、ゲーム完成率未測定。新しい観測設計はglobal.sav既存/不存在・正常2token・途中EOF・壊れたtokenのreader/exception/vptr identity差分。すべてNOT RUN、T018には未統合。
- PC Local接続成功。owner直下active.lockなし、既存Localセッション3件には干渉しない。FreePhysicalMemory=14835600 KiB、CPU負荷不明（OS値null）。新規Ghidra/REA実行0回、解析全体所要時間未計測。
- 安全拒否今回0。原本ZIP/EXE/SAVE、MASTER/A～E/T018/dev_lab、既存REA RUN/QUEUE/PROGRESS、Git/公開先/スケジュール無変更。REA ownerに本ファイルのみ新規保存。
- 次の許可済み解析位置: 0x428010のCALL 0x4282F4→0x4283A7 / 0x428710のCALL 0x428A1F→0x428ADFにおいて隠れたthisの同一性を既存許可済み証拠で検証。その後0x470980の+0x18/+0x1Cの実指先を証拠で限定。
