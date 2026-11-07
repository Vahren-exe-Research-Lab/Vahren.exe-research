# 迫真戦記 新B T011｜member参照の `+0x1A4` と木構造 `+0x2FC/+0x300` の同一領域照合（2026-10-21 07:16 JST）

- **研究候補ID:** `B-OFFLINE-20261021-0716-01`（正式なB READY IDではない）。**担当:** B / T011。T013の汎用木挿入 helper は参照のみ。
- **状態:** STATIC（保存擬似C・直接CALL表の記載）／INFERRED（データ型・実ゲーム意味）／VERIFY（ASM・到達条件・runtime）／OFFLINE-UNSYNCED／NOT READY。B限定READY+0、E正式統合+0、Task DONE+0。
- **接続復旧ID:** `B-RC-20261021-0716-LOCAL-429-01`。最初にDesktop Commander Local Compactで PC `%USERPROFILE%\Documents\迫真戦記\_REDEV_RESEARCH\MASTER_LEDGER.md` の末尾読取を試行。実エラー：`UNAVAILABLE: Error code: UNAVAILABLE; Error: McpServerError: MCP SSE probe returned 429 from openai.org`。**CONNECTION/TRANSIENT**、安全拒否ではない。PC正本・B HANDOFFの最新状態、予約、今回研究のPC保存状態は未確認。Remote経由の切替なし。
- **証拠源:** ユーザー提供 `HAKUSHIN067_AI_OFFLINE_PACK_20261021(1).zip`（外側SHA256 `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`、34 entries CRC PASS）。`headless_analysis/search_index/search.sqlite` SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF` は `BUILD_MANIFEST.json` 記載と一致。Python標準sqlite3の `mode=ro` で派生コピーを検索。元ZIP/EXE/既存PC研究正本は改変なし。
- **対象原作:** ver0.67 EXE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` は**収録マニフェストの識別子**であり本runに原本から再採取していない。`research_snapshot`は最新PC MASTERと同一視しない。
- **擬似C独立一致確認:** 収録SQLite `functions.code` と内包 `HAKUSHIN067_FULL_PSEUDOC.zip` の同名 `.c` を文字単位で一致検証：`0x00463280`=`71422E164E422AF8665F4B7F6C9CD93A96CEA2CE5F5278D4EABA75035939ECAE`、`0x00467DE0`=`BBAABFDEFFD065F862307964D73E46442959DCDCDF2DBFD392BAD1EF56D5CA09`、`0x00582D90`=`0C97A9F541E871B941734CAC55644C0E68E80566BE16D84D9D8B641F690FED8E`、`0x00583DC0`=`9ACAED8DB47886D40CD1F8A96FACCA3A64004502A334840F8F5B25AC93E4369E`、`0x00583CF0`=`D4F4F50FFBA4DA16416C1BB8EAA017020EA0A6C6DEE82A35B9923E65AAD997FC`。保存擬似Cであり原作ソース／ASM対照済みとは言えない。

## 新規局所STATIC 1：`owner+0x2FC`と`owner+0x300`は同一treeオブジェクト内で連結

- 前回 `B-OFFLINE-20261021-0610-01` で確認済み：`0x00466F60` の直接CALL site `0x004671B3 -> 0x00463280` は第1引数として `param_1+0x2FC` を渡す。ここでは `param_1` を「当該callerのコンテキストポインタ」と呼び、ゲーム上の所有者を確定しない。
- `0x00463280` 冒頭で `puVar3=*(param_1+4)`、`puVar7=(*(param_1+4))[1]` を用いてtreeを探索し、挿入候補／重複候補を分岐する。callerからの加算により、参照されるポインタスロットは **`(context+0x2FC)+4 = context+0x300`** となる。
- `0x00467DE0` の既知lookupでは `local_10 != *(context+0x300)` をhit判定の一部に使用し、hit時に `*(returned_record+0x1A4)=context` を書く。したがって `+0x2FC` はtreeオブジェクトの起点候補、`+0x300`はそのオブジェクト内部のhead/sentinel候補として**同一管理領域**に属する、という相互整合がある（STATICのポインタ算術）。
- ただし挿入callerとlookup callerが全runtimeで同一インスタンスを受け取るか、`std::map`/標準木そのものか、key重複時の生存期間や例外時まで確定したわけではない（VERIFY）。`+0x2FC`と`+0x300`を独立した「別tree」として実装する根拠はない。

## 新規局所STATIC 2：`+0x1A4`バックリンクが後段のtree走査で消費される

