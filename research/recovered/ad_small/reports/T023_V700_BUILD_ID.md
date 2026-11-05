# T023 Vahren ver7.0 build 同定メモ
調査日: 2026-10-06

## 現時点の結論
[VERIFY] 迫真戦記同梱engineは「ver7.0系」を意図しているが、2017-10-12版そのものとは考えにくい。
[CONFIRMED] 同梱Vahren.exeはSHA-256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187、size 2,910,720。
[CONFIRMED] PE timestampは1476792537 = 2016-10-18 12:08:57 UTC。ただしtimestamp単独でversion認定しない。
[CONFIRMED] PDB pathはVisual Studio 2010系。Vahren701はVisual Studio 2017系。

## 文字列fingerprint
- target: unit_suck_limitなし / quickreloadなし / offset_onあり / personal_battleあり / no_autosaveあり / assist_skillあり。
- Vahren701: unit_suck_limitあり / quickreloadあり / offset_onなし / personal_battleあり / no_autosaveあり / assist_skillあり。
- 2017-10-12版は公開記録上 unit_suck_limit=25 追加。よってtargetは少なくともこの特徴を持つ10/12 buildとは不一致。
- personal_battleがtargetに存在するため、2017年独立parserで未認識だったことはengine機能不存在の証拠にならない。

## 外部候補
- SoftonicはVahren700.zip、version 7.00、62.94 MB、SHA-256 bb08db97de21956ca1cc9247f8ba3b06f713b2cabeb123d076d7f10d8dd0e3cb と掲載。
- ただしarchive bytesは今回取得できず、内部Vahren.exeとの比較未実施。公式正本扱いはしない。
- 2017-10-12版は実機報告で ver7.00(17/10/12 20:12) と明記される。

## 次の確定条件
1. 上記Softonic archiveまたは同一hashのVahren700.zipを回収。
2. 内部Vahren.exeのsize/SHA-256/CRC32/section/PDB/stringsをtargetと比較。
3. 必要なら8/28版・10/1版・10/12版の既知fingerprintを追加し、targetの枝を特定する。

## bundled target engineの世代再判定（2026-10-06 継続監査16）
[HIGH-CONFIDENCE, exact sub-build VERIFY]
- bundled target `Vahren.exe` は PE timestamp 1476792537 = 2016-10-18 12:08:57 UTC、LinkerVersion 10.0、PDB `[PERSONAL_PDB_PATH_REDACTED]`。
- Vahren701比較は timestamp 2018-05-01、LinkerVersion 14.13、PDB Visual Studio 2017。toolchain世代が明確に異なる。
- targetは`offset_on`をnative文字列/grammarとして保持する。Vahren Wikiは `offset_on` を「v7時点で廃止」と明記する。
- targetには10/12版追加の `unit_suck_limit` がなく、従って2017-10-12 buildではない。
- Wiki一行メモの2016-11-23報告が『Ver6.85o時点』を明記しており、targetの2016-10-18 build時刻と同じpre-v7世代に入る。
- よってプロジェクトreadme上の『7.0へダウングレード』という作者意図と、実際にver0.67へ同梱されたtarget engine binaryの世代は一致しない可能性が高い。
- 現時点の最有力仮説は **6.85o-era engine**。ただし6.85o正本EXEとのbyte/hash比較が未実施なのでexact labelはVERIFYのまま。

[REIMPLEMENT]
- strict compatibility authorityはver0.67同梱binary。『V7互換』というラベルではなくtarget native挙動を優先する。
- Wiki/独立parserの証拠採用では、V7後年仕様よりpre-v7/6.85o時代の記録を優先照合候補に昇格する。

[EVIDENCE]
- `exe/T023_DEEP_FINGERPRINT.txt`。
- Vahren Wiki skill: https://w.atwiki.jp/vahren_ency/pages/378.html (`offset_on`: v7時点で廃止)。
- Vahren Wiki 一行メモ: https://w.atwiki.jp/vahren_ency/pages/16.html （2016-11-23『Ver6.85o時点』）。
- SoftonicのVahren700.zip SHA-256は候補archive情報のみで、target世代認定には使用しない。

