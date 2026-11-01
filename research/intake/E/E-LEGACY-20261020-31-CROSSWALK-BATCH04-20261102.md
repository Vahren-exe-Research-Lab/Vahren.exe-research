# E/T018 T020 research archive, legacy batch 04

Verified source provenance: authorized PC, 2026-11-02 JST; 23 E-owned markdown reports each matched to private develop catalog SHA256. PRIVATE intake only; source assertions may be historical STATIC, INFERRED, SYNTHETIC or VERIFY, not curator-approved source of truth. Original native behavior, complete Golden, formal READY and newly executed test numbers must not be inferred from this copy.

## E-AUDIT-20261030-06H-T020-T028-MODE1-CASCADE-ALIAS-GATE-01

**E source:** `tests/T020_E_T028_MODE1_CASCADE_ALIAS_ACCEPTANCE_20261030_06H.md`; **SHA256:** `3a8df10bf567b52f9f90c6a94568d395f94a062024ff650e29540af97c1b1536` (4948 bytes). **Subject:** 研究E｜T020 mode1二段階cleanupとalias警戒の受入検証（2026-10-30 06H JST）. **Confidence:** report-original STATIC/SYNTHETIC/VERIFY; **actual Golden:** not demonstrated.

Selected report claims (L=owner E file line, shortened):
- L5: - B owner: 'B-20261030-0615-T028-MODE1-CASCADE-DTOR-01', 'data/T028_RETREAT_MODE1_CASCADE_DTOR_NATIVE_20261030_06H.md'。B owner 'data/T028_MORALE.md'、'evidence/LANE_B_HANDOFF.md'の同ID各1出現を読取確認。
- L10: - mode0: 0x5984DF/0x598596でdeep cleanupをskip。ただし旧01Hで確認済みの先行tree範囲erase callsiteは保持する。mode0を完全no-opにしてはならない。
- L11: - mode1: vectorの候補各要素で0x598543 '0x467DE0' 返値が非NULLなら0x598553/0x598555 '0x463590' cleanupへ、NULLなら当該候補cleanupをskip。0x59855Aでloop indexを復帰する。
- L12: - mode1: vector終了後は0x598591/0x5985A2/0x5985A3/0x5985A5から、第2引数primary objectへの別cleanupを試みる。vector空でもこの経路を維持する。
- L13: - '0x463590'は既B 10/28のowner索引整理・destructor様・解放callを参照する。各候補とprimaryの指す実メモリが同一の場合、重複破棄の可能性を**警告**し、エンジンの実際のdouble-free発生・防止は推測で確定しない。
- L14: - このモデルのtree_calls=1+vector長は原ASM上のcallsite通過を模した理想正常経路であり、木の削除ノード数・実解放完了を表さない。resolverの返値も注入した合成値のみ。

To promote: inspect superseding E errata, B/REA ownership, underlying native byte/DAT proof, and legitimate same-battle G0/G1/G2 evidence.

## E-AUDIT-20261030-04H-T020-T028-NOTIFY-GATE-DECOUPLING-01

**E source:** `tests/T020_E_T028_POSTRELEASE_NOTIFY_ACCEPTANCE_20261030_04H.md`; **SHA256:** `919ac3760f4ff56896ced88825029975928b9510f64620af48e9fda2f8f68da9` (4365 bytes). **Subject:** 研究E｜T020 T028退却予約減算と通知gateの独立受入（2026-10-30 04H JST）. **Confidence:** report-original STATIC/SYNTHETIC/VERIFY; **actual Golden:** not demonstrated.

Selected report claims (L=owner E file line, shortened):
- L7: - Ghidra現行状態は2026-10-29更新 'rea_lab/headless_analysis/00_START_HERE_ACTIVE_RESEARCH.md' と 'CURRENT_ACTIVE_RESEARCH_STATE_LATEST.json' で V9選択を確認。DBのE独立再ハッシュは未実施。旧V3選択という古い案内へ巻戻さない。
- L9: - '0x495578' でSpot参照一致時のみ '0x495580' のSpot+0xB8減算呼出経路。一致・不一致はその後の通知判定と独立。実メモリ値・下限保証はVERIFY。
- L10: - '0x495586' と '0x49558C' はESI+0x77またはESI+0x75の非0を要求、'0x495596' はstack+0x6F非0を要求。どちらか不成立なら '0x49516F' の次要素経路へ。
- L11: - 条件を満たす場合、'0x4955A8' のmanager mode==1側は '0x4956AA CALL 0x52CF50'、その他側は '0x49579E CALL 0x434B10' (ECX=10)。これはCALL分岐であり、表示・通知配信成功ではない。
- L12: - CP932 string 'decide11' と '$$$は###へ退却しました' はB原PEの候補文字列。どの経路で実際に表示されるか、APIの意味、producerと有効な入力状態はVERIFY。
- L13: - 静的gate入力が取得不能の場合はUNKNOWN/INELIGIBLEとし、通常UIの撮影から内部flagや正確なSpot+0xB8値を捏造しない。原作GAMEPLAY証明には使わない。

To promote: inspect superseding E errata, B/REA ownership, underlying native byte/DAT proof, and legitimate same-battle G0/G1/G2 evidence.

## E-RC-20261030-08H-T020-TOOL-PATH-AND-OUTPUT-FORMAT-01

