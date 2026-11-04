# REA-20261022-0737-T014-STREAMBUF-VIRTUAL-SEMANTICS-ABI-STATIC-01
- 2026-10-22 07時台JST / owner=REA独立 / 重点T014（REA内P0） / 状態=STATIC・VERIFY・NOT READY。旧20261022-0638/0535/0443/0137と差分照合、既存成果の二重計上なし。
- 元EXEは現物再hashせず、既存manifestとRUN_RESULTのsource_SHA=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187を使用。原EXE・ゲーム未実行。
- Local接続成功。MASTER、ANALYSIS_LANES_PROTOCOL、REA README/QUEUE/PROGRESS、最新sync（20261011T153958076Z）、旧RUN_RESULT、前回0638/関連STATICを先読。QUEUE/PROGRESSはrename EPERMによるstaleで、既存Wave1–5の正式値はsync 64/64。
- 現物search.sqlite SHA256=0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF、search.py SHA256=DF2E4C9220E6EA564C3955D5BF60628D0F2B04F850CDC0FBFD8F413B412A44B0、いずれもBUILD_MANIFEST一致。read-only immutable SQLite integrity_check=ok、関数10456。
## 既存検索DBから得た新規の横断的な仮想メソッド意味論（すべて実calleeの確定ではない）
- 0x42A460の新規照合: 先頭スロット0x0063848C→0x0042A460（旧pointer_refs既知）。疑似Cはvptrをbasic_stringbufのvftableに戻し、破棄helper・条件付きdeallocateを呼ぶので、先頭は削除デストラクタの高確度候補。codeSHA=5B13545504CA6CA932905AA01D4C4B918BC82F510E9AC4274E96240F54852D96。
- +0x04（site 0x4709D0/0x42E74E）: 両readerの開始側、buffer非NULLならsentryより前に呼ぶ。_Lock相当の候補。callee未確定。
- +0x08（site 0x470AE3/0x42E810、別途0x42E700のsentry失敗枝）: 全終了側で呼ぶ。_Unlock相当の候補。stateの副作用が無いことは未証明。
- +0x18（site 0x470A1B）: 先読みで値を得る。後でbuffer pointerを進めるか+0x1Cを呼んで消費するため、非消費のunderflow相当という候補。0x470980 codeSHA=850A2D2AFD2929E4228F1232AACC50394ECCE9C289CFA3D7834824FA96D8A446。
- +0x1C（site 0x470A66）: bufferから直接消費できない場合に呼ぶ。返値を使わずgcountを1加算するため、消費するuflow相当の候補。動的副作用は未検証。
- +0x20（site 0x42ED07）: 0x42ECF0経由でブロックを読み、0x42E700のgcount低高32bitへ実取得数を加算。xsgetn相当の候補。stub codeSHA=509ABCB0231F72EE6B7D32D3F197B65F895CDFE2812F22188DBE481B45285E21。
- 5スロットを順序・用法で横断比較するとMSVC basic_streambufの_lock/_unlock/underflow/uflow/xsgetnという一貫した契約候補になる。先頭0x42A460は破棄系。この型付けは機能意味の仮説であり、vtable各slotの実ポインタ値を復元したものではない。
## 新たに明確になった64-bit ABIの注意
- 0x42ECF0の機械疑似Cはvoid __thiscallで3つのstack値を+0x20仮想関数へ転送する。一方0x42E700の疑似Cは戻りをundefined8として使い、64-bit gcountへ加算する。両者のvoid/uint64の型が一致せず、擬似C宣言をそのままhookシグネチャに採用不可。
- xsgetn相当ならスタックはdestポインタ1 dword + 要求数streamsize 2 dwordという3 dwordに整合し、戻り値EDX:EAXの64-bit実取得数が自然なABI候補。ただし実ASMでPUSH順・RET n・EDX:EAX更新を未確認のためVERIFY維持。
- 0x42ECF0→vtable+0x20 CALLsite0x42ED07、0x42E700→0x42ECF0 CALLsite0x42E77F。0x42E700 codeSHA=E50363BD394C5A7820AADE195D5B53B5B02CF000DA9C4AE12D6EB29C168C8A76。
## 検証境界・差分・次手
- 既存vftable pointer[15]のうちpointer_refsは先頭1件のみ。+0x04/+0x08/+0x18/+0x1C/+0x20の実メモリ内容・runtime vptr変更・異常時の仮想unlock副作用は未解決。欠落14件は旧既知で新規数に含めない。
- 0x470AACの旧疑似CはEH状態[EBP-4]=-1→+0x08仮想CALL→ExceptionList復元→親[EBP-0x14]返値という順序を示すが、保存実ASMは0x470AC5で切れる。epilogue/RET4・仮想unlock非throwは決め付けない。cleanup codeSHA=EDCF4BF40F09829251103D9A908D61652A194200D5FD66595F69E4035DF9094D。
- Ghidra pseudo/関数/参照は機械抽出。今回対象関数についてREA正式info/pseudo/assembly/callers/calleesの新規5種完全取得0、Evidence ID新規0、VERIFIED新規0。既存Wave1–5=64/64、Wave6正式0/16、旧候補TODO12/BLOCKED4/VERIFY0、今回の正式差分0/0/0。
- Golden旧EXE実ゲームPASS0・strict MATCH0・完全再実装率未計測。設計のみ: 1byte（通常/0xFF/EOF）、block（要求4取得3）、bufferあり/なし、開始sentry成功/失敗で+04/+08の回数とstate/例外型/64bit gcountを実機観測（すべてNOT RUN）。
- 接続時active.lock不在、Java/Ghidra process非検出、空き物理メモリ14054516KiB（約13.4GiB）、CPU使用率不明。新規REA/Ghidra実行0秒、軽量調査の全所要時間未測定、新規安全拒否0。
- 次回P0: 正規保存済みの+0x08/+0x20メソッド実装先証拠の有無、EDX:EAX/RET n ABIをさらに照合。拒否済みCALL_INDEX_V2、0x429620、Wave6/REA export等を再試行・迂回しない。見つからなければ仮説のまま。
- 書込範囲はREA担当の本新規Markdownだけ。MASTER/QUEUE/PROGRESS/A〜E/T018/dev_lab/旧runs/evidence/原EXE・SAVE/Git/公開先/毎時スケジュールへ変更なし。保存後readbackとSHA256は後続実行で確認する。
