# P0｜迫真戦記 ver0.67 召喚Unitの経験値所有者を静的追跡
**Task ID:** HAKUSHIN-P0-SUMMON-EXP-OWNER-20261021  
**対象EXE:** `rea_lab/targets/hakushin067_Vahren.exe`  
**SHA-256:** `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`  
**範囲:** 既存SQLite+擬似C、既存B/REA native、原本コピーの該当x86命令の読み取りのみ。原作EXE/セーブ/DATを起動・変更していない。  
**評価ラベル:** STATIC VERIFIED=命令・CALL参照・書込先を証拠で確認、INFERRED=条件付き推論、VERIFY=未確認、DYNAMIC OBSERVED=0、BLOCKED=今回新規なし。  
**作業所有:** `rea_lab/headless_analysis/search_index` 派生研究のみ。MASTER、A～E、REAキュー、製品コード、Git、Workへの書込なし。

## 1. 結論：召喚UnitのEXP蓄積先
[STATIC VERIFIED] **召喚で作られる戦闘Unitの+0x1C8は、0x54E7B0が召喚元Unitの+0x1E4B4にあるキー付きツリーから検索／必要に応じ作成した「UnitData相当の別レコード R」に設定する。** 一律に元Unitの+0x1C8をコピーする構造ではない。
[STATIC VERIFIED] この戦闘UnitがEXP helper `0x551E50` の獲得条件を満たすと、`R+0x16C` に加算する。つまりこの経路における書込先はまずツリーのRで、召喚元Unit自身の+0x1C8先への自動振替ではない。
[STATIC VERIFIED] `0x57F190` から召喚を発動すると、その後別途 `0x57F4E9` で `0x551E50` を発行し、発動元Unitをcontext actorとする。こちらの技能使用EXPと、召喚後の子Unitが稼ぐEXPは**別イベント**。
[INFERRED] 同一召喚元＋同一検索キーでキャッシュがhitするとRが再利用され得るため、Rポインタと個々の召喚Unitの一対一対応は保証されない。実機での再利用・キャッシュキー内容は未確定。
[VERIFY] ツリーのRが戦闘終了／召喚元死亡後に存続するか、戦略UnitのEXPへ同期されるかは未確認。DLLの最終配分先を永続的に同定したわけではない。

