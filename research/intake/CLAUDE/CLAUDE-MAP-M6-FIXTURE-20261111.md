# M5/M6 確認外伝の設計で得た静的事実（CLAUDE-MAP-M6-FIXTURE-20261111）

担当: Claude（2026-11-11）。対象: ver0.67 OGG テストコピー（Vahren.exe SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`）の .map・script を Python で読取りのみ。製品リポジトリ `ButaMonky/Vahren.exe-MapGimmick` branch `codex/m6-block` の保存 ASM `research/raw/dis_4f0be0.txt` を再読。ゲームの起動・メモリ書込み・DLL/DAT 導入は行っていない。原作素材の本文・画像は収録しない（マス座標・定義名・行番号だけを記す）。

確度: **静的確認**＝原 EXE の命令列または原作データファイルの内容で確認／**推定**＝根拠はあるが実機未確認／**未確認**。製品側の試験外伝は `docs/M6_FIXTURE_PLAN.md`（commit a79f445）。REF_MAP_TERRAIN.md は別担当が §31 を編集中のため本ファイルに分けて記録する。後で REF §2・§28・§30 へ統合してよい。

## 1. loader の object 分岐と通行 grid［静的確認］

0x4F1D11〜0x4F1D53 は object エントリの ObjectDef（node+0x28）の +0（type、REF §1.1 の値）で分岐する。

| type | 分岐先 | 通行 grid（+0x60/+0x7C） |
|---|---|---|
| 5 break / 6 break2・gate | 0x4F251E（stage+0xE4 でさらに分岐、0x4F3290 で範囲を作る） | 少なくとも 0x4F2ED2〜0x4F2EDC の分岐で 0x4E9A20（ECX=x, EDX=grid, EAX=y）を呼び1を立てる。0x4F251E 以降の全分岐は未読 |
| 2 coll / 3 wall / 4 wall2 | 0x4F2108。ObjectDef+4（blk）==0 なら 0x4DF200 で Block を作り、0x4F2140〜0x4F217C で範囲内なら自マスの細 grid と粗 grid（/2、符号付き）に1。blk!=0 なら 0x4F219D→0x4F3290 で範囲を作り、範囲内の各マスを 0x4C1690 で変換して /32、0x4F2308 で既に0のマスだけ Block を作って 0x4F239F〜0x4F23C8 で細・粗 grid に1 | 立てる |
| 7 goal / 8 start | 0x4F1D59 / 0x4F1E21（0x148 byte を確保し 0x4FCA30 / 0x4FCDF0、stage+0x204 / +0x200 に保存） | 書かない（この区間では） |
| 9 box | 0x4F1EEB | 未読 |
| 0 無指定 / 1 floor / その他 | 0x4F20CB（0x4DF200 で Block を作り stage+0x148 へ追加するだけ） | 書かない |

帰結: 木・灯籠など type 無指定の object が載るマスは、field が床なら通行 grid では通れる。REF §2 の「object エントリ: type 5/6 は専用経路、その他は 0x4DF200 で Block」に、grid を立てるのは type 2/3/4（と 5/6 の一部分岐）だけ、という区別を足せる。type 0/1 の Block は +0x67 を持たないので空間表にも登録されない（REF §30.6 の登録条件から推定）。

## 2. 試験地図 sKamakura_normal の静的配置［静的確認（原作データ）］

sKamakura_normal.map（150×150、SHA256 `f496e050d9e9227990499b252c7ed48bf8878ecc29b14437e7ba6d0acc867dc2`）。field 定義は field_02_神苑_鎌倉.dat（SHA256 `0f8baf6b4a074001b0bdfbe2f8319514e202aa0220feaf5d6cae746e801db1ad`）、field_01.dat（`3e6cb61a…8a61`）。

- 地図中の field type=coll は highland_128_coll（2,664マス、field_02 の 2419 行付近、image=rock、attr なし、alt=128）、hori（105マス、attr=mersh、id=hori）、hori2（7マス、id=hori）。OGG の a_default\stage 直下の .map を走査した範囲で、field の壁系を持つのは s4_shinen と sKamakura 系4枚だけ（サブフォルダは見ていない）。
- 外周を coll で囲まれた区画: x=71..92, y=51..64。開口は南の x=78..85, y=63..64 だけで、その両脇 x=77・86 が堀（hori/hori2）。区画の内側は4方向連結で 179 マス（x=73..90, y=53..62）。
- 開口16マスは stone2_k / stone_k（attr=road）。(79,63)(81,63)(84,63)(79,64)(84,64) に type 無指定の object（sakur・sakur2・torii2_k）があるが §1 により grid は立たない。
- id=stone2_off のマスは地図全体で8つ（x=89, y=54..61）。field stone2_off は親 stone2、id 無指定（＝field 名）、attr=road。
- 8方向・壁角すり抜けなしの BFS（通行不可＝field coll/wall/wall2 と object coll/wall/wall2/break/gate）で (81,69)→(81,59): 通常は x=81 直進11マス、x=78..83 を塞ぐと x=84 経由11マス、x=78..85 を塞ぐと経路なし。［原作の領域分割 4E9A60 とは別の簡略モデルによる予測。実機未確認］

## 3. DAT と試験設計の事実

- DAT 入力座標とマス: s1919 での M4/M5 観測（addTroop 入力 700→マス21、850→26、1000→31、y 650→20、700→21）は「マス＝floor(入力/32)」と整合する。REF §21・M5 の 4B41B0→4C1770 の変換族と矛盾しない。M4 の 1800,700 が無効だったのは 45×45 地図の範囲外（1800/32=56）と整合する。［推定。sKamakura_normal では未確認。試験外伝は cell_of で検証して不一致なら測定不成立にする］
- event 戦闘の `limit`: 原作で event 戦闘に使う例は RTS 系の 6000（RTSscenario.dat 629・918 行など）、spot 定義では 900〜99999（spot.dat、skilltest.dat、dr_spot.dat）。0x565700/0x565730 の戦闘時間制限と対応するが単位は未確認。試験外伝は 99999 にした［未確認］。
- sortkey: 原作の 10_ユニット/03_*.dat:177、30_スキル/Status_30_*.dat:424/1129/1242 が `sortkey = 992` を使う（シナリオ以外の定義）。980〜999 で OGG 全 .dat に出ないのは 991 等。外伝の sortkey は 991 を使った［静的確認（データ）。シナリオと他定義の sortkey 名前空間が別かは未確認なので避けた］。
- cp932: U+301C（〜 WAVE DASH）は Python の cp932 で 0x8160 になり、戻すと U+FF5E になる。導入スクリプトの UTF-8→cp932 変換前後で文字が変わるので、試験 DAT では使わない［Python で確認。ゲーム側の表示は未確認］。
- hkmap_init は hk_map_battle を加算するので、hk_map_setup が -11 の間に毎回 hkmap_init を呼ぶと戦闘番号が回数分進む（M5 normal fixture の書き方）。setup 成功時の番号で控えが作られるので致命的ではないが、新しい外伝は1回だけ呼ぶ形にした［DAT の記述と製品 src/hakushin_map_chip.h の setup 処理から静的確認］。
- 製品 DLL（a79f445 時点、55a854f と同じ src）の hk_map_chip_field / hk_map_field_rect は成功時だけ hk_map_count を書く。壁系の判定は対象マスの id（セル +0xF0）を type≠0 の定義名の一覧と比べ、1マスでも一致すれば何も変えずに -27。hk_map_block_rect / block_restore は成功時と「変化なし」の時に count を書く［製品ソースの読取り］。
- OGG の現状（2026-11-11 読取り）: plugins\HakushinMapGimmick.dll は M5 の SHA256 `6d124bcc41d109f927112003ec4b4b2802c6ef1e108e3a5968fb2f992f2a6f7d`、6005 の mapgimmick_test.dat は `7948270226167ea9…9400`。chip_field・block 命令を持つ M6 DLL（`FBF0A3C8…7C3`）は未導入。

## 4. 未確認として残すこと

sKamakura_normal の event 戦闘で stage+0xE4・評価器+0x1EED42 の実値と領域グラフの有無、入口マスの実 grid 値（試験では block の count 12/16 で確かめる）、経路が無いときの moveTroop の挙動（停止・手前まで移動・直進）、type 9 box と break/gate の残り分岐の grid 処理、`limit` の単位、DAT 入力＝マス×32＋16 の対応。

## 5. 根拠

| もの | SHA256 / 位置 |
|---|---|
| 製品 research/raw/dis_4f0be0.txt | 0x4F1D11〜0x4F1D53（行 1185〜1215 付近）、0x4F20CB〜0x4F23D1（行 1430〜1650 付近）、0x4F251E・0x4F2ED2〜0x4F2EDC |
| movetype.dat | bf553c354dac1eb1a8c5435d8945ca323776cde8e25dbe9f0404ac90018b696a（normal: grass 6, road 6, sea 3） |
| 一時調査スクリプト | %TEMP%\m6fx\survey*.py・plan*.py（非収録） |