## quickreload 時系列fingerprint（2026-10-06 継続監査17）
[HIGH-CONFIDENCE / exact sub-build VERIFY]
- Vahren Wikiの2017年6月17日当時の更新・制作者記録では、標準データのスキルへ `quickreload = on` が追加されたことが言及されている。
- ver7.00公開は同年7月2日。従って quickreload は少なくとも「7.00公開より前の標準データ」で既に使われ始めていた。
- bundled target EXEには exact ASCII/UTF-16LE `quickreload` が存在しない一方、廃止前要素 `offset_on` は存在する。
- これは target が 2017-06-17 より前の pre-v7 系統であるというfingerprintを補強し、2016-10-18 PE timestamp / VS2010 PDB / unit_suck_limit欠落と整合する。
- ただし標準データへの記述追加だけでは、その時点のEXE native handler存在を単独では証明しない。exact 6.85o labelは公式6.85o EXEとのhash/section比較までVERIFYを維持する。

[REIMPLEMENT]
- strict authorityは引き続き bundled target binary。
- quickreload は target profileでは native未対応候補として扱い、後期/V701 profileと分離する。

[EVIDENCE]
- Vahren Wiki 制作スレ/更新記録（2017-06-17 quickreload追加、2017-07-02 ver7.00公開）。
- 本ファイル既存 target raw-string fingerprint。


## exact keyword cross-version matrix（2026-10-06 継続監査18）
[CONFIRMED]
- target vs V701 exact NUL keywordをbinary scanした。
- target: quickreload=0 / unit_suck_limit=0 / event_bg_size=0 / offset_on=1。
- V701: quickreload=1 / unit_suck_limit=1 / event_bg_size=4 / offset_on=0。
- `event_bg_size` はV701で4箇所すべてnative lookup xrefを持ち、fallback=768。targetはliteral自体0件。
- この4-key差は単なる未使用文字列差ではなく、少なくともevent_bg_sizeについてnative機能世代差を直接示す。
- `pre\0` はtarget=0 / V701=0。従来のtarget `pre` hitはhprec/mprec substring誤検出で、version fingerprintから除外する。
- story/fight/friend/politics自体のexact literal countはtargetとV701で概ね同等だが、target story collectorはfight/friend/blockのみを参照する。
- exact sub-build labelは引き続きVERIFY。ただし bundled target が2017後期7.x native feature setより古いという証拠はさらに強化。

[EVIDENCE] `exe/T023_KEYWORD_MATRIX.txt`, `exe/T009_EVENT_BG_SIZE_CROSSVERSION.txt`
## save_name feature boundary（2026-10-06 継続監査23 checkpoint 1）
[CONFIRMED-CROSS-VERSION]
- bundled target EXE は exact NUL `save_name` を ASCII/UTF-16LE とも **0件**。
- Vahren701 EXE は exact ASCII `save_name` を2件（VA 0x63888C / 0x63A7BC）持ち、`.text` direct xrefも 0x590869 / 0x5AD8D5 の2件を確認した。単なるdead stringではなくnative consumerが存在する。
- V701側の文字列近傍は一方が `open/load/.sav/auto.sav/save_name/no save/name/scenario`、もう一方が `open/.sav/save/save/save_name/scenario/auto save/no save` で、load/save UIとscenario propertyの双方に接続する。
- 同じextended matrixで target は `no_autosave/personal_battle/assist_skill/ground` を保持し、V701にも存在する。一方 `quickreload/unit_suck_limit/event_bg_size` はtargetに無く、`offset_on` はtargetだけにある。
- よって `save_name` 欠落は bundled target が後期7.x feature setより古いことを示す新しいnative feature boundary。`ground` 等の存在だけを後期build指標にしてはいけない。
- 現行Wikiの7.01更新詳細は `save_name/no_autosave/personal_battle/assist_skill/ground` を「以前のいろいろ」と列挙するが、targetではその集合が一様に実装されていない。後年Wikiの機能群をtargetへ一括適用しない。

[REIMPLEMENT]
- strict target profileではscenario `save_name` をnative-supported fieldとして扱わない。後期/V701 profileのみfeature gateで有効化する。
- exact 6.85o label自体は正本EXEとのbyte/hash比較までVERIFYを維持する。

[EVIDENCE]
- `exe/T023_EXTENDED_KEYWORD_MATRIX.txt`
- `exe/t023_extended_keyword_probe.py`
- `exe/t023_save_name_xrefs.py`, `exe/t023_save_name_context.py`, `exe/t023_save_name_strings.py`
- Vahren Wiki「最新版の更新詳細」7.01ページ（save_name等は「以前のいろいろ」）。


