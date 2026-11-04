# 迫真戦記 ver0.67 REA｜P0 DirectMusic拡張子判定のfirst-dot/prefix境界
研究ID: REA-LOCAL-20261027-01HB-P0-DMUSIC-FIRST-DOT-EXT-DISPATCH-STATIC-01
実施: 2026-10-27 01時台後半 JST（同時間帯の別研究と区別する追補B）。状態: STATIC / VERIFY / NOT READY。原作ゲーム Golden NOT RUN。
原作研究用EXE SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
旧SQLite: 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF
統合V9: 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE

## 既存01Hからの差分
01Hは名前検索木のlower_bound/一致確認とmiss時のランダム選択→キャッシュ挿入を静的に確認済み。本回はさらに前段の拡張子判定入力・長さ・比較・分岐を原作PEの命令と埋込文字列から限定検証した。既存64関数や01Hの51検査条件を本回の新規VERIFIEDへ加算しない。

## 新規STATIC：拡張子の3バイト部分だけを比較
0x004BE820:0x004BE917 PUSH 1、0x004BE919 PUSH 0x00630024（ASCII '.'）、0x004BE92E CALL 0x00426490。0x00426490は先頭からmemchr→比較を繰り返し最初の一致位置を返すfind系。
一致位置があれば0x004BE93E INC ESIで「最初のドットの次」へ移動、0x004BE951 PUSH 3→0x004BE95E CALL 0x004261B0で3バイト文字列を構築する。長さ不足ならこの抽出をしない。
0x004BE9B5のECX=0x00630028はASCII 'ogg'、0x004BE9BA CALL 0x00402C40の非符号バイト比較と3バイト長一致でOGG分岐を決める。
それ以外は0x004BE9DC JE 0x004BEC0Cへ進み、0x004BEC0CのECX=0x0063002C（ASCII 'mp3'）と0x004BEC15 CALL 0x0040B200で同じ3バイト候補の完全一致を検査する。
MP3でなければ0x004BEC31 JE 0x004BEE7Eに進み、既報のDirectMusic系名前検索・ランダムfallbackの処理へ入る。判定関数0x00402C40の比較はmovzx byteによる大文字小文字を区別した比較。
## 新規STATIC：上流の拡張子補完も最初のドットで分岐
呼出元0x004BDE40:0x004BDEB6は0x00630000の'.'を検索し、0x004BDEC7 CALL 0x00426490で不在か判断する。
ドット不在時は0x004BDED5から0x0068C7D0の3ポインタ配列を巡回する（".mid"→".mp3"→".ogg"）。候補文字列を0x00416970で作り、0x004BDF0F CALL 0x004BDAF0で既存登録/音楽名を確認し、値が非0なら採用する経路がある。
ドットが1つでもあればこの自動拡張子探索を迂回する（0x004BDECF JNE 0x004BDF82）。ドットがパス中のディレクトリ名にある場合でも最初のドットが使われる可能性を静的に確認。
上流にも0x004BDF89 PUSH '.'、0x004BDF93 CALL 0x00426490、0x004BDFB3 CALL 0x004261B0、0x004BDFBD ECX='mp3'、0x004BDFCC CALL 0x0040B200があり、3文字抽出によるMP3判定が存在する。

## 合成例（引数のバイト列を0x004BE820に直接渡すモデル、原作実機ではない）
- track.ogg→OGG / track.mp3→MP3 / track.mid→DirectMusic。
- track.oggbak→OGG / track.mp3.extra→MP3（最初のドットの後の3文字だけを見ている）。
- track.OGG / track.Mp3→DirectMusic（この関数自体にcase foldingは無い）。
- track.x.mp3 / a..ogg→DirectMusic（末尾拡張子ではなく最初のドットを参照）。
- 拡張子なしは子関数内ではDirectMusicだが、上流0x004BDE40が補完候補を試すため、ゲーム全体の結果と同一視しない。
16入力の合成分類を監査した結果、想定との不一致0。ファイル存在/コーデック成功/ユーザー指定文字列が上流で変換される可能性は実機未検証。

## 出典・独立監査・保留
原作PEの実バイト、Capstone x86命令、ASCII定数/ポインタ配列、旧10/21 SQLiteと統合V9のE8直接CALL site、前回01H証拠を使用。監査77/77 PASS、追加Golden0、strict MATCH/完全互換率は未測定。
5種類のREA証拠: info/pseudo/callers/callees=INDEX_ONLY_V9、assembly=TARGETED_PE_NATIVE。新規正式VERIFIED=0。過去Wave1～5 64/64は既存同期記録のみを保持。正式TODO/VERIFY/BLOCKED書込差分0/0/0。
VERIFY: 実際のBGM指定に階層ドット/大文字拡張子/長い拡張子が存在するか、0x004BDE40の呼出元が入力を正規化するか、ドット無し自動補完の実ゲーム時の探索成功条件。
次の関数: 0x004BDE40のcallerおよび0x00416970/0x004BDAF0の候補組立・探索副作用、0x00463280の挿入成功/重複時帰結。原作ゲーム Golden隔離環境なしにつきNOT RUN。
原本/MASTER/QUEUE/PROGRESS/既存runs/他レーン/Git/スケジュールは変更せず。REA・Ghidra・ゲーム・Workは実行していない。安全拒否なし。
