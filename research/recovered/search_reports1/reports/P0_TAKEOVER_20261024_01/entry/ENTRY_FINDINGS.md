# P0 入口・初期化・名簿・MAP調査
研究ID: P0_TAKEOVER_20261024_01 / 担当 A・B・C・F・G / 2026-10-24 JST
EXE SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
V9 DB SHA256: 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE
状態: STATIC REVALIDATED / DESIGN CANDIDATES / LIVE NOT RUN / NOT HANDOFF READY
由来: V9専用CLIのみのmode=ro/immutable=1検索、既存Stage14/16/17資料、SHA一致targets/hakushin067_Vahren.exeコピーのread-only機械語確認。V9現物verifyは親担当からPASS受領。元EXE/DAT/SAVE、既存DB、他レーン、MASTER、実プロセスに変更なし。
既知知識の再照合: Fade分岐、active後3Side callback、VM後続、非原子的RAWという既存結論を再発見扱いしない。本回の増分は経路一覧と入口ABIの具体化・現在の原本バイト照合・同期受入条件の統合である。

## A・B: 記録済み直接経路と入口ABI
| 対象 | 入力と復帰（静的確定） | 根拠 |
|---|---|---|
| 004922A0 request | entry ESP+4=GameEvent E、ESP+8の低byte=route。RET8。通常thiscallではない | 4922D5/DC/E3、4926FE、4921CB/CD、522295/97・5222A7/AA |
| 0048D6A0 Scene builder | ECX=G+504=E、通常RET。V9の__fastcall表記だけでEDX入力を追加しない | 4B99C7 LEA ECX、4B99CD CALL、48EA5A RET |
| 00492890 activation | ESI=Eという隠れた入力、entry ESP+4=ScriptBattle。RET4 | 433E57 PUSH EDI、433E58 CALL、4928C1/C7、492D70 |
| 0040D0A0 BattleWnd | EAX=&(E+1EED20)、ECX=&(E+1EED30)、DL=分岐byte、ESP+4=field pointer。RET4 | 491FEC–491FFB、492464–492473、40D0A7–D0C6、40D1C8/D1F0/D213 |

4922A0へのV9直接CALLは3件: 4921CD (caller 491870)、522297/5222AA (caller 521D90)。後者はPlayer object+194からEを取得、522297側はEBX値をstackへ、5222AA側は1を渡す。522297側の0という意味はEBX初期化まで追う必要があり、本報告では生値として保持する。
requestはE+1EED43へrouteを書き、0ならFadeOutSheet経由Scene selector=2、非0なら432EE0→40D0A0。Scene2の直接CALLは4B99CDのみ、activation直接CALLは433E58のみ（V9に記録された参照範囲内）。
重要: 40D0A0へは計5個の直接CALL。491870内の491FFB(DL1)、49204F(DL0)、492143(DL0)、4921F7(DL0)は4922A0を経由しない。492473(DL1)だけが4922A0内。request hook一箇所で全戦闘を捕捉したとしない。
491FFBの枝はfield+24==0かつ(field+90==0またはE+1EED44指示先+48/+4C同値)を含む。49204FはE+1EED56、469170結果、global683748の分岐。492143はE+1EED54/55とglobal683749の分岐。4921F7はglobal683748や*(E+10)+Bの分岐。これらのUI意味・CPU/自動戦ラベルは未検証。
全経路網羅の上限: 記録済み直接CALLについて列挙済み。未認識コード・間接呼出・runtime生成・未知のscript要求まで完全網羅を主張しない。呼出元、route/DL、要求世代、同一threadを同時記録する。

## C: 完成境界はactive書込みより後
既知命令を131/131再照合。492960 mode=2、49296A active=1の後、条件付き49D6A0、Player vf+0C(492A4E)、Enemy vf+0C(492A5B)、Enemy vf+0C(492A68)が続く。Player実体51EF80は447810と47BB50によるTroop並べ替えを呼ぶ。Enemy基底447810はRNGやSide状態を更新する。active=1時点の名簿順・RNGは完成保証がない。
492A6Aは3callback終了直後だが、その後にUI ownerの書込み、dungeon/event分岐、564160、cleanupがある。初期化関数全体の完了候補は492D53以降/492D70正常returnであり、3callback後だけより強い。ただしsafe holdではない。
48D6A0はMAP構築→参加Unit構築(48E4CC→4F6540等)→4342A0/4DDCF0→48F080→条件付き48E9F0→4338D0(VM)→FadeIn構築→48EA5A RETの順を含む。activationはScene builderからのVM内でも起き得るため、433E58から戻っただけでScene構築全体が終わったとは言えない。