## 2. 全4直接CALLのレジスタ／スタック実引数
Ghidra CALLGRAPH + Capstoneで原本コピーのx86 `E8` CALL直前を再照合。Ghidra擬似Cで欠けていたレジスタ引数を読んだ。この呼出形式ではECX/EDXが先頭2引数で、残り4引数は**第6→第3引数の順にpush**され、calleeが第3～第6引数として受け取る。
| 呼出site → 0x54E7B0 | ECX / EDX | stack第1項: sourceUnit候補 | stack第2項: 第4引数 | 条件 |
|---|---|---|---|---|
| 0x54DCA0 **0x54DF4B** | ECX=0 / EDX=効果Skill | EBX=[ESI+0x78] | 0 | +0x40 kind4、Skill+0x74=0 |
| 0x5501A0 **0x550219** | ECX=&[ESI+0x1E8] / EDX=EDI | EBX=下記の条件付選択 | [ESI+0x1F0] | timer/interval処理、kind4 |
| 0x57F190 **0x57F484** | ECX=0 / EDX=EBX(skill) | EBP=発動元戦闘Unit | 0 | Skill+0x74=0、座標sentinel |
| 0x57F190 **0x57F492** | ECX=&stack座標 / EDX=EBX(skill) | EBP=発動元戦闘Unit | 0 | Skill+0x74=0、座標有 |
stack第3・4項は座標候補 x/y に対応。詳しいraw命令・バイトは `P0_SUMMON_CALLSITE_ASM_20261021.json`。4件は「直接CALL全件」であり、未知の間接発動が不在だと証明するものではない。
`0x5501A0` では EBX を `[ESI+0x1D8]`、`ESI+8`、`[ESI+0x80]` から+0x65/+0x6D条件で選ぶ。したがってタイマ経由で常に画面上の詠唱者ポインタになるとは断定しない。
## 3. キャッシュhit／missの実行経路
1. **元Unitのツリーを使う**：[STATIC VERIFIED] `0x54EE7F MOV ECX,[effect+0x7C]` → `0x54EE82 CALL 0x577260`。`0x577260` は `sourceUnit+0x1E4B4` を検索し、`+0x1E4B8` と一致すればNULL（`0x5772EE XOR EAX,EAX`）、見つかれば `0x5772B2 LEA ESI,[EAX+0x28]` を返す。
2. **hit時**：[STATIC VERIFIED] `0x54EE87` が返ったRをローカル枠へ保持し、`0x54EF8A` へ分岐する。既存値のレベル・EXP・キーの比較意味はVERIFY。
3. **miss時**：[STATIC VERIFIED] `0x54EF3E CALL 0x58B7F0` が召喚用UnitData相当の能力値を生成する。入力にはSkill+0x238が非0ならその値、未指定時には発動元のlinked+0x168レベルと倍率関連値が用いられる枝を含む。初期EXP、倍率丸めの全条件はVERIFY。
4. **miss時の格納**：[STATIC VERIFIED] `0x54EF69 CALL 0x577310`。その内部は `0x577380→0x57A6E0` が0x200バイトノードを確保し（`0x57A714`）、`0x57738B→0x57A240` で元Unitのツリーへ挿入、`0x5773E6→0x577260` で再検索して、`0x577405 MOV EAX,ESI` で結果Rを返す。
5. **コンストラクタへの接続**：[STATIC VERIFIED] hit側 `0x54EE87` の保存位置とmiss側 `0x54EF71` の保存位置は、途中pushを差し引くと同じローカル枠。`0x54F06D/0x54F06E` で2pushした後 `0x54F06F MOV ECX,[ESP+0x2C]` を使い、3番目の引数として `0x54F07A CALL 0x56F880` に渡す。この引数が新Unit+0x1C8へ格納される。
6. **別用途でも同じツリー**：[STATIC VERIFIED] `0x577260` は `0x547490`・`0x553390`・`0x54E7B0`・`0x577310` から直接呼ばれる。ツリーは「召喚専用」とは断定できず、効果／技能共有のデータ格納の可能性がある。
[B差分] 研究BのB-20261013-1134-01（大きな召喚関数）、B-1141-01（577260戻値node+28）、B-1146-01（56F880新Unit）、B-1436-01（579940探索）の核は既知。**今回の増分は全4 callerの実際のactor供給と、577310新規生成→戻りR→56F880+1C8→EXP加算先までのエンドツーエンド照合。** 既存READYは再計上しない。
## 4. Troopモードと+0x1CCの分岐
[STATIC VERIFIED] `0x54E7B0` は元Unit+0x1D0がNULLならモードを0に補正する。モード（0/1/2/3）の意味名は未確定だが、**選ぶTroop pointer**は次の通り。
| 分岐 | 生成Unit+0x1D0へ渡す値 |
|---|---|
| mode=0 | NULL |
| mode=1 | 元Unit+0x1D0（既存Troop） |
| mode=2/3、core第4引数=0 | `0x567EE0` で新しいTroopを割当／初期化（失敗ならNULL） |
| mode=2/3、core第4引数≠0 | 元Unitの+0x178..+0x17Cリスト末尾memberの+0x1D0（取得不可ならNULL） |
[STATIC VERIFIED] `0x56F880` 内の実store（保存済x86命令）：
- `0x56FEA2`: Unit+0x1D8 = param4（元Unit+0x1D8）。
- `0x56FEAF`: Unit+0x1C8 = param3（検索/生成済R）。
- `0x56FEB5`: Unit+0x1D4 = param5（元Unit+0x1D4）。
- `0x56FEBB`: Unit+0x1D0 = param6（上記の選択Troop）。
- `0x56FEC1`: Unit+0x1CC = NULL。Troopが非NULLなら、memberが空/NULLのとき自分のR、そうでなければ先頭memberの+0x1C8を `0x56FEE3` に書く。
- `0x54F096`: 選択Troopが非NULLのとき `0x568710` でUnitを関連付ける。
**結論**：[STATIC VERIFIED] +0x1CCは「召喚主の恒久Unit ID」ではない。Troop内容によって変わり、自分のRにも、別memberのRにもなり得る。
## 5. EXP書込の2系列を混同しない
[STATIC VERIFIED] `0x551E50` はhit context actor+0x1D0非NULL、+0x18614=0、context+0xC=0、Skill+0x2A8 sentinelではない場合、context+0xCを先行1にセットし、そのactor+0x1C8の先 `R+0x16C` に量を加算する（`0x551FB2`）。閾値+0x170とLevel+0x168は `0x58A650`／`0x58A400` に続く。成功を見ずに無条件加算は禁物。
- **召喚子の戦闘EXP**：生成子actor+0x1C8=キャッシュR、加算先はR+0x16C。
- **召喚技能発動者のEXP**：`0x57F190` は `0x57F4C7` でcontext actor=EBPをセットし、`0x57F4E9` の `0x551E50` はその発動者の+0x1C8経由で加算を試みる。召喚子の戦闘経験値を直接転送している証明ではない。
- [VERIFY] 戦略Unit保存時にキャッシュRの獲得EXPが移されるか／別処理で確定されるか、drainや直接slot書込を含む全経験値を同じ経路で捕捉できるかは未確認。
- [VERIFY] +0x1C8のRの使い回し、同一子Unitの複数hit-contextの扱い、+0x1D0 NULLでの経験値不獲得、召喚技能や回復のexp_per実効値は旧原作動作未観測。
- [VERIFY] `0x54E7B0` 自身に6件の間接CALL候補がある（`0x54F16D/239/2A5/2D7/2F0/3F8`）。対象の完全解決・全分岐のruntime到達は未完了。
## 6. DLL拡張における段階的な実現可能性
| 追加要件 | 判断 | 最低限必要な事実 |
|---|---|---|
| 同一戦闘中の召喚子獲得EXP観測 | **技術的に有望**（静的） | 召喚生成で子UnitとRを対応付け、0x551E50前後の実差分を測る。drainは別hook。 |
| 召喚元Unitに一定比率でEXP分配 | **条件付き** | 生成時coreのsourceUnit actor→sourceUnit+0x1C8を捕捉。+0x1CCをowner IDと誤認しない。ネスト召喚/複数子ではR共有を考慮。 |
| 召喚元死亡後の反映 | **未保証** | source UnitとR双方の解放時刻、永続UnitID、戦闘終了/セーブロードの同一性、pointer世代番号。 |
| 変身に伴う追随 | **未保証** | 同じ戦略UnitのRか、別登録・再生成か、イベント変更とlevel保持を個別確認。 |
| CPU簡易戦闘共通化 | **未保証** | 0x491870/0x521D90等の簡易戦闘結果からEXP付与先・戦略UnitIDを別に調査。 |
**推奨する設計順**：[INFERRED] ①読み取り専用で生成時 `source actor, source+1C8, R, newUnit, selectedTroop` を同時記録する ②通常hitとdrainでR+16Cのpre/postを分離採取する ③死亡後は生pointerでなく安定ID＋値snapshotを保存する ④実機で永続ownerと簡易戦闘のpathが確定した後に割合配分をPoC化する。
[WARNING] cache Rが1 actor内で複数召喚子に再利用される可能性があるため「RのXP増分＝個別1子のXP」とは必ずしもいえない。発生contextのactorもログのキーに加える。
[WARNING] 出力は解析用コードの技術的見通しであり、DLLを実装・注入した結果ではない。x86 ABI/例外/FPU、再入、死亡・メモリ再利用、元EXE ASLR/保護方式は実行前に別途調査が必要。
## 7. 原作の実機観測が必要な最小ケース（設計のみ、NOT RUN）
- **S0** baseline：原本と合法なセーブを複製し、SHA、戦略UnitID、発動者・対象を固定。
- **S1** 同じ召喚元が1体召喚→生成時actor、cache R、newUnit+1C8/1CC/1D0、Skill+2A8とEXP前後を別記録。
- **S2** 同じ召喚元が同じSkillで2回召喚→cache hit、R再利用、各子の経験値増加を分離。
- **S3** 1Troop内に召喚主2体、各召喚Unit2体→+1CCが先頭memberである場合と真の召喚主識別を対照。
- **S4** mode0/1/2/3・タイマ経路core第4引数0/非0→Troop実体と+1D0のNULL条件を対照。
- **S5** 召喚子が先に死亡／召喚元が先に死亡→キャッシュRの生存範囲・destructor・EXP結果をtrace。
- **S6** 召喚の発動だけ・召喚子の命中だけ・両方→`0x57F4E9` と `0x551FB2` の発動者/子の2経路を分離。
- **S7** 戦闘後セーブ→再ロード→次の戦闘でRが消えるか、戦略側のEXPへ反映されるかを検証。
いずれもDYNAMIC OBSERVED=0／Golden PASS0、未許可の旧EXE起動・DLL注入・SAVE変更は禁止。

