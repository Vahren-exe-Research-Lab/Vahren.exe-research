# ChatGPT への依頼：ゲームが起動直後に終了する問題（Claude 作成 2026-11-03 20:2x）

## 症状
- 起動すると読み込み画面が出て約 1.5 秒で消える。エラー表示なし、終了コード 0（Claude が PowerShell から起動して確認）。
- hakushin_plugins.log に何も追記されない（最後は 2026-11-03 19:42 の正常起動）。プラグイン読み込みより前に終了している。
- ユーザーの経験：「起動中に同じ exe をもう一度起動すると起きる」「元の zip で上書きすると直る」。

## 確認済み（原因ではなさそうなもの）
- hakushin.exp を conf で無効にしても同じ症状 → HakushinExp.dll は無関係の見込み。
- Vahren.exe SHA-256 = E8DAC301…（正規）。dinput8.dll・HakushinCore.dll は 10/31 から不変。
- 試験用 DAT 2 つ（6001_召喚研究テスト\HS_Summon_Test.dat、6002_HakushinExp\HakushinExp_v1.dat）は 19:42 に動いていた版に戻し、ハッシュ一致を確認。それでも起動しない。
- ゲームフォルダ内で最近ゲームが書いたファイルはセーブ（save4.sav 11/03 09:05、auto.sav 11/01）だけ。
- 起動中の Vahren / x32dbg プロセスは残っていない。

## 19:42（正常）以降に変わったファイル
- plugins\HakushinExp.dll、hakushin_plugins.conf（exp 行のハッシュ更新。現在は切り分けのため exp を無効化＝3 項目目 0）
- 上記 DAT 2 つ（現在は 19:42 の内容に復元済み）

## 怪しいところ（優先順）
1. zip と今のフォルダの差分。「上書きで直る」なら壊れたファイルがあるはず。比較スクリプト compare_game_zip.py（同じフォルダ、読み取りのみ、サイズと CRC32）を用意したが Claude の環境では途中で止まった。差分の一覧を出してほしい。
2. 二重起動のときにゲームが書く・ロックするもの（名前付きミューテックス、レジストリ、%TEMP%・AppData の一時ファイル、a_default 内の設定ファイル）。
3. ゲームフォルダ直下の HakushinUI_v1.0 フォルダや、a_default\script 以下の .dat 以外のファイル（Thumbs.db など）が読み込みに影響していないか。
4. 切り分け：全プラグイン無効（conf の 3 項目目を全部 0、または dinput8.dll を一時退避）、6000〜6002 の試験フォルダを一時退避、の状態で素のゲームが起動するか。

## 守ってほしいこと
- 変更前に必ずバックアップ。
- DAT は Shift_JIS・CRLF のまま（LF にすると構文エラーになる実例あり）。
- plugins\HakushinExp.dll と HakushinExp.ini は原因でない限り変更しない（Claude 担当）。直ったら hakushin.exp の 3 項目目を 1 に戻すのは Claude が行う。
