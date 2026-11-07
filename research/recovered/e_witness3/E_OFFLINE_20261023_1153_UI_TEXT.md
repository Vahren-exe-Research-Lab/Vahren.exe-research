迫真戦記・研究E｜2026年10月23日 11:53

今回は、前回10:53に作成したT018/T020検証器に、重要な証拠が欠落していても「設計上の条件を満たした」と判定する不具合を発見し、修正版を作成しました。

旧検証器で問題を実際に再現したうえで、独立した新検証器を作成しています。

新規合成回帰45/45件成功、成果物5/5件のLibrary保存・SHA256読み戻し成功です。

研究ID：`E-OFFLINE-20261023-1153-T018-T020-WITNESS-COMPLETENESS-01`

1. T018/T020：今回発見した不具合

前回の検証器では、次の情報がすべて欠落していても、6個の証拠確認フラグを`True`にするだけで設計完了と判定されました。

欠落していた情報	問題
実際のCALL site	どこから戦闘が始まったか不明
実vptr・間接CALL先	呼出先を実証できない
run_id・battle_id	異なる戦闘の証拠を混同する危険
直前SAVE・入力のSHA256	G1の根拠不足
MAP・実出撃名簿	G2の根拠不足

旧検証器を変更せずに実行し、問題を再現しました。

旧判定：

DESIGN_COMPLETE_NATIVE_PROOF_NOT_ASSESSED

これはactual Golden PASSではありませんが、必須情報がない状態を「設計上完備」と分類する問題です。

修正内容

新しい検証器では、G0・G1・G2の識別情報、実際のアドレス、証拠SHA256、観測時刻を必須にしました。

証拠不足は`VERIFY_INCOMPLETE`、確認済み情報の矛盾は`BLOCK_CONTRADICTION`として区別します。

さらに、援軍がUNKNOWNの場合、G2の証拠が完全であるとは判定しません。

今回の重要な改善は、証拠がないことと、矛盾する証拠があることを区別しながら、誤った設計完了判定を防止した点です。

2. 検証結果
検証項目	結果
旧検証器の問題再現	PASS
前回結果JSONの実バイト照合	PASS
新規合成回帰	45/45 PASS
Library保存	5/5成功
Library読み戻しSHA256	5/5一致
読み戻した検証器の再実行	45/45 PASS
原作EXE・SQLiteの今回の再照合	NOT RUN
原作Gameplay	NOT RUN

保存済みの旧研究を変更することなく、修正版を独立して作成しました。

3. T018：Golden観測
条件	状態
G0：合法UIからの戦闘開始	NOT OBSERVED
G1：同一戦闘直前SAVE＋入力	NOT OBSERVED
G2：MAP・三陣営・実出撃Unit/Troop	NOT OBSERVED
G3：戦闘終了	NOT OBSERVED
G4：戦略画面復帰	NOT OBSERVED
DYNAMIC OBSERVED	0件
actual Golden PASS	0件
strict MATCH	0件

新しい観測fixtureも作成しました。原作の実機証拠がない項目には、未観測状態を維持しています。

4. T019：矛盾研究

新規確定矛盾は0件です。

今回発見した問題は、原作仕様の矛盾ではなく、Eレーン内部のT020検証条件の不備として分類しました。

GameClearの既存整理を継承し、`script2`の優先順位、内部フラグ、TXT実読込、`gwrite`復帰はVERIFYを維持しています。

5. MASTER・34 Task

Desktop Commander Local CompactによるPC正本の読み取りを試みましたが、今回も接続制限が発生しました。

MCP SSE probe returned 429 from openai.org

安全拒否ではなく接続障害です。

指標	状態
checkpoint	196（旧確認値）
READY累計	596（旧確認値）
A / B / C / D	115 / 229 / 136 / 116（旧値）
DONE	9（旧値）
IN_PROGRESS	21（旧値）
VERIFY	4（旧値）
新規正式READY	0件
オフライン統合待ち	暫定26研究

前回の25研究に今回の独立研究を追加しました。

MASTER最新版との重複・競合は未確認のため、正式統合していません。

接続障害ID：`E-RC-20261023-1153-LOCAL-SSE-429-01`

旧安全拒否案件はBLOCKEDを維持しています。

6. 成果物の保存

今回の成果物は5件です。

成果物	ダウンロード
研究報告書	
T018/T020不具合修正報告

検証結果	
結果JSON

修正版検証器	
Pythonプログラム

Golden観測fixture	
G0〜G2観測条件JSON

統合待ち記録	
追加台帳JSON

ChatGPT Libraryの保存先：

/迫真戦記再開発プロジェクト/E_OFFLINE_UNSYNCED/

5ファイルすべての保存・読み戻し・SHA256一致を確認しました。

Windows PCのMASTER正本は未同期です。

7. 次の優先研究

引き続き、C-NB02の合法な戦闘開始操作から、実際の戦闘開始関数までの到達経路を観測することが最優先です。

今回の修正により、今後取得する原作証拠の受入条件が厳密になりました。

次に必要なのは、新しい合成テストではなく、G0の実到達、G1の直前SAVE・入力、G2のMAP・実出撃名簿を同一戦闘として確認する一次証拠です。

今回の結論

旧検証器が重要な証拠の欠落を見逃していた問題を実際に再現し、修正版を作成しました。

新規回帰45/45件成功。成果物5件はLibrary保存・読み戻し済みです。

オフライン統合待ちは暫定26研究。新規正式READY0件、原作Golden PASS0件、strict MATCH0件を維持しています。