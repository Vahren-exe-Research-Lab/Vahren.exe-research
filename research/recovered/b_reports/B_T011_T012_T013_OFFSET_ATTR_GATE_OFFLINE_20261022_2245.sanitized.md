> Recovery annotation (2026-11-05): privacy-sanitized derivative. One personal absolute research-root prefix is replaced with `<research-root>`; the full authored technical body, historical status and corrections are otherwise preserved.

# 迫真戦記 ver0.67｜新B：`offset`・`offset_on`・`attr` の独立ゲートと単独 `on` 正規化

**研究ID:** `B-OFFLINE-20261022-2245-T011-T012-T013-OFFSET-ATTR-GATE-01`  
**復旧ID:** `B-RC-20261022-2245-LOCAL-SESSION-TERMINATED-01`  
**日時:** 2026-10-22 22時台 JST  
**所有範囲:** B T011 / T012 / T013。製品コード・原本EXE・MASTER・他レーンへの変更はなし。  
**状態:** `OFFLINE-UNSYNCED / STATIC-ASM / STATIC-SAVED-PSEUDOC / INFERRED / VERIFY / NOT READY`。

## 0. 接続・原本・復旧状況

Desktop Commander Local Compactで PC `<research-root>\MASTER_LEDGER.md` と `evidence\ANALYSIS_LANES_PROTOCOL.md` / `evidence\LANE_B_HANDOFF.md` の読取りを先行試行し、`INVALID_ARGUMENT: Error code: INVALID_ARGUMENT; Error: McpServerError: Session terminated` が返った。**接続障害**であり安全チェック拒否ではない。Remoteや他のPC経路へ切り替えていない。PC最新MASTER・HANDOFF・未保存復旧索引・最新READYは今回未確認。

Libraryルートの `/HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip` と `/Vahren(2).exe` を読み取り専用で取得。ZIP内の snapshot B HANDOFF、Protocol、T011/T012/T024資料を読み、既存の21:13 T012/T013研究と非重複部分を絞った。原作実行・EXE改変・全面逆コンパイルはしていない。原作指定SHA256を実バイトから検証：

| ソース | SHA256 / 検証 |
|---|---|
| EXE | `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` 一致 |
| 34ファイルのオフラインZIP | `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`、CRC PASS |
| Ghidra search.sqlite | `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`、`PRAGMA quick_check=ok` |

既存未同期成果は未同期のまま。18時台の訂正版Libraryへの再反映は復旧ID `B-RC-20261022-1813-LIBRARY-OVERWRITE-CONTAINER-01` のまま未解決で、今回修復したとは主張しない。拒否済み `0x5710C0..0x571500` 等の範囲は調査していない。

## 1. 最重要な訂正：当たり判定用の集合は `attr` ではなく `offset` 由来

前回 `B-OFFLINE-20261022-2113-T012-T013-ATTR-MAP-COLLISION-01` は「元スキルの属性集合が接触候補の `attr` を検索する」と整理したが、**元スキル側の集合がどのDATプロパティから構築されるかは未確定**だった。今回はその writer を追跡した。

- `0x0059C9C7`: `mov edx,0x00624F90`。原作 `.rdata` の `0x00624F90` は **`offset`**、`0x00624F98` は `skill`。
- `0x0059C9EC → 0x00465770`、`0x0059CA05 → 0x00415770`、`0x0059CA2E → 0x00415CF0` が `offset` スクリプトデータを解釈する連鎖として存在。
- `0x0059CA56: lea edi,[ebp+0x12C]`、`0x0059CA5C → 0x00468440`。`offset` の取得データを Skill `+0x12C` から始まるコンテナへ格納する。
- `0x0046845D → 0x00417250` はコンテナ挿入処理、後続 `0x004165B0` のノード挿入／要素数増分は map count `+0x134` と整合（元ASM・保存擬似C）。

一方、**候補側の属性文字列**は `0x0059A559` にて `0x006248BC="attr"`、`0x0059A57A → 0x004647D0`、`0x0059A582: lea esi,[ebp+0x110]` のため、Skill `+0x110` に由来する。

接触判定 `0x004E6F60..0x004E6F8C` は**元ミサイルのSkill `+0x12C` の `offset` 集合を、接触候補Skill `+0x110` の `attr` をキーとして検索**する。`0x004E6F85 → 0x00415460` 後、iteratorがhead/endに一致すれば対象をスキップしてAABBを実施しない。STATIC-ASM。`offset` のゲーム中の正式な意味、具体的な属性相性やDAT配列記法はVERIFY。

このため前回資料の『元Skill属性map』という**説明名称は不正確**。物理的な格納先 `+0x12C/+0x130/+0x134` と `attr` で検索するASM自体は正しいが、正本へ統合するときは『`offset` 定義の文字列キー集合』に訂正する。旧資料は削除せず、今回IDを参照するsupersedes注記をB所有資料へ一度だけ反映する必要がある。

## 2. 新発見：`offset_on` はSkillの別フラグ `+0x1FD` に格納

`0x0059BAE0` の `0x00624C78` は `.rdata` の **`offset_on`**。`0x0059BAD2` はカテゴリ `skill` を指定し、`0x0059BB05 → 0x004647D0` が解析値を返す。`0x0059BB0D` で `.rdata` `0x00624C74="on"` と比較し、`0x0059BB1A → 0x0040B200` の比較結果を `0x0059BB1F: mov [ebp+0x1FD],al` に書く。すなわち `offset_on=on` はフラグ `+0x1FD` を有効にする経路を持つ。

