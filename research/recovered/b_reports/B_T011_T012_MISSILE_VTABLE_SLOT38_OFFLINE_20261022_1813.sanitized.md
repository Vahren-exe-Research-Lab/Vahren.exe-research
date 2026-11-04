> Recovery annotation (2026-11-05): privacy-sanitized derivative. One personal absolute research-root prefix is replaced with `<research-root>`; the full authored technical body, historical status and corrections are otherwise preserved.

# 迫真戦記 新B｜Missile / SimpleMissile 仮想関数と候補ソートの静的接続（2026-10-22 18:13 JST）

**研究増分ID:** `B-OFFLINE-20261022-1813-T011-T012-MISSILE-VTABLE-SLOT38-01`  
**接続復旧ID:** `B-RC-20261022-1813-LOCAL-SESSION-TERMINATED-01`  
**所有者:** B T011(Unit/Skill) / T012(戦闘・ミサイル)  
**状態:** `OFFLINE-UNSYNCED / STATIC-ASM / STATIC-SYMBOL / INFERRED / VERIFY / NOT READY`。

## 証拠源と復旧
- `Desktop Commander Local Compact` で `<research-root>\MASTER_LEDGER.md` を最初に読み取り試行：`INVALID_ARGUMENT: Error code: INVALID_ARGUMENT; Error: McpServerError: Session terminated`。**接続障害**。Remote/shell等でLocal接続を迂回せず、PCを無断操作していない。
- 認可済みLibrary `/HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip` を読み取り専用の作業コピーへmaterialize。全34件のZIP CRC PASS、ZIP SHA256 `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`。抽出のscratch SQLiteに対する `PRAGMA quick_check=ok`、SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF` でManifest一致。元ZIP・DBの内容は変更していない。
- Libraryの元ファイル `/Vahren.exe` は**実行せず読み取り専用の一時作業コピー**からSHA256を直接計算し、指定のver0.67 SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` と完全一致。`.text`の指示バイト・`.rdata`のvtablesを直接参照した。原本は一切変更しない。
- 10月21日ZIPの `research_snapshot/evidence/LANE_B_HANDOFF.md`（保存スナップショット）と、Libraryの回収索引、17時台のB独立資料を照合した。**最新PC MASTER / HANDOFF / ACTIVE / READY / 未保存・未同期26候補の状態は確認不能**。過去の安全拒否を解除・再試行したとみなさない。Library `/MASTER_LEDGER.md` は旧checkpoint資料で、現行数値の根拠にしない。

## 発見A：旧検索DBで直接callerが0だった `0x0054D970` のvtable登録先を原作EXEで確認
- 原作`.rdata`内にGhidraが `Missile::vftable` と名付けた `0x0063A544` と `SimpleMissile::vftable` と名付けた `0x0063A5A4` が存在する（両方とも原作vtableの実体バイトとSYMBOL索引で照合）。直前の4バイトRTTI-COL候補はそれぞれ `0x0063F7C8`、`0x0063F76C`。
- `.text`内 `0x005823FB` は `mov [esi],0x63A544`、`0x0054A3AB` は `mov [esi],0x63A5A4`。**2種類の実際の初期化経路からvptr設定を確認**（STATIC-ASM）。`0x0054F7BD` の `[esi+8]`設定も存在するがサブオブジェクト候補であり、ルートvptrと混同しない。

| virtual slot | Missile entry / function | SimpleMissile entry / function | 確認 | 
|---|---|---|---|
| `+0x24` | `0x63A568 → 0x54D8E0` | `0x63A5C8 → 0x54D8E0` | 同一、スキル参照/別オブジェクトへtail-JMPあり |
| `+0x30` | `0x63A574 → 0x54D940` | `0x63A5D4 → 0x54D940` | 同一、スキル配列値候補を読む |
| `+0x38` | `0x63A57C → 0x54D970` | `0x63A5DC → 0x54D970` | **同一、今回のソートキー候補** |
| `+0x3C` | `0x63A580 → 0x402CD0` | `0x63A5E0 → 0x402CD0` | 同一、`this+0x54` を返す |
| `+0x40` | `0x63A584 → 0x546A20` | `0x63A5E4 → 0x546A20` | 同一、`Skill+0x28` を返す |
| `+0x04` | `0x63A548 → 0x54BA00` | `0x63A5A8 → 0x552030` | **異なる**、同一クラス扱い禁止 |
| `+0x54` | `0x63A598 → 0x54DB60` | `0x63A5F8 → 0x552E60` | **異なる** |
| `+0x58` | `0x63A59C → 0x54DCA0` | `0x63A5FC → 0x552EF0` | **異なる** |

旧SQLiteは `0x0054D970`、`0x0054D940`、`0x0054D8E0` それぞれの**直接caller 0、pointer_refs 0**。しかし原作EXEを対象アドレスの4バイトリトルエンディアンで限定照合すると、**各関数2箇所（各クラスvtableの上記エントリ）**を確認。これは既存参照索引の**静的vtableエントリ漏れ**を実証する（SQLiteを改造しない）。現行PCのV3索引に収録済みかは未確認。

