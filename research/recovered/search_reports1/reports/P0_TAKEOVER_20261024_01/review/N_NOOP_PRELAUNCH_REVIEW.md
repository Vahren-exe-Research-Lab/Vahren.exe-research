# N bounded NOOP静的review
研究ID P0_TAKEOVER_20261024_01。EXE SHA E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187、V9 DB SHA 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE。
対象runtime/observe_noop.js・run_noop.pyをread-only review。保存snapshot reviewed_noop_observe.js.txt / reviewed_noop_runner.py.txt。修正・実機操作は親のみ。

確定（静的）: C1 4C2935のeligibleはUnit未更新、開始時owner/pass一致、EBX=E、GameEvent/Scene深度0、開始origin GameEvent>0/Scene0/VMreturn433620で制限。seq1かつholdDoneで一回のみ。UUID eventはauto-reset、initial unsignaled。wait指定500ms。結果apply/native finish呼出なし。
原作識別: disk EXE SHA、copy path一致、対象process image path、ia32、フック各8byte校正（ASLR relocation byte除外）。PIDだけで原作へattachしない。owned spawnの準備失敗時のみkillし、user attach processはkillしない。
計測: before/after state+roster+task counter digest、tick/Unit counter、wait result、native_result_applied=falseを記録。source書込みnewline LF明示。ready/error待ち5秒。

## 未解決・注意
1. cleanup RPCはholdEventを無条件closeする。NativeFunction待機中に別RPCが実行できる場合、STOP→cleanupがWaitForSingleObject中のhandleを閉じ得る。未実測の終了競合候補。親へwaitInProgress+deferまたはresume受領後cleanupを提案済み。通常の戦闘終了後STOPとは区別する。
2. elapsed_msはsnapshot準備/後処理を含まない。wait指定500msをcallback全体の最大停止500msと呼べない。JSON/roster/hash/sendの負担とスケジューラ遅延は別測定。
3. holdDone=true以降の例外（roster全体のvec等）はresume receipt欠落を起こす。Frida errorを失敗扱いし、そのrunをPASSにしない。個別Unitのunavailableはsafeで保持されるためdigest一致だけでは完全captureにならない。
4. sampled_state_equalは列挙した範囲の同値。全writer停止・全ゲーム状態停止・RNG停止・frame/timer全部停止の証明ではない。Unit hookは最初の1回のみだが0→1検知には使える。
5. tokenはside/indexの診断ID。generation unverified表記は妥当。Unit+1C8は実測でaliasし一意IDではない。完全G1やresult mappingへ昇格禁止。
6. EFLAGSnull、callback内FS0、C1 caller slot計測汚染は前receipt同様未解決。stack relocationの全面安全証明ではない。
7. world_return_taskはGameEvent onLeaveでmode1/active0観測に限定。戦略の全effect/永続SAVE commit完了は別契約。
8. runnerのimage query handle未closeは小さいresource leak。native applyや原作誤attachの根拠にはならない。

## 実機receiptの合格条件（subsetのみ）
同一run/seq/UUIDのrequest/resumeとworker receipt、digest照合、wait成功0（timeout258は失敗として別記録）、前後sample完全読取かつ一致、ticksBefore=After=0・unitsBefore=After=0、後続Unit/tickと自然finish/世界復帰、Frida/controller errorなしを個別確認する。worker ackだけ、wait成功だけ、digest一致だけでPASSにしない。
静的reviewは実行成功・安全停止・G2完全PASSではない。停止不能/結果apply検証は今回のscope外。
再開地点: snapshot2本とN_NOOP_READBACK.jsonを照合し、親による修正後snapshotを別revisionで再確認。その後新NOOP runの固定prefixを独立監査する。
