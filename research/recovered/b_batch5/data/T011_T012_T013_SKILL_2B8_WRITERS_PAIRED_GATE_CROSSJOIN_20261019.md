# B-20261019-0520-01｜Skill候補+0x2B8 の既保存writer・+0x2B9対gate・座標consumer静的接続
[OWNER/DATE] 2026-10-19 05時台 JST。T011/T012主、T013参照。限定SAVED ASM STATIC。原作同梱Vahren.exe SHA256=e8dac301050c8e630d7e0ce93aeefd95e641207d9c0576017f62ba46a8767187。原本EXE未実行・未変更・新逆解析0。
[SAVED PRIMARY] read-only exe/T011_STRUCTURE_DISPATCH_PROBE.txt VA0x59AF4F..0x59AF69、0x59B024..0x59B050、0x59F74A..0x59F76E。exe/T013_FLAG8C_WRITES.txt VA0x5490A8..0x5490D0、0x581214..0x58123C。exe/T012_DAMAGE_CALLER_CONTEXTS.txt VA0x54DA16..0x54DA2C/0x54DA97..0x54DAD2。
[FACT WRITER-A] VA59AF4F CALL4647D0、59AF64 CALL40B200の結果ALを59AF69でbyte [EBP+0x2B8]へ書く。CALLのproperty文字列・返値意味は未読解。
[FACT WRITER-B] VA59B024でbyte [EBP+0x2B9]をcmp0し、非0ならAL=1、0ならAL=[EBP+0x2B8]を選択し、59B04Aで[EBP+0x2B8]へ格納。途中のparser/property lookupと+2B9設定元は未確認。
[FACT WRITER-C] VA59F75E CALL464290の戻りALを59F763で検査し、AL==0の枝だけ59F767でbyte [EBP+0x2B8]=1。これがどのSkill/propertyやmodeの値かはVERIFY。
[FACT OTHER GATES] VA5490C0/5490C9では[ESI+0x2B8]/[ESI+0x2B9]を順に比較し、VA58122C/581235では[EBX+0x2B8]/[EBX+0x2B9]を比較。+0x3B1とstack flagの先行gateあり、後段作用・対象優先は未確定。
[PREVIOUS VERIFIED CONSUMER] 既正式 B-20261019-0408-01 のVA54DA1C/54DA9DではESI+B0経由のbyte +0x2B8が矩形の第2座標中点化・CALL4C5EF0/4C60F0分岐を制御。今回この既存消費処理を再度新証拠として加算しない。
[STATIC NOVELTY] 保存済み別証拠窓の同一offsetについて「+2B8への3箇所の条件付きwriter」「+2B9と組になった2箇所のgate」を追加して整理。単一の正しい呼出元・同一物理Skill instance到達・実効値は未証明で、offset同一性以上のruntime接続はVERIFY。
[VERIFY] +0x2B8/+0x2B9の生property名、初期値、+2B9 producer、EBP/ESI/EBXが同じ型か、4647D0/40B200/464290戻りと条件意味、実Script Skillとの連結、0x5490D2/0x58123E以降の作用、対象・MP/HP・弾/衝突/RNG・次tickは未知。+2B8=1を「発射成功」や「target優先」とみなさない。
[REIMPLEMENT] rawKey(nullable), parsedValue(nullable), flag2B9(nullable), writerSite/条件、compiledField2B8(nullable)、gateSite、geometry branch、effect/resultを別stage。writer間の適用順・優先順位を証明なく実装しない。
[DEDUP] B-20261019-0408-01 cp188正式、B-0209-01 E統合BLOCKED、B-0210-02/B-0117-01/B-20261018-1813-01 owner BLOCKEDは独立。前者のhelper/中点と後者のdamage/580280/ctxは再READY計上せず、拒否本文・禁止0x5710C0..0x571500は触れない。
[GOLDEN] 原作合法UIで問題のSkill保有・発動と2B8=0/非0の対照が成立し、旧原本EXE/DAT/SAVE/map/input/capture SHAと入力時刻、可視座標・弾・target/HP/MP/次tickを採取可能になった場合のみold/new比較。内部字段しかないケースINELIGIBLE。現DESIGNED_NOT_RUN、原作Gameplay PASS0、strict MATCH0、Task DONE+0。
[READY] detail/T011/T012/T013/B HANDOFF の独立5/5読み戻しと最終READY記録保存後だけB限定SAVED ASM STATIC READY。MASTER cp188・公式585(A115/B218/C136/D116)はE管理・本回加算0。
[SAFETY] 原本・MASTER/T018/他lane/REA/dev_lab/Work/WRQ/Git/push/Remote/設定/automation不変更。Local PID23860入力待ち非介入、CPU率n/a低負荷未確認。