さらに `offset` の集合構築後、`0x0059CA61` は `[Skill+0x134]` を検査し、0でないとき `0x0059CA6A` で **`[Skill+0x1FD]=1`** に設定する。これは前段の `offset_on` 値とは別の有効化条件である。`+0x1FD` と `+0x134` を同一の真偽値として扱えない。

## 3. 新発見：`offset=on` が唯一のキーなら、集合を空に戻してフラグを維持

`0x0059CA71` で `[Skill+0x134] == 1` のとき、集合の先頭キー（node+0x0C）を `.rdata` `0x00624FA0="on"` と比較する（`0x0059CA8A → 0x0040B200`）。一致時には `0x0059CAA3 → 0x00416870` でノード消去処理、`0x0059CAA8..0x0059CAC1` でheadリンクを自己参照に初期化、`0x0059CAC4` で **`[Skill+0x134]=0`** を設定する。

重要なのは、その前の `0x0059CA6A` で**既に `+0x1FD=1` が設定されており、この正規化ブロック中には取り消す書込みがない**こと。特別な **`offset` が単独で `on` → count=0、flag=1** という組合せが生成され得る。これは `offset_on=on` によって flag=1、count=0 となる経路と、保存上の状態が似る可能性がある（全呼出パスで同一意味であるとは未証明）。

| 合成入力条件（説明用） | 処理後 `+0x134` | 処理後 `+0x1FD` |
|---|---:|---:|
| offsetなし / offset_onなし | 0 | 0 |
| offsetなし / offset_on=on | 0 | 1 |
| offset=`on` だけ | 0 | 1 |
| offset=`fire` だけ | 1 | 1 |
| offset=`fire,ice`（異なる2キーのモデル） | 2 | 1 |
| offset=`on,fire`（2キーのモデル） | 2 | 1 |

この表の属性値・記法は**合成例**であり、原作DATに `fire` / `ice` が登録されている、またはCSV記法で解釈されると確認したものではない。条件コードを再現するためのモデルでありゲーム実行結果ではない。

## 4. 2つの独立ゲートを同一視しない

- `0x00515470` では、`0x00515477` が元Missileの Skill `+0x134`（集合要素数）を判定。0なら `xor eax,eax; ret`。非0なら `0x00515489 → 0x004E6D10` の **接触候補探索**へ進む。つまり、特殊例 `offset=on` で集合が空になった直後は、この探索経路へは進まない。
- 別関数 `0x00515420` は `0x0051542D` で参照先 `Skill+0x1FD` を確認。非0のときにだけ `0x00515445 → 0x00579AA0` と `0x0051545A → 0x00510850` を通る**管理treeの対象範囲探索・更新／消去候補**処理へ進む。`+0x134` の値はこの入口ゲートに含まれていない。

このように、同じ Skillレコードで `+0x1FD=1` かつ `+0x134=0` が成立しても矛盾しない。ただし `0x00515420` の管理treeの所有権・消去対象、`0x00510850` の副作用および実戦での到達条件は未確定。`offset_on` を命中可否や無制限ターゲット許可と翻訳してはならない。

## 5. 今回の静的検証と既存成果の非重複

原作EXE実バイトから**`.rdata` 文字列8箇所**、E8直接CALL **12/12** をデコードして旧SQLite CALLエッジ **12/12** と照合、対象ASMオペコード **10/10** が期待値に一致した。対象10関数の保存済み擬似Cハッシュを索引から取得、SQLite `quick_check=ok`。合成分岐モデル8ケースを作った（合成モデルはGoldenではない）。追加の非重複事項は `offset` writerとのDAT文字列接続、`offset_on` 別flag、単一`on`正規化、`+0x1FD` と `+0x134` の入口分離。前回21:13の接触tree走査順・AABB・早期returnは既知として再計上していない。

既存 `B-OFFLINE-20261022-2113-T012-T013-ATTR-MAP-COLLISION-01` のsource-mapプロパティ名の誤認をここで訂正。オフライン snapshot 内の旧研究IDと今回IDの重複はチェックしたが、**最新PC MASTERとの正式な重複・READY照合は未実施**。新発見は実装可能な最終仕様にはまだ達していない。

## 6. Golden・未解明P0・次回再開点

対象スキル定義に `offset_on=on`、`offset=on`、複数 `offset` キー、候補Skillの `attr` 値が一致・不一致、矩形端接触、同時複数候補を用い、原作で **(A) `Skill+0x134` (B) `Skill+0x1FD` (C) treeに格納されたキー (D) `0x515420` が処理したID (E) `0x515470` が返した候補 (F) RNG消費とHP変化** を分離採取する必要がある。現在はいずれも実機未測定。

次回P0：`0x00468440 → 0x00417250 → 0x004165B0` のDATトークン→一意キー挿入と比較・順序・重複処理のABI確認、`0x00515420 → 0x00579AA0 → 0x00510850` の別treeの所有者と副作用、`0x004E6D10` の候補treeのソートキー、T012/T013最終命中→HP確定、T024/T028残未解明。原作EXEの実機Golden PASS=0、strict MATCH=0、新規READY=0、Task DONE=0、MASTER統合=0。EによるPC復帰後の正式照合・一度だけ取り込み待ち。

## 7. 保存・読み戻し欄

B所有の研究本文、構造化証拠JSON、検証スクリプトを独立成果物として作成する。Library側の保存／読み戻し確認は実際の結果を必ず別途追記／報告する。ローカル作業領域に保存しただけで **PC正本の保存・同期完了とはしない**。
