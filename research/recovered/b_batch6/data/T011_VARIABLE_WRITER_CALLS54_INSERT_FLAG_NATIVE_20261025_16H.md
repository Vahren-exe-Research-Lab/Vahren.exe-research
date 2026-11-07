# T011｜数値変数writerの直接CALL 54件・更新flag・挿入結果の静的監査（2026-10-25 16H）
ID: B-20261025-1615-T011-WRITER-CALLSITE-54-INSERT-FLAG-01 / Owner=B / STATIC-ORIGINAL-PE-ASM + STATIC-GHIDRA / VERIFY / NOT READY
## PRECHECK / SOURCE / 未同期
- Desktop Commander Local Compact接続成功。MASTER cp196/READY596（E旧正式値）、ANALYSIS_LANES_PROTOCOL・B HANDOFF・B担当T011/T012/T013/T024/T028と15H detail・未同期/既拒否の状態を先読。
- 原作rea_lab/targets/hakushin067_Vahren.exe実SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。search_index/search.sqlite実SHA256=0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF（BUILD_MANIFEST一致）。active.lock2候補false、Java/Ghidra 0。原作・Ghidra・REAは実行/再解析せずread-only。
- 13H詳細回収は前15Hでreadback済。14H OFFLINEの B-OFFLINE-20261025-1411-T011-COUNTER-REPLACE-ERASE-01 は前15Hが局所ASM確認済だが全文PC同期/全ID統合未完。回収済22件+後続10件+Library訂正版2の全意味照合も未完。旧安全拒否を別経路で再試行せず。
## 新規証拠1｜writer 0x004637A0 の参照fan-in
- 既存search.py callers 0x004637A0 --limit 100 からGhidra直接CALL候補54件・呼出元10関数を取得。原作PEの各site E8 rel32を独立検査した結果、54/54件が同VAへの直接CALL（MISMATCH 0）。索引外CALLを否定しないため『少なくとも54件』。
- 10関数内訳：0x4321B0:1、0x441200:1、0x45BE10:11、0x466F60:1、0x46B3A0:1、0x46B8D0:1、0x46BB80:1、0x46C710:1、0x4A7A90:2、0x4AE0F0:34。合計54。opcode VM側34+11の実ゲーム上の意味は担当Aの領域と混同しない。
- 原作PEのsorted 54サイトに (site VA LE4 + E8の5B) を連結した486BのSHA256=DC3D4397869E64187A64BE60257699FE676509A71B10C66CFB5724E187A526DB。
## 新規証拠2｜B関係の型復元済7 callerの更新flag
- Ghidra擬似Cに3引数が残る7関数のCALLはすべて第3引数=1：0x432379（0x4321B0）、0x44130A（0x441200）、0x467126（0x466F60）、0x46B53C（0x46B3A0）、0x46B9FB（0x46B8D0）、0x46BC39（0x46BB80）、0x46C8D1（0x46C710）。これらのCALL site E8自体は原作PE 7/7一致。引数1という判断はGhidra pseudo由来、0x467121 PUSH1→0x467126 CALLのみ既14H nativeでも確認。
- 残47 site（0x45BE10内11、0x4A7A90内2、0x4AE0F0内34）のGhidra pseudoはFUN_004637a0()無引数表示。全47件のflag値や永続化スコープを1と仮定しない（VERIFY）。
## 新規証拠3｜insert helperは正常経路で成功flagを1にする
- 原作PE 0x004A69B0の178B窓SHA=46247E4D5C71AEF8EFF1610332663CB179A45EF502ECB4F5386C828A36528419。ASM 0x4A6A48 CALL0x4A6700→0x4A6A55 MOV [EAX],EDX→0x4A6A57 MOV byte[EAX+4],1→0x4A6A5F RET 0xC。Ghidra pseudoは正常search終了後に0x4A6700を呼びflag=1をセットする。
- 原作PE 0x004A6700先頭100B窓SHA=632DCD134A1D92A1A21527B4988E791AC090D3218745E364CB15D795BD2490F1。0x4A6708 CMP count,0x7FFFFFE→0x4A670E JB0x4A6747（非上限枝）。正常挿入枝0x4A6747 INC ECX→0x4A6748 MOV [EDI+8],ECXでmap要素数を1増やす。上限側は解放/例外経路であり正常挿入と区別。
- 旧14Hのwriter 0x4637A0はflag!=0で既存key検索し、既存時0x46386C erase→0x463896 fresh48B node→0x4638A2 insert（新32B値object生成は先行）。今回の独立増分は54サイトの原作rel32全件検証、7型復元callerのflag分布、挿入helperの正常結果flag/要素数増分のnative裏付け。旧14H/15Hのeraseや値pointer +0x28/free不在を新発見として再計数しない。
## 再実装・VERIFY・Golden・状態
- 値の更新結果と node/value identity は別に検証する。0x4A6A57のflag1は当該正常挿入枝の返却であって、全callerでの重複key不存在/値解放/リーク無しを証明しない。param4=0の実caller、48B nodeとの同名競合、他owner lifetime、例外巻戻し、actual gameplayはVERIFY。
- 原作Golden: 同じ無改変旧EXE、X20改変前DAT、同一SAVE/MAP/input/RNGで数値変数の初回作成→同名更新→別owner→保存復帰、old/new値・map count・node/value identity・旧値解放/次tickを同一run比較。DESIGNED_NOT_RUN、Gameplay PASS0、strict MATCH0。
- ID重複はB5主資料/HANDOFFへの今回主要アドレス・研究ID直接照合で未発見（他lane/未同期の意味的重複はVERIFY）。新B READY0、E MASTER統合0、Task DONE0。書込先はB所有detail、T011_DATA_MODEL、LANE_B_HANDOFFのみ。原本/他lane/REA/dev_lab/Git/Work/設定/automation書込0。
- NEXT: T011の値ポインタ最終ownerは引き続きVERIFYとし、0x4A69B0正常枝と例外/duplicate境界を必要な範囲で確認。その後はT024/T028の実戦P0へ研究資源を戻す。
