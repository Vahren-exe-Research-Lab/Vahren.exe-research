# 保存済みnative証拠の追加照合：0x57EB40呼出し・負値healの途中終了（2026-10-10）

## 範囲と安全条件

- 根拠は既存Ghidra results＋A/B ownerの保存native TXTのみ。**新規EXE/Ghidra/REA逆コンパイルプロセス0**。過去のSAFETY_REFUSALをshell/Remote/tool変更で迂回しない。原本ZIP/EXEはread-only、A〜E owner data/exe/MASTER/T018は編集しない。REA重点39/48（Wave4未9）のまま。
- MASTER正本は開始時checkpoint69（統合済みREADY119、Task34: DONE9/IN_PROGRESS21/VERIFY4）。後続checkpointが他レーンで進んだ場合はそちらが正本。

## S-EB40-01：同一calleeを引数0/1で使う異なる二つのcaller

- **本体0x57EB40は既存保存済みGhidraの5点エントリに無い**。`runs/20261009T224617297Z/4E7ED0_procedure_callers.json`は`0x57EB40`を第2 callerとして列挙するだけ。callee内部で0x4E7ED0を呼ぶ前提条件・戻り値用途・0/1の意味は確認できていない。
- callsite A: `exe/T013_UNIT_SEARCH_CONSUMERS.txt` 0x57E5A0..0x57E610。+0x1E538 delay<=0後、+0x1E534をglobal unit_search_bdrへ設定→0x57B870 refresh→Unitのvtable[+0x40]に基づく4分岐。**特定分岐**0x57E5D0 `PUSH 0; PUSH ESI(Unit); CALL 0x57EB40`。4エントリjump-tableの値はこの保存断片に無いため「action type=2」と確定しない。
- callsite A直後0x57E5D8 JMP0x57E5EC、`TEST AL,AL; JNE 0x57E610`。AL!=0では同branchからの後段をskip。AL==0で0x57E5F0 `CALL 0x57DF90`（自然回復）、0x57E5F5..0x57E5FF `CALL 0x4E13F0(Unit,0x627C44,0,0)`へ進む。`0x4E13F0`のゲーム意味とAL==0になる条件はVERIFY。
- callsite B: `exe/T013_1D0_GLOBAL_PROBE.txt` 0x4B618C..0x4B61B5。先行の比較0x4B618Fの結果が特定側へ進んだ場合、stack byte `[EBP-0x76]` 非zeroなら呼出へ直行。byteが0の場合はcandidate `+0x1867C` が0でなければ0x4B6245へskip。許可時0x4B61A4 `PUSH 1; PUSH candidate`, 0x4B61A7 `MOV EAX,[EBP-0x88]`, 0x4B61AD `CALL 0x57EB40`。
- callsite Bの直後は0x4B61B2 `INC EDI` →0x4B61B3 `JMP 0x4B6170`。この**局所caller**はALをTEST/CMPしない（callee内部でAL/ほか戻りを使うかは不明）。0x4B618F以前のcompare条件と0x4B6245 branch最終効果はサンプル境界外につきVERIFY。
- **互換性への影響**：この2callerのmode0/1引数差、delay→refresh→dispatch順、AL非zeroなら自然回復/後続callをskipする局所動作、B側ではALを使わない点を別々の契約にする。0x57EB40自体の完全動作の復元とは数えない。
- `dev_lab/eb40_caller_contract.py`と専用合成テスト6件PASS。上位gameplay golden0。

## S-HEAL-02：負値healの第一阻止と第二阻止で候補ループ制御が異なる

- 保存native `exe/T012_HEAL_ATTR_PROBE.txt` の0x551490..0x551E4A、B owner `data/T012_BATTLE_CALC.md` §43〜§46をread-only交差照合。現owner文書で既に確認済みの仕様であるため**A/B新READY発見として二重登録しない**。DEV側での未実装契約を機能に変換した。
- 入口skill+0x230 <100なら0x5514E4 1回CRT draw→百分率相当へ整数化→roll>=chanceなら0x551E23早期ret。>=100ならその乱数消費なし。これは候補ごとではなく**当該core callにつき1回**。
- candidateから得たamountが非負なら0x55177C/0x55177Eにより負値専用RNG/resistanceをskipし、後続のeffectを処理する。負値ではUnit+0x13Cのresistance mapからr取得、未存在は5、0..10へclamp。
- 第一阻止：0x551832 1回CRT rand、0x551850~57は整数化後の`roll<r*r`なら **0x551DF5**の全関数cleanupへ早期ジャンプ。通常次候補tail0x551D40へ進まないため、現候補だけでなく**未処理の後続候補も中止**する。
- 第一を通過した時だけ0x551893/0x5518E5の**独立2 rand**を消費してsource/target dext scoreを比較。0x551919 SUB sourceScore−targetScore、0x55191B CMP 0xA、0x55191E JLE 0x551D40は差<=10（等号含む）なら現候補を飛ばして**次候補へ進む**。差>10のときだけstat mutation側へ。
- 第一阻止のrand消費は1回、第2阻止を判定するには負値候補あたり3回。加えてcore共通chance RNGが1回ある場合がある。randの他consumer/helperやnative x87 roundを本数へ推測加算しない。
- r値によるdecomposition係数はnative初期表11要素(3,2,1.75,1.5,1.2,1,5/6,2/3,4/7,0.5,1/3)。実際の負値healはr=0なら係数10、r=10なら0、r=1..9はtable slot。0x45B3E1..0x45B43Bは`damage_consti`非ゼロ値を百分率×0.01にして該当slotを上書きする（最大11要素、0なら従前値維持）。定数表とruntime overrideを混同しない。
- 新規`dev_lab/negative_heal_flow_subset.py`: skill共通chance/候補ごとの負値/第1全中断/第2単一skip/draw順序/係数overrideの**合成契約**を実装し、専用10件PASS。x87 scoreとnative 0x5D1B80整数化はCALLBACK注入・ゲームeffect本体未実装と明示。

## 未解決事項

- 0x57EB40本体のnative Ghidra証拠は未取得。Mode0/1が何を変更するか・0x4E7ED0へどう入るか・AL返却規則はVERIFY。いずれも他shell/processで禁止された逆解析を再試行しない。
- 負値healの確率端点とnative score、Unit+0x13C抵抗key選択、複数Unit本家実機テスト、その他属性のstat mutationはVERIFY。TARGET OBSERVED actual 0 / new strict MATCH 0。
- 次に読むなら、0x4B61ADへ至る上位caller種別と、合法な人手観測で可視化できる負値heal/golden候補（ユーザーはPCに触れないため手作業依頼は保留）。


## このrunの全回帰チェック（同日17時台JST）

- Desktop Commander Localで `dev_lab/run_checks.ps1` を一度フル実行し、process PID28000が **exit0**、`Ran 172 tests` / `OK`、末尾 `DEV_LAB_ALL_CHECKS_PASSED` を返した。内訳は既存156＋今回16（EB40 caller6／negative heal10）。
- map151、atlas513、context204、script590、parent refs21,214、event/scenario sampled516 body、既存合成1v1/2v2 VM・AI traceを再照合。旧EXEの実ゲームOBSERVED golden=0、strict MATCH=0。
- `dev_lab/README.md`・`docs/IMPLEMENTATION_PLAN.md`・`docs/DEVLAB_HANDOFF_20261010_EB40_HEAL_172.md` の保存とreadbackを確認。REA優先関数5点取得は39/48据置（新規0）。
