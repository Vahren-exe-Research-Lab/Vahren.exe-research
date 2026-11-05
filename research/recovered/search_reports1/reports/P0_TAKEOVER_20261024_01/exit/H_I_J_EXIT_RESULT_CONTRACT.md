# P0 H/I/J: native終了と最小結果契約
研究ID: P0_TAKEOVER_20261024_01 / 2026-10-24 / 担当 exit_hij。
状態: STATIC PE CHECKED + V9 DECOMP INFERENCE / ORIGINAL RUNTIME NOT TESTED / RESULT WRITER NOT IMPLEMENTED。
EXE SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
V9 SHA256: 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE（親の現物verify PASS通知、および使用V9明示）。
V9専用CLIから関数情報を取得。SQLite ro/immutable/query_only。Ghidra変更、実機attach/start、元EXE/DAT/SAVE/他owner変更なし。

## 既存成果の再利用（新規発見として加算しない）
- BATTLE_FINISH_STAGE6_EXACT_NATIVE_ABI_GATE_20261021.json: ECX Battlefield, EDX War, stack E/result, RET8。
- Stage6 SCRIPT_WIN_OPCODE5_RESOLVED: opcode5 winは004A1302 XOR EDIから004A175C PUSH EDIでraw0。continue(-4)は別switch先。
- BATTLE_SIDE_LIFECYCLE: finishのSide vf+14はPlayer005200A0/Enemy00514C50。
- Stage7 GAMEEVENT_DIRECT_WRITESET と TASK_VM_REENTRY: finishがactiveをclear後、同一GameEvent callback0043360Cで判定し0043361B→004338D0に再入し得る。
- EXP_SUMMON_DEATH_RESEARCH と Stage15 CASUALTY: shared EXP/死亡flag/医療費/RNGはfinish前にも変わる。

## 今回の追加照合
- native_exit_windows.json: 11局所窓の元PE現物命令を独立読取。native_exit_extra.json: V9 exact function rangesを入口として死亡関連writer抽出。
- 00493630のSEH prolog: PUSH -1, PUSH005FC949, FS:[0]保存、cookie、00493665 FS:[0]設定。0049366BでEを[ESP+130]からEBPへ、ECX→EDI、EDX→ESI。
- 004936E4/F1/FEが3Side vf+14、00493746がactive0。00494667のAttackMap count gateより先に実行される。
- 00494855 RET8、00494858 byte result比較→非0は00494F8E。空AttackMapは00494673へ進み通常勝敗枝を通らない。
- 00575152..18DでUnit+8C==0,+1D0!=0,+18614==0を条件にshared=[Unit+1C8]のEXP+16Cと閾値+170を比較。V9疑似CはLv+168と能力更新、0058A400閾値更新を反復する。従ってEXPはfinish前段より前に整合している必要がある。
- 00578970→00588470のALを0057897Bでshared+1B0へ保存。別経路00544B4B/56も同様。+1B0と+1B1は同一flagではない。
- 00575AAC Unit+1867C=1、00575AB3 shared+1B1=1、00575ABC Unit+90=0。HP0だけの書込はこの遷移群やイベントを代替しない。
- 00588DE0 shared+16C補正→00588E34 related-record+174または00588E40 Power+5C減算→alive_per RNG経路。分岐条件付きであり全死者に一律適用とは言えない。
- 攻撃勝利枝の00495A97: record+174加算、00495AA9攻撃Power+5C減算。対象は+77==0,+7A==0,+75!=0に限定される（生のflag語義未確定）。
- 続く00495B23..52は防衛Power+64木から対象Battlefieldキーを削除し、攻撃Power+64木へ挿入する。0041DDB0は木erase helper、00416790はnode作成、00416B90は挿入。占領所属更新と整合するがSpot全writerの網羅ではない。
- 004951A4..D2で対象Battlefield+1C木をclearする枝あり。勝利時の旧部隊処理→受入/報酬→所有木移動の順序を保持する必要がある。
- 00494E4D→00432EE0の文字列引数は元PEでworld。00432EE0はevent/ScriptFuncも扱うためworld要求の観測とScene遷移完了を分離する。

