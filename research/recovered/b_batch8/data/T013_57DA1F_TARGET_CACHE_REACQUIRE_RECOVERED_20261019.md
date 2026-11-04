# B-20261019-1317-01｜T013 0x57DA1F 条件付き再探索ゲート（旧オフライン成果のPC正本照合）
[DATE/OWNER/PROVENANCE] 2026-10-19 17時台 JST再照合。T013主・T012参照。対象: 迫真戦記ver0.67同梱Vahren.exe、既記録SHA256 e8dac301050c8e630d7e0ce93aeefd95e641207d9c0576017f62ba46a8767187。原本の新規hash/起動/改変、新REA/Ghidra解析は行わない。
[ORIGIN-ID] 2026-10-19 13時台オフライン候補 B-20261019-1317-01 を維持し、新番号で同じ事実を重複計上しない。元メモ T013_57DA1F_AUX_NULL_REACQUIRE_GUARD_20261019.md は一時sandbox成果でありPC B台帳へ未登録だった。
[DIRECT SAVED-B PROBES] exe/T013_UNIT_OWNER_PROBE.txt と exe/T013_POOL_SEMANTICS_PROBE.txt のVA0x57D9EF..0x57DA4EをLocal Compactで再読。両資料にVA0x57D9F5,57DA07,57DA1F,57DA2C/36/3Cが一致。新しいEXE bytes抽出ではない。
[FACT 1: SIGNED GATE] 0x57D9F5 CMP dword [ECX+0x1EED64],0x64; 0x57D9FC SETLE AL; 0x57DA05 JE 0x57DA42。signed値>100なら本局所CALLをskipし、負値/100は通過する。
[FACT 2: AUX GATE] 0x57DA07 CMP dword [EBP+0x1E580],0; 0x57DA0E JNE 0x57DA42。補助cache非nullならselector 0x514D60はこの地点では呼ばれない。２条件を両方通過したときのみ0x57DA1F CALL0x514D60。
[FACT 3: DISTINCT WRITERS] CALLの結果バッファから0x57DA2C FSTP→Unit+0x1E578（distance）、0x57DA36 MOV→+0x1E574（selected）、0x57DA3C MOV→+0x1E580（aux）。0x57DA42は後続処理へ続き、skipは行動全体の中止を意味しない。
[PREEXISTING CALLEE CONTRACT] 既B所有 exe/T013_TARGET_SELECTOR_PROBE.txt VA0x514E48..0x514F0B と data/T013_AI.md の旧target選択節はprimary/fallback最近接と二出力を書いている。出力が異なるpointerになることは既知で、今回再READYしない。
[CONDITIONAL CROSSJOIN] 0x514D60の局所戻りではselected/auxのnullnessが一致し得るが、他writer後や別フレームまで保証しない。既B/T013 §0x57B887..0x57B88F はsearchCounter<Bかつnearby cache null時に1E580を明示clearせず戻るため、古いaux非nullが残る→本0x57DA07をskipし得る、という条件付きテスト仮説が成立する。二callerの実行順・他writer無し・生存は未確認。
[SEPARATION] 0x57B983も0x514D60を呼ぶ既知の別site。0x57B870と0x57D8B0はcallers関数入口、0x57B983/0x57DA1FはCALL命令VA。cache-nullness、targetの実寿命、実弾/命中/HP/MP/RNG/優先行動、+1EED64の意味はVERIFY。
[REIMPLEMENT] source_callsite、context signed value、aux_before、selected_after、distance_after、aux_after、selector_called、postcondition branchを独立receipt化。cache非nullだけからselectorを必ず実行済みと断定しない。
[GOLDEN-DESIGNED/NOT RUN] 合法原作で100境界・候補の有無・selectedとauxの差分・target消失/refreshを観測可能な条件を先に固定。old/new同EXE/DAT/SAVE/map/input/capture SHA・seed・操作順で可視ターゲット/移動/発射/HP/MP/次tickを比較。内部slotだけしか見えないcaseはINELIGIBLE。旧Gameplay Golden PASS0、strict MATCH0。
[OVERLAP/SAFETY] T013既存primary/fallback、scratch論理clear、grid mode1を新発見として重複登録しない。拒否済0x5710C0..0x571500/0x58021E..0x580340・旧HANDOFF拒否本文は別tool/path/shell/Remoteで迂回しない。
[FILES/STATUS] 本detail、data/T013_AI.md、evidence/LANE_B_HANDOFF.mdの3点独立readbackと最新MASTER cp189/正式586件との重複照合後に限り B OWNER LIMITED SAVED-ASM STATIC READY。Eだけ正式統合。実機PASS0・strict0・Task DONE増0。
[NEXT] +1E580の別writer/clearと0x57DA42以降の実callbackと射撃coreへの因果接続はVERIFY。T012 MP fallback・0x580280下流も別課題。