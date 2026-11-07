# EXP-CACHEKEY-20261021-01｜召喚用UnitDataキャッシュの文字列キー・記録幅・ABI（新規独立研究）

- Owner: 独立経験値研究。関連T011/T012/T013は参照のみ。状態: STATIC-X86 / INFERRED / VERIFY / NOT READY。
- 原本: ver0.67のコピー `rea_lab/targets/hakushin067_Vahren.exe`、SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`（今回実測）。
- 今回の新証拠: `EXP_STRING_CACHE_ABI_EVIDENCE_20261021.json`。Capstoneで39 native siteを検証し39/39 PASS。元PE未変更。
- 既存との重複: B-20261013-1134-01はfixed/list/+270選択、B-1141-01は検索EAX・ret0x1C、P0_SUMMON_EXP_OWNER_REPORTはR→+1C8→+16Cを既報。このCPでは新READY再計上0。
- 独立増分: 文字列キーのレイアウトと比較方法、キャッシュレコードの大きさ、挿入時の468-byte by-value ABIと返値を横断して明示・検証。

## 1. キーは数値との複合キーではなく文字列
- `0x579940`のnative: candidate node+0x1Cから文字列長、+0x20から格納capacityを取得し、+0x20<16ならnode+0x0Cから、>=16ならnode+0x0Cのpointer先から文字を読む。
- 入力キー（EDI基準）も+0x10=文字列長、+0x14=capacity、+0x00=短い文字列本体または長い文字列のpointer。比較長はmin(両方の長さ)。
- 比較呼出 `0x579984→0x402C40` は生byteの辞書順比較（保存擬似C＋原本の比較・後続長さ分岐）。同じ先頭部分でも長さが違えば別キー。
- したがって「文字列+第2の数値フィールド」という以前の未確定推測は採用しない。node+0x1Cは文字列の**長さ**。
- 大文字/小文字の正規化はこの比較箇所に無い。別の上流でキー文字列が正規化されるかはVERIFY。

## 2. キー供給元と候補の選択
- 0x54E82A: Skill+0x14C!=0なら0x54E835のSkill+0x13Cという固定文字列を選択。0x14Cは+0x13C基準の **+0x10（文字列長）**。
- 空の場合: Skill+0x158/+0x15Cをbegin/endとする0x1C byte-strideの文字列候補一覧から選択（0x54E83E/44と0x54E8AA）。
- 0x54E862でSkill+0x270を判定。非0ならcaller供給のindexを個数で剰余、0なら0x54E886でrand系へ。raw DAT `next_order` はB-20261013-1951-01で+0x270に接続済み（今回の新規発見ではない）。
- 0x547490と0x553390にも同じ固定文字列/一覧があり、原本で各呼出元のアクセスに条件差がある。3経路で**同一文字列候補が選ばれる可能性**があるが、同一親Unit保証なし。
- キーのDAT上の正規フィールド名・全継承規則とcanonicalizationは、既存Bの `next/next2` 検証を参照し、別途producer確認。

## 3. ノード構造とUnitData（記録R）のサイズ
- `0x57A70F push 0x200`: ノードサイズ512 bytes。
- `0x57A73E mov word [node+0x1FC],0`: ノード末尾に管理フラグ。
- node+0x0C..+0x23: 文字列キー部分、node+0x28: R（UnitData相当）の先頭。
- 0x200 - 0x28 - 0x04 (末尾管理4byte) = **0x1D4 (468 bytes)** をR payloadに確保できる。
- `0x57A764 add ESI,0x1C`→`0x57A76F CALL 0x466BA0`: pair内の文字列キー領域(0x1C)を越えたコピー対象Rをnode+0x28へ構築。
- `0x466BA0`がUnitData+0x168/+0x16C/+0x170を個別に値コピーする（保存擬似C）。生成用一時元とは少なくともLv・EXP・閾値は**独立の数値ストレージ**になる。
- 同関数内の他のpointer/stringも存在するので、コピー対象全体を「すべて深いコピー」と呼ばない。

## 4. DLL/EXE連携で絶対に崩せないABI
- `0x577260`: ECX=tree owner BattleUnit、文字列キーを呼出側stackにvalue形式で配置。正常返値はEAX=R or 0、成功/失敗両端で `ret 0x1C`（28-byte cleanup）。通常C関数への無根拠キャスト禁止。
- `0x577310`: ECX=tree owner、呼出前に `sub esp,0x1D4`して0x466BA0で値引数payloadを構築し、`ret 0x1D4`（468-byte cleanup）。EAXは末尾`0x577405 mov eax,esi`により再検索のR pointer。
- 3つのproducer（0x547490、0x553390、0x54E7B0）すべてで `sub esp,0x1D4 → 0x466BA0 → call0x577310` をnativeで確認。
- Ghidraは0x577310の戻値をvoid扱いするため、そのまま関数ポインタを定義してフックすると戻値・stackを破損し得る。
- 0x577260がキー引数の長い文字列をcleanupする経路にも注意（渡す形式とヒープ所有権は手書きhookで再検証要）。

## 5. 条件付きの経験値共有と未解明
- [STATIC/INFERRED] **同じowner treeと同じ比較キー**で、先行Rが残っていればlookupはそのRを返す構造。複数のBattleUnitがRを参照すれば経験値カウンタも共有し得る。
- [VERIFY] 実際に同一キーが連続選択されるか、3pathのownerが同一か、Rへの別writer、戦闘終了前のtransfer、親の消滅とnode destructorの順序は未証明。
- [PRIOR] node+0x28に対する破棄関数0x5454D0→0x4591F0は以前のCP12/B先行資料で既出。二重計上しない。
- [IMPORTANT] 先行B所有資料に安全拒否範囲 `0x579A20` が記録されていると本回の重複照合時に判明。以後このVAの新規解析を停止し、今回の結論は他の許可済み原本サイト `0x579940`、`0x402C40`、`0x57A6E0`等に限定して裏付ける。

## 最小の再現テスト（DESIGNED / NOT RUN）
- S0 親P・固定キーAで子1生成→子1のEXP/Lv、親EXPを別採取。
- S1 同親P・同キーAで子2生成→子1子2のR参照先・EXP増加/再利用を確認。
- S2 同親P・異キーBで子生成→新規Rか、共有/上書きが発生するか確認。
- S3 別親Q・同キーA→別ツリーRか。親P/Qが同一部隊にいる場合も独立観測。
- S4 `next_order` on/off・候補数1/2/3・連続発動・乱数状態を固定し、キー選択とEXPの帰属先を対応付ける。
- S5 戦闘終了→戦略側EXP→SAVE/LOAD後を追跡し、RのEXPが残るか／移行するか検証。
- 原作Gameplay Golden PASS0。正式B READY追加0、E MASTER統合0、Task DONE追加0。

