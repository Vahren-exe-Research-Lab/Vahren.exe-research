# 迫真戦記 新B｜T012 damage core x87 フラグ分岐の限定再検証（2026-10-24 13時台）

研究ID: `B-OFFLINE-20261024-13H-T012-DAMAGE-X87-FLAG-GATE-01`。復旧ID: `B-RC-20261024-13H-LOCAL-SESSION-LIBRARY-DELTA-01`。状態: **OFFLINE-UNSYNCED / STATIC-RECORDED-PE-HEX / ISA-DERIVED / VERIFY / NOT READY**。

## 証拠と安全境界

Desktop Commander Local Compact で MASTER・規約・B HANDOFF の一括読取りを最優先で試行したが、実エラーは `INVALID_ARGUMENT: McpServerError: Session terminated`。分類は **CONNECTION** であり安全拒否ではない。PC最新MASTER、READY/owner、未同期22ファイルと後続10研究のID対応は未照合。過去の安全拒否範囲（`0x005710C0..0x00571500`、`0x0058021E..0x00580340`）は今回検索・読取りをしていない。Work/Remote/原作EXEの実行・再解析を行わず、原本/他レーン/Git/設定/スケジュールに変更なし。

現runで閲覧できた2026-10-24 11:11保存済みの `B_T012_T028_STATIC_RETURN_DEATHBRANCH_EVIDENCE_20261024_1111.json` に格納された**原作PEの既保存hex**から、限定 `0x005510E1..0x00551156`（end exclusive; 117 bytes）を再度機械的にSHA256検証し、`objdump -m i386 -M intel`で再解釈した。保存区間のSHA256=`BDB6A82E2E265E72DC8323CC2855694F456532DB208C6DD82507A9010D9458DB`（既存JSON記載値と**一致**）。本runでは原作EXE実体と検索SQLiteを新たに入手・ハッシュ照合していないため「今日のEXE現物検証」とは称さない。保存レポートに記載された元EXE SHA256=`E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`は過去の証拠由来。

## 新たに詳細化した局所的制御条件

`0x00550E70`内で `0x005510F1 FLD QWORD PTR [ESI+0x280]` → `0x005510F9 FLDZ` → `0x005510FB FUCOMPP` → `0x005510FD FNSTSW AX` → `0x005510FF TEST AH,0x44` → `0x00551102 JP 0x00551108` が並ぶ。

`FNSTSW AX`のAHにはx87状態のC3(bit6), C2(bit2), C0(bit0)が含まれる。`TEST AH,0x44`後の`JP`は、**C3とC2のセット数が偶数である場合**に成立する（C0はマスク対象外）。これにより、単なる「浮動小数点値が非ゼロならJP」という一般化から、以下の**例外的なunordered条件**を区別できる。

| 0 vs Skill+0x280 | C3 | C2 | AH&0x44 | JP | 当該ゲートの出口 |
|---|---:|---:|---:|---|---|
| ordered、値が正 | 0 | 0 | 0x00 | **成立** | `0x551108` |
| ordered、値が負 | 0 | 0 | 0x00 | **成立** | `0x551108` |
| ordered、値が+0/-0 | 1 | 0 | 0x40 | 不成立 | `0x551104` でECX=0 |
| unordered（NaN） | 1 | 1 | 0x44 | **成立※** | `0x551108` |

※NaNが実データから到達可能で、x87例外で処理が中断せず、該当命令まで到達する場合の**命令レベルの条件付き推定**に限る。原作ゲームでNaNダメージや命中成功を観測したわけではない。

後続の条件も同じ保存hexで確認した。`0x005510E5 CMP EDX,0x0A`一致なら`0x5510EC JMP 0x551156`でvslot+0x70 CALL `0x551154`を飛ばす（これは以前からの抵抗10既存成果）。一致しなければ、上記x87ゲートでゼロ時はECX=0を設定し、`0x551143`の4引数組立てへ直行する。JP側では`0x551108 CMP [ESP+0x18],6`一致時はECX=EDI、`0x551113 TEST EDX,EDX`ゼロ時は`0x551117 MOV ECX,0xF4240`、その他の通常枝のみ`0x551138 MOV EAX,[0x65BDA4]`→`0x55113D CMP ECX,EAX`→`0x55113F JGE`による**符号付き下限clamp**へ進む。したがって**下限clampは全経路共通ではない**（この構造自体は旧T012既成果、再加算しない）。

