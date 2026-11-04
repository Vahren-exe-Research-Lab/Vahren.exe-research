# B-20261019-1811-01｜Skill+0x3E8/+0x3EC setter上限・0時fallbackと54E420/54E3F0 consumerの静的接続
[OWNER/TASK] 2026-10-19 18時台JST、T011主・T012参照。限定SAVED-ASM STATIC。旧Gameplay Golden PASS0、新旧strict MATCH0、Task DONE+0。
[ORIGINAL/PROVENANCE] 原本迫真戦記同梱Vahren.exe保存SHA256=e8dac301050c8e630d7e0ce93aeefd95e641207d9c0576017f62ba46a8767187。B保存exe/T011_STRUCTURE_DISPATCH_PROBE.txt lines16444-16519 と exe/T013_SUPPORT_CORE_54E0B0_NATIVE_20261013.txt lines289-329をread-only照合。原本EXE実行・新逆解析0。
[WRITER 3E8] VA0x59EAFB CALL0x4647D0結果node+0x20をVA0x59EB03で[EBP+0x3E8]へstore。VA0x59EB3Dからsigned CMP EAX,0x20 / JLE; >32ならMOV EAX,32し、VA0x59EB62で[EBP+0x3E8]へ再store。負値/0の下限clampはこの局所窓に見えない。
[WRITER 3EC] VA0x59EB68 CALL0x4647D0結果node+0x20をVA0x59EB70で[EBP+0x3EC]へstore。VA0x59EBAA..0x59EBD2はEAX=[EBP+3EC]、比較相手EDI=0（直前VA59EAE4 XOR EDI,EDI以降保存窓で明示変更無し）、等しい時EAX=4、最後に[EBP+3EC]へstore。負値を4へ替える証拠は無し。
[CONSUMER COUNTER] 既B-20261019-0910-01の保存VA0x54E437..0x54E468：Skill候補(ESI+0x88)+3E8>0時、ESI+A4増分をsigned 32bit積(3E8×3EC)と比較し、signed >=なら0へfold。+3E8<=0なら局所更新skip。
[CONSUMER HELPER] 独立VA0x54E3F0..0x54E41DはSkill+3E8>0時、signed IDIV(A4,Skill+3EC)の商からSkill+3F0+24*商のpointerを返す。+3E8<=0ならSkill+3F0を返す。helper実callerは未確定。
[NEW LIMITED CONSEQUENCE] 同一Skill定義/インスタンスがwriter→consumerへ流れる場合、parser側3E8の正値は高々32、3ECの解析値0は4へ置換されるため、その後のhelperの0除算危険を「raw zero入力」に直接帰属させない。writer不経由・実体差・別代入の可能性はVERIFY。3EC負値・signed積overflow・A4初期値・0以外のdivisor・合法Skill到達もVERIFY。
[DEDUP] 旧B-20261019-0910-01はconsumer・A0 effect gate・A4 helperを既正式cp190で統合済み。今回の独立増分はproducer VA59EB03/62/70/BD2の上限32とfallback4およびそのconsumerとの条件付きDATAFLOWのみ。旧E拒否B-20261019-0814-01、B0725 HANDOFF拒否、B-20261019-1317-01 HANDOFF拒否は独立BLOCKEDのまま、再提出なし。
[REIMPLEMENT] raw property key unknown(nullable)、raw parsed3E8、upperClamp32、effective3E8、raw parsed3EC、zeroFallback4、effective3EC、runtime Skill identity、A4 before/after、cycleProduct signed32、helper IDIV result/recordIndex、551490-call-issued、visible HP/MP/resultを別stageとする。原文key・VC static Skill同一性は未確認。
[GOLDEN DESIGN] 合法旧UIで該当Skillの有効parser入力/発動を確認できた場合のみ、3E8=0/1/32/33、3EC=0/1/4/負値の合法設定が成立する範囲で、同旧EXE/DAT/SAVE/map/input/capture SHA・同tickの可視周期/HP/MP/次行動を比較。値を原本改変して作らない。未成立はINELIGIBLE、実機NOT RUN/PASS0。
[VERIFY/NEXT] 0x62554C/0x62555C等保存parser文字列アドレスの人間可読key、VA59EAFB/59EB68所定this Skill identity、3E8/3EC他writer・別instance、+3F0 record source、54E3F0 callsite、flag+48/a0と最終HP/MP/RNGを既保存証拠でさらに検査。
[READY GATE] 本detail＋data/T011_DATA_MODEL.md＋data/T012_BATTLE_CALC.md＋evidence/LANE_B_HANDOFF.mdの同ID 4/4独立readback・owner重複検査を満たす場合のみB限定STATIC READY。EのMASTER統合は別権限。
[SYNTHETIC BOUNDED CHECK / 2026-10-19 18時台] 追加の実行ファイル/原本編集をせず、既保存branchに従う独立メモリ内JSモデルで境界14/14一致：3E8=-1/0/32/33/100、3EC=-1/0/9、counter閾値直前/同値、32clamp周期、3E8<=0 skip、負divisor時の局所signed比較。式の自己整合検証であり原作実機・native runtime PASSではない。ソースファイルとしてのテストは未保存、再実行には同条件の再構築が必要。
