# REA-20261022-0535-T014-CATCH-RETHROW-MASK-CONTRAST-STATIC-01
- 日時: 2026-10-22 05時台 JST。owner=REA独立、対象=T014、独立優先P0。状態=STATIC / VERIFY / NOT READY。既存0443報告・旧VERIFIEDを二重計上しない。
- 解析元EXE記録SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（現物EXE未再hash）。Ghidra12.1.4既存索引のみ、原EXE/ゲーム未実行。
- PC=Local接続成功。先読=MASTER_LEDGER、ANALYSIS_LANES_PROTOCOL、REA README/QUEUE/PROGRESS/WAVES、最新progress_sync_20261011T153958076Z（64/64）、旧REA run、0443/0337/0137報告。旧QUEUE/PROGRESSはEPERMでstaleのため集計正本にしない。
- DB現物SHA256=0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF、CLI=DF2E4C9220E6EA564C3955D5BF60628D0F2B04F850CDC0FBFD8F413B412A44B0（各BUILD_MANIFEST一致）。ro+immutable SQLite integrity_check=ok、10456関数。
- 既存実ASM=exe/T014_READER_CHAR_PROBE.txt、現物SHA256=B42A217769E1E6EC3E770308665A6EA79E0F2BD31431D0710E664DA157E0EDAD（再取得ではない）。
- 保存済み擬似CコードSHA: 0x470A78=43CF83D92FE754DFBA87E9F086D535174B8FEFAA0E967688E96DC150683CA79C、0x470AAC=EDCF4BF40F09829251103D9A908D61652A194200D5FD66595F69E4035DF9094D、0x426E00=7BEBA43A38A9E3880B88EFBA64A11D7CE7087E53C03C0BCF4B846B3C828B1A43。
## 新規差分：catch時の再送出と通常EOF時の新例外は別経路
- catch入口0x470A78の保存実ASM: 0x470A82 MOV EAX,[ECX+0xC]→0x470A85 OR EAX,4、0x470A88 CMP [ECX+0x38],0、0x470A8E OR EAX,4（重複）、0x470A91 PUSH 1→0x470A93 CALL 0x426E00。元のstateにbadbit=4を必ずORして更新関数へ渡す。
- 0x426E00の既存Ghidra疑似C（新REA VERIFIEDではない）: field state=[incoming EAX]&0x17、交差=exception_mask & incoming EAX &0x17。交差0ならreturn、交差非0かつ第2引数!=0なら__CxxThrowException_8(0,0)を呼ぶ。これは既存例外再送出の候補であり、ASMによるcallee内部の確証は今後VERIFY。
- catchは第2引数1なので、badbitを含む新状態とexception maskが交差すればrethrow候補、交差しなければ正常return。続いて0x470A98で[EBP-4]=1、0x470A9Fで継続0x470AA5を返す。0x470AA5はEDI復元・EBX/ESI=0化を経て0x470AACの共通cleanupへ合流する。
- 前回0443の通常EOF経路（sentry成功→virtual +0x18 が EAX=-1）: 0x470A25 LEA ESI,[EAX+4] => ESI=3、0x470AB7..0x470AC5で oldstate|3（buffer==nullなら更に|4）を作り、PUSH 0で0x426E00。exception_maskが交差すると、badbit > failbit > eofbit相当のメッセージで新ios_base::failureを構築する候補。catchのPUSH1/rethrowとは異なる。
- 重要な関数関係: 0x470A93→0x426E00（catch）、0x470AC5→0x426E00（normal cleanup）、0x470AE3=未解決computed CALL vtable+0x08。0x470A78はGhidra Catch_All・size45、0x470AA5が関数範囲直後に位置するが、前回既知の境界規則なので新規として重複計上しない。
## 合成状態・maskモデル（実ゲームではNOT RUN）
- unsigned state=0..31、exception_mask=0..31の1024組ずつを独立演算で再計算。catch: new=(state|4)&0x17、交差非0=808、交差0=216。normalEOFかつbufferあり: new=(state|3)&0x17、新例外候補=880（bad256/fail384/eof系240）、交差0=144。buffer無し: new=(state|7)&0x17、新例外候補=928（bad512/fail256/eof系160）、交差0=96。
- state=0を例にするとmask1ではcatchはrethrowせず通常EOFはeofbit系failure、mask2ではcatchはrethrowせず通常EOFはfailbit failure、mask4ではcatchはrethrow候補で通常EOF（bufferあり）は交差0。これらは旧類似論理検証の重複を含む新たな条件分類で、Golden PASSや新規関数数には加算しない。
- ただし0x470AE3の仮想CALLがstateへ与える副作用、0x470ACA以降の実ASM/RET4/最終EAX、MSVC再送出呼出しの命令証拠は未確定。catch非rethrow後に上位0x4705F0で最終的にLoadExceptionになるかはVERIFY。安全拒否済みCALL_INDEX_V2/0x429620/Wave6/REAエクスポートを再試行・迂回しない。
## 保存状況・正式進捗・次回位置
- 実ASM後半探索: exe配下既存*.txtの文字列00470ACAをread-only検索し一致0件。これは探索対象内の未発見であり、バイナリ上に存在しない証明ではない。新Ghidra抽出は実施せず、後半ABI=VERIFY維持。
- REA正式5種(info/pseudo/assembly/callers/callees)新規完全充足0関数・新規Evidence ID0・新規VERIFIED0。既存Wave1～5=64/64、Wave6正式0/16、旧候補TODO12/BLOCKED4/VERIFY0（最新状態を新規確認した値ではない）、正式差分0/0/0。
- 旧EXE実ゲームGolden PASS0、strict MATCH0、完全複製率未計測。Golden設計=catch時の元state0/0x10、mask0/1/2/4/0x10、通常EOFのbuffer有無を分け、例外型・state・EAX・gcountと上位LoadExceptionを比較（すべてNOT RUN）。
- 実行: 新規Ghidra/REA起動0、解析実行0秒。Local active.lock不在・Java/Ghidra稼働なし、Local既存セッション6件は不干渉、FreePhysicalMemory=14564380KiB（約13.9GiB）、CPU使用率不明、調査総所要時間未計測。新たな安全拒否0件。
- 保存先は本REA ownerの新規Markdownのみ。MASTER/QUEUE/PROGRESS/他A～E/T018/dev_lab/原本ZIP/EXE/SAVE/既存RUN/Git/スケジュールへ変更なし。保存後の独立readback・SHA検査は別途実施。
- 次のP0: 0x470AE3のvtable+0x08仮想calleeの既存許可済み証拠を照合し、stateを書き換える可能性を評価。0x470ACA以降の実ASMが正規保存済み資料にない場合はABI推測をVERIFIEDへ昇格させない。既存同ID/owner競合確認後の正本統合のみ許す。