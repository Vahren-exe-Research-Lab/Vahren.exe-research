# REA-20261022-0443-T014-CHAR-EOF-ESI3-STATE-BRIDGE-STATIC-01
- 日時: 2026-10-22 04時台 JST。REA独立担当 / T014（REA優先P0）。STATIC / VERIFY / NOT READY。既存成果の再取得・二重計上無し。
- 解析元EXE記録SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。現物EXEの再ハッシュは未実施。
- 検索DB現物SHA256: 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF（BUILD_MANIFEST一致）。検索CLI現物SHA256: DF2E4C9220E6EA564C3955D5BF60628D0F2B04F850CDC0FBFD8F413B412A44B0。SQLite read-only immutable integrity_check=ok、functions=10456。
- 既存資料先読: MASTER_LEDGER、ANALYSIS_LANES_PROTOCOL、REA README/QUEUE/PROGRESS/WAVES、既存runと最新progress_sync_20261011T153958076Z、前回0337と既存0047/2339/0137報告。0x4705F0既存RUN_RESULT=20261011T144115307Z、5種の保存済み証拠の存在確認（新規計上禁止）。
- 実アセンブリ原資料（既存・read-only）: exe/T014_READER_CHAR_PROBE.txt SHA256=B42A217769E1E6EC3E770308665A6EA79E0F2BD31431D0710E664DA157E0EDAD。exe/T014_RECORD_CODEC_PROBE.txt SHA256=B8919E34D260739BC00488D0DCBF3B10D3F98F84BD4FD10C34D18C57C0221CCE。新たなGhidra/REAエクスポートは実施しない。
- 保存済みGhidra12.1.4機械疑似C: 0x470980 code_SHA=850A2D2AFD2929E4228F1232AACC50394ECCE9C289CFA3D7834824FA96D8A446、0x470AAC=EDCF4BF40F09829251103D9A908D61652A194200D5FD66595F69E4035DF9094D、0x426E00=7BEBA43A38A9E3880B88EFBA64A11D7CE7087E53C03C0BCF4B846B3C828B1A43。これらはREA5種証拠の新規取得には該当しない。
## 新たに結び付けたP0静的結論：1-byte readerのEOF=−1でESI=3、stateへeofbit|failbit
- 原資料ASM: 0x4709AE XOR EBX,EBX、0x4709BF XOR ESI,ESI、0x4709C1 MOV [EBP-0x14],EBX。0x4709D5 CALL 0x42EC60（読込sentry）。
- sentry=0の別枝: 0x4709E8 MOV [EBP-0x14],0xFFFFFFFF、0x4709EF JMP 0x470AAC。ESIは0のままなので、cleanupで新しいbitのORを行わない（先に立っていたstream state等は別検証）。
- sentry成功後の1-byte候補取得: 0x470A1B CALL EAX（vtable+0x18候補）または0x470A11 MOVZX EAX, BYTE PTR [EAX]（buffer）。0x470A1D MOV [EBP-0x14],EAXで取得値を退避。
- **決め手:** 0x470A20 CMP EAX,-1、0x470A23 JNE 0x470A31。EAX=-1のとき0x470A25 LEA ESI,[EAX+4] -> 32-bit ESI=3、0x470A2F JMP 0x470AAC。ここでの3は別の「取得長」ではなくcleanupの状態bitマスク候補。
- cleanupの既存ASM: 0x470AAC MOV EDX,[EDI]、0x470AAE MOV ECX,[EDX+4]、0x470AB1 ADD ECX,EDI、0x470AB3 CMP ESI,EBX(=0)、0x470AB5 JE 0x470ACA、0x470AB7 MOV EAX,[ECX+0xC]、0x470ABA OR EAX,ESI、0x470ABC CMP [ECX+0x38],EBX、0x470AC1 OR EAX,4（buffer参照0の場合）、0x470AC4 PUSH EBX(=0)、0x470AC5 CALL 0x426E00。
- よって**「sentry成功後に仮想1byte取得でEAX=-1を返した通常cleanup」**の局所条件下では、下層0x426E00へ渡すEAX=(元state|3|[buffer==0 ?4:0])。0x426E00疑似Cはstateフィールドへ EAX&0x17 を格納し、例外マスク交差を判定する。元stateに何があっても下位2bit=1/2が立つので、正常帰還できればcallerの(state&7)!=0に必ず該当する。
- この結果、旧0047報告の「EAX=-1、post-call state&7=0ならprefixを正常返却しうる」は論理的な条件分岐として残るが、今回追跡した**成功sentry→EOF(-1)→cleanup**経路からは、他の後続state再書込が無い限り**到達しない**。実際のstreambufがどの条件で-1を返すかと動的観測は未確定。
## 正常文字・ABI・例外優先順位
- 正常byte: 0x470A20のEAX!=-1経路ではESI=0を維持。0x470A48..0x470A55または0x470A61..0x470A6Cでbuffer消費しgcount低32+1/carry高32+1、cleanupの0x470AB3は等値で0x426E00状態更新を飛ばす。この正常経路の「更新無し」は新規状態仕様として独立したものではなく今回のEOF対照。
- 0x470A61..0x470A66のvtable+0x1C呼出しでEAXが変わっても、0x470A1Dで既に[EBP-0x14]へ退避している。最終返値候補は取得時EAXであり消費時のvcall返値ではない。ただし実際の出口のMOV EAX,[EBP-0x14]とRETの命令は保存ASMの切出しが0x470AC5で終わるため未観測、Ghidra疑似Cとの照合によるVERIFY。
- 入力の部分ABI: caller 0x470610 PUSH EDI / 0x470611 CALL 0x470980、callee 0x4709AB MOV EDI,[EBP+8]を保存ASMで確認。最低1スタック引数は確実。callerにADD ESP,4が見えないためcallee-cleanup RET4の可能性が高いが末尾RETはASM原資料範囲外、ABI正式確定扱いにはしない。
- 0x426E00の保存疑似Cでは新stateと例外maskの交差が非ゼロならios_base::failureをthrowしうる。throwされなければcaller 0x4705F0は0x470616でEAX=-1を判定後、0x470621..0x47063Bでstate&7異常を優先しLoadExceptionへ。sentry失敗、間接関数が他の挙動をするケース、例外ハンドラ経路は別VERIFY。
- 本件は**既存exe/T014_READER_CHAR_PROBE.txtに含まれていた実ASMからの新たな横断推論**であり、既存A資料の新規取得や新REA機械出力とは呼ばない。旧報告の条件付きEOF正常終了モデルを否定しすぎず、該当経路を絞った反証として扱う。
## 進捗・実機・所有権・再開位置
- 情報の出典VA/CALL: 0x470611→0x470980、0x4709D5→0x42EC60、0x470A1B computed vtable+0x18、0x470A2F→0x470AAC（GhidraはCALLと登録、実ASMはJMP）、0x470AC5→0x426E00。**索引CALL分類とASMに不一致を発見**：0x470A2FはGhidra isCall=直接CALL記録だが実ASMではJMP。現行検索DBの呼出種別を blindly 信用せず、その他3箇所の0x470AAC参照も実ASMでJMPを確認（0x4709EF/0x470A5F/0x470A76）。分類問題は検索基盤ownerへ情報共有候補、当担当から索引を編集しない。
- info/pseudo/assembly/callers/calleesのREA5種について0x4705F0の既存VERIFIEDは再利用のみ。0x470980・0x470AAC・0x426E00新規5種完全充足0、Evidence ID新規0、今回REA VERIFIED新規0。Wave1～5の64/64は保存済syncの既存数値、Wave6正式0/16、旧候補TODO12/BLOCKED4/VERIFY0は旧報告値、正式差分0/0/0。
- 実ゲームGolden PASS0 / strict MATCH0 / 完全複製率未計測。Golden条件（DESIGNED/NOT RUN）: mask0・mask1・mask2・mask3下で 1byte正常→EOF、空stream開始EOF、buffer欠損、sentry初期state非0を個別に観測し、EAX/ESI/gcount/state/例外型を比較。原作実ゲーム/保存ファイルは今回は実行・変更していない。
- 解析実行: Desktop Commander Local接続成功、owner直下active.lock無し、既存3Local session不干渉、Java/Ghidraプロセス新規起動0、FreePhysicalMemory=15741544KiB（約15.0GiB）、CPU負荷不明、全所要時間未計測。Ghidra/REA新規実行0秒、新規安全拒否0件。
- 未解決: 0x470AAC 末尾の実ASM/RET4/戻値EAX、0x470980から0x470AACへの非例外全path、virtual+0x18で実際にEOF=-1になる条件、0x426E00の実ABI、xrefs機械CALL分類の誤りの範囲。拒否済みCALL_INDEX_V2/0x429620/Wave6/REA exportを迂回・再試行しない。
- 次のREA P0: 保存済み許可ASMにある0x470ACA以降の正規末尾が既に独立保管されていないかだけ確認。見つからなければreturn ABIはVERIFYを維持。続いて直接CALL索引がJMPを誤分類するケースを許可範囲内の既存データと照合し、分類誤差を他ownerへHANDOFF候補として提示（他ownerファイル編集禁止）。
- 書込は本REA owner新規Markdownのみ。MASTER、A～E、原本ZIP/EXE/SAVE、T018、dev_lab、既存runs/QUEUE/PROGRESS、Git/公開先、スケジュールは変更しない。保存と独立readback/SHAを実施し、失敗があれば未保存として別途復旧報告。
- 注意（分類上の補正）: Ghidraが0x470AAC宛edgeをUNCONDITIONAL_CALLと付すのは、物理opcodeがCALLでなくJMPでも**tail-call等の関数間フロー**として分類した結果の可能性がある。したがって現段階で索引生成の「不具合」とは断定せず、ASM opcodeと機械call-edgeの意味論の差としてVERIFYに置く。再実装・フックで戻りアドレス/スタック効果を決める際は実ASMのJMPを一次根拠とする。
- 到達性の厳密な限定（上記結論の補正）: 「正常帰還できればcallerで必ずstate&7非ゼロ」という表現はcleanup末尾の仮想CALL+0x08がstream状態を変更しないことを暗黙に仮定していた。**直接証明できたのは0x470AC5→0x426E00へ渡す入力に0x03が必ず含まれること、および0x426E00の正常帰還直後にstate&3が立つことまで**。0x470AE3仮想CALLの副作用とepilogueを独立確認するまでは最終caller到達時のstate&7はVERIFYのままとする。今回の重要成果は「EOF枝でflag3を組み立て状態更新するコードが存在すること」の確証。