## 最小結果契約（設計、native書込表ではない）
1. result_id、protocol_version、EXE/DAT定義digest、session_id、battle_sequence、entry_epoch/digest、route/caller、attacker/defender/target/援軍identityを必須とする。外部へ生pointerを渡さない。
2. 勝者はattacker/defender、終了理由はannihilation/retreat/time-limit/script-forced/unknown等の意味値で返す。P0許可routeにない理由は拒否。raw0/1を外部APIにしない。自然終了とDAT winのraw0を共通のPlayer勝利にしない。
3. 参加tokenごとにpersistent/transient区分、final戦闘HP/MPが必要なルールならその値、alive/retreated/incapacitated/permanent-lossを別状態で返す。未解決の死亡と未知を0やfalseに潰さない。
4. 経験値はpre-settlement final EXP一方式とする候補。親側が開始EXP・同一record世代・重複tokenを検査し、native growth前に一度だけ準備する。deltaも同時適用しない。即時成長済みか遅延成長かを別policyで固定する。
5. casualty_preprocess_ownerをnativeまたはadapterに固定する。native採用でも00588470を任意ABIで直接呼ぶのは未認可・未検証。adapter採用時はEXP損失・medical費・alive_per・dead_event・+1B0/+1B1・除去の対応すべてが必要。現時点ではこのwriter契約が未完成。
6. P0の狭い初回NOOPは既存recordを変更しない。最初の結果適用試験は全員生存、EXP変化なし、捕獲/変身/召喚/死亡/途中eventなし、合法原作結果と照合できるケースを選ぶ設計。一般結果対応PASSに拡張しない。
7. 捕獲/所属替え/生成・消滅/支援帰還の未知は対応外拒否。外部結果から新しいpersistent Unitを登録しない。
8. 原作finishを戦略settlement唯一ownerにする。Power/Spot所属、報酬、native成長、world/event復帰を外部で再計算しない。外部結果はnativeが消費する戦闘中の事実を供給する役割。
9. bridge apply前にBattlefield/War/AttackMap/3Side/Troop/shared record世代と各元値を再検証。AttackMapをfreeze目的で空にしない。準備した結果の全検査が通るまで原作値を書かない。
10. PREPARED→APPLYING→NATIVE_FINISH→COMMITTEDを同じbattle sequenceで一回だけ進める。workerは要求を渡すだけ、ゲームthread上で所有権を確保する。ACKは単なるIPC受信ではなくcommit完了を意味する。
11. native finishはSEH正常経路を一度だけ完走させる。偽装return、途中RET、activeだけclear、途中世界木の先行書換えをしない。commit前に0043361B等のVM再入を許さない。
12. APPLYING以後に失敗した場合はUNKNOWN/PARTIALとして停止し、finish再実行・結果再送・自動rollbackをしない。深いheap/参照/乱数/eventの全rollbackは未確立。

## 呼出経路
| callsite | raw flag | 戻り後/制限 |
|---|---|---|
|0049303A|1|自然tick。defending Side生存判定の枝。攻撃勝利候補。|
|00493082|1|自然tick。Side state4比較の枝。0049303Aとcauseを分ける。|
|004930A1|0|自然tick。防衛勝利候補。timeout/双方不在等の細分類は実機で確認。|
|004A1764|EDI=0|DAT opcode5 win。native flag0を無条件Player勝利へ変換しない。|
|0040E2B9|EBP==1からSET E|BattleWnd独自context/War pointer。通常mode2とは別ゲート。|
上記意味はStage6既存成果と今回自然3サイトの元命令照合。終わった後だけのflagでは終了原因を復元できない。

