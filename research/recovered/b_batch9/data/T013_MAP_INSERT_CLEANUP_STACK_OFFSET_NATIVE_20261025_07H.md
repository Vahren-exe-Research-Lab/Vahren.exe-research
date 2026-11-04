# B-20261025-07H-T013-INSERT-CLEANUP-STACK-OFFSET-01
Task T013（T028死亡callback文脈の辞書更新を参照） / B owner / 2026-10-25 07H JST
判定: PC-CONNECTED / STATIC-ORIGINAL-PE-ASM / STATIC-GHIDRA-V3 / VERIFY / NOT READY。実機Golden=0、strict MATCH=0。

## 開始監査・出典
Local CompactでMASTER（E旧checkpoint196、READY596）、ANALYSIS_LANES_PROTOCOL、LANE_B_HANDOFF・B担当T011/T012/T013/T024/T028、回収・安全拒否索引を先読。10/21回収22ファイル＋後続10研究、Library訂正版2、10～18H OFFLINE成果のID完全照合は未完。旧拒否操作再試行0。
原作EXE=rea_lab/targets/hakushin067_Vahren.exe 現物SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。search.sqlite現物SHA256 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF（BUILD_MANIFEST一致）。active.lock確認2箇所false。再Ghidra/REA・原作起動/改変なし。

## 独立増分A：0x0049CED0は挿入「成否8B」ではなく複合要素の破棄処理
Ghidra既存擬似C function 0x49CED0はsize72B。原作ASM 0x49CED0 MOV EAX,[ESI+0x1C]→0x49CED8 JE0x49CEF0、非NULL時0x49CEDE CALL0x415A60、0x49CEE7 CALL0x5B6BBB。0x49CEF0/F3/F6は[ESI+0x1C/+0x20/+0x24]を全0化。
0x49CEF9 CMP [ESI+0x14],0x10→短SSOなら解放なし、長なら0x49CF02 CALL0x5B6BBB、0x49CF0A [+0x10]=0、0x49CF0D [+0x14]=15、0x49CF14 先頭byte=0、RET0x49CF17。ESIは先頭文字列相当0x1C B＋[+1C,+20,+24] 3ポインタ様の複合オブジェクト。正確なC++型と例外時副作用はVERIFY。
0x49CED0本体は成功flagとしての[ESI+4] byteを検査しない。05Hの0x49F7D0 result[+0] iterator / [+4] flag1/0 の「8B結果」と区別する。

## 独立増分B：duplicate時の候補node破棄
原作ASM 0x49F8D8 CALL0x405370→0x49F8DF JE0x49F90C。0x49F90C LEA ESI,[EBP+0x0C]→0x49F90F CALL0x49CED0→0x49F917 CALL0x5B6BBB(EBP)→0x49F91F MOV [EBX],EDI→0x49F923 MOV BYTE [EBX+4],0→0x49F927 MOV EAX,EBX→0x49F92D RET8。
この等価キー候補経路は新候補側の埋込複合値を先に破棄し候補node自体をfree、既存iterator EDIとflag0を返す。JE成立の入力条件・例外時と実辞書不変条件はVERIFY。成功flag0/1自体は05H既知で再計上しない。

## 独立増分C：0x49CD60のstack offset補正（06H疑義にERRATUM）
0x49CE07 PUSH EAX / 0x49CE08 PUSH ESI によりCALL前ESP=S-8。0x49CE09 LEA EBX,[ESP+0x18] はS+0x10を指す。0x49CE0D CALL0x49F7D0のcallee RET8後ESP=Sに戻るため、出力結果は[ESP+0x10] iterator,[ESP+0x14] flagに位置する。
対して0x49CE52 MOV ESI,[ESP+0x18]、0x49CE5A MOV EDI,[ESP+0x1C]は結果構造体の直後を読んでおり、結果flagを消費する証拠ではない。06Hの「結果領域と位置が重なる」はこのスタック変動を無視した未確定記述だったため、ここで明示訂正する。別のalias /間接利用・全consumer不在までは断定しない。

## 呼出分布・非重複・局所署名
V3 read-only callers 0x49CED0 --limit 100 で直接CALL記録82件: 0x49F7D0内1件、0x4AE0F0本体38件、0x5Fxxxxアドレス43件（Unwind@005FE731/Unwind@005F58B8の2件はGhidra名を確認、残41名と到達はVERIFY）。通常内で0x4AE36A、0x4B00D3、0x4B0203（各0x49F7D0呼出の直後）のESI=ローカル複合要素、cleanupをASMで照合。
原作PE RAW窓SHA256: 0x49CED0+72B=BF08CDC3C9580A4EF3739FD9C5936EC247FDC6CDFCA5EC619537D8834464960E、0x49CE07+181B=05B85E5EE6A8B55B1B958BBE2636CC55D56AB640B30F57D8CC85A3B6DBAB345F、0x49F903+53B=4E411AAD60C2D80A0F7A113F5E8D1B90485B5B816B55B17219BB9D7743DFBB2B。
既B 05H insert結果ABI、06H13 caller/戻り値上書き、10/24 T028 writerは既知として再計上しない。新増分はcleanup構造/duplicate破棄/ESP+8ずれERRATUM/82参照の分類。T013/T028/HANDOFF直接照合済、全意味的重複・未同期統合はVERIFY。

## Goldenと次回
原作未改変EXE・X20強化前DAT・同SAVE/MAP/入力/RNGで新キー/同キー/複数文字列、死亡a/d callback各2経路のresult+0/+4、候補nodeの存否、辞書前後、可視イベントを比較DESIGNED_NOT_RUN。source/ASMのSTATICは実機strictを意味しない。
次は0x49F7D0の重複分岐の全入力・0x49CE0D以降[ESP+0x10/+0x14]の直接consumer有無と0x4AE0F0各cleanupの直前owner初期化をread-onlyで絞る。新B READY0、E MASTER0、DONE0、旧Gameplay PASS0、strict MATCH0。B-ownedだけ書込。