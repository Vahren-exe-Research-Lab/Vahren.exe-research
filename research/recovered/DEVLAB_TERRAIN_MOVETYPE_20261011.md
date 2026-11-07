# 迫真戦記 ver0.67 — BF-07 地形・移動種別の原DAT検証（2026-10-11）

## 背景・独立担当
Claude CodeはUnit/Class型別レジストリ・親継承の原作native解析を担当中（画面時点は手順6/9、最終結論未確認）。本制作DEVタスクはこれと重複しない戦闘地形・移動種別に限定した。5レーンのMASTER cp83・所有プロトコル・git dirty・既存B資料を確認済み。研究A〜E・Claudeの継承解析・dirtyのGUI/loaderには手を触れていない。

ユーザーは憶測で元ゲーム性を作ることを拒否しており、原作データ・EXE/保存nativeから確証できたことだけ新ゲームへ反映する。**この文書で確認したのはあくまで原MAP・原DATの関係**。原作ゲームでの物理的な障害判定、移動速度、当たり判定の正規命令は今回未立証。

## 原作地形と移動データの全量観測
- 完全解凍豪華版 ver0.67、a_default/stage の151ファイルすべてを既存byte-exact map codecで読取専用デコード。terrain（kind0）は合計 **2,055,881レコード**、ユニークタグ **223種類**。
- a_default/script の590 DATを既存保守的 top-level ASTで静的解析。field **276宣言**、movetype **33宣言**。Unit/Class・Skillの親レジストリ解析とは別namespace。
- kind0 map tagからfield同名定義へ対応でき、raw attrまたはfield同種類の親を追ってattrを取得できたレコードは **2,030,182件**。
- source fieldは存在するが親連鎖にattrがないもの **25,694件**：highland_128_coll が24,382、highland_128_coll_w が1,312。
- source field宣言自体が見当たらないもの **5件**：sea2=3、stone1_k=2。この5件を推測で別タグに割り当てない。
- highland_128_coll は元DATで type = coll、alt = 128 を宣言。highland_128_coll_w は alt = 128だが type=coll はコメントで、アクティブ属性として扱わない。**collを必ず壁/通行禁止として実装できるnative証拠は未取得**。

## source attrごとの地形レコード数（直接・継承含む）
sea=619820、grass=588206、road=174638、mud=163752、snow=137454、rock=116256、sand=115177、wood=103302、mersh=11577。これらを合算すると2,030,182件。

## movetypeの元の整数値
- 原作script/movetype.datの33 movetype宣言はそれぞれ consti = attr*integer,... を持ち、**33/33の生トークンを欠落・重複なく構文解析**できた。
- raw例 normal: grass*6, sand*4, wood*3, rock*3, mersh*3, sea*3, road*6。normalにmudトークンはない。
- raw例 ship: grass*0, sand*0, wood*0, rock*0, mersh*0, sea*5, road*0, snow*0, mud*0。
- 上記から確定できるのは「文字列属性名→元DAT数値」の対応のみ。値が0の時と、トークンが記述されていない時は**必ず別扱い**。ゼロを通行不能、整数を速度倍率、欠落をゼロとするには原作の登録・参照・計算式が必要。
- raw field属性は各地形宣言と同種類の親宣言から探索。親が欠落／循環／重複／variant/明示@の場合は未確定としてfail-closedする。

## 新エンジン用read-onlyデータ接続
- 新規 src/hakushin_compat/terrain_movetype_source.py：入力をraw DAT + raw MAPとし、原ソースSHA manifest、全tag件数、field属性・親の出典、33種movetype raw consti tokenをimmutableなデータ索引へ変換。
- pair(terrain_tag,move_type)はSOURCE_ATTR、CONSTI_TOKEN_PRESENT / CONSTI_TOKEN_ABSENT / UNKNOWN_FIELD_ATTRIBUTEを区別する。
- SourceTokenLink.native_passable()は**どの値でもNativeTerrainBehaviorUnverifiedを発生**させ、原作の当たり判定を捏造しない。新EXE試遊モードの仮移動ルールとは接続しない。
- 元のDAT/map EXE/実saveを変更せず、ログ・レポートにゲームの元raw asset bytesやPC個人パスを出さない。

## 検証
- 新tests/test_terrain_movetype_source.py：合成MAPによる同種類field親attr、explicit 0とトークン欠落、type=collを通行不可扱いしない検査、未知/循環/無効値の拒否、実590 DAT+151MAPの全件count、原本SHAとmtime不変、実ship/normal対応を確認。
- 専用10件 **10/10 PASS**（再実行最終確認の結果を優先）。これは原作物理移動の同条件goldenではない。
- reports/TERRAIN_MOVETYPE_SOURCE_AUDIT_20261011.jsonには、原作ソースSHA、223tagの使用回数・親出典、33profileの整数テーブルと未知を区別する状態を記録。
- 原作EXE gameplay actual Golden **0**、新エンジンstrict MATCH **0**。動的通行試験は未実施。

## 今後の逆解析の的
1. **B/T011,T013/T012**または担当合意した新DEV独立解析で、元EXEがUnitのmovetype定義を読んで、地形属性・consti整数・座標へ適用する具体的なconsumer/callsiteを特定。field attr、type coll、alt/smooth/member、欠落constiのfallbackを別々に確認。
2. Bレーンが既に追う0x4E5040/0x4E4C70/0x4C59F0等の座標更新・候補方向/障害判定を**新しい研究で重複実行せず**必要な情報だけ参照し、意味が不明なhelperはUNKNOWNのまま置く。
3. 元ゲームの合法戦闘UIで、同条件の平地・海・高地・障害付き移動、通常/船/飛行系の差を実測して native source vs UI Goldenを照合。ユーザーの口頭説明を根拠にしない。
4. 根拠が揃ってから試遊側の任意地形自由移動をstrict modeの正しいルールへ差し替える。現時点は既存HakushinPlaytestの仮物理を変更しない。

### 安全・並列境界
原本・B所有data/exe/handoff・E MASTER・既存GUI/F3/逆コンパイルZIP・Git stage/commit/push、Remote、automation変更なし。制作側dev_labに新ソース・新test・本doc・reports JSONのみを追加。次回も最初に最新git status・レーン所有権を再確認すること。

## 並列Claude作業の読取専用確認（同日・後続）
- 開始時のユーザー画面ではUnit/Class同名parentの追跡はステップ6/9。今回の地形解析を実行している間に、共有dev_labへ新規の未コミットsrc/hakushin_compat/peer_script01_native_definitions.pyとtests/test_peer_script01_native_definitions.pyが現れた。
- この新コードの冒頭資料は、0x50D650の種別ごとのstd::map初期化、0x464290/0x4647D0/0x465060/0x465770で同kindのsuper検索、0x585AD0でUnit側のscenario variant→Unit通常→Class側variant→Class通常の順というstatic x86証拠を記述している。Unit/Class親優先を解明する上で前進の可能性が高い。
- ただしClaudeの編集完了状態・独立x86検証・実ゲームGolden・本人の最終報告は本制作DEV側で確認していない。これらのdirtyファイルは**read-onlyで眺めただけで改変・実行・stage/commitなし**。該当レーンの検証が済むまで本地形監査から依存しない。
- 当方は原作151MAP/field/movetypeソースの独立read-only紐付けと10/10専用テストに集中し、ClaudeのUnit/Class解析と重複していない。
