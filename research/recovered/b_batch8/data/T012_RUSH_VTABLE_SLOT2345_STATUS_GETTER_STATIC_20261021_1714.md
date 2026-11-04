# B-20261021-1714-01｜RushMissile vtable後半のstatus/getterと初期化値の接続
[OWNER/TIME] 新B・T012主（T011参照）。2026-10-21 17時台 JST。STATIC/INFERRED/VERIFY・NOT READY。PC正本read-only参照。EXE実行/変更0。
[SOURCE] PC MASTER cp195/公式READY595（E記載値、今回全件再計数なし）；evidence/ANALYSIS_LANES_PROTOCOL.md；B HANDOFF；rea_lab/headless_analysis/search_index/README.md・BUILD_MANIFEST.json・search.sqliteを既存search.pyで読取。
[TARGET] ver0.67同梱EXE SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（manifest一致。今回原本再ハッシュなし）。
[PRIOR DEDUP] B-OFFLINE-20261021-1608-01でRushMissile vtable 0x63A6B4のslot0..5とslot1=0x5501A0がPE根拠で記録済み。本回はvtable byte/relocationを再解析せず、後半4slotの関数本体とinit fieldの関係だけを増分とする。
[VTABLE 0-BASED] slot2 @0x63A6BC → 0x431910；slot3 @0x63A6C0 → 0x54E0A0；slot4 @0x63A6C4 → 0x54E0A0；slot5 @0x63A6C8 → 0x43B5A0。slot対応は先行16:08 STATIC研究から継承。
[NEW GHIDRA] search.py function 0x431910: size3, return 1、直接caller0。search.py function 0x54E0A0: size7, __fastcall record→return *(byte *)(record+0x210)、直接caller0。search.py function 0x43B5A0: size3, return 0、直接caller0。
[FACT] slot3/slot4は同じbyte getterを共有し、slot2/slot5は定数1/0を返す。機械的な関数本体はSTATIC-PSEUDOC。各slotの意味名（alive/visible/collidable等）はUNKNOWN。
[ASM JOIN] 保存済B owner exe/T013_RUSH_RECORD_54F990_NATIVE_20261013.txt。0x54F9C5: byte[Rush+0x210]=0；0x54F9DA actor byte+0x65==0なら0x54F9E2 CALL 54FD50後、0x54F9ED actor+0x1C4 byte→Rush+0x210。
[ASM JOIN CONT] actor byte+0x65!=0なら0x54F9FB→0x54FA01: [actor+0x1C8]+0x1A8 byte→Rush+0x210（0x54FA07）。両枝は0x54FA0Dに合流。
[CROSS] slot3/4 getterが読むRush+0x210はinitializerがactor状態からコピーする値。これはstatic owner-state snapshot候補であり、後続の書換え有無・virtual呼出時刻は未確認。
[IMPORTANT] slot3とslot4の同一関数ポインタは、ゲーム上の2メソッドの同義性や動的分岐の相等性を証明しない。複数slotの異なるinterface用途はVERIFY。
[GOLDEN DESIGN] 合法Rush技能でactor+0x65の2分岐に相当する出撃形態とRush初回/再利用・状態変化前後を旧EXE/DAT/SAVE/map/input/capture各SHAで採取。slot内部byte不可視ならINELIGIBLE、可視挙動との一致確認までactual Golden PASS0・strict MATCH0。
[UNKNOWN] slot1 0x5501A0の実際のCALL [vptr+4]位置、slot2-5の間接caller、0x210後続writer、0x54FD50副作用、owner pointer妥当性、getterのゲーム上の意味、実機時刻/RNG/HP/MP。
[SAFETY] 本回別件 B-RC-20261021-1714-INDIRECT-SQL-SAFETY-01：Localで間接call索引の軽量read-only SQL結果取得を意図した2回の起動。最初は引用符構文エラー（OTHER、実際のSQLは未実行）；修正版はOpenAI safety checks拒否（SAFETY_REFUSAL）。拒否SQLの結果0／内容未取得。
[SAFETY IMPACT] 拒否された間接call一覧取得は未実行・未保存。拒否後、同一SQLの別shell/tool/path/Remote/ZIP再試行0、禁止VA 0x5710C0..0x571500等の探索0。別題の既許可search.py functionによるslot body照合は実行。
[RECOVERY] 本文とB HANDOFFの安全IDは新規独立記録。既B-RC-20261021-0910拒否2件、旧08時台同期拒否、26候補、X14/P4/I0/D1/C4/L2/O1、部分JSON INVALID、旧拒否案件は状態変更なし。
[READY/OWNERSHIP] B新規READY0、E MASTER統合0。HANDOFFへの通知後もNOT READY、原作Gameplay PASS0・strict0。MASTER/T018/他lane/REA/原本/Work/Git/スケジュール設定変更禁止。
[LOAD] PC Local接続成功。既存active.lockはENOENT、terminal sessions0、CPU使用率n/a（低負荷確証なし）。Ghidra/Java起動・再逆解析なし。
[NEXT] PC最新のB T012/T013と間接dispatch関係を通常の許可済み独立検索で確認する。ただし拒否されたSQL操作や証拠を再実行しない。slot2-5実callerとbyte+0x210の後続writerはVERIFYで維持。T011経験値/死亡、T012最終damage/MP、T013最終target、T024 AI時間、T028士気寿命はOPEN。
