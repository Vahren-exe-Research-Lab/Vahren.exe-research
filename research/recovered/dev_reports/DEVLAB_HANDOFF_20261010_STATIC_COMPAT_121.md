# 迫真戦記再開発・DEVLAB追加引き継ぎ（2026-10-10／保存済み逆解析の互換修復）

## 基準と実行制約

- 開始時の正本`MASTER_LEDGER.md`はcheckpoint67（READY108 ID、Task34＝DONE9/IN_PROGRESS21/VERIFY4、旧ゲームTARGET OBSERVED0）と5レーン規約をread-only確認。実際のリアルタイム最新状態は次作業の開始時に再確認。
- 既存Ghidra/REA関数取得はWave1 16/16、Wave2 10/10、Wave3 10/10、Wave4 3/12の計**39/48 STATIC VERIFIED**。この回の新規Ghidra function acquisition=0。前回拒否された`run_decompile.ps1`を再実行・別経路へ変更しない。
- `rea_lab/decomp_task/STATIC_DECOMP_COMPAT_CORRECTIONS_20261010.md`へ保存済みGhidra/owner static証拠のクロスウォークを新規記録（既存ランナ/QUEUE/PROGRESS/EXEには書かない）。

## 互換実装の主な成果（すべて`dev_lab/`内）

- `targeting_subset.py` 修正：primary最近接が射程外でもその距離を保持し、fallbackがstrict近距離ならbestを置換、同距離なら先勝ち。native helperのbest pointer(out[0])とprimary/cache用pointer(out[+0x10])を`uid/auxiliary_uid`で分離。上位AI行動の最終採否はVERIFY。
- `synthetic_ai_scene.py` 修正：旧`full_searches`表記を`refresh_checks`にし、timer満了と`0x514D60` selector実呼出を分離。cached target pointerが非NULLならtimer用jitter乱数を消費してもprimary helperを再呼出しない。仮チーム・合成1v1・120tickではrefresh4/primary2、2v2ではrefresh8/primary4。Unitsは移動も攻撃もせず、Native game side/team仕様は未確定。
- `native_vector_shuffle_subset.py` 新規：Ghidra保存ASM `0x479A30`の28byte stride、6dword=24byte swap、残4byte固定、index上限32767→32768の15bit rand2-draw拡張をbyte-level fixtureで再現。既存文字列shuffleの完成扱いや末尾4byteの意味解釈はしない。
- `script_rng_quirks.py` 新規：index(list,i)はnegative→先頭、>=N→末尾。pre-drawのraw index Nを受理した後に末尾へ折り畳むためraw N-1/Nが同じ要素を指す。pushRand2は15bit kをR(k)=floor((2^31-1)*k/32768)へ写像、k>0なら65536*k-1の疎な出力。native `mod`やイベント選択の実結果はVERIFY。
- `confusion_refresh_subset.py` 新規：Ghidra保存0x57B870の直接CRT rand callをtimer jitter、cached targetがNULL時の混乱primary、support capability時の混乱supportの別3siteとしてモデル化。関数外calleeの追加RNG・reseed・実戦targetingは未実装。

## 検証結果

- 専用テスト：`test_targeting_subset`9、`test_synthetic_ai_scene`4、`test_native_vector_shuffle_subset`4、`test_script_rng_quirks`5、`test_confusion_refresh_subset`6、全件PASS。
- `dev_lab/run_checks.ps1` フル実行で**Python単体テスト121/121件PASS**（直前103→18増）、原作map151/151 byte exact、atlas513、context204、script590（14,591,845byte）・parent21,214参照、本文516サンプルのspan検証、RTS1v1/2v2ヘッドレスfixture、その他既存回帰が成功、exit0 `DEV_LAB_ALL_CHECKS_PASSED`。
- `reports/synthetic_ai_1v1rts1_20261010T065337961614Z.json`、`...2v2rts1_20261010T065338191804Z.json`に新trace保存（refreshとselectorの件数を明確に区別）。
- **旧EXE実ゲームTARGET OBSERVED0／新エンジンMATCH0／全EXE逆解析率は不明。** ここでのPASSは内部単体・静的/合成契約テストの合格。

## ユーザーの手動協力（セーブは保留）

- 追加した`docs/MANUAL_OBSERVATION_WITHOUT_SAVE_20261010.md`を参照。優先は①タイトル・オプション・シナリオ選択の画面画像2～3枚、②BGM=1→0→1で再生挙動を観察、余裕があれば③戦闘の初期UIとユニット選択画面を撮影。今回は`.sav`不要。原本ZIP変更・Windows保護無効化・管理者実行は避ける。
- 既存19時頃のリマインダーはこの開発チャットから追加・変更していない。ユーザーがセーブを後日共有したら保存済み`save_probe.py`をread-onlyで利用し、unknown tailを解読済み扱いしない。

## 次回作業

- T013 support/attack候補のcacheと一次/二次selector側分岐をVM状態から分離、ステルス・混乱・RNG消費の相互作用は合成fixtureから順に拡張。
- T031 shuffle末尾4byteの正式意味と原作実動作の対応、`mod`のnative算術、pushRand2偏りのゲームUI到達を**安全に許可された証拠から**検証。拒否済み逆コンパイルプロセスの迂回は禁止。
- 原作設定/UI/音声の観測がユーザーから届いたら、T015/D ownerへREAD-ONLYの再現条件として整理。5レーン所有資料・MASTER/T018は独立チャットから編集しない。

