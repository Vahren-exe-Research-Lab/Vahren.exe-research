# EXP-SIMPLE-LIFECYCLE-20261022-02｜簡易戦闘と召喚EXPの破棄境界

更新: 2026-10-22 JST。独立経験値研究、原本EXE/DAT/SAVE・他レーン正本・Work・Gitは変更しない。
状態: STATIC_PE_AND_CURRENT_INDEX_VERIFIED / VERIFY_REMAINING / GAMEPLAY_NOT_RUN。最終結果はCP02以降。
使用索引: rea_lab/headless_analysis/search_index/search_current.py → HAKUSHIN067_CURRENT_CANONICAL_V2_20261022.sqlite。
対象EXE SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
先読: MASTER末尾、ANALYSIS_LANES_PROTOCOL、B HANDOFF末尾、Work依頼キュー、既存EXP索引。以前の拒否領域本文は新規取得しない。

## CP01｜この回で追加した接続（原本機械語の最終照合前）
1. 現行保存擬似Cの0x514AA0は陣営+0x48/+0x58/+0x38の順に配列を走査し、各非NULL objectのvtable[0]へflag=1を渡す。原本x86では0x514ABC/0x514ADC/0x514AFCの間接CALL。
2. 原本PEのPlayer(0x639B08)、Enemy(0x638B60)、DemoPerson(0x638030)のvtable+0x10はいずれも0x514AA0。前回確定の通常Unitと、この回確認したSimpleUnit(0x63A4BC)のvtable[0]はいずれも0x570C90。
3. したがってこの片付け経路に残るUnit/SimpleUnitは、旧証拠0x570C90→0x543E00→0x5450C0→0x5454D0→0x4591F0により、所有する召喚UnitDataキャッシュの解放へつながる。実際のR転送不存在は未証明。
4. 0x40CCF0は2個のDemoPersonを生成。0x40F320は0x544290でSimpleUnitを4つのcallsiteから生成し、BattleWndの実行配列へ登録する。
5. 0x40E2F0は反復処理を持ち、BattleWnd+0x238の配列要素のvirtual+4を実行。SimpleUnitのvirtual+4は0x545740、そこから0x545CC0へ接続。
6. 0x545CC0はSkill kind3の枝で0x551490を呼び、既知の共通EXP helper 0x551E50につながる。SimpleUnit+0x8C=1なら同helper内で条件付き即時Lv判定を行う。全攻撃種別の接続は追加確認中。
7. 0x40E220は結果コード0では描画へ、非0では0x493630→0x40F000→0x48ABF0の順。0x40F000はBattleWndの2陣営へvirtual+0x10を呼ぶ。
8. 0x40E2F0の局所counterは最大500反復、50反復ごとの条件判定がある。ゲームの実時間・UIフレーム数・最終経験値量とは同一視しない。

## 未解決
- 0x493630および下位イベント処理で、召喚用RのEXPが別の永続Unitへ明示的に移されるか。
- 2陣営のSimpleUnit実生成から共通攻撃/回復EXP処理までのnative callsite・引数・型の照合。
- すべてのCPU同士戦闘、途中中断、タイムアウト、親/子死亡、連戦での実機挙動。
- 各phaseの到達順の静的確認と、原作実機での一致検証は分離する。

## CP02｜簡易戦闘の経験値計算に接続できた経路
- 0x40CCF0はBattleWndの2陣営にDemoPerson vtable=0x638030を設定（0x40CD63等）。BattleWnd主vtable=0x638074、副vtable=0x6380CCは0x51D260の原本storeで確認。
- BattleWnd副vtable+4=0x40E220が0x40E2F0を呼ぶ。0x40E2F0の0x40E447はwindow+0x238を読み、0x40E46Eで配列要素のvirtual+4を実行する。
- 0x40F320で生成したSimpleUnitは、返値EAX→EBP（0x40F7AE）、[0x8B8ECC]が指す末尾への書込み（0x40F89C）、末尾+4（0x40F8AB）を経て、同じ更新配列に登録される。
- 0x8B8EC8 - BattleWnd本体0x8B8C90 = 0x238、endは+0x23C。単に同じoffsetが出るだけでなく、生成側globalと更新側this-relativeの一致を確認。
- SimpleUnit vtable0x63A4BC+4=0x545740 → 0x545C5B CALL 0x545CC0。
- 近接kind1: 0x545CC0のvirtual+0x7C → [0x63A4BC+0x7C]=0x546C90 → 0x546DDF CALL 0x550E70 → 0x551167 CALL 0x551E50。
- 回復kind3: 0x545CC0@0x5461FF → 0x551490@0x551C6A → 0x551E50。
- 共通helperは0x551FB2でUnitData+0x16Cへ加算。SimpleUnit constructorの0x5442E4は+0x8C=1/+0x8D=0を設定し、0x551FBAの方式判定と閾値判定を通れば0x551FD3→0x58A650の即時Lv更新へ。
- いずれも条件付き経路。技能の成功条件、経験値無効設定、troop有無、ctx重複、+0x18614等の除外は依然有効。すべての行動で獲得するという結論ではない。
- 限定結論: この簡易戦闘には個体ごとの技能処理と通常系と共通の経験値計算がある。「戦闘後の固定経験値だけで成長する」とするモデルでは不足する。
- 同じ計算関数でも、命中回数・技能選択・対象や戦闘時間が違えば総経験値は異なる。通常戦闘と簡易戦闘の最終獲得量が一致するとは主張しない。