**新規増分の範囲**は、この既存damage routeにおける`TEST AH,0x44` / `JP`の真理値と、有限ゼロ・非ゼロ・unorderedの分離を保存済み生バイトから局所再導出したこと。x87 unorderedを考慮した*別の距離比較*は既にB-20261015-1817-01で研究済みであり、同じ成果として計上しない。PC最新T012/HANDOFFとの同義重複検査ができないため独立正式READYにはしない。

## 実機Golden条件と次P0

Goldenには同一の無改変原作EXE/DAT/SAVE/MAP/入力/RNGを揃え、`Skill+0x280`の実effective倍率が正／負／ゼロになる合法DATとresistance=0/1..9/10、mode6/non6、最低ダメージ分岐および被弾側のHP・死亡イベントを比較する。NaN/±∞は合法DAT生成・x87 control word/例外が未確認なので**Golden適格性はVERIFY**。追加調査すべき源はBの保存T012 parser (`Skill+0x280`) と受け渡しルート `0x00550E70` / CALL site `0x00551154`。既拒否コードには踏み込まない。

原作Gameplay Golden PASS=**0**、strict MATCH=**0**、新規READY=**0**、DONE増加=**0**。保存先はこのチャットの作業用ファイル、Library B所有`data/`（成功後にreadback）。PC `LANE_B_HANDOFF.md`への書込みは未実施。

## 復旧事項

12:09旧研究ID `B-OFFLINE-20261024-1209-T012-T028-STATIC-RETPOINTER-BRANCH-ABI-01`のLibrary初回版と手元の完全版が食い違うことを、両MD/JSONを入手しSHA256比較した結果として再確認。Library初回 MD SHA=`3939366537CF40D1CABA6D796F538AFE875EBE3BD6E10F5DC96CB52E7DFB6C49`、完全 MD SHA=`54732BCAFE3B469B2B4F8CDB46F6F6C7A291D080565149391C1CA76E9D5BE1D3`、Library初回JSON SHA=`709139201F32A1ACDFA46E7D19C5D4BF3ABC9C62A6AD72D65E620D72ADF1D5A2`、完全 JSON SHA=`02F90F3BDDFD4EAB4B733A82297073033ED9F4F3C3F04DB36ED371BF0813931F`。差分は3つのvcall後のAL非消費検証と保存失敗記録。B Library内の旧研究を重複作成せず、同名の改訂版への上書き・読み戻し可否を別途記録すること。PC正本は未同期のまま。

## 13時台保存・readback確定状況（本run追記）

1. **12:09既存2ファイルのLibrary版ズレを回収成功**：Library `B_T012_T028_STATIC_RETPOINTER_BRANCH_ABI_OFFLINE_20261024_1209.md/.json` は同名の完全版で上書きし、別途Libraryから実ファイルを取得して2/2のSHA256一致を再確認した。最新MD=`54732BCAFE3B469B2B4F8CDB46F6F6C7A291D080565149391C1CA76E9D5BE1D3`、JSON=`02F90F3BDDFD4EAB4B733A82297073033ED9F4F3C3F04DB36ED371BF0813931F`。これはBの**Library保存・読み戻し成功**であり、PC `LANE_B_HANDOFF`同期ではない。元の12:09本文内の「Library旧版」という記述は当時の失敗履歴で、**現在の保存状況ではない**。
2. 初回Library更新に`container_session_unavailable`が2件生じたが、安全拒否ではなく**FILES TOOL TRANSPORT**。会話に既存する完全版の`source_file_ref`を正規のアップロード手段として使い、2/2復旧。既拒否済みコードの取得迂回ではない。
3. **本13時台の新規MD/JSONは作業コンテナに保存・ローカル読み戻し2/2**。Libraryへの新規アップロードは`container_path`側の同じ transport 障害により未達（以後の重複作成は避ける）。PC正本への保存・読み戻しも0。PC復帰時にはB HANDOFF/既存IDを照合し一度だけ取り込む。
