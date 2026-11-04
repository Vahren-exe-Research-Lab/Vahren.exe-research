# 迫真戦記 新B／T012 — RushMissileの仮想表初スロットと論理終了・物理解放の分離（2026-10-21 15時台）

- ID: `B-OFFLINE-20261021-1509-01`（新候補、B/T012所有、STATIC/INFERRED/VERIFY/OFFLINE-UNSYNCED/NOT READY）。障害ID: `B-RC-20261021-1509-LOCAL-SESSION-01`。
- PC優先：Desktop Commander Local CompactにMASTER/規約/B HANDOFF/README/manifestを一括read-only試行。結果 `INVALID_ARGUMENT: Error code: INVALID_ARGUMENT; Error: McpServerError: Session terminated`。**接続障害であって安全拒否ではない**。PC最新版 checkpoint/READY/owner・復旧台帳・active.lock/負荷不明。PC回収・PC保存・MASTER統合・B HANDOFF追記は全て0。
- 証拠：Library root `/HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip` を取得、19,646,444 bytes、実測SHA256 `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`、34件、ZIP CRCエラーなし。内包 `search.sqlite` 実測SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`、BUILD_MANIFEST PASS・一致。検索CLIは `mode=ro`、追加監査は SQLite `mode=ro&immutable=1`。対象原作 EXE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` は**マニフェスト由来**、今回EXE実体をハッシュせず、実行せず。
- 重複境界：既 `B-20261013-1130-01` は0x54F720 pool factory、`B-20261013-1154-01` は0x54F990 initializer、`B-20261013-1239-01` は0x4C22B0 unregister、`B-20261021-0910-01` は0x5501A0 periodic/quota、`B-OFFLINE-20261021-1412-01` は初期timerと初回tick推論。これらの単独BODY/初期timer/生成回数を新規READYに再計上しない。今回の増分は**RushMissile vtable初スロットの実参照と、logical deactivateとdeleting/freeの静的な分離、vtableの索引未充足範囲**。2026-10-20 snapshot `LANE_B_HANDOFF.md` SHA256 `6C8A5359E6214F1504D9A288D17BB8F75725A788337F669366949748DC71ADBE`に0x54F910の記録は検索上0。ただしPC最新との非重複照合は未了。

## 具体的STATIC：仮想表と物理解放

1. `0x0054F720` は0x218バイト確保した新規Rush系recordに `*local_4=RushMissile::vftable`、`local_4[2]=Missile::vftable` を設定。名前の正式symbolは `0x0063A6B4=RushMissile::vftable`、`0x0063A544=Missile::vftable`。`0x0054F7DD`（pool再利用）と`0x0054F819`（新規）が同じ `0x0054F990` initializer を呼ぶ事実は既存研究。
2. オフライン `DATA_POINTER_REFS.jsonl` の静的DATA参照：`0x0063A6B0 → 0x0063F83C` (`RushMissile` RTTI CompleteObjectLocator)、**`0x0063A6B4 → 0x0054F910`** (`RushMissile` vtableの最初の記録済みslot)。これはDATA参照であってCALLではない。近傍 `[0x63A6B4,0x63A6CC)` の参照索引件数は **1件のみ**。未索引位置にゼロが入る・他スロットが存在しないとは言えない。
3. `0x0054F910` 擬似Cは2箇所のvtable参照を`Actionable::vftable`へ変え、`(param_2 & 1) != 0` の条件で **CALL site `0x0054F928 → 0x005B6BBB`**。`0x005B6BBB`は `_free(param_1)` の薄いラッパー。よって `0x54F910` は**deleteフラグ付き物理解放候補**として位置づけ可能。ただしvtable経由の到達・継承関係の厳密なC++ destructor semanticsはASM/RTTIおよび到達元でVERIFY。

## 具体的STATIC：使用終了は上記freeと別経路

