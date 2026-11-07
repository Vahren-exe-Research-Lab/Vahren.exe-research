# 迫真戦記 新B｜T012/T028 静的オブジェクト死亡分岐と戻り値低位バイト（OFFLINE）

研究ID: `B-OFFLINE-20261024-1111-T012-T028-STATIC-RETURN-DEATHBRANCH-01`（2026-10-24 11時台 JST）。状態 **OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY**。

## 接続・証拠

- Desktop Commander Local Compactを最初に使用し、`MASTER_LEDGER.md`・`ANALYSIS_LANES_PROTOCOL.md`・`LANE_B_HANDOFF.md`の一括読みを試行したが、実エラーは `McpServerError: Session terminated`（分類 **CONNECTION**、安全拒否ではない）。**PC現行正本・予約・競合・READYの再確認不能**。Work/Remoteは使用しない。
- Libraryの `HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip` を読取専用で使用。ZIP SHA256 `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`、**34/34 CRC PASS**。同梱2026-10-21検索DB `search.sqlite` SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF` は `BUILD_MANIFEST.json`一致、`PRAGMA quick_check=ok`。旧スナップショットであり現行PC正本ではない。
- Libraryの原作 `Vahren.exe` SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` が指定対象に一致。原作EXE起動・改変なし。DBは`mode=ro&immutable=1`、局所PEバイトを`objdump`読取専用で検査。以下のVA・命令には原作EXE静的証拠を用い、擬似Cは補助資料にとどめる。
- 未同期22ファイル回収と後続「10研究未同期」のID対応、Library訂正版2件および旧安全拒否案件は未照合。拒否済み`0x5710C0..0x571500`・禁止された証拠ペイロードの再読取・再提出・迂回は実施していない。

## 今回の新規増分

### 1. StaticUnit（vslot+0x70: `0x0055ABA0`）の死亡時「文字列長」分岐

`0x0055ABBC`で`this+0x90`のHPを減らし、`0x0055ABC5`でHP残存か判定。死亡側に`0x0055AC2D CMP DWORD PTR [EDI+0x1E808], EBX`（EBX=0）がある。

`0x0055AC41 LEA EDX,[EDI+0x1E7F8]` で文字列オブジェクトを指定し、`0x0055AC54 CALL 0x00402710`でコピーする。オブジェクトの`+0x10`は長さ、`+0x14`は容量という既存文字列配置と合う。独立した後片付け`0x0055A000`でも`0x0055A053/0x0055A05D/0x0055A064`の処理で`this+0x1E80C=15`、`this+0x1E808=0`、`this+0x1E7F8`先頭NULへリセットする。**ゆえに+0x1E808は単なる謎フラグではなく、`this+0x1E7F8`の文字列長と整合**（STATIC-ASM、正確なゲーム内名称はVERIFY）。

- **長さ非0**: `0x55AC54`文字列コピー→`0x55AC5F CALL 0x4678A0`。得られた戻りオブジェクトの`+0x74`を`0x55AC65`で確認し、0なら`0x55AC71 CALL 0x580280`、非0なら`0x55AC84 CALL 0x54F720`。これを「死亡時のカスタム動作候補」と呼ぶが、効果名/引数型/実発火はVERIFY。
- **長さ0**: `0x55AC91`以降で文字列`BreakFire`（`0x629998`）を作り、`0x55AD05 CALL 0x4E1550`と`0x55AD1E`の間接CALLに進む。単純に何もせず死亡する経路ではない。視覚・音声についてはDの責任範囲と区別し、ここでは分岐条件のみ扱う。
- 両側合流後`Skill+0x1BC bit1`と`Skill+0x194 !=0`によって `0x55AD5F CALL 0x580280` へ進む **afterdeath候補** があり、`0x55AD6E`で `this` のvtable+0x58を呼ぶ。効果発火・オブジェクトの寿命はVERIFY。

### 2. SimpleStaticUnit（vslot+0x70: `0x0055B060`）との差

`0x0055B07D`でHP減算、`0x0055B083/8D`で生存・死亡を分岐。生存時は`Skill+0x1B0`条件で`0x55B0D7 CALL 0x547FC0`。死亡時は`Skill+0x1BC bit1`と`+0x194!=0`条件で`0x55B124 CALL 0x547FC0`、最後に`0x55B133`のvtable+0x58呼出し。

**StaticUnitに固有な`+0x1E808`の文字列長分岐・`BreakFire`経路は、SimpleStaticUnitのこの関数にはない。** これは両者の死亡契約の局所的相違であり、別関数による後処理の不在まで断定しない。

### 3. AL戻り値の落とし穴：`1`≠「この攻撃で新しく死亡」

StaticUnitでは`0x55ABB0`の死亡済みbyte `this+0x1867C !=0`で **HPを減らさず** `0x55AD70→0x55AD72 MOV AL,1`へ進む。生存側は`0x55AC22 XOR AL,AL`、HP<=0を処理した側は`0x55AD72 MOV AL,1`。

SimpleStaticUnitでも`0x55B06D`→既死亡なら`0x55B135→0x55B136 MOV AL,1`、HP>0なら`0x55B0DF XOR AL,AL`、HP<=0なら`0x55B136 MOV AL,1`。

つまり**両静的クラスの低位8ビットALは「すでに死亡扱い」でも1**。`AL=1`を新規死亡イベントの発生証明として数えてはいけない。さらに命令は`XOR AL,AL`/`MOV AL,1`であり、**EAXの上位24bitが0である保証はこの局所returnからはない**。再開発/フックでは`bool`相当の低位8bitと新規状態遷移を区別する（STATIC-ASM）。これらの関数は`RET 0x10`で終わり、4スタック引数を回収する。