- `0x00582D90`冒頭で `*(param_2+0x1A4)=param_3` を初期化し、`0x00467DE0`はlookup hit時に返却recordの`+0x1A4`へ検索コンテキストを書き戻す（いずれも前回までのSTATIC）。
- 今回新たに確認した `0x00583DC0` は `*(char*)(param_1+0x78)==0 && *(int*)(param_1+0x94)==0` の場合、`*(int*)(param_1+0x1A4)` を取り、さらにその `+0x300` を参照してtreeを走査する。この読み取りは**`+0x1A4`が後段で実際に利用される**ことのSTATIC根拠。NULL/寿命・型整合は未検証。
- 走査候補には `candidate+0x78!=0 || candidate+0x94!=0` の入口条件があり、候補の `[+0xD4,+0xD8)` という0x1C strideの配列風領域から `+0x10` 相当の値を取り、元の `param_1+0x10` と `0x00402C40` comparator経由で照合する。局所の擬似Cでは `comparator==0 && candidate_key<=query_key && candidate_key==query_key` の場合にそのcandidateを返す。
- 対象が見つからなければ局所的に`param_1=0`として0を返す経路がある。**入口の2条件を満たさなければ元のparam_1をそのまま返す**。この「入力を返す／別candidateを返す／NULL」の三分岐はSTATICだが、`+0x78/+0x94`のゲーム上の名称と全てのruntime経路はVERIFY。
- 直接CALL索引：`0x00583CF0` 内 `0x00583D82 -> 0x00583DC0`。`0x00583CF0`はまず `*(param_1+0x1A4)+0x2F0` を介した別の走査を行い、行き着かない場合に `0x583DC0` のフォールバックへ進む擬似Cがある。**`+0x2F0`と`+0x300`のコンテナ同一性は証明していない**ため混同しない。
- CALLGRAPH `0x00583DC0` の直接CALLは **30 site／17 caller**、 `0x00583CF0` は **70 site／42 caller**。頻用経路の可能性を示す静的件数であり、ゲーム実行時の頻度ではない。

## 再実装の影響とGolden（設計のみ）

- `+0x1A4`は単にメモとして設定されるだけでなく、後段のtree探索の入口に使われる。lookup時の参照更新を省略した実装では、同じrecordを使いながら探索コンテキストの違いにより戻り値がずれる可能性がある（INFERRED）。
- treeコンテナ起点`+0x2FC`、内部head候補`+0x300`、別参照`+0x2F0`をフィールド単位で保持し、頭ポインタとmap本体を重複コピーしない設計が必要な可能性がある。型確定・所有権・破棄タイミングはVERIFY。
- Golden条件（DESIGNED/NOT RUN）：同一原本EXE/DAT/SAVE/map/input/seed観測可否・capture SHAを揃え、member「見つからない／既存／重複」および参照する所属コンテキストの違いを原作合法操作と原作DATで確保できるか先に評価。合法的に再現可能なら旧新の可視Unit/member数・クラス/レベル/EXP・所属・行動・保存後状態を比較。非可視の`+0x1A4`やtree内部はUNKNOWNとし、憶測で一致判定しない。
- 本run原作実機を動かしておらず、**Gameplay Golden PASS=0、strict MATCH=0、DYNAMIC OBSERVED=0**。B限定READY=0、正式E統合=0、原作バグ新確定0。

## 重複境界・復旧・再開点

- **既存との差分:** `B-OFFLINE-20261021-0510-01`はmember初期化のcycleとフラグgate、`B-OFFLINE-20261021-0610-01`はlookup hit時の+0x1A4書込とtree挿入の成功/重複処理。今回の増分は **`+0x2FC`挿入treeの内部`+0x300`がlookup/後段consumerとつながること**、および `0x583DC0` の guard・return 分岐である。古いLibraryおよび2026-10-21 ZIP同梱T011/B HANDOFFスナップショットでは当該VA説明の全文一致を確認できていないが、**最新PC正本との重複・所有権・予約照合は未了**。前回内容を再採番してREADYにしない。
- 10/20〜10/21 01時台の旧26候補の二次分類は `X14/P4/I0/D1/C4/L2/O1` を**履歴**として継承。12ファイルPC回収の歴史的記録、10/20旧安全拒否12案件と168行／6,940バイトのINVALID JSON、`B-OFFLINE-20261021-0200-01`のPC同期不明も維持。新しいPC回収0、拒否済み操作の再試行0。
- **今回保存:** LibraryへのB/data独立文書1件を予定。Local接続429のためPC/dataと `evidence/LANE_B_HANDOFF.md` には今回書込0、PC保存／HANDOFF反映は**未実施**。読み戻し成功が確認できるまではクラウド保存完了と主張しない。
- **次の一手:** Local復帰時はMASTER最新版(TASK QUEUE/checkpoint/READY)、規約、B HANDOFF・T011..T028と復旧索引を読取り、同ID／同内容／予約競合と安全拒否を確認。今回の独立静的差分だけをB所有資料へ1回同期、独立readbackを実施。OFFLINE側は合法な保存済擬似Cに限り `0x00583DC0` caller別の入力・`+0x78/+0x94`のwriter、`0x00583CF0`との連動を追い、ASMとDAT未確認箇所はVERIFY維持。
- 安全拒否既往のVA `0x5710C0..0x571500` の新逆解析や拒否済み操作の別shell/tool/path/Remote/ZIP迂回0。重いGhidra/REA新規実行0、原本EXE/ZIP/SAVE実行／変更0、他lane/MASTER/REA/dev_lab/Git/push/Work/設定/automation変更0。PC CPU/RAM実使用率未取得、不明。
