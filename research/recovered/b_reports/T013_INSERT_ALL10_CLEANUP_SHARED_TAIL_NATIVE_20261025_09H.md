# B-20261025-09H-T013-ALL10-INSERT-CLEANUP-SHARED-TAIL-01
日時 2026-10-25 09H JST / owner B T013（T028参照） / STATIC-ORIGINAL-PE-ASM・VERIFY・NOT READY。公式READY追加0、E MASTER統合0、DONE0、原作Gameplay Golden PASS0、strict MATCH0。
## 事前確認
Desktop Commander Local Compact接続。MASTER最終E cp196・READY596は旧値（再集計なし）。ANALYSIS_LANES_PROTOCOL、B HANDOFF、T011/T012/T013/T024/T028、UNSYNCED_RECOVERY_REGISTER、安全拒否記録を先読。
検索基盤は旧search.sqliteではなくCURRENT_ACTIVE_RESEARCH_STATE_LATEST指定のV3。既存guard PASS_ACTIVE_V3_STATIC、入力SHA14/14、PE E8 CALL44889、E9/EB JMP6324、errors=[]。旧search.sqlite/README/BUILD_MANIFESTも履歴確認のみ。
対象：rea_lab/targets/hakushin067_Vahren.exe（ファイルの読取だけ）。本回で現物SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187一致。原作実行・変更なし。
## 新規確認：0x004AE0F0内の辞書挿入10 CALLの後処理
前06HでE8 CALL先0x0049F7D0が13箇所・0x004AE0F0所有10箇所であることは既成果（今回再計数0）。今回は原作PEの各CALL命令境界からCapstone x86/32で後続を個別decodeし、10/10のcleanup・共通終端到達を追加証明。
0x004AE35F CALL→0x004AE364 LEA ESI,[EBP-0xC34]→0x004AE36A CALL 0x0049CED0→0x004AE385 XOR AL,AL→0x004AE387 JMP 0x004B37CE。
0x004B00C8 CALL→0x004B00CD ESI=[EBP-0xF4C]→0x004B00D3 cleanup→0x004B00F9 XOR AL,AL→0x004B00FB JMP 0x004B37CE。
0x004B01F8 CALL→0x004B01FD ESI=[EBP-0xC8C]→0x004B0203 cleanup→0x004B0229 XOR AL,AL→0x004B022B JMP 0x004B37CE。
0x004B03AA CALL→0x004B03AF ESI=[EBP-0x10AC]→0x004B03B5 cleanup→0x004B03DB XOR AL,AL→0x004B03DD JMP 0x004B37CE。
0x004B05B0 CALL→0x004B05B5 ESI=[EBP-0xCE4]→0x004B05BB cleanup→0x004B05E8 XOR AL,AL→0x004B05EA JMP 0x004B37CE。
0x004B06C7 CALL→0x004B06CC ESI=[EBP-0xFA4]→0x004B06D2 cleanup→0x004B06F8 XOR AL,AL→0x004B06FA JMP 0x004B37CE。
0x004B07A1 CALL→0x004B07A6 ESI=[EBP-0xD3C]→0x004B07AC JMP 0x004B06D2（共有cleanup）→0x004B06F8 XOR AL,AL→共通終端。
0x004B087D CALL→0x004B0882 ESI=[EBP-0x1188]→0x004B0888 cleanup→0x004B08A3 XOR AL,AL→0x004B08A5 JMP 0x004B37CE。
0x004B20ED CALL→0x004B20F2 ESI=[EBP-0xE18]→0x004B20F8 JMP 0x004B1FD1（共有cleanup）→0x004B1FF7 XOR AL,AL→0x004B1FF9 JMP共通終端。
0x004B345C CALL→0x004B3461 ESI=[EBP-0xEF4]→0x004B3467 cleanup→0x004B348D XOR AL,AL→0x004B348F JMP 0x004B37CE。
結論：10箇所すべてで結果EAXを直後に直接判定せず、異なるローカル複合値のcleanup（8件直CALL＋2件共有JMP）から共通終端に進む。0x004B37CEはstack/cookie epilogue→0x004B37E9 RET4。cleanupが挿入結果8Bレコードのfreeではないことは前07Hの独立証拠。cookie helper 0x005B6513のEAX副作用は未監査につき、関数の最終AL=0は断定しない。
前08Hは0x004A60AA→0x004A64A0の別vector cleanupを確定。今回の10箇所は0x0049CED0型である（前08Hの別callerと混同しない）。今回の新規差分は未走査7箇所を含む全10での共通cleanup/終端網羅と、2箇所の共有JMP実体の特定。
## 限界／受入条件
RESULT[+4]挿入成功フラグの全consumer不存在、間接alias、例外/Unwind、cleanup副作用、辞書のゲーム上の用途、実行時到達・重複イベント効果はVERIFY。ALクリアとGameplay成功/失敗の同一視禁止。T013対象選択アルゴリズムの完成を意味しない。
既存ID/Owner直接照合：B T013/HANDOFFで新ID・0x4B07AC・0x4B20F8の正規表記一致0、過去06Hの13 E8 site、07Hのcleanup関数契約・3例、08Hの別cleanupは再計上0。他owner/Library/OFFLINE全件意味照合は未完。
旧22ファイル回収＋後続研究・Library訂正版・オフライン成果は全ID統合未了、既拒否VA0x5710C0..0x571500・0x599BD0照会・拒否記録を迂回/再試行しない。
Golden設計のみ：無改変原作EXE・20倍変更前DAT・同一SAVE/MAP/input/RNGで各10分岐の合法到達、同key/新key、event辞書前後、可視Unit/HP/イベントを同run照合する。NOT RUN、actual gameplay PASS0、strict MATCH0。
## 次の許可された一手
0x004AE0F0の10分岐へ至る入力条件と辞書KEY/valueのproducerをV3索引＋B既保存ASMから限定調査。後続0x004B37CEのreturn contractは別に検証。T024/T028と連携して死亡イベント辞書更新（0x0049CD60）との差異を証拠で区別。MASTER正式統合はEのみ。
PC書込はこのB-owned詳細とT013_AI、LANE_B_HANDOFFに限定。新Ghidra/Java/REA・原作プログラム起動/変更なし。安全拒否新規0。初回Python UTF-8 STDINで日本語パス文字化け＋誤ったheadless_analysis/targets指定によりFileNotFound/AssertionError（OTHER/RECOVERED）後、rea_labを作業ディレクトリにしてASCII相対targetsを使った同一許可済読取で成功。復旧ID B-RC-20261025-09H-PE-PATH-ENCODING-01。