### 4. 100万と100万1の違いは4クラス一律ではない

前回10:16の研究済み: `Unit`実装`0x5783D7 CMP EAX,0xF4241`により`Unit+0x1E568`の更新を2分岐する。一方、原作機械語と2026-10-21 Ghidra全関数を照合した範囲では、**SimpleUnit `0x544790`、StaticUnit `0x55ABA0`、SimpleStaticUnit `0x55B060`の各関数本体に同じ比較はなく**、HPはそれぞれ入力値をそのまま減算する。Unitの補助値処理を一律に4型へ複写する実装は禁止。いずれも可視結果/動的型別ルーティングはVERIFY。前回の4クラスRTTI表と3間接CALLは既成果として再計上しない。

## 重複・エラー・根拠強度

2026-10-21旧B snapshot `data/T012_BATTLE_CALC.md`（§17/§18のobject afterhit/afterdeathは既知）と前回`B-OFFLINE-20261024-1016-T012-T028-VSLOT70-ABI-SENTINEL-JOIN-01`を照合。今回は**StaticUnit個別文字列分岐、2つのStatic型のAL戻り値、4型のセンチネル差**に限定し、既存のvtable型名・afterdeath基本則を新規加算しない。PCの現行HANDOFF全IDとの意味重複照合はできないので **NOT READY**。初回Local一括読取の`Session terminated`以外に安全拒否なし。原本コード/ゲーム/DAT/SAVE/Git/Work/設定/スケジュールへの書込0。

## Golden必要条件・次回検索先

対象EXEと無改変DATのSHA、SAVE/MAP/同一入力・RNGを固定し、原作実測で4つのRTTIクラス（生存HP正/0/負、既死亡状態、1000000/1000001）を比較。StaticUnitの文字列長0/非0と戻りオブジェクト+0x74の0/非0、`Skill+0x1BC bit1`/`+0x194`も変化させ、HP・死亡イベント回数・オブジェクト存在・可視効果・RNGを観測する。内側レジスタだけの合成比較はGolden対象外。新旧両実装のstrict MATCHはまだ0。

次回: `0x0055ABA0`/`0x0055B060`のvslot+0x70間接CALLから`AL`を実際に読む呼出元の有無、`0x0055AC2D`の文字列を作るロード/コピー元、`0x00578370`のdynamic receiver型、以前の拒否案件から独立した安全な読取だけ継続。

保存区分: 本文とJSONをコンテナ/LIBRARYのB所有 `data/`へ格納可。PC `LANE_B_HANDOFF.md`への保存・readbackは**未実施**。B→E正式READY連絡・MASTER統合なし。原作Gameplay Golden PASS **0**、strict MATCH **0**、今回新規READY **0**、DONE増加 **0**。

## 原本PE局所バイト照合

| name | VA範囲 | SHA256 |
|---|---|---|
| static_guard_damage | 0x0055ABB0..0x0055ABCB (exclusive) | `F705B124F2F0A3314B22BFC9B3AA6CFE233449B3EF74D4705E29C0AA06601AC4` |
| static_survive_return_and_custom_gate | 0x0055AC22..0x0055AC35 (exclusive) | `34DF032FA0BF26FD72561816D6920B711E148E43333DE33B17BAC5E3EC491B42` |
| static_custom_string_copy | 0x0055AC3E..0x0055AC59 (exclusive) | `8A2B42908FB809512F759917A9CA80D0B90B92333543720F2B1E18D09920EC4D` |
| static_custom_callback_split | 0x0055AC64..0x0055AC91 (exclusive) | `90800584C5E08F1A397A98976F78BD3EF6D1C1646590937B42DF25ACBF7138BC` |
| static_lethal_cleanup_low_al | 0x0055AD67..0x0055AD7B (exclusive) | `299BE1E7D9FFB1CA4C84A81700A073BC2DD61A930CB6761C21F6ADAD1DA62954` |
| simple_static_guard_damage | 0x0055B06D..0x0055B08F (exclusive) | `7320F72951B7AEAF0CF370AE4E0FDA703D2063FF63343DFBA4938EC465B7D7BC` |
| simple_static_survive_return_afterdeath_gate | 0x0055B0DF..0x0055B0FB (exclusive) | `58D0DBA9EE4D3DE69117CE4EA55DA8BCBCCA03E4AAB51E933DC5F23B973DF6CE` |
| simple_static_lethal_cleanup_low_al | 0x0055B12C..0x0055B13F (exclusive) | `7BE8E4AC9CFD256494CCBFCD59A4BBED4D07B9D91D8F984B2ED9299D0C1384CB` |
| static_string_cleanup | 0x0055A043..0x0055A06B (exclusive) | `B080D829861AF26A32423C1531C1FBD0B2C9F886C53B0C38D01B97D0B25015B4` |
| unit_sentinel_aux_damage | 0x005783D4..0x005783F6 (exclusive) | `A076759E5E9A1EA1C25AA21ECC4F23202304B6486CA6A8EFA68F150D2472855F` |
| ordinary_damage_dispatch | 0x005510E1..0x00551156 (exclusive) | `BDB6A82E2E265E72DC8323CC2855694F456532DB208C6DD82507A9010D9458DB` |

証拠JSON内には各区間の原本hex、関数擬似Cハッシュ、出典・既知ID・VERIFY条件を保存。
