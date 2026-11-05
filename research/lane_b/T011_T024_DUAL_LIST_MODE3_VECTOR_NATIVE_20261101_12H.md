> **B-OWNED PRIVATE RESEARCH INTAKE — PUBLISHED_INTAKE / NOT_CURATED / STATIC-VERIFY / NOT READY**. Historical local owner report recovered and SHA256-readback verified from the authorized PC on 2026-11-01 22H JST. This is a text-only sanitized copy, not original game assets or the curated KB. Duplicate-path mirrors carry the SAME research ID; count once.
>
> research_id: `B-OFFLINE-20261101-12H-T011-T024-DUAL-LIST-MODE3-VECTOR-01`; owner: B; tasks: T011,T024; local_source_relative: `data/T011_T024_DUAL_LIST_MODE3_VECTOR_NATIVE_20261101_12H.md`; **original local report SHA256: `8ED8FCFD43200DB30236A0E6D219E0E3440DBD3A90EE6C68F80C81A0708F7B88`** (GitHub sanitized copy intentionally hashes differently). Original EXE identifying SHA256: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (prior verified reference; not rehashed this hour). Golden PASS=0; strict MATCH=0; DYNAMIC=0; READY=0.
>
> The historical text below retains its historical `OFFLINE-UNSYNCED` label describing original evidence collection; this new GitHub staging does not retroactively change that observation. Private GitHub branch/readback is the new preservation state; curator reviews all semantics and source SHA separately.

# 迫真戦記 ver0.67｜B/T011・T024：二系統リストからモード3のVectorへの連結経路（2026-11-01 12H JST）

**研究ID**：`B-OFFLINE-20261101-12H-T011-T024-DUAL-LIST-MODE3-VECTOR-01`。owner B、tasks T011/T024。**状態**：`OFFLINE-UNSYNCED / STATIC / INFERRED / VERIFY / NOT READY`。DYNAMIC=0、原作Golden PASS=0、strict MATCH=0、新規READY=0。

## 1. 証拠源・復旧・禁止条件

最初に Desktop Commander Local Compact でPCの `MASTER_LEDGER.md`、`evidence/ANALYSIS_LANES_PROTOCOL.md`、`evidence/LANE_B_HANDOFF.md`、`knowledge/README.md`、`SYNC_STATUS.md` の読み取りを試したが、`INVALID_ARGUMENT: Error code: INVALID_ARGUMENT; Error: McpServerError: Session terminated` で失敗。**接続障害**であり新規の安全拒否ではない。PC最新正本、3時台書込の実在、4〜11時台の取り込みは確認できない。

代替証拠はChatGPT Library由来の `Vahren.exe`（原作ver0.67、SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`）、`HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip`（SHA256 `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`）、`HAKUSHIN_B_LANE_SAFE_RECOVERY_20261029_V3.zip`（SHA256 `059B91381C1B58214353769006E0F4049FCDE393A6B7970F4513602878A2B2C9`）。ZIP CRC 34/34、136/136正常。旧 `search_index/search.sqlite` SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`、SQLite quick_check=ok（読取専用で実施）。原本EXEを**起動していない**。Ghidra全体解析・再生成もしていない。

非公開GitHub `ButaMonky/Hakushin067-Research-Knowledge` の `develop` は閲覧権限を確認し、`README.md`、`SYNC_STATUS.md`、`symbols.tsv`、`structs.tsv`、`REF_BATTLE_AI_MORALE.md`、`GHIDRA_V9_B_REVIEW_TOP150.tsv`、`KNOWLEDGE_CURATION_PROTOCOL.md` を読み取り専用で参照。現行PCの研究全文は未照合であり、**重複ゼロを保証しない**。従来11Hの `0x528DB0` における二系統集計（合計A/Bの独立IDIV）は先行成果として継承し、今回の新発見には計上しない。旧SAFE134の全件再検査は未実施、既存安全保留21件は変更しない。過去の安全拒否対象 `0x5710C0..0x571500` にも、その他既拒否コマンドにも触れない。

## 2. 新規STATIC：AリストとBリストは異なる挿入経路で管理される

