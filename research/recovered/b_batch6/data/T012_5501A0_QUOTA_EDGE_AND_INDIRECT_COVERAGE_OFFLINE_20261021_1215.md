# 迫真戦記 新B / T012 — 0x5501A0の試行上限境界と間接参照索引の盲点（2026-10-21 12:15 JST）

- 研究候補ID: `B-OFFLINE-20261021-1215-01`。owner: B/T012（T011召喚、T024間接呼出への参照のみ）。
- 接続復旧ID: `B-RC-20261021-1215-LOCAL-SESSION-01`。
- 状態: `OFFLINE-UNSYNCED / STATIC-SAVED-REPORT / INFERRED-SYNTHETIC / VERIFY / NOT READY`。新規ネイティブ解析・DYNAMICなし。正式READY追加0 / E MASTER統合0 / 原作Gameplay Golden PASS0 / strict MATCH0。
- 原作ver0.67 SHA256（過去マニフェスト記録、今回原本の再hashなし）: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
- 使用済み証拠源1: 本会話内 `/mnt/data/hakushin_B_1110/data/T012_MODE4_EMPTY_CANDIDATE_QUOTA_CROSSGATE_OFFLINE_20261021_1110.md` SHA256 `2e00f50e7701e0c7276067326686926a33cb637d043a33b148e26b0e75d4e00f`。
- 使用済み証拠源2: 本会話内 `/mnt/data/hakushin_B_1015/data/T012_5501A0_MODE4_RESULT_LINK_ABI_VERIFY_OFFLINE_20261021_1015.md` SHA256 `3b29651c2ecd048b61b7b1272182a9219088c8cb12460deca515c778e3ff358a`。
- 使用済み証拠源3: Library `HAKUSHIN067_VTABLE_63848C_FULL_AUDIT_20261021.md`（独立の原本PE再配置/生バイトと索引照合報告）。**本件0x5501A0のvtable帰属を証明するものではない**。
- オフライン元ZIP `HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip` は今回の可視container/Library/会話一覧では参照可能なraw fileとして見つからない。過去報告にあるSQLite SHA `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF` は今回未再検証。PC検索DB、ASM、DAT、CALLGRAPH実体は今回未読。

## 解析1（保存済みGhidra STATICの跨関数合成 → 新たな境界ケースの予測）

- 呼出 site `0x00550219 → FUN_0054E7B0`: `def+0x40 == 4` の場合に選択。0x54E7B0側の保存済み擬似C条件 `Skill+0x14C == 0 && Skill+0x158 == Skill+0x15C` はeffect生成に進まずcleanupへ分岐すると先行研究に記録。条件が合法DATで達成可能かはVERIFY。
- 下位から戻った上位では、保存済み擬似C上、**生成成功をチェックする前に**`manager+0x1F0`を加算し、`def+0x74`上限と比較する。達したら site `0x005503F9 → FUN_004C22B0(manager,0)`後`manager+0x1D0`byteを0にする。**生成成功数ではなくattempt count**に基づく経路（これ自体は1110報告に既出）。
- 今回新たに境界を分離: `def+0x78 == 0` で上限未達時に同一関数内で反復する保存済み擬似Cから、初期attempt=0・limit=3・候補空なら **同じtickの試行3回/可視生成0候補/解除**、limit=0なら**比較前に1回はdispatchされ得る**、既にattempt>=limitでも**gateに入れば1回余計にdispatchされ得る**（いずれも推論/合法到達未検証）。
- 正のintervalに関しては、呼出ごとの周期ゲート・上限未達後returnというモデル上の差。`manager+0x1F4`（周期カウンタ）と`manager+0x1F0`（試行数）を同一変数にしてはならない。32-bit整数符号、型、activeフラグ入口チェックや副作用、RNG総数は今回証明なし。
- **限界**: 元ASM未再照合。Ghidraのブランチ復元に誤認があり得る。モデルでgenerated=0とするのは「下位が空候補cleanupを取る」場合を強制した条件付きモデルであり、上位以外のeffect・callback・死亡等を観測したという意味ではない。

## 解析2（索引欠落に関する別資料との整合性）

