# Stage13：戦闘開始情報は全取得できているか――実バイトの網羅性検査
研究ID：BRIDGE-20261022-RESEARCH-13。2026-10-22 JST。
対象：9cddfc86 / b8419f5d の原作実戦中8RAW、元SUMMARY/READY/FAILURE/EVENTS、SHA一致原作EXE。
原本SHA256：E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
結論：**全取得には到達していない。** 現行v7の成功は陣営・部隊・Unit参照などの構造保存であり、外部EXEへ渡せる完全な開始状態の保存ではない。
本runは保存済み実バイトと原作PEのオフライン解析のみ。原作プロセスへのアクセス、起動・書込・フック、セーブ変更、GUI/core/v7変更、Work、MASTER/他レーン、Git/pushは実施していない。

## 1. 8RAWを実バイト単位で検査した結果
各Unit参照は同一Unitを別時刻に繰り返し観測しているので、延べ4,190件を「4,190人」と数えない。
| 対象 | 8RAW全体での保存状況 | 判定 |
|---|---|---|
| Unit+1C8の記録参照、Unit+1D0の部隊参照 | 延べ4,190件すべて有り | 参照先の実値・恒久IDまで取得した意味ではない |
| Unit+90/+94のHP/MP領域 | 延べ4,190件すべて無し | 現在のHP/MP値は分からない |
| Unit+98..E4の能力・状態領域 | 同4,190件すべて無し | 型別の完全意味や全バフを解明したとの主張でもない |
| Unit+214..230の座標等の候補領域 | 同4,190件すべて無し | 実配置を原本の初期DATから補完しない |
| Unit+1CC・+178一覧・+1E4B4キャッシュ・+1E594リンク | 同4,190件すべて無し | 生成元・一時Unitの寿命等は未確定 |
| E+1EED44/48のSide pair、+1EED4C/50の勢力pair | 全8件有り | 今回新たに意味を結合した |
| E+1EED60/64の戦闘時計、+68の終了gate | 全8件無し | GUIに出るframe_counterはGameTask-passの値で、戦闘時計ではない |
| E+1EED78/88/98/A8の4本のVM stack header | 全8件無し | 実行ブロック・PC・モード・frame種別の中断位置は未取得 |
| G+1EF570のマップ管理領域、E+1EECC4の入力候補 | 全8件無し | 採用map/地形実体の未取得を維持 |
| CRT slot-index global、native limit tag/current | 全8件無し | 動的な乱数状態・時間制限も未取得 |
検査したのは必要な主要範囲で、原作の全状態を列挙し尽くした証明ではない。未読値を0/defaultで置き換えずABSENTと保存。
証拠：BATTLE_STAGE13_INPUT_COVERAGE_20261022.json、analyze_stage13_packet_coverage_20261022.py。

## 2. 保存済みの未解釈領域から、攻撃・防衛の対応を新たに確認
原作0x493630の変数反映をPEバイトで確認：E+1EED50→文字列@battleattack、E+1EED4C→@battledefense。元A/T010/T006の静的知見と整合し、知見そのものを重複READY計上しない。
Side初期化0x514A80は+14に第1引数、+18に別byte、+1Cに別参照を書き込む。8RAWのSide+14と上記勢力pairを実ポインタで照合し、今回の全8件でSide0/Player=攻撃勢力、Side1/Enemy=防衛勢力、Side2は未使用側と対応した。
HelpMapのPower参照も全8件で防衛勢力に一致。Stage12で参加表の3項目目がEnemy部隊先頭8件と対応した結果に、原作の攻撃・防衛勢力の意味を加えられた。
これは今回の2戦に限定した実測であり、Playerは必ず攻撃側という一般則ではない。勢力の恒久ID・表示名は今回も未解決。別PID間の生pointer比較で同じ勢力とみなさない。
特に、今回のSide0+18は1、Side1+18は0だが、HelpMap側のside_byteは1で防衛側へ結び付いている。同じ1でも別構造では別の意味を持ち得るので、共通のattack/defense boolへ潰さない。
E+1EED44/48は8件すべてSide1/Side0の順だった。元配列順Player/Enemyと、終了判定のside pair順は異なり、出力schemaには別々に保持する。

## 3. マップ形式を解読済みでも、当該戦闘のマップを取れたことにはならない
T007の原作map形式と可逆parserは既存成果として再利用できる。しかし当該実戦で採用されたファイル・動的地形・配置の実値は8RAWにない。
原本0x48D6A0のPEで0x48D801 LEA EDX,[GameManager+1EF570]、0x48E15A LEA EAX,[GameEvent+1EECC4]、0x48E180 CALL0x4F0BE0を確認。Ghidraソースでは後者にCreateFileA/ReadFileによる読込経路が存在する。
別枝の0x48DFFDと0x48E0ECでは0x4F08E0を呼び、既存領域の破棄・寸法/作業領域初期化等へ進む。全戦闘が1つのmapファイル名だけで再現できるとは仮定しない。生成/空間初期化側の完全意味・実採用枝は未検証。
最低限、採用ファイルまたは非ファイル構築経路、実寸法、field/object/grid状態、配置と衝突状態を区別する必要がある。ファイルSHAを取るだけで原本のruntime地形と一致するとは保証しない。

