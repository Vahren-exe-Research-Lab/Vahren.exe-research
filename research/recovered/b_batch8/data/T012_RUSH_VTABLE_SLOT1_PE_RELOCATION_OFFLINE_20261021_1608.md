# 迫真戦記 新B T012｜RushMissile仮想更新スロットを原作PE生バイトで特定（2026-10-21 16:08 JST）

- 研究ID: `B-OFFLINE-20261021-1608-01`。所有: B/T012（T011召喚・T024更新到達性は参照のみ）。状態: `STATIC-ORIGINAL-PE + ASM + INFERRED-CROSSJOIN / VERIFY / OFFLINE-UNSYNCED / NOT READY`。
- 接続障害ID: `B-RC-20261021-1608-LOCAL429-01`。Desktop Commander Local CompactでPC MASTER、規約、B HANDOFF、検索索引README/manifestを一括読取しようとしたが `UNAVAILABLE: Error code: UNAVAILABLE; Error: McpServerError: MCP SSE probe returned 429 from openai.org`。接続/レート制限であり安全拒否ではない。PC最新版、active.lock、CPU/RAM、未同期の同期先は未確認。
- 証拠源（Library所有資料を読取専用でmaterialize）: `/HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip` SHA256 `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`、19,646,444B、34件CRC正常。内包SQLite SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`はBUILD_MANIFESTと一致。`Vahren.exe` 実体もLibraryから取得し、実測SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`が原作ver0.67の対象値に**一致**。EXEは実行・書換え・公開していない。
- 諸制約: PC正本の2026-10-21最新版と重複・owner・READYは確認不能。利用した過去スナップショットは2026-10-20版で更新可能性あり。原本PE生バイトは読取専用、検索DBは `mode=ro&immutable=1`。安全拒否済みの `0x5710C0..0x571500`、`0x58021E..0x580340` および拒否された証拠・コマンドにアクセスしていない。

## 新規の確定可能なSTATIC事実（既報の15:09にはなかった部分）

1. 原作PEは32bit（PE32）、ImageBase `0x00400000`。`RushMissile::vftable` `0x0063A6B4` は `.rdata` に存在。**第1仮想スロット（0-origin index 1）`0x0063A6B8`、ファイルoffset `0x00239AB8` に little-endian 4B `A0 01 55 00`、すなわち関数VA `0x005501A0`が記録されている**。このスロットはPE `.reloc` に `IMAGE_REL_BASED_HIGHLOW`（type 3）登録。Ghidra関数入口・擬似C SHA256 `1687A2EB67E5D43881EE8E1BCA397AB1089B23168D02AA5D7E86E13DA932CB31`に一致。
2. `RushMissile::vftable` の6スロット（0..5）は順に `0x54F910 / 0x5501A0 / 0x431910 / 0x54E0A0 / 0x54E0A0 / 0x43B5A0`。全6スロットにHIGHLOW再配置が存在。直後の `0x0063A6CC` は次の `GameEvent::vftable` 用RTTIメタポインタ `0x0063FB40`、次テーブルは `0x0063A6D0`から。ゆえにRush表を6スロットとして区切れる（STATIC-PE/RTTI）。
3. **原作ASMの生成側** `0x0054F773: mov dword ptr [esi],0x0063A6B4` は新規確保したRushオブジェクトの主vptrを設定。`0x0054F7BD: mov dword ptr [esi+0x8],0x0063A544` はMissileサブオブジェクト側の別vptrを設定。既存研究の `0x54F7DD / 0x54F819 → 0x54F990` 初期化と合わせ、Rush型の主vtableが `0x5501A0`を仮想スロットに持つことを**生バイトレベルで接続**した。
4. **更新関数ASM** `0x005501AC: mov esi,ecx` はECXを本体オブジェクトポインタとして使用し、`0x005501AE: inc dword [esi+0x1F4]` でtimer加算。`0x005501C1: cmp eax,[edi+0x78]` に対し `0x005501C4: jl` は**符号付き比較**。試行数 `0x005503BE: inc [esi+0x1F0]`、上限 `0x005503D0: cmp eax,[edi+0x74]` に対し `0x005503D3: jge 0x5503E7` も**符号付き比較**である（既存擬似Cの<=に対する実ASM確認）。終了CALL `0x005503F9 → 0x004C22B0`、直後 `0x005503FE: mov byte [esi+0x1D0],0`。
5. Ghidra検索DBの `calls` では `0x5501A0`の直接caller=0、`pointer_refs` の`target=0x5501A0`も0。ただし上記原作 `.rdata` の実ポインタとPE再配置が存在。`0x63A6B4→0x54F910`のみ索引済。**静的参照索引の欠落を個別対象について反証した**。vtableの型帰属はSTATIC確認だが、実際の `CALL [vptr+4]` がどこで、どの周期・順で実行されるかは未証明。

## 差分・解釈・非重複

- 前回 `B-OFFLINE-20261021-1509-01` はvtable先頭`0x54F910`だけが索引済とし、第2スロットは未確認だった。**今回の新規増分は第2スロット0x5501A0の原作PE実証・全6スロット・再配置・生成時vptr設定のASM照合・timer/quotaの符号付きASM分岐**。前回の論理終了/物理解放や `B-OFFLINE-20261021-1412-01` 初回tick仮説は再計上しない。
- スロット帰属を確定できたことで `0x54F720`が生成するRush型と `0x5501A0`が更新する型との**静的クラス対応**が前進。ただし仮想呼出元、実際の初回tick発火条件、メモリ解放到達性、同一オブジェクトの実時系列はVERIFYのまま。原作ゲーム性の厳密一致には未到達。
- 前回までの既存READY、拒否復旧ID、未同期26候補などは**変更せず**。今回の局所静的監査は付随JSONで **16/16 PASS**。これはPE/ASM/索引整合チェックでありGameplayテストではない。

## 復旧・未保存・Golden・次の一手

- PC接続・正式 `MASTER_LEDGER.md`、`evidence/LANE_B_HANDOFF.md` 読取失敗。Libraryの今回B所有dataにのみ独立保存を試みる。PC保存=0、過去成果PC取込=0、正式B HANDOFF更新=0、MASTER統合=0、新規正式READY=0。保存したと言えるのはアップロード・独立readback後のみ。
- 旧安全拒否 `B-RC-20261021-0910-T011-08-SAFETY-01` と `B-RC-20261021-0910-HANDOFF-METADATA-SAFETY-02` は `BLOCKED` を維持。同一ペイロードの再提出/別経路回避をしていない。今回の新規安全拒否=0、接続障害=1。
- Golden必要条件: 同一原作ver0.67 EXE/DAT/SAVE/skill/seed、Rush生成新規/再利用、初回と次回tick、period=0/正値、quota到達、生成候補空、終了後の再利用の実時系列を合法的な入力から観測。各発射時点・生成数・Troop・RNG・解除を比較する。実測がないので**原作Gameplay Golden PASS=0、strict MATCH=0、DYNAMIC=NOT RUN**。
- 次回は接続復帰後、まずPC MASTER最新checkpoint・B所有資料/READY・安全拒否・未同期IDの重複をread-only再照合。技術面は独立した許可済み静的証拠で `CALL [vptr+4]` の呼出位置・型・実行順を追う。これが取れるまでは仮想更新を実際に1tickごとに呼ぶと断定しない。T011経験値/召喚/死亡、T012最終ダメージ・MP・RNG、T013最終対象、T024戦闘AI、T028士気敗走もP0継続。
