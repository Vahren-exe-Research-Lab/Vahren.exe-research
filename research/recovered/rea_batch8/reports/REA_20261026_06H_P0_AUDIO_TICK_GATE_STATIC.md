# REA P0｜音楽EOF判定の32カウント周期と4カウント補助更新（2026-10-26 06時台）
研究ID: REA-LOCAL-20261026-0635-P0-AUDIO-TICK32-MULTIGATE-STATIC-01
状態: PC-SAVED / STATIC / VERIFY / NOT READY。原作Golden PASS0、新規正式REA VERIFIED0。
原作SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
検索DB SHA256: 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF

## 今回の新規成果（05時台のEOF consumer追跡と非重複）
1. メインタスク関数0x004C24B0の0x004C26BDで task+0x3CをEAXへ読み、0x004C26C0のTEST AL,3 / 0x004C26C2のJNEで下位2ビット非0をスキップする。条件成立時だけ0x004C26CFから0x004BE220を直接CALL。
2. 0x004BE220では管理オブジェクト先頭ポインタの非NULLを確かめた後、0x004BE261で0x004BF410を呼ぶ。この4カウント段階では時間/フェード等の状態が進み得る。ここでまだEOFの判定をしていない。
3. 0x004BE266のTEST BYTE PTR [ESP+0x4C],0x1F / 0x004BE26BのJNEで下位5ビット非0をスキップ。呼出引数は0x004C26C7でPUSHした同じtask+0x3Cの値。したがって、後続の0x004BF6A0 / 0x004BF780 / 0x004BE2CA曲index加算/0x004BE307の次曲起動は、両ゲート成立時（counter & 31 == 0）だけ到達可能。
4. 0x004C2714から直接呼ばれる0x004C28D0の0x004C29C6はtask+0x3CをINCする。これは通常タスク更新経路でカウンタを進める仕組みの静的証拠。メッセージ処理・デバイス喪失・早期分岐では通常更新ルートを必ず通るとは限らず、実時間の更新周期は確定していない。
5. 0x004BE28Aのmanager+0x24ゲートが0なら曲送りへ進まない。0x004BE297はstream+0x38が0なら0x004BF780を飛ばして後続の停止/次曲処理へ進む。非0なら0x004BE29Dで継続判定を呼び、ALが非0なら0x004BE2A4で次曲処理を回避する。
6. 0x004BF6A0が非0を返すと0x004BE280から0x004BF720に進み、当該回の自動次曲は実行しない。0x004BF410内部には別の音声停止・再開へのCALL経路があるため「すべての音声停止/切替は32カウントごと」と一般化してはいけない。
7. 0x004C2611のtimeGetTime、0x004C262CのSleep、0x004C2509のPeekMessageAを確認。32は時間msではなくタスクカウンタ単位。単純な32×一定ミリ秒への換算は実ゲーム未実測のため禁止。

## 形式化した周期・条件
- 128カウント模擬入力：4ゲート成立 = 0,4,...,124（32回）。32ゲート成立 = 0,32,64,96（4回）。算術確認は原作ゲームGoldenではない。
- EOF consumerは前回発見済みの0x00502580（stream+0x58/0x54）。今回はその読取が、メインタスクから条件付きでしか呼ばれない構造を解明した。
- 通常ルートでEOFが32ゲート通過直後に変化すれば、次の評価まで最大31回のカウンタ更新を待つ可能性。ただし切替条件にはstream+0x38 / manager+0x24 / 0x004BF6A0 / 再生位置判定があり、実時間の上限や実際の遅延は保証できない。
- 0x004BF410の4ゲート内フェード/リスタート経路と、0x004BE220の32ゲート内自動次曲は分離して実装・テストする必要がある。

## 独立証拠・既存成果との区別
- 原作研究用EXE SHAおよびSQLite SHAは実計算一致。SQLite quick_check=ok。原作実バイトをCapstoneで限定ASM逆アセンブルし、関数サイズ・直接CALL索引と一致照合。
- 新規静的監査41/41 PASS：機械語23、関数サイズ5、直接CALL7、EXE/DB/PE/SQLite各1、周期算術2（内訳はEvidence JSONのchecks参照。検査総数はJSONを優先）。
- 06時台の証拠：REA_20261026_06H_P0_TICK_GATE_PROBE.py（限定ASM）、REA_20261026_06H_P0_COUNTER_PROBE.py（増分と時間制御）、REA_20261026_06H_P0_AUDIO_TICK_AUDIT.py（41条件）、REA_20261026_06H_P0_AUDIO_TICK_EVIDENCE.json。
- 正式REA info=INDEX_ONLY / pseudo=INDEX_ONLY / assembly=TARGETED_SOURCE / callers=INDEX_ONLY / callees=INDEX_ONLY。正式5種類証拠新規完備0。Wave1〜5既存64/64は旧syncログの数値、二重計上しない。正式TODO/VERIFY/BLOCKED書込差分0/0/0。
- 旧05時台の48/48と今回の41/41は異なる監査集合で、全関数カバレッジや完成率に換算しない。ゲームGolden PASS0、strict MATCH・完全複製率未測定。

## Golden設計（NOT RUN）
- 模擬taskCounter=0,4,28,32,36,63,64について4ゲート・32ゲート・EOF処理到達を比較。0,32,64のみ後者に入り得る。
- stream+0x38が非0なら再生カーソル・EOF戻り値により次曲が抑制されることを検証。0ならスキップ経路との比較を行う。
- EOF state1、bytes=1024、pos=2000の早期切替候補を異なるcounter位相（31/32/33）で採取。ログは原作実機Goldenとしてのみ新規PASSに昇格する。
- メッセージ集中・device lost・Sleep実時間・fade進行中の例外ルートも別試験とし、「32カウント=所定ミリ秒」の仮定を採用しない。

## 未確認・再開位置・変更禁止範囲
- 次回P0：0x004BF6A0の非0分岐と0x004BF720の効果、0x004BF410における4カウント更新の各経路を精査。0x004C28D0のcounter wrapはゲーム実測無し。
- 13/14時台OFFLINE-UNSYNCED成果のPC正本同期は未実施。原本/MASTER/QUEUE/PROGRESS/既存runs/他レーン/Git/Work/スケジュール不変更。安全拒否済みFLS/Wave6/禁止VAは再試行しない。