**E source:** `tests/T020_E_T028_POSTRET_08H_TOOL_RECOVERY_20261030.md`; **SHA256:** `5a3711c8c6b0c688ce6d9b9f4d74ae177e7b707fc35b6ad143234e92275c5512` (1905 bytes). **Subject:** E 08H tool recovery: non-safety failures (2026-10-30). **Confidence:** report-original STATIC/SYNTHETIC/VERIFY; **actual Golden:** not demonstrated.

Selected report claims (L=owner E file line, shortened):
- L3: Owner: E/T020。状態 OTHER / RECOVERED / 未保存の新規研究差分0 / 既存安全拒否とは別。
- L4: 発生1: Local read_fileで旧rea_lab/headless_analysis/search_index/README.mdを要求したがENOENT。2026-10-29の既存整理でREADME/BUILD_MANIFESTの旧名称は非現行。安全拒否ではない。旧pathを作らず、既存の許可済み00_START_HERE_ACTIVE_RESEARCH.mdとCURRENT_ACTIVE_RESEARCH_STATE_LATEST.json、V9統合入口をread-onlyで確認。現行V9 state取得成功。ゲーム・DB・元資料変更なし。
- L5: 発生2: 既存11本のT028検証器をPowerShellで一括再実行した最初の集計は、出力が一律JSONであると誤認。JSON以外の9本をFAILEDと表示したが、これは出力パース誤判定。再実行時に各検証器のexit codeと先頭出力を個別読み取りし、11/11 exit0を確認（検証コードの失敗は0）。

To promote: inspect superseding E errata, B/REA ownership, underlying native byte/DAT proof, and legitimate same-battle G0/G1/G2 evidence.

## E-AUDIT-20261030-07H-T020-T028-POSTRET-BUFFER-RELEASE-01

**E source:** `tests/T020_E_T028_POSTRET_BUFFER_FREE_ACCEPTANCE_20261030_07H.md`; **SHA256:** `9607b54ce9b25720f4d17ac55be45c280efe7ed15bcca6c4f22569fbe9021b48` (4415 bytes). **Subject:** 研究E｜T020 T028 mode1後の条件付きvector-buffer解放（2026-10-30 07H JST）. **Confidence:** report-original STATIC/SYNTHETIC/VERIFY; **actual Golden:** not demonstrated.

Selected report claims (L=owner E file line, shortened):
- L8: B保存局所PE窓: 0x5AC3A0+0x7A SHA43B013048E6BDE945B84BEFEBBE3EE5124DF98328D829851906F26A68AF2A8DC、0x5AC5E3+0x70 SHA6D421D77C8258538E8567B72C6C24783E877A567FB2780A41B39950010192F35。本E回では窓を再読しておらずBのSTATICを検証条件とする。
- L10: 通常走査完了: 0x5AC3C4 CMP EDI,EBX → equalなら0x5AC3D1へskip、異なる時だけ0x5AC3C9 CALL0x5B6BBB。通常経路と後段の総副作用は未確定。
- L11: 早期mode1: 0x5AC3AF Unit+0x77==0 かつ 0x5AC3B5 Unit+0x75==0 の局所gate→0x5AC3B9 JE0x5AC5E3→0x5AC5E7 CALL0x598450(mode1)。これは05/06H既知・二重計上しない。

To promote: inspect superseding E errata, B/REA ownership, underlying native byte/DAT proof, and legitimate same-battle G0/G1/G2 evidence.

## E-RC-20261030-07H-T020-PS-AUDIT-OTHER-01

**E source:** `tests/T020_E_T028_POSTRET_TOOL_RECOVERY_20261030_07H.md`; **SHA256:** `fc0d8f7cd67d4c40608e840bc2a440ae7e952928b7d0a4a7dd80f376d0a70c56` (1753 bytes). **Subject:** E T020｜07H 軽量集計コマンドのOTHERエラー回復記録. **Confidence:** report-original STATIC/SYNTHETIC/VERIFY; **actual Golden:** not demonstrated.

Selected report claims (L=owner E file line, shortened):
- L5: 失敗1: PowerShell既定実装が演算子「??」を受理せず、集計用コマンドがParserError。Python再実行には到達せず、ファイル変更・未保存差分なし。
- L7: 初回集計構造の問題: 21H検証器はSYNTHETIC 8/8行の後にsource-check 3/3を出す。最後のPASSだけを取る簡易パーサが3/3を拾う誤集計を確認し修正。
- L8: 回復: 各検証器の正規出力を区別し、合計をPowerShell foreachで整数加算する軽量read-only監査を実行。全11検証器exit0、T020合成299/299 PASS（既存266＋新規33）。

To promote: inspect superseding E errata, B/REA ownership, underlying native byte/DAT proof, and legitimate same-battle G0/G1/G2 evidence.

## E-AUDIT-20261030-08H-T020-T028-POSTRET-RANGE-ERASE-CALLSITE-CORRECTION-01

**E source:** `tests/T020_E_T028_POSTRET_TREE_RANGE_ERASE_CORRECTION_AUDIT_20261030_08H.md`; **SHA256:** `7d8cc7e67ef899aaeec2f27d436bef8fa71e81b4d079d0b170e87e5c5e37e6ec` (4027 bytes). **Subject:** 研究E｜T020 T028 post-RET木範囲消去・呼出位置の訂正（2026-10-30 08H JST）. **Confidence:** report-original STATIC/SYNTHETIC/VERIFY; **actual Golden:** not demonstrated.

