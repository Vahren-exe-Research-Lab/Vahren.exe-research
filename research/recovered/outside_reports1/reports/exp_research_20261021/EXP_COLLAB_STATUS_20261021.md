# EXP-COLLAB-20261021-2112-01｜2026-10-21 PC研究成果の最終状態

[COMPLETED / STATIC-INDEPENDENT / NOT READY / GAMEPLAY NOT RUN]
- PC Local接続成功。既存 MASTER/B HANDOFF/解析規約/Work queue・search_indexを先読し、担当ファイルはread-only。新規記録は既存 `exp_research_20261021` だけ。
- 新しい独立照合: `0x547490`, `0x553390`, `0x54E7B0` が4共通callee `0x577260 → 0x58B7F0 → 0x466BA0 → 0x577310` を条件付きに呼び出す。計12 direct siteをSQLで検証。12/12 PASS。
- 既知再確認: node+0x28 のR破棄連鎖。前回CP12と既P0の再チェックであり新規READY加算なし。
- `EXP_AI_EVIDENCE_20261021.json`: 26関数/26コードSHA一致、8指定CALL一致、SQLite integrity=ok、検索DB実SHA=manifest一致、+0x16C生文字列hit32（真のEXP writerは一部）。保存後独立readback成功。JSONのSHA256=BD709A5378F6C16CF8DBA74354F591A6736158E53B4D96E92A3A76267ECA60B8。
- `EXP_THREE_PRODUCER_CALLS_20261021.json`: 12/12 PASS・SHA256=BADC35023251625B22C902C9121F048D76C5BCF741FC9C1E49B4F5A122D96F1C。
- 研究入口 `EXP_SHARED_INDEX_20261021.md`、再開 `EXP_RESUME_20261021.md`、手順 `EXP_COLLAB_HANDOFF_20261021.md`、2つのCPをPCに新規保存/読み戻し。
- PC独立共有 `EXP_AI_COLLAB_PACK_20261021.zip`: 11エントリ、31,589 bytes、SHA256=178535E0F6B2F01BCBB339E52935E6D043D465B320CD963B6173FF783280EDF8。ZIP CRC + 同梱MANIFEST全ファイルSHA=PASS。
- ChatGPT作業環境側では別の `HAKUSHIN067_EXP_COLLAB_PORTABLE_20261021.zip` を作成（研究資料+元オフライン機械解析、374エントリ、20,780,782 bytes、SHA256=C92E1FB104989B528573DD37E642B41D8082F1C51B7FD3AC5D9A158BE7BF8213、CRC+各SHA=PASS）。この20MB版は **PCへコピー済みではない**。チャットの添付リンク経由で別AIに渡す。

[NOT CLAIMED]
- 新 B READY=0 / E MASTER正式統合=0 / Task DONE追加0 / 原作実機Golden PASS=0 / 新旧strict MATCH=0。
- 間接callerの完全性、同一キーによる3producer間R共有、戦闘終了時のR→戦略EXP移転やR破棄の実時刻は未証明。
- 原本EXE/DAT/SAVE・既存DB・MASTER・B/E/Work/REA/他lane・Git/pushに変更なし。既安全拒否案件の代替再試行なし。

[NEXT]
- PC接続あり: `EXP_SHARED_INDEX_20261021.md` からコードSHAと各siteを復元し、0x547490/0x553390と0x54E7B0のcache-ownerとキー供給元を比較。
- PC接続なし: 20MBポータブルZIP内 `AI_HANDOFF/INDEX.md` と `AI_HANDOFF/EXP_MACHINE_CROSSJOIN.json` を読み、オフラインGhidra DBに対して確認する。
- 研究B/E/Workへは各担当がこの文書と索引を読み、重複・所有権を判定したうえで正式取り込み。別チャットへの自動通知／統合は未実施。

[CP03 POST-CHECKPOINT]
- 上位種別4分岐: 0x545CC0→0x547490@0x546469、0x552EF0→0x553390@0x553177。Skill+0x40==4分岐および後者Skill+0x74反復/zero fallbackを保存擬似C確認。
- `EXP_KIND4_DISPATCH_EVIDENCE_20261021.json` 条件6/6・直接CALL2/2・関数コードSHA2/2 PASS、SHA256=2ED20B36BAFD21338B169A236C9AED92A151566F7B3F9C8E8F35D985672186ED。
- 既存CP02との重複部分は再計上0。新たに確定したのは上位dispatch gate、通常battle実機は依然NOT RUN。

[ADDENDUM / 2026-10-21 / EXP-CACHEKEY-20261021-01]
- ユーザー方針により、通常研究中の新規ZIP作成を停止。新規資料は既存exp_research_20261021直下のMD/JSON/Pythonで直接読めるよう保存。
- 新規限定静的差分: node+0x0Cが文字列キー、node+0x1Cが文字列長、node+0x20がcapacity。UnitData R=node+0x28、node512byte/R468byte。登録0x577310=EAX pointer、ret0x1D4（元Ghidra voidとの不整合）。
- EXP_STRING_CACHE_ABI_EVIDENCE_20261021.json: 原本SHA実測一致、native39/39 PASS（PE変更0）。
- SAVE root+0x300のnode+0x28はUnitData*値、召喚元+0x1E4B4のnode+0x28はUnitData値本体。EXP_SAVE_TREE_BOUNDARY_EVIDENCE_20261021.json: native10/10 PASS、SAVE writer0x58EFD0直接caller=0x460000@0x46030B 1件。
- 先行Bのnext_order/+0x270・固定文字列/候補一覧、既存CP12 R破棄は旧知見。新規採番/READY重複加算0。
- 独立 `EXP_SHARED_INDEX_20261021.md` 冒頭索引更新成功/読み戻し済。
- 原本EXE/DAT/SAVE、既存DB/Ghidra、MASTER/他lane/Work/queue/Gitの変更0。拒否対象再試行停止。
- 残り: native直接SERIALIZE != EXP TRANSFER無しの証明。実機未観測・Golden0/strict match0・正式READY0。