## 発見B：`+0x38/+0x3C/+0x40`を利用する実際の間接ディスパッチを局所ASMで確認
- `0x004BC4F0` の `0x004BC67E/0x004BC693/0x004BC69F` でそれぞれ vslot `+0x40/+0x38/+0x3C` が呼ばれる。vslot+0x40の値に3を加えて3と比較（mod 2^32なので元が0の条件に等しい）し、通過するとslot+0x38の戻り値を、当該仮想呼出対象が指すオブジェクトの`+0x04`へ、slot+0x3Cの戻り値を同じオブジェクトの`+0x08`へ格納する。**ただし対象実体が毎回Missile型かは未確認**（STATIC-ASMの間接ディスパッチ、インスタンス型はVERIFY）。`0x004C4142 → 0x004BC4F0` はGhidra直接CALL索引に登録。
- `0x004C5910` の `0x004C5950/0x004C595E` は2オブジェクトから vslot `+0x38` を呼ぶ。比較結果が等しい場合は `0x004C596D/0x004C5976` で `+0x3C` の値を取り、異なる場合は `+0x38` を再取得。`0x004C5991: setl al` は**符号付き32bit小なり**比較を実施。条件成立で `0x004C59AA → 0x004C5800` に進み候補リストのリンクを移動。`0x004C55A0` からのE8 CALL site `0x004C567B/0x004C56C2/0x004C5725` は旧CALL索引に登録されている。
- vslot+0x38がこの2クラスなら、`0x0054D970`の返り値が**並べ替えの第一キー**、slot+0x3Cの`this+0x54`が**同値時第二キー**となる。+0x54は従来 `0x004BC920` 登録処理が設定する値でもある。ただし、**AIの最終対象選択/命中判定/ダメージ順序と同一のソートであると断定しない**。描画向け候補の可能性を含む。オブジェクト型到達条件はVERIFY。
- `0x54D970`の原作ASMでは `Skill+0x28==0 && Skill+0x9F5!=0` のときMissile自身の`+0xE4`を返し、その他は `Skill+0x9F4!=0`なら **1,000,000**、そうでなければ **0**。この分岐自体は17時台の既知成果であり**新発見として再計上しない**。今回初めて「vtable/間接sortとの接続」と「signed comparator」を原作ASMで確証した。返り値1,000,000をダメージ量と誤同定してはならない。

## 発見C：型・ABI/レイアウトの注意
- `0x0054D8E0` はvslot `+0x24`で共有だが、`Skill+0x9F4`成立時に `0x0054D930: jmp eax` で `*(vtable_of(*(this+0x78))+0x24)` へ**他オブジェクトへ委譲**する。この時の `ECX` は`[this+0x78]`に更新済み。自クラスへの無条件再帰とみなすのは誤り。原作ASM確認。
- `0x0054D940`は`Skill+0x3B0/+0x9F4`条件で`Skill+0x3C8+(this+0x110)*4`を読み取る。索引範囲・型・配列長は今回未確定でVERIFY。
- ソート時の`setl`は符号付き比較であり、`+0xE4`が負に解釈されるケースの並びは0/1000000と異なる可能性あり（適法値・ゲーム内可達はVERIFY）。同値の処理も、リスト操作を含めて原作ASMと照合すること。

## 重複禁止・P0・Golden
既知ID: `B-OFFLINE-20261022-1715-T011-T012-SKILL9F5-WRITER-CONSUMER-01`（+9F5パーサーと`0x54D970`分岐）と `B-OFFLINE-20261022-1609-T012-MISSILE-POSTREGISTER-01`（登録時`+0x54`等）。**今回の独立増分は二重vtable登録、原作ASM間接consumer、 signed comparator、旧SQLite pointer index欠落**。10月21日B HANDOFFスナップショットに `0x63A57C`、`0x54D970`、`0x4C5910` の一致記録なし。ただし最新PC正本と現行V3は未照合なので正式な非重複はVERIFY。

次回P0は① `0x004BC4F0/0x004C5910` へ渡る実オブジェクト型の追跡、② `0x54D970`の`Skill+0x28/+0x9F5/+0x9F4`と`+0xE4/+0x54`境界でsort結果・RNG消費・可視挙動を隔離観測、③+0x9F5真にする原作DATプロパティの同定、④ T013の最終対象選択・T012実命中/HP・T024 AI・T028士気敗走の未解明P0に戻ること。GoldenにはSHA一致の無改変EXE/DAT/SAVE/MAP、同一入力、同じUnit・Skill、seed/RNG順、生成したMissile/Object IDとリストの配列順をそろえた原作実機実測が必要。

**今回増分:** 新規B READY **0**、MASTER正式統合 **0**、Task DONE **0**、原作Gameplay Golden PASS **0**、strict MATCH **0**。Libraryへ独立成果を保存してreadbackするが、PC正本への同期完了と主張しない。接続安全拒否の混同や過去拒否ペイロードの別ルート再試行は行わない。