## 8. 重複・引継ぎと再開地点
- **既存B**：`data/T012_SUMMON_CORE_54E7B0_CONTRACT_20261013.md`、`data/T013_SUMMON_LOOKUP_577260_CONTRACT_20261013.md`、`data/T011_SUMMON_RUNTIME_UNIT_56F880_CONTRACT_20261013.md`、`data/T012_BATTLE_CALC.md` §59、`data/T011_DATA_MODEL.md` §20。旧STATIC READYを再採番せず、主に4 caller引数とキャッシュnew/miss→R→EXPの交差を増分にする。
- **REA**：旧 `REA_20261019_2143_DEATH_SECOND_CALL_REACHABILITY_QC.md` 等の死亡部隊経路は既存成果。今回新しい死亡実測なし、死亡処理の再逆解析なし。
- **E**：`MASTER_LEDGER.md` 正式統合はE担当。静的事実のみ確認し、実機Golden・厳密互換をREADYとして勝手に宣言しない。
- **新しい証拠**：`P0_SUMMON_CALLSITE_ASM_20261021.json`、`P0_SUMMON_EXP_OWNER_GRAPH_20261021.json`、`P0_SUMMON_EXP_OWNER_VALIDATION_20261021.json`、本書。
- **再開地点**：キャッシュ検索キーの生成元を`0x54EE54→0x577260`周辺の合法既存命令から確定し、同じキーの複数子が同じRを共有するかさらに検証する。次いで「Rを戦闘後どう扱うか」と「どのポインタを永続UnitIDに結合できるか」に限定。
- **境界**：本報告は独立search_indexへの保存による引継ぎであり、別チャットへのライブ通知・B/E正本の改訂ではない。原作、製品コード、既存調査成果、REA queue、MASTER、Gitの公開先は変更しない。
