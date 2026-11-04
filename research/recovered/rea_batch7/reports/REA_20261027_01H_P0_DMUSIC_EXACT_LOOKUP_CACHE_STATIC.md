# 迫真戦記 ver0.67 REA｜2026-10-27 01時台 P0 DirectMusic厳密キー探索とmissキャッシュ
研究ID: REA-LOCAL-20261027-01H-P0-DMUSIC-EXACT-LOOKUP-CACHE-STATIC-01
状態: PC-SAVED / STATIC / VERIFY / NOT READY。ゲーム実機Golden NOT RUN。
原作研究EXE SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
旧検索DB SHA256: 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF
統合V9 DB SHA256: 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE

## 旧成果との分離
前回23Hまでで0x004BE820の名前検索不一致→乱数×個数→+0x70配列参照をSTATIC確認済み。本回では「どの比較条件で不一致になるか」と「選択後のキー登録」を新規限定監査。既存64関数や23Hの結果は再カウントしない。

## 新規結果A：lower_boundに加えて一致確認する（STATIC）
0x004BDE40:0x004BE178 CALL 0x004BE820。0x004BE820:0x004BEEACでESI=[EBP+0x7C]の検索木、0x004BEEBE CALL 0x004C1200。0x004C1200:0x004C1209 CALL 0x004682B0で木のlower_bound候補を取得。
0x004682B0:0x004682F9 CALL 0x00402C40、0x0046830D/0F/14/18の分岐は「candidate>=requested key」の先頭候補に向かう。0x00402C40はmovzxの非符号byte比較、差の符号を0/-1/+1へ変換（0x00402C6E/0x00402CA3/0x00402CA7）。
0x004C1200:0x004C1244でも同じ比較器を逆側の引数順で使用し、0x004C124Fの長さ分岐と0x004C1258の符号分岐によって候補がkeyより大きいと番兵を返す。lower_bound候補がkey未満にならないことと合わせ、返したノードは実質的にkey一致。Ghidra擬似Cのみでなく各命令をCapstoneで確認。
0x004BE820:0x004BEEE3 CMP ECX,[EBP+0x80]→0x004BEEE9 JE 0x004BEEFAで番兵時のみ既報の乱数fallback。一致時は0x004BEEEBでnode+0x28から登録済み値を使用、乱数を使わない。

## 新規結果B：乱数fallbackの直後に木への登録がある（STATIC）
0x004BEF04 rand→0x004BEF1B FTOL→0x004BEF27 [EDX+EAX*4]でPerformanceスロット取得（ここは既報）。
追加で0x004BEF2F MOV [EBX],EAX（EBX=[EBP+0x78]）。0x004BEF48 CALL 0x00510F70が文字列+値ペアを構築し、0x00510F91でpair+0x1Cへ値を書き込む。
0x004BEF5C CALL 0x00436680がノードを生成。0x004366FE/0x00436701によりnode+0x28へペアの値を格納する。0x004BEF68 CALL 0x00463280は検索時と同じESI=[EBP+0x7C]の木にinsert-if-absentを実行する経路と整合。generic insert-if-absent自体はMASTERの既存成果であり新規に数えない。
同一オブジェクト・同一正規化キーで登録成功した後の再呼出しなら、次回は既存ノードを使って乱数選択を省略する構造と推定。ただし挿入成功率・オブジェクト破棄/再生成・名前正規化・実ゲーム時の再利用は未実測のためVERIFY。

## 独立照合・状態
原作EXE/旧DB/V9をSHA256確認、両SQLiteのquick_check、PE32 ImageBase、関数とCALL siteの登録5対×DB2、対象限定の31個の原作ASM条件、過去23Hの証拠および64/64同期記録を照合。静的監査51/51 PASS。lower_bound+reject-greaterの合成モデルはkey集合256種×問合せ12種=3,072条件でfalse positive/false negative 0。ただし合成検証でありGoldenには加算しない。
正式REA新規VERIFIED 0。旧Wave1～5 VERIFIED 64/64を旧同期記録として保持。5種はinfo/pseudo/callers/callees=INDEX_ONLY、assembly=TARGETED_PE_NATIVE。正式TODO/VERIFY/BLOCKED書込差分=0/0/0。原作Golden実測PASS0、strict MATCH・完全複製率未測定。
PC接続成功、active.lockなし、Java/Ghidra稼働検出なし、初期空き物理RAM約12.49GiB、CPU負荷不明。独立監査単体3.826秒、保存実行2.247秒、全作業時間未測定。新REA/Ghidra/原作ゲーム/Workなし。安全拒否なし。
原本ZIP/EXE/SAVE、MASTER/QUEUE/PROGRESS/既存runs、他A～E/T018/dev_lab、Git/公開先/スケジュール未変更。過去のOFFLINE-UNSYNCEDは未統合。

## 次のP0
0x004BE820の検索キー生成・入力文字列変換（0x00426490、0x00402800、0x004261B0、0x0040B200）を限定追跡し、完全一致になる入力条件・大文字小文字・拡張子処理の仮説を整理。次に0x00463280のinsert成功フラグと同一キー再利用、count=0でのlookup miss到達性、+0x70配列所有権をVERIFY。原作Goldenは隔離環境がないためNOT RUN。
