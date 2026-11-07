# 迫真戦記 ver0.67 REA｜P0 BGM存在確認の二段階パス探索と固定長リングバッファ
研究ID: REA-LOCAL-20261027-02H-P0-DMUSIC-TWO-PATH-BANKS-RING-BUFFER-STATIC-01
実施: 2026-10-27 02時台 JST。状態 PC-SAVED / STATIC / VERIFY / NOT READY。原作ゲームGolden=NOT RUN。
原作EXE SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
旧検索DB SHA256: 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF
統合V9 SHA256: 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE

## 既存成果との違い
01HBは最初のドットによる拡張子判定と、拡張子なしの候補 .mid→.mp3→.ogg を既に確認済み。今回は候補名を実パスへ解決する0x004BDAF0と0x00406CF0を深掘りした。
以前の01HBの77条件、およびWave1～5の既存64/64は新規成果として計上しない。

## 新規STATIC A：二つのパスバンクを優先順で巡回する
0x004BDE40の0x004BDF0Fと0x004BE018は、0x004BDAF0を呼ぶ直接E8 CALL。
0x004BDAF0では、構造体の[ESI+4]～[ESI+8]を第一バンク、[ESI+0x14]～[ESI+0x18]を第二バンクの範囲として順に巡回する。各エントリは0x1Cバイト刻み（0x004BDB72,0x004BDBF0）。
第一バンクは0x004BDB37 CALL 0x00406CF0で候補パスを組立て、0x004BDB47 CALL [0x00609178]でFindFirstFileA、成功なら0x004BDC2Eへ分岐。
第一で見つからなければ第二バンクへ移行し、0x004BDBB5 CALL 0x00406CF0、0x004BDBC5 CALL [0x00609178]で同APIを呼び、成功なら0x004BDC6Cへ分岐。
二つの成功経路は0x00609174のFindCloseを呼び、見つかった候補パスの文字列を返す。双方が不一致なら0x004BDC15で空文字列を構築して返す。
IATのFindFirstFileA/FindClose識別は原作PEインポートを直接検査。指定ファイルを実際に開いたりデコーダが受理することまで証明するAPIではない。

## 新規STATIC B：パス組立ヘルパーの共有16スロット
0x00406CF0はDAT_00AC0860のカウンタを増加し、0x10到達で0に戻し、0x00406D07 SHL EAX,0xAにより1スロット0x400=1024バイト分のオフセットを計算する。
0x00406D0BでベースDAT_00ABC460を加えて保存先を選択。続いて0x00406D16～0x00406D1Eでパス接頭辞をNUL込みコピー、0x00406D20～0x00406D48で後続文字列をNUL込み連結する。
関数内のCMPは0x00406CFBのスロット循環判定だけ。入力2文字列の合計長を1024バイトと照合する分岐は機械語上確認されなかった。

## 条件付きP0 VERIFY：1024バイト境界
prefix長512 + filename長511 + NUL1 = 1024 はスロット内に収まるが、512 + 512 + 1 = 1025 は1バイト超過する計算。
実入力で1024バイトを超える合成パスを渡せるか、OS側の長さ制限、外側のスクリプト・パーサで制限されるかは未検証。実際のヒープ破壊・クラッシュを確認したものではない。
FindFirstFileAはファイルをopenして内容を検査する処理ではない。Find結果の属性を見てdirectoryを拒否する処理も、このヘルパー内では未確認。実際の音声ファイル探索・存在しない/同名ディレクトリ時のゲーム挙動はVERIFY。

## 独立監査・関数別5証拠
原作EXE・旧SQLite・統合V9をSHA256確認、両SQLiteをimmutable/read-onlyでquick_check、原作PE32/IAT、指定VAの実命令、4件のcallsite×2DB、前回01HB/旧64件を照合。56/56 PASS。監査単体1.203秒、保存時1.930秒。
証拠種別: info=INDEX_ONLY_V9、pseudo=INDEX_ONLY_V9、assembly=TARGETED_PE_NATIVE、callers=INDEX_ONLY_V9、callees=INDEX_ONLY_V9。REA正式5種完備と取り違えない。
既存Wave1～5 VERIFIED 64/64（旧同期ログ）、新規正式VERIFIED=0、正式TODO/VERIFY/BLOCKED書込差分0/0/0。旧Golden実測PASS=0、strict MATCH・完全複製率は未測定。
PC接続成功、active.lock無し、空き物理RAM7.45GiB（単発観測。REAの8GB条件に未達）、CPU負荷不明、研究全体所要時間未測定。REA・Ghidra・ゲーム・Work起動なし、安全拒否なし。
既存MASTER/QUEUE/PROGRESS/runs/元EXE/元ZIP/SAVE/A～E/T018/Git/公開/スケジュールには触れていない。過去OFFLINE-UNSYNCED成果を正式同期していない。

## 次のP0
0x00406CF0の外側入力長の上限とDAT_00AC0860初期化、0x004BDAF0の二つのパスバンクが何の設定から組み立てられるかをそれぞれ参照元から静的追跡する。候補選択の実ゲームGolden・同名ディレクトリ・ロングパスの再現は隔離環境が無いため NOT RUN。
対象は0x00406CF0 callers、0x004BDAF0の保持オブジェクト構築元、0x004BDE40の引数供給元。重複を防ぎ既存V9のデータを優先し、REA再実行を先行させない。