Selected report claims (L=owner E file line, shortened):
- L8: 統合V9の関数0x510850出力ではE8_DIRECT_CALLとして0x510867→0x44D0D0、0x5108DF→0x510C20を記録。ABIは未検証。
- L10: 旧07H E文書の「0x5AC609 CALL0x510850」は誤り。B08H原生ASM訂正をEの新独立BYTEゲートで照合した。
- L11: 研究PEの0x5AC609はE8でない。正しい直接E8 CALLは0x5AC611→0x510850。07H文書・検証器の過去成果を消去/改変せず、当該siteだけ本08Hを正本の後続訂正とする。

To promote: inspect superseding E errata, B/REA ownership, underlying native byte/DAT proof, and legitimate same-battle G0/G1/G2 evidence.

## E-AUDIT-20261030-01H-T020-T028-PREFLAG-ERASE-PROVENANCE-01

**E source:** `tests/T020_E_T028_PREFLAG_ERASE_ACCEPTANCE_20261030_01H.md`; **SHA256:** `8b5e744f978f609967253b3d9d366b300e2b2496dbcbb821d4b7dfaf6b1ebf3f` (3493 bytes). **Subject:** 研究E T020 退却Spot-index range-eraseのflag前呼出を回帰契約へ追加（2026-10-30 01H）. **Confidence:** report-original STATIC/SYNTHETIC/VERIFY; **actual Golden:** not demonstrated.

Selected report claims (L=owner E file line, shortened):
- L7: - B原作ASM根拠：0x598469 CALL0x416080→0x59847C CALL0x415CF0（初回key）、0x5984C7 CALL0x416080→0x5984DA CALL0x415CF0（各vector entry）、flag判定0x5984DFより前。従ってflag0でも範囲探索とerase-rangeへの呼出経路が存在する。vector長0でも初回key経路は残る。
- L8: - 0x415CF0はfirst/lastに応じて0x415D0A→0x416870全消去候補、または0x415D8F→0x416220逐次消去。実際に何node削除されるか、key比較0x402C40の等価性、tree owner、元GAMEでの到達はVERIFY。B sideより強い動的断定を行わない。
- L11: - 合成モデルは、正常に呼出が進む仮定で初回1+vector長のerase-range callsiteを数える。**実際の削除node数はUNKNOWN**。flag0・vector0を無副作用と誤認しない。
- L12: - unsupported claim（lookup-only、no mutation、full clear、1node除去、Golden PASS）、comparator未確定、0x5AC5E7のCFG未確定、site/mode不一致、不明入力をfail closed。
- L21: - 次：B owner 0x402C40 comparator / 0x416220 node removal帰結の一次証拠が得られた場合のみ受入分類更新。同時に合法同run G0-G1-G2の旧SAVE/UI入力/MAP/名簿receiptの有無を優先監査。

To promote: inspect superseding E errata, B/REA ownership, underlying native byte/DAT proof, and legitimate same-battle G0/G1/G2 evidence.

## E-AUDIT-20261030-05H-T020-T028-RETRY-MODE1-CFG-01

**E source:** `tests/T020_E_T028_RETRY_MODE1_CFG_ACCEPTANCE_20261030_05H.md`; **SHA256:** `7979d4da779261f42d0b9ec9161c368440b56f38e2da05eb471354da5f761ac6` (4315 bytes). **Subject:** 研究E｜T020 二度の退却先探索と post-RET mode1 入口の局所CFG受入（2026-10-30 05H JST）. **Confidence:** report-original STATIC/SYNTHETIC/VERIFY; **actual Golden:** not demonstrated.

Selected report claims (L=owner E file line, shortened):
- L5: - B owner 'B-20261030-0515-T028-DUAL-RETRY-POSTRET-MODE1-JUMP-01'、'data/T028_RETREAT_DUAL_ATTEMPT_POSTRET_EDGE_NATIVE_20261030_05H.md'。EのLocal readと独立Get-FileHashにより出典実SHA256='9510EAE2532D8DFE854EFB46DBC393E5C61EF5F2AA4553E355C27A156374727A'を確認。
- L9: - '0x495032'既存Unit+0x1B4が非NULLなら保存済Spotを使用。NULLの場合 '0x495050'が候補探索初回index0 /第三引数0、失敗時のみ二度目index1/第三引数1を試みる。二度目はUnit+0x77非0が必要、index2は無い。
- L10: - '0x5AC3AF/0x5AC3B5/0x5AC3B9'のcandidate+0x77/+0x75両0は'0x5AC5E3'に直接分岐し'0x5AC5E7'の'0x598450(mode1)' CALL siteへ到達し得る。このCFG上の明示枝は、RET直後に位置することだけを理由に到達不能扱いしない。
- L11: - ただし'0x5AC36D'までの上流caller/第三引数stack対応、候補listの生成、実ゲームで条件が成立すること、mode1 helper副作用はVERIFY。静的辺存在と正常Gameplay到達、実際の画面通知・予約数変化を別評価とする。
- L12: - '0x494F98'の[ESP+0x6F] writerと'0x495596'の[ESP+0x6F] readerは間のSUB ESPにより同一slot未証明。同名offsetだけで通知flag producerを確定しない。
- L16: - この36件はBのSTATIC研究を模した検証器自身の合成分岐であり、原作退却成功・新エンジンstrict互換・未解明のstack由来を証明しない。

