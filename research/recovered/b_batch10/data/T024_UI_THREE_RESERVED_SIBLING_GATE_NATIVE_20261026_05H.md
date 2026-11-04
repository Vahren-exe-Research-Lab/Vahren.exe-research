# B-20261026-0511-T024-UI-THREE-RESERVED-SIBLING-GATE-01 | T024 UI可変枠24と兄弟Unit描画フィルタの非対称
日時 2026-10-26 05時台 JST | 所有 B/T024 | STATIC-ORIGINAL-PE-ASM / INFERRED / VERIFY / NOT READY
## 接続・事前照合
Desktop Commander Local Compact ONLINE。MASTER既存checkpoint196/READY596、5レーン規約、B HANDOFF、T011/T012/T013/T024/T028現行、未同期回収索引・既安全拒否をread-only照合。旧14Hオフライン全文/他lane・Library等の完全ID意味統合は未完。
原作: rea_lab/targets/hakushin067_Vahren.exe 読取専用、実SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。旧search.sqlite SHA256 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF、URI mode=ro quick_check=ok。Ghidra/REA再解析・原作実行なし。
旧検索: python search.py function 0x41EF50 --max-chars 11500 --limit 1、元原作PEの限定Capstone ASM読取。旧Ghidra pseudoはSTATIC参考・実測ではない。
## 新規増分1：3枠を差し引く可変表示数上限
先行03H/04H既知: 0x41F0E2/0x41F0F5で表示管理総枠 N<=27、基数3。今回 0x41F5E6 LEA ESI,[EDX+3] → 0x41F5E9 CMP ESI,[0x65EB60] → 0x41F5EF JGE 0x41F76B、0x41F755 INC EDX、0x41F765 JB 0x41F5E2 のループ境界を原PE検査。
mode==0描画側で child_index+3 >= N なら停止。N<=27 だから追加子要素は高々24件、N=3なら0件。Nの27は「描画した子の件数27」ではない。0x41F3F4 CMP EDI,[0x65EB60]のmode!=0側も先頭カウンタ3から比較するため可変owner列挙枠は高々24。
厳密なUIの3固定枠の画面上の名称/使用法は未確定。N=27を戦闘Unit上限や同時攻撃候補27件と同一視しない。
## 新規増分2：先頭判定と後続描画の粒度が異なる
mode!=0描画列挙: 0x41F419 CMP [ECX+8C],0 と0x41F426 CMP [ECX+1F8],0 はownerごとの先頭Unit資格判定。そのownerが通ると0x41F45Bに子+1C8取得。arg!=0時はowner+1C gateも再適用。
mode==0描画の範囲 0x41F5AD..0x41F76B は全131命令を元PE ASM順に走査。0x41F5E9の総枠gate/0x41F5F5のchild index範囲gate後、0x41F601で各childポインタを取得し0x41F60Cで child+1C8 を直接読み、0x41F613 CALL 0x584970へ送る。兄弟の個々の+8C/+1F8再判定はこの区間に存在しない。
ゆえに最初のchildがeligibleなら後続childは資格フラグに関係なく表示用下位処理へ送られる構造。ただし表示下位関数のskip/NULL/描画実体は未追跡で、最終的に無効childが見える・クラッシュする等は確定しない（VERIFY）。
mode0空inner配列の危険経路と+1C8 alias/Nullの合法到達は02H〜04Hの既存VERIFYであり、新たな原作バグ認定はしない。
## 直接ASM出典・同一ソースの限定窓SHA
0x41F408..0x41F5AD (421B) 原作SHA256 05824A35BA69D9BB898C01DB5976D485C4B2CD68C0D762311DAF441297995A34、127命令。
0x41F5AD..0x41F76B (446B) 原作SHA256 CAC760EAB7862BE1A4EDA141AE4253CBA5E9268CA766E718ABF10330A9A376B0、131命令。両範囲とも命令終端が範囲末尾と一致。
コール位置0x41F613→0x584970 は元E8命令、意味は文字情報/描画用データ加工候補に留める。
## ID・所有・Golden・再開
先行 B-20261026-0417 のfirst-ownerとcount27、03Hのarg filter/NULL候補は重複計上0。本増分は「3固定基数→可変最大24」の描画消費側制約と「owner先頭gate対mode0兄弟個別gate無し」。本IDのB資料既存検索一致0、他レーン/14H未同期完全意味照合VERIFY。
無改変原作ver0.67・20倍強化前DAT・同SAVE/MAP/input/RNGでmode0/非0、owner1/複数、子数1/24/25、先頭と兄弟の+8C/+1F8差、表示実件数と次tickを合法条件で確認するまでGolden DESIGNED_NOT_RUN。Gameplay PASS0/strict MATCH0、新B READY0/E MASTER0/DONE0。
次P0: 0x584970/0x424C80/0x423D70の表示入力でchildの非対象状態がskipされるか、既存B内範囲でread-only callerを確認。生成側のinner nonempty不変条件も引き続きVERIFY。
既安全拒否（0x5710C0..0x571500ほか）を別tool/path/ZIP/Remoteで再試行・迂回0。MASTER/他lane/REA/dev_lab/元EXE/DAT/SAVE/Git/Work/設定/スケジュール変更0。
