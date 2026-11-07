# REA｜2026-10-31 14H｜Vorbis初期化ラッパーの重複cleanup・戻り値伝播（P0）
研究ID: `REA-LOCAL-20261031-14H-P0-VORBIS-WRAPPER-DOUBLE-CLEANUP-GATE-STATIC-01`
Owner=REA、Task=T015。状態 **PC-SAVED / STATIC+INFERRED / VERIFY / NOT READY**。
前件13H `REA-LOCAL-20261031-13H-P0-VORBIS-CLEANUP-COUPLED-ARRAY-GUARD-STATIC-01` の同CALL・calloc・条件付きリークは再計上しない。

## 入力・非重複照合
- 研究専用PE: `rea_lab/targets/hakushin067_Vahren.exe`; SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
- 統合V9 read-only: `rea_lab/headless_analysis/search_index/HAKUSHIN067_UNIFIED_V9_20261023.sqlite`; SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`、SQLite quick_check=ok。
- MASTER/レーン規約/REA README・QUEUE・旧PROGRESS、最新正式sync `logs/progress_sync_20261011T153958076Z.json`（64/64）、13H evidence/readback、PC knowledge README/SYNC_STATUS、GitHub private develop `REF_AUDIO_VORBIS.md`/symbols.tsvを先読。
- `knowledge/kb.py addr/docs/research 0x005D5BD0` は0件、`addr 0x005D57C0` は未命名。共有 `REF_AUDIO_VORBIS.md` に今回の研究ID・wrapper VAなし（14H照合時）。
- 旧 `search_index/README.md`/`BUILD_MANIFEST.json` は現在のrootに存在せず ENOENT。既存13Hと同じ配置差異なので、承認済みV9別名入口・固定SHAを使用。安全拒否ではない。
- 事前 `active.lock`なし、Java/Ghidra競合プロセスなし、空きRAM約15.74GiB。CPU負荷・総作業時間不明。ゲーム・REA/Ghidraの新規実行0。

## 新規差分1｜wrapperが失敗と成功を正規化
- 原作x86 `0x005D5BD0` の `0x005D5BDE: E8 -> 0x005D57C0` は引数末尾0で初期化コアを呼ぶ。直後 `0x005D5BE7 test eax,eax` / `0x005D5BE9 je 0x005D5BFB`。
- 非0時は `0x005D5BEB: E8 -> 0x005D4AE0` で外側cleanupし、`0x005D5BF3` で戻り値を1へ正規化。0時は `0x005D5BFB: E8 -> 0x005D4D20` 後、`0x005D5C03 xor eax,eax` で0を返す（calleeの戻り値は局所では確認しない）。
- wrapperを呼ぶ `0x005CF9A1` と `0x005CFA45` は双方とも原作E8直接CALL。周囲のcaller error mappingは別件なので、今回の関数意味の確定ABIや実ゲーム戻り値とは混同しない。

## 新規差分2｜変換失敗時のcleanup二回到達と限定的な安全条件
- `0x005D57C0` のcodebook変換非0結果は `0x005D5B59/5B5B` から失敗側へ分岐し、`0x005D5BB8: E8 -> 0x005D4AE0` を経て `0x005D5BC2 or eax,-1` / `0x005D5BC9 ret`。wrapperは非0としてさらに `0x005D5BEB` cleanupへ進む（STATIC）。
- `0x005D4AE0` の正常完了は `0x005D4D0E` の memset(outer,0,0x70) を経由する。よって**最初のcleanupが正常に完了し、対象outが同一で、途中に再初期化・競合・aliasがない条件**では二回目はゼロ化された管理領域を再処理する。これ自体は二重freeの実証ではない。
- 変換成功側 `0x005D5B84 jmp 0x005D59A9` が後段の外側配列確保 `0x005D59BA/0x005D59CD` へ合流する。失敗側 `0x005D5B89..0x005D5BC9` はそこへ合流せずcleanupするため、**13H外側+8=NULL/+0xC非NULLの部分確保状態をこの変換失敗分岐から実証したことにはならない**。
- 一方 `0x005D57CD` の [param2+0x1C] NULLは `0x005D57D8 ret` で**outer memsetより前に+1で戻る**。wrapperはそれでもcleanupする。呼出元が提供したouterの既存初期化状態・再入/alias・NULL時の完全安全性は VERIFY。

## 証拠品質・境界
- 新規probe `REA_20261031_14H_P0_WRAPPER_CFG_PROBE.py`：許可済み研究用PE32を非実行で局所disasm。V9検索CLI function/callers/calleesで関数入口・CALL siteの所有関係を確認。
- `REA_20261031_14H_P0_WRAPPER_ERROR_GATE_AUDIT.py`: **41/41 PASS（0.8475秒）**。E8 9件、命令16箇所、局所PE window 4件、親13H証拠・正式64件・V9/hash/SQLiteを照合。
- `REA_20261031_14H_P0_WRAPPER_ERROR_GATE_READBACK_VERIFY.py`: 独立再読取 **39/39 PASS（0.8508秒）**。出典PEとV9・CALL/ASM・window hash・証拠SHAを再照合。
- 証拠 `REA_20261031_14H_P0_WRAPPER_ERROR_GATE_EVIDENCE.json` SHA256 `36979FE291CB56A319D7C993DC5080218A3D0C7F4DBD8ADCB2110A6000CF1E3F`、読戻しJSONを新規保存。元PE / V9 / 旧成果 / 他owner / Git / MASTER / QUEUE / PROGRESSは変更0。
- 正式5種（info/pseudo/assembly/callers/callees）**新規完備0**、新規正式VERIFIED **0**、既存正式STATIC VERIFIED **64/64維持**、正式TODO/VERIFY/BLOCKED差分 **0/0/0**。原作Golden実測PASS **0**、strict MATCH **0**、完全複製率 **未測定**。

## KB_CANDIDATE（統合担当への候補／REAから共有knowledgeの直接編集禁止）
- 新規固有差分：`0x005D5BD0` の内部初期化非0時の `0x005D5BEB` 再cleanupと1への正規化、0時の `0x005D4D20` 戻り値破棄。内部 `0x005D5BB8` cleanup後の2回目到達。欠落+0x1C時の前memset早期return。source SHA / call sites / 研究ID・ownerは上記。
- 13Hの外側配列リーク候補は**独立の条件付き発見**として維持し、変換失敗にそのまま結び付ける解釈は避ける。STATIC/INFERRED/VERIFY、DYNAMIC=0、READY=NO、Golden=0。
- **次回P0**：`0x005CF970`/`0x005CFA10` の `outer+0x1E0` 初期値・再初期化所有権と `0x005D4D20` の後処理失敗条件を独立追跡。未実測のNULL/例外・OOM/実ゲーム到達性はVERIFY。

## 障害・保存
- RECOVERY-ID `REA-LOCAL-20261031-14H-OTHER-OLD-INDEX-PATH-ENOENT-01`: 旧README/MANIFESTのENOENTを確認。既知の配置差異であり、安全拒否ではない。現物V9入口をread-only検証し、未保存の解析差分なし。
- 既存13H報告の名前を取り違えた最初のread_fileはENOENT、実在の `REA_20261031_13H_P0_VORBIS_COUPLED_ARRAY_CLEANUP_STATIC.md` を読み戻して復旧。安全拒否・PC接続失敗なし。新規5ファイル（probe/audit/evidence/readback verifier/result）と本報告のみ追加、担当外へ書込なし。