## PE version resource / 2016-10-18 save_name boundary（2026-10-07 継続監査29 checkpoint 4）
[CONFIRMED-TARGET]
- bundled target `Vahren.exe` のPE resourceを `pefile` で再走査したが、VS_VERSION_INFO / StringFileInfo / VS_FIXEDFILEINFO は存在せず `NO_VERSION_RESOURCE`。従ってFileVersion/ProductVersion resourceからexact sub-buildを直接復元する経路はない。
- target PE timestamp `2016-10-18 12:08:57 UTC` はJSTでは `2016-10-18 21:08:57`。
- 当時の改造・制作スレでは同日 `2016-10-18 23:00:34 JST` に、scenarioの保存表示名を `savename=` で別指定できるようにしてほしいという機能要望が投稿されている。target timestampから約1時間51分37秒後である。
- target native scanでは exact `save_name`/`savename` consumerがなく、V701には `save_name` consumerが存在する。したがって「2016-10-18 target時点ではsave-name override未実装」というchronologyはbinary evidenceと contemporaneous report が一致する。
- Wiki一行メモでは2016-11-23に明示的に `Ver6.85o時点` と書かれた報告、2017-02-17にも `Ver6.85oで確認` がある。現行IF一覧は「戦いの序幕・Restructure」を `6.85oのみ本体同梱` と記録する。

[INTERPRETATION]
- 以上はtargetが2017後期7.xではなく2016秋の6.85系統に属する証拠をさらに強化する。
- ただし `6.85o` の公開日/正本EXE byte fingerprintとtargetの直接一致は未取得。2016-10-18 targetをexactに6.85oと断定せず、**6.85o-era / pre-v7** をHIGH-CONFIDENCE、exact labelはVERIFY維持する。
- exact版確定条件は依然として当時配布された6.85系Vahren.exeを取得してhash/section/code/data fingerprintを比較すること。

[EVIDENCE]
- `exe/T023_VERSION_RESOURCE.txt`, `exe/t023_version_resource.py`, `exe/T023_EXTENDED_KEYWORD_MATRIX.txt`。
- contemporaneous modding thread 2016-10-18 23:00 savename要望、Vahren Wiki 2016-11-23/2017-02-17 6.85o記録、現行IF一覧の6.85o-only同梱記録。

## 6.85o → 6.85p chronology bracket（2026-10-07 継続監査31 checkpoint 2）
[HIGH-CONFIDENCE / exact binary identity VERIFY]
- bundled target PE timestampは既知どおり **2016-10-18 21:08:57 JST**。
- Vahren Wiki「一行メモ」では **2016-11-23** の報告が明示的に「Ver6.85o時点」と記し、さらに **2017-02-17** の別報告も「Ver6.85oで確認」と記している。
- Vahren Wiki「手動アンテナログ」では **2017-03-26 23:57:32** に「ヴァーレントゥーガ本体 ver6.85p」が記録される。
- よってtarget timestampは、後世の曖昧な“pre-v7”分類だけでなく、公開記録上 **6.85o と明示されている期間より前寄りかつ、6.85p登場より約5か月前**に位置する。2016秋〜2017冬のnamed intervalとして6.85o系統との整合性が非常に高い。
- ただし6.85oの正本配布EXEそのものを取得してhash/section/.text比較したわけではないため、「target binary = official 6.85o」のexact identityは引き続きVERIFY。chronologyだけでT023をDONEにしない。

[REIMPLEMENT]
- strict profileのauthorityは引き続きbundled target binary。内部profile labelは暫定 `pre-v7 / 6.85o-era` を維持できるが、exact 6.85o文字列を保存形式・互換判定の必須IDには使わない。

[EVIDENCE]
- Vahren Wiki「一行メモ」2016-11-23 / 2017-02-17 の6.85o明記。
- Vahren Wiki「手動アンテナログ」2017-03-26 ver6.85p記録。
- `exe/T023_VERSION_RESOURCE.txt`, `exe/T023_DEEP_FINGERPRINT.txt`, `exe/T023_EXTENDED_KEYWORD_MATRIX.txt`。
