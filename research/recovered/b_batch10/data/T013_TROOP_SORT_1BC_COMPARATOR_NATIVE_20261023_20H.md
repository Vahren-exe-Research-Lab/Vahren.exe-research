# T013｜Troop配置候補の比較関数 0x00567EC0：Unit+0x1BC signed昇順（20時台・独立静的解析）
研究ID: B-20261023-20H-T013-TROOP-SORT-1BC-NATIVE-01 / owner B:T013 / 関連T011（+0x1BC writer）。
状態: PC-CONNECTED / V9-STATIC / ORIGINAL-PE-ASM / INFERRED / VERIFY / NOT READY。
## 先行・安全・基盤
先読: MASTER cp196/既READY596（旧値、今回再集計なし）、ANALYSIS_LANES_PROTOCOL、LANE_B_HANDOFF、T011/T012/T013/T024/T028、未同期・安全拒否索引。
10月23日03～12時オフライン研究10件、02時Library訂正版、14:14保存拒否本文は未同期/未保存を維持し、再統合・拒否迂回はしない。
V9入口は 00_START_HERE_UNIFIED_V9_20261023.md。verify = V9_INDEPENDENT_READBACK_PASS、SQLite SHA256=2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE。PC標準V3は変更無し。
今回読取した原作targets/hakushin067_Vahren.exe 現物SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（一致）。原作実行0、新Ghidra/REA起動0。
## 新しい機械語証拠
V9 function 0x00567EC0 は NOT_FOUND（登録済み内部関数ではない）。しかし原作PEの同VAに実在し、0x00567ED9 RET、直後0x00567EDA～DF INT3 padding、その後0x00567EE0から別のコンストラクタが始まる。未登録独立callback候補。
原作ASM: 0x00567EC0 mov eax,[esp+4] / 0x00567EC4 mov ecx,[eax+0x1BC] / 0x00567ECA mov edx,[esp+8] / 0x00567ECE xor eax,eax。
続き: 0x00567ED0 cmp ecx,[edx+0x1BC] / 0x00567ED6 setl al / 0x00567ED9 ret。setl はsigned比較。戻りEAX=1 iff signed32(first->+0x1BC)<signed32(second->+0x1BC)、同値は0。
PE bytes VA 0x00567EC0..0x00567ED9: 8B4424048B88BC0100008B54240833C03B8ABC0100000F9CC0C3（現物読取）。
CALLER-1 ASM: 0x005697DA push 0x00567EC0 / 0x005697E5 call 0x0047BB50 / 0x005697EA add esp,0x10。
CALLER-2 ASM: 0x00569929 push 0x00567EC0 / 0x00569934 call 0x0047BB50 / 0x00569939 add esp,0x10。
V9 Ghidra擬似C: 0x00569730 と 0x00569880 はともに local_1C～local_18 の4byte Unit参照候補配列を 0x0047BB50（第4引数 comparator）で並べ替え、後続へ配送する。V9 E8索引は0x5697E5/0x569934→0x47BB50と一致。
V9 Ghidra擬似C: 0x0047BB50 は要素数<=32で 0x0044D6A0 挿入ソート、>32で 0x0047BCC0 partition等を使用。0x0044D6A0 は comparator(x,y)の真でxを前方へ移す。比較式からsigned +0x1BC昇順がSTATIC-DERIVED。全サイズで等値キーの安定順序は未保証。
## 既存B成果との関係
B-20261023-18H: 二経路の配置・ソート存在／B-20261023-1915: 候補生成とscratch寿命は再計上0。今回増分は未登録callbackの原本ASM特定、+0x1BC signed比較、2つの実push/call site、32件閾値のソート方式接続。
T011_DATA_MODEL §16 に Unit+0x1BC writer→0x587CC0系列の既存STATICがあるが、+0x1BC のゲーム内名称や実効値・更新時機は未確定。「移動速度順／隊列優先順」などと命名しない。Skill+0x1BC等の別型にも安易に流用しない。
## 再実装・Golden・次回
原作配列順、signed +0x1BC 比較、同値、負/零/正、候補0/1/2/3/32/33と死亡/flag除外を別軸にする。>32はソート安定性と実際の機会の有無をVERIFY。現時点で実ゲームの可視配送順とnative Unit参照同一性は未確認。
Golden条件: 同じ無改変原作EXE/DAT/SAVE/MAP/入力/seedでUnit参照・+0x1BC値・ソート前後配列・候補配送順を旧新比較。DESIGNED / NOT RUN、旧原作Gameplay PASS0、strict MATCH0。
残るP0: +0x1BC実際のwriter/型・ソート後とscratch pairの対応・同値安定性・mode+0x30の設定元・RNG消費、T024/T028への実接続。次はT013の許可済みUnit+0x1BC writerとTroop命令配送順を照合。
新規READY0、E MASTER統合0、Task DONE0。原本/MASTER/他owner/REA/dev_lab/Git/Work/設定/スケジュールの変更0。既安全拒否領域/既拒否XREFの再照会0。