原作ASMの `0x52909E: lea edi,[esp+0x68]` はA側の linked-list `head/count` 組へ `EDI` を設定し、`0x5290A2: E8 -> 0x5299E0` でAリストへノードを挿入する。`0x5290A7/0x5290AA` は既報どおり対応グループ `+0x34` をAの合計 `[esp+0x18]` へ加える。B側は `0x5290BE: E8 -> 0x4C52D0` で別途ノードを挿入、`0x5290D1: inc [esp+0x60]` でB件数を増やし、`0x5290DD/0x5290E0` でB合計 `[esp+0x20]` を更新する。

`0x5299E0` 内部の `0x5299E9 -> 0x4C52D0` はノード挿入補助への直接CALL。直後の `0x5299F1: mov edx,0x3FFFFFFE`、`0x5299F6: sub edx,ecx`、`0x5299F8: cmp edx,1`、`0x5299FB: jae 0x529A07` の**符号なし**空き件数判定を原作バイトで確認した。成功側 `0x529A07: inc ecx` と `0x529A08: mov [edi+4],ecx` がA件数を加算・保存する。

**Ghidra擬似Cとの差**：`functions/0052/005299E0.c` は上限を `unaff_EDI[1] == 0x3FFFFFFE` と略記しているが、元ASMには `0x3FFFFFFE - count >= 1`（unsigned条件）という分岐が存在する。普通の正規範囲では同等の境界を示す場合も、異常値・wrapを含めると単純な「==」と同一ではない。**コード忠実性の訂正候補**として記録し、異常状態で実際にどの経路が可能かはVERIFY。

## 3. 新規STATIC：モード3はB→Aの順にポインタVectorへ格納する

平均計算の後 `0x529138: cmp dword [ebp+0x474],3`、`0x52913F: JNE 0x5295E4`。モードが3なら、`0x529145..0x52914D` により `[esp+0x74/0x78/0x7C]` に0を書き込み、vectorのbegin/end/capacity相当を初期化。

- **1回目（Bリスト）**：`0x529159` で範囲終端の候補を取得し、`0x52915D: mov ecx,[edi]` から先頭取得、`0x529162: xor eax,eax; push eax` で挿入先先頭(0)を指定し、`0x52916C: E8 -> 0x52AB50` を実行。
- **2回目（Aリスト）**：`0x529171` で次の終端候補、`0x529175: mov eax,[esi]` で先頭、`0x529177: mov edx,[esp+0x78]` で**1回目後のvector末尾**を取得、`0x529186: E8 -> 0x52AB50` を実行。

**この制御フローの性質**は、既存11HのA/B二分岐を**単一vector上でBリストの範囲、続けてAリストの範囲**という順に格納することである。2リストを無条件に混ぜて平均するわけではない。以後に並べ替えやスキップがあり得るため、この順序が最終的な移動・対象選択の順序を決めると断定しない。

ヘルパー `0x52AB50` は `0x52AB85: cmp eax,ecx` で空範囲を判定し、異なれば `0x52AB90: mov eax,[eax] / 0x52AB92: inc edi` で範囲のノード数を走査。`0x52ABAB: mov ebx,0x3FFFFFFF` と `0x52ABB0..0x52ABB4` で容量上限を検査し、必要時には `0x52ABFC: E8 -> 0x42AC20` で増設経路を辿る。Ghidra擬似Cに`FUN_00535850`（範囲のコピー・構築）、`FID_conflict__memcpy` 等があり、例外時や容量境界のABI厳密性はVERIFY。

## 4. 後続処理への接続と未確証境界

直後 `0x5291A3..0x5291B4` はvectorの `end-begin` を4で割って要素数にする。`0x5291D4: fld qword [esp+0xF8]`、`0x5291DE: fstp qword [ebp+0x28]` は**vectorから取り出した要素が指すレコードの+0x28に、スタック上のdoubleをコピー**する。`0x52920F: cmp byte [edi+0x1867C],0` は、そのレコードのメンバーUnitを処理する際の喪失状態確認、非0なら `0x52921A -> 0x5292F3` のスキップ分岐。これは**11Hの5条件付き適格判定 `0x569610` と同じフィルタではない**。