To promote: inspect superseding E errata, B/REA ownership, underlying native byte/DAT proof, and legitimate same-battle G0/G1/G2 evidence.

## E-AUDIT-20261030-11H-T020-T028-SENTINEL-BRANCH-RNG-01

**E source:** `tests/T020_E_T028_SENTINEL_RNG_ACCEPTANCE_20261030_11H.md`; **SHA256:** `81ba9a46b1fbc02e6aacf60e9af1ae9673b5275a146292dc017a6db529000422` (3463 bytes). **Subject:** 研究E｜T020 selector後段 +0xD0 sentinel／局所RNG分岐受入（2026-10-30 11H JST）. **Confidence:** report-original STATIC/SYNTHETIC/VERIFY; **actual Golden:** not demonstrated.

Selected report claims (L=owner E file line, shortened):
- L10: 局所PE 0x447BB8+0xB0、0x447D52+0x155のSHAを2/2一致。RNGの直接E8 CALL 0x447C6E/0x447E1A→0x5B6EABを2/2、double 0x63B348=1000000.0・0x63B0B0=2.0を2/2実バイト確認。
- L11: 局所state分岐: selectorをskippedしても初期local flag=1が残り得る。selector NULLまたは走査Unit+0x1AD非零はflag0経路。関連先+0x10が零、またはflag0で+0xD0 sentinel 1000000.0に進む。
- L12: 逆に関連先+0x10が非零かつflag1で計算経路へ進み、ローカル比較の有限値下限2.0をモデル化。計算式・x87 NaN/Infinity/丸めは今回の合成スコア入力からは導けない。

To promote: inspect superseding E errata, B/REA ownership, underlying native byte/DAT proof, and legitimate same-battle G0/G1/G2 evidence.

## E-AUDIT-20261030-02H-T020-T028-SPOT-TREE-LIFETIME-PROVENANCE-01

**E source:** `tests/T020_E_T028_SPOT_TREE_LIFETIME_ACCEPTANCE_20261030_02H.md`; **SHA256:** `0ce6c6345ab622559bca2b522d8570598e2e1994d75b8d920f2e21aec3526919` (4191 bytes). **Subject:** 研究E T020｜退却Spot treeの文字列容量・erase寿命／合成契約（2026-10-30 02H）. **Confidence:** report-original STATIC/SYNTHETIC/VERIFY; **actual Golden:** not demonstrated.

Selected report claims (L=owner E file line, shortened):
- L7: - 参照B: B-20261030-0215-T028-SPOT-TREE-ERASE-STRING-RELEASE-01（VERIFY/NOT READY）。詳細SHA256=1C95D49A632F3C27B800C774E6CA738A4CF58116D96709587FDC8823225F5AAF、Local実バイト再計算で一致。
- L8: - 元PE SHA=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（B側の元PE検証結果を継承。E本回ではPE実ハッシュ/ASM再抽出なし）。V9 DB=2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE（B側検証、E再計算なし）。
- L9: - 既E01Hのflag前erase-range呼出し・0x415CF0 partial/full分岐は既知として再計数0。新規はB02Hの文字列容量閾値/iterator不正/解放順/条件付きcount減算の受入モデル。
- L12: - VA0x4160D5 node+0x1C byte lengthと0x4160E4 node+0x20 capacity、VA0x4160E7 capacity16ならinline、それ以外heap。長さ比較はprefix一致時のみ、非ASCII実encode/辞書順はVERIFY。
- L13: - VA0x416224 node+0x29 byteが非0で0x41622F CALL0x5B5BBA（invalid iterator経路）。実合法到達・画面例外はVERIFY。
- L14: - VA0x41646A capacity=16なら0x416474 CALL0x5B6BBB(buffer)→0x41648F CALL0x5B6BBB(node)。capacity16は前者を通らず後者へ。free実成功・double free不存在・全消去0x416870での同一動作は未証明。

To promote: inspect superseding E errata, B/REA ownership, underlying native byte/DAT proof, and legitimate same-battle G0/G1/G2 evidence.

## E-AUDIT-20261030-10H-T020-T028-THIRD-SELECTOR-OPAQUE-EAX-01

**E source:** `tests/T020_E_T028_THIRD_SELECTOR_OPAQUE_EAX_ACCEPTANCE_20261030_10H.md`; **SHA256:** `c69a44308381bee64399b2ce7fe5dbadb0ac4879b053074ba5f8629eff8d17a8` (4121 bytes). **Subject:** 研究E｜T020/T028 第3 selector caller と opaque EAX 受入（2026-10-30 10H JST）. **Confidence:** report-original STATIC/SYNTHETIC/VERIFY; **actual Golden:** not demonstrated.

Selected report claims (L=owner E file line, shortened):
- L8: V9 DBはB出典既確認SHA=2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE。本EでDB再SHA・Ghidra新解析なし。PC標準LATESTのV9昇格完了を仮定しない。
- L10: PEのセクションRVA変換後、0x447BF0から134Bと0x597BA0から234Bの局所SHAをB記録と2/2一致。
- L11: E8 rel32 CALL site→calleeを6/6実バイト確認: 0x447C23→0x597BA0、0x447C2F→0x5AC1A0、0x5682B5→0x597BA0、0x5682C3→0x5AC1A0、0x597BDF→0x49E490、0x597C6B→0x5A8110。

