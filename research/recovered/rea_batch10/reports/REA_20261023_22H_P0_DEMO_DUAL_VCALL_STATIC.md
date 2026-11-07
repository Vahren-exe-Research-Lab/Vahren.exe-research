# REA-LOCAL-20261023-2236-P0-FASTSIM-DUAL-DEMO-VCALL-STATIC-01
日時: 2026-10-23 22時台 JST。owner=REA、関連T010/T012(P0)。STATIC / VERIFY / NOT READY、原作ゲームNOT RUN。
## 先行・出典・非重複
- 研究PC Local Compact接続成功。MASTER/解析規約/REA README/QUEUE/PROGRESS、保存済み21時台MD/JSON、既RUN・progress_sync、統合V9入口を先読。
- 研究コピー rea_lab/targets/hakushin067_Vahren.exe SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（今回実バイト再計算）。
- V9=HAKUSHIN067_UNIFIED_V9_20261023.sqlite SHA256=2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE、verify=V9_INDEPENDENT_READBACK_PASS（functions11950、refs243678）。PC標準ポインタはV3のまま。
- 既知: 20hのDemoPerson+0x90 secondary vptrとstate4 writer、21hの+0xA5 RTTI gate、18hのstate getter、16hの500反復。今回の新規差分は**反復ループ内の2箇所の実indirect CALL site**と**Player側virtual起点の初期化連結**。既知件数は再計上しない。
## 新規P0-A：indirect CALL siteを実機械語で特定
- 0x0040E40C CMP DWORD [EDI+0x288],0、0x40E413 JLE 0x40E639。したがって該当分岐でカウンタ+0x288>0のときだけ次の2更新が実行される（さらに手前の0x40E3F6/0x40E3FFの退出条件を通過した場合）。
- **第1 site 0x0040E42E FF D0 CALL EAX**: 0x40E419 ECX=[EDI+0x1C8] → 0x40E41F EDX=[ECX+0x90] → 0x40E425 EAX=[EDX+4] → 0x40E428 ECX+=0x90 → 0x40E42E CALL EAX。
- **第2 site 0x0040E445 FF D0 CALL EAX**: 0x40E430 ECX=[EDI+0x1CC] → 0x40E436 EDX=[ECX+0x90] → 0x40E43C EAX=[EDX+4] → 0x40E43F ECX+=0x90 → 0x40E445 CALL EAX。
- 2箇所とも副オブジェクトthis=元オブジェクト+0x90でvtable slot+0x04を呼ぶ。+0x1C8側を先に、+0x1CC側を後に呼び出す機械語順を確認。
- DemoPerson secondary vtable=0x00638054、pointer cell 0x00638058=0x00449730。Enemy secondary vtable=0x00638B84、cell 0x00638B88=0x004498E0。従って元オブジェクトがDemoPersonなら0x449730へ、Enemyなら0x4498E0へディスパッチする構造。実行時クラス固定・置換禁止までは未証明。
- +0x288<=0の分岐0x40E639からは既知のprimary vptr+0x18（0x40E644/0x40E658）によるstate4比較経路。今回の発見は、継続中の副vfunc更新と終了時のprimary状態読出しの境界を結ぶ。
## 新規P0-B：Player側virtual初期化チェーン
- `Player` primary vtable=0x00639B08、slot+0x04（cell 0x639B0C）=0x0051E6F0、slot+0x0C（cell 0x639B14）=0x0051EF80。PE pointer 2/2独立検証。RTTI .?AVPlayer@@、primary COL offset=0。
- 0x0051E13E MOV [EDI],0x639B08・0x51E144 MOV [EDI+0x90],0x639B2C によるPlayer主・副vptrを原作機械語で確認。0x51E59B/0x51E5A1でも同じ代入を確認（後者はcleanup側の可能性があり新規生成数には加算しない）。副COL offset=0x90。
- Player slot+0x04の0x51E6F0はGhidra疑似C上で分岐case1において0x51ED78 CALL 0x0040CCF0（E8 rel32を機械語で独立計算）。この関数の0x40CD63/0x40CD69、0x40CDBE/0x40CDC4でDemoPerson primary vptr=0x638030、secondary vptr=0x638054を設定する2箇所を確認（生成可否・存在数は条件付き）。
- Player slot+0x0Cの0x51EF80は0x51EF8Fで0x00447810を直接CALL。21h既知のRTTI/+0xA5初期化ゲートと構造的に結合。DemoPerson primary slot+0x0C（0x63803C）も0x447810を指す（クラスごとの動的対象は確認中）。
- **slot順序や関数ポインタ登録は実行時の呼出順序を証明しない**。0x51E6F0→0x40CCF0と0x51EF80→0x447810の各条件付き静的接続のみ認定し、Player/SIMの動的時系列と戦闘勝敗意味はVERIFY。
## 検証・証拠
- 原作EXEをpefile PE32 RVA→raw bytesで読み、Capstone x86独立逆アセンブル。今回の検査: opcode25/25、pointer12/12、RTTI4/4、E8 rel32 target2/2、合計43/43 PASS。期待命令・pointer集合は同研究IDのJSONに記録。
- RTTI subobject offsets: Player主0、Player副0x90、DemoPerson副0x90、Enemy副0x90。RTTI/ptrの静的検証であり安全なフックABIや生存時vptrの実値を保証しない。
- V9 search_unified_v9_20261023.py: callers 0x449730=0、callers 0x51EF80=0（E8直接CALLだけ）、pe-to 0x449730=0x638058、pe-to 0x51EF80=0x639B14、pe-to 0x639B08=0x51E140/0x51E59D。**直接caller=0は間接CALL不存在を意味しない**。
- 既存REA Wave1-5=64/64はlogs/progress_sync_20261011T153958076Z.json由来。今回は新規Ghidra0/REA0、正式5種類info/pseudo/assembly/callers/callees新規完全セット0、REA新VERIFIED0、正式TODO/VERIFY/BLOCKED差分0/0/0。
- 原作実機Golden PASS0、strict MATCH0、複製率未測定。+288>0 / <=0・各2側vptr・状態4のGolden条件設計のみ、未実測・NOT RUN。
## 安全・保存範囲・次回
- 直前prefight: active.lockなし、Java/Ghidraプロセス0、空きRAM約13.44GiB。CPU負荷・総研究所要時間は未測定。新規Ghidra/REA、旧原作ゲーム実行なし。
- 原本ZIP/EXE/SAVE、MASTER、他A-E、QUEUE/PROGRESS、既存runs/evidence、dev_lab/Work、Git/push、UI/操作、スケジュールを変更しない。安全拒否済み範囲・Wave6・export未試行。保存はREA所有固有ファイルだけ、保存結果とreadbackは別途確認。
- 次P0: 0x40E419/0x40E430で読む+0x1C8/+0x1CCオブジェクトの実行時型/寿命、Player slot+0x04/+0x0Cを実際に呼ぶ上位indirect site、+0x14/+0x18/+0xA5の初期化writer、state4到達時の順序。Golden実測へ無断昇格しない。
