> 回収版注記（2026-11-05）: 原文を全文レビューし、個人用絶対パスのゲームルート接頭辞だけを `<GAME_ROOT>` に置換した。技術本文は保持し、注記以外の変更は台帳の置換回数に記録する。原本は変更していない。

# 迫真戦記 ver0.67 — 初の原作実セーブBYTE証拠（2026-10-11）

**訂正（2026-10-11・後続解析）:** この文書に記録されたnumeric 1,960／2,593は、数値群の終了を空文字と誤認した旧パーサの集計です。原作の正しい終了記号は `----------`、実数値レコードはsave1=1,958、save2/auto=2,591です。Unit/Spot/Power/外交/WorldGraphまで完全バイト再構築できました。**最新正本は `dev_lab/docs/DEVLAB_NORMAL_SAVE_WIRE_COMPLETE_20261011.md` および `dev_lab/reports/ACTUAL_SAVE_SECTIONS_CORRECTED_20261011.json`。** 本文は監査履歴のため旧数値を残しています。

## 取得・保全範囲
- ユーザー提供：原作画面のスクリーンショット（戦略マップ、turn 2表示）とPC内 a_default へのセーブ作成報告。
- 原本ディレクトリ：<GAME_ROOT>\新約迫真戦記―ほのぼの神話ver0.67 豪華版\a_default
- 検出した *.sav は save1.sav／auto.sav／save2.sav の3件。**元の3ファイルは読取専用**でSHA256取得し、dev_lab/_work の target_actual_20261011_{name}.sav へ新規コピーした。
- コピー後は元ファイルとバイトサイズ・SHA256完全一致。別の作業フォルダは増やしていない。ゲームEXE実行・リロード・Ghidra逆解析起動なし。
- save1.sav: 4,660,064 bytes; SHA256 15776d294a0c4f66568e7964331d60990b704f2ca324c568c49560561ae1947a
- auto.sav: 5,558,753 bytes; SHA256 08b3e05176dbb2ef076142c1bc91a586b428e82cccf44e6e6ac58cd46fb2e594
- save2.sav: 5,558,753 bytes; SHA256 45ccef306b56bf66810726436365207ca18b63d7cc0e432e784034d196fa5635

## 原作ファイルから直接確認できた事実（BYTE / TARGET CAPTURED）
- 3件とも先頭4 byte 01 02 03 04、後続28byte key、加算式envelope。保存済みnative 0x427040/0x4270F0および既存dev_lab/save_envelope.pyと一致。
- 復号後の先頭は u32=1、NUL終端ASCII sci1、po2、続いて**意味未確定のu32×5**（save1=0,6666,11,6,51 ／save2/auto=1,6666,11,6,52）。先頭numeric groupは復号payload offset33から開始。
- auto.savとsave2.savは**異なる暗号文**だが、復号後5,558,721 bytesが完全一致。plaintext SHA256 7c5127e85b3e7d622a7e0eb731ed8f0eeb56d131f6eeaf529e1b16a452bc052f。
- save1.sav復号SHA256 7d863ba369898da306bcef5dba8ee88baf2131e7c9cd9f32acd1869f8bc88fef（復号payload 4,660,032 bytes）。

## 先頭numeric groupと実データの差分
- save1: group offset [33,34737)、1,960 ordered records、distinct key1,960、追加重複0。
- save2/auto: group offset [33,47318)、2,593 ordered records、distinct key2,589、追加重複4。
- save1→save2で新規key629、削除key0、同名keyのaux/valueリスト変更67。全差分キーとbefore/afterは reports/ACTUAL_SAVE_BYTE_GOLDEN_20261011.json に格納。
- checkturn=1→2、siegeturn=1→2。スクリーンショットのturn2と整合（ただし画面撮影時刻と個別セーブ作成時刻の厳密な結び付きは未証明）。
- bonusmoney=0→1、turneventleague=0→1。ゲーム的意味・どのイベントで書かれるかは現段階でVERIFY。
- キー _pm_001_resilience1 は新save中5個あり、同名でaux文字列が cmd_beer_beer/cmd_deka_makura/cmd_oil_nuro/cmd_weekly_peer/cmd_briefs、全value0。既存 numeric_group_first はキー重複でraiseするため、この**同名・異auxのordered recordsを失わず保持**する実装が必要。
- 先頭groupで同名key重複が実際に存在する事実はBYTE-confirmed。ただしnative readerが参照時にどれを可視値として採用するか、multimapとしてのruntime意味論は引き続きVERIFY。