## CP03｜通常参加兵は登録済みUnitDataへ直接書く経路を持つ
- 0x467DE0はcontext+0x300の永続登録ツリーを検索し、node+0x28に格納されたUnitData*を返す。0x467E3B MOV ESI,[EAX+0x28]→0x467E4D MOV EAX,ESI。
- 0x40F320@0x40F761→0x467DE0、0x40F766 MOV EDI,EAX、0x40F7A5 PUSH EDI、0x40F7A9 CALL 0x544290。
- constructorは0x5442C3で当該stack引数をEBPへ取得し、0x54436EでBattleUnit+0x1C8へ保存。この参加兵経路はUnitDataの新規コピーではなく、取得した同じ参照を渡している。
- したがってこの経路で加算されたEXPは、まず登録済みUnitDataのカウンタそのものを更新する。終了時にEXPを一括コピーしなければ一切残らない、という実装ではない。
- 対照: 召喚子は親BattleUnitの一時ツリーに埋め込まれた別Rを+0x1C8へ結び付ける既存経路。共通の計算関数を使っても、記録先の寿命が違う。
- 制限: 具体的にどのセーブ対象インスタンスと一致するか、全参加兵・全シナリオ・全CPU戦闘に適用されるかは実機未観測。上記は追跡できた登録済み参加兵の分岐に限定。

## CP04｜簡易戦闘の決着処理が先、ユニット破棄は後
- BattleWnd callback0x40E220は0x40E27F→0x40E2F0の返値を調べる。返値0なら0x40E28E→0x40D220で表示更新し、決着処理を呼ばず復帰する。
- 非0の枝は0x40E2B9 CALL 0x493630 → 0x40E2BE CALL 0x40F000 → 0x40E2C3 CALL 0x48ABF0。この正常枝で、戦略側結果処理がユニット破棄より先と確認できる。
- 0x40F000はBattleWnd+0x1C8/+0x1CCの2陣営へvirtual+0x10を実行する。これらはUnitDataではなく陣営ポインタ。BattleUnit+0x1C8と同一視しない。
- DemoPersonのvtable+0x10=0x514AA0。同関数は陣営+0x48の通常個体、+0x58の静的個体、+0x38の部隊の順に、非NULL要素のvirtual slot0へflag=1を渡す。
- SimpleUnitのslot0=0x570C90は通常Unitと同じ。既知0x543E00以下の破棄連鎖により、その個体が所有する召喚Rツリーも解放対象になる。
- この回の新規性は、既報の破棄関数単体を「簡易戦闘結果callback→2陣営cleanup→SimpleUnit→R解放」まで連結した点。既知の関数/fieldを新発見として二重計上しない。
- 最重要の未解決: 先に実行する0x493630やその下位イベントがRのEXPを親/別の永続Unitへ移す可能性は、今回も排除していない。後段の解放の存在だけで「必ず失われる」と断定しない。
- 通常3陣営の一般cleanup0x48AA00にも+0x10経路があるが、すべての通常戦闘終了がそこへ到達する証明は今回の範囲外。

## CP05｜500回で返る0は戦闘終了ではない
- 0x40E2F0は局所counterを0から増やし、0x40E617 CMP EAX,0x1F4（500）、0x40E61C JLで反復。上限到達時は0x40E622 XOR EAX,EAXで0を返す。
- 0x40E3CEの0x32（50）による周期判定があり、局所counterが0,50,100,…の時点に陣営の決着・時間制限条件を調べる。
- 別の早期中断でも0を返し得る。0は「この呼出しで決着値を返していない」のであり、引き分け確定を表す値として扱えない。
- 500は1呼出しの内部反復上限。500秒、画面上の500フレーム、必ず500回命中、全戦闘の総上限という意味ではない。
- 再開発上の影響: 続行0で戦闘結果を確定したり、EXPを初期化したり、召喚Rを破棄したりしない。結果確定と単なる処理の区切りを区別する必要がある。

## 検証結果と証拠
- EXP_SIMPLEBATTLE_LIFECYCLE_EVIDENCE_20261022.json: 直接CALL21、vtable8、原本命令32の計61検査が一致。25関数の保存擬似C SHAと必要な行を収録。
- EXP_SIMPLEBATTLE_LIFECYCLE_VALIDATION_20261022.json: 上記61項目を独立に原本から読み直して一致。さらに更新配列登録/constructor returnの命令9、絶対アドレスとoffsetの一致4を確認。
- 元EXEと現行検索DBは解析前後のSHA一致。研究用Pythonの結果がPASSであっても、原作ゲーム実行・実機Golden・新旧互換試験の成功ではない。
- 原作Gameplay tests=0、正式B READY追加0、E MASTER統合0、Task DONE追加0。修復Ghidra本体、他担当正本、製品コード、Git、原本ゲームは更新なし。
- 続きの入口: 0x493630の結果分岐と召喚R参照の結合、簡易戦闘各技能の獲得gate、原作の通常/簡易の同条件比較。今回の発見から全シナリオの数値一致へ飛躍しない。