To promote: inspect superseding E errata, B/REA ownership, underlying native byte/DAT proof, and legitimate same-battle G0/G1/G2 evidence.

## E-AUDIT-20261030-00H-T020-T028-VECTOR-HELPER-MODE-SOURCE-GATE-01

**E source:** `tests/T020_E_T028_VECTOR_HELPER_MODE_ACCEPTANCE_20261030_00H.md`; **SHA256:** `c39e7a54f8b4da3e2519cf4cbe51fa671922ffcd0e7fa89d839b936bd76a13f6` (3453 bytes). **Subject:** E/T020 T028 ベクタhelper 第3引数modeの証拠境界（2026-10-30 00H）. **Confidence:** report-original STATIC/SYNTHETIC/VERIFY; **actual Golden:** not demonstrated.

Selected report claims (L=owner E file line, shortened):
- L5: - B-20261030-0010-T028-SPOT-VECTOR-FLAG-SPLIT-01 (Owner B/T028) は VERIFY / NOT READY。detail実SHA256=6F972CFB462306B9DF4620768E3C212E391A4153D6110F5F5F6EEC30DD53C9C6を今回独立Get-FileHash確認。
- L6: - B既存の0x495544(PUSH0)と0x495079(PUSH0)から0x598450への第3引数0、対照0x5AC5E7(PUSH1)の第3引数1を区別。0x5AC5E3はRET後に位置し合法正常CFG到達は未証明。
- L7: - 0x5984DF/0x5984E4・0x598591/0x598596のbyte条件でmode0は追加0x402710/0x467DE0/0x463590個別経路と末尾0x463590経路をskipする。共通の0x416080/0x415CF0はmode0でも候補として残り、「全副作用ゼロ」は禁止。
- L8: - この分岐は0x495578比較一致時の0x495580 DEC [EBX+0xB8]の完全実行、実Spotの予約解除、可視退却や勝敗を証明しない。flag1側の全到達・resolver非NULL・非空vectorも未証明。
- L9: - 検索索引は独立V9別名CLIの保存済み結果に基づくB資料。V9統合案内は旧標準LATEST/V3 pointerを置換済とは記載していないため、標準化完了と混同しない。
- L11: - 新規tests/T020_E_T028_VECTOR_HELPER_MODE_CASES_20261030_00H.jsonに18負例/分岐fixtureを記録。mode0の追加経路skip、mode1のCFG未確認、site/mode不一致、未知site、null・不正型・負vector、NO_SIDE_EFFECT/RELEASE/GOLDEN誤断定をfail-closedで区別。

To promote: inspect superseding E errata, B/REA ownership, underlying native byte/DAT proof, and legitimate same-battle G0/G1/G2 evidence.

## E-AUDIT-20261024-0344-T020-F720-CALLER-NULL-CONTRACT-01

**E source:** `tests/T020_F720_CALLER_NULL_CONTRACT_CROSSWALK_20261024_0344.md`; **SHA256:** `4f0ab78242eb6c0628194cd00403ca69761b7bb932fd32f0f2a47c73c9a692a3` (4154 bytes). **Subject:** 研究E｜F720戻値NULL契約：呼出元ガード非対称とGolden非昇格. **Confidence:** report-original STATIC/SYNTHETIC/VERIFY; **actual Golden:** not demonstrated.

Selected report claims (L=owner E file line, shortened):
- L7: - REA03H STATIC.md SHA256 DABA032A4DB9821DEE5DE5BA92E9BB3BE7BAE87EEC888B264FB02A0438153EA3、EVIDENCE.json SHA256 78F8B1FCA145FD33552AD68F09A0FF2D23FE8CA71484ED539BDECC9D35B4911C。E checkerで両SHA2/2再確認。24バイト検査24/24・E8 target9/9はREA既実績で、Eが新たに逆アセンブルした件数ではない。
- L9: - 0x48F720には戻り値0の静的経路がある。03H REA新規差分はcaller間NULL防御の違いであり、02Hのfilter規則/7 caller抽出自体は重複加算しない。
- L10: - 0x4901C1 - 0x4901EE CMP EAX,EBX（EBX=0）-0x4901F0 JE 0x490223 - 非NULL時のみ0x4901F2 [EAX+0x94]。局所明示NULLガードSTATIC。
- L11: - 0x40F393 -0x40F398-0x583C76 [EDI+0x94]、0x48FBD9-0x48FBF7-同callee、0x4F66ED-0x4F66F2-同calleeの局所経路には同様のNULLガード未確認。
- L12: - 0x4905F2と0x49381Eのmode等先行条件は、F720戻りポインタ自身のNULLチェックとは別。0x434EF3の後続EBP使用は未監査。
- L13: - 候補不在で0を返せることと、一部callerの明示NULLガードは、旧ゲームで0が非ガード経路に実際に届くこと、クラッシュ、原作バグ、データ破損を証明しない。上位の候補存在不変条件と同一実行での観測が未取得。

To promote: inspect superseding E errata, B/REA ownership, underlying native byte/DAT proof, and legitimate same-battle G0/G1/G2 evidence.

## E-AUDIT-20261024-0447-T020-F720-OWNER-CONTAINER-PROVENANCE-01