## 新実装と厳密な境界
- src/hakushin_compat/real_save_frontmatter.py を作成。原作envelope復号→raw先頭u32・2string・5u32・先頭numeric key/aux/int32列をtyped/lossless抽出。
- レコードはtupleとして入力順を保ち、同名keyをdedupしない。NUL区切り・native printableASCII・int32/上限を確認。数値group終端以降はunparsed_suffixの**不透明なbyte列**として保管。
- 保存済み28byte keyで再暗号化した3ファイルが各原本暗号文と**1byteも異ならない**（BYTE-repack exact 3/3）。これはセーブ**全構造を解読した証明ではない**。
- tests/test_real_save_frontmatter.py：合成の不正・同名別aux・不透明suffix・byte roundtripと、3現物のSHA・レコード数・同一plaintext等を検証。実セーブはZIPには同梱せず、_work不在環境の原本検証はskipする。

## 未解明・研究所有境界
- group1終端以降はsave1で4,625,295 bytes、save2で5,511,403 bytesが未意味解析。Unit/Spot/Power、外交・SpotGraph・セーブロード後のゲーム状態一致は未実装/NOT RUN。
- group1直後のoffset+1を既存UnitPrelude限定readerへ渡すと57bytesのempty prefixらしい値を取得可能で、後続に@@@@/arbeit/arbeit_user/item_skill/friendタグが現れる。ただし**厳密なgroup2境界・初回unit key意味は未確定**。空文字から元ゲームreaderがどう進むかを推測で補完しない。
- 保存済みnative writer0x460000およびreader0x45E1E0のgroup serializer順は参照済み。T014 owner Aのdata/T014_GLOBAL_SAVE.md・HANDOFFとEのT018は読取専用であり直接改稿しない。
- 推奨A/T014：実normal saveの先頭raw metadata/重複key＋aux契約、group2先頭境界、保存後readerのrecord実効、Unit/Spot/Power後段の静的根拠を照合。
- 推奨E/T018：スクリーンショットturn2、save1/save2 checkturn値、autoとsave2の同一plaintextを**BYTE captured fixture**として登録検討。TARGET gameplay Golden PASSやreimplementation strict MATCHへ自動加算しない。
- 過去のSAFETY_REFUSAL済み逆解析操作を別経路・別shellで再実行しない。原本ZIP/EXE、MASTER、他レーン資料・REA正本、Git、Remote、OS/automation変更禁止。


## 検証結果と現段階の制限（2026-10-11追加）
- new actual-save focused Python unittest: **13/13 PASS, exit0**（実capture3件のbyte exact往復／turn counters／distinct aux／synthetic bad input）。原本の再起動・セーブの上書き無し。
- 実save audit Python（real_save_audit.py）: exit0、reports/ACTUAL_SAVE_BYTE_GOLDEN_20261011.json 新規保存成功。source_sha256一致・3/3 captured byte-repack exactを確認。
- 全run_checks.ps1は実行開始したが、別AI所有の test_peer_script01_script_runner.TestRunnerRealCorpus.test_survey_counts が長時間完了しないため約545秒で**当方所有のテスト子processのみ停止**。run_checks exit1（中断に起因）。従ってこのrunを FULL PASS と報告しない。peer所有ファイル改変なし、別AIの既存解析processは停止していない。
- 従来保存の全322テストPASSは前回チェックポイントの結果。今回の13件専用PASSと合算して全335件PASSとは呼ばない。今後PEER_SCRIPT01担当にsurveyコスト上限/分割調査を依頼し、所有境界維持でfullを再実施する。
- ユーザー撮影画像：turn2の戦略マップ、画面右側の内政・資金表示が観察できる。画面値をlive save内部slotへ対応付けるには合法なロード前後UI観測が必要で、現時点で対応はVERIFY。
