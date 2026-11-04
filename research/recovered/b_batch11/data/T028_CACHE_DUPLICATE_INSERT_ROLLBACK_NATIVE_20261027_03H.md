# B-20261027-03H-T028-CACHE-UNIQUE-INSERT-ROLLBACK-01｜経路cacheハッシュ一意挿入時の重複候補rollback
日時 2026-10-27 03H JST／owner B T028／STATIC-ORIGINAL-PE-ASM＋STATIC-GHIDRA／INFERRED/VERIFY／NOT READY
## Precheck・証拠源
- Desktop Commander Local Compactに接続。MASTER最終正式cp196/READY596（E既値）、LANE規約、B5資料、HANDOFF、未同期・拒否回収索引を先読。10/25 14Hオフライン全文と他laneの完全意味同期は未了。
- 旧README/BUILD_MANIFESTを読取。原本ゲーム直下Vahren.exe実SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187 (2910720B)。旧search.sqlite SHA0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF、独立V9 DB SHA2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE、いずれもimmutable read-only quick_check=ok。ACTIVE切替なし。
- 原本PEのCapstone限定disasm＋既存search.py function/callers。Ghidra/REA再実行・原本起動/改変なし。active.lock（検索indexとheadless root）なし、稼働プロセス一覧で新Ghidra/Java開始なし。
## 今回の独立差分（前02H cache erase一般APIの疑問を局所解決）
- 0x4EC4BD CALL0x4ED350：hashへの登録要求前、0x4ED360 CALL0x4EDFE0で16Bリンクノードを作成し、0x4ED37E〜0x4ED388で双方向リストへlink＋countを1増加。0x4ED38F/390でnode先頭+8のkey/record pointerとnode本体を渡し、0x4ED397 CALL0x4FC710でunique insertへ進む。
- 0x4FC790 MOV EBX,[EBX+4] → 0x4FC793 CMP [EBX+8],EAX（signed key比較）。0x4FC796 JLE0x4FC7D9；同所0x4FC7D9 JGE0x4FC7DF。両条件が成立する等値キーに専用duplicate branchが存在する。
- duplicate 0x4FC7DF〜0x4FC7E9：param4の「今回新規の一時ノード」を0x4FC920へ渡す。0x4FC92E..0x4FC93Bで双方向リンクを外し、0x4FC93E CALL0x5B6BBBで16Bノードをfree、0x4FC94Aでリスト件数を1減算。結果的に直前の一時node/count追加を戻す経路。
- 0x4FC7EE/0x4FC7F1：結果out[0]に既存一致ノードEBX、0x4FC7F3：out[+4] = 0（inserted=false）、0x4FC7FD RET0xC。対して新規キー登録は0x4FC829 CALL0x4FC850（bucket/update）、0x4FC836 out[0]=新node、0x4FC838 out[+4]=1、0x4FC840 RET0xC。
- 同hash bucket衝突と「キー自体の等値」は異なる。上記はキー等値専用rollbackで、単なるbucket衝突時に挿入を拒否するという証明ではない。0x4FC920が先頭sentinel自身ならfreeしない分岐0x4FC92A/0x4FC954あり。
- これにより前02Hの「hash equal-range erase複数件とorder1件減算に矛盾が生じるかも」という仮説のうち、この0x4ED350→0x4FC710という通常insert経路の同一キーhash重複蓄積懸念は緩和。一般0x4EC5F0 APIが複数消せること自体は既知・変更なし。
## 境界・新しいVERIFY
- 0x4EDFE0は8B記録をshallow copyするが、duplicate側0x4FC920の可視処理は16Bノードfreeのみ。新規path payload holderの所有権・解放、失敗/再入時の実到達、別caller 0x4FACA0/0x4FC850経由での同値重複可否はVERIFY。現時点でメモリリーク・二重解放などの原作BUG認定0。
- 0x4EC4BDの呼出元0x4EC1E0は戻値flagを直後に直接分岐させず0x4EC4CCで順序key登録へ進む。重複ケースが合法到達した際のcache/order整合性は別途VERIFY。実機観測0。
## 検証・重複・安全
- native E8 CALL 5/5一致：0x4EC4BD→4ED350、0x4ED360→4EDFE0、0x4ED397→4FC710、0x4FC7E9→4FC920、0x4FC829→4FC850。
- 原作PE固定窓 SHA256：4ED350/90B=577E04BCC308649FA924A23F885BC965889EAE3F60615877EB2A8B24898A1EF0、4FC790/112B=47B977AAA4AB9C09E79211906C7EBE2336216C700A5BE0ABE6707D49F86A85E4、4FC920/57B=26485F29FC7E5D93D2D69C70164035473DAEBA87472B6B0FC9307D6450FDE8F8。窓長を関数全長と混同しない。
- B T028/T012/HANDOFF内で0x4FC7E9/0x4FC920/0x4FC94Aの事前直接文字列一致0。旧01H threshold、02H erase、0H route listは再計上0。他lane・オフライン全文の意味的非重複はVERIFY。
- 初回PowerShell Select-Stringで配列パス結合に失敗（InvalidArgument/OTHER）。同等のread-only独立dedupをLocal Pythonで完了・RECOVERED。安全拒否ではない。禁止VA0x5710C0..0x571500/旧拒否ペイロードの再試行・迂回0。
## Golden / 状態 / 次
- 無改変EXE、X20前DAT、同一SAVE/MAP/input/RNGでcache hit/miss、鍵一致・hash bucket衝突・新規/既存flag・payload lifetime・order件数・8192境界とUnit+0x186B0経路を比較するまではDESIGNED_NOT_RUN。
- 新B READY0、E MASTER統合0、Task DONE0、旧原作Gameplay Golden PASS0、strict MATCH0。original code patch0、Git/Work/schedule/settings0。他lane・REA・dev_lab・EXE/ZIP/DAT/SAVE/MASTERの書込0。
- NEXT: 0x4FC710別caller 0x4FACA0におけるduplicate out flag用途と0x4EC4CC順序key追加の条件、0x4EC4BDで生成されたpath payload holderの未採用時の解放、実際のUnit+0x186B0の経路消費を限定照合。安全拒否領域は対象外。