## F: 同期名簿の最小読取仕様（設計・実機未検証）
E=G+504。3SideはE+1E8630/34/38のpointer32。class slotはPlayer/Enemy/Enemyだが、slot番号だけで攻撃/防御を決めない。48D6A0の+1EED44/48指示先+0Cの分岐でPower割当が変わる。E+1EED4C防御Power、+1EED50攻撃Powerとの実照合を別に保持する。
Side期待vtable preferred VA=639B08,638B60,638B60（module baseで再配置）。Unit配列headerはSide+48/+4C/+50、Troop配列headerは+38/+3C/+40。各要素は4byte pointer。Troop期待vtable639A30、member配列header+0C/+10/+14。Troop+8はraw owner_refに留める。
Unit+1C8=shared record、+1D0=Troop、+1D4=Side候補、+1CCはleader-linked recordでsummonerと断定しない。Unit pointerとshared record pointerの一対一性・世代は未証明。生ポインタを外部の恒久IDに使わない。
stable token案=(session,battle_sequence,snapshot_epoch,side_slot,unit_ordinal,generation)と原プロセス内の対応表。record識別digestとdefinition IDは取得できたものだけ付与。pointer再利用や同definitionの複数Unitを誤結合しない。token案は設計であって原作IDではない。
Unit raw windows: +90..E3 (84 bytes: HP90/MP94/maxDC/E0含む)、+1C7..1D7 (17 bytes)、+214..233 (32 bytes: logical X214/Y218、別座標220/224)。計133byteだがskill・cooldown・全能力を含まず、完全戦闘packetとはしない。
受入検査: header単調性begin<=end<=cap、4byte整列、予算内、null/重複、vtable、3Side間重複、Troop membership↔Side Unit vector、Unit+1D0逆参照を診断。矛盾を正規化しない。既存RAW05にはTroopにだけいる3memberという証拠があるため、片方を自動削除・補完しない。
各配列の順序とraw pointerを保ったsnapshotを同一game-thread停止境界で読む。読取前後counter一致は必要な補助情報にすぎず、原子的取得の証明にはならない。既存readerの最大2048Task超過失敗を名簿取得失敗へ波及させない。
## G: MAP・初期配置
map manager M=G+1EF570は埋込オブジェクトである（48D801 LEA）。まずowner=ptr32(M+E8)を読み、期待Gと同じであることを確認。grid=ptr32(owner+90)でありM+90を辿らない。
grid+6C/+70はwidth/height、+60/+64/+68は各row tableへのpointer32。行は非連続で各行pointerを個別に読む。セル幅は1/4/4byte。layer+64の0x80000008 sentinelを0へ補正しない。+68のpointer様セルの参照payloadは別収集。coarse grid+7C、寸法+74/+78も別。
48E180→4F0BE0のMAPロード枝、4F08E0の生成枝を区別する。ファイルhashはruntime地形・オブジェクト層を証明しない。生成/ファイル/メモリ入力、dimensions、layer digest、Unit論理座標を同じepochで保持する。
Scene builderのMAPロードreturn時は後続のUnit構築・Script/開始callbackをまだ含む。MAP定義読込完了と最終初期配置確定を同一視しない。MAPIDの安定文字列offsetは本担当では未確認、field pointerだけをIDに偽装しない。

## 観測候補と採否
| 候補 | 読める段階 | 採否 |
|---|---|---|
| 4922A0 entry | 要求・route。名簿未完成 | 要求記録のみ、開始確定に不可 |
| 40D0A0 entry | bypass含むBattleWnd要求とDL | 独立記録候補。通常Scene引渡しへ混ぜない |
| 492890 onLeave | callback含むactivation関数完了 | read-only候補、Scene深さとtask-pass記録必須 |
| 48D6A0 onLeave | Scene builder全体完了 | read-only候補、active未開始のケースあり |
| 433E5D | activation後、VM SEH復元前 | 無条件パッチ/安全holdとして不採用 |
| 4C2933後 | 現Task callbackからの復帰 | 後続Unitを抑止しない限りsafe holdでない |

引渡し受入案: request世代一致・activeをこの世代で確認・activation正常return・3Side callback完了・scene_builder_depth==0・ゲームthread同一・VM復元済み・残Taskを再実行/実行継続しない保持方法の実機証拠・全必須読取同一epoch、を全て満たす。AND条件は設計であり、現時点PASS0。

## 証拠・限界・再開地点
- native_entry_evidence.json: 今回のSHA一致コピーからの388命令。入力範囲の誤境界を生成中に修正済み。最終証拠は492123/492A43/48D7EAを既知命令開始として使う。
- ENTRY_VERIFICATION.json: Stage14/16/17既存アンカー131/131実バイト一致、生成JSON16件のparse/readbackとSHA。これは既存意味の独立再照合であり、新しい実機PASSではない。
- function_*.json / refs-to_*.json / callers_*.json: V9専用CLIの全文、最大chars100000・limit200。各dataのverified_abi=0を保持し、V9 DBの正式ABI3件へ勝手に昇格していない。ここで記す入口ABIは局所native確認結果。
- 継承出典: BATTLE_TAKEOVER_OBSERVABILITY_CONTRACT_20261023.md、BATTLE_STAGE14_READ_LAYOUT_SPEC_20261022.json、BATTLE_STAGE14_MISSING_STATE_NATIVE_EVIDENCE_20261022.json、BATTLE_STAGE16_NATIVE_ENTRY_EVIDENCE_20261022.json、BATTLE_STAGE17_ACTIVATION_BOUNDARY_20261022.json、battle_native_war_tree_decoder_v5_20261021.py、battle_bridge_detached_snapshot_v2/v3_20261021.py。
- 確定: 記録済みCALL経路、入口のレジスタ/stack/RET、active後callback順序、埋込MAP manager、保存済み読取offsetに対応するバイト。
- 推測/設計: 安全引渡し候補、世代token、AND受入条件、各生fieldのUI意味。設計の承認はruntime成功ではない。
- 未検証: 全間接経路、実機入口のthread/再入/例外、全分岐MAP配置、同時点完全名簿、stable MAPID/Unit定義ID、停止再開、安全な結果引渡し。
- 再開地点1: 親の実機所有権ゲート後に492890 onEnter/onLeaveと48D6A0 depth、40D0A0入力を受動記録し、世代・Task-pass・threadを照合。手動pause flag変更はこの仕様から許可されない。
- 再開地点2: fieldのstable ID・Unit+1C8 record定義ID・3Sideの役割を元PEのwriter/readerで特定し、runtime値を一戦闘内で検証。
- 再開地点3: 観測が成立してから別担当Task/VM保持証拠と統合。独自にonLeaveへ無限待機を入れず、native更新を止める選択は実証まで保留。

