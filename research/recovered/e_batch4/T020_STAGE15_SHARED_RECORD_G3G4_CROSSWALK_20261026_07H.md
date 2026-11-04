# E-AUDIT-20261026-07H-T018-T020-SHARED-RECORD-G3G4-CROSSWALK-01
Owner E / T018・T020（T019照会）。2026-10-26 07H JST。保存済み原作静的証拠＋保存RAWの再検証。STATIC / SYNTHETIC PASS / VERIFY / NOT READY。新規原作ゲーム実行なし。
## 既存研究の独立突合：新しいE受入差分
Stage13 BATTLE_STAGE13_INPUT_COVERAGE_20261022.jsonの実RAW8件・原作2セッションを再照合。Unit+0x1C8（shared-record pointer）は延べ4190観測でPRESENT。一方、Stage13のunit_coverageには指し先Recordの+0x16C EXP・+0x1B0/+0x1B1等の実バイトbefore/after取得証拠がない（抽出範囲の欠落であって元ゲームメモリの不存在ではない）。
Stage15既保存ASMの0x551EA3はUnit+0x1C8を取得し、0x551FB2はRecord+0x16C加算を行う局所writer。0x575AB3のRecord+0x1B1=1、0x57897BのRecord+0x1B0書込みは異なるfield。Stage15 casualty保存命令0x588E34は+0x174減算、0x588E40は+0x5C減算、medical/alive_per等の条件付き副作用候補あり。全Unit/全戦闘で必ず適用と断定しない。
**受入上の重要な限定:** 勝者side/resultCodeだけ取得できても、戦略へ持ち越すUnit状態・経験値/死亡・費用を復元・検証できるとは限らない。外部戦闘からの勝敗のみを書き戻す設計は、元native finishに共有Recordの変更を任せる契約を別途実証するまで、G4とsemantic strategy consistencyへ昇格不可。
保存済Stage15の126 synthetic/own-childテストは実ゲームresult writebackの証明ではない。native_result_writeback_proven=false、gui_connected_to_new_backend=falseを今回のEゲートで再確認。
## セッション真正性とGolden
原作旧G0観測は2026-10-21 PID23272の一件でnative mode2/active1が事後PASS。これに対しStage13 RAW8件はPID28432/32468の別セッションであり、G0とRAWを一つの戦闘として結合できない。元G0の攻撃Spot/native ID・直前SAVE+入力・MAP/三陣営・確定出撃名簿は未取得。C-NB02 E_G0_FULL_RECEIPTも未充足。
G3は勝敗結果・意味陣営・時相の実観測が欠落。G4は同一戦闘のpre/post共有Record・World差分とnative finish一回性が欠落。Stage13 outcome_side_pair_indices=[1,0]は勝者ではない（前06H監査と重複加算しない）。
新規E DYNAMIC OBSERVED=0、actual Gameplay Golden PASS=0、strict MATCH=0。REA過去原作native G0 OBSERVED1は別の既存指標。T018/C-NB02 G0/G1/G2/G3/G4正式受入0。
## T020 新規実行結果・出典
新規 tests/t020_stage15_shared_state_exit_crosswalk_20261026_07H.py、SHA256=15561B2545BF6F09AE7192E8C1693C4D430D07966793DC2A79744A6AAB78DAED。
Python -Bで9/9 unittest PASS、FAIL0、exit0。内容：stage13/stage15/casualty/G0のsource SHA4件、RAW8件のSHA8件、Unit record参照延べ4190、別セッション、共有Record native writer、医療系条件付き減算、欠損G3/G4、synthetic negative winner-only/一回性/World欠損。これは旧証拠再解析と合成境界検査であって原作Goldenテストではない。
source original EXE識別SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（保存済み各manifestの値。今run原EXE再hashなし）。現行V3 Ghidra DBは起動/書込/再構築せず。
## MASTER・T019・安全
MASTER TASK QUEUEを今run read-only再集計：34 unique、DONE9 / IN_PROGRESS21 / VERIFY4。最後の正式checkpoint196／READY596（A115/B229/C136/D116）は既存公式値・596ID全列挙なし。新規統合READY0。B最新07HはNOT READY、代理統合しない。
T019新規確定Wiki/DAT/EXE矛盾0。GameClear DAT13/TXT2字句検索範囲差RESOLVED、script2優先・phase flag・TXT実読込・gwrite復帰はVERIFY。
既存拒否T018表境界、旧Stage15意味出口ノート保存拒否（E-RC-20261022-0849）、C T026/T032、D T030 TSV、0x5710C0等はBLOCKED継続。元拒否本文/操作の再提出・迂回なし。13/14H OFFLINE-UNSYNCEDは正式未統合。
今回の新規PC書込はE所有T020検証器とこの独立E所有資料のみ。MASTER/A-D/REA/dev_lab/原本EXE・DAT・ZIP・SAVE・Git/push・Work/設定/automation変更なし。
次の優先：合法C-NB02同一runの旧G0 UI→G1直前SAVE+入力→G2 MAP/3陣営/確定名簿の実バイトreceipt。出口はG3勝敗/意味side、G4共有Record pre/post＋World差分＋single native finishをそれぞれ独立に取得し、結果packetだけで戦略互換を認定しない。