## 4. 乱数取得で原作関数を呼ぶ案に副作用の注意
既存のCRT乱数式と__getptd+14の状態参照は再利用するが、原作0x5BC630(__getptd_noexit)は単なるgetterではない。
PEでglobal0x65A9A4由来index→関数pointer取得/呼出、戻りNULLなら0x214byteのcalloc、indexへの登録、初期化、現在Thread IDの格納を確認。既存データの有無で内部状態を作成し得る。
したがって「乱数状態を読むためだけに原作の__getptdを実行」することを読み取り専用の採取とは扱わない。rand()呼出は乱数そのものを進める。別WorkerのCRT状態とも同じではない。
必要なのは対象の元ゲームthread/fiber contextに紐付いた既存stateの同時点の観測。実address解決と動的照合は未達で、固定seedや別スレッド値を代入しない。

## 5. 8RAWは開始瞬間の固定スナップショットではない
先の戦闘の最初のRAWはTask-pass63→89、後の戦闘は73→94。全8RAWの採取中差は19～101。これは原作Task-pass指標であり、描画frameやbattle-tick回数と同一視しない。
現行collectorはmode2/active1を外側からpollして動作中の各配列を順に読むため、最初のnative tick前という保証はない。0.1秒の監視間隔や高速化だけでは同期点の証明にならない。
一貫した開始情報には、開始経路と初期化済み条件を固定し、元スレッドの更新順/VM/乱数/寿命を保つ取得境界の検証が必要。既存0x4B99CD/CALL-return0x4B99D2は静的候補のみで、実フックを行ったことはない。

## 6. 最小受渡し仕様を7群に分けて記録
BATTLE_STAGE13_PACKET_REQUIREMENTS_20261022.jsonに、参加関係・Unit詳細状態・runtime map・時計/limit・RNG・VM/Task・同時点handoff/returnを分離した最低限の要求を保存。
これは全エンジン状態の完全inventoryではない。nativeのVMやOS構造全部を別EXEへコピーすべきという仕様でもない。原作側に状態を保持する設計なら、その状態を壊さず一度だけ中断/続行する境界を別途実証する。
取得の優先は中核の値と参照を先に保存→補助Task型調査を別段階→欠落と時間整合性をoffline判定。補助調査の上限失敗だけで中核成果を無効にしないが、中核が未完でも「採取成功＝G1完了」にもしない。
今回は現行採取器・GUIへ追加実装せず、設計と証拠監査に限定した。今すぐ同じ戦闘を増やす必要はなく、次の取得改修に必要な項目を具体化できた。

## 7. 検証・保存・進捗
解析器：analyze_stage13_packet_coverage_20261022.py。機械証拠：BATTLE_STAGE13_INPUT_COVERAGE_20261022.json。
検証器：validate_stage13_packet_coverage_20261022.py。結果はBATTLE_STAGE13_VALIDATION_20261022.jsonを正本とする。実戦の追加実行数ではなく、保存済み実戦データ・元PE・欠落判定を照合する検証。
元12証拠ファイル、SUMMARY/EVENTS、採取コード4本の元SHAを前後照合し、原作PEの18局所命令・3変数名文字列・3つのmap setup callとHP/MP参照命令を保存した。
最新入口BATTLE_BRIDGE_RESEARCH_INDEX.mdとBATTLE_BRIDGE_FINDINGS_LEDGER.jsonlへ増分登録する。旧RAW/SUMMARY・他レーン・MASTER・原本EXE・セーブ・採取ツールを変更しない。新ZIPも作らない。
Work引継ぎの客観的ゲートは3/9、完全G1は未達。従来の参考値51.75%は今回再推定しない。これは完成率や成功確率ではない。
次回の焦点は、これら未取得項目を含む段階別の採取設計と、本当に同一時点へ固定できる原作境界の検証。単にRAW件数を増やすのではなく情報の意味と時点を揃える。

## 復旧・限定事項
RC13-ENCODING-01 RESOLVED：初回のread-only資料検索でPython標準出力がcp932のままのためUnicodeEncodeError。原本やファイルに書込む前の表示失敗。子プロセスにPYTHONIOENCODING=utf-8を渡して同一資料の再読取り成功。接続権限・安全制約を変更していない。
原作の未知領域・別mode・間接callback・追加乱数源・同時更新を全て解明したとの主張はしない。旧レーンの静的知見は再利用であり、新規READYとして二重計上しない。