**E source:** `tests/T020_F720_OWNER_CONTAINER_PROVENANCE_CROSSWALK_20261024_0447.md`; **SHA256:** `ae6397b9ce3f587d6f0a16198ad8290a618ea59081afe6a4d6261196e67a2b20` (4746 bytes). **Subject:** 研究E｜F720候補コンテナ所有元・比較木の分離とG2誤昇格防止. **Confidence:** report-original STATIC/SYNTHETIC/VERIFY; **actual Golden:** not demonstrated.

Selected report claims (L=owner E file line, shortened):
- L7: - REA 04H native監査script実SHA F72B87051A6C75430FF453EE3418E345B67426E4CD5BD3065CD4372C5F4B831A。REA 03H evidence実SHA 78F8B1FCA145FD33552AD68F09A0FF2D23FE8CA71484ED539BDECC9D35B4911C。Eのsource hash4/4 PASSはファイルバイト照合であり新規native22/22実行の主張ではない。
- L9: - REAの既保存ASMによる0x40D0A0局所: 0x40D0AE→global 0x8B8E48へEDI、0x40D0B4→0x8B8E4CへEAX、0x40D0B9→0x8B8E50へECX、0x40D0BF→0x8B8E54をゼロ化、0x40D0C6→0x40F320をCALL。局所のポインタ設定は初期化CALL以前。
- L10: - 0x40D0A0の上位direct CALL siteは 0x491FFB,0x49204F,0x492143,0x4921F7,0x492473。上下位の引数対応はcontext+1EED1C/1EED20/1EED30、DL列1/0/0/0/1（意味未確定）。これらを実施済みの旧ゲームイベント数にしない。
- L11: - 0x40F38Dで[0x8B8E4C]を読み、0x40F393→0x48F720へ候補コンテナ、0x40F398→0x583C70へ戻り値を渡す。局所の戻り値NULLガード無しはREA03H以前の既知差分で再加算しない。
- L12: - 0x40F367..370 の比較用ESIは別のglobal 0x8B8D28由来、0x48F73Cの+1EED34参照と候補list ownerを混同しない。identity/alias/lifetimeはVERIFY。
- L13: - 0x48F720の先頭ヘッダ=候補headの空条件は0x48F7E4でEAX=0帰還へ到達し得る。0x49AF10には候補リストの空初期化/clear候補があるが、クリア後の挿入と戦闘入口時の非空保証は未解明。静的空経路と実クラッシュは別。

To promote: inspect superseding E errata, B/REA ownership, underlying native byte/DAT proof, and legitimate same-battle G0/G1/G2 evidence.

## E-AUDIT-20261024-05H-T020-F720-REBUILD-PHASE-GATE-01

**E source:** `tests/T020_F720_REBUILD_PHASE_CROSSWALK_20261024_05H.md`; **SHA256:** `84f2075b14b5aa405fb3f2c304b88f025794afd9881680a7362fc31c583af337` (4323 bytes). **Subject:** E/T018・T020｜F720前のreset→rebuild→選択の時相受入ゲート. **Confidence:** report-original STATIC/SYNTHETIC/VERIFY; **actual Golden:** not demonstrated.

Selected report claims (L=owner E file line, shortened):
- L4: REA 05:41保存の0x48F9E0監査は、候補listヘッダ初期化だけではなく0x48FBD1で0x498E60をCALLし、続けて0x48FBD9で0x48F720をCALLする経路を報告。04時台Eの「過去に空初期化された」という観測から「選択時も空」と推測してはいけない。
- L5: 0x498E60→0x498F90→0x476830ではinsert成功経路のcount+1が原作ASMで確認された（REA05:41既存知見）。ただし入力rangeの実要素数、duplicate排除、F720のfilter通過、リアルな非NULL保証はVERIFY。
- L6: 別0x0040D0A0→0x0040F320→0x0040F393経路を、0x0048F9E0のreset/rebuild経路と実行時同一コンテナ・同一時刻として結合する証拠はない。0x4918B4..CBのtimerと0x4923EB/F1のflagは局所ゲートで、合法UI G0の観測ではない。

To promote: inspect superseding E errata, B/REA ownership, underlying native byte/DAT proof, and legitimate same-battle G0/G1/G2 evidence.

## E-AUDIT-20261023-2252-FASTSIM-CLEANUP-CFG-01

**E source:** `tests/T020_FASTSIM_CLEANUP_CFG_AUDIT_20261023_2252.md`; **SHA256:** `aadc42a7c2fa7ef502389e43ed4f8d30580b76a0975a812f3e121216fc27382d` (4061 bytes). **Subject:** T020｜簡略戦闘後段の欠落CALLと正常復帰前cleanup境界（22:52）. **Confidence:** report-original STATIC/SYNTHETIC/VERIFY; **actual Golden:** not demonstrated.

Selected report claims (L=owner E file line, shortened):
- L27: - 新E検証器をPCで実行し、原作研究コピーEXE SHA256一致、ネイティブ10命令/10期待一致、JSON fixture ID一意7/7、exit正常。これはSTATIC検査で、7件の原作ゲームケースを実行した意味ではない。

To promote: inspect superseding E errata, B/REA ownership, underlying native byte/DAT proof, and legitimate same-battle G0/G1/G2 evidence.

## E-AUDIT-20261023-2052-T020-FASTSIM-RET-DOMAIN-TAIL-01

