# P0 M/L: 保存証拠・現在SAVE独立監査
研究ID: P0_TAKEOVER_20261024_01。担当exit_hij。保存資料読取とオフラインparseのみ。原作操作・attach・SAVE書換・新試験なし。
EXE SHA: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（親現物照合＋本担当H/I/J PE読取と一致）。
V9 SHA: 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE。本監査は保存証拠と既存wire parser、V9新query不要。
結論: 手動save1/2は現在byte同一のLOAD候補。既存8RAWは構造証拠として受理、G1一貫開始/G5戦略Goldenでは未受理。autoは監査中にコピー側だけ別hashになった。

## 現物SAVE照合
SAVE_HASH_QUICK.jsonの採取時点はoriginal/game_copy 5/5一致。SAVED_EVIDENCE_AUDIT.jsonでは各SAVEを順次read→parse→hash再確認した。
| name | original bytes | original SHA256 | copy結果 |
|---|---:|---|---|
|save1.sav|5855610|30269789DC954EB60DBA0F3B906C58A57C8E1C5B90F122D1949C27F8B8F107E4|一致、処理前後不変|
|save2.sav|5859022|F106A64A6E791601662C68C498085A34E9D73409BE30A0356B21F05295070DF9|一致、処理前後不変|
|save3.sav|5855610|3728603D180E353A6B4FCE6DB8229E32D0BAF31802F5E30206B4C7CAE0F24E9E|一致、処理前後不変|
|auto.sav|6089846|871FA2717011EB118FC6E5D1CD5BAE52AC6A58128728713FFA6594F1E1386A82|quick時一致、詳細時16A46584F1EC53100583C41803BCF386B0C520CCD566585361C7AFC70D6745E2|
|global.sav|141|D3CA8A61476E1B97E4D73D749445292B91FFEDDC6F2F155CE5939A9D62E624C0|一致|
auto変化のwriter/時刻は本監査では不明。親の複製runtimeと時間的重なりはあるが原因断定しない。詳細autoの元側は同じ871FA...のまま。全保存を同一時刻の原子的snapshotと扱わない。
save1/2のfullwire全section消費、再構築暗号文一致を確認。両方scenario sci1 / power po2 / checkturn候補6。checkturnを画面の実turnへ自動昇格しない。
save3/autoはfrontmatter再暗号化一致、leading_u32_unlabeled=3だがfull parserでgraph末尾未消費。破損認定ではなく未対応保存variant候補。runtime LOAD成功/失敗は本担当未観測。

## 今回の合法LOAD候補
- 第一候補save1、代替save2。理由は現物identity、全wire再構築一致、原作同梱正常LOADの検証入力を固定できること。合法LOAD・攻撃成功は親の実機確認待ち。
- 現在両SAVEのpo2 Spot refsはsp2,sp24,sp49,sp50,sp7,sp7b。sp2の保存Unit refs128、sp16は48。sp16のPower refsは空。これは保存参照であり実出撃人数/中立陣営確定ではない。
- CURRENT_SAVE_ROUTE_CANDIDATES.jsonで両現SHAのpath sp16+sp2、endpoints sp2/sp16、route名route、byte88=1を再parse。従って画面確認候補はpo2/sp2→sp16。
- 元BATTLE_BRIDGE_SAVE2_WAR_ROUTE_20261021.jsonは旧SHA45CCEF306B56BF66810726436365207CA18B63D7CC0E432E784034D196FA5635/5558753B専用。新SAVEに旧戦況・名簿・操作列を流用しない。
- 親の入力手順はLOAD対象slot/SHAを先に固定→画面のscenario/勢力/turn/領地所属→source/targetの合法選択→実際に確定されたSide/Troop/Unit/MAPを採取。graph path存在だけで攻撃合法PASSにしない。
- save3/autoは固定正常LOAD候補として優先しない。global.savは通常SAVEではない。autoは可変なので同じ名前で前後証拠を接合しない。

