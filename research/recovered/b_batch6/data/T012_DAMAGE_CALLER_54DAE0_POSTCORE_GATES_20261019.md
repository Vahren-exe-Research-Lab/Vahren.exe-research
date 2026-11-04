# B-20261019-0209-01｜T012 0x54DAE0局所damage呼出と後段virtual/flag分離
[SCOPE] B/T012のみ。対象は同梱Vahren.exeの既保存ASM（SHA256 e8dac301050c8e630d7e0ce93aeefd95e641207d9c0576017f62ba46a8767187）。原本EXE新解析・実行なし。
[EVIDENCE] read-only `exe/T012_DAMAGE_CALLER_CONTEXTS.txt` の VA 0x54DAE0..0x54DB56。既T012の通常caller mode gateを再READY化せず、call以後の局所branchに限定。
[FACT 1] 0x54DAE1 は [ESI+0xB0] をEAXへ読み、+0x24Cをsigned 0と比較（0x54DAE7）、負なら0x54DB03へ。非負でも+0x27Cが0なら0x54DB03へ。両gate成立時のみpush EDI、lea EAX,[ESI+0x78]、push EAX、0x54DAFE CALL 0x550E70。
[FACT 2] core呼出の有無と無関係に0x54DB03へ合流し、Skill+0x274 !=0 または byte +0x26F !=0 なら0x54DB25へ分岐。それ以外では0x54DB1B..23にてESI vtable+0x58をpush EDI付きで間接CALL。
[FACT 3] 0x54DB25..3CでSkill byte+0x1CC !=0なら[ESI+0xF8]=1かつ[ESI+0x1A4]=0xF4240。0x54DB46..4FでSkill+0x1C4 ==0なら[ESI+0xF8]=1。0x54DB55..56でret。
[STATIC CONCLUSION] この局所routeではdamage core呼出、後段のvirtual CALL、ESI+0xF8 flag、+0x1A4書込が別々のSkill field gateで制御される。+0xF8=1やvirtual呼出は命中・HP減少・可視弾発生の証明ではない。
[VERIFY] ESI object typeと+0x78 context layout、Skill+0x274/+0x26F/+0x1CC/+0x1C4の正確な意味、virtual+0x58の本体、+0xF8/+0x1A4の外部consumer、54DAFE context+0x0E setter・実Unit/Skill/target identity、戻り値と例外、全RNG順は未確定。
[REIMPLEMENT] gateを `damage-core-invoked`, `virtual-invoked`, `flag-F8-set`, `timer-1A4-set` の別receiptとして保持。攻撃成功、命中、HP変化をいずれかのgateで偽装しない。既B-20261019-0117-01はSAFETY BLOCKED/NOT READYのままでcontext+0x0Eを推測補完しない。
[GOLDEN] 合法旧ゲームの該当Skillと発動が独立に確定した後、同EXE/DAT/SAVE/map/input/capture SHAと時刻・seed可否・対象HP/MP/可視弾/後続tickを採取。内部flagが可視化不能ならUNKNOWN/INELIGIBLE。現時点DESIGNED_NOT_RUN、原作Gameplay PASS0、新旧strict MATCH0。
[DEDUP] T012既存§ str-mode normal gate とB-20261019-0117-01のctx+0x0E分類、E-AUDIT-20261019-0150のcore/flash gateは新証拠に再計数しない。本件増分は54DAE0局所call後の+274/+26F virtual gateと+1CC/+1C4 state gateに限定。
[STATUS] B OWNER LIMITED SAVED ASM CANDIDATE。detail/T012/HANDOFFの独立readback完了までNOT READY。EのみMASTER統合。原本・他owner・REA/dev_lab/Work/Git/push/Remote/設定/automation変更禁止。
