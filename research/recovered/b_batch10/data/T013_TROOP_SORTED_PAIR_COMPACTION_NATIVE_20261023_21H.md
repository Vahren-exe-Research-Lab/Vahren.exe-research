# T013｜Troop整列後のUnit走査と8-byte座標pair割当：2カウンタと候補不足gate（2026-10-23 21時台）
研究ID: B-20261023-21H-T013-SORTED-PAIR-COMPACTION-01
担当: B/T013。T011のUnit+0x1BC writerは既存参照のみ。状態: STATIC-PE-ASM / STATIC-V3 / INFERRED / VERIFY / NOT READY。

## 先読・安全・証拠源
Desktop Commander Local CompactでPC接続成功。MASTER cp196／正式READY596（既存値）、レーン規約、B HANDOFF、T011/T012/T013/T024/T028の担当資料、既拒否記録・未同期復旧を確認した。
03〜12時台オフライン研究10件、02時台Library訂正版2件はPC正式未同期、14:14詳細文書も拒否・未保存。既拒否操作（0x5710C0..0x571500、0x514C50、旧T024、旧0x5769B0のXREF等）への代替照会／迂回なし。
標準現行V3入口CURRENT_ACTIVE_RESEARCH_STATE_LATEST.jsonを確認。verify_active_research_state_v3_20261022.py（python -B、read-only）=PASS_ACTIVE_V3_STATIC、input_hashes_verified=14、machine_native_callers=44889、jumps=6324、errors=[]。旧search.sqliteはhistorical。
原作read-only: rea_lab/targets/hakushin067_Vahren.exe、実SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（今回現物再計算・一致）。pefile+Capstoneで指定3窓だけASMを独立照合、EXE起動・変更・Ghidra再解析なし。

## NEW 1：0x00569730の後段ではUnit走査と座標pair消費のordinalが独立
原作窓VA0x005697F5..0x0056983C SHA256=F925F9DC2CF55BA3DDB93D61E733F2FBCC598246FD2484CB8FE73F63B6B98E70（read-only実bytes）。
0x5697F5: mov eax,[ebx+ebp*4]：EBPで整列済みUnit pointer配列を参照。
0x5697F8: cmp byte [eax+0x1867C],0 / 0x5697FF jne 0x569838：状態不適格ならUnit走査だけ進む。
0x569801: cmp byte [esp+0x4C],0 / 0x569808: cmp byte [eax+0x1F9],0：追加flag有効時のみ+0x1F9非zeroを除外、同様に0x569838へ。
0x569811..0x56981C：別vector begin/endを取り、8byte strideで座標pair数を算出。
0x56981F cmp ecx,edi / 0x569821 jbe 0x56983D：座標pairの残数が無ければUnit走査を打ち切る。
0x569823 lea ecx,[edx+edi*8]：EDIがpair ordinal。0x569832 inc edi は配送CALL直前の適格経路だけ。0x569838 inc ebp は不適格を含む各Unit走査で増える。
よって一時的に不適格Unitが混在すると、Unit側indexだけ進む一方、座標pair indexは詰めて利用される静的制御フロー。元の候補indexとpair indexを常に一致させる実装は一致しない。

## NEW 2：0x00569880の後段は+0x1F9による追加除外がなく同じ2カウンタを使用
原作窓VA0x00569946..0x0056997A SHA256=D6285CC1946A29E394C28A6C6DD0AD276513B4373E7DC3044FCF9F1B100762BD。
0x569946 mov eax,[ebx+ebp*4] → 0x569949 cmp [eax+0x1867C],0 → 0x569950 jne 0x569976。
0x569952..0x56995D は別vectorを8byte単位で数え、0x569960 cmp ecx,edi / 0x569962 jbe 0x56997B で足切り。
0x569964 lea ecx,[edx+edi*8]、0x569970 inc edi（適格時）、0x569976 inc ebp（走査毎）。この窓には+0x1F9検査は無い。
2経路とも「sorted Unitsの第EBP番目」を見ながら「座標pairの第EDI番目」を使い、除外・不足によって2つの数え方が乖離する。CALL先0x5769B0は既拒否XREFとの境界であり内部、副作用、ABIは本run調査・証明しない。

## NEW 3：少数候補の同値キーは挿入ソート経路では順序維持
V3 Ghidra cached 0x0047BB50：候補数1以下で実sort無し、2..32件で0x0044D6A0を使用、33件以上は別partition処理を含む（他条件により分岐）。
原作窓VA0x0044D6A0..0x0044D726 SHA256=9BFC75D4C5C77738E8D5199A4B35499931BE2E4BB2260369E33A46A596AC706A。
0x44D6B5..0x44D6C2はcomparator(new,first)を評価、同値ならfalseで前挿入しない。0x44D6E5..0x44D712はcomparator(new,prev)がtrueの間だけ既存要素を右移動、等値なら停止。
既確認0x567EC0のsigned32(Unit+0x1BC) strict-< 比較を前提に、2..32件の同値キーは元の相対順序を保つ（STATIC-DERIVED）。33件以上の安定性、partitionの等値挙動はVERIFYであり一律stable sortと断定しない。

## 既存成果との非重複・実装上の拘束
既B-20261023-18H（2配送経路と状態フィルタ）、19H（0x5699C0とscratch）、20H（0x567EC0 signed comparatorと<=32分岐）は再計上0。
本IDの追加分は、原作ASMで示したEBP/EDI独立更新、pair不足時break、2ループのflag差、および<=32同値順の限定的安定性。T011 §16の+0x1BC writer、T013原本内の他XREFは今回新規成果に算入しない。
効果配送先への呼出しの存在だけを採録し、既安全拒否範囲の内容を推定しない。Ghidraの暗黙引数プロトタイプは未検証。原作内での実移動・合法AI意思決定・RNG消費・座標vector生成時点での除外と配送直前の除外が実際に相違するかはVERIFY。
REIMPLEMENT: sorted Unit pointer indexと位置pair ordinalを別変数にすること。配送側で不適格Unitはpairを消費しない。pairが尽きたら後続Unitには配送しない。挿入ソート(2..32)の同値順を保持。実装確定は追加の呼出時ABI・Golden後。

## Golden／未解明P0
条件設計（DESIGNED / NOT RUN）: 同一無改変原作EXE/DAT/SAVE/MAP/input/seed/capture SHAで、Unit+0x1BCキーの同値／負零正、整列済みUnit数2/3/32/33、Unit+0x1867C適格／不適格、+0x1F9=0/1と分岐flag=0/1、座標pair数0/1/2/3を直交比較。原作側のsorted pointer配列、EBP/EDI更新、候補pair、最終移動可視位置を同一runで観測。0x5699C0生成数・元Unit state変化のタイミングは未確定。
次回優先: T013で生成pair数を規定するTroop+0x30 writer/+0x38 setterと、元Unit+0x1BC writer→実sorted ordinalのクロスジョイン。0x5769B0の既拒否XREFは対象外。T011/T012/T024/T028のP0はこの成果だけで解消しない。
旧原作Gameplay Golden PASS=0、strict MATCH=0、新正式READY=0、MASTER統合=0、Task DONE増分=0。B限定STATIC成果・NOT READY。
