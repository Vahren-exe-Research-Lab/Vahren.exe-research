# E/T018・T020｜F720前のreset→rebuild→選択の時相受入ゲート
ID: E-AUDIT-20261024-05H-T020-F720-REBUILD-PHASE-GATE-01 / 2026-10-24 05時台 JST / owner E / STATIC-CROSSWALK + SYNTHETIC / NOT READY
## 新規E差分
REA 05:41保存の0x48F9E0監査は、候補listヘッダ初期化だけではなく0x48FBD1で0x498E60をCALLし、続けて0x48FBD9で0x48F720をCALLする経路を報告。04時台Eの「過去に空初期化された」という観測から「選択時も空」と推測してはいけない。
0x498E60→0x498F90→0x476830ではinsert成功経路のcount+1が原作ASMで確認された（REA05:41既存知見）。ただし入力rangeの実要素数、duplicate排除、F720のfilter通過、リアルな非NULL保証はVERIFY。
別0x0040D0A0→0x0040F320→0x0040F393経路を、0x0048F9E0のreset/rebuild経路と実行時同一コンテナ・同一時刻として結合する証拠はない。0x4918B4..CBのtimerと0x4923EB/F1のflagは局所ゲートで、合法UI G0の観測ではない。
## 新しいT018受入条件
E-F720-01: 時点を「reset」「0x498E60復元後」「F720直前・返却」「0x583C70後」に分離し、同run/PID+戦闘窓、ポインタ基点、list header・count、range要素、filter比較木を別receiptで保存。
E-F720-02: 再構築CALLを観測・静的に確認しても、実挿入数や有効候補数は証明しない。ヘッダ空はF720がNULLを返す条件付き静的分岐にとどまる。
E-F720-03: source_rangeが空でもゲーム不具合を確定せず、NULL時の0x583C70経路の到達性・上位不変条件・原作実行結果を別確認。改造原本や旧拒否済み操作への介入をしない。
E-F720-04: G0合法旧UI、G1同run直前SAVE+入力byte/SHA、G2実MAP・攻防援のpower identity・ordered deployed Unit/Troopは上記内部ゲートで代替しない。G3結果/G4戦略状態も独立receiptを要する。
## 出典・真正性
原作コピー EXE SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（今runでread-only再hash）。
REA primary 05:41 STATIC.md SHA 9D3E9BC4387B36DD9F8AE3AD3DE3C4EC545C94DBA18177A29BA10814B9DBB4BA、EVIDENCE.json SHA 770DAF331D49EE2697B9904F10A2050237B41230E0CA56B6B21E12FB8FE0CDA4、検証source.py SHA 4D175B5A1A6C978BF23776B24CF8B8034937593240C2A96B3B35CC62D2BC43A1（今runのLocal Get-FileHashとREA保存記録一致）。
REAは原作ネイティブ25/25・E8 13/13 PASSと記録するが、Eによる独立再逆アセンブルではなく保存一次資料の照合。REA自身の状態はNOT READY/新VERIFIED0。
T020合成fixture20件・軽量checkerは同ディレクトリのF720_REBUILD_PHASE_*_20261024_05Hとt020_f720_rebuild_phase_gate_20261024_05H.py。合成結果から原作Gameplayを主張しない。
## 非昇格・引継ぎ
T019新確定矛盾/原作BUG 0。GameClear DAT13/TXT2字句scopeのみRESOLVED。script2同名優先・TXT runtime・phase flag・gwrite復帰はVERIFY。
MASTER最後の正式checkpoint196・READY596(A115/B229/C136/D116)、34Task DONE9/IN_PROGRESS21/VERIFY4は旧値。今回新規正式READY0、MASTER変更0。E原作DYNAMIC OBSERVED0/actual Golden PASS0/strict MATCH0。OFFLINE-UNSYNCED暫定26研究はID別未照合。
拒否済みT018表境界/E過去の各安全拒否/C T026,T032/D T030/禁止0x5710C0はBLOCKEDのまま再試行0。A-D/REA/dev_lab・原本・Git/Work・設定・schedule変更0。
次: 合法同run G0/G1/G2 receiptを最優先探索し、REAには0x48FBCA input rangeと0x498E60 duplicate/insert条件、0x40F320とのlist identityの追加根拠を待つ。保存/直接readback/合成試験は実施結果を別途確認。

## 05時台の実施結果（保存後確認）
Local CompactでE所有3ファイルをPC保存し、read_fileでそれぞれ21/29/86行の直接readback成功。検証器を保存状態から `python -B` で実行し、出典実バイトSHA256 4/4・REA E8 site 6/6・合成fixture 20/20 PASS。旧原作のGameplay/Goldenやstrict比較は一度も実行していない。
fixture SHA256 DDEBE173CF5FFECD8EB091870B39BA606FBD3279B3EA711D26A35D625E36502F、checker SHA256 ECB9EB191E12CA03863B4EEB5E86E5F5B3E320F480B5773D275643C2B9781753。新規安全拒否0。今回E所有資料以外の書込0、正式READY統合0。