**E source:** `tests/T020_FASTSIM_NONZERO_RETURN_TAIL_CROSSWALK_20261023_2052.md`; **SHA256:** `13b9b35dc5cd684ff3e723df5bdf9bf0fb5f139942f3c2618e650adcbf890974` (4035 bytes). **Subject:** E T018/T020｜簡略戦闘 nonzero 戻り値と条件付き後処理の未照合分岐. **Confidence:** report-original STATIC/SYNTHETIC/VERIFY; **actual Golden:** not demonstrated.

Selected report claims (L=owner E file line, shortened):
- L5: 出典: 2026-10-23統合V9（SQLite SHA既記録値 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE）、同CLI function 0x0040E220, 0x0040E2F0, 0x0048EEE0, 0x0048ABF0。
- L6: 注意: V9 pseudoCは原ソースではなく ABI 未認証。出典 E8 native索引・callsiteとC擬似コードは強度を区別。原作実行・新プロセス観測0。
- L8: 0x0040E220 の元擬似Cには、0x0040E2F0のret==0時は0x0040D220(1)へ進むが、ret!=0なら **間接virtual +0x10** を先に呼ぶ経路がある。間接callの実到達先/終了は未確認。

To promote: inspect superseding E errata, B/REA ownership, underlying native byte/DAT proof, and legitimate same-battle G0/G1/G2 evidence.

## E-AUDIT-20261023-1952-T020-FASTSIM-SELECTOR-PRIORITY-01

**E source:** `tests/T020_FASTSIM_PRESELECTOR_BRANCH_GATE_20261023_1952.md`; **SHA256:** `5e5455326be70f5a7128a39794731fab8da5b0b07b71f36af2ce70bb2e575e4c` (3775 bytes). **Subject:** E T018/T020｜簡略戦闘の計算前selector・早期分岐を分離（STATIC）. **Confidence:** report-original STATIC/SYNTHETIC/VERIFY; **actual Golden:** not demonstrated.

Selected report claims (L=owner E file line, shortened):
- L5: 証拠版: search_index/HAKUSHIN067_UNIFIED_V9_20261023.sqlite（既検証DB SHA256 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE）。
- L6: 参照: V9 CLI function 0x0040E220・0x00431FB0・0x0040D220・0x00452FF0。前回E T020_FASTSIM_RETURN0_PRIMARY_VTABLE_DRAW_GATE_20261023_1850.mdとの差分のみ。
- L8: 0x40E220（secondary側this候補）は、冒頭で+0x78と+0x7Cがそれぞれ0x80000008かを比較。いずれか不一致なら0x40E2DF CALL 0x452FF0へ。ここを簡略戦闘実行と数えない。

To promote: inspect superseding E errata, B/REA ownership, underlying native byte/DAT proof, and legitimate same-battle G0/G1/G2 evidence.

## E-AUDIT-20261023-1651-T018-T020-FASTSIM-EXIT-PROOF-SPLIT-01

**E source:** `tests/T020_FASTSIM_RETURN0_1_2_G3G4_PROOF_GATE_20261023_1651.md`; **SHA256:** `607f9ee4c00c6ec3b5dbaac2d4cbc8a311d08e3fac5fc3ffbb75fedf19346e1e` (4944 bytes). **Subject:** 迫真戦記 E T018/T020｜簡略戦闘return0/1/2とG3/G4受入境界（2026-10-23 16:51 JST）. **Confidence:** report-original STATIC/SYNTHETIC/VERIFY; **actual Golden:** not demonstrated.

Selected report claims (L=owner E file line, shortened):
- L3: 状態: PC-SAVED / STATIC V9 CROSS-SOURCE / SYNTHETIC 15/15 / VERIFY / NOT READY / ORIGINAL GAMEPLAY NOT RUN。
- L4: 根拠: REA所有 rea_lab/decomp_task/REA_20261023_1638_P0_FAST_SIM_500TICK_OUTCOME_CONTRACT_STATIC.md、E既存 tests/T020_BATTLE_RETURN_COMMIT_GATE_20261021_2147.md と E T020 2026-10-23 15H、統合V9 CLIで本回read-only取得した0x40E220/0x40E2F0とcallers 0x493630。
- L8: V9直接E8 callers 0x00493630 は5 site: fast-sim 0x0040E2B9、通常時計0x0049303A/0x00493082/0x004930A1、DAT VM 0x004A1764。5 siteを一つの簡略戦闘経路へ統合しない。

To promote: inspect superseding E errata, B/REA ownership, underlying native byte/DAT proof, and legitimate same-battle G0/G1/G2 evidence.

## E-AUDIT-20261023-1850-T020-FASTSIM-DRAW-VSLOT-01

**E source:** `tests/T020_FASTSIM_RETURN0_PRIMARY_VTABLE_DRAW_GATE_20261023_1850.md`; **SHA256:** `281078eed8c9fbd7a2f298a2468eb25a68ed8452fc3462b774b63b54ed15d01d` (4882 bytes). **Subject:** E T018/T020｜簡略戦闘return0の描画可否を決めるprimary vtable slot. **Confidence:** report-original STATIC/SYNTHETIC/VERIFY; **actual Golden:** not demonstrated.