## RAW8件・watchの独立受入監査
- SAVED_EVIDENCE_AUDIT.json: 元SUMMARYのREADY2+RAW8+FAILURE2計12receiptの現物SHAが12/12一致。collector4本も両SUMMARY期待値と一致。新しい原作採取ではない。
- RAW_WATCH_AUDIT.json: RAW内guardを直接読取り、8件全てstable=false/frozen=false。Task-pass差は9cddfc86=26,19,68,55、b8419f5d=21,34,77,101。最初も63→89/73→94で開始tick0ではない。
- pid28432と32468の2sessionを別runとして保持。別PIDの同じpointer値を同一Unitへ接合しない。
- 9cddfc86の記録上active開始16:31:09.851534 UTC→active0 16:32:42.123141→mode1 16:32:44.520240。
- b8419f5dは16:46:32.185603→16:47:26.822051→16:47:28.680895。これらはpoll観測時刻でnative命令の実行時刻ではない。
- 旧Watch1/2も現物SHA一致: 9DF9A0D8...62A7/234行、1D60CC8C...4B46/85行。同PID23272でも異なる時間窓。RAW8件のrunへ加算しない。Watch complete packet成功0。
- Stage13の既存coverageは延べ4190 Unit参照にHP/MP(+90/+94)、能力(+98..E4)、配置(+214..230)、owner候補+1CCが欠落。実MAP、battle clock、VM stacks、RNGも未読。今回このcoverage計算は再実行せず既存SHA固定資料を解釈。
- b8419f5d最後はSide1=200に対しTroop member=203。poll中更新の可能性があり欠けた3名を補完しない。既存Stage11既知成果で新規発見加算なし。

## G5 Goldenに不足するもの
G0合法UI/Spot同定、G1同run直前SAVE byte+SHAと入力列、G2実MAP/攻防支援/順序付き実出撃名簿、G3終了直前、G4復帰後の可視世界差分を一つのbattle epochへ結びつける必要がある。
mode1復帰・active0・AttackMap残留だけでは勝敗/死亡/経験値/財政/占領の一回commitを証明しない。旧VM/Taskの再開や同callback内順序もpollでは判定不能。
現行SAVEの構造解読は同run戦闘直前SAVE証拠ではなく、Spot Unit一覧も実出撃名簿ではない。旧保存map候補s16.mapを実MAP欄へ代入しない。
G5には原作の合法条件を固定したbaselineと新実装同条件の出力・build/source/input/capture SHA、結果比較が必要。旧新実測がなければNO_STRICT_COMPARISON。保存資料だけでactual Golden PASS/strict MATCHを増やさない。
B限定G0（申告+mode遷移）、E受入G0-G4、bridge G1-G6は別namespace。番号一致を同じ達成条件と扱わない。
親が進める今回runtimeの証拠は別runであり本監査旧RAW/Watchの不足を遡って充足しない。

## 出典・再開
一次: 現在original/game_copy SAV、2 SUMMARY/12 receipts/2 EVENTS、RAW内guard、旧watch2ファイル。
二次: BATTLE_STAGE11_TWO_RUNS_REPORT、BATTLE_TAKEOVER_RESEARCH_STAGE13、T020_CNB02_RECEIPT_PROVENANCE_GATE、T020_BATTLE_RETURN_COMMIT_GATE、T020_SAME_PID_DUAL_BATTLE_WINDOW_CROSSWALK、T020_NATIVE_PREBATTLE_AND_EXIT_TRANSIENT_GATE。
全出力は専有evidence_audit。元資料・game files・共通索引変更なし。候補parserは既存dev_labモジュールを-Bでimportし、元モジュールやテストを実行/修正せず読取関数のみ使用。
再開: game_copy save1/2の現在SHAをLOAD直前に確認し、親runtimeのrun ID/入力/画面/callsiteと結合する。原作側autoの同時変化を監視する必要がある場合も別receiptで扱う。
