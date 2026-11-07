# RTS scenario / wave / settlement — curated D/T030, A/T010 crosswalk

Scope: original normalized RTS DAT STATIC-SCRIPT; saved native handler STATIC; actual game effects VERIFY. Gameplay Golden PASS=0, strict MATCH=0, no formal READY upgrade.
Owner D/T030; primary data/T030_RTS_MODE.md; clock cross-reference data/T010_EVENT_SCHEDULER.md. Never consume denied/incomplete evidence/T030_RTS_PRODUCTION_GRAPH.tsv.
Verified normalized RTSscenario.dat SHA256 D73AD85D7AE4DF0DF170AD5AC532386D1982BE82A041A3FCE2C1F3DEBD1F0BEB.

## 1. Distinct RTS scenario and battle identity
- Scenario rts uses separate world and battle blocks. World power IDs rtsp1/rtsp2/rtsp3 are not interchangeable with battle Unit IDs rtsplayer1..4; a same numeric suffix is not identity.
- 2v2 script tests isAllDead(rtsplayer2) for win, isAllDead(rtsplayer1) for loss, and getLimit()==0 for timeout; rtsplayer3/4 are not explicitly joined to those predicates. The helper reports whether eligible candidates exist; the script isAllDead result also depends on mode and a raw zero/nonzero gate. An empty eligible set does not imply a universal false result (see §5). Actual 2v2 team interpretation remains VERIFY.
- Distinct branches execute modal dialog, then set(lose,1), wait(15), win(), with two dialogs before timeout's set. Common native win result flag does not itself encode user-visible win/loss. World then may terminate on lose==1; Yield/tick ordering is not yet Golden.

## 2. Clocks and wave commands
- getTime is elapsed/resettable battle time, while getLimit is a separate remaining counter. A limit of 6000 cannot be treated as 6000 getTime ticks; D/T030 and A/T010 document separate update cadence.
- Waves use independent if(getTime()>=N), not else-if. 7000/7300, 15000/15300, 20000/20300 include active then sleep; later 25000/25300 through 55000/55300 often call active at BOTH thresholds. 2v2 has a Samson-infantry re-activation at 20300. Do not normalize away command order.
- activeTroop and sleepTroop use a native shared command route writing a target-object +0x70 byte as 1/0; exact effective movement/spawn behavior is VERIFY.

## 3. Difficulty, choices and resource graph boundaries
- The initial HQ starts with script-defined large MP and distinct skill/building/summon stages. An RTS skill and class can have the SAME name; collapsing namespaces can route a build command to the wrong object.
- rtsdiff is called for both 1v1 and 2v2. Difficulty 2/3/4 branches also issue skill commands for battle IDs rtsplayer3/4 even when 1v1 has no proven corresponding in-scene Unit. hqgenenone has references but no confirmed definition in the normalized RTS corpus; keep it as missing/VERIFY rather than fabricating a skill.
- Samson unlocking uses different gates for manual choice, player skill and random-selection list; do not assume the 1v1/2v2 random pool excludes Samson because a manual menu hides him. No uniform 1/9 probability claim without native RNG proof.
- RTS easy/new have distinct declared HQ stats and CPU next2 lists, including duplicates. A declaration does not prove current new-game reachability or native spawn counts.

## 4. Testing and corrections
- Verification priorities: 1v1/2v2 unit identity and side/team resolution, isAllDead conditional empty-side results and winner conditions, actual wave-order effects at each threshold, distinct getTime/getLimit phases, modal Yield, HQ MP/regen, addSkill missing targets and code-defined difficulty gates.
- Use original unmodified EXE/DAT/SAVE/MAP/input/RNG comparison for Golden. No source-only observation or a synthetic trace can establish original gameplay strict MATCH. Never import the incomplete refused production graph.
- Sources: data/T030_RTS_MODE.md §§1–17, normalized RTSscenario.dat and RTSbuilding.dat, data/T010_EVENT_SCHEDULER.md clock sections, exe/T006_TARGET_DISPATCH.md. The named D-owner file is the evidence history and this page is just the low-cost AI entrypoint.


## 5. isAllDeadの適格候補と最終boolを分ける（2026-11-05 訂正）

旧要約の「empty candidatesならfalse」は一般化し過ぎていた。[T030の後日記録633–640行](research/recovered/principal_models1/reports/data/T030_RTS_MODE.md?plain=1#L633-L640)では、`0x514C80` のAL1は「走査対象の適格候補なし」を表すが、命令の最終boolは別の条件付きとしている。

- helperはside+0x48..+0x4Cの範囲で候補を探し、適格候補が見つかればAL0、なければAL1（547–550行）。空の配列だけを意味せず、全候補が適格条件から外れる場合も区別する。
- AL1の後、mode==1ならDWORD[0x8B8F1C]、それ以外はDWORD[engine+0x1EED68]のゼロ判定を局所returnへ返す（636行）。旧文中の「pointer」という型推定は、局所コードがdereferenceしないraw DWORD gate以上には確定しない。
- 通常setupの0x49273E到達後に後続writerがなく、mode==2、対象outerの解決成功、helper AL1なら、初期化された+0x1EED68=0によりこの局所returnはbool1になる（637行）。この条件例から「適格候補ゼロなら常にtrue」とも一般化しない。
- helper AL0または対象outer未解決は共通tailへ分岐し、保存範囲では最終bool未確定。2v2のrtsplayer1..4の実owner・具体型・別poolの反映、実勝敗は未確認（638–640行および727–731行）。

主根拠：固定保存版 `research/recovered/principal_models1/reports/data/T030_RTS_MODE.md`、SHA256 `1e462ef63681ab1a57425c6b686af4534eb2a0e2f9a4180c8bdb6a167ffce0b7`、633–640行（D-20261013-1615-02）。補助547–550行・727–731行。[helperの関数ページ](reference/symbols/00514C80.md)と[訂正一覧](reference/CORRECTIONS.md)の `CORRECTION-RTS-EMPTY-SIDE-NOT-ALWAYS-FALSE` へ接続する。記述は保存済み静的報告の確認範囲で、今回の原作再解析・実機Golden・新しいREADYはない。