Selected report claims (L=owner E file line, shortened):
- L7: 既存証拠: E tests/T020_FASTSIM_RETURN0_UI_BRANCH_AUDIT_20261023_1745.md と REA_20261023_17H_P0_BATTLEWND_SECONDARY_VTABLE_FASTSIM_STATIC.md、REA_20261023_1833_P0_DEMOPERSON_VSLOT18_STATE4_STATIC.md（後二者はread-only/NOT READY）。
- L9: BattleWnd primary vtable=0x00638074、secondary vtable=0x006380CC（primaryから+0x28）は既知。
- L10: primary vtable+0x0C、PE VA 0x00638080に原EXE実ポインタ 0x00452D90 を確認。secondary+0x04は別の 0x0040E220 であり混同禁止。

To promote: inspect superseding E errata, B/REA ownership, underlying native byte/DAT proof, and legitimate same-battle G0/G1/G2 evidence.

## E-AUDIT-20261023-1745-T020-FASTSIM-RETURN0-UI-GATE-01

**E source:** `tests/T020_FASTSIM_RETURN0_UI_BRANCH_AUDIT_20261023_1745.md`; **SHA256:** `19843138fbb0ad73a60e13bff8a4aaf2705f70427c186e46388ef3089fb1570e` (3623 bytes). **Subject:** E T018/T020 | FastSim return0 の描画処理と結果commitを分離する証拠ゲート. **Confidence:** report-original STATIC/SYNTHETIC/VERIFY; **actual Golden:** not demonstrated.

Selected report claims (L=owner E file line, shortened):
- L7: 本回は search_unified_v9_20261023.py function(0x40D220,0x40D0A0,0x40F000,0x48ABF0) / callers(0x40D220,0x40F000)をread-only照合。V9 CLIは当該呼出元をPE E8_DIRECT_CALLとして記録。
- L9: 0x40D220へ入る直接E8は2箇所：0x40D0D2（caller 0x40D0A0、E8=E849010000）、0x40E28E（caller 0x40E220、E8=E88DEFFFFF）。
- L10: 0x40D0A0疑似CではFUN_0040D220(0)を呼び、sim_return==0側の0x40E220はFUN_0040D220(1)へ入る。CALL先は共通でも第2引数が異なる。

To promote: inspect superseding E errata, B/REA ownership, underlying native byte/DAT proof, and legitimate same-battle G0/G1/G2 evidence.

## E-AUDIT-20261023-2153-T020-FASTSIM-TAIL-MULTIENTRY-01

**E source:** `tests/T020_FASTSIM_TAIL_MULTIENTRY_CROSSWALK_20261023_2153.md`; **SHA256:** `9259c4fe463574e6b698d232c4e453ef7544cb2e620c5680161b4a2f193c2ac8` (4193 bytes). **Subject:** E T018/T020｜0x0048EEE0共有後処理の入口・擬似C欠落差分. **Confidence:** report-original STATIC/SYNTHETIC/VERIFY; **actual Golden:** not demonstrated.

Selected report claims (L=owner E file line, shortened):
- L5: 出典: 統合V9 search_unified_v9_20261023.py function 0x0040E220 / 0x0048EEE0 / 0x0048C880 と callers 0x0048EEE0。
- L8: V9 PE確認済みE8 CALLは0x0048EEE0へ計4箇所: 0x0040E2D2 (caller 0x0040E220/簡略戦闘)、0x0048D603 (0x0048C880/初期化系候補)、0x004A2D17 と 0x004A2EA1 (0x004A1250/DAT VM系)。
- L9: 同一calleeを複数の入口から使うため、0x0048EEE0を「簡略戦闘だけの結果コミット」としては扱わない。CALLの存在は実行時到達・全分岐完了の証拠ではない。

To promote: inspect superseding E errata, B/REA ownership, underlying native byte/DAT proof, and legitimate same-battle G0/G1/G2 evidence.

## E-AUDIT-20261024-0646-T018-T019-T020-G0-RECEIPT-EPOCH-01

**E source:** `tests/T020_G0_RECEIPT_EPOCH_GATE_20261024_06H.md`; **SHA256:** `3b169a0d89940391e0c84965141bd22eaa1a0168bd0f0f9437e3c5dfa3dbcf9f` (4843 bytes). **Subject:** E-AUDIT-20261024-0646-T018-T019-T020-G0-RECEIPT-EPOCH-01｜旧原作G0の時点別receiptとE Golden受入境界. **Confidence:** report-original STATIC/SYNTHETIC/VERIFY; **actual Golden:** not demonstrated.

Selected report claims (L=owner E file line, shortened):
- L2: 分類: STATIC_AUDIT_OF_SAVED_DYNAMIC_EVIDENCE / VERIFY / NOT READY / NEW GAMEPLAY NOT RUN。E担当T018/T019/T020、PC Local Compact接続。
- L4: REAのwatch開始時READY (2026-10-21 14:27:10 UTC) の native_gameplay_G0_confirmed=false と、事後G0報告 (14:52:18 UTC作成) の gate_status=PASS / actual_original_game_run=true は時点が違う。T019の真正な矛盾とは分類しない。
- L7: REA native G0イベントと利用者による侵攻申告は既存の実観測1件であり、今回の新規Gameplay試行ではない。戦闘窓active1時間は約116.56秒。

To promote: inspect superseding E errata, B/REA ownership, underlying native byte/DAT proof, and legitimate same-battle G0/G1/G2 evidence.

## Scope
Source record cursor 70-92 / 147; next 92. No original binaries/saves, Ghidra DB, unsafe refused sources, user private paths or other-owner text copied. Original-game DYNAMIC 0, Golden PASS 0, strict MATCH 0, formal READY additions 0. No change to curator develop or MASTER.
