# 迫真戦記 ver0.67｜新B T012/T013 接触候補の属性集合ゲートとtree走査順の修正

**研究ID:** `B-OFFLINE-20261022-2113-T012-T013-ATTR-MAP-COLLISION-01`  
**状態:** `OFFLINE-UNSYNCED / STATIC-ASM / STATIC-SAVED-PSEUDOC / INFERRED / VERIFY / NOT READY`  
**日時:** 2026-10-22 21時台 JST。担当：B T012 / T013。原作EXEは実行・変更・公開していない。

## 0. 実際の接続・証拠源と未同期回収

- Local Compact の `MASTER_LEDGER.md` 読取試行は `UNAVAILABLE: MCP SSE probe returned 429 from openai.org`。安全拒否ではなく接続先429の一時障害。Remote等へ切り替えず、PC最新正本は未確認。
- 正規Libraryの `HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip` と `Vahren(2).exe` を読み取り専用で確認。ZIP SHA256 `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`、CRC PASS（34件）、SQLite `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`、`PRAGMA quick_check=ok`、EXE `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`（指定SHA一致）。
- SNAPSHOT `research_snapshot/evidence/LANE_B_HANDOFF.md` と `ANALYSIS_LANES_PROTOCOL.md` をZIP内読取り。前回20:16の研究IDは重複計上せず、今回増分は「Skill属性集合の存在判定」および「候補treeは単なる挿入順走査とは限らない」という厳密化。
- 18時台のLibrary訂正版未反映を再確認。元Libraryと訂正ローカルの差分は本文1行／JSON2表現のみ。正規Libraryへの上書き試行は `container_session_unavailable` のため未反映、**復旧ID** `B-RC-20261022-1813-LIBRARY-OVERWRITE-CONTAINER-01` を未解決維持。原本・他レーン・MASTER未変更。

## 1. 発見A：`Skill+0x134` は候補属性mapの要素数と整合

`0x00599600` 擬似Cで大きなSkill候補レコードの `+0x134=0` を初期化し、`+0x130` には0x2Cバイト確保したtree head/sentinelを格納する。head+0/4/8を自分へ接続し `head+0x28/+0x29=1` とする。これは旧MSVC treeのhead初期化レイアウトと整合する。`+0x12C` はコンテナ基点、`+0x130` はhead、`+0x134` は要素数候補。

`0x00515470` のASM `0x00515477` は `[Skill+0x134]==0` なら `0x00515480 xor eax,eax` → return0。そうでなければ **`0x00515489 → 0x004E6D10`**。このため、20時台に「Skill+0x134≠0で衝突探索許可」と呼んだフラグは、単純なbooleanでなく **属性mapが空でないことを示す要素数** と解釈する方が整合的（STATIC-ASM + 型意味INFERRED）。

## 2. 発見B：候補側の `attr` 文字列が source Skillのtreeに登録されていないとAABBへ進まない

`0x004E6F60..0x004E6F8C` の実ASMは以下。

```asm
4E6F60 mov eax, [edi+0xB0]  ; 元MissileのSkill候補
4E6F66 mov esi, [ebp+0x0C]  ; 候補tree node value = 物体候補
4E6F69 mov edi, [esi+0xB0]  ; 候補物体のSkill候補
4E6F6F mov ebx, [eax+0x130] ; 元Skill属性mapのend/head
4E6F79 add edi, 0x110       ; 候補Skillのattr文字列
4E6F80 add eax, 0x12C       ; 元Skillの属性map
4E6F85 call 0x00415460     ; string-key tree lookup -> iterator出力
4E6F8A cmp [eax], ebx      ; iterator == end?
4E6F8C je 0x004E706A       ; 無ければAABBを調べず次候補
```

`0x00415460 → 0x00415E20` はtreeの候補位置を検索し、`0x004154A4 → 0x00402C40` で文字列バイト列と長さを比較する。未登録ならend/headを返す経路がある。従来既知の `0x0059A57A` 付近はDATの **`attr`** 属性（PE `.rdata` `0x006248BC` は `attr`、`0x006248C4` は `skill`）を `Skill+0x110` のC++ stringへ取り込む。

したがって **元Skill+0x12C の文字列集合に、接触候補Skill+0x110 の属性が存在することが、矩形判定より前の独立条件**。具体的な属性名の集合・DATの集合指定キー・敵味方や同属性に対するゲーム意味は未確定。これは全スキル一般のT013最終ターゲット選別だとの主張ではない。

## 3. 発見C：接触treeの先頭一致は登録順序ではなく tree iterator順序に依存

`0x004E6F49..0x004E6F52` は `param_2+4` のheadからleftmost nodeを取得。候補nodeは `+0x00 left / +0x04 parent / +0x08 right / +0x0C object* / +0x11 isNil` と整合。`0x004E706A..0x004E70AA` の実ASMは右部分木の左端へ移動するか親へ上がる **successor** 反復を構成。重なった最初の適格候補は `0x004E70BC mov eax,esi` から早期return。

よって20時台の「候補走査順が結果を左右する」を具体化すると **scene内treeの中順順序で最初の、attr集合に入っていてAABBが重なる候補** が選ばれる。**木の挿入順・距離順・描画順と等しいとは証明できない**。treeのソートキーと登録元はVERIFY。

## 4. PC復帰時の実証と未解明P0

- `0x00515470` のEDX入力は、上位 `0x0054C96F..0x0054C97B` および `0x0055267C..0x00552688` の間接参照 `[[Missile+0x78]+0x1D4]+0x1C` から配送され、`0x00515484` で **+0x68** のtreeを参照。所有者・コンテナ登録キーは未同定。
- 検証すべき最小ケース：元Skillのattr集合が空／候補attrが集合外／集合内、2物体のAABB辺接触のみ／重複、候補物体の登録順とtreeキー順を逆転させたケース。原作側で選択Object ID、Skill attr、集合内容、tree-key、コールバック順を原作ASM/実機で記録する。
- 次の検索先：候補treeのwriter（オブジェクトの`+0x68`コンテナ操作）、`0x00599BD0`におけるSkill属性集合のDATキー解析、`0x00465770`、`0x00468440`、`0x00417250`。それから `0x54DB60 / 0x552E60` からHP・MP確定箇所へ追跡。T024/T028未解明P0を維持。

## 5. 検証と判定

オフライン元を改変せず、索引擬似Cと**元SHA一致EXEの局所ASM**を照合。対象オペコード 27箇所中 27 PASS、直接E8 CALL 4箇所中 4 PASS。検索インデックスは10月21日版STATICで、現行V3との比較は未実施。詳細・機械的証拠はJSONに保存した。既存20時台T012/T013とB snapshotのT013「0x415460一般lookup」事実は繰り返さず、**そのlookupが接触候補の具体的フィルタとして動く**点が今回増分。

原作実測Gameplay Golden PASS **0**、strict MATCH **0**、新規B READY **0**、Task DONE **0**、E MASTER統合 **0**、PC正本同期 **未実施**。判定 `OFFLINE-UNSYNCED / STATIC-ASM / INFERRED / VERIFY / NOT READY`。既拒否範囲 `0x5710C0..0x571500` は未試行。
