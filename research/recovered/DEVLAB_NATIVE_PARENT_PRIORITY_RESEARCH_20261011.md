# 迫真戦記 v0.67 — 原作の親継承を推測せず解析する（DEV / 2026-10-11）

## 目的と範囲
- ユーザーはゲーム性の正解をチャットで教えて推測実装させることを望まず、原作EXE/保存Ghidra疑似C/保存native ASM/原DAT/実セーブから仕様を調べて、確定事項だけをコンパイル可能な再実装コードにするよう要求。
- ここは制作 dev_lab の独立研究資料。原本・MASTER・レーンA〜Eの所有資料はread-only。旧EXE/新Ghidra/REA逆解析プロセスは実行していない。過去の安全拒否の別shell/tool迂回なし。
- 原DATの宣言名一致、Ghidra自動生成疑似C、既存ネイティブ命令と新Python自己検査は異なる証拠水準。テスト合格を旧ゲームとの同条件Gameplay一致に読み替えない。

## 原DAT 590本の構文索引で確定した事実
- 既存 BattleDefinitionCatalog を変更せずread-only利用。原DAT 590ファイルから unit 4586/class 4080/skill 16554/skillset 106、計25326件の構文的宣言を索引化。各 (kind,name) は25326件すべて一意（索引可能な4種限定）。
- Unit/Classで両kindに同名tagがあるのは base 1個だけ。出典は unit base が 10_ユニット/00_base.dat、class base:base_kn が 20_クラス/00_汎用兵科.dat。source line/SHAはreportsの監査JSONに格納。
- baseへ直接親参照する宣言259件（unit11/class248）。候補連鎖でbase二重候補に到達するのは6041/8666件。他は候補を一意に終点までたどれる2601、途中で未宣言親名を踏む24。source graph最長の既知prefixは6。
- これはUnit/Class両方を調査候補として検索する際の構文上の分類である。原作nativeが同じ候補名前空間で検索する・二候補のどちらを優先する・どの値を継承するかは未確定。古いゲームに実際のバグがあるという報告ではない。
- unit:tnok→unit:base2→unit:base1はparent baseで停止、候補unit:base/class:baseを勝手に選ばない。class:baseにはparent base_knがあり、両候補を同一扱いできない。

## 実セーブ3件との相互照合
- 既存のsaved_unit_definition_bridge（保存Unit+0x1Cと原DAT名前の一致）を使い、元のsav SHA256 gateと原DAT manifest SHAを照合。これはgameplay内の真のclass bindingを証明しない。
- save1: 7355保存Unitのうちbase親衝突候補へ6150、候補rootまで一意1201、DAT宣言名不一致4。
- save2/auto: 8763保存Unitのうちbase親衝突候補へ7428、候補rootまで一意1331、DAT宣言名不一致4。
- DAT名不一致4は bakushin+0 / dammy_ru+0 / dammy_sakerobo+0 / knnnnk+0。出典未確認の代替親を合成しない。
- 候補rootまで一意はsourceヘッダの名前連鎖の意味であり、class=合成、variant、level、skill2、runtime HP/MP・battle参加が証明されたわけではない。

## Skill / Skillsetの親候補調査
- skill 16554件: 同種名でrootまでたどれるもの16515件、親が直接または途中で見つからないもの39件、うち直接欠落37件。最大候補連鎖6。
- skillset 106件: 今回索引の全件がparent指定なし。
- これはソース構文の網羅性。nativeのskill抽選、MP消費、next/next2、status、範囲、命中、AI行動の正しい再現ではない。存在しない親tagを暗黙に補わない。

