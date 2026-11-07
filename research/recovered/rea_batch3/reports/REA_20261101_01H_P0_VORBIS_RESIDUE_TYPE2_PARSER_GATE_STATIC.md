# REA｜2026-11-01 01時台：Vorbis residue type 2 の入力ゲートと実行経路
研究ID：`REA-LOCAL-20261101-01H-P0-VORBIS-RESIDUE-TYPE2-PARSER-GATE-STATIC-01`。担当 REA / T015、P0。分類 **PC-SAVED / STATIC / VERIFY / NOT READY**。旧00H成果 `REA-LOCAL-20261101-00H-P0-VORBIS-INDIRECT-CALLBACK-DISPATCH-STATIC-01` の「間接CALL実在」と重複させず、今回の差分を**入力からtype 2が保存される条件と範囲検査**に限定する。

## 独立した新規証拠（元PE x86）
- 対象 `FUN_005D4160` はVorbis setupの型別情報を読み取る静的解析上のパーサ候補。原本コピーのSHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。2026-10-23統合V9 DBのSHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE` と照合。
- `0x5D428F: lea edi,[ebx+0x620]`、`0x5D4295: push 0x10` に続く `0x5D4298: call 0x5E6E10` は16-bit selector読取候補。 `0x5D42A0: mov [edi-0x100],eax` で配列の `setup+0x520+index*4` に格納する。
- `0x5D42A6: test eax,eax`、`0x5D42A8: js 0x5D43FD` は負値を拒否、`0x5D42AE: cmp eax,3`、`0x5D42B1: jge 0x5D43FD` は **3以上を拒否**。よって受理される型番号は **0, 1, 2** であり、**2は静的に有効な入力**。元x86命令バイト・命令境界を独立照合した。
- `0x5D42B7: mov eax,[eax*4+0x612E60]` は型番号からcallback groupを選び、`0x5D42C1` で `group+4` のparserを読み、`0x5D42C6: call edx` を実行。後続 `0x5D42CD:test eax,eax` と `0x5D42CF:je 0x5D43FD` はparse結果NULLを拒否。type 2では `0x612E68 -> 0x61AEA0`、`0x61AEA4 -> 0x5DFE10`。前回発見したtype 2の `0x5E0B80 / 0x5E0CF0 / 0x5E0DC0` 間接呼出しに、入力検証済み型番号の上流出典を接続できた。
- この番号は初期化 `0x5D57C0` の `0x5D5AAA: lea ebx,[esi+0x520]` / `0x5D5AC0:mov edx,[ebx]`、解放 `0x5D4AE0` の `0x5D4BE0:mov eax,[edi+ebx*4+0x520]` でも参照される。同じsetup配列を読取・初期化・解放に使う関係が成立する。ただしパーサの戻り後の実プレイ到達は未確認。

## 以前の疑問の訂正：root +0x0C は第4の有効residue型ではない
`0x5D4313` にある別配列への型保存、`0x5D4321:cmp eax,1` / `0x5D4324:jge 0x5D43FD` により、この別型は **0のみ受理**。`0x5D432A` は `[eax*4+0x612E6C]` を参照し、`0x5D4339` で別callbackを呼ぶ。ここは**別のmapping型選択系**と区別する。以前の00H報告で第4グループにも見える `0x612E6C` の隣接ポインタを、**residue selector=3 が有効**との推測には使えない。旧00Hの「3到達未確認」は今回 **residue parserが3を拒否する** ことで絞り込まれた。ただし不正メモリ破損等での異常selectorや別入口は無証明。

## 未解決、KB_CANDIDATE、判定
- **実ゲームのOGGが residue type 2 を含むか**、parse成功後に該当decodeが実行されるか、NULL確保時に挙動が破綻するかはVERIFY。 `0x5E0DC0` の分母は `piVar1[2]` と `*(int*)param_2[4]`。共通parse `0x5DFE10` では `piVar1[2] = read24+1` と見えるが、bit reader異常値・第二分母・上流入力検証は未証明。ABIの正式確定やクラッシュ実証はしない。
- **KB_CANDIDATE**: owner REA/T015、VA `0x5D4160`、実行site `0x5D4298,0x5D42A0,0x5D42A8,0x5D42B1,0x5D42B7,0x5D42C6`、residue setup `+0x520`、mapping `0x5D4324/0x5D432A`、参照 `0x5D57C0,0x5D4AE0,0x5DEDF0,0x5DF7D0`。相対証拠 `rea_lab/decomp_task/REA_20261101_01H_P0_RESIDUE_TYPE2_EVIDENCE.json`。ソース/索引SHAは上記。STATIC、実動作VERIFY、Golden0、READY0。共有KBは専任統合担当のみ改訂。
- 新規正式5種証拠（info/pseudo/assembly/callers/callees）完備 **0**、新規正式VERIFIED **0**、旧正式STATIC VERIFIED **64件を前回保存履歴として維持（今回再認定していない）**、正式TODO/VERIFY/BLOCKED差分 **0/0/0**。原作Golden実測PASS0、strict MATCH0、完全複製率未測定。
- 自担当内に読取専用プローブ2本、原本PE/統合V9 SHAと**42項目の独立静的監査PASS**を保管。新規REA/Ghidra/ゲーム実行なし。PCは01:34 JSTに接続正常、active.lockなし、Java/Ghidra競合0、開始時空きRAM 17,207,432 KiB。CPU実測と全工程時間は不明。readback証跡は別ファイルで保存する。
- **次の優先**：実OGG音声の原作パケットを実行せずに許可済み解析資料から型番号の存在/欠如を探す。 `0x5DFE10` の戻り値エラー時も含め `0x5E0DC0` 二つの除数の非ゼロ保証を上流へ伝播、必要なら5種証拠の新規正式取得候補として別途条件確認。旧禁止VA/Wave6には触れない。原本・MASTER・QUEUE・PROGRESS・他owner・共有knowledge・Git・スケジュールを変更しない。
