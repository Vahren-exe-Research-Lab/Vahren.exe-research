# B-20261017-1517-01｜T012/T011 MP回復healと列車砲missileの同一raw gun_delayキー（限定SOURCE）
[DATE/TYPE] 2026-10-17 15時台JST。T012主/T011参照。迫真0.67 CORE正規化DATの原文をLocal Compact read-only確認したSOURCE-LEXICAL限定命題。原本EXE起動・改変・新逆解析0。
[ORIGINAL] data/normalized/hakushin067_core/a_default/script/30_スキル/F13_heal_support.dat。
[RAW-A] L176 skill b_mp（親指定なし）: L186 attr=mp、L190 func=heal、L197 mp=-1、L199 gun_delay=b_mp*1。自己用派生b_mp_faroff:b_mpは明示gun_delay無し（継承実効値VERIFY）。
[RAW-B] 同F13 L279 skill s_mp（親指定なし）: L289 attr=mp、L293 func=heal、L296 range=0、L299 str=fix*20、L300 mp=-1、L302 gun_delay=b_mp*3。
[RAW-C] 同F13 L2038 skill tadora_charge:sk_ms: L2043 mp=-100、L2044 check=9999、L2047 gun_delay=b_mp*1、L2059 attr=mp、L2060 func=missile。親sk_msからのeffective fieldはVERIFY。
[LEGAL-RAW CLASS] 20_クラス/24_26_ONDISK_二軍_原理.dat L774前後 class a265:base は L780 skill=tadora_cannon,tadora_charge,...；class a2652:a265 L814、a2653:a265 L827にもそれぞれ直接tadora_charge宣言。changeはa265→a2652*15、a2652→a2653*25で、親辺とchange辺は別。
[SUMMON-RAW] 30_スキル/F20_summon.dat L11989-12011：class tadora_s:a265、tadora2_s:a2652、tadora3_s:a2653が各skill=tadora_cannon,tadora_charge,...を明示。上流add2=tadora_s,tadora2_s,tadora3_sは別宣言であり実召喚/発火はVERIFY。
[CONFIRMED SCOPE] 異なるfunc（healとmissile）・異なるmp宣言（-1と-100）にもかかわらず、同一文字列キーb_mpを各技能のgun_delayで直接参照する。b_mpとtadora_chargeのraw倍率1、s_mpの倍率3。F13の既知alias census(B-20261017-1313-01)自体は新規計上しない。
[EXE VA/XREF EXISTING ONLY] B保存VA0x59C1BA..0x59C253（関連skill keyed fields）、0x57BEC3→0x4C1200、0x57BEDB付近のSkill+0x210/+0x214・Unit+0x1E53Cは先行証拠の参照だけ。gun_delay raw producer→compiled field接続は未確定で今回の新native断定無し。
[BOUNDARY VERIFY] 語彙上の共有キー≠runtime共有クールダウン。異Unitのkey storage、負MPの意味（消費/回復/例外）、ミサイル実副作用・MP fallback・射撃ラッチ、各classでのeffective取得、Task/弾/HP/MP/実技能使用、同戦場での2技能取得はいずれもVERIFY。
[REIMPLEMENT] skill本体ID、親edge、func、attr、mp raw、gun_delay参照keyと倍率、Class直接skill/parent/change/召喚Classを独立保持。func=missileからgun_delayのキーをtadora_chargeへ自動置換しない。mp=-100を単なる通常正costへ丸めない。
[GOLDEN DESIGNED NOT RUN] 合法a265系列/召喚tadora_s系列の可視tadora_charge取得・発動/MP・時間、別合法b_mp/s_mp保有者の可視待機を原作EXE/DAT/SAVE/Input/capture SHAとseed条件が揃った場合に旧新比較。両技能同Unit保有やdelay共有は合法性を先に証明、不可視keyのみINELIGIBLE。原作Gameplay PASS0/new-old strict MATCH0、DONE+0。
[DEDUP] B-20261017-1313-01はheal3のb_heal alias、B-20261017-1413-01はそのUnit/Class取得元。今回の新増分はb_mp系heal二種×missile tadora_charge のraw同名keyとa265系列取得元。旧B-20261017-1216-01 NOT READY、E cp169旧拒否別件は一切再登録/迂回しない。
[NEXT] 保存済み許可x86内gun_delay native field対応とキー単位管理を証拠がある範囲でのみ確認。次点T012射撃latch/Unit+0x18688/0x4E7ED0/攻撃HP、T013最終target/Skill+A18/A1C、T011実効親子。未判明ならVERIFY維持。
[STATUS BEFORE READBACK] DETAIL SAVED候補、OWNER T012/T011 + HANDOFF個別読み戻し後のみB OWN LIMITED STATIC SOURCE READY。EのみMASTER/T018統合、旧Gameplay PASS0/strict MATCH0。