## 親の観測DLLに渡す最小pre/post仕様（read-only）
- 共通: battle sequence/entry digest/同一game thread ID/時刻/QPC/callsite、moduleBase+RVA、全GPR/EFLAGS、hook段階。
- finish entry: ESP+0..11の12 bytes（戻り先/E/result DWORD）、ECX/EDX、FS:[0]値。既知５callerの戻り先のみrouteに結びつける。unknown callerは記録のみ。
- E: +1E8630..3B（3 pointers）、+1EEC3C..4B（mode,active等16 bytes）、+1EED1C..2B（field/War header/count16 bytes）、+1EED40..55（22 bytes）、+1EED60..6B（counter/time12 bytes）。一つの巨大窓にまとめない。
- 原作別object: 攻撃/防衛Powerの+5C 4 bytes、+64木headerは根参照と件数を構造validatorで取得。target context+1C木はroot/countを保存。全木rollback可能とは扱わない。
- 各token: Unit+90..97（HP/MP8 bytes）、+1C8..1D7（shared/related/Troop/Side16 bytes）、+1867C..7D（死亡/選択2 bytes）、shared+168..177（Lv/EXP/threshold/金銭16 bytes）、+1B0..1B1（2 bytes）。
- Unit+8C,+18614とshared+74..7A,+C0も成長/費用枝の条件判定用に小窓読取。offset名が未確定のものはrawとして残す。
- onLeave: entryで得たE/Power/token世代を再validateして同窓再読。失効/破棄はUNKNOWNとして記録し、pointerを再dereferenceしない。
- entry ESPからnative正常RET8直後の実ESPは+12（return4+args8）。hookフレームワークが保存するESPの時点差は別途校正。callee-saved EBX/EBP/ESI/EDIとFS:[0]の復元を比較する。EAX/ECX/EDX/EFLAGSは保存義務を勝手に仮定しない。
- pre/postだけでは途中のUnit削除・case分岐・VM/event再入順を証明できない。最小追加イベントは00493746(active clear)、00494667(count gate)、00494858(flag gate)、00495B32/52(所属木移動)、0043360C/1B(callback続行)、00432EE0(world要求)。
- 観測callback内でnative helperを呼ばない。例外を原作SEHへ漏らさず、alloc/I/O/待機/worker返信待ちをcritical pathで行わない。これは設計制約であり実装成功の証拠ではない。

## 未解決と最小実験
H: entry/leave ABI実機、全caller別SEH正常復元、連戦一回性、途中例外rollbackは未検証。
I: HP/MP戦略への実際の持越し、召喚/変身sharedのidentity、死亡+1B0の意味確定、dead_eventの前後関係、casualty直接呼出ABIは未解決。
J: 占領の全Spot/Power alias writer、部隊全転送、外交/イベント/報酬の全副作用は未網羅。報酬額の原作ルールを単独再実装できるとは主張しない。
最小実験1: 観測のみで自然finish 3causeを区別しentry/pre-active-clear/leave/同callback VM/world再入を同battle IDで記録。コード/結果変更なし。
最小実験2: 全員生存NOOPで元値不変・正常復帰を確認。これをHP0/死亡/EXP適用証拠へ流用しない。
最小実験3: XP閾値跨ぎ1名、戦闘不能1名、恒久死亡候補1名を別ケースにし、00588470前後→shared flags→finish前段→世界値を順に捕捉。実機担当は親のみ。
最小実験4: capture済み合法原作結果を複製SAVEで再現し、同一結果をbridgeが一回だけ反映。所属/部隊/EXP/財政/戦略イベントをGolden比較。未実行。
再開地点: 本フォルダ保存query JSONとnative_exit_windows/extra。新規生存/死亡writerを実装する前に00578370/00544790→00588470のABIと戻りAL、Unit除去、dead_event順を原作観測で確定する。
保存/回復: 初回出力先未作成ENOENTは専有exitディレクトリ作成で回復。初回手動disasm窓の一部開始位置は命令途中だったため、最終native_exit.pyで既知境界へ訂正しJSON再生成。初回表示の不正命令は根拠から除外。既存正本変更なし。

