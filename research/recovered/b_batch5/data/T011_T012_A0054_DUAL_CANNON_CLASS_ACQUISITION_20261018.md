# B-20261018-1328-01｜a0054の二種砲撃Skill同一Class直接指定（T011主／T012参照）
[TYPE/BASE] 2026-10-18 13時台JST。STATIC ORIGINAL SOURCE CROSS-KIND ACQUISITION。原作同梱EXE既保存SHA256=e8dac301050c8e630d7e0ce93aeefd95e641207d9c0576017f62ba46a8767187（今回EXE直接解析0）。
[SOURCE-CLASS] 正規化 20_クラス/1919_その他.dat L895-906: class a0054:a005 は level=70、change=@、skill=sp_cannon,b_cannon,seiretsu,c_at3 と二つの別Skill IDを同一直接skill行に列記する。
[SOURCE-PARENT/REACHABILITY] 正規化 20_クラス/00_汎用兵科.dat L359-418: class a005:base は skill=tuyo_cannon,boost_a005,seiretsu,c_at1、change=a0052*15; a0052:a005 は change=a0053*25、a0053:a005 は change=@。a0054への通常change辺をこの列では確認できない。a0054親辺とchange辺は別。
[SOURCE-SKILLS/PRIOR] 既公式B-20261018-1214-01: skill b_cannon:sk_ms の raw gun_delay=cannon*4 (F10)、skill sp_cannon:b_cannon の raw gun_delay=cannon*6 (C_必殺)。同一raw delay名と4対6は旧証拠であり新READY再計数しない。
[NEW FACT] 旧B1214はUnit nikuojaがpuddingを直接保有する原文まで。今回の独立増分は原作Class a0054が b_cannon と sp_cannon を同一skill宣言で直接指定すること、およびa005→a0052→a0053の通常change列からa0054合法到達が証明されない境界。
[NEGATIVE SCOPE] 20_クラス/各DATを文字列検索した限りpuddingの直接名は0、10_ユニット/*.datでa0054文字列は0。ただし検索範囲外のevent/召喚/保存状態や暗黙skill伝播までは否定しない。
[NATIVE SAVED XREF ONLY] 既B資料 VA0x59C1BA..0x59C253 Skill数値・文字列field（+210/+214）／VA0x57BEC3→0x4C1200 Unit+1E53C keyed処理は旧参照のみ。raw gun_delay→compiled key/timer対応、Class.skill→実Unit技能集合、同一Unitでの両発動は新規証明なし。
[REIMPLEMENT] {classId,parentClass,changeTarget,rawDirectSkill[],skillId,parentSkill,gunDelayRawKey,rawMultiplier}を別保持。a0054の二skill宣言を片方で上書きせず、原文の通常changeに存在しないa0053→a0054を自動生成しない。
[VERIFY] a0054のゲーム内合法取得・実Unit instance/effective保有、同時表示/使用、cannonキーの実効runtime共有、待機4/6、射撃latch Unit+1E560、方向+18688、MP fallback、0x4E7ED0/0x580280、最終発射・対象HP/RNGは未検証。
[GOLDEN DESIGNED NOT RUN] 旧原作UIでa0054実在Unitが合法に出撃し両技能を保持したことを可視確認できた場合のみ、b_cannon→sp_cannon・逆順・再使用時刻/MP/HP/可視弾/次tickを旧新同EXE/DAT/SAVE/map/input/capture SHA・seedで比較。取得不可ならfixture INELIGIBLE、別合法caseを探索。旧Gameplay PASS0／strict MATCH0。
[DEDUP/READY] B-20261018-1214-01に統合済のraw技能/key/nikuojaは再READY0。今回SOURCE新項目はa0054 direct double-acquisition と合法change boundaryのみ。detail/T011/T012/HANDOFFの4点独立readback成功後のみB OWN LIMITED STATIC ORIGINAL SOURCE READY 1件、EのみMASTER統合。
[SAFETY/NEXT] 禁止0x5710C0..571500／0x58021E..580340／拒否済0x4E13F0の新規逆解析や元拒否書込の迂回0。原本ZIP/EXE/SAVE・MASTER/T018/他lane/REA/dev_lab/Work/WRQ/Git/push/設定/automation変更0。