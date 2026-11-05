# 迫真戦記ver0.67：Ghidra・検索CLIの追加入念監査と非破壊修復（2026-10-22）

- 作業ID: `REDEV-RESEARCH-CANONICAL-V3-NATIVE-CALL-FTS-20261022`
- **状態:** `STATIC VERIFIED / PC LOCAL / GAME NOT RUN / ORIGINALS PRESERVED`
- 現行Ghidra: `Hakushin067_FunctionRepair_20261021.gpr`。その修復済み関数体には今回は変更を加えていない。
- 現行検索DB: `HAKUSHIN067_CURRENT_CANONICAL_V3_20261022.sqlite` SHA256 `0B057C43D30EAEC74588C84CF7E09AA7A488BD0FF170925591953EF578AFCB25`
- 現行CLI: `search_current.py` SHA256 `23B116E1EC898183FBECEC1F33C063BF01D86E97D301206ADBD8964256CEC450`
- **AIが最初に確認するファイル:** `CURRENT_ACTIVE_RESEARCH_STATE_LATEST.json` → `CURRENT_ACTIVE_RESEARCH_STATE_V3_20261022.json` → `00_START_HERE_ACTIVE_RESEARCH.md`
- 正式検証: `verify_active_research_state_v3_20261022.py`（PC）と`verify_offline_current_v3_20261022.py`（展開ZIP内）。
- 原作EXEハッシュ `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、初期旧DBハッシュ `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`。原EXE・原Ghidra・DAT・SAVE・MASTER・他レーン・過去DBに修正なし。

## 修復A：GhidraのCALL区分はDLLフック候補として不十分

修復済みGhidraの`UNCONDITIONAL_CALL`51,213件を、原作EXE機械語の相対分岐先と全件照合。**不一致0件**、内訳：
- `E8`の本来の直接CALL：**44,889件**
- `E9`のJMP：**6,309件**
- `EB`のJMP：**15件**
- Ghidraの`RefType.isCall()`は末尾のJMPもCALL相当で記録する。したがって、以前のCLI`callers`をそのままフック命令一覧として使うと、6,324件のJMPを間違ってCALLとして扱い得る。
- V3で`native_callsite`を独立テーブル化（全51,213行、全てPE実バイト照合済み）。
- `callers`/`callees`はE8だけを返す。`jump-callers`/`jump-callees`はE9/EBだけ、`flow-callers`は両方を機械語種別付きで返す。
- **JMPが他関数への末尾呼び出しか、関数内部のジャンプかは別途CFGで確認が必要**。JMPを必ず「tailcall」だと断定しない。

## 修復B：Ghidra擬似Cの文字列検索で部分一致が漏れていた

旧CLIの`search`はFTS5トークン一致。例えば`ctx_ea`が含まれる擬似Cが1件あっても結果0件、`load`という文字列を含む擬似C35件に対しFTSは1件（関数名なども含めた新しい部分一致では42件）。

- V3 `search`は大小文字を区別しない文字列の**literal部分一致**。`%/_`を検索ワイルドカードとして扱わない。`search-token`は従来のFTS5単語検索を明示的に提供。
- 結果には一致箇所近傍のコード断片を表示する。
- 22件のCLI回帰テスト（直接CALL、JMP、混在経路、部分一致、FTS、ABI、関数範囲、雇用画面8件、PE再配置等）は22/22 PASS。
- 整合性の独立検証：旧V2の関数10,462、関数区間11,091、Ghidra参照243,670、PE再配置57,921、ABI3、FTS/旧疑似C/未解決レコードの全表を1件ずつ照合。全行不変。新機械語区分51,213件を原EXEから独立計算し全件一致。
- V3の`callers`で雇用画面のレンダラ`0x004D4A50`を調べると**E8 8箇所**。別チャット担当の「雇用画面V2失敗」は本研究で修理していない。

## 最新オフラインパック

`HAKUSHIN067_CURRENT_AI_OFFLINE_PACK_V3_20261022.zip`、**27,800,102 bytes / 30ファイル**、SHA256 `C05E85DE770241A70D625C365EB93C362A1683C8F08FC355683007D1031B7FF5`。
- 全ファイルCRC/SHA検査合格。
- ZIP展開後、Ghidra／原EXEがなくても9種類の検証・検索テストが合格。
- PCの`search_index`に保存済み。Project Libraryへの完全ZIP同期はこの時点では行っていない。**PCオフライン時に他AIが自動で読めるとは限らない**。
- `search_current_V2_20261022_ARCHIVED.py`、従来のV2 DB・V2案内・V2マニフェストは削除せず保存。
- 旧`verify_active_research_state_20261022.py`はV2用なので現行CLI変更をSTALEと判定し得る。V3用の`verify_active_research_state_v3_20261022.py`を使う。

## 今後の優先未解決箇所

1. 修復済みGhidraでも、関数所属が未設定の本来E8直接CALLが約3,024件。多くは`0x005Exxxx～0x0060xxxx`に集中。ジャンプ分岐・例外処理のCFGと照合せず、近接関数に無理に結合しない。
2. 間接CALL・COMPUTEDの実ターゲットは未解決。スタック・ECX/EAX・戻り値が未認証の関数には危険なDLLフックを作らない。
3. 原作ゲーム実行とGolden比較、雇用画面V2失敗の解析は別レーン。静的修復が動的動作成功を意味しない。

## ツール拒否からの復旧記録
- `REDEV-REPAIR-V3-EDIT-MCP-FUZZY-20261022`: Local Desktop Commanderの`edit_block`が`fastest-levenshtein`依存のモジュール欠落でエラー。ソースの状態を読み直した結果、候補コードには必要な変更が反映済みで、22/22テストで確認した。API拒否に対する強行ループは行わず、自己所有の候補ファイルをPythonで構文検証して継続。
- `REDEV-REPAIR-V3-CANDIDATE-ALIAS-20261022`: 二次的な候補変更用スクリプトは「対象文字列が存在しない」で停止（元候補にすでに変更が反映されていた）。**中間候補の作成・検証に限定**、本番CLIは候補22/22合格後に旧ファイルのハッシュ付きアーカイブを作り、安全に差し替え。元EXE／Ghidraへの影響ゼロ。
- 新索引V3の生成は成功、旧V2索引のSHAは不変。データを未保存で放置しないよう、検証済みマニフェスト・レポート・テスト結果を同フォルダへ保存した。
