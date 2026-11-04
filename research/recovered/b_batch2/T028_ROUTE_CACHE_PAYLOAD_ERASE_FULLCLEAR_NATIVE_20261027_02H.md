# B-20261027-0216-T028-CACHE-ERASE-PAYLOAD-OWNER-01｜T028経路キャッシュ退避物の破棄順とhash一括削除分岐
記録時刻: 2026-10-27 02H JST / owner=B/T028 / STATIC-ORIGINAL-PE-ASM + STATIC-GHIDRA / INFERRED・VERIFY / NOT READY

## 先行確認・基盤
- Desktop Commander Local Compact接続。MASTER最後のE正式checkpoint196・READY596（全件再集計ではない）、ANALYSIS_LANES_PROTOCOL、B HANDOFF、B所有T011/T012/T013/T024/T028、未同期回収索引・安全拒否履歴を読取。
- 2026-10-25 14H OFFLINE研究全文などの意味的同期未完。既拒否0x5710C0..0x571500/拒否済ペイロードの再試行・迂回0。新Ghidra/REA/Work起動0。原本実行/改変0。
- 原作Vahren.exe（ゲーム直下）SHA256実測 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。V9検索DB現物SHA256 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE、SQLite immutable read-only quick_check=ok。旧search.sqlite README/BUILD_MANIFEST確認、新規Ghidra全面再解析なし。

## 新しい原作ASM証拠（01Hのキャッシュキー・8000/8192分岐は再計上しない）
- 0x4EC4F0 CALL0x4EC720（順序リスト先頭のキーでhash node検索）、0x4EC4F9 MOV ESI,[ECX+0xC]でpayload pointerを読む。0x4EC4FC TEST ESI,ESI / 0x4EC4FE JE0x4EC505、非NULLだけ0x4EC500 CALL0x432180。NULLならcleanup呼出を飛ばす。
- 0x432180実ASM: 0x432180 MOV EAX,[ESI]、0x432184 JE0x43218F（内部bufなし）。bufありなら0x432187 CALL0x5B6BBBで解放。0x43218F PUSH ESI、0x432190/196/19Dで+0/+4/+8を0化し、0x4321A4 CALL0x5B6BBBでholderも解放。つまりhash node消去に先立ちpayloadが所有する内部領域・holder自体の二段階解放を行う経路がある。
- 次に0x4EC510 CALL0x4EC5F0が同じキーのhash側eraseを担当する。0x4EC604〜0x4EC619は[begin,end)を単方向nextで走査して件数ESI++。0x4EC623 CALL0x4EC6C0で範囲削除、0x4EC629 MOV EAX,ESIで実削除件数を返却。
- 呼出元は0x4EC510の戻値を利用せず、0x4EC515以降で順序リストの先頭が非emptyなら先頭1ノードだけunlink/freeし、0x4EC536で順序件数を1減らす。hash eraseの件数と順序1件との一致は正常データの一意キー不変条件に依存する可能性があるが、合法運用で常に1件かはVERIFY。
- 0x4EC7E0 equal-range検索はhash bucket索引（0x4EC7E9 XOR key,0xDEADBEEF→0x4EC7F9 CALL0x5B7AC2）に加え、0x4EC854 JGE/0x4EC874 JLによってノード+8のキーをsigned比較し、同値連続範囲を[begin,end)で返す。Ghidraの推定型だけで同値重複・並べ替えの可否を断言しない。
- 0x4EC6C0は0x4EC6D0/0x4EC6D4で対象範囲がcontainer全域（先頭sentinel.nextからend sentinel）かを判定。全域なら0x4EC6D8 CALL0x4F4140、部分範囲なら0x4EC6EC〜0x4EC708で各ノードを0x4ECC30へ渡す。
- 0x4ECC30は対象node+8で同じhashを再計算し、0x4ECC88/8D/AA等でbucket先頭・末尾ポインタを補正、0x4ECCBF〜0x4ECCCDでnext/prevを連結し直してfree、0x4ECCD5 DEC [ESI+8]でhash件数減算。
- 全域用0x4F4140では0x4F4146/4B sentinel自己リンク、0x4F414F count=0、0x4F4163全旧node free、0x4F41AF bucket再初期化call、0x4F41B4 mask=7 / 0x4F41BB capacity=8。これは単なる1ノード削除と別の再初期化処理。

## 再現性・非重複・検証限界
- native raw SHA256: 0x4EC5F0/66B CD71A861A68EA8FA4AE6BCD5D67B4C3DBD066CBABF954A53078C19B2193A6703; 0x4EC7E0/203B F96BB5A854D4B03AD232A4A4321A9632C4F4C57EE52B2378087CF6F959BF2E6D; 0x4EC6C0/84B 74D68DF51F700EA64A4A6881E801461FF8A1B708CFCE082AD01BB1C3E5026BBD。
- native raw SHA256: 0x4ECC30/177B 443A12D06AA01F88AD2733BC17567A31DEDD6033EEB78ED71BF3E135A044E917; 0x432180/47B 4E0502B31A60AD610125345B9F544567B8A569DF9DC7A3E4322FF6A81735BFB6; 0x4F4140/130B 252CD62D0C2EBEDDFA0D5CC1A4AC90BA3005871E35F2AED335FA5B7FDDCAF61E。
- 原作CALL site: 0x4EC4F0→0x4EC720、0x4EC500→0x432180、0x4EC510→0x4EC5F0、0x4EC5FF→0x4EC7E0、0x4EC623→0x4EC6C0、0x4EC6D8→0x4F4140、0x4EC6FB→0x4ECC30、0x4ECCCD→0x5B6BBB、0x432187/0x4321A4→0x5B6BBB。原作Capstone逆ASMでCALL位置確認。前01Hのkey/8192閾値・hash lookup、00HのUnit経路列は既存で再計上0。
- 今回B owner T028/T012・直前詳細・HANDOFFに対する主要新規VA 0x4EC4F9/0x432180/0x4EC6D8/0x4ECC8D/0x4ECCCD/0x4EC629の事前直接literalヒット=0（対象4文書）。他lane/2026-10-25未同期全文を含む意味的全件照合はVERIFY。
- 推定payload本体の型、holder+0/+4/+8の正式意味、重複キー到達可能性、全域erase分岐の合法実機到達、例外時二重free/UAF不変条件はVERIFY。原作BUG認定しない。
- 合法Golden: 無改変EXE＋20倍強化前DAT＋同SAVE/MAP/input/RNGでroute cache hit/miss、同一・異キー、8192境界、長時間反復・全消去条件のhash件数/順序リスト件数/payload生存/Unit+186B0/翌tickを原作と新実装で比較。原作Gameplay PASS0、strict MATCH0、現在NOT RUN。

## 安全・復旧・再開点
- OTHER/RECOVERED: root\\targets一覧はNOT_FOUNDだったため、許可済み親フォルダのファイル名検索でゲーム直下Vahren.exeを同定して現物SHA確認。初回python -B -cはPowerShell引用符除去でNameError、同じLocal許可済read-only操作をPowerShell here-string標準入力に修正し原作ASM/SQLite照合に成功。安全拒否ではない。
- 新規正式B READY0、E MASTER統合0、Task DONE0、原作Gameplay Golden PASS0、strict MATCH0。原本EXE/DAT/SAVE/ZIP、他lane、REA/dev_lab、MASTER/Git/Work/設定/automationは書込なし。
- 次回: 0x4FC710のduplicate-insertフラグと0x4ED350の一時record lifetimeを読取専用で接続し、hash一意キー不変条件/record挿入失敗時rollbackを検証。次点はUnit+186B0 route consumer。拒否済み処理を迂回しない。