T013の別研究にある `candidate+0xA14` や別の `record+0x28` との**同一オブジェクト同定はできない**。今回の `+0x28` が標的スコアや最終攻撃対象を表すとの推測は行わない。`0x5295E4` の非モード3経路、Vector後続の座標・行動制御・乱数やリアルタイム状態遷移はVERIFY。

## 5. 正確な出典・限定検証・KB_CANDIDATE

- 原作PE（SHA上記）の指定byte window、CALLsite `0x5290A2 -> 0x5299E0`、`0x52916C/0x529186 -> 0x52AB50`、`0x5299E9 -> 0x4C52D0`、`0x52ABBB -> 0x5B5B6D`、`0x52913F: JNE -> 0x5295E4` を原作ASMで検査。
- 擬似C `functions/0052/00528DB0.c` SHA256 `A2444391476AF79BF31F64465B3D344C30EA3E499E9D722D5D01F11D639CBEBC`、`functions/0052/005299E0.c` SHA256 `A4A9C3F7782D515032EA734D870758CE8913578B8CD70D9873591FC63DB2EE0C`、`functions/0052/0052AB50.c` SHA256 `51DB822423C6C80271801C2B42D0554840F6A5D1F7220387F25CCDEBA6089EFE`。相対pathはoffline pack内 `headless_analysis/full_pseudoc_20261020/HAKUSHIN067_FULL_PSEUDOC.zip` を起点。
- **限定静的検証 42/42件PASS**（原作EXE SHA・原本ZIP SHA・原作x86 byte windows・E8分岐・Ghidra関数SHA・アーカイブCRC）。読取専用スクリプト `data/B_20261101_12H_MODE3_DUAL_LIST_READONLY_VERIFY.py` と証拠 `data/B_OFFLINE_20261101_12H_MODE3_DUAL_LIST_EVIDENCE.json` に個別サイト記録。これは静的同一性・構造証拠であり実機Goldenではない。

**KB_CANDIDATE（正式登録しない）**：研究ID `B-OFFLINE-20261101-12H-T011-T024-DUAL-LIST-MODE3-VECTOR-01`、owner=B、task=T011/T024。VA `0x528DB0/0x5299E0/0x52AB50`、site `0x5290A2/0x52916C/0x529186/0x5299E9/0x52913F`、group `+0x34`、manager `+0x474`、Unit `+0x1867C`、record `+0x28`、relative source/SHA上記。STATIC=二分岐の元ASM、リスト件数、モード3のB→A vector挿入、容量ガード。INFERRED=隊列やAI用の候補集合形成という解釈。VERIFY=フィールド意味、挿入後の順序変更・最終行動、例外、PC新資料との重複・衝突。**Golden0 / strict MATCH0 / READY0**。10H/11Hの確認済み集計・近接式を重複計上しない。

## 6. Goldenで必要な対照・次の再開位置

原作ver0.67の同一EXE/DAT/MAP/SAVE、同じ戦闘シナリオ・グループ、Unit群、RNG、0/1/複数のA/B分類、`manager+0x474` が3／非3、`group+0x34`の正負境界、前後のlinked-list順序とvector要素順、各Unit+0x1867C、Record+0x28の変更、実際の移動/選択対象、次tickの差分を**原作で実測**して初めてGolden/MATCH判定できる。

PC復帰時は新規実装より先にMASTER/PROTOCOL/B HANDOFF/安全拒否台帳と、03H失敗ファイルの存在・SHA、04〜12H未同期成果のID重複・競合をチェックして、一度だけ許可B資料へ統合・独立readback。PC不通なら次は `0x5291D0..0x5293C2` でvector各レコードへ値を書き込んだ後の使用先、`0x5295E4` 非mode3経路、`0x52AB50`の例外/容量境界を**範囲限定**で比較する。T012のダメージ・回復・状態、T013の最終対象選択、T024通常AI、T028士気/敗走、T011召喚/経験値の未解明P0はすべて維持。