4. `0x005501A0` 擬似Cの生成回数上限到達側は **CALL site `0x005503F9 → 0x004C22B0(param_1,0)`** の後、 `*(byte *)(param_1+0x1D0)=0`。`0x004C22B0` 擬似Cは管理配列からポインタを0にする、別配列で要素を詰める等の解除操作があり、第二引数0では任意の追加enqueue処理に入らない。**直接の `_free` CALL は存在しない**（内部で間接releaseするかは未確定）。
5. `0x0054F720` は global vector `DAT_008BE278..DAT_008BE27C` を走査し、`record+0x1D0==0`なら**同じrecordを0x54F990へ再初期化**して返る。したがって制御フローが同一Rush record上で成立するなら「quota到達→論理非active→poolへ戻り再初期化」が可能であり、**quota到達はメモリfreeの証明ではない**。逆に `0x54F910` に delete flag=1 で到達すれば物理解放の別契約がある。global vectorからのremove/廃棄がいつ発生するかはVERIFY。
6. `0x005501A0` の直接callerはDB上0件、`DATA_POINTER_REFS.jsonl`の`target_va=0x005501A0`も0件。対してRush vtable先頭`0x54F910`は1件。**0x5501A0がRushのどのvtableスロットか、そもそも同じrecordへのvirtual updateかは未証明**。vtable未索引は別監査でも既知なので「unused」断定はしない。原本に直接アクセスできた許可済み環境でvtable残余スロット/PE再配置と間接CALL元を新規照合するのが優先。

## 監査・再現・未解明

- 添付 `T012_RUSH_VTABLE_POOL_LIFETIME_AUDIT_20261021_1509.json` にSQLite source code SHA、DATA_POINTER_REFS抜粋と12件の一貫性assertion記録。**12/12 STATIC抽出確認**。この数値は原作ゲームテストではない。
- Golden設計：同EXE SHA/DAT/SAVE/skill/seed/可視条件で、pool新規→継続tick→quota終了→別skillで再利用、明示終了/戦闘終了、同時2recordの区別、ポインタ寿命が関連する可視発射時点・個体・所属・MP・HP・次乱数を比較。内部アドレスは実機合法観測なしに一致扱いしない。**原作Gameplay Golden PASS=0、strict MATCH=0、DYNAMIC NOT RUN**。
- 他P0維持：T011 XP/召喚/死亡、T012 最終ダメージ/MP fallback/生成RNG、T013 最終対象/キャッシュ、T024 AI time/rand、T028 士気効果寿命/敗走。全体Task DONE=0、新規READY=0。`0x54F910`のASMは今回取得しておらず、Ghidra擬似C/データ参照限定。 

## 安全・復旧・次回再開

- 既拒否 `B-RC-20261021-0910-T011-08-SAFETY-01` および `B-RC-20261021-0910-HANDOFF-METADATA-SAFETY-02` は以前のBLOCKEDを維持。拒否された0x5710C0..0x571500・0x58021E..0x580340、他拒否済証拠/コマンドを別tool/ZIP/Remoteで迂回せず。今回の新規safety拒否は0件。
- 今回オフライン成果をLibrary B所有 `data/` に単独保存、独立readback後のみ「Library保存成功」と報告。PCへの未同期回収=0、正式B HANDOFFの更新=0、PC側への取り込み=0。復旧IDの実エラー・影響・次の対応をこの本文に保持。
- 再開：Local復旧後は最初に最新MASTER checkpoint/Task Queue/READY/重複、規約、B HANDOFF、失敗復旧台帳と本人所有タスクを読み、既存安全拒否を再試行せず、Library IDの競合/重複を照合して一度だけB許可範囲へ取り込む。技術先行は許可済みPE/DATA索引の**`0x63A6B8`以降のvtable entry実体**を確認し`0x5501A0`到達の論拠を得る。その後 `0x54F910`が本当にrelease契約かASM確認。これは暫定STATIC候補でありMASTER統合・原作実測PASSにしない。