- 既存B `B-OFFLINE-20261021-1015-01` では`0x5501A0`の直接`calls` caller=0、`DATA_POINTER_REFS.jsonl`内の`0x005501A0`文字列一致=0、と記録。しかしこの数値は**実際の間接到達不可能の証明ではない**。
- 独立のLibrary監査 `HSK-VTABLE-63848C-20261021-FULL-RECONCILIATION` は、別のvtable `0x0063848C`の+0x04..+0x38に存在した14スロットが、PE HIGHLOW再配置付きで既知関数入口を指すにもかかわらず、`pointer_refs`が0だったことを生バイトで確認したと報告。よってGhidraのindex検索陰性だけでvirtual reachabilityを否定するのは不健全。
- **今回の増分**: `0x5501A0`の間接callerが0という陰性判定は`UNKNOWN / VERIFY`のままと明示し、「原本`.rdata`のlittle-endian DWORD `A0 01 55 00`を安全・許可済みraw dataで検索→再配置(type3)確認→対象入口の一致・table境界・CALL EAX/EDXの消費関係を確認する」という索引欠落対応を独立検証項目に追加した。**0x5501A0のraw pointer/vtable所属は未発見。** vtable監査をT012の新ネイティブ検証件数に再計上しない。

## 合成モデル実測（Nativeではない）

- 独立スクリプト: `test_T012_5501A0_QUOTA_MODEL_20261021.py` SHA256 `e3d99f79f39430ff72d76bb5717308de94d7c914ef1b4383b0aada25758d52c0`。
- 実行結果: `SYNTHETIC_MODEL_PASS=9/9`（8境界ケース＋inactiveケース）。結果例: interval0/limit3/候補空→同tick dispatch3, generated0, activeFalse；interval2/timer0→dispatch0；limit0のgate通過→dispatch1。実原作のバイナリテストやGoldenではなく、既存報告から読んだ制御フローの再現可能性を合成モデル上で確認しただけ。
- modelの`candidate_available=True`による「1回で1生成」は仮定であり、原作成功数と同一視しない。今回のチェックは全て候補空経路のため、原作命中/召喚実装の正しさを証明しない。

## PC・拒否・復旧の状態

- 初回Local read_multiple_files（MASTER、規約、B HANDOFF、検索README/MANIFEST）は `INVALID_ARGUMENT: Error code: INVALID_ARGUMENT; Error: McpServerError: Session terminated`。分類`CONNECTION/TRANSIENT`（安全拒否ではない）。最新checkpoint/Task Queue/予約/26旧候補/過去02～11資料のPC版は読めず、最新重複判定不可。
- Library確認: B/dataに02～11時台の研究資料は存在するが、**PC側への保存・統合は推定しない**。09時台報告の08文書同期とHANDOFFの安全拒否`B-RC-20261021-0910-T011-08-SAFETY-01`/`B-RC-20261021-0910-HANDOFF-METADATA-SAFETY-02`はBLOCKED維持。拒否本文・拒否コマンド・旧拒否VA`0x5710C0..0x571500`は一切取得・再提出していない。
- 別のLibraryアーカイブ`HAKUSHIN067_VTABLE_63848C_AUGMENTED_DB_20261021.zip`に対する**1回だけのmaterialize試行**は `This Project file does not have an authorized raw-byte materialization path.`で失敗。分類`ACCESS-UNAVAILABLE`。再試行・経路変更なし。raw DBの内容に基づく新たな結論なし。
- PC CPU/RAM/active.lockは未取得。Work/Remote不使用。PC、Git、MASTER、他lane、REA、dev_lab、原本EXE/ZIP/SAVE、スケジュール・設定への変更なし。

## 重複とREADY、Golden、次回

- 前回ID`B-OFFLINE-20261021-1110-01`の**候補空→上位試行回数増加**は新規発見として数えない。今回の独立増分は (a)具体的な境界入力の合成試験と (b)独立vtable監査を踏まえた`0x5501A0`の間接caller陰性の証拠品質判定。最新PCとの差は未照合につき`NOT READY`。
- Golden必須条件: 同一原作0.67のEXE/DAT/SAVE/入力/マップ・周期/上限値、合法的に空候補へ進む設定があるかをまず確認。実発火のtick、生成数、召喚者/登録/解除、RNG消費、HP/MP/XPと新buildを照合する。見えない内部値は`UNKNOWN`、実機未測定の今は`Gameplay Golden PASS=0 / strict MATCH=0`。
- 次回Local復帰時: まず最新MASTER+規約+B HANDOFF+T011/T012/T013/T024/T028+復旧索引の重複/安全拒否をread-only確認。非拒否の未同期だけowner範囲に一度だけ取込・readback。技術面は`0x550219`前後の許可済みASMでECX/EDXと4 stack argsを確定し、`0x5503F9`比較の有符号/無符号を確認。`0x5501A0`への実raw pointerは安全/権限確認後に検索し、実機では合法DATで境界を作れるか先に確認する。
- このB候補と合成コードをLibrary `data/`へ別資料として保全する（readbackされるまでは「保存成功」としない）。PC未同期のままREADY追加0。