## 保存逆コンパイル・逆アセンブル証拠と次の研究課題
1. A/T005 と B/T011：unit:base / class:baseのnative parent lookup優先、same-kind/other-kind scope、継承後のscalar/array/mapコピー、variant優先とUnit factory実効値を元命令で立証。Wikiでの名称優先規則を同梱EXEの直接証拠に代用しない。
2. 保存Ghidra ZIP recovered_source/peer_script01_ghidra_named_decomp_20261011.zip内、decomp_0050xxxx.c の 0x50BF60 は Win32 FindFirstFileA(*.dat) を列挙後、0x5116B0(..., &LAB_0050BF00) で明示ソート、さらに下層フォルダをqueue方式で巡回する形。だが比較述語LAB_0050BF00は独立関数として10,257関数indexに無く、既存exe/*.txtの保存native検索でも当該アドレスの命令本文を確認できなかった。ネイティブの相対file rankはUNKNOWNである。Path.rglobのsorted順を原作とみなさない。
3. 既存A/T005の保存命令0x464B41..0x464B49には特定property fallback検索で50回境界がある。しかし今回のsource親候補連鎖最大6とnative探索loopが同じアルゴリズムであることは未実証。
4. B/T011へSkill header欠落39件の親tag・影響子リストを提供可能。Skill実効状態の実装は既存native capability/kind、Skill fieldsとruntime Unitの接続が先。
5. E/T018：旧EXE合法UIの同入力・同乱数・同条件によるbattle Golden=0。新エンジンstrict MATCH=0。静的source/保存BYTE試験とは別証拠として維持。

## 安全な独立実装と試験
- 新規 src/hakushin_compat/native_parent_candidate_audit.py: 親名の候補連鎖をimmutable mappingで記録し、CROSS_KIND_COLLISION / MISSING_PARENT / CYCLE / DUPLICATE / UNIQUE_CANDIDATE_ROOTを分類。
- CandidateParentPath.require_resolved_native_lineage()は、候補が一意でもnative実際の継承は不明なので必ず拒否する。元のHP/MPやskillを推測で埋めて本番Unitへ流入させない。
- inspect_saved_unit_parent_impact()は実セーブsource名参照と原DAT SHA manifest整合のみ。audit_single_kind_parent_candidates()はskill/skillsetのヘッダだけ調査する。
- 専用test_native_parent_candidate_audit.py 13/13 PASS と test_native_single_kind_parent_audit.py 6/6 PASS。syntheticで欠落/循環/重複を試験。実データで元590DATとsave1/save2を固定SHAチェック。
- reports/PARENT_CANDIDATE_CONFLICT_AUDIT_20261011.json に監査値と出典、原sav本体を含まない保存ID標本を記録。原DAT/scriptやゲームEXE/画像/音声は無改変。
- 旧本家ゲーム挙動を実証していないため、研究MASTERのTask DONE、原作strict互換PASS、製品EXEの実装完成を増やさない。

## 実装へ移行できる条件
- A/B担当の根拠VAとreg/stack/メモリ演算から、親lookupの選択優先が確認できた部分だけを具体的な兼容データ組立として追加し、別途合成/元EXE観測goldenを比較する。
- 一度に全関数のGhidra出力をコンパイルするのではなく、原作に必要な動作をsource化してビルド可能なゲームエンジンへ統合する。遊べる仮ルールは別のHakushinPlaytest EXEで隔離し、原作再現度へ算入しない。


## 追加: 同名baseの宣言値は実際に異なる
- 元DATの単独source preview（native実行ではない）で unit:base は attack_max=130、HP宣言なし。
- class:base の既知候補親連鎖 class:base→class:base_kn から得たpreviewでは attack_max=180、hp=10000。class:base自身がすべての値を直接宣言しているわけではない。
- この差は「同じbaseならどちらでも同値」という逃げ道が成立しないことを示す。反面、native lookupがどちらを使うか、そもそも同一field copyがどうなるか、実戦でこの値がどう効果を持つかは未証明。
- 比較の出典・値・警告は reports/PARENT_CANDIDATE_CONFLICT_AUDIT_20261011.json の base_branch_source_contrast に、実際のソーステストは test_native_parent_candidate_audit.py に保存。


## 追加（保存Ghidra＋x86 caller直接照合）：汎用検索APIは構造種類パラメータを持つ
- saved Ghidra decomp_0046xxxx.c 0x465060（既存自動名 Prop_LookupParentChain）の署名は、param_2が種類文字列、param_3が対象名の候補として追える。先頭でparam_2をバッファ化→0x462B30で登録表候補を取得し、その木でparam_3を検索→superを最大50境界で探索する構造が読み取れる。Ghidra推定型/ABIは元のx86レジスタ証拠で補強が必要。
- 別系統の保存native一次命令 exe/T006_CORE_HANDLERS.txt VA0x4A18CC..0x4A18E2 は literal event をpush、literal block をECXへ配置して0x465060 call。exe/T010_PHASE_DISPATCH_CORE.txt VA0x432FA1..0x432FB5 にもpush literal event、ECX=literal block の同型呼出が存在。従って**少なくともイベント・ブロック検索の一部では種類を明示指定している**ことは命令列から確証できる。
- この証拠によって、原DATに同名unit:base/class:baseが存在することだけでは、「原作が6,041宣言の継承時に曖昧」とも「unitが優先される」とも断定できない。**原作は呼出元が指定する種類で検索結果が変わる可能性があり、従来のcollision件数はあくまでユニットとクラスを無差別集合にした構文調査の診断件数である**。
- 最重要P0は、Unit/Class構築時の0x465060/0x464290/0x4647D0系呼出元が、具体的にどのkind文字列/レジスタとどの順序で同名baseを検索し、その返り値をどのfield consumerへ渡すかをA/T005・B/T011所有資料で静的同定すること。イベントでblockを使う実例からUnit/Classの優先順へ一般化しない。
- saved native callerの出典は既存ローカルTXTのみ。旧EXE・Ghidra/REA新規起動なし、原本/他owner不変更。厳密互換Golden0。


## 追加（T011保存静的callsite）：Unit/Classを別々に問い合わせる実在caller
- 全関数Ghidra ZIP decomp_0058xxxx.c の0x588470 (FUN_00588470) と0x58A650 (FUN_0058A650) をread-only再読。両関数はUnit相当object+0x1C stringから型名 unit を渡して Prop_LookupParentChain(...,unit,name,0)、同object+0x54 stringから型名 class を渡して Prop_LookupParentChain(...,class,name,0) を別々に呼び、結果を後続処理へ渡す静的分岐を含む。
- B所有exe/T011_STRUCTURE_DISPATCH_PROBE.txt VA0x5885CA..0x588605の保存nativeは、+0x1C文字列取得→0x627784 push→0x465060 call。0x627784は保存exe/T014_ENTITY_MARKERS.txtに literal unit と明示されている。+0x54 class側は現時点で保存Ghidra疑似Cによるためnative ABI/効果の同一性はさらに要VERIFY。
- 後段GhidraにはUnit側のproperty有無を確認して、別Class側のproperty有無に応じて異なる処理へ進む分岐がある。全Unitが単に同名unit:base/class:baseのどちらか一方を親採用するようなモデルを、これだけから固定しない。
- また、実save1の保存Unit+0x1Cに照合できる原DATタグの多くはclass名称（6725/7355件）。よってこの二つの局所関数だけからUnit一般への優先順位・fallback・typed registryの効力を無条件拡張できない。
- 結論は「タイプを明示したunit/class別検索の実callerが存在」まで高確度で、gameplayでbaseのnative実効値が確定したわけではない。Owner研究B/T011の資料を直接修正せず、この引継ぎ記録から依頼対象のVAを特定する。
