# 迫真戦記 ver0.67｜REA 18時台：OggDecoder仮想cleanupと再ロード時のFILE*寿命
研究ID：REA-LOCAL-20261025-1836-P0-OGG-VSLOT10-RELOAD-LIFETIME-STATIC-01
状態：PC-SAVED / STATIC / VERIFY / NOT READY。新規正式VERIFIED=0、原作Golden実測=0。
原作SHA256：E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
検索DB SHA256：0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF。
既存17時台ID REA-LOCAL-20261025-1736-P0-FILE-CLOSE-CALLBACK-BRIDGE-STATIC-01を継承し、fclose callbackの既存発見は再計上しない。

## 新発見：0x0050202A間接CALLのvtable slotを解決
- 0x00501E7Eでowner[0]=0x006395CC（OggDecoder vftable）を設定し、0x00501E93→0x00502020を直接呼ぶ。
- 0x00502024 MOV EAX,[ESI] → 0x00502026 MOV EDX,[EAX+0x10] → 0x0050202A CALL EDX。静的Ogg vtable実バイト：slot[4] +0x10 = 0x00501EB0。
- 0x00501EB0はowner[+5]==1の場合のみ0x00501EC1→0x005CFE00を呼び、先に発見した+0x2C8 fclose callbackの条件付き経路へ接続。以後0x2D0-byte contextとowner側フィールドをクリアする。
- 続いて0x00502038→0x005D16C0が新ファイルを開く。戻り値非0（失敗）なら0x00502046でAL=0を返し、成功なら0x00502085でowner[+5]=1とし0x0050208AでAL=1。
- このため【Ogg vtableが保持され、既存FILE*が所有者に残り、cleanup gateを満たす】再ロードでは、旧FILE*を閉じてから新しく開く契約が静的に成立する。全呼出元・異常例外での保証は未実測。

## 新発見：初回構築とvirtual cleanupの差
- 0x00501E52 MOV WORD [ESI+4],0、0x00501E84によるcontext初期化が0x00501E93のloadより先。よって通常の新規構築時の仮想cleanupはowner[+5]=0のためfcloseを実行しない。
- 0x00501E93でのload戻り値はctorから上位へBOOLとして伝播せず、0x00501E98 MOV EAX,ESIにより常にthisが返る。load失敗後の状態検査は呼出側の責任（上位詳細VERIFY）。
- 破棄0x00501DF0は0x006395CCにvtableを設定して0x00501DF9→0x00501EB0を直接実行し、その後0x00501E03でPCMDecoder vtable 0x006395E4へ変更。削除フラグがあればdelete処理へ進む。
- PCMDecoder vtableの+0x10は0x005020C0（基底フィールド初期化）で、OggDecoderの+0x10=0x00501EB0と異なる。仮想slot番号だけで一律にfclose処理と解釈しない。

## 根拠と制約
- 出典：2026-10-21初期Ghidra search.sqlite（function/callers/callees/related、indirect_calls site 0x0050202A）と同一SHAの隔離EXEのPE実バイト。vtableをstructで独立読取、Capstoneで対象機械語を独立復号。
- 独立静的監査39/39 PASS（原作・DB SHA、PE image base、vtable 6条件、ASM20条件、DB整合性・直接CALL4・間接CALL1・関数4）。これは検査条件数であり正式新規VERIFIED件数ではない。
- REA正式5種：info=既存索引、pseudo=既存Ghidra機械出力、assembly=局所独立照合、callers/callees=既存索引。5種新規関数別完成0、VERIFIED増加0。旧Wave1-5=64/64は2026-10-11保存済sync照合、QUEUE/PROGRESSは旧EPERMのため状態表示が古い。
- 正式TODO/VERIFY/BLOCKED書込差分=0/0/0。旧EXE Golden PASS=0、strict MATCH未測定、完全複製率未測定。13/14時台OFFLINE成果のPC正本への完全同期は未実施（今回も触れない）。
- 未解決：virtual再ロードが実機でどの呼出元から発生するか、例外時の所有権、二重closeが起きない全経路証明、上位constructorの失敗チェック。

## PC・保存状態と次のP0
- PC接続成功。開始時active.lock=False、Java/Ghidra/REA専用の並行解析プロセスは確認されず。開始時空きRAM約12942MiB、CPU瞬間値32%。研究全体実行時間は未測定。監査初回約0.7644秒、別実行約0.3371秒。
- REA・Ghidra・原作ゲームの新規起動0。安全拒否済Wave6/0x5710C0..0x571500、09時台拒否済監査追記は再試行しない。
- 書込はREA所有の新規18時台成果のみ。原本/MASTER/QUEUE/PROGRESS/runs/他レーン/Git/Work/スケジュールは無変更。
- Golden設計（NOT RUN）：有効Ogg→別Ogg成功、成功→存在しないファイル、失敗→正常ファイル、成功→オブジェクト破棄の各ケースでfclose回数・state byte・bool・handleを測定。
- 次のP0は0x004BEAD9の上位ctor呼出元・0x00502220・0x00501E20戻り値無視からのエラー処理を追い、失敗したOggの所有者破棄・例外後状態をVERIFY。0x00502020への外部仮想呼出し（vtable+0x0C）の発生元も未同定。
- 独立audit/probe/JSON/report各ファイルを保存した後に、readbackとSHAを別プロセスで検査する。現時点でformal verified増分0。
