# E-AUDIT-20261031-05H-T020-T013-MODE3-EBX-GATE-01
Owner: E/T018-T019-T020 | 2026-10-31 05H JST | STATIC BYTE / SYNTHETIC EXECUTED / VERIFY / NOT READY

## 入力・重複・所有権
- PC ONLINE（Desktop Commander Local Compact）。MASTER、ANALYSIS_LANES_PROTOCOL、A-D HANDOFF、E T018/T019/T020、DEV IMPLEMENTATION_PLAN、REA現行V9案内をread-only参照。非公開GitHub知識正本developのREADME.md/SYNC_STATUS.md読取成功。GitHub先端コミットSHAの独立照合は未実施。
- PC knowledge/README.md、SYNC_STATUS.md、symbols.tsv、kb.py addr/docs/research/findを先読。0x44C72Bの手書き名前なし・研究全文索引にはB05所有記事あり。KB/sourceとE04資料を重複しないよう確認。
- 今回の独立入力はB-20261031-05H-T013-EBX3-INPUT-01（B/T013、VERIFY/NOT READY）。B詳細data/T013_MODE3_EBX_CATEGORY_PRODUCER_NATIVE_20261031_05H.md SHA256=B215DA79D04633E82714FFE8FBD5888F8B5758F507BF0FDCB1BA4EA7ED7187CF。B ownerは変更しない。

## 原PE BYTE／V9 静的照合と条件付き推論
- 研究コピーPE SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。0x44BBB0..0x44C78Fの局所SHA256=038074665B67A98162A469F99444886898148A5DF2EB2BD939132BEB5EA61CE2（B根拠と一致）。
- 0x44C72B MOV EBX,3、0x44C76C PUSH EBX、0x44C76D PUSH EBPを独立Capstone byte decode照合。E8 CALLの実宛先は0x44C743→0x5690C0、0x44C767→0x49D1B0、0x44C76E→0x449500で3/3一致。
- V9 function 0x49D1B0は163-byteの保存擬似Cで、vtable+0x58と+0x24の間接CALLを含みverified_abi=0。従ってEBX=3が0x449500へ届くのは間接calleeを含むEBX保存が成立する場合のみ。原作実機の引数値は未観測。
- 非空Unit配列の場合の限定モデル：manager+0x98>10なら3(push)、<=10なら6(advance)、さらにgroupflag!=0かつmanager+0x18==0で7(even)。空配列はUnit書戻しなし。0x49D1B0呼出gateはmanager+0x18==0 AND manager+0xA5==0。入力3では1/7専用btl_limit時計条件を通らない。

## T020合成回帰（原作互換性ではない）
- E専用tests/t020_e_t013_mode3_ebx_conditional_gate_20261031_05H.pyを新規作成し、原PE/B出典SHA・命令・3直接CALLを固定。fixtureはtests/T020_E_T013_MODE3_EBX_CASES_20261031_05H.json。
- vector長0/1/4 × manager+0x98=9/10/11 × groupflag0/1 × manager+0x18=0/1 × manager+0xA5=0/1 = 72件。合成出力はUnit書込なし24、category3=16、category6=24、category7=8件。72/72 PASS、独立再実行72/72 PASS。
- E04の288件、E03の144件、E02の224件も実行し、今回の異なるfixture群合計728/728 PASS、exit codeすべて0。前回までの全履歴を再実行したという意味ではない。PE/static係数検証と実Gameplay MATCHを混同しない。
- 既E04のUnit複数fan-out・ランダム呼出回数モデルと今回のカテゴリ入力条件を接続。ただし動的vector変化・EBX非保存virtual・FPUゲートの合法到達・最終Unit field・乱数系列・実移動/戦闘動作はVERIFY。

## T018/T019、MASTERとKB候補
- C-NB02原作合法G0通常戦闘UI／G1同run直前未改変SAVE bytes+入力／G2実MAP・攻防支援3sideとordered Unit/Troop／G3終了可視／G4 World差分は必要な一体化証拠が未充足。Karate×20改変前DAT bytes復元確認も前提。DYNAMIC OBSERVED0 / actual Golden PASS0 / strict MATCH0。
- T019新規確定原作矛盾0。GameClear DAT13+TXT2はsource-scope RESOLVED、script2優先/flag/TXT runtime/gwrite/decide11はVERIFY。B19/B01のSHA記載不整合は旧E04時点の要訂正であり今回は独立再検査せず。
- KB_CANDIDATE: owner B/T013; VA 0x44C72B(code MOV EBX,3), 0x44C76E(E8→0x449500), 0x49D1B0(virtual間接呼出 ABI未検証); source=data/T013_MODE3_EBX_CATEGORY_PRODUCER_NATIVE_20261031_05H.md:L9-L18 SHA256=B215DA79D04633E82714FFE8FBD5888F8B5758F507BF0FDCB1BA4EA7ED7187CF; evidence=原PE局所SHAと3 E8 source SHA EXE=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187; classification=STATIC/INFERRED/VERIFY、actual Golden=0、READY=NO。knowledge/symbols.tsv/structs.tsv/生成DB/Gitは変更せず専任KB統合担当判断待ち。
- MASTER最終正式checkpoint196/READY596=A115/B229/C136/D116、34 Task DONE9/IN_PROGRESS21/VERIFY4は既確認値の継承であり今回再集計なし。B05 NOT READYのため正式新規READY ID0・MASTER反映0。

## エラー・保存・再開
- 初回のread-only Python -cはPowerShell引用符のためNameError（OTHER/RECOVERED、検証結果未成立、書込0）。E所有新規スクリプトを保存し正規実行して解消。新規SAFETY_REFUSAL0、旧拒否はBLOCKED維持で別tool/path/shell/Remote/ZIP迂回0。旧OFFLINE-UNSYNCED全照合は未完了。
- NEXT: 0x49D1B0の間接calleeレジスタ保存・0x44C778分岐と、0x577220の書戻し後効果を合法STATICで限定検証。原作G0/G1/G2同run一次証拠の確保が最優先。
