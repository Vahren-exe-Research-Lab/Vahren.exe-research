# 迫真戦記 ver0.67｜REA 18時台 P0：CRT SEH funcletの未索引E8 CALL
研究ID: REA-LOCAL-20261026-18H-P0-CRT-SEH-ORPHAN-E8-XREF-STATIC-01
状態: PC-SAVED / STATIC / VERIFY / NOT READY（2026-10-26 JST）
対象原作EXE SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
現行V3 DB SHA256: 0B057C43D30EAEC74588C84CF7E09AA7A488BD0FF170925591953EF578AFCB25

## 前提と重複防止
PCはLocal Compactでアクセス成功。MASTER/規約/REA README・QUEUE・PROGRESS/旧RUN・保存済み16H報告/旧検索README・manifest/現行V3 guide・stateを先読。
V3のread-only guardはPASS_ACTIVE_V3_STATIC、input hashes 14件、エラー0。旧search.sqliteは歴史的snapshotであり、今回の新規解析の正本はV3。
既存REA同期ログ progress_sync_20261011T153958076Z.json は64/64（古いQUEUE/PROGRESSはEPERM後のstale）。過去64件・16Hの既存CRT SEH発見は今回の新成果へ加算しない。
今回の新規差分は、16Hでnative CALLを確認した起動側SEH funcletが、現行V3の関数所有範囲とCALL索引から欠落している点の独立照合。

## 独立静的証拠：3つの未索引E8
| 原作CALL site | 原作E8 bytes | 解決先 | 現行V3 E8 call rows | Ghidra ref rows |
| --- | --- | --- | ---: | ---: |
| 0x005B8612 | e882630000 | 0x005BE999 (__XcptFilter) | 0 | 0 |
| 0x005B862A | e8f62f0000 | 0x005BB625 | 0 | 0 |
| 0x005B862F | e816300000 | 0x005BB64A | 0 | 0 |
原作EXEのPE ImageBase=0x00400000を使用し、各E8+rel32の転送先を個別計算。Capstone独立逆アセンブルでも3個ともCALL。
CRTのSEH4 scope record (0x006412D0) は filter=0x005B8606、handler=0x005B861A。つまり0x005B8606..0x005B8633の46バイトは例外処理用の実行コードであり、単なる未使用paddingではない。
現行V3の0x005B84D7(___tmainCRTStartup)のfunction_rangeは 0x005B84D7..0x005B8605 (303B) と 0x005B8634..0x005B8643 (16B)。間の46Bはこの関数のbodyに属していない。
比較対象の0x005B7CA7→0x005BE999と0x005B863E→0x005BB6C5はV3にE8として存在。索引全般の壊れではなく、今回の未所有例外funcletの限定的な参照欠落。
その結果、現行V3のcallers 0x005BE999は__callthreadstart側 0x005B7CA7だけを返し、CRT startup SEH filter側0x005B8612を表示しない。**V3の44,889件はGhidraに既登録されたE8参照の分類結果であり、EXE上の全E8の網羅証明ではない。**

## 境界・リスク・継続
本件は検索索引の取りこぼしであり、原作のゲーム動作不具合を示すものではない。Ghidra/検索DBを改変せず、REA所有の独立証拠だけを新規保存する。
16Hで示した「初期状態の12種のCRT例外表にbad_allocコードE06D7363が無い」という条件付き結論を維持。今回、runtime signal登録/VEHの有無やゲームでの終端を追加実証していない。
新規限定監査: 20/20 PASS。info=INDEX_ONLY、pseudo=INDEX_ONLY、assembly=TARGETED_NATIVE、callers/callees=INDEX_ONLY（例外funclet欠落あり）。正式REA5種完備追加0、正式VERIFIED追加0、TODO/VERIFY/BLOCKED公式書込差分0/0/0、原作ゲームGolden実測PASS0、strict MATCHと完全複製率は未測定。
次P0は0x004BE480の+0x70管理配列の例外時解放者を限定確認。また0x005B8612/2A/2Fは他担当へ修正要請する場合も静的索引欠落として渡し、Ghidra全件再抽出は禁止。
原本EXE/ZIP/SAVE、既存runs、QUEUE、PROGRESS、MASTER、A〜E、Ghidra検索DB・正本、T018、dev_lab、Git、公開先、Work、スケジュールの変更なし。旧OFFLINE-UNSYNCEDは未